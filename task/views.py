import random
from ninja import Router
from .models import Task
from .schema import *
from user.schema import Message
from django.contrib.auth.models import User

task_api = Router(tags=["Task"])

@task_api.get('', response={200: List[TaskOutSchema]})
async def tasks(request):
    user = request.auth
    print(user)
    tasks = [task async for task in Task.objects.filter(assigned_to=user)]
    return 200, tasks

@task_api.put('{id}', response={201: Message, 404: Message, 405: Message, 406: Message})
async def complete_task(request, id, data: CompleteTaskSchema):
    if await Task.objects.filter(id=id).aexists():
        task = await Task.objects.aget(id=id)
        if task.status != "completed":
            if task.status != data.status:
                task.status = data.status
                if data.status == "completed":
                    task.report = data.report
                    task.worked_hour = data.worked_hour
                await task.asave()
                return 201, {"message": "Task updated succesfully"}
            return 405, {"message": f"Task is already marked as {data.status}"}
        return 406, {"message": f"Task is already completed"}
    return 404, {"message": "Task not found"}

@task_api.get('{id}/report', response={200: TaskReportSchema})
async def task_report(request, id):
    if await Task.objects.filter(id=id).aexists():
        task = await Task.objects.aget(id=id)
        if task.status != 'completed':
            return 405, {"message": "Task not completed yet"}
        return 200, {"id": task.id, "report": task.report, "worked_hour": task.worked_hour}
    return 404, {"message": "Task not found"}
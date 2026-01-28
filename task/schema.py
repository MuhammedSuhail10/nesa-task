from ninja import Schema
from typing import *
from datetime import date

class TaskOutSchema(Schema):
    id: int
    title: str
    description: str
    due_date: date
    status: str

class CompleteTaskSchema(Schema):
    status: str
    report: Optional[str]
    worked_hour: Optional[int]

class TaskReportSchema(Schema):
    id: int
    report: str
    worked_hour: int
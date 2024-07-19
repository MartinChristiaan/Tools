from dataclasses import dataclass
from datetime import datetime


@dataclass
class GoogleTask:
    id: str
    title: str
    updated: str
    status: str
    links: list = None

    @staticmethod
    def generate_from_api(task: dict):
        return GoogleTask(
            task["id"], task["title"], task["updated"], task["status"], task["links"]
        )

    def __repr__(self) -> str:
        return (
            f" - [ ]{self.title}"
            if self.status == "needsAction"
            else f" - [x]{self.title}"
        )

    @staticmethod
    def parse_from_string(string: str, title_task_lut: dict):
        if string.startswith(" - [ ]"):
            status = "needsAction"
            title = string[6:]
        elif string.startswith(" - [x]"):
            status = "completed"
            title = string[6:]
        else:
            raise ValueError("String must start with ' - [ ]' or ' - [x]'")
        if title in title_task_lut:
            task = title_task_lut[title]
            task.status = status
            return task
        current_time_in_google_format = datetime.utcnow().isoformat() + "Z"
        return GoogleTask(None, title, current_time_in_google_format, status, None)

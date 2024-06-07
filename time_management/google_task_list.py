# %%
import pickle
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List

from google_task import GoogleTask

# %%

basedir = Path(__file__).parent

@dataclass
class GoogleTaskList:
    id: str
    title: str
    updated: str
    tasks: List[GoogleTask]

    def find_added_tasks(self, other: "GoogleTaskList") -> List[GoogleTask]:
        tasks_to_add = []
        title_task_lut = {task.title: task for task in other.tasks}
        for task in self.tasks:
            if task.title not in title_task_lut:
                tasks_to_add.append(TaskModification(task, self, Modication.ADDED))
        return tasks_to_add

    def find_removed_tasks(self, other: "GoogleTaskList") -> List[GoogleTask]:
        tasks_to_remove = []
        title_task_lut = {task.title: task for task in self.tasks}
        for task in other.tasks:
            if task.title not in title_task_lut:
                tasks_to_remove.append(TaskModification(task, self, Modication.REMOVED))
        return tasks_to_remove

    def find_modified_tasks(self, other: "GoogleTaskList") -> List[GoogleTask]:
        tasks_to_modify = []
        title_task_lut = {task.title: task for task in other.tasks}
        for task in self.tasks:
            if (
                task.title in title_task_lut
                and task.status != title_task_lut[task.title].status
            ):
                tasks_to_modify.append(TaskModification(task, self, Modication.UPDATED))
        return tasks_to_modify

    @staticmethod
    def generate_from_json(service, tasklist: dict):
        tasks_results = service.tasks().list(tasklist=tasklist["id"]).execute()
        tasks = [
            GoogleTask.generate_from_api(x) for x in tasks_results.get("items", [])
        ]
        return GoogleTaskList(
            tasklist["id"], tasklist["title"], tasklist["updated"], tasks
        )

    def __repr__(self) -> str:
        return f"**{self.title}**\n" + "\n".join([repr(x) for x in self.tasks])

    @staticmethod
    def parse_from_string(string: str, title_tasklist_lut: dict):
        lines = string.split("\n")
        title = lines[0].strip().replace("**", "")
        title_task_lut = {}
        tasklist = None
        if title in title_tasklist_lut:
            tasklist = title_tasklist_lut[title]
            title_task_lut = {task.title: task for task in tasklist.tasks}

        tasks = []
        for line in lines[1:]:
            if line.startswith(" - [ ]") or line.startswith(" - [x]"):
                tasks.append(GoogleTask.parse_from_string(line, title_task_lut))
        if tasklist is None:
            return GoogleTaskList(None, title, None, tasks)
        else:
            tasklist.tasks = tasks
            return tasklist

    @staticmethod
    def read_pickle() -> List["GoogleTaskList"]:
        with open(f"{basedir}/tasklists.pkl", "rb") as f:
            return pickle.load(f)

    @staticmethod
    def write_pickle(tasklists: List["GoogleTaskList"]):
        with open(f"{basedir}/tasklists.pkl", "wb") as f:
            pickle.dump(tasklists, f)

    @staticmethod
    def read_tasklists_from_markdown(
        markdown_file="tasks.md",
        recent_tasklists: List["GoogleTaskList"] = None,
    ) -> List["GoogleTaskList"]:
        with open(markdown_file, "r") as f:
            lines = f.readlines()
        title_tasklist_lut = {}
        if recent_tasklists is not None:
            for tasklist in recent_tasklists:
                title_tasklist_lut[tasklist.title] = tasklist

        tasklists = []
        header_line_indices = [
            i for i, line in enumerate(lines) if line.startswith("**")
        ]
        for start_idx, stop_idx in zip(
            header_line_indices, header_line_indices[1:] + [len(lines)]
        ):
            text = "\n".join(lines[start_idx:stop_idx])
            tasklist = GoogleTaskList.parse_from_string(text, title_tasklist_lut)
            tasklists.append(tasklist)
            title_tasklist_lut[tasklist.title] = tasklist
        return tasklists

    @staticmethod
    def write_tasklists_to_markdown(
        tasklists: List["GoogleTaskList"], markdown_file="tasks.md"
    ):
        md_string = ""
        for tasklist in tasklists:
            print(str(tasklist), tasklist.tasks)
            md_string += str(tasklist) + "\n"
        with open(markdown_file, "w") as f:
            f.write(md_string)

    @staticmethod
    def read_from_api() -> List["GoogleTaskList"]:
        from auth import authenticate
        from google.oauth2.credentials import Credentials
        from google_task_list import GoogleTaskList
        from googleapiclient.discovery import build

        creds = authenticate()
        service = build("tasks", "v1", credentials=creds)
        results = service.tasklists().list(maxResults=10).execute()
        task_lists = [
            GoogleTaskList.generate_from_json(service, t) for t in results["items"]
        ]
        return task_lists


class Modication(Enum):
    ADDED = "ADDED"
    REMOVED = "REMOVED"
    UPDATED = "UPDATED"


@dataclass
class TaskModification:
    task: GoogleTask
    tasklist: GoogleTaskList
    modification: Modication

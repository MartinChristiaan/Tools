# Lists tasks from google tasks

# load credentials
# %%
from auth import authenticate
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.pickle.


# tasklist example
# {'kind': 'tasks#taskList',
#  'id': 'S2V6d3FFYkxrZDlGNWtUMA',
#  'etag': '"MjQ3Nzk2NDU2"',
#  'title': 'KCP',
#  'updated': '2023-05-12T07:02:56.577Z',
#  'selfLink': 'https://www.googleapis.com/tasks/v1/users/@me/lists/S2V6d3FFYkxrZDlGNWtUMA'},
class TaskList:
    def __init__(self, id, title, updated):
        self.id = id
        self.title = title
        self.updated = updated


creds = authenticate()
service = build("tasks", "v1", credentials=creds)
results = service.tasklists().list(maxResults=10).execute()
# %%
tasklists = results.get("items", [])
parsed_tasklists = []
for tasklist in tasklists:
    parsed_tasklists = TaskList(tasklist["id"], tasklist["title"], tasklist["updated"])


# with open("tasks.md", "w") as file:
# file.write("#Tasks:\n")
# %%
for tasklist in tasklists:
    # Call the Tasks API for each tasklist
    tasks_results = service.tasks().list(tasklist=tasklist["id"]).execute()
    tasks = tasks_results.get("items", [])

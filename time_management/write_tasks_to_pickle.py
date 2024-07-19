# Lists tasks from google tasks

# load credentials
# %%
import pickle

from google_task import GoogleTask


def read_from_api():
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


# write to pickle
with open("tasklists.pkl", "wb") as f:
    pickle.dump(task_lists, f)

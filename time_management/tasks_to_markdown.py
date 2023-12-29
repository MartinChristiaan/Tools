# reads pickle file and converts tasklists to markdown

from google_task import GoogleTask
from google_task_list import GoogleTaskList

tasklist = GoogleTaskList.read_pickle()
GoogleTaskList.write_tasklists_to_markdown(tasklist)

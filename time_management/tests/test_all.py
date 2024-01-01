# %%
# %load_ext autoreload
# %autoreload 2
from cv2 import add
from google_task_list import GoogleTaskList
from icecream import ic


def test_api_to_pickle():
    tasklist = GoogleTaskList.read_from_api()
    GoogleTaskList.write_pickle(tasklist)
    assert True


def test_pickle_to_markdown():
    print("writing")
    tasklist = GoogleTaskList.read_pickle()
    GoogleTaskList.write_tasklists_to_markdown(tasklist)
    assert True


def test_markdown_read():
    GoogleTaskList.read_tasklists_from_markdown()
    assert True


def test_no_modification_after_markdown_to_pickle():
    tasklists2 = GoogleTaskList.read_pickle()
    tasklists = GoogleTaskList.read_tasklists_from_markdown()

    # %%

    for tasklist in tasklists:
        tasklist_to_compare = [t for t in tasklists2 if t.title == tasklist.title][0]

        # print(tasklist.tasks[0].title== tasklist_to_compare.tasks[0].title)
        tasklist.find_added_tasks(tasklist_to_compare)
        tasklist.find_removed_tasks(tasklist_to_compare)
        tasklist.find_modified_tasks(tasklist_to_compare)

        assert tasklist.find_added_tasks(tasklist_to_compare) == []
        assert tasklist.find_removed_tasks(tasklist_to_compare) == []
        assert tasklist.find_modified_tasks(tasklist_to_compare) == []


# if __name__ == "__main__":
# 	te
#     test_pickle_to_markdown()
# test_markdown_read(kkkkkk
# test_no_modification_after_markdown_to_pickle()
# test_no_modification_after_markdown_to_pickle()
# %%

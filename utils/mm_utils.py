from media_manager.core import MediaManager


def get_result_options(mm: MediaManager):
    result_options = set()
    for video_info in mm._video_infos:
        result_dirpath_parts = len(video_info.result_dirpath.parts)
        results = video_info.result_dirpath.glob("**/*.csv")
        for x in results:
            result_item = "/".join(x.parts[result_dirpath_parts:])
            result_options.add(result_item)

    result_options = list(result_options)

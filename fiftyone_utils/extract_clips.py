""" 
Split video clips to deal with bug in FiftyOne when loading videos with a large amount of labels/detections
https://github.com/voxel51/fiftyone/issues/1607
"""
import os

import fiftyone.utils.video as fouv
from fiftyone import ViewField as F
import cv2


def extract_clips(sample_collection, clips, clips_dir):
    """Creates a new dataset that contains one sample per video clip defined by
    the given ``clips`` argument.

    Each sample in the output dataset will contain all sample-level fields of
    the source sample, together with any frame labels for the specified clip
    range.

    The specified segment(s) of each video file are extracted via
    :func:`fiftyone.utils.video.extract_clip`.

    Args:
        sample_collection: a :class:`fiftyone.core.collections.SampleCollection`
        clips: the clips to extract, in either of the following formats:

            -   a list of ``[(first1, last1), (first2, last2), ...]`` lists
                defining the frame numbers of the clips to extract from each
                sample in ``sample_collection``
            -   a dict mapping sample IDs to
                ``[(first1, last1), (first2, last2), ...]`` lists

        clips_dir: a directory in which to write the extracted clips

    Returns:
        a :class:`fiftyone.core.dataset.Dataset`
    """
    if isinstance(clips, dict):
        sample_ids, clips = zip(*clips.items())
        sample_collection = sample_collection.select(sample_ids, ordered=True)

    # Create a new dataset containing the clip's labels
    new_dataset_name = f"{sample_collection.name}_clips"
    dataset = (
        sample_collection
        .to_clips(clips)
        .set_field(
            "frames.frame_number",
            F("frame_number") - F("$support")[0] + 1,
        )
        .exclude_fields("_sample_id", _allow_missing=True)
    ).clone(new_dataset_name)

    # Extract the video clips and update the dataset's filepaths
    for sample in dataset.select_fields("support").iter_samples(progress=True):
        video_path = sample.filepath
        root, ext = os.path.splitext(os.path.basename(video_path))
        clip_name = "%s-clip-%d-%d%s" % (
            root,
            sample.support[0],
            sample.support[1],
            ext,
        )
        clip_path = os.path.join(clips_dir, clip_name)

        if os.path.exists(clip_path):
            continue

        fouv.extract_clip(video_path, clip_path, support=sample.support)

        sample.filepath = clip_path
        sample.save()

    # Cleanup
    # dataset._set_metadata("video")
    dataset.compute_metadata(overwrite=True)
    dataset.delete_sample_fields(["sample_id", "support"])

    return dataset

def split_vid_datasets(dataset, split_size):
    """Splits a video dataset into multiple datasets, one for each video clip.
    """
    clips = {}
    for sample in dataset:
        clips[sample.id] = []
        # Get number of frames in video
        cap = cv2.VideoCapture(sample.filepath)
        num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Split frames based on split_size
        for i in range(0, num_frames, split_size):
            add_size = min(split_size, num_frames - i)
            clips[sample.id].append((i+1, i + add_size))

    clips_path = os.path.dirname(dataset.head(1)[0].filepath)
    clips_dataset = extract_clips(dataset, clips, clips_path)
    return clips_dataset
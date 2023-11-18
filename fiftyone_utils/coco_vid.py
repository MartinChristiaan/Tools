import fiftyone as fo
import fiftyone.utils.coco as fouc
import fiftyone.core.labels as fol
import fiftyone.core.metadata as fom
import fiftyone.utils.data as foud
from pathlib import Path
import imageio
from tqdm import tqdm
import json
import numpy as np
from PIL import Image
import cv2

Image.MAX_IMAGE_PIXELS=None

class COCOtoVidDetectionDatasetExporter:
    def __init__(self, export_dir, image_format="jpg", export_media=None):
        self.export_dir = Path(export_dir)
        self.labels_path = self.export_dir / "labels.json"
        self.data_path  = self.export_dir / "data"

        if export_media is None:
            export_media = True

        self._media_exporter = foud.ImageExporter(
            export_media,
            export_path=self.data_path,
            default_ext=image_format,
        )

    def export_dataset(self, dataset, classes=[], vid_name="vid"):
        self._media_exporter.setup()
        data = {"categories": [], "images": [], "annotations": [], "videos": []}

        data['videos'].append({
            "id": 0,
            "name": vid_name,
        })
        ann_counter = 0
        for frame_idx, sample in enumerate(dataset):
            output_file = Path(vid_name) / f"{vid_name}_{str(frame_idx).zfill(6)}.jpg"
            self._media_exporter.export(sample.filepath, self.data_path / output_file)
            width, height = sample.metadata.width, sample.metadata.height
            data['images'].append({
                "id": frame_idx,
                "frame_id": frame_idx,
                "video_id": 0,
                "file_name": str(output_file),
                "width": width,
                "height": height,
            })

            for detection in sample.ground_truth.detections:
                if detection.label not in classes:
                    classes.append(detection.label)
                # print(detection)
                bbox = list(detection.bounding_box)
                
                data['annotations'].append({
                    "id": ann_counter,
                    "instance_id": int(detection.index) if detection.index is not None else -1,
                    "frame_id": frame_idx,
                    "image_id": frame_idx,
                    "video_id": 0,
                    "category_id": classes.index(detection.label),
                    "bbox": [bbox[0]*width, bbox[1]*height, bbox[2]*width, bbox[3]*height],
                    "area": bbox[2]*width * bbox[3]*height,
                    "iscrowd": 0
                })
                ann_counter += 1

        for cat_id, cat in enumerate(classes):
            data['categories'].append({
                "id": cat_id,
                "name": cat,
                "supercategory": cat
            })

        with open(self.labels_path, 'w') as f:
            json.dump(data, f)



class COCOVidDetectionDatasetImporter(fouc.COCODetectionDatasetImporter):
    def __init__(self, dataset_dir, max_samples=None, as_video=False, vid_fps=30, calculate_bbox_stats=False):
        self.as_video = as_video
        self.vid_fps = vid_fps
        self.max_samples = max_samples
        self.calculate_bbox_stats = calculate_bbox_stats

        self.data_path = Path(dataset_dir) / "data"
        self.labels_path = Path(dataset_dir) / "labels.json"
        self.videos_path = Path(dataset_dir) / "videos"

        self.sample_paths = None
        self.sample_ids = None
        self.sample_labels = None

    def get_dataset(self, name=None):
        data = load_json(self.labels_path)

        if self.as_video:
            generate_vids(data, self.data_path, self.videos_path, fps=self.vid_fps)
        
        dataset = fo.Dataset(name=name)

        video_data = data["videos"]
        if self.max_samples is not None:
            max_samples = min(self.max_samples, len(video_data))
            video_data = video_data[:max_samples]

        vid_frames = {vid['id']: [] for vid in video_data}
        vid_frames[-1] = []
        for img in data['images']:
            if 'video_id' not in img or 'frame_id' not in img:
                img['video_id'] = -1
                img['frame_id'] = -1
            vid_frames[img['video_id']].append(img)

        # sort video frames
        for vid_id, frames in vid_frames.items():
            vid_frames[vid_id] = sorted(frames, key=lambda x: x['frame_id'])

        frame_anns = {img['id']: [] for img in data['images']}
        for ann in data['annotations']:
            try:
                frame_anns[ann['image_id']].append(ann)
            except KeyError:
                continue

        cat_id_to_name = {cat['id']: cat['name'] for cat in data['categories']}

        if self.as_video:
            samples = parse_anns_as_videos(video_data, self.videos_path, vid_frames, frame_anns, cat_id_to_name, self.calculate_bbox_stats)
        else:
            samples = parse_anns_as_imgs(data['images'], self.data_path, frame_anns, cat_id_to_name)


        dataset.add_samples(samples)
        # print([cat['name'] for cat in data['categories']])
        dataset.default_classes = [cat['name'] for cat in data['categories']]
        
        dataset.save()

        return dataset

    @staticmethod
    def get_frame_id_to_vid_id(dataset):
        frame_id_to_vid_id = {}
        for sample in dataset:
            for frame in sample.frames:
                frame_id_to_vid_id[sample.frames[frame].image_id] = sample.id
        return frame_id_to_vid_id

    @staticmethod
    def add_coco_labels(dataset, labels, name):
        sample_ids = {}
        for sample in dataset:
            sample_ids[sample.video_id] = sample.id
            # print(sample)
        
        frame_id_to_vid_id = COCOVidDetectionDatasetImporter.get_frame_id_to_vid_id(dataset)

        frame_labels = {}
        for label in tqdm(labels):
            im_id = label['image_id']
            # print(label)
            width = dataset[frame_id_to_vid_id[label['image_id']]].metadata.frame_width
            height = dataset[frame_id_to_vid_id[label['image_id']]].metadata.frame_height
            attrs = label.copy()
            for key in ['bbox', 'score']:
                del attrs[key] 
            
            cat = dataset.default_classes[label['category_id']] if len(dataset.default_classes) > label['category_id'] else str(label['category_id'])
            bbox = [label['bbox'][0] / width, label['bbox'][1] / height, label['bbox'][2] / width, label['bbox'][3] / height]
            detection = fo.Detection(
                label=cat, bounding_box=bbox, confidence=label['score'], **attrs
                )
            if im_id not in frame_labels:
                frame_labels[im_id] = [detection]
            else:
                frame_labels[im_id].append(detection)
        
        for sample in dataset:
            for frame in tqdm(sample.frames):
                found_labels = frame_labels.get(sample.frames[frame]['image_id'], [])
                sample.frames[frame][name] = fo.Detections(detections=found_labels)
            sample.save()

        dataset.save()
        

def parse_anns_as_imgs(img_data, data_path, frame_anns, cat_id_to_name):
    samples = []
   
    
    for img in img_data:
        sample = fo.Sample(filepath=data_path / img['file_name'])
        width = img['width']
        height = img['height']

        detections = []
        for ann in frame_anns[img['id']]:
            bbox = [ann['bbox'][0] / width, ann['bbox'][1] / height, ann['bbox'][2] / width, ann['bbox'][3] / height]
            attrs = ann.copy()
            for key in ['bbox', 'id']:
                del attrs[key] 
                
            detections.append(
                fo.Detection(label=cat_id_to_name[ann['category_id']], bounding_box=bbox, **attrs)
            )
        sample['ground_truth'] = fo.Detections(detections=detections)
        sample['metadata'] = fo.ImageMetadata(width=width, height=height)
        samples.append(sample)

    return samples

def parse_anns_as_videos(video_data, videos_path, vid_frames, frame_anns, cat_id_to_name, calculate_bbox_stats=False):
    samples = []
    width, height = None, None
    for vid in tqdm(video_data):
        sample = fo.Sample(filepath=videos_path / f"{vid['name']}.mp4")
        for new_frame_id, img in enumerate(vid_frames[vid['id']]):
            frame = fo.Frame()
            width = img['width']
            height = img['height']

            detections = []
            for ann in frame_anns[img['id']]:
                bbox_stats = {}
                bbox = [ann['bbox'][0] / width, ann['bbox'][1] / height, ann['bbox'][2] / width, ann['bbox'][3] / height]
                index = ann.get('instance_id', None)
                if index is None:
                    index = ann.get('sequence_id', None)

                if calculate_bbox_stats:
                    bbox_stats['width'] = ann['bbox'][2]
                    bbox_stats['height'] = ann['bbox'][3]
                    bbox_stats['area'] = ann['bbox'][2] * ann['bbox'][3]
                detections.append(
                    fo.Detection(label=cat_id_to_name[ann['category_id']], bounding_box=bbox, index=index, **bbox_stats)
                )
            frame['ground_truth'] = fo.Detections(detections=detections)
            frame['metadata'] = fo.ImageMetadata(width=width, height=height)
            frame['image_id'] = img['id']
            frame['frame_id'] = img['frame_id']
            frame['video_id'] = img['video_id']
            sample.frames[new_frame_id+1] = frame
        
        sample['metadata'] = fo.VideoMetadata(frame_width=width, frame_height=height)
        sample['video_id'] = vid['id']
        samples.append(sample)

    return samples


def load_json(annotation_file):
    with open(annotation_file) as f:
        data = json.load(f)
    return data

def parse_coco_vid_annotations(data):
    vid_frames = {vid['id']: [] for vid in data['videos']}
    for ann in data['annotations']:
        if 'video_id' not in vid_frames:
            ann['video_id'] = -1
        vid_frames[ann['video_id']].append(ann)

    return vid_frames

    

def generate_vids(data, image_dir, video_dir, fps=2):
    vid_writer_kwargs = {
        'macro_block_size': None,
    }

    print(f"Generating videos to {video_dir} with fps={fps}")

    Path(video_dir).mkdir(parents=True, exist_ok=True)

    vid_frames = {vid['id']: [] for vid in data['videos']}
    vid_frames[-1] = []
    for img in data['images']:
        if 'video_id' not in img:
            img['video_id'] = -1
        vid_frames[img['video_id']].append(image_dir / img['file_name'])
    
    # sort video frames by file name
    for vid_id, frames in vid_frames.items():
        vid_frames[vid_id] = sorted(frames, key=lambda x: x.name)

    for vid in tqdm(data['videos'], desc='Generating videos'):
        vid_file = video_dir / f"{vid['name']}.mp4"
        if not vid_file.exists():
            writer = imageio.get_writer(vid_file, fps=fps, **vid_writer_kwargs)
            for filename in tqdm(vid_frames[vid['id']], desc=f"Writing {vid['name']}", leave=False):
                image = cv2.imread(str(filename))
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                pad = [(0, size % 2) for size in image.shape[:2]] + [(0, 0)]
                image = np.pad(image, pad)
                writer.append_data(image)
            writer.close()


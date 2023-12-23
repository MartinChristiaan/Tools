from dataclasses import dataclass


@dataclass
class ProcessingConfig:
    video_dir: str
    root_annotation: str
    local_path: str
    annotations_file: str
    dataset_name: str
    suffix: str
    downscale: int
    flip: int
    subdivide_x: int
    subdivide_y: int
    tile_data: str
    sample: int
    ds_blur_kernel: int
    ds_blur_sigma: int
    ir_mode: int


# @dataclass
# class ClipConfig(VideoConfig):
# 	start_timestamp:float
# 	end_timestamp:float
# 	x1:int
# 	y1:int
# 	x2:int
# 	y2:int
# 	identifier:str
# 	video_index:int
# 	valid_clip:bool

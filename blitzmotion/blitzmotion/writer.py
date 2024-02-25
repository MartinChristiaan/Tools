# estimator_bwd = MotionEstimator()
# estimator_fwd = MotionEstimator()
# estimators = [MotionEstimator(), MotionEstimator()]


from typing import List

import cv2
import pip
from dlutils_ii import DatasetConfig
from loguru import logger
from tqdm import tqdm

from blitzmotion.estimation import MotionEstimator, OutSadComputer
from blitzmotion.refinement import HierarchicalMotionEstimator, MotionEstimator
from blitzmotion.upscaling import nearest_neighbours_upscale, triple_median
from blitzmotion.vizualization import flow_to_color, get_mixing_image


class MotionSADWriter:
    def __init__(
        self, frame_offset: int, config=DatasetConfig, write_output=False
    ) -> None:
        """
        Class for writing SAD images to disk for training with TYOLO. Uses dlutils.
        """
        self.frame_offset = frame_offset
        self.estimator = HierarchicalMotionEstimator()
        self.sad_computer = OutSadComputer()
        self.config = config
        self.refiner = MotionEstimator()
        self.write_output = write_output

    def _write_sad(self, image, timestamp):
        if not self.write_output:
            return
        pathfinder = self.config.pathfinder
        path = pathfinder.frame_filename(self.frame_offset * 10, timestamp)
        cv2.imwrite(path, image)

    def process(
        self,
        frame_center,
        frame_offset,
        timestamp,
        apply_triple_median=False,
        refine=True,
    ):
        sad = None

        mvf, sad = self.estimator.estimate(frame_center, frame_offset, refine=refine)
        if apply_triple_median:
            mvf_hr = triple_median(mvf)
        else:
            mvf[0] = cv2.medianBlur(mvf[0], 3)
            mvf[1] = cv2.medianBlur(mvf[1], 3)
            mvf_hr = nearest_neighbours_upscale(mvf)
        sad = self.sad_computer.compute_out_sad(mvf_hr, frame_center, frame_offset)
        self._write_sad(sad, timestamp)
        return sad

    @staticmethod
    def export(config: DatasetConfig):
        from dlutils_ii import CacheReader

        try:
            for offset_scale in config.options.offset_scales:
                reader = CacheReader(
                    config, [0, int(-15 * offset_scale), int(15 * offset_scale)]
                )
                pipelines = [
                    MotionSADWriter(int(15 * offset_scale), config, True),
                    MotionSADWriter(int(-15 * offset_scale), config, True),
                ]
                for i in tqdm(range(len(reader))):
                    frames, annotations = reader.read(i)
                    frames = [
                        cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) for frame in frames
                    ]
                    t = annotations.timestamp[0]
                    pipelines[0].process(frames[0], frames[2], t)
                    pipelines[1].process(frames[0], frames[1], t)
            return True
        except Exception as e:
            logger.error(f"Error in {config.pathfinder.name}: {e}")
            return False

    @staticmethod
    def export_multiprocessed(configs: List[DatasetConfig], num_processes=6):
        import logging
        from multiprocessing import Pool

        logging.getLogger("numba").setLevel(logging.WARNING)
        with Pool(num_processes) as p:
            results = p.map(MotionSADWriter.export, configs)
        for x, config in zip(results, configs):
            if not x:
                logger.error(f"failed to process {config.pathfinder.name}")
            else:
                logger.info(f"Successfully processed {config.pathfinder.name}")


import numpy as np

path = "/media/martin/DeepLearning/mantis_drone_2023/raw/mantis_drone_2023/DJI_202309101443_008_wide_hd/0/1694357059368.jpg"
if __name__ == "__main__":
    frame = cv2.imread(path, 0)
    frame0 = np.zeros_like(frame)
    pipeline = MotionSADWriter(config=None)
    pipeline.process(frame0, frame, 0)
    from viztracer import VizTracer

    # tracer = VizTracer()
    # tracer.start()
    for j in tqdm(range(400)):
        pipeline.process(frame0, frame, j)
    # tracer.stop()
    # tracer.save("pipeline.json")
    # os.system("vizviewer pipeline.json")

    # frame1 = np.zeros_like(frame)

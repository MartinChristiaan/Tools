import dlutils_ii as du
from engine_utils.engine_utils import AbstractEngine
from motiontoolbox.estimators import ransac
from motiontoolbox.motionmodels import MotionModel, MotionModels
from motiontoolbox.motionvectors import CalcMotionVectorsOpticalFlowOpenCV
from motiontoolbox.warping import warp_image


class MotionModelComputer(AbstractEngine):
    def __init__(self, parameter1=0, parameter2=2.0):
        super().__init__()
        self._config["parameter1"] = parameter1


def compute_motion_model(t0, t1, frame, frame_target, max_iters=250):
    dpos = 20
    motionvectors = CalcMotionVectorsOpticalFlowOpenCV(frame, frame_target, dpos=dpos)
    motionmodel, _, _, _ = ransac(motionvectors, model="projective", maxiters=max_iters)
    return MotionModel(t0, t1, motionmodel)


def process_sequence(pf: du.Pathfinder):
    pf.media_manager

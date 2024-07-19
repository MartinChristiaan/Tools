from example.datasets import get_mantis

from blitzmotion.writer import MotionSADWriter

mantis = get_mantis()
MotionSADWriter.export_multiprocessed(mantis)

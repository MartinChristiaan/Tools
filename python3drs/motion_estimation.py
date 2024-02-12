import cv2
import numpy as np
from numba import jit, prange

updatesetx = [0, 0.25, 1, 3, -0.25, -1, -3] + [0] * 6
updatesety = [0, 0, 0, 0, 0, 0, 0] + [0.25, 1, 3, -0.25, -1, -3]
updateset = np.array(list(zip(updatesetx, updatesety))).astype(np.float32)
candidate_set = np.array([(0, -1, -1), (0, -1, 1), (-1, 1, 1)]).astype(np.int32)
candidate_set = np.array([(0, -1, -1), (0, -1, 1)]).astype(np.int32)


@jit(nopython=True, parallel=False)
def three_drs(
    mvf_cur,
    mvf_prev,
    frame_center,
    frame_offset,
    out_sad,
    alpha,
    num_blocks_x,
    num_blocks_y,
    block_size,
    downscale,
    actual_updates,
    reverse,
):

    candidates = np.zeros(
        (len(candidate_set) * actual_updates + 1, 2), dtype=np.float32
    )
    # SADs = np.ones((len(candidate_set) * actual_updates + 1)) * 9999
    n = 1
    h, w = frame_center.shape
    for y_block in range(num_blocks_y):
        if reverse:
            y_block = num_blocks_y - y_block - 1

        for x_block in range(num_blocks_x):
            for i in range(candidate_set.shape[0]):
                dn, dy, dx = candidate_set[i]

                if (
                    x_block + dx >= 0
                    and x_block + dx < num_blocks_x
                    and y_block + dy >= 0
                    and y_block + dy < num_blocks_y
                    and n - dn >= 0
                ):
                    if reverse:
                        dy = -dy
                    update_candidates = np.random.randint(
                        0, updateset.shape[0], actual_updates
                    )
                    for j in range(actual_updates):
                        candidates[i * actual_updates + j] = (
                            (
                                mvf_cur[:, y_block + dy, x_block + dx]
                                + updateset[update_candidates[j]]  # / downscale
                            )
                            if dn == 0
                            else (
                                mvf_prev[:, y_block + dy, x_block + dx]
                                + updateset[update_candidates[j]]  # / downscale
                            )
                        )
                else:
                    candidates[i * actual_updates] = np.zeros(2)

            candidates[-1] = np.zeros(2)
            min_sad = out_sad[y_block, x_block]
            mv = mvf_cur[:, y_block, x_block]
            for idx in range(len(candidates)):
                candidate = candidates[idx]
                sad = compute_sad(
                    frame_center,
                    frame_offset,
                    alpha,
                    block_size,
                    downscale,
                    h,
                    w,
                    y_block,
                    x_block,
                    candidate,
                )
                if sad < min_sad:
                    min_sad = sad
                    mv = candidate

            mvf_cur[0, y_block, x_block] = mv[0]
            mvf_cur[1, y_block, x_block] = mv[1]
            out_sad[y_block, x_block] = min_sad


@jit(nopython=True)
def compute_sad(
    frame_center,
    frame_offset,
    alpha,
    block_size,
    downscale,
    h,
    w,
    y_block,
    x_block,
    candidate,
):
    frame2_x = int((x_block * block_size + candidate[0] * (1 - alpha)) * downscale)
    frame2_y = int((y_block * block_size + candidate[1] * (1 - alpha)) * downscale)
    frame1_x = int((x_block * block_size - candidate[0] * alpha) * downscale)
    frame1_y = int((y_block * block_size - candidate[1] * alpha) * downscale)

    frame2_x = min(max(frame2_x, 0), w - block_size * downscale)
    frame1_x = min(max(frame1_x, 0), w - block_size * downscale)
    frame2_y = min(max(frame2_y, 0), h - block_size * downscale)
    frame1_y = min(max(frame1_y, 0), h - block_size * downscale)
    sad = 0
    for i in range(block_size):
        for j in range(block_size):
            v1 = frame_center[frame1_y + i * downscale, frame1_x + j * downscale]
            v2 = frame_offset[frame2_y + i * downscale, frame2_x + j * downscale]
            if v1 > v2:
                sad += v1 - v2
            else:
                sad += v2 - v1
    return sad


@jit(nopython=True, parallel=True)
def compute_out_sad(mvf, frame_cur, frame_next, alpha, sad, h=1080, w=1920):
    max_h = h - 1
    max_w = w - 1
    for y in prange(h):
        for x in prange(w):
            mv_x = mvf[0, y, x]
            mv_y = mvf[1, y, x]

            frame2_x = int((x + mv_x * (1 - alpha)))
            frame2_y = int((y + mv_y * (1 - alpha)))
            frame1_x = int((x - mv_x * alpha))
            frame1_y = int((y - mv_y * alpha))

            frame2_x = min(max(frame2_x, 0), max_w)
            frame1_x = min(max(frame1_x, 0), max_w)
            frame2_y = min(max(frame2_y, 0), max_h)
            frame1_y = min(max(frame1_y, 0), max_h)

            v1 = frame_cur[frame1_y, frame1_x]
            v2 = frame_next[frame2_y, frame2_x]
            if v1 > v2:
                sad[frame1_y, frame1_x] = v1 - v2
            else:
                sad[frame1_y, frame1_x] = v2 - v1


def convert_to_gray_if_needed(frame):
    if len(frame.shape) == 3:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return frame


class MotionEstimator:
    def __init__(self, block_size=8, downscale=1, alpha=0, actual_updates=6):
        self.block_size = block_size
        self.downscale = downscale
        self.alpha = alpha
        self.mvf_prev = None
        self.actual_updates = actual_updates

    def compute(
        self, frame_center, frame_offset, mvf_cur=None, sad=None, reverse=False
    ):
        frame_center = convert_to_gray_if_needed(frame_center)
        frame_offset = convert_to_gray_if_needed(frame_offset)
        num_blocks_x = frame_center.shape[1] // (self.block_size * self.downscale)
        num_blocks_y = frame_center.shape[0] // (self.block_size * self.downscale)
        if mvf_cur is None:
            mvf_cur = np.zeros((2, num_blocks_y, num_blocks_x), dtype=np.float32)
        if sad is None:
            sad = np.ones((num_blocks_y, num_blocks_x), dtype=np.float32) * 999999
        if self.mvf_prev is None:
            mvf_prev = np.zeros((2, num_blocks_y, num_blocks_x), dtype=np.float32)
        else:
            mvf_prev = self.mvf_prev

        three_drs(
            mvf_cur,
            mvf_prev,
            frame_center,
            frame_offset,
            sad,
            self.alpha,
            num_blocks_x,
            num_blocks_y,
            self.block_size,
            self.downscale,
            self.actual_updates,
            reverse,
        )
        self.mvf_prev = mvf_cur
        return mvf_cur * self.downscale, sad


class OutSadComputer:
    def __init__(self, alpha=0) -> None:
        self.alpha = alpha

    def compute_out_sad(self, mvf, frame_center, frame_offset):
        h, w = frame_center.shape
        full_out_sad = np.zeros((h, w), dtype=np.float32)
        compute_out_sad(mvf, frame_center, frame_offset, self.alpha, full_out_sad, h, w)
        return full_out_sad

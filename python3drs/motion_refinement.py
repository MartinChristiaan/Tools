# %%
import numba
import numpy as np
from numba import cuda
from tqdm import tqdm

# updatesety = [0, 0, 0, 0, 0, 0, 0] + [0.25, 1, 3, -0.25, -1, -3
# updateset = np.array(list(zip(updatesetx, updatesety))).astype(np.float32)

BLOCK_SIZE = 8
SEARCH_SPACE = 8
OFFSET_CACHE_SIZE = BLOCK_SIZE + SEARCH_SPACE * 2


@cuda.jit
def mvf_refine(
    mvf_cur,
    mvf_hr,
    frame_center,
    frame_next,
    num_blocks_x,
    num_blocks_y,
    block_size,
    downscale,
):

    min_sad = 9999999999999
    x_block = cuda.blockIdx.x * cuda.blockDim.x + cuda.threadIdx.x
    y_block = cuda.blockIdx.y * cuda.blockDim.y + cuda.threadIdx.y
    h, w = frame_center.shape
    if not (x_block < num_blocks_x * downscale and y_block < num_blocks_y * downscale):
        return
    mv_x = mvf_cur[0, y_block // downscale, x_block // downscale]
    mv_y = mvf_cur[1, y_block // downscale, x_block // downscale]
    # mvf_cur[0, y_block, x_block] = 1
    mv_best_x = mv_x
    mv_best_y = mv_y

    # allocate cashes

    frame_center_cache = cuda.local.array((BLOCK_SIZE, BLOCK_SIZE), numba.uint8)
    frame_offset_cache = cuda.local.array(
        (OFFSET_CACHE_SIZE, OFFSET_CACHE_SIZE),
        numba.uint8,
    )

    x0 = block_size * x_block
    y0 = block_size * y_block
    for xb in range(block_size):
        for yb in range(block_size):
            x = xb + x0
            y = yb + y0
            v = frame_center[y, x]
            frame_center_cache[yb, xb] = v

    x0 = int(block_size * x_block + mv_x - SEARCH_SPACE)
    y0 = int(block_size * y_block + mv_y - SEARCH_SPACE)

    for xb in range(block_size + SEARCH_SPACE * 2):
        for yb in range(block_size + SEARCH_SPACE * 2):

            x = xb + x0
            y = yb + y0
            if x < 0 or x >= w - 1 or y < 0 or y > h - 1:
                frame_offset_cache[yb, xb] = 0
            else:
                v = frame_next[y, x]
                frame_offset_cache[yb, xb] = v

    # run convolution

    for xo in range(SEARCH_SPACE * 2):
        for yo in range(SEARCH_SPACE * 2):
            sad = 0
            for xc in range(block_size):
                for yc in range(block_size):
                    v1 = frame_center_cache[yc, xc]
                    v2 = frame_offset_cache[yo + yc, xo + xc]
                    if v1 > v2:
                        sad += v1 - v2
                    else:
                        sad += v2 - v1

            if min_sad > sad:
                min_sad = sad
                mv_best_x = mv_x + x0 - SEARCH_SPACE
                mv_best_y = mv_y + y0 - SEARCH_SPACE
    mvf_hr[0, y_block, x_block] = mv_best_x
    mvf_hr[1, y_block, x_block] = mv_best_y


class MotionRefiner:
    def __init__(self, threads_per_block=16) -> None:
        self.threads_per_block = threads_per_block

    def refine(self, mvf, frame_center, frame_offset, downscale, block_size=8):
        y_blocks, x_blocks = [x * downscale for x in mvf.shape[1:]]
        cuda_x_blocks = x_blocks // self.threads_per_block
        cuda_y_blocks = y_blocks // self.threads_per_block + 1
        mvf_cuda, frame_center_cuda, frame_offset_cuda = [
            cuda.to_device(x) for x in [mvf, frame_center, frame_offset]
        ]
        mvf_hr_cuda = cuda.device_array((2, y_blocks, x_blocks), np.float32)

        mvf_refine[
            (cuda_y_blocks, cuda_x_blocks),
            (self.threads_per_block, self.threads_per_block),
        ](
            mvf_cuda,
            mvf_hr_cuda,
            frame_center_cuda,
            frame_offset_cuda,
            x_blocks,
            y_blocks,
            block_size,
            downscale,
        )


if __name__ == "__main__":
    refiner = MotionRefiner()
    f0 = np.zeros((1080, 1920), dtype=np.uint8)
    f1 = np.zeros((1080, 1920), dtype=np.uint8)
    mvf = np.zeros((2, 135 // 4, 240 // 4), dtype=np.float32)
    downscale = 1
    block_size = 8
    for j in tqdm(range(1000)):
        refiner.refine(mvf, f0, f1, downscale, block_size)

# %%

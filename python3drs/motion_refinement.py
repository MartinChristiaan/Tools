# %%
import cv2
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
    out_sad,
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
    mv_x = 0  # mvf_cur[0, y_block // downscale, x_block // downscale]
    mv_y = 0  # mvf_cur[1, y_block // downscale, x_block // downscale]
    # mvf_cur[0, y_block, x_block] = 1
    mv_best_x = 0  # mv_x
    mv_best_y = 0  # mv_y

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

    for x_o in range(SEARCH_SPACE * 2):
        for y_o in range(SEARCH_SPACE * 2):
            sad = 0
            for xc in range(block_size):
                for yc in range(block_size):
                    v1 = frame_center_cache[yc, xc]
                    v2 = frame_offset_cache[y_o + yc, x_o + xc]
                    if v1 > v2:
                        sad += v1 - v2
                    else:
                        sad += v2 - v1

            if min_sad > sad:
                min_sad = sad
                mv_best_x = mv_x + x_o - SEARCH_SPACE
                mv_best_y = mv_y + y_o - SEARCH_SPACE
    mvf_hr[0, y_block, x_block] = mv_best_x
    mvf_hr[1, y_block, x_block] = mv_best_y
    out_sad[y_block, x_block] = min_sad


class MotionRefiner:
    def __init__(self, grid_shape, threads_per_block=8) -> None:
        self.y_blocks, self.x_blocks = grid_shape
        self.threads_per_block = threads_per_block
        self.mvf_hr_cuda = cuda.device_array(
            (2, self.y_blocks, self.x_blocks), np.float32
        )
        self.out_sad = cuda.device_array((self.y_blocks, self.x_blocks), np.float32)

    def refine(self, mvf, frame_center, frame_offset, downscale, block_size=8):
        y_blocks, x_blocks = [x * downscale for x in mvf.shape[1:]]
        cuda_x_blocks = x_blocks // self.threads_per_block + 1
        cuda_y_blocks = y_blocks // self.threads_per_block + 1

        mvf_refine[
            (cuda_x_blocks, cuda_y_blocks),
            (self.threads_per_block, self.threads_per_block),
        ](
            mvf,
            self.mvf_hr_cuda,
            out_sad,
            frame_center,
            frame_offset,
            x_blocks,
            y_blocks,
            block_size,
            downscale,
        )
        return self.mvf_hr_cuda.copy_to_host(), self.out_sad.copy_to_host()


path = "/media/martin/DeepLearning/mantis_drone_2023/raw/mantis_drone_2023/DJI_202309101443_008_wide_hd/0/1694357059368.jpg"
if __name__ == "__main__":
    frame = cv2.imread(path, 0)
    frame0 = np.zeros_like(frame)
    # frame1 = np.zeros_like(frame)
    delta = 3
    frame0[delta:] = frame[: 1080 - delta]

    mvf = np.zeros((2, 135 // 4, 240 // 4), dtype=np.float32)
    refiner = MotionRefiner((135, 240))
    downscale = 4
    block_size = 8
    for j in tqdm(range(100)):
        mvf, out_sad = refiner.refine(mvf, frame0, frame, downscale, block_size)
    print(mvf[0, :, :].mean())
    print(mvf[1, :, :].mean())
    import matplotlib.pyplot as plt

    plt.figure()
    plt.imshow(mvf[1, :, :])

    plt.figure()
    plt.imshow(out_sad[:, :])
    plt.show()


# %%

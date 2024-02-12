import cv2
import numpy as np
import skimage.transform
from cv2.ximgproc import guidedFilter, jointBilateralFilter


def guided_filter(mvf, guide):
    guide_gray = cv2.cvtColor(guide, cv2.COLOR_BGR2GRAY)

    return perform_per_direction(mvf, lambda m: _guided_filter(m, guide_gray))


def bilateral_filter(mvf, guide):
    guide_gray = cv2.cvtColor(guide, cv2.COLOR_BGR2GRAY).astype(np.float32)
    return perform_per_direction(mvf, lambda m: _bilateral_filter(m, guide_gray))


def _guided_filter(mvf, guide):
    if guide.shape[-1] == 3:
        guide = cv2.cvtColor(guide, cv2.COLOR_BGR2GRAY).astype(np.float32)

    guide_0 = cv2.resize(guide, (240, 135))  # cv2 resize uses (xres yres)
    guided_0 = guidedFilter(guide_0, mvf, 7, 0.1)
    mvf1 = nearest_neighbour_upscale(guided_0, (270, 480))
    guided_1 = guidedFilter(guide, mvf1, 14, 0.1)
    return guided_1


def get_nearest_candidate(mvf0, cmvf1):
    # yy,xx = np.meshgrid((np.arange(270)/2.0).astype(int),
    #     (np.arange(480)/2.0).astype(int))
    H, W = mvf0.shape
    options = np.expand_dims(mvf0, 0).repeat(5, 0)
    options[1, :, :-1] = mvf0[:, 1:]  # right
    options[2, :, 1:] = mvf0[:, :-1]  # left
    options[3, :-1, :] = mvf0[1:, :]  # up
    options[4, 1:, :] = mvf0[:-1, :]  # down

    distances = np.zeros((5, H, W))
    option_upscaled = np.zeros((5, H, W))

    for idx in range(5):
        option_upscaled[idx] = nearest_neighbour_upscale(options[idx], (H, W))
        distances[idx] = np.abs(cmvf1 - option_upscaled[idx])

    choices = np.argmin(distances, axis=0)
    final_vector = np.zeros_like(cmvf1)
    for idx in range(5):
        final_vector += (choices == idx) * option_upscaled[idx]
    return final_vector


def get_dual_direction_nearest_candidate(fwd_mvf, bwd_mvf, ret_mvf):
    # yy,xx = np.meshgrid((np.arange(270)/2.0).astype(int),
    #     (np.arange(480)/2.0).astype(int))
    H, W = fwd_mvf.shape
    options = np.expand_dims(fwd_mvf, 0).repeat(10, 0)
    options[1, :, :-1] = fwd_mvf[:, 1:]  # right
    options[2, :, 1:] = fwd_mvf[:, :-1]  # left
    options[3, :-1, :] = fwd_mvf[1:, :]  # up
    options[4, 1:, :] = fwd_mvf[:-1, :]  # down
    options[5] = bwd_mvf  # down

    options[6, :, :-1] = bwd_mvf[:, 1:]  # right
    options[7, :, 1:] = bwd_mvf[:, :-1]  # left
    options[8, :-1, :] = bwd_mvf[1:, :]  # up
    options[9, 1:, :] = bwd_mvf[:-1, :]  # down

    distances = np.zeros((10, H, W))

    for idx in range(10):
        distances[idx] = np.abs(ret_mvf - options[idx])

    choices = np.argmin(distances, axis=0)
    final_vector = np.zeros_like(ret_mvf)
    for idx in range(10):
        final_vector += (choices == idx) * options[idx]
    return final_vector


def _bilateral_filter(mvf, guide):
    mvf0 = cv2.medianBlur(mvf, 3)
    if guide.shape[-1] == 3:
        guide = cv2.cvtColor(guide, cv2.COLOR_BGR2GRAY).astype(np.float32)

    guide_0 = cv2.resize(guide, (240, 135))  # cv2 resize uses (xres yres)
    guided_0 = jointBilateralFilter(guide_0, mvf0, 15, 30, 100)

    mvf1 = get_nearest_candidate(mvf0, guided_0)

    mvf1 = nearest_neighbour_upscale(mvf1, (270, 480))

    mvf1 = cv2.medianBlur(mvf1, 5)
    mvf2 = nearest_neighbour_upscale(mvf1)
    mvf2 = cv2.medianBlur(mvf2, 5)
    return mvf2

    # return get_nearest_candidate(mvf,guided_1)


def calc_median(inputs):
    x = np.concatenate([np.expand_dims(x, 0) for x in inputs], axis=0)
    x.sort(axis=0)
    return x[1]


def test_calc_median():
    a = np.ones(5)
    b = np.ones(5) * 3
    c = np.ones(5) * 2
    assert (calc_median([a, b, c]) - c).sum() == 0


test_calc_median()


def median_erosion(mvf):
    return perform_per_direction(mvf, _median_erosion)


def triple_median(mvf):
    return perform_per_direction(mvf, _triple_median)


def nearest_neighbours_upscale(mvf):
    return perform_per_direction(
        mvf, lambda x: cv2.resize(x, (1920, 1080), interpolation=cv2.INTER_NEAREST)
    )


def perform_per_direction(mvf, func):
    return np.concatenate([np.expand_dims(func(mvf[i]), 0) for i in range(2)], axis=0)


def _median_erosion(vectorfield):
    v0 = vectorfield[1:-1, 1:-1]

    vu = vectorfield[:-2, 1:-1]
    vl = vectorfield[1:-1, :-2]

    vr = vectorfield[1:-1, 2:]
    vb = vectorfield[2:, 1:-1]

    ul = calc_median([v0, vu, vl])
    ur = calc_median([v0, vu, vr])
    bl = calc_median([v0, vb, vl])
    br = calc_median([v0, vb, vr])

    resized = nearest_neighbour_upscale(vectorfield, (270, 480))
    resized[2:-3, 2:-3][::2, ::2] = ul
    resized[2:-3, 3:-2][::2, ::2] = ur
    resized[3:-2, 2:-3][::2, ::2] = bl
    resized[3:-2, 3:-2][::2, ::2] = br

    return resized


def _triple_median(vectorfield_raw):
    vectorfield_l0 = cv2.medianBlur(vectorfield_raw, 3)
    vectorfield_l1 = cv2.resize(
        vectorfield_l0, (480, 270), interpolation=cv2.INTER_NEAREST
    )
    vectorfield_l1 = cv2.medianBlur(vectorfield_l1, 5)
    vectorfield_l2 = cv2.resize(
        vectorfield_l1, (1920, 1080), interpolation=cv2.INTER_NEAREST
    )
    return cv2.medianBlur(vectorfield_l2, 5)

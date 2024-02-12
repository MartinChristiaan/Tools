import cv2
import numpy as np


def make_colorwheel():
    """
    Generates a color wheel for optical flow visualization as presented in:
        Baker et al. "A Database and Evaluation Methodology for Optical Flow" (ICCV, 2007)
        URL: http://vision.middlebury.edu/flow/flowEval-iccv07.pdf

    According to the C++ source code of Daniel Scharstein
    According to the Matlab source code of Deqing Sun
    """

    RY = 15
    YG = 6
    GC = 4
    CB = 11
    BM = 13
    MR = 6

    ncols = RY + YG + GC + CB + BM + MR
    colorwheel = np.zeros((ncols, 3))
    col = 0

    # RY
    colorwheel[0:RY, 0] = 255
    colorwheel[0:RY, 1] = np.floor(255 * np.arange(0, RY) / RY)
    col = col + RY
    # YG
    colorwheel[col : col + YG, 0] = 255 - np.floor(255 * np.arange(0, YG) / YG)
    colorwheel[col : col + YG, 1] = 255
    col = col + YG
    # GC
    colorwheel[col : col + GC, 1] = 255
    colorwheel[col : col + GC, 2] = np.floor(255 * np.arange(0, GC) / GC)
    col = col + GC
    # CB
    colorwheel[col : col + CB, 1] = 255 - np.floor(255 * np.arange(CB) / CB)
    colorwheel[col : col + CB, 2] = 255
    col = col + CB
    # BM
    colorwheel[col : col + BM, 2] = 255
    colorwheel[col : col + BM, 0] = np.floor(255 * np.arange(0, BM) / BM)
    col = col + BM
    # MR
    colorwheel[col : col + MR, 2] = 255 - np.floor(255 * np.arange(MR) / MR)
    colorwheel[col : col + MR, 0] = 255
    return 255 - colorwheel


def flow_compute_color(u, v, convert_to_bgr=False):
    """
    Applies the flow color wheel to (possibly clipped) flow components u and v.

    According to the C++ source code of Daniel Scharstein
    According to the Matlab source code of Deqing Sun

    :param u: np.ndarray, input horizontal flow
    :param v: np.ndarray, input vertical flow
    :param convert_to_bgr: bool, whether to change ordering and output BGR instead of RGB
    :return:
    """

    flow_image = np.zeros((u.shape[0], u.shape[1], 3), np.uint8)

    colorwheel = make_colorwheel()  # shape [55x3]
    ncols = colorwheel.shape[0]

    rad = np.sqrt(np.square(u) + np.square(v))
    a = np.arctan2(-v, -u) / np.pi

    fk = (a + 1) / 2 * (ncols - 1)
    k0 = np.floor(fk).astype(np.int32)
    k1 = k0 + 1
    k1[k1 == ncols] = 0
    f = fk - k0

    for i in range(colorwheel.shape[1]):

        tmp = colorwheel[:, i]
        col0 = tmp[k0] / 255.0
        col1 = tmp[k1] / 255.0
        col = (1 - f) * col0 + f * col1

        idx = rad <= 1
        col[idx] = 1 - rad[idx] * (1 - col[idx])
        col[~idx] = col[~idx] * 0.75  # out of range?

        # Note the 2-i => BGR instead of RGB
        ch_idx = 2 - i if convert_to_bgr else i
        flow_image[:, :, ch_idx] = np.floor(255 * col)

    return flow_image


def flowtensor_to_color(flowtensor, rad_max=None):
    if len(flowtensor.shape) == 4:
        return flow_to_color(flowtensor[0].cpu().numpy(), rad_max=rad_max)
    else:
        return flow_to_color(flowtensor.cpu().numpy(), rad_max=rad_max)


def get_norm_factor_tensor(flowfields):
    maxes = []
    for flow_uv in flowfields:
        u = flow_uv[0, 1, :, :].cpu().numpy()
        v = flow_uv[0, 0, :, :].cpu().numpy()
        rad = np.sqrt(np.square(u) + np.square(v))
        maxes += [np.max(rad)]
    return max(maxes)


def get_norm_factor(flow_uv):
    u = flow_uv[1, :, :]
    v = flow_uv[0, :, :]
    rad = np.sqrt(np.square(u) + np.square(v))
    return np.max(rad)


def flow_to_color(flow_uv, clip_flow=None, convert_to_bgr=False, rad_max=None):
    """
    Expects a two dimensional flow image of shape [2,H,W]

    According to the C++ source code of Daniel Scharstein
    According to the Matlab source code of Deqing Sun

    :param flow_uv: np.ndarray of shape [2,H,W]
    :param clip_flow: float, maximum clipping value for flow
    :return:
    """

    assert flow_uv.ndim == 3, "input flow must have three dimensions"
    assert flow_uv.shape[0] == 2, "input flow must have shape [2,H,W]"

    flow_uv = np.moveaxis(flow_uv, 0, -1)
    if clip_flow is not None:
        flow_uv = np.clip(flow_uv, 0, clip_flow)

    u = flow_uv[:, :, 0]
    v = flow_uv[:, :, 1]

    if rad_max == None:
        rad = np.sqrt(np.square(u) + np.square(v))
        rad_max = np.max(rad)

    epsilon = 1e-5
    u = u / (rad_max + epsilon)
    v = v / (rad_max + epsilon)

    return flow_compute_color(u, v, convert_to_bgr)


def norm(arr):
    arr = arr.astype(np.float32)
    return (arr - arr.min()) / (arr.max() - arr.min())


def apply_colormap(frame):
    return cv2.applyColorMap((frame * 255).astype(np.uint8), cv2.COLORMAP_JET)


def apply_norm_colormap(frame):

    return cv2.applyColorMap((norm(frame) * 255).astype(np.uint8), cv2.COLORMAP_JET)


def draw_sad_vf(vf, sad, block_size, frame):
    vf = draw_vector_field(vf, block_size)
    print(vf.shape, sad.shape, frame.shape)
    sad_upscaled = cv2.resize(sad, vf.shape[::-1], interpolation=cv2.INTER_NEAREST)
    vf_sadmod = apply_norm_colormap(vf * sad_upscaled)
    print(vf.shape)
    out_img = vf[:, :, np.newaxis] * vf_sadmod + ~vf[:, :, np.newaxis] * cv2.resize(
        frame, vf.shape[::-1], interpolation=cv2.INTER_NEAREST
    )
    return out_img


def get_mixing_image(frame, featuremap):
    fcolor = featuremap.astype(np.float32)
    if len(featuremap.shape) == 2:
        fcolor = apply_norm_colormap(fcolor)
    # print(fcolor.shape)
    if len(frame.shape) == 3:
        gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).astype(np.float32)
    elif len(frame.shape) == 2:
        gray_image = frame
    else:
        gray_image = np.zeros_like(fcolor)[:, :, 0]
    if fcolor.shape[:2] != gray_image.shape[:2]:
        fcolor = cv2.resize(fcolor, (gray_image.shape[:2][::-1]))
    # print(fcolor.shape)
    mixed = ((np.expand_dims(gray_image, -1) + fcolor) / 2).astype(np.uint8)
    return mixed


def get_flow_vizualization(frame, mvf):
    return get_mixing_image(frame, flow_to_color(mvf))


def draw_vector_field(vector_field, block_size, background, thickness=1, tipLength=0.2):
    num_blocks_y, num_blocks_x = vector_field.shape[-2:]
    for y_block in range(num_blocks_y):
        for x_block in range(num_blocks_x):
            y_start = int((y_block * (block_size) + block_size))
            x_start = int((x_block * (block_size) + block_size))
            color = (255, 255, 255)
            cv2.arrowedLine(
                background,
                pt1=(x_start, y_start),
                pt2=(
                    x_start + int(vector_field[1, y_block, x_block]),
                    y_start + int(vector_field[0, y_block, x_block]),
                ),
                color=color,
                thickness=thickness,
                tipLength=tipLength,
            )

    return background

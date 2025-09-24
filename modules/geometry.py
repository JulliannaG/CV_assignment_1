import cv2 as cv
import numpy as np

window_name = "Webcam Feed"

def init_translation_trackbars():
    cv.createTrackbar("tx", window_name, 300, 600, lambda x: None) 
    cv.createTrackbar("ty", window_name, 300, 600, lambda x: None)

def init_rotation_trackbars():
    cv.createTrackbar("angle", window_name, 0, 360, lambda x: None) 

def init_scaling_trackbars():
    cv.createTrackbar("scale", window_name, 10, 30, lambda x: None) 

def apply_translation(frame):
    tx = cv.getTrackbarPos("tx", window_name) - 300
    ty = cv.getTrackbarPos("ty", window_name) - 300
    M = np.float32([[1, 0, tx],
                    [0, 1, ty]])
    return cv.warpAffine(frame, M, (frame.shape[1], frame.shape[0]))

def apply_rotation(frame):
    angle = cv.getTrackbarPos("angle", window_name)
    h, w = frame.shape[:2]
    M = cv.getRotationMatrix2D((w//2, h//2), angle, 1.0)
    return cv.warpAffine(frame, M, (w, h))


def apply_scaling(frame):
    scale_val = cv.getTrackbarPos("scale", window_name)
    scale = max(0.1, scale_val / 10.0)  #assure the value is not <= 0

    h, w = frame.shape[:2]
    new_w, new_h = int(w * scale), int(h * scale)

    scaled = cv.resize(frame, (new_w, new_h), interpolation=cv.INTER_CUBIC)

    #adding black background around picture
    background = np.zeros_like(frame)

    x_offset = (w - new_w) // 2
    y_offset = (h - new_h) // 2

    #display cropped frame
    x1_bg = max(0, x_offset)
    y1_bg = max(0, y_offset)
    x2_bg = min(w, x_offset + new_w)
    y2_bg = min(h, y_offset + new_h)

    x1_sc = max(0, -x_offset)
    y1_sc = max(0, -y_offset)
    x2_sc = x1_sc + (x2_bg - x1_bg)
    y2_sc = y1_sc + (y2_bg - y1_bg)

    background[y1_bg:y2_bg, x1_bg:x2_bg] = scaled[y1_sc:y2_sc, x1_sc:x2_sc]

    return background



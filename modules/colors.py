import cv2 as cv

window_name = 'Webcam Feed'

def normal(frame):
    return frame

def apply_rgb(frame):
    return cv.cvtColor(frame, cv.COLOR_BGR2RGB)

def apply_grayscale(frame):
    return cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

def apply_hsv(frame):
    return cv.cvtColor(frame, cv.COLOR_BGR2HSV)

def init_cb_trackbars():
    cv.createTrackbar("Contrast (alpha)", window_name, 10, 30, lambda x: None) 
    cv.createTrackbar("Brightness (beta)", window_name, 50, 100, lambda x: None)

def apply_contrast_brightness(frame):
    alpha = cv.getTrackbarPos("Contrast (alpha)", window_name) / 10  
    beta = cv.getTrackbarPos("Brightness (beta)", window_name) - 50
    return cv.convertScaleAbs(frame, alpha=alpha, beta=beta)



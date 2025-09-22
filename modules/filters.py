import cv2 as cv

window_name = "Webcam Feed"

def init_gaussian_trackbars():
    cv.createTrackbar("ksize", window_name, 0, 9, lambda x: None)  # 10 wartości -> kernel_sizes[0..9]
    cv.createTrackbar("sigmaX", window_name, 5, 50, lambda x: None)

def apply_gaussian(frame):
    kernel_sizes = [3, 5, 7, 9, 11, 13, 15, 17, 19, 21]
    k_index = cv.getTrackbarPos("ksize", window_name)
    sigma = cv.getTrackbarPos("sigmaX", window_name) / 10.0
    ksize = kernel_sizes[k_index]
    return cv.GaussianBlur(frame, (ksize, ksize), sigma)

def init_bilateral_trackbars():
    cv.createTrackbar("d", window_name, 9, 20, lambda x: None)
    cv.createTrackbar("sigmaColor", window_name, 75, 250, lambda x: None)
    cv.createTrackbar("sigmaSpace", window_name, 75, 250, lambda x: None)

def apply_bilateral(frame):
    d = cv.getTrackbarPos("d", window_name)
    sigmaColor = cv.getTrackbarPos("sigmaColor", window_name)
    sigmaSpace = cv.getTrackbarPos("sigmaSpace", window_name)
    return cv.bilateralFilter(frame, d, sigmaColor, sigmaSpace)

def init_canny_trackbars():
    cv.createTrackbar("Threshold1", window_name, 50, 255, lambda x: None)
    cv.createTrackbar("Threshold2", window_name, 150, 255, lambda x: None) 

def apply_canny(frame):
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    tresh1 = cv.getTrackbarPos("Treshold1", window_name) / 10  
    tresh2 = cv.getTrackbarPos("Treshold2", window_name) - 50

    final = cv.Canny(gray, threshold1=tresh1, threshold2=tresh2, L2gradient=True)
    return final

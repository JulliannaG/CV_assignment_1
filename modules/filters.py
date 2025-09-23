import cv2 as cv
import numpy as np

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

    tresh1 = cv.getTrackbarPos("Threshold1", window_name) 
    tresh2 = cv.getTrackbarPos("Threshold2", window_name) 

    final = cv.Canny(gray, threshold1=tresh1, threshold2=tresh2, L2gradient=True)
    return final

def init_hough_trackbars():
    cv.createTrackbar("Rho", window_name, 3, 5, lambda x: None)
    cv.createTrackbar("Theta", window_name, 90, 180, lambda x: None) 
    cv.createTrackbar("Threshold", window_name, 200, 255, lambda x: None) 

def apply_hough(frame):
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    edges = cv.Canny(gray, 50, 150)   

    rho = cv.getTrackbarPos("Rho", window_name)
    theta_deg = cv.getTrackbarPos("Theta", window_name)
    threshold = cv.getTrackbarPos("Threshold", window_name)

    if rho < 1:
        rho = 1
    theta = np.deg2rad(max(theta_deg, 1)) 

    lines = cv.HoughLines(edges, rho, theta, threshold)

    if lines is not None:
        for line in lines:
            rho, theta = line[0]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            cv.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

    return frame




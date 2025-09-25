import cv2 as cv
import numpy as np

def show_histogram(frame, submode):
    hists = []

    if submode == "rgb":
        # jeśli obraz jest 1-kanałowy, zamień na 3 kanały
        if len(frame.shape) == 2:
            frame = cv.cvtColor(frame, cv.COLOR_GRAY2BGR)

        colors = ('b', 'g', 'r')
        for i, col in enumerate(colors):
            hist = cv.calcHist([frame], [i], None, [256], [0, 256])
            hists.append((hist, col))

    elif submode == "hsv":
        if len(frame.shape) == 2:  
            frame = cv.cvtColor(frame, cv.COLOR_GRAY2BGR)

        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        colors = ('m','c','y')  
        for i, col in enumerate(colors):
            hist = cv.calcHist([hsv], [i], None, [256], [0, 256])
            hists.append((hist, col))

    elif submode == "gray":
        if len(frame.shape) == 3:  
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        else:
            gray = frame
        hist = cv.calcHist([gray], [0], None, [256], [0, 256])
        hists.append((hist, 'w'))

    elif submode == "brightness":
        if len(frame.shape) == 2:
            frame = cv.cvtColor(frame, cv.COLOR_GRAY2BGR)

        ycrcb = cv.cvtColor(frame, cv.COLOR_BGR2YCrCb)
        hist = cv.calcHist([ycrcb], [0], None, [256], [0, 256])
        hists.append((hist, 'w'))

    hist_img = np.zeros((300, 256, 3), dtype=np.uint8)
    for hist, col in hists:
        cv.normalize(hist, hist, 0, 300, cv.NORM_MINMAX)
        for x, y in enumerate(hist):
            if col == 'b':
                color = (255, 0, 0)
            elif col == 'g':
                color = (0, 255, 0)
            elif col == 'r':
                color = (0, 0, 255)
            elif col == 'm':
                color = (255, 0, 255)
            elif col == 'c':
                color = (0, 255, 255)
            elif col == 'y':
                color = (0, 255, 255)
            else:
                color = (200, 200, 200)
            cv.line(hist_img, (x, 300), (x, 300 - int(y)), color, 1)

    cv.imshow("Histogram", hist_img)

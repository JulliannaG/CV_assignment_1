import cv2 as cv
from modules import colors, filters, histograms

cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

mode1 = 'normal'
mode2 = 'colors'
mode3 = 'filters'
mode4 = 'geometry'

mode = mode1
submode = None
last_submode = None
window_name = 'Webcam Feed'
show_hist = False

while True:
    ret, frame = cap.read()
    cv.namedWindow(window_name, cv.WINDOW_NORMAL)
    cv.setWindowProperty('Webcam Feed', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)

    if not ret:
        print("Can't receive frame. Exiting ...")
        break

    if submode != last_submode:
        cv.destroyWindow(window_name)
        cv.namedWindow(window_name, cv.WINDOW_NORMAL)
        cv.setWindowProperty('Webcam Feed', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)

        if submode == "gaussian":
            filters.init_gaussian_trackbars()
        elif submode == "bilateral":
            filters.init_bilateral_trackbars()
        elif submode == "brightness":
            colors.init_cb_trackbars()
        elif submode == "canny":
            filters.init_canny_trackbars()
    
    if mode == mode1:
        frame = colors.normal(frame)
    if mode == mode2:
        if submode == "rgb":
            frame = colors.apply_rgb(frame)
        elif submode == "hsv":
            frame = colors.apply_hsv(frame)
        elif submode == "gray":
            frame = colors.apply_grayscale(frame)
        elif submode == "brightness":
            frame = colors.apply_contrast_brightness(frame)
    
    if mode == mode3:
        if submode == "gaussian":
            frame = filters.apply_gaussian(frame)
        elif submode == "bilateral":
            frame = filters.apply_bilateral(frame)
        elif submode == "canny":
            frame = filters.apply_canny(frame)

    last_submode = submode  

    if mode == mode1:
        menu_text = "[C]olors [F]ilters [P]anorama [G]eometry [A]R [C]alibration [Q]uit"
    elif mode == mode2:
        menu_text = "[R]GB [H]SV [G]ray [B]rightness/contrast [N]ormal"
        menu2_text = "[O]pen / [C]lose histogram"
        cv.putText(frame, menu2_text, (10, 30),
           cv.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

    elif mode == mode3:
        menu_text = "[G]aussian B[i]lateral [C]anny [N]ormal"
    elif mode == mode4:
        menu_text = "[H]ough [T]ranslate [R]otate [S]cale"

    cv.putText(frame, menu_text, (10, frame.shape[0]-10),
           cv.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
    cv.imshow(window_name, frame)

    key = cv.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('n'):  
        mode = mode1
        submode = None

    elif key == ord('c') and submode == None:
        mode = mode2 
        submode = None
    elif key == ord('r') and mode == mode2:
        submode = "rgb"
    elif key == ord('h') and mode == mode2:
        submode = "hsv"
    elif key == ord('g') and mode == mode2:
        submode = "gray"
    elif key == ord('b') and mode == mode2:
        submode = "brightness"

    elif key == ord('f') and submode == None:
        mode = mode3
        submode = None
    elif key == ord('c') and mode == mode3: #do naprawy -- ten przycisk czasami nie działa!!!
        submode = "canny"
    elif key == ord('g') and mode == mode3:
        submode = "gaussian"
    elif key == ord('b') and mode == mode3:
        submode = "bilateral"


    elif key == ord('o') and submode in ["rgb", "hsv", "brightness", "gray"]:
        histograms.show_histogram(frame, submode)
        show_hist = True  

    elif key == ord('c') and show_hist:  
        cv.destroyWindow("Histogram")
        show_hist = False

    if show_hist and submode in ["rgb", "hsv", "gray", "brightness"]: 
        histograms.show_histogram(frame, submode)
        #do naprawy - histogram zostaje przykryty przez video po zmianie trybu!!!
    

cap.release()
cv.destroyAllWindows()
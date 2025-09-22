import cv2 as cv
from modules import filters, blur

cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

mode = "normal" 
submode = None
last_submode = None
window_name = 'Webcam Feed'

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
            blur.init_gaussian_trackbars()
        elif submode == "bilateral":
            blur.init_bilateral_trackbars()
        elif submode == "brightness":
            filters.init_cb_trackbars()
        elif submode == "canny":
            filters.init_canny_trackbars()
    
    if mode == "normal":
        frame = filters.normal(frame)
    if mode == "filters":
        if submode == "rgb":
            frame = filters.apply_rgb(frame)
        elif submode == "hsv":
            frame = filters.apply_hsv(frame)
        elif submode == "gray":
            frame = filters.apply_grayscale(frame)
        elif submode == "brightness":
            frame = filters.apply_contrast_brightness(frame)
        elif submode == "canny":
            frame = filters.apply_canny(frame)
    if mode == "blur":
        if submode == "gaussian":
            frame = blur.apply_gaussian(frame)
        elif submode == "bilateral":
            frame = blur.apply_bilateral(frame)

    last_submode = submode  

    if mode == "normal":
        menu_text = "[F]ilters [B]lur [P]anorama [G]eometry [A]R [C]alibration [Q]uit"
    elif mode == "filters":
        menu_text = "[R]GB [H]SV [G]ray [B]rightness/contrast [C]anny [N]ormal"
    elif mode == "blur":
        menu_text = "[G]aussian B[i]lateral [N]ormal"
    elif mode == "geometry":
        menu_text = "[H]ough [T]ranslate [R]otate [S]cale"

    cv.putText(frame, menu_text, (10, frame.shape[0]-10),
           cv.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
    cv.imshow(window_name, frame)

    key = cv.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('n'):  
        mode = "normal"
        submode = None

    elif key == ord('f') and submode == None:
        mode = "filters" 
        submode = None
    elif key == ord('r') and mode == "filters":
        submode = "rgb"
    elif key == ord('h') and mode == "filters":
        submode = "hsv"
    elif key == ord('g') and mode == "filters":
        submode = "gray"
    elif key == ord('b') and mode == "filters":
        submode = "brightness"
    elif key == ord('c') and mode == "filters":
        submode = "canny"

    elif key == ord('b') and submode == None:
        mode = "blur"
        submode = None
    elif key == ord('g') and mode == "blur":
        submode = "gaussian"
    elif key == ord('i') and mode == "blur":
        submode = "bilateral"
    

cap.release()
cv.destroyAllWindows()
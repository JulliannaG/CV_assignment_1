import cv2 as cv
from modules import colors, filters, histograms, geometry, calibration, ar
from modules import panorama as panorama_module

def run():
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        return

    mode1 = 'normal'
    mode2 = 'colors'
    mode3 = 'filters'
    mode4 = 'geometry'
    mode5 = "panorama"
    mode6 = "calibration"
    mode7 = "ar"

    mode = mode1
    submode = None
    last_submode = None
    window_name = 'Webcam Feed'
    show_hist = False
    panorama_builder = panorama_module.PanoramaBuilder()
    panorama_on = False

    while True:
        ret, frame = cap.read()
        cv.namedWindow(window_name, cv.WINDOW_NORMAL)
        cv.setWindowProperty('Webcam Feed', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)

        if not ret:
            print("Can't receive frame. Exiting ...")
            break

    #trackbars conditions
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
            elif submode == "hough":
                filters.init_hough_trackbars()
            elif submode == "translation":
                geometry.init_translation_trackbars()
            elif submode == "rotation":
                geometry.init_rotation_trackbars()
            elif submode == "scaling":
                geometry.init_scaling_trackbars()

    #function call condition  
        if mode == mode1:
            frame = colors.normal(frame)

        elif mode == mode2:
            if submode == "rgb":
                frame = colors.apply_rgb(frame)
                cv.putText(frame, "[O]pen / [C]lose histogram", (10, 30),
                cv.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

            elif submode == "hsv":
                frame = colors.apply_hsv(frame)
                cv.putText(frame, "[O]pen / [C]lose histogram", (10, 30),
                cv.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

            elif submode == "gray":
                frame = colors.apply_grayscale(frame)
                cv.putText(frame, "[O]pen / [C]lose histogram", (10, 30),
                cv.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

            elif submode == "brightness":
                frame = colors.apply_contrast_brightness(frame)
                cv.putText(frame, "[O]pen / [C]lose histogram", (10, 30),
                cv.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

        
        elif mode == mode3:
            if submode == "gaussian":
                frame = filters.apply_gaussian(frame)

            elif submode == "bilateral":
                frame = filters.apply_bilateral(frame)

            elif submode == "canny":
                frame = filters.apply_canny(frame)

            elif submode == "hough":
                frame = filters.apply_hough(frame)

        elif mode == mode4:
            if submode == "translation":
                frame = geometry.apply_translation(frame)

            elif submode == "rotation":
                frame = geometry.apply_rotation(frame)
                
            elif submode == "scaling":
                frame = geometry.apply_scaling(frame)
    
        elif mode == mode5:
            if not panorama_on:
                cv.putText(frame, "Mode: PANORAMA ('c' to capture, 'r' to reset)", (10,30),
                        cv.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

            if key == ord('c'):
                panorama = panorama_builder.add_frame(frame)
                panorama_on = True
                if panorama is not None:
                    cv.imshow("Panorama", panorama)

            elif key == ord('r') or cv.getWindowProperty("Panorama", cv.WND_PROP_VISIBLE) < 1:
                panorama_on = False
                panorama_builder.reset()
                cv.destroyWindow("Panorama")

                
        elif mode == mode6:
            frame, finished = calibration.run_calibration(frame)
            cv.imshow(window_name, frame)
            key = cv.waitKey(1) & 0xFF
            if finished and (key == ord('c') or cv.getWindowProperty("Calibration Results", cv.WND_PROP_VISIBLE) < 1):
                cv.destroyWindow("Calibration Results")
                calibration.run_calibration(frame, reset=True)  
                mode = mode1

        elif mode == mode7:
            ar.process_frame(frame)

        last_submode = submode  

    #display menu text conditions
        if mode == mode1:
            menu_text = "[C]olors [F]ilters [G]eometry [P]anorama Cal[i]brate [A]R [Q]uit"
        elif mode == mode2:
            menu_text = "[R]GB [H]SV [G]ray [B]rightness/contrast [N]ormal [Q]uit"
        elif mode == mode3:
            menu_text = "[G]aussian B[i]lateral [C]anny [H]ough [N]ormal [Q]uit"
        elif mode == mode4:
            menu_text = "[T]ranslate [R]otate [S]cale [N]ormal [Q]uit"
        elif mode in [mode5, mode6, mode7]:
            menu_text = "[N]ormal [Q]uit"

        cv.putText(frame, menu_text, (10, frame.shape[0]-10),
            cv.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
        cv.imshow(window_name, frame)

    #keys conditions
        key = cv.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('n'):  
            mode = mode1
            submode = None

        elif key == ord('c') and mode==mode1 and submode == None:
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

        elif key == ord('f') and mode==mode1 and submode == None:
            mode = mode3
            submode = None
        elif key == ord('c') and mode == mode3:
            submode = "canny"
        elif key == ord('g') and mode == mode3:
            submode = "gaussian"
        elif key == ord('b') and mode == mode3:
            submode = "bilateral"
        elif key == ord('h') and mode == mode3:
            submode = "hough"

        elif key == ord('g') and mode==mode1 and submode == None:
            mode = mode4
            submode = None
        elif key == ord('t') and mode == mode4:
            submode = "translation"
        elif key == ord('r') and mode == mode4:
            submode = "rotation"
        elif key == ord('s') and mode == mode4:
            submode = "scaling"

        elif key == ord('p') and mode==mode1 and submode == None:
            mode = mode5
            submode = None

        elif key == ord('i') and mode==mode1 and submode == None:
            mode = mode6
            submode = None

        elif key == ord('a') and mode==mode1 and submode == None:
            mode = mode7
            submode = None


        elif key == ord('o') and submode in ["rgb", "hsv", "brightness", "gray"]:
            histograms.show_histogram(frame, submode)
            show_hist = True  

        if show_hist:
            try:
                if key == ord('c') or cv.getWindowProperty("Histogram", cv.WND_PROP_VISIBLE) < 1:
                    cv.destroyWindow("Histogram")
                    show_hist = False
            except cv.error:
                show_hist = False

        if show_hist and submode in ["rgb", "hsv", "gray", "brightness"]: 
            histograms.show_histogram(frame, submode)
        
    cap.release()
    cv.destroyAllWindows()
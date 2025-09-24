import cv2
import numpy as np
import time

CHESSBOARD_SIZE = (9, 6)
SQUARE_SIZE_MM = 25
TARGET_IMAGES = 20

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objp = np.zeros((CHESSBOARD_SIZE[0] * CHESSBOARD_SIZE[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHESSBOARD_SIZE[0], 0:CHESSBOARD_SIZE[1]].T.reshape(-1, 2)
objp *= SQUARE_SIZE_MM

objpoints = []
imgpoints = []
images_captured = 0
last_capture_time = time.time()


def run_calibration(frame, reset=False):
    global objpoints, imgpoints, images_captured, last_capture_time

    if reset:
        objpoints, imgpoints = [], []
        images_captured = 0
        last_capture_time = time.time()
        return frame, False

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret_corners, corners = cv2.findChessboardCorners(gray, CHESSBOARD_SIZE, None)

    display_frame = frame.copy()
    done = False

    if ret_corners:
        cv2.drawChessboardCorners(display_frame, CHESSBOARD_SIZE, corners, ret_corners)
        if time.time() - last_capture_time > 2 and images_captured < TARGET_IMAGES:
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            objpoints.append(objp)
            imgpoints.append(corners2)
            images_captured += 1
            last_capture_time = time.time()

    cv2.putText(display_frame, f"Calibration {images_captured}/{TARGET_IMAGES}", (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    if images_captured >= TARGET_IMAGES:
        print("Performing calibration...")
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
        if ret:
            np.savez('calibration.npz', mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs)
            print("Calibration successful! Saved to calibration.npz")
            print("Camera matrix:\n", mtx)
            print("Distortion coefficients:\n", dist)

            # results popup window
            result_img = np.zeros((400, 600, 3), dtype=np.uint8)
            cv2.putText(result_img, "Calibration Done!", (50, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(result_img, "Results saved to calibration.npz", (50, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            # add distortion and matrix to popup window
            y = 160
            cv2.putText(result_img, "Camera matrix:", (50, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 1)
            for row in mtx:
                y += 30
                text = " ".join([f"{val:.2f}" for val in row])
                cv2.putText(result_img, text, (60, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
            y += 50
            cv2.putText(result_img, "Distortion coeffs:", (50, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 1)
            y += 30
            text = " ".join([f"{val:.3f}" for val in dist.ravel()])
            cv2.putText(result_img, text, (60, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
            
            cv2.imshow("Calibration Results", result_img)

            done = True

    return display_frame, done

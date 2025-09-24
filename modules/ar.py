import cv2
import numpy as np
import os

def draw_text(frame, text, pos=(20, 50), scale=1.0, color=(255, 255, 255)):
    """Draw text with black outline for visibility."""
    thickness = int(scale * 2)
    cv2.putText(frame, text, pos, cv2.FONT_HERSHEY_SIMPLEX, scale,
                (0, 0, 0), thickness + 1, cv2.LINE_AA)
    cv2.putText(frame, text, pos, cv2.FONT_HERSHEY_SIMPLEX, scale,
                color, thickness, cv2.LINE_AA)
    
def estimatePoseSingleMarkers(corners, marker_size, mtx, distortion):
    '''
    This will estimate the rvec and tvec for each of the marker corners detected by:
       corners, ids, rejectedImgPoints = detector.detectMarkers(image)
    corners - is an array of detected corners for each detected marker in the image
    marker_size - is the size of the detected markers
    mtx - is the camera matrix
    distortion - is the camera distortion matrix
    RETURN list of rvecs, tvecs, and trash (so that it corresponds to the old estimatePoseSingleMarkers())
    '''
    marker_points = np.array([[-marker_size / 2, marker_size / 2, 0],
                              [marker_size / 2, marker_size / 2, 0],
                              [marker_size / 2, -marker_size / 2, 0],
                              [-marker_size / 2, -marker_size / 2, 0]], dtype=np.float32)
    trash = []
    rvecs = []
    tvecs = []
    for c in corners:
        nada, R, t = cv2.solvePnP(marker_points, c, mtx, distortion, False, cv2.SOLVEPNP_IPPE_SQUARE)
        rvecs.append(R)
        tvecs.append(t)
        trash.append(nada)
    return rvecs, tvecs, trash


# --- AR Module State ---
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
aruco_params = cv2.aruco.DetectorParameters()
aruco_detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

mtx = np.eye(3)
dist = np.zeros((1, 5))

if os.path.exists('calibration.npz'):
    with np.load('calibration.npz') as X:
        mtx, dist = [X[i] for i in ('mtx', 'dist')]
    print("Calibration data loaded for AR.")
else:
    print("WARNING: 'calibration.npz' not found. AR may be inaccurate.")


def process_frame(frame):
    """Process single frame in AR mode: detect ArUco and draw cube."""
    draw_text(frame, "Mode: AUGMENTED REALITY")

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, _ = aruco_detector.detectMarkers(gray)

    if ids is not None:
        rvecs, tvecs, _ = estimatePoseSingleMarkers(corners, 0.05, mtx, dist)

        axis_len = 0.05
        obj_pts = np.float32([
            [0,0,0], [axis_len,0,0], [axis_len,axis_len,0], [0,axis_len,0],
            [0,0,-axis_len], [axis_len,0,-axis_len], [axis_len,axis_len,-axis_len], [0,axis_len,-axis_len]
        ])
        img_pts, _ = cv2.projectPoints(obj_pts, rvecs[0], tvecs[0], mtx, dist)
        img_pts = np.int32(img_pts).reshape(-1, 2)

        faces = [
            [0, 1, 2, 3],  # bottom
            [4, 5, 6, 7],  # top
            [0, 1, 5, 4],
            [1, 2, 6, 5],
            [2, 3, 7, 6],
            [3, 0, 4, 7],
        ]
        face_colors = [
            (255, 0, 0), (0, 255, 0), (0, 0, 255),
            (255, 255, 0), (255, 0, 255), (0, 255, 255)
        ]

        for idx, face in enumerate(faces):
            cv2.fillConvexPoly(frame, img_pts[face], face_colors[idx], lineType=cv2.LINE_AA)
        for face in faces:
            cv2.polylines(frame, [img_pts[face]], True, (0,0,0), 2, lineType=cv2.LINE_AA)
    else:
        draw_text(frame, "No ArUco markers detected", pos=(20, 80), color=(0, 0, 255))

    return frame

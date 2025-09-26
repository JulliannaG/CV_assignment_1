import cv2
import numpy as np
import os
import math

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

def load_obj(filename):
    vertices = []
    faces = []
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('v '):
                _, x, y, z = line.strip().split()
                vertices.append([float(x), float(y), float(z)])
            elif line.startswith('f '):
                parts = line.strip().split()[1:]
                face = [int(p.split('/')[0]) - 1 for p in parts]
                faces.append(face)

    verts = np.array(vertices, dtype=np.float32)

    #Normalization - too many poligons in .obj file
    verts -= np.mean(verts, axis=0)     
    scale = np.max(np.linalg.norm(verts, axis=1))  
    verts /= scale                       

    return verts, faces

def rotate_x(vertices, angle_deg):
    a = math.radians(angle_deg)
    R = np.array([[1, 0, 0],
                   [0, np.cos(a), -np.sin(a)],
                   [0, np.sin(a),  np.cos(a)]], dtype=np.float32)

    return vertices @ R.T

def rotate_y(vertices, angle_deg):
    a = math.radians(angle_deg)
    R = np.array([[ math.cos(a), 0, math.sin(a)],
                  [0,            1, 0          ],
                  [-math.sin(a), 0, math.cos(a)]], dtype=np.float32)
    return vertices @ R.T

def rotate_z(vertices, angle_deg):
    a = math.radians(angle_deg)
    R = np.array([[np.cos(a), -np.sin(a), 0],
                   [np.sin(a),  np.cos(a), 0],
                   [0, 0, 1]], dtype=np.float32)
    return vertices @ R.T


def process_frame(frame):
    """Process single frame in AR mode: detect ArUco and draw 3D model (T-Rex)."""
    draw_text(frame, "Mode: AUGMENTED REALITY")

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, _ = aruco_detector.detectMarkers(gray)

    if ids is not None:
        rvecs, tvecs, _ = estimatePoseSingleMarkers(corners, 0.05, mtx, dist)

        if model_vertices is not None and len(model_vertices) > 0:
         
            scale = 0.55
            verts = model_vertices.copy()
            verts = rotate_x(verts, 90)
            verts = rotate_z(verts, 90)
            verts = verts * scale 

            img_pts, _ = cv2.projectPoints(verts, rvecs[0], tvecs[0], mtx, dist)
            
            img_pts = np.int32(img_pts).reshape(-1, 2)

            for face in model_faces:
                pts = img_pts[face]
                cv2.fillConvexPoly(frame, pts, (100, 200, 100), lineType=cv2.LINE_AA)
                cv2.polylines(frame, [pts], True, (0, 0, 0), 1, lineType=cv2.LINE_AA)
        else:
            draw_text(frame, "Model not loaded", pos=(20, 80), color=(0, 0, 255))
    else:
        draw_text(frame, "No ArUco markers detected", pos=(20, 80), color=(0, 0, 255))

    return frame


# AR
model_vertices, model_faces = load_obj("modules/trex_model.obj")

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
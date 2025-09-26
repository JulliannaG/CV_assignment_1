import cv2 as cv
import numpy as np

class PanoramaBuilder:
    def __init__(self, ratio=0.75, overshoot=1.3):
        self.base_frame = None
        self.panorama = None
        self.last_added = None
        self.ratio = ratio
        self.overshoot = overshoot 

    def reset(self):
        self.base_frame = None
        self.panorama = None
        self.last_added = None

    def add_frame(self, frame):
        if frame is None:
            return self.panorama

        frame = frame.copy()
        h, w = frame.shape[:2]

        if self.base_frame is None:
            self.base_frame = frame.copy()
            self.panorama = frame.copy()
            self.last_added = frame.copy()
            return self.panorama

        ref_frame = self.last_added
        ref_gray = cv.cvtColor(ref_frame, cv.COLOR_BGR2GRAY)
        frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        sift = cv.SIFT_create()
        kp1, des1 = sift.detectAndCompute(ref_gray, None)
        kp2, des2 = sift.detectAndCompute(frame_gray, None)

        dx = 0
        if des1 is not None and des2 is not None:
            bf = cv.BFMatcher()
            matches = bf.knnMatch(des1, des2, k=2)
            good = [m for m,n in matches if m.distance < self.ratio*n.distance]
            if len(good) >= 4:
                src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1,2)
                dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1,2)
                dx = int(np.mean(dst_pts[:,0] - src_pts[:,0]))

        pano_h, pano_w = self.panorama.shape[:2]

        # adding panorama to the right side
        if dx > 0:
            new_w = pano_w + dx
            new_canvas = np.zeros((pano_h, new_w, 3), dtype=np.uint8)
            new_canvas[:, :pano_w] = self.panorama
            
            copy_w = min(dx, w)
            new_canvas[:, pano_w:pano_w+copy_w] = frame[:, -copy_w:]
            self.panorama = new_canvas

        # adding panorama to the left side
        elif dx < 0:
            dx = -dx
            new_w = pano_w + dx
            new_canvas = np.zeros((pano_h, new_w, 3), dtype=np.uint8)
            new_canvas[:, dx:] = self.panorama
            copy_w = min(dx, w)
            new_canvas[:, :copy_w] = frame[:, :copy_w]
            self.panorama = new_canvas

        self.last_added = frame.copy()
        return self.panorama

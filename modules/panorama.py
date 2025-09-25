import cv2 as cv
import numpy as np

class PanoramaBuilder:
    def __init__(self):  
        self.panorama = None
        self.last_frame = None
        self.T_last = np.eye(3)

    def reset(self):
        self.panorama = None
        self.last_frame = None
        self.T_last = np.eye(3)

    def add_frame(self, frame):
        if frame is None:
            return self.panorama

        if self.panorama is None:
            self.panorama = frame.copy()
            self.last_frame = frame.copy()
            self.T_last = np.eye(3)
            return self.panorama

        # feature detection
        last_gray = cv.cvtColor(self.last_frame, cv.COLOR_BGR2GRAY)
        new_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        sift = cv.SIFT_create()
        kp1, des1 = sift.detectAndCompute(last_gray, None)   # last_frame
        kp2, des2 = sift.detectAndCompute(new_gray, None)    # current frame

        if des1 is None or des2 is None:
            print("[panorama] brak deskryptorów -> pomijam")
            return self.panorama

        bf = cv.BFMatcher()
        matches = bf.knnMatch(des1, des2, k=2)

        good = []
        for m, n in matches:
            if m.distance < 0.85 * n.distance:
                good.append(m)

        if len(good) < 4:
            print("[panorama] za mało dobrych matchy:", len(good))
            return self.panorama

        src_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1,1,2)
        dst_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1,1,2)

        #Panorama only in x axis
        dx = np.mean(src_pts[:,0,0] - dst_pts[:,0,0])
        T = np.array([[1, 0, dx],
                        [0, 1, 0],
                        [0, 0, 1]], dtype=np.float32)

        H_total = self.T_last.dot(T)

        # Panorama canvas
        h_p, w_p = self.panorama.shape[:2]
        h2, w2 = frame.shape[:2]

        corners_new = np.array([[0,0],[w2,0],[w2,h2],[0,h2]], dtype=np.float32).reshape(-1,1,2)
        corners_new_trans = cv.perspectiveTransform(corners_new, H_total)

        corners_pan = np.array([[0,0],[w_p,0],[w_p,h_p],[0,h_p]], dtype=np.float32).reshape(-1,1,2)
        all_corners = np.vstack((corners_pan, corners_new_trans)).reshape(-1,2)

        xmin, ymin = np.int32(np.floor(all_corners.min(axis=0)))
        xmax, ymax = np.int32(np.ceil(all_corners.max(axis=0)))

        tx = -xmin if xmin < 0 else 0
        ty = -ymin if ymin < 0 else 0
        new_w = xmax - xmin
        new_h = ymax - ymin

        T_offset = np.array([[1.0, 0.0, tx],
                             [0.0, 1.0, ty],
                             [0.0, 0.0, 1.0]])

        pano_warped = cv.warpPerspective(self.panorama, T_offset, (new_w, new_h))
        H_to_canvas = T_offset.dot(H_total)
        new_warped = cv.warpPerspective(frame, H_to_canvas, (new_w, new_h))

        # blending
        result = pano_warped.astype(np.float32)
        mask_new = (new_warped.sum(axis=2) > 0)
        mask_pano = (pano_warped.sum(axis=2) > 0)

        only_new = mask_new & ~mask_pano
        result[only_new] = new_warped[only_new].astype(np.float32)

        overlap = mask_new & mask_pano
        if overlap.any():
            result[overlap] = (pano_warped[overlap].astype(np.float32) + new_warped[overlap].astype(np.float32)) / 2.0

        result = np.clip(result, 0, 255).astype(np.uint8)

        self.panorama = result
        self.last_frame = frame.copy()
        self.T_last = H_to_canvas.copy()

        return self.panorama

    def get_panorama(self):
        return self.panorama

    def crop_black(self):
        if self.panorama is None:
            return None
        gray = cv.cvtColor(self.panorama, cv.COLOR_BGR2GRAY)
        _, th = cv.threshold(gray, 1, 255, cv.THRESH_BINARY)
        cnt = cv.findNonZero(th)
        if cnt is None:
            return self.panorama
        x, y, w, h = cv.boundingRect(cnt)
        return self.panorama[y:y+h, x:x+w]

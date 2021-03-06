import cv2
import time
import pathlib
import numpy as np

import common

if __name__ == "__main__":
    OBJ_POINTS = np.zeros((1, common.CHESSBOARD[0] * common.CHESSBOARD[1], 3), np.float32)
    OBJ_POINTS[0,:,:2] = np.mgrid[0:common.CHESSBOARD[0], 0:common.CHESSBOARD[1]].T.reshape(-1, 2) * common.SIZE

    image_points = []
    object_points = []
    for f in pathlib.Path.cwd().glob("*.jpg"):
        # read image
        image = cv2.imread(str(f), cv2.IMREAD_GRAYSCALE)
        # find chessboard corners
        found, corners = cv2.findChessboardCorners(image, common.CHESSBOARD, common.FIND_CHESSBOARD_FLAGS)
        if found:
            # refine corners
            corners = cv2.cornerSubPix(image, corners, (11, 11),(-1, -1), common.SUBPIX_CRITERIA)
            # collect object points
            object_points.append(OBJ_POINTS)
            # collect image points
            image_points.append(corners)
            # draw corners
            image = cv2.drawChessboardCorners(image, common.CHESSBOARD, corners, found)
    camera_matrix_guess = np.array([[1250.0, 0, (common.WIDTH-1)/2.0], [0, 1250.0, (common.HEIGHT-1)/2.0], [0, 0, 1.0]])
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(object_points, image_points, image.shape[::-1], camera_matrix_guess, None, flags = common.CALIBRATE_CAMERA_FLAGS)

    print("Error: ", ret)        
    print("Camera matrix: ")
    print(mtx)
    print("Distortion coeffs: ")
    print(dist)
    print(rvecs)
    print(tvecs)

    common.DumpResults(mtx, dist)

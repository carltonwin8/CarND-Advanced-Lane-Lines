#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Carlton Joseph
"""
import numpy as np
import cv2
import glob

def calibrateCamera(imgGlob, img_size=(1280,720), rows=6, cols=9):
    """
    :param imgGlob: File glob pattern camera calibration images
    :param img_size: Size of image 2
    :param rows: Number of corners in the row of the chessboard images
    :param cols: Number of corners in the column of the chessboard images
    """
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((rows*cols,3), np.float32)
    objp[:,:2] = np.mgrid[0:cols, 0:rows].T.reshape(-1,2)
    
    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d points in real world space
    imgpoints = [] # 2d points in image plane
    
    images = glob.glob(imgGlob)
    if len(images) == 0:
        raise NameError("Found No Images For => " + imgGlob)
    for idx, fname in enumerate(images):
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (cols,rows), None)
        if ret == True:
            objpoints.append(objp)
            imgpoints.append(corners)
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img_size, None, None)
    return mtx, dist

def undistortImage(img, mtx, dist):
    """
    :param img: image
    :param mtx: Camera calibartion mtx value
    :param dist: Camera calibartion dist value
    """
    return cv2.undistort(img, mtx, dist, None, mtx)

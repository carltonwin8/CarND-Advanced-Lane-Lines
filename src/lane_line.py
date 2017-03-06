#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Carlton Joseph
"""
import glob
import numpy as np
import cv2


def calibrate(img_glob, img_size=(1280, 720), rows=6, cols=9):
    """
    :param img_glob: File glob pattern camera calibration images
    :param img_size: Size of image
    :param rows: Number of corners in the row of the chessboard images
    :param cols: Number of corners in the column of the chessboard images
    """
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((rows * cols, 3), np.float32)
    objp[:, :2] = np.mgrid[0:cols, 0:rows].T.reshape(-1, 2)

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d points in real world space
    imgpoints = []  # 2d points in image plane

    images = glob.glob(img_glob)
    if len(images) == 0:
        raise NameError("Found No Images For => " + img_glob)
    for _, fname in enumerate(images):
        gray = cv2.cvtColor(cv2.imread(fname), cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (cols, rows), None)
        if ret:
            objpoints.append(objp)
            imgpoints.append(corners)
    _, mtx, dist, _, _ = cv2.calibrateCamera(objpoints, imgpoints, img_size, None, None)
    return mtx, dist


def undistort(img, mtx, dist):
    """
    :param img: image
    :param mtx: Camera calibration mtx value
    :param dist: Camera calibration dist value
    """
    return cv2.undistort(img, mtx, dist, None, mtx)


def sobel_x_binary(img, thresh_min=20, thresh_max=100):
    """
    :param img: image
    :param s_thresh_min: threshold min
    :param s_thresh_max: threshold max
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0)  # Take the derivative in x
    # below absolute x derivative to accentuate lines away from horizontal
    abs_sobelx = np.absolute(sobelx)
    scaled_sobel = np.uint8(255 * abs_sobelx / np.max(abs_sobelx))
    sxbinary = np.zeros_like(scaled_sobel)
    sxbinary[(scaled_sobel >= thresh_min) & (scaled_sobel <= thresh_max)] = 1
    return sxbinary


def hls_s_binary(img, s_thresh_min=150, s_thresh_max=255):
    """
    :param img: image
    :param s_thresh_min: threshold min
    :param s_thresh_max: threshold max
    """
    hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
    s_channel = hls[:, :, 2]
    s_binary = np.zeros_like(s_channel)
    s_binary[(s_channel >= s_thresh_min) & (s_channel <= s_thresh_max)] = 1
    return s_binary


def combine_binary(img1, img2):
    """
    :param img1: image
    :param img2: image
    """
    combined_binary = np.zeros_like(img1)
    combined_binary[(img1 == 1) | (img2 == 1)] = 1
    return combined_binary

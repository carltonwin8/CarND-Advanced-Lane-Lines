#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. moduleauthor:: Carlton Joseph <carlton.joseph@gmail.com>

"""
import glob
import numpy as np
import cv2


def calibrate(img_glob, img_size=(1280, 720), rows=6, cols=9):
    """
    Creates a cameras calibration information based on the images provided
    
    :param img_glob: File glob pattern camera calibration images
    :param img_size: Size of image
    :param rows: Number of corners in the row of the chessboard images
    :param cols: Number of corners in the column of the chessboard images
    :return: image calibration parameters
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
    Undistorts an image with the provided calibration information
    
    :param img: image
    :param mtx: Camera calibration mtx value
    :param dist: Camera calibration dist value
    :return: undistored image
    """
    return cv2.undistort(img, mtx, dist, None, mtx)


def sobel_x_binary(img, thresh_min=20, thresh_max=100):
    """
    Identifies edges in an image using sobel x and the thresholds provided
    
    :param img: image
    :param s_thresh_min: threshold min
    :param s_thresh_max: threshold max
    :return: binary image
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
    Identifies edeges in an image using the HLS S dimension and the thresholds provided
    
    :param img: image
    :param s_thresh_min: threshold min
    :param s_thresh_max: threshold max
    :return: binary image
    """
    hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
    s_channel = hls[:, :, 2]
    s_binary = np.zeros_like(s_channel)
    s_binary[(s_channel >= s_thresh_min) & (s_channel <= s_thresh_max)] = 1
    return s_binary


def combine_binary(img1, img2):
    """
    Combines two binary images via an OR operator
    :param img1: image
    :param img2: image
    :return: binary image
    """
    combined_binary = np.zeros_like(img1)
    combined_binary[(img1 == 1) | (img2 == 1)] = 1
    return combined_binary

def edge_detect(img):
    """
    Detects the edges by ORing the sobel x and hls s channel threshold detects
    """
    return combine_binary(sobel_x_binary(img),hls_s_binary(img))

def perspective_transform_values(tl=-55, tr=55, bl=-10, br=60, img_size=(1280, 720)):
    """
    Creates perspective transform values
    """
    src = np.float32(
        [[(img_size[0] / 2) + tl, img_size[1] / 2 + 100],
        [((img_size[0] / 6) + bl), img_size[1]],
        [(img_size[0] * 5 / 6) + br, img_size[1]],
        [(img_size[0] / 2 + tr), img_size[1] / 2 + 100]])
    dst = np.float32(
        [[(img_size[0] / 4), 0],
        [(img_size[0] / 4), img_size[1]],
        [(img_size[0] * 3 / 4), img_size[1]],
        [(img_size[0] * 3 / 4), 0]])
    return src, dst

def perspective_transform_map(src, dst):
    M = cv2.getPerspectiveTransform(src, dst)
    return M

def perspective_transform(img, M, img_size=(1280, 720)):
    warped = cv2.warpPerspective(img, M, img_size)
    return warped

def create_lines(points):
    lines = []
    start = points[0]
    for i in range(len(points) - 1):
        end = points[i + 1]
        lines.append([[start[0], start[1], end[0], end[1]]])
        start = end
        
    lines.append([[points[0][0], points[0][1], start[0], start[1]]])
    return lines
    
def draw_lines(img, lines, color=[255, 0, 0], thickness=10, weights=(0.5, 0.5)):
    img2 = np.zeros_like(img)
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(img2, (x1, y1), (x2, y2), color, thickness)
    return cv2.addWeighted(img, weights[0], img2, weights[1], 0)
    
def find_window_centroids(warped, window_width=50, window_height=80, margin=100):
    """
    Find the center of the lane lines
    """
    window_centroids = [] # Store the (left,right) window centroid positions per level
    window = np.ones(window_width) # Create our window template that we will use for convolutions
    
    # First find the two starting positions for the left and right lane by using np.sum to get the vertical image slice
    # and then np.convolve the vertical image slice with the window template 
    
    # Sum quarter bottom of image to get slice, could use a different ratio
    l_sum = np.sum(warped[int(3*warped.shape[0]/4):,:int(warped.shape[1]/2)], axis=0)
    l_center = np.argmax(np.convolve(window,l_sum))-window_width/2
    r_sum = np.sum(warped[int(3*warped.shape[0]/4):,int(warped.shape[1]/2):], axis=0)
    r_center = np.argmax(np.convolve(window,r_sum))-window_width/2+int(warped.shape[1]/2)
    
    # Add what we found for the first layer
    window_centroids.append((l_center,r_center))
    
    # Go through each layer looking for max pixel locations
    for level in range(1,(int)(warped.shape[0]/window_height)):
        # convolve the window into the vertical slice of the image
        image_layer = np.sum(warped[int(warped.shape[0]-(level+1)*window_height):int(warped.shape[0]-level*window_height),:], axis=0)
        conv_signal = np.convolve(window, image_layer)
        # Find the best left centroid by using past left center as a reference
        # Use window_width/2 as offset because convolution signal reference is at right side of window, not center of window
        offset = window_width/2
        l_min_index = int(max(l_center+offset-margin,0))
        l_max_index = int(min(l_center+offset+margin,warped.shape[1]))
        l_center = np.argmax(conv_signal[l_min_index:l_max_index])+l_min_index-offset
        # Find the best right centroid by using past right center as a reference
        r_min_index = int(max(r_center+offset-margin,0))
        r_max_index = int(min(r_center+offset+margin,warped.shape[1]))
        r_center = np.argmax(conv_signal[r_min_index:r_max_index])+r_min_index-offset
        # Add what we found for that layer
        window_centroids.append((l_center,r_center))

    return window_centroids

def window_mask(width, height, img_ref, center,level):
    output = np.zeros_like(img_ref)
    output[int(img_ref.shape[0]-(level+1)*height):int(img_ref.shape[0]-level*height),max(0,int(center-width/2)):min(int(center+width/2),img_ref.shape[1])] = 1
    return output

def draw_window_centroids(warped, window_centroids, window_width=50, window_height=80):
    """
    Identify lane lines in a binary image
    """
    # Points used to draw all the left and right windows
    l_points = np.zeros_like(warped)
    r_points = np.zeros_like(warped)

    # Go through each level and draw the windows
    for level in range(0,len(window_centroids)):
        # Window_mask is a function to draw window areas
        l_mask = window_mask(window_width, window_height, warped, window_centroids[level][0], level)
        r_mask = window_mask(window_width, window_height, warped, window_centroids[level][1], level)
        # Add graphic points from window mask here to total pixels found 
        l_points[(l_points == 255) | ((l_mask == 1) ) ] = 255
        r_points[(r_points == 255) | ((r_mask == 1) ) ] = 255

    # Draw the results
    template = np.array(r_points+l_points,np.uint8) # add both left and right window pixels together
    zero_channel = np.zeros_like(template) # create a zero color channle 
    template = np.array(cv2.merge((zero_channel,template,zero_channel)),np.uint8) # make window pixels green
    warpage = np.array(cv2.merge((warped*255,warped*255,warped*255)),np.uint8) # making the original road pixels 3 color channels
    output = cv2.addWeighted(warpage, 1.0, template, 0.5, 0.0) # overlay the orignal road image with window results
    return output
    

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Carlton Joseph
"""
import glob
import numpy as np
import cv2
import display

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
    
    Args:
        img: image
        s_thresh_min: threshold min
        s_thresh_max: threshold max
    
    Returns: binary image
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0)  # Take the derivative in x
    # below absolute x derivative to accentuate lines away from horizontal
    abs_sobelx = np.absolute(sobelx)
    scaled_sobel = np.uint8(255 * abs_sobelx / np.max(abs_sobelx))
    sxbinary = np.zeros_like(scaled_sobel)
    sxbinary[(scaled_sobel >= thresh_min) & (scaled_sobel <= thresh_max)] = 1
    return sxbinary


def hls_s_binary(img, s_thresh_min=180, s_thresh_max=255):
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

def threshold(img, sbl_x_thres_min, sbl_x_thres_max, hls_s_thres_min, hls_s_thres_max):
    """
    Detects the edges by ORing the sobel x and hls s channel threshold detects
    """
    sxb = sobel_x_binary(img, sbl_x_thres_min, sbl_x_thres_max)
    hsb = hls_s_binary(img, hls_s_thres_min, hls_s_thres_max)
    cmb = combine_binary(sxb,hsb)
    display.imshow([sxb,hsb,cmb], cmap='gray', show=False)
    return cmb

def perspective_transform_values(tl=-60, tr=60, bl=-10, br=40, img_size=(1280, 720)):
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
    """
    Draw lines on an image
    
    Args:
        img (array): RGB image
        lines (array): Containing the points of the line
        thickness (int): The thickness fo the line
    
    Returns:
        img: RGB image    
    """    
    img2 = np.zeros_like(img)
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(img2, (x1, y1), (x2, y2), color, thickness)
    return cv2.addWeighted(img, weights[0], img2, weights[1], 0)
    
def fit_poly(binary_warped, img_size=(1280, 720)):
    ## use to get histogram for part of the binary image
    # Take a histogram of the bottom half of the image
    histogram = np.sum(binary_warped[int(binary_warped.shape[0]/2):,:], axis=0)
    # Find the peak of the left and right halves of the histogram
    # These will be the starting point for the left and right lines
    midpoint = np.int(histogram.shape[0]/2)
    leftx_base = np.argmax(histogram[:midpoint])
    rightx_base = np.argmax(histogram[midpoint:]) + midpoint

    # Choose the number of sliding windows
    nwindows = 9
    # Set height of windows
    window_height = np.int(binary_warped.shape[0]/nwindows)
    # Identify the x and y positions of all nonzero pixels in the image
    nonzero = binary_warped.nonzero()
    nonzeroy = np.array(nonzero[0])
    nonzerox = np.array(nonzero[1])
    # Current positions to be updated for each window
    leftx_current = leftx_base
    rightx_current = rightx_base
    # Set the width of the windows +/- margin
    margin = 120
    # Set minimum number of pixels found to recenter window
    minpix = 50
    # Create empty lists to receive left and right lane pixel indices
    left_lane_inds = []
    right_lane_inds = []

    # Step through the windows one by one
    for window in range(nwindows):
        # Identify window boundaries in x and y (and right and left)
        win_y_low = binary_warped.shape[0] - (window+1)*window_height
        win_y_high = binary_warped.shape[0] - window*window_height
        win_xleft_low = leftx_current - margin
        win_xleft_high = leftx_current + margin
        win_xright_low = rightx_current - margin
        win_xright_high = rightx_current + margin
        # Identify the nonzero pixels in x and y within the window
        good_left_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & (nonzerox >= win_xleft_low) & (nonzerox < win_xleft_high)).nonzero()[0]
        good_right_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & (nonzerox >= win_xright_low) & (nonzerox < win_xright_high)).nonzero()[0]
        # Append these indices to the lists
        left_lane_inds.append(good_left_inds)
        right_lane_inds.append(good_right_inds)
        # If you found > minpix pixels, recenter next window on their mean position
        if len(good_left_inds) > minpix:
            leftx_current = np.int(np.mean(nonzerox[good_left_inds]))
        if len(good_right_inds) > minpix:
            rightx_current = np.int(np.mean(nonzerox[good_right_inds]))

    # Concatenate the arrays of indices
    left_lane_inds = np.concatenate(left_lane_inds)
    right_lane_inds = np.concatenate(right_lane_inds)
    
    left_fit, right_fit, left_curverad, \
    right_curverad, left_fit_cr, right_fit_cr = \
        get_poly(nonzerox, nonzeroy, left_lane_inds, right_lane_inds)

    return left_fit, right_fit, left_curverad, right_curverad, left_fit_cr, right_fit_cr   
        
    
def get_poly(nonzerox, nonzeroy, left_lane_inds, right_lane_inds):
     # Extract left and right line pixel positions
    leftx = nonzerox[left_lane_inds]
    lefty = nonzeroy[left_lane_inds]
    rightx = nonzerox[right_lane_inds]
    righty = nonzeroy[right_lane_inds]

    # Fit a second order polynomial to each
    left_fit = np.polyfit(lefty, leftx, 2)
    right_fit = np.polyfit(righty, rightx, 2)
    
    # Define conversions in x and y from pixels space to meters
    ym_per_pix = 30/720 # meters per pixel in y dimension
    xm_per_pix = 3.7/700 # meters per pixel in x dimension
    
    # Fit new polynomials to x,y in world space
    ly_eval = np.max(lefty)
    ry_eval = np.max(righty)
    left_fit_cr = np.polyfit(lefty*ym_per_pix, leftx*xm_per_pix, 2)
    right_fit_cr = np.polyfit(righty*ym_per_pix, rightx*xm_per_pix, 2)
    # Calculate the new radii of curvature
    left_curverad = ((1 + (2*left_fit_cr[0]*ly_eval*ym_per_pix + left_fit_cr[1])**2)**1.5) / np.absolute(2*left_fit_cr[0])
    right_curverad = ((1 + (2*right_fit_cr[0]*ry_eval*ym_per_pix + right_fit_cr[1])**2)**1.5) / np.absolute(2*right_fit_cr[0])
    
    return left_fit, right_fit, left_curverad, right_curverad, left_fit_cr, right_fit_cr   

def fit_poly_noslide(binary_warped, left_fit, right_fit, img_size=(1280, 720)):
    """
    find line pixels with a warped binary image 
    from the next frame of video (also called "binary_warped")
    """
    nonzero = binary_warped.nonzero()
    nonzeroy = np.array(nonzero[0])
    nonzerox = np.array(nonzero[1])
    margin = 100
    left_lane_inds = ((nonzerox > (left_fit[0]*(nonzeroy**2) + left_fit[1]*nonzeroy + left_fit[2] - margin)) & (nonzerox < (left_fit[0]*(nonzeroy**2) + left_fit[1]*nonzeroy + left_fit[2] + margin))) 
    right_lane_inds = ((nonzerox > (right_fit[0]*(nonzeroy**2) + right_fit[1]*nonzeroy + right_fit[2] - margin)) & (nonzerox < (right_fit[0]*(nonzeroy**2) + right_fit[1]*nonzeroy + right_fit[2] + margin)))  
    
    # Again, extract left and right line pixel positions
    leftx = nonzerox[left_lane_inds]
    lefty = nonzeroy[left_lane_inds] 
    rightx = nonzerox[right_lane_inds]
    righty = nonzeroy[right_lane_inds]
    # Fit a second order polynomial to each
    left_fit = np.polyfit(lefty, leftx, 2)
    right_fit = np.polyfit(righty, rightx, 2)
    
    left_fit, right_fit, left_curverad, \
    right_curverad, left_fit_cr, right_fit_cr = \
        get_poly(nonzerox, nonzeroy, left_lane_inds, right_lane_inds)

    return left_fit, right_fit, left_curverad, right_curverad, left_fit_cr, right_fit_cr   


def poly2image(img, left_fit, right_fit, Minv):
    # Generate x and y values for plotting
    ploty = np.linspace(0, img.shape[0]-1, img.shape[0] )
    left_fitx = left_fit[0]*ploty**2 + left_fit[1]*ploty + left_fit[2]
    right_fitx = right_fit[0]*ploty**2 + right_fit[1]*ploty + right_fit[2]
    
    # Create an image to draw the lines on
    warp_zero = np.zeros_like(img).astype(np.uint8)
    #color_warp = np.dstack((warp_zero, warp_zero, warp_zero))
    color_warp = warp_zero
    # Recast the x and y points into usable format for cv2.fillPoly()
    pts_left = np.array([np.transpose(np.vstack([left_fitx, ploty]))])
    pts_right = np.array([np.flipud(np.transpose(np.vstack([right_fitx, ploty])))])
    pts = np.hstack((pts_left, pts_right))
    
    # Draw the lane onto the warped blank image
    cv2.fillPoly(color_warp, np.int_([pts]), (0,255, 0))
    
    # Warp the blank back to original image space using inverse perspective matrix (Minv)
    newwarp = cv2.warpPerspective(color_warp, Minv, (img.shape[1], img.shape[0])) 
    # Combine the result with the original image
    result = cv2.addWeighted(img, 1, newwarp, 0.3, 0)
    return result

    
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
    """
    Create a mask for a window region
    """
    output = np.zeros_like(img_ref)
    y_start = int(img_ref.shape[0]-(level+1)*height)
    y_end = int(img_ref.shape[0]-level*height)
    x_start = max(0,int(center-width/2))
    x_end = min(int(center+width/2),img_ref.shape[1])
    output[y_start:y_end, x_start:x_end] = 1
    return output

def lane_mask(warped, window_centroids, window_width=50, window_height=80):
    """
    Create the mask for the right and left lane
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

    return l_points, r_points

class Line():
    def __init__(self):
        # was the line detected in the last iteration?
        self.detected = False  
        # x values of the last n fits of the line
        self.recent_xfitted = np.array([]) 
        self.recent_rc = np.array([])
        #average x values of the fitted line over the last n iterations
        self.bestx = None     
        #polynomial coefficients averaged over the last n iterations
        self.best_fit = None  
        #polynomial coefficients for the most recent fit
        self.current_fit = [np.array([False])]  
        #radius of curvature of the line in some units
        self.radius_of_curvature = None 
        #distance in meters of vehicle center from the line
        self.line_base_pos = None 
        #difference in fit coefficients between last and new fits
        self.diffs = np.array([0,0,0], dtype='float') 
        #x values for detected line pixels
        self.allx = None  
        #y values for detected line pixels
        self.ally = None
    
    def check_resutls(self, fit, radius):
        return fit, radius
        
    def history(self):
        return self.recent_xfitted, self.recent_rc

class find_lane_lines():
    """
    find image lane line for given camera calibartion and perspective transform 
    values
    """
    def __init__(self, mtx, dist, src, dst, M, Minv, 
                 sbl_x_thres_min, sbl_x_thres_max, hls_s_thres_min, 
                 hls_s_thres_max, log, retpt=False):
        self.mtx = mtx
        self.dist = dist
        self.src = src
        self.dst = dst
        self.M = M
        self.Minv = Minv
        self.retpt = retpt
        self.check_l = Line()
        self.check_r = Line()
        self.log = log
        self.sbl_x_thres_min = sbl_x_thres_min
        self.sbl_x_thres_max = sbl_x_thres_max
        self.hls_s_thres_min = hls_s_thres_min
        self.hls_s_thres_max = hls_s_thres_max
        self.first = True
        self.lf_old = None
        self.rf_old = None
            
    def fll(self, img):
        undist = undistort(img, self.mtx, self.dist)
        thresh = threshold(undist, self.sbl_x_thres_min, self.sbl_x_thres_max, 
                           self.hls_s_thres_min, self.hls_s_thres_max)
        pt = perspective_transform(thresh, self.M)
        if self.retpt:
            return pt

        if self.first:
            lf_f, rf_f, lc_f, rc_f, lf_cr, rf_cr = fit_poly(pt)
            self.first = False;
        else:
            lf_f, rf_f, lc_f, rc_f, lf_cr, rf_cr = fit_poly_noslide(pt, self.lf_old, self.rf_old)            
        self.lf_old = lf_f
        self.rf_old = rf_f
            
        lf, lc = self.check_l.check_resutls(lf_f, lc_f)
        rf, rc = self.check_r.check_resutls(rf_f, rc_f)
        ll = poly2image(undist, lf, rf, self.Minv)

        left_base_undist = lf_cr[2]*self.src[1][0]/self.dst[1][0]
        right_base_undist = rf_cr[2]*self.src[2][0]/self.dst[2][0]        
        offset = (left_base_undist + right_base_undist)/2 - img.shape[0]*3.7/700/2
        
        text = "Left/Right Curvatures = {:5.0f}/{:5.0f}, offset = {:3.1f} (meters)".format(
                  lc, rc, offset)
        out = cv2.putText(ll, text, (100,50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255), 2)
        self.log.data(lf, rf, lc_f, rc_f, left_base_undist, right_base_undist, offset)
        return out
    
    def history(self):
        return  self.check_l.history(), self.check_r.history()
    
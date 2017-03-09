#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Carlton Joseph
"""
import pickle
import numpy as np
import cv2
import lane_line as ll

class fn():
    """
    Class to contain all the file names used by screen.py and files.py
    """
    pickle_file = '../dist_pickle.p'
    cal_glob = '../camera_cal/calibration*.jpg'
    cal_test_img = '../camera_cal/calibration1.jpg'
    cal_test_img_undist = '../output_images/calibration1_undist.jpg'
    test_img1 = '../test_images/straight_lines1.jpg'
    test_img2 = '../test_images/straight_lines2.jpg'
    test_img1_undist = '../output_images/straight_lines1_undist.jpg'
    test_img1_sobel_x = '../output_images/straight_lines1_sobel_x.jpg'
    test_img1_hls_s = '../output_images/straight_lines1_hls_s.jpg'
    test_img1_sxs = '../output_images/straight_lines1_sxs.jpg'
    test_img1_sxs_c = '../output_images/straight_lines1_sxs_c.jpg'
    test_img1_trans = '../output_images/straight_lines1_trans.jpg'
    test_img1_sxs_trans = '../output_images/straight_lines1_sxs_trans.jpg'
    test_img1_sxs_trans_nl = '../output_images/straight_lines1_sxs_trans_nl.jpg'
    test1 = '../test_images/test1.jpg'
    test2 = '../test_images/test2.jpg'
    test3 = '../test_images/test3.jpg'
    test4 = '../test_images/test4.jpg'
    test5 = '../test_images/test5.jpg'
    test6 = '../test_images/test6.jpg'
    testset = [test_img1, test_img2, test1, test2, test3, test4, test5, test6]
    testset2 = [test4, test5]
    testset3 = [test4]
    
    def temp(name, post):
        base = name.split('/')[-1]
        no_ext = base.split('.')[0]
        return '../tmp/' + no_ext + '_' + post +'.jpg'
    
def distort_save(file, mtx, dist):
    """
    Saves a distortion matrix to a file
    
    :param file: Filename to save undistorted parameters
    :param mtx: Camera calibartion mtx value
    :param dist: Camera calibartion dist value
    :return: None
    """
    dist_pickle = {}
    dist_pickle["mtx"] = mtx
    dist_pickle["dist"] = dist
    pickle.dump(dist_pickle, open(file, "wb"))

def distort_load(file):
    """
    Loads a distortion matrix from a file
    
    :param file: Filename to save undistorted parameters
    :return: map containing a distortion matrix
    """
    dist_pickle = pickle.load(open(file, "rb"))
    return dist_pickle['mtx'], dist_pickle['dist']

def calibrate(execute):
    if execute:
        mtx, dist = ll.calibrate(fn.cal_glob)
        distort_save(fn.pickle_file, mtx, dist)
        
def bin2color(img):
    """
    Converts a binary image to a full scale RGB Image
    """
    img255 = img*255
    rgb255 = np.dstack((img255, img255, img255))
    return rgb255

def bin22color(img1, img2):
    """
    Converts two binary image to a full scale RGB image with 
    """
    return np.dstack((img1*255, np.zeros_like(img1), img2*255))

class perspective_transform():
    """
    Class to help test out various transform values and determine which is best
    """
    def __init__(self, tl=-55, bl=-10, br=60, tr=55, size=(1280, 720)):
        self.tl = tl
        self.bl = bl
        self.br = br
        self.tr = tr
        self.img_size = (1280, 720)
        self.src = None
        self.dst = None 
        
    def transform(self, img):
        src, dst = ll.perspective_transform_values(self.tl, self.tr, self.bl, self.br, self.img_size)
        M = ll.perspective_transform_map(src, dst)
        self.src, self.dst = src, dst
        return cv2.warpPerspective(img, M, self.img_size)
        
    def transform_l(self, img):
        src, dst = ll.perspective_transform_values(self.tl, self.tr, self.bl, self.br, self.img_size)
        M = ll.perspective_transform_map(src, dst)
        persp = cv2.warpPerspective(img, M, self.img_size)
        lines = ll.create_lines(dst)
        perspll = ll.draw_lines(persp, lines)
        self.src, self.dst = src, dst
        return perspll
    
    def file_post(self):
        return str(self.tl) + str(self.tr) + str(self.bl) + str(self.br)
    
def draw_window_centroids(warped, l_points, r_points, weights=(0.5, 0.5)):
    """
    Draw centroids on an image
    """
    # Draw the results
    # add both left and right window pixels together
    template = np.array(r_points+l_points,np.uint8) 
    zero_channel = np.zeros_like(template) # create a zero color channle 
    # make window pixels green
    template = np.array(cv2.merge((zero_channel,template,zero_channel)),np.uint8) 
    # making the original road pixels 3 color channels
    warpage = np.array(cv2.merge((warped,warped,warped)),np.uint8)
    # overlay the orignal road image with window results
    output = cv2.addWeighted(warpage, weights[0], template, weights[1], 0.0)
    return output
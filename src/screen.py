#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Carlton Joseph
"""
import cv2
import matplotlib.pyplot as plt
import lane_line as ll
import utils as utl


def main():
    """
    Displays processed images on screen to verify they the image pipeline
    """
    #mtx, dist = ll.calibrate('../camera_cal/calibration*.jpg')
    pickle = '../dist_pickle.p'
    #utl.distort_save(pickle, mtx, dist)
    mtx, dist = utl.distort_load(pickle)
    cal_test_img = '../camera_cal/calibration1.jpg'
    img_dist = cv2.imread(cal_test_img)
    img_undist = ll.undistort(img_dist, mtx, dist)
    plt.imshow(img_dist)
    plt.imshow(img_undist)
    img_name = '../output_images/straight_lines1_undist.jpg' # undistorted image
    img = cv2.imread(img_name)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    img_sx_b = ll.sobel_x_binary(img)
    plt.imshow(img_sx_b, cmap='gray')
    plt.show()
    img_hls_sb = ll.hls_s_binary(img)
    plt.imshow(img_hls_sb, cmap='gray')
    plt.show()
    img_sxb = ll.combine_binary(img_sx_b, img_hls_sb)
    plt.imshow(img_sxb, cmap='gray')


if __name__ == "__main__":
    main()

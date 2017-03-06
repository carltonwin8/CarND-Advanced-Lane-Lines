#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Carlton Joseph
"""
import cv2
import lane_line as ll
import utils as utl

def add_file_name_ps(file, insert):
    """
    :param file: file storage path
    :param insert: text to insert into path
    """
    paths = file.split('/')
    pre_post = paths[-1].split('.')
    return '../output_images/' + pre_post[0] + '_' + insert + '.' + pre_post[1]

def main():
    """
    Generate image file for documentation
    """
    mtx, dist = ll.calibrate('../camera_cal/calibration*.jpg')
    pickle_file = '../dist_pickle.p'
    utl.distort_save(pickle_file, mtx, dist)
    mtx, dist = utl.distort_load(pickle_file)
    cal_test_img_fn = '../camera_cal/calibration1.jpg'
    cal_test_img_dist = cv2.imread(cal_test_img_fn)
    cal_test_img_undist = ll.undistort(cal_test_img_dist, mtx, dist)
    test_img1_fn = '../test_images/straight_lines1.jpg'
    test_img1_dist = cv2.imread(test_img1_fn)
    test_img1_undist = ll.undistort(test_img1_dist, mtx, dist)
    cv2.imwrite(add_file_name_ps(cal_test_img_fn, 'undist'), cal_test_img_undist)
    cv2.imwrite(add_file_name_ps(test_img1_fn, 'undist'), test_img1_undist)

if __name__ == "__main__":
    main()

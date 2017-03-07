#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Carlton Joseph
"""
import cv2
import matplotlib.pyplot as plt
import lane_line as ll
import utils as utl


def imshow(img, show=True, cmap=None):
    if show:
        if cmap == None:
            plt.imshow(img)
        else:
            plt.imshow(img, cmap="gray")
        plt.show()
    

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
    imshow(img_dist, show=False)
    imshow(img_undist, show=False)
    img_name = '../output_images/straight_lines1_undist.jpg' # undistorted image
    img = ll.undistort(cv2.imread(img_name), mtx, dist)
    imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), show=False)
    img_sx_b = ll.sobel_x_binary(img)
    imshow(img_sx_b, cmap='gray', show=False)
    img_hls_sb = ll.hls_s_binary(img)
    imshow(img_hls_sb, cmap='gray', show=False)
    img_sxb = ll.combine_binary(img_sx_b, img_hls_sb)
    imshow(img_sxb, cmap='gray', show=False)
    img_pt = utl.perspective_transform(img)
    imshow(img_pt, show=False)
    img_sxb_pt = utl.perspective_transform(img_sxb)
    imshow(img_sxb_pt, cmap='gray', show=False)
    src, dst = ll.perspective_transform_values()
    lines = ll.create_lines(src)
    imshow(cv2.cvtColor(ll.draw_lines(img, lines), cv2.COLOR_BGR2RGB),show=False)
    img_sxb_ptc = ll.bin2color(img_sxb_pt)
    imshow(img_sxb_ptc, show=False)
    img_sxb_ptc_l = ll.draw_lines(img_sxb_ptc, ll.create_lines(dst))
    imshow(img_sxb_ptc_l, show=True)
    centroids = ll.find_window_centroids(img_sxb_ptc)
    print(len(centroids))
if __name__ == "__main__":
    main()

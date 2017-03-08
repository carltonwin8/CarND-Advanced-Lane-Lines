#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Carlton Joseph
"""
import cv2
import matplotlib.pyplot as plt
import lane_line as ll
import utils as utl


def imshow(img, cmap=None, show=True):
    if show:
        if cmap == None:
            plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        else:
            plt.imshow(img, cmap="gray")
        plt.show()

def undistort1(fn, mtx, dist, execute):
    if execute:
        img_dist = cv2.imread(fn)
        img_undist = ll.undistort(img_dist, mtx, dist)
        imshow(img_dist)
        imshow(img_undist)
    

def undistort(execute):
    if execute:
        mtx, dist = utl.distort_load(utl.fn.pickle_file)
        undistort1(utl.fn.cal_test_img, mtx, dist, False)
        undistort1(utl.fn.test_img1, mtx, dist, False)

def edge_detect(execute):
    if execute:
        img = cv2.imread(utl.fn.test_img1_undist)
        img_sx_b = ll.sobel_x_binary(img)
        imshow(img_sx_b, cmap='gray', show=True)
        img_hls_sb = ll.hls_s_binary(img)
        imshow(img_hls_sb, cmap='gray', show=True)
        img_sxb = ll.combine_binary(img_sx_b, img_hls_sb)
        imshow(img_sxb, cmap='gray', show=True)
        imshow(utl.bin22color(img_sx_b, img_hls_sb), show=True)

def transform(execute):
    if execute:
        fn = utl.fn.test_img1_sxs
        img = cv2.imread(fn)
        pt = utl.perspective_transform()
        pt.tl = -60
        pt.tr = 60
        pt.br = 40
        imshow(pt.transform_l(img))
        print(pt.src)
        print(pt.dst)
        
def identify_line(execute):
        centroids = ll.find_window_centroids(img_sxb_ptc)
        print(len(centroids))
        
def main():
    """
    Displays processed images on screen to verify they the image pipeline
    """
    utl.calibrate(False)
    undistort(False)
    edge_detect(False)
    transform(True)

if __name__ == "__main__":
    main()

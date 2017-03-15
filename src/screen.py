#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Carlton Joseph
"""
import cv2
import lane_line as ll
import utils as utl
import display
import config

def undistort1(fn, mtx, dist, execute):
    if execute:
        img_dist = cv2.imread(fn)
        img_undist = ll.undistort(img_dist, mtx, dist)
        display.imshow([img_dist, img_undist])
    

def undistort(execute):
    if execute:
        mtx, dist = utl.distort_load(utl.fn.pickle_file)
        undistort1(utl.fn.cal_test_img, mtx, dist, False)
        undistort1(utl.fn.test_img1, mtx, dist, False)

def edge_detect(execute):
    if execute:
        img = cv2.imread(utl.fn.test_img1_undist)
        img_sx_b = ll.sobel_x_binary(img)
        display.imshow(img_sx_b, cmap='gray', show=True)
        img_hls_sb = ll.hls_s_binary(img)
        display.imshow(img_hls_sb, cmap='gray', show=True)
        img_sxb = ll.combine_binary(img_sx_b, img_hls_sb)
        display.imshow(img_sxb, cmap='gray', show=True)
        display.imshow([[img_sx_b,'gray'],])
        display.imshow(utl.bin22color(img_sx_b, img_hls_sb), show=True)

def transform(execute):
    if execute:
        fn = utl.fn.test_img1_sxs
        img = cv2.imread(fn)
        pt = utl.perspective_transform()
        pt.tl = -60
        pt.tr = 60
        pt.br = 40
        display.imshow(pt.transform_l(img))
        print(pt.src)
        print(pt.dst)
     
def identify_line(execute):
    if execute:
        pass



def lane_line(execute):
    if execute:
        mtx, dist = utl.distort_load(utl.fn.pickle_file)
        src, dst = ll.perspective_transform_values()
        M = ll.perspective_transform_map(src, dst)
        Minv = ll.perspective_transform_map(dst,src)
        
        combinations = config.get_combinations(1)
        log = utl.log("../../project/img.log")

        for combo in combinations:
            sbl_x_thres_min, sbl_x_thres_max, hls_s_thres_min, hls_s_thres_max = combo  
            fl = ll.find_lane_lines(mtx, dist, src, dst, M, Minv,
                                    sbl_x_thres_min, sbl_x_thres_max, 
                                    hls_s_thres_min, hls_s_thres_max, log)
            for imgfn in utl.fn.testset2:
                img = cv2.imread(imgfn)
                print(imgfn, sbl_x_thres_min, sbl_x_thres_max, 
                      hls_s_thres_min, hls_s_thres_max)
                #display.imshow(img)            
                display.imshow(fl.fll(img))
        
def main():
    """
    Displays processed images on screen to verify they the image pipeline
    """
    utl.calibrate(False)
    undistort(False)
    edge_detect(False)
    transform(False)
    identify_line(False)
    lane_line(True)    
    
if __name__ == "__main__":
    main()

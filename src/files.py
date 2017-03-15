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

def undistort(execute):
    if execute:
        mtx, dist = utl.distort_load(utl.fn.pickle_file)
        cal_test_img_dist = cv2.imread(utl.fn.cal_test_img)
        cal_test_img_undist = ll.undistort(cal_test_img_dist, mtx, dist)
        test_img1_dist = cv2.imread(utl.fn.test_img1)
        test_img1_undist = ll.undistort(test_img1_dist, mtx, dist)
        cv2.imwrite(utl.fn.cal_test_img_undist, cal_test_img_undist)
        cv2.imwrite(utl.fn.test_img1_undist, test_img1_undist)

def edge_detect(execute):
    if execute:
        img = cv2.imread(utl.fn.test_img1_undist)
        img_sx_b = ll.sobel_x_binary(img)
        cv2.imwrite(utl.fn.test_img1_sobel_x, img_sx_b*255)
        img_hls_sb = ll.hls_s_binary(img)
        cv2.imwrite(utl.fn.test_img1_hls_s, img_hls_sb*255)
        img_sxb = ll.combine_binary(img_sx_b, img_hls_sb)
        cv2.imwrite(utl.fn.test_img1_sxs, img_sxb*255)
        img_sxbc = utl.bin22color(img_hls_sb, img_sxb)
        cv2.imwrite(utl.fn.test_img1_sxs_c, img_sxbc)
       
def transform(execute):
    if execute:
        fn = utl.fn.test_img1_sxs
        img = cv2.imread(fn)
        pt = utl.perspective_transform()
        pt.tl = -60
        pt.tr = 60
        pt.br = 40
        tuning = False
        if tuning == True: # temp storage during tuning above values
            cv2.imwrite(utl.fn.temp(fn, pt.file_post()), pt.transform_l(img))
        else:
            cv2.imwrite(utl.fn.test_img1_sxs_trans, pt.transform_l(img))
            cv2.imwrite(utl.fn.test_img1_sxs_trans_nl, pt.transform(img))
            cv2.imwrite(utl.fn.test_img1_trans, pt.transform_l(cv2.imread(utl.fn.test_img1_undist)))
        
def identify_line(execute):
    if execute:
        img = cv2.imread(utl.fn.test_img1_sxs_trans_nl)
        channel = img[:, :, 0]
        centroids = ll.find_window_centroids(channel)
        print(centroids)
        output = ll.draw_window_centroids(channel, centroids)
        print(output.shape)
        display.imshow(output)

        
def lane_line(execute):
    if execute:
        mtx, dist = utl.distort_load(utl.fn.pickle_file)
        src, dst = ll.perspective_transform_values()
        M = ll.perspective_transform_map(src, dst)
        Minv = ll.perspective_transform_map(dst,src)
        
        combinations = config.get_combinations(1)
        log = utl.log("../../project/img.log")
        utl_fn = utl.fn()
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
                cv2.imwrite(utl_fn.output(imgfn), fl.fll(img))
def main():
    """
    Generate image files for the documentation
    """
    utl.calibrate(False)
    undistort(False)    
    edge_detect(False)
    transform(False)
    identify_line(False)
    lane_line(True)

if __name__ == "__main__":
    main()

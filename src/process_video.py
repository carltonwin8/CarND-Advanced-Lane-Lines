#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: carltonj2000
"""
from moviepy.editor import VideoFileClip
import lane_line as ll
import utils as utl
import argparse
import sys
import config

def main():
    parser = argparse.ArgumentParser(description='Process video file.')
    group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument("videos", help="video sequence",type=int)
    group.add_argument("-r", "--tranges", help="threshold ranges", type=int, default=-1)
    group.add_argument("-c", "--tcombinations", help="threshold combinations", type=int, default=-1)
    args = parser.parse_args()
            
    if args.tranges != -1:
        sbl_x_thres_mins, sbl_x_thres_maxs, hls_s_thres_mins, hls_s_thres_maxs = config.get_thresholds(args.tranges)
        print(sbl_x_thres_mins, sbl_x_thres_maxs, hls_s_thres_mins, hls_s_thres_maxs)
    if args.tcombinations != -1:
        combinations = config.combinations(args.tcombinations)
        print(combinations)
    videos_in = config.get_videos(args.videos)
    print(videos_in)
    
    logbase = "../../project_video/"  
    
    mtx, dist = utl.distort_load(utl.fn.pickle_file)
    src, dst = ll.perspective_transform_values()
    M = ll.perspective_transform_map(src, dst)
    Minv = ll.perspective_transform_map(dst,src)
    
    
    
    def calc(sbl_x_thres_min, sbl_x_thres_max, 
             hls_s_thres_min, hls_s_thres_max):
        
        for video_in in videos_in:
            file, ext = video_in.split('/')[-1].split('.')
            logdir = logbase + file
            log = utl.log(logdir)
            name = str(sbl_x_thres_min) + '_' + str(sbl_x_thres_max) + '_' + \
                str(hls_s_thres_min)  + '_' + str(hls_s_thres_max)
            video_out = '../../out/' + file + '_' + name + '.' + ext
            
            print("From =>", video_in, "To =>", video_out)
            fl = ll.find_lane_lines(mtx, dist, src, dst, M, Minv,
                                    sbl_x_thres_min, sbl_x_thres_max, 
                                    hls_s_thres_min, hls_s_thres_max, log)
             
    
            clip2 = VideoFileClip(video_in)
            clip = clip2.fl_image(fl.fll)
            clip.write_videofile(video_out, audio=False)

    if args.tranges != -1:
        for sbl_x_thres_min in sbl_x_thres_mins:
            for sbl_x_thres_max in sbl_x_thres_maxs:
                for hls_s_thres_min in hls_s_thres_mins:
                    for hls_s_thres_max in hls_s_thres_maxs:
                        calc(sbl_x_thres_min, sbl_x_thres_max, 
                             hls_s_thres_min, hls_s_thres_max)
    elif args.tcombinations != -1:
        for combo in combinations:
            sbl_x_thres_min, sbl_x_thres_max, hls_s_thres_min, hls_s_thres_max = combo
            calc(sbl_x_thres_min, sbl_x_thres_max, hls_s_thres_min, hls_s_thres_max)
    else:
        calc()

    #((lfit, lradius), (rfit, rradius)) = fl.history()
    
    #print(log.lf.shape, len(log.lf))
    #analyze = utl.analyze(log.lf, log.rf, log.lc, log.rc, log.ofset)
    #analyze.plot1()
    
if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: carltonj2000
"""
from moviepy.editor import VideoFileClip
import lane_line as ll
import utils as utl

def main():
    if False:
        sbl_x_thres_mins = [20]
        sbl_x_thres_maxs = [100]
        hls_s_thres_mins = [180]
        hls_s_thres_maxs = [255]
    elif False:
        sbl_x_thres_mins = [40]
        sbl_x_thres_maxs = [80]
        hls_s_thres_mins = [160]
        hls_s_thres_maxs = [205]
    elif True:
        sbl_x_thres_mins = [40]
        sbl_x_thres_maxs = [100, 80, 120]
        hls_s_thres_mins = [180, 160, 200]
        hls_s_thres_maxs = [255, 225, 205]
    else:
        sbl_x_thres_mins = [20, 40]
        sbl_x_thres_maxs = [100, 80, 120]
        hls_s_thres_mins = [180, 160, 200]
        hls_s_thres_maxs = [255, 225, 205]

    combinations = [
        [40, 100, 160, 225],
        [40, 100, 160, 255],
        [40, 100, 180, 255],
        [40, 120, 160, 225],
        [40, 120, 160, 255],
        [40, 120, 180, 255],
        [40, 80, 160, 225],
        [40, 80, 160, 255],
        [40, 80, 180, 255]
    ]
    
    logbase = "../../project_video/"
    x = 5
    if x == 1:
        video_in = "../../project_video_4s.mp4"
    elif x == 2:
        video_in = "../../project_video_s20t6.mp4"
    elif x == 3:
        video_in = "../../project_video_s38t5.mp4"
    elif x == 4:
        video_in = "../../project_video_1s.mp4"
    else:
        video_in = "../project_video.mp4"
    
    file, ext = video_in.split('/')[-1].split('.')
    
    mtx, dist = utl.distort_load(utl.fn.pickle_file)
    src, dst = ll.perspective_transform_values()
    M = ll.perspective_transform_map(src, dst)
    Minv = ll.perspective_transform_map(dst,src)
    
    logdir = logbase + file
    log = utl.log(logdir)
    
    
    def calc(sbl_x_thres_min, sbl_x_thres_max, 
             hls_s_thres_min, hls_s_thres_max):
        
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
    
#    for sbl_x_thres_min in sbl_x_thres_mins:
#        for sbl_x_thres_max in sbl_x_thres_maxs:
#            for hls_s_thres_min in hls_s_thres_mins:
#                for hls_s_thres_max in hls_s_thres_maxs:
#                    calc(sbl_x_thres_min, sbl_x_thres_max, 
#                         hls_s_thres_min, hls_s_thres_max)
    for combo in combinations:
        sbl_x_thres_min, sbl_x_thres_max, hls_s_thres_min, hls_s_thres_max = combo
        calc(sbl_x_thres_min, sbl_x_thres_max, hls_s_thres_min, hls_s_thres_max)
    
    #((lfit, lradius), (rfit, rradius)) = fl.history()
    
    #print(log.lf.shape, len(log.lf))
    #analyze = utl.analyze(log.lf, log.rf, log.lc, log.rc, log.ofset)
    #analyze.plot1()
    
if __name__ == '__main__':
    main()

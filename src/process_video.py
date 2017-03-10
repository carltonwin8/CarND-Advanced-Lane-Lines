#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: carltonj2000
"""
from moviepy.editor import VideoFileClip
import lane_line as ll
import utils as utl
import matplotlib.pyplot as plt

def main():
    x = 4
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
    video_out = '../../' + file + '_out.' + ext
    
    print("From =>", video_in, "To =>", video_out)
    
    mtx, dist = utl.distort_load(utl.fn.pickle_file)
    src, dst = ll.perspective_transform_values()
    M = ll.perspective_transform_map(src, dst)
    Minv = ll.perspective_transform_map(dst,src)
    fl = ll.find_lane_lines(mtx, dist, src, dst, M, Minv)
                
    clip2 = VideoFileClip(video_in)
    yellow_clip = clip2.fl_image(fl.fll)
    yellow_clip.write_videofile(video_out, audio=False)
    
    ((lfit, lradius), (rfit, rradius)) = fl.history()
    
    print(lfit.shape, lradius.shape)
    lfit
    if True:
        plt.plot(lradius)
        plt.show()
        plt.plot(rradius)
        plt.show()
        plt.plot(lfit[0::3])
        plt.show()
        plt.plot(lfit[1::3])
        plt.show()
        plt.plot(lfit[2::3])
        plt.show()
        plt.plot(rfit[0::3])
        plt.show()
        plt.plot(rfit[1::3])
        plt.show()
        plt.plot(rfit[2::3])
        plt.show()

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: carltonj2000

Ideally a config file should not be a straight up python file
but json, yaml, toml, etc.
The file provides a video file to process and threshold values
to process the video with.
"""

def get_thresholds(t):
    if t == 1:
        sbl_x_thres_mins = [40]
        sbl_x_thres_maxs = [80]
        hls_s_thres_mins = [160]
        hls_s_thres_maxs = [205]
    elif t == 2:
        sbl_x_thres_mins = [20]
        sbl_x_thres_maxs = [100]
        hls_s_thres_mins = [180]
        hls_s_thres_maxs = [255]
    elif t == 3:
        sbl_x_thres_mins = [40]
        sbl_x_thres_maxs = [100, 80, 120]
        hls_s_thres_mins = [180, 160, 200]
        hls_s_thres_maxs = [255, 225, 205]
    else:
        sbl_x_thres_mins = [20, 40]
        sbl_x_thres_maxs = [100, 80, 120]
        hls_s_thres_mins = [180, 160, 200]
        hls_s_thres_maxs = [255, 225, 205]
    return sbl_x_thres_mins, sbl_x_thres_maxs, hls_s_thres_mins, hls_s_thres_maxs

def get_videos(x):
    if x == 1:
        videos_in = ["../../project_video_4s.mp4"]
    elif x == 2:
        videos_in = ["../../project_video_s20t6.mp4"]
    elif x == 3:
        videos_in = ["../../project_video_s38t5.mp4"]
    elif x == 4:
        videos_in = ["../../project_video_1s.mp4"]
    elif x == 5:
        videos_in = ["../../project_video_s20t7.mp4",
                     "../../project_video_s38t6.mp4"]
    else:
        videos_in = ["../project_video.mp4"]
    return videos_in


def get_combinations(c):
    if c == 1:
        combinations = [
            [40, 120, 160, 225],
            [40, 120, 180, 255]
        ]
    elif c == 2:
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
    return combinations
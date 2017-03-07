#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Carlton Joseph
"""
import pickle
import lane_line as ll

def distort_save(file, mtx, dist):
    """
    Saves a distortion matrix to a file
    
    :param file: Filename to save undistorted parameters
    :param mtx: Camera calibartion mtx value
    :param dist: Camera calibartion dist value
    :return: None
    """
    dist_pickle = {}
    dist_pickle["mtx"] = mtx
    dist_pickle["dist"] = dist
    pickle.dump(dist_pickle, open(file, "wb"))

def distort_load(file):
    """
    Loads a distortion matrix from a file
    
    :param file: Filename to save undistorted parameters
    :return: map containing a distortion matrix
    """
    dist_pickle = pickle.load(open(file, "rb"))
    return dist_pickle['mtx'], dist_pickle['dist']

def perspective_transform(img):
    src, dst = ll.perspective_transform_values()
    warped = ll.perspective_transform(img,ll.perspective_transform_map(src, dst))
    return warped
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Carlton Joseph
"""
import pickle

def distort_save(file, mtx, dist):
    """
    :param file: Filename to save undistorted parameters
    :param mtx: Camera calibartion mtx value
    :param dist: Camera calibartion dist value
    """
    dist_pickle = {}
    dist_pickle["mtx"] = mtx
    dist_pickle["dist"] = dist
    pickle.dump(dist_pickle, open(file, "wb"))

def distort_load(file):
    """
    :param file: Filename to save undistorted parameters
    """
    dist_pickle = pickle.load(open(file, "rb"))
    return dist_pickle['mtx'], dist_pickle['dist']

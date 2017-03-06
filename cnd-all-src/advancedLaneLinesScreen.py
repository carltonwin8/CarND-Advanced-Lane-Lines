#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Carlton Joseph
"""
import cv2
import matplotlib.pyplot as plt
import advancedLaneLinesLib as alll
import advancedLaneLinesUtils as allu

def main():
    #mtx, dist = alll.calibrateCamera('../camera_cal/calibration*.jpg')
    pickleFile = '../dist_pickle.p'
    #allu.distortSave(pickleFile, mtx, dist)
    mtx, dist = allu.distortLoad(pickleFile)
    calTestImg = '../camera_cal/calibration1.jpg'
    imgDist = cv2.imread(calTestImg)
    imgUndist = alll.undistortImage(imgDist, mtx, dist)
    plt.imshow(imgDist)
    #plt.imshow(imgUndist)    

if __name__ == "__main__":
    main()
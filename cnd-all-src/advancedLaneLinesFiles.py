#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Carlton Joseph
"""
import cv2
import advancedLaneLinesLib as alll
import advancedLaneLinesUtils as allu

def addFileNamePs(distImgFile,ps):
    fileName = distImgFile.split('/')
    prePost = fileName[-1].split('.')
    return '../output_images/' + prePost[0] + '_' + ps + '.' + prePost[1]
    
def main():
    #mtx, dist = alll.calibrateCamera('../camera_cal/calibration*.jpg')
    pickleFile = '../dist_pickle.p'
    #allu.distortSave(pickleFile, mtx, dist)
    mtx, dist = allu.distortLoad(pickleFile)
    calTestImgFileName = '../camera_cal/calibration1.jpg'
    calTestImgDist = cv2.imread(calTestImgFileName)
    calTestImgUnDist = alll.undistortImage(calTestImgDist, mtx, dist)
    testImg1FileName = '../test_images/straight_lines1.jpg'
    testImg1Dist = cv2.imread(testImg1FileName)
    testImg1Undist = alll.undistortImage(testImg1Dist, mtx, dist)
    cv2.imwrite(addFileNamePs(calTestImgFileName,'undist'), calTestImgUnDist)
    cv2.imwrite(addFileNamePs(testImg1FileName, 'undist'), testImg1Undist)
    
if __name__ == "__main__":
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Carlton Joseph
"""
import cv2
import matplotlib.pyplot as plt

def imshow(imgs, cmap=None, show=True):
    if show:
        if type(imgs) is not list:
            imgs = [imgs]
        for img in imgs:            
            if len(img) == 2 and type(img[1]) is bool:
                if img[1]:
                    plt.imshow(img[0])
            elif len(img) == 2 and type(img[1]) is str:
                    plt.imshow(img, cmap=img[1])
            elif len(img) == 3 and type(img[1]) is bool:
                if img[1]:
                    plt.imshow(img[0], cmap=img[2])
            elif len(img) == 3 and type(img[1]) is bool:
                if img[2]:
                    plt.imshow(img[0], cmap=img[1])
            elif cmap == None:
                    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            elif cmap != None:
                    plt.imshow(img, cmap=cmap)                    
            else:
                print('NO display! Input format incorrect')
                
            plt.show()

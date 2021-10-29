# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 16:35:38 2021

@author: HungBT
"""

import cv2
frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture("C:/Users/HungBT/Documents/Github/Image-Processing-Using-Python/Example codes/Resources/Test_Video.webm")
while True:
    success, img = cap.read()
    img = cv2.resize(img, (frameWidth, frameHeight))
    cv2.imshow("Result", img)
    if cv2.waitKey(1) and 0xFF == ord('q'):
        break
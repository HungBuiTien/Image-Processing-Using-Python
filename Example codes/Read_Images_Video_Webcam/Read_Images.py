# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 16:33:13 2021

@author: HungBT
"""

import cv2
# LOAD AN IMAGE USING 'IMREAD'
img = cv2.imread(r"C:\Users\HungBT\Documents\Github\Image-Processing-Using-Python\Example codes\Resources\lena.png")
# DISPLAY
cv2.imshow("Lena Soderberg",img)
cv2.waitKey(0)
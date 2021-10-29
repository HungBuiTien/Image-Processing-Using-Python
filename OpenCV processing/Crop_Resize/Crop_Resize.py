# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 16:49:57 2021

@author: HungBT
"""

import cv2
import numpy as np
 
img = cv2.imread(r"C:/Users/HungBT/Documents/Github/Image-Processing-Using-Python/Example codes/Resources/lambo.png")
print(img.shape)

# Resize image
imgResize = cv2.resize(img, (1000, 500))

# Crop image
imgCrop = img[0:200, 200:500]

cv2.imshow("Image",img)
cv2.imshow("Resized Image", imgResize)
cv2.imshow("Cropped Image", imgCrop)
 
cv2.waitKey(0)
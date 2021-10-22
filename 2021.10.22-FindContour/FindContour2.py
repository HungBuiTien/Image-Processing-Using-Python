# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 13:20:22 2021

@author: Nuelab03
"""
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os 
import glob
from ellipse import LsqEllipse
from matplotlib.patches import Ellipse
from skimage.transform import rotate

#%%%
def read_raw(raw_img_path):
	# Number of Rows
	ROWS = 2352
	# Number of Columns  
	COLS = 2944
	raw_img = open(raw_img_path)  
	# Loading the input image
	img = np.fromfile(raw_img, dtype = np.uint16, count = ROWS * COLS)
	# Conversion from 1D to 2D array
	img.shape = (img.size // COLS, COLS)
	img = np.rot90(img,2)
	return img

def Read_All(path):
    data_path = os.path.join(path,'*raw') 
    files = glob.glob(data_path) 
    data = [] 
    for f1 in files: 
        img = read_raw(f1)
        data.append(img)
    img3D = np.array(data)
    return img3D

def Find_Contour(original_img):
    rotated_img = rotate(original_img, -0.146)
    # Chuyển thành ảnh 8 bit
    imge_8bit = (rotated_img/rotated_img.max()).astype('uint8')
    cv2.normalize(imge_8bit, imge_8bit, 0, 255, cv2.NORM_MINMAX)

    # Cắt ngưỡng ảnh
    thresh = cv2.Canny(imge_8bit, 0, 200)
    # Tìm contours
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse= True)
   
    # Get contour points
    x, y = [], []
    for i in range (len(sorted_contours[0])):
        x.append(float(sorted_contours[0][i,0,0]))
        y.append(float(sorted_contours[0][i,0,1]))
    data_point = np.array(list(zip(x, y)))
    
    # Fit ellipse for contour points
    reg = LsqEllipse().fit(data_point)
    center, width, height, phi = reg.as_parameters()
    print(f'center: {center[0]:.3f}, {center[1]:.3f}')
    print(f'width: {width:.3f}')
    print(f'height: {height:.3f}')
    print(f'phi: {phi:.3f}')
    return center[0], center[1]
    
    # Vẽ hình
    # figure = plt.figure(figsize=(5, 5))
    # ax = plt.subplot()
    # ax.set_title('A single plot')
    # ax.plot(x, y, 'o',  markersize=1, color='red')
    # ellipse = Ellipse(xy=center, width=2*width, height=2*height, angle=np.rad2deg(phi),
    #                   edgecolor='b', fc='None', lw=2, label='Fit', zorder=2)
    # ax.add_patch(ellipse)
    # plt.show()

#%% Read image
allImage = Read_All(r'G:\Geometric_calibration\bottom')
x = []
y = []
for i in range(0,allImage.shape[0]):
    print("=> Loading {} of {}".format(i+1, allImage.shape[0]))
    original_img = allImage[i]
    x_center, y_center = Find_Contour(original_img)
    x.append(x_center)
    y.append(y_center)
    
data_point = np.array(list(zip(x, y)))
reg = LsqEllipse().fit(data_point)
center, width, height, phi = reg.as_parameters()

#%% Plot
figure = plt.figure(figsize=(5, 5))
ax = plt.subplot()
ax.set_title('A single plot')
ax.plot(x, y, 'o',  markersize=1, color='red')
ellipse = Ellipse(xy=center, width=2*width, height=2*height, angle=np.rad2deg(phi),
                  edgecolor='b', fc='None', lw=2, label='Fit', zorder=2)
ax.add_patch(ellipse)
plt.show()
print("Ellippse fitting center = ({};{}).".format(center[0], center[1]))
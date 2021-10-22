# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 20:33:56 2021

@author: HungBT
"""
#%%%
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os 
import glob
from ellipse import LsqEllipse
from matplotlib.patches import Ellipse
import ellipse as el

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
def FindContour(img):
    # Chuyển thành ảnh 8 bit
    imge_8bit = (original_img/256).astype('uint8')
    cv2.normalize(imge_8bit, imge_8bit, 0, 255, cv2.NORM_MINMAX)
    
    # Cắt ngưỡng ảnh
    # ret,thresh = cv2.threshold(imge_8bit, 38, 255, 0)
    thresh = cv2.Canny(imge_8bit, 0, 200)
    
    # Tìm contours
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Tìm chỉ số của đối tượng có kích thước lớn nhất
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse= True)
    
    # Chuyển ảnh xám thành ảnh màu RGB
    color_image = cv2.cvtColor(imge_8bit, cv2.COLOR_GRAY2RGB)
    
    # Vẽ contour lên ảnh
    contour_color = cv2.drawContours(color_image,sorted_contours, 0, (0, 255, 0), 2)
    
    # Hiển thị ảnh
    # plt.imshow(contour_color,'gray')
    
    # Tính thông tin
    cnt = sorted_contours[0]
    M = cv2.moments(cnt)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    print("     Centroid = ({}; {}). Unit:pixel".format(cx, cy))
    area = cv2.contourArea(cnt)
    perimeter = cv2.arcLength(cnt,True)
    print("     => Area = {}; Perimeter = {} Unit:Pixel".format(area, perimeter))
    print("       Radius1 = Perimeter/(2*pi) = {}".format(perimeter/(2*np.pi)))
    print("       Radius2 = sqrt(Area/(pi)) = {}".format(np.sqrt(area/np.pi)))
    (x,y),radius = cv2.minEnclosingCircle(cnt)
    center = (int(x),int(y))
    radius = int(radius)
    print("     => The circumcircle of an object: center = {}; radius = {}".format(center, radius))
    return center, radius
    

# Đọc ảnh gốc
x = []
y = []
Data = Read_All(r"G:\CT3DMachine\LabTest_Thuan\Lab\Lab5\Mode_Normal\Dataseries")
for i in range(Data.shape[0]):
    print("* Loading ... {} of {}".format(i+1,Data.shape[0]))
    original_img = Data[i]
    center_temp, radius_temp = FindContour(original_img)
    x.append(float(center_temp[0]))
    y.append(float(center_temp[1]))
#%% Fit hàm
data_point = np.array(list(zip(x, y)))
reg = LsqEllipse().fit(data_point)
center, width, height, phi = reg.as_parameters()

print(f'center: {center[0]:.3f}, {center[1]:.3f}')
print(f'width: {width:.3f}')
print(f'height: {height:.3f}')
print(f'phi: {phi:.3f}')

# Vẽ hình
figure = plt.figure(figsize=(5, 5))
ax = plt.subplot()
ax.set_title('A single plot')
ax.plot(x, y, 'o',  markersize=1, color='red')
ellipse = Ellipse(xy=center, width=2*width, height=2*height, angle=np.rad2deg(phi),
                  edgecolor='b', fc='None', lw=2, label='Fit', zorder=2)
ax.add_patch(ellipse)
plt.show()

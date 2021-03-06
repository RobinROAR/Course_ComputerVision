#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
#Project:     Effects of  different convolutioanl kernels, brute calculation
#Purpose:   Compare the effects of different convolution kernels
#Abstract:  The project presents various of convolution kernels and shows their effects on demo pictures, you can definate your own convolution kernels and see its effect. The caculation function can get the size of  convolution templates and calculate automatically.
#Author:     RobinZheng    zhengruobing@cnic.cn
###############################################################################
#2016-02-26 19:47:42   support grey->support color


import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys
import time


#获取卷积近似模板的实际尺寸
#get the size of  convolution template
def getTemSize(tem):
	wid = tem.shape[0]
	print "COV template:"
	print tem
	print 'Template size:',wid,'*',wid
	return wid
	

#通过原始定义的方法，对图像计算卷积，返回一个图像矩阵。
#calculate the convolution by brute force, return a image matrix.
def calCov(tem,img):
	st = time.time()
	print 'Input image : ',img.shape
	size = getTemSize(tem)
	#扩充图片的像素数
	es = (size-1)/2
	
	#区别灰度图像与彩色图像
	if len(img.shape) is 2:
		y,x,z = img.shape[0],img.shape[1],1
	else:
		y,x,z = img.shape[0],img.shape[1],img.shape[2]
	#将图像上下左右各增加（模板宽度-1)/2个像素，用于计算卷积时的边界计算。
	#Expand image by es pixel around for edge calculation.
	if len(img.shape) is 2:
		eimg = np.uint8(np.zeros((y+2*es,x+2*es,1)))
		eimg[es:y+es,es:x+es,0] = img[:,:]
	else:	
		eimg = np.uint8(np.zeros((y+2*es,x+2*es,z)))
		eimg[es:y+es,es:x+es,:] = img
	result = np.uint8(np.zeros(eimg.shape))
	x=x+es   
	y=y+es
	for i in range(z):		
		a = b =1
		#扩充后图像的坐标,从0开始
		#设置一个dif变量，用于卷积窗内计算。
		dif = (size-1)/2
		while(b<y):
			a = 1
			while(a<x):
				cntx = 0
				dify = size/2
				result[b][a][i] = 0
				while(cntx<size):
					cnty = 0
					difx = size/2
					while(cnty<size):
						#print b,a,b-dify,a-difx
						result[b][a][i] +=tem[cntx][cnty]*eimg[b-dify][a-difx][i]
						cnty+=1
						difx-=1
					cntx+=1
					dify-=1	
				a+=1
			b+=1	
	et = time.time()
	print 'Cal time:',str(et-st)
	return np.uint8(result)	




img = cv2.imread('image.jpg',1)

#~ temp1 = np.zeros((5,5))
#~ temp1[[2,2,0,1,3,4,2,2],[0,1,2,2,2,2,3,4]] =-1 
#~ temp1[2][2] = -8

#~ temp2 = np.zeros((5,5))

#~ temp2[[0,1,2,3,0,1,2,0,1,0],[0,0,0,0,1,1,1,2,2,3]] = -1
#~ temp2[[4,3,4,2,3,4,1,2,3,4],[1,2,2,3,3,3,4,4,4,4]] = 1



temp1 = np.zeros((3,3))
temp1[:,:] = 1
temp1[1][1] = -7

temp2 = np.zeros((3,3))
temp2[[0,1,2],[0,1,2]] = 1/3.0

temp3 = np.zeros((3,3))
temp3[[1,1,1],[0,1,2]] = [-1,0,1]

res1 = calCov(temp1,img)
res2 = calCov(temp2,img)
res3 = calCov(temp3,img)

#显示
#~ cv2.imshow("1",res)
#~ cv2.imshow("12",img)
#~ cv2.waitKey(0)  #等待键盘任意输入
#~ cv2.destroyAllWindows()
#~ sys.exit(0)

#opencv图片数组为bgr，matplotlib为rgb，需要转换一下
b,g,r = cv2.split(img)
img = cv2.merge([r,g,b])
b,g,r = cv2.split(res1)
res1 = cv2.merge([r,g,b])  
b,g,r = cv2.split(res2)
res2 = cv2.merge([r,g,b]) 
b,g,r = cv2.split(res3)
res3 = cv2.merge([r,g,b]) 

plt.figure(figsize = (8,6))

plt.subplot(221)
plt.imshow(img)
plt.title("Origin")
plt.subplot(222)
plt.imshow(res1)
plt.title("Sharpen")
plt.subplot(223)
plt.imshow(res2)
plt.title("motion blur")
plt.subplot(224)
plt.imshow(res3)
plt.title("Edge detection")

plt.show()

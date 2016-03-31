#!/usr/bin/env python
# -*- coding:utf8 -*-
###############################################################################
# Project:  CVhomework2
# Purpose:  Movement tracking based on meanshift
# Author:   RobinZheng    zhengruobing@cnic.cn
# Stu No.   201418016029010
###############################################################################
#2016-01-18 09:47:42   New
#2016-01-20 09:47:42   Fixed
#Not realized capture ROI by mouse yet, realized in another py
import numpy as np
import cv2
import random

#Meanshift实现方法，通过反向投影ROI的H通道灰度直方图，在概率图上根据质心位置漂移，参数n为最大迭代次数
def meanshift(d, t, n):
	t=np.array(t)
	print "搜索框位置:",t[0],t[1]
	i=1
	while(i<n):
		temp = cv2.moments(d[t[1]:t[1]+t[3],t[0]:t[0]+t[2]])
		#当搜索框内0阶矩为0时，随机扰动
		if temp.get('m00',1) == 0:
			bw = random.randint(-2,2)
			bh = random.randint(-2,2)
		else:
			mc = (temp.get('m10',0)/(temp.get('m00',1)),temp.get('m01',0)/(temp.get('m00',1)))
			print mc
			#现实当前帧搜索框左上角点，和质心相对坐标
			#设置移动步长，图像中心移动到质心的的距离/n，防止因为像素过低造成质心反复抖动
			bw = (mc[0]-t[3]/2)/1
			bh = (mc[1]-t[2]/2)/1
		#边缘检查，移动追踪框不能出图像
		if ((t[0]+bw) < 0 or (t[0]+bw)>d.shape[1]):
			t[0]+=0
		else:
			t[0]+= bw
		if ((t[1]+bh) < 0 or (t[1]+bh)>d.shape[0]):
			t[1]+=0
		else:
		    t[1]+= bh
		#移动距离差小于1时停止迭代
		if((abs(bw)+abs(bh))<=0.5):
			print "Distinct < 0.5"
			break
		i+=1
	print '================='
	return 1,t

#videoWriter = cv2.VideoWriter('MyTrackingResult.avi',cv2.cv.CV_FOURCC('M','J','P','G'),15,(640,480))
#主程序
if __name__ == "__main__":
	cap = cv2.VideoCapture('Homework_video.avi')
	# 读取视频
	ret,frame = cap.read()
	#x,y,w,h = 120,240,60,60  #ball 3
	x,y,w,h = 70,250,65,65  #ball 1
	track_window = (x,y,w,h)
	#指定直方图区域大小，小于搜索框
	roi = frame[250:275,70:95] #ball 1
	#j将色彩转换到HSV空间
	hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
	#计算ROI区域H通道灰度直方图
	roi_hist = cv2.calcHist([hsv_roi],[0],None,[18],[0,180])
	#0-1规范化直方图
	cv2.normalize(roi_hist,roi_hist,0,1,cv2.NORM_MINMAX)
	#~ print roi_hist

	j = 1
	while(1):
		ret ,frame = cap.read()
		print "第",j,"帧"
		if ret == True:
			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
			#用掩膜只留下一个小球a
			maskb1 = cv2.inRange(hsv,np.array((100., 50.,0.)), np.array((120.,100.,255.)))
			hsv  = cv2.bitwise_and(hsv,hsv,mask=maskb1)
			#使用计算出的直方图，在H通道上进行反向投影，得到每一帧的概率分布图。
			dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)
			#在概率图像上根据搜索框大小进行均值漂移
			ret, track_window = meanshift(dst, track_window,20)
			x,y,w,h = track_window
			#显示蓝色搜索框
			cv2.rectangle(frame, (x,y), (x+w,y+h), 255,1)
			#显示绿色锁定框
			w1=w/3
			h1=h/3
			cv2.rectangle(frame, (x+w1,y+h1), (x+2*w1,y+2*h1), (0,255,0),2)
			cv2.imshow('img2',frame)
			#videoWriter.write(frame)
			k = cv2.waitKey(60) & 0xff
			if k == 27:
				break
			j+=1
		else:
			break
	cv2.destroyAllWindows()
	cap.release()

#!/usr/bin/env python
# -*- coding:utf-8 -*-
#~~~~~~~~~~~~~~~~~~~~~~~~
# 预处理模块：
#   将鼠标轨迹数据转化为矩阵
#   膨胀边缘，调整尺寸
#   存储为二进制文件
#Robin 2016.7
#~~~~~~~~~~~~~~~~~~~~~~~~
# Standard
import cPickle
import random
#Third-party
import numpy as np
import matplotlib.pyplot as plt
import cv2


#读取data.txt文件，保存到数组
def read_as_list(filename):
    #文本方式读取文件
    #返回list[picture1[坐标1[x,y]]]
    with open(filename,'rt') as file:
        data = file.readlines()
    #转化成list
    content = []
    picture = []
    cnt = 0
    for line in data:
        ##处理两行间隔的划分
        if line == '\n':
            cnt+=1
            if cnt%2 == 0:
                print 'num',cnt/2
                content.append(picture)
                picture = []
        else:
            #op1:去除前后空行
            line = line.strip()
            #op2:划分成list
            line = line.replace(': ',',')
            temp = line.split(',')
            #op3: 拼装成新list,  x,y 与图像中相反
            temp = [np.int32(temp[3]),np.int32(temp[1])]
            # print temp
            picture.append(temp)
            temp = []
    print '~~~ Load finished'
    return content

def list_to_ndarray(data):
    #返回 list[ndarray1,ndarray2]
    #将坐标信息转化为图像，ndarray格式
    result = []
    for i in data:
        #生成合适大小的0数组
        a = np.array(i)
        max = np.max(a,axis=0)
        min = np.amin(a,axis = 0)
        #左右预留1像素距离
        size = (max - min)+3
        picture = np.zeros(size)
        #归一化坐标
        a = a - min+1
        #填充矩阵
        picture[a[:,0],a[:,1]] = 1
        #print picture
        #print picture.shape
        result.append(picture)
    return result

def make_to_binary(list):
    #将结果转存为二进制文件
    with open('./data/pictures.pickle','wb+') as file:
        cPickle.dump(list,file)
    print '~~~ Dump finished!'

def view_picture(list):
    #观看转化后图片的方法,看随机3个

    #从本地读取
    if list == '':
        with open('./data/pictures.pickle', 'rb') as file:
            list = cPickle.load(file)
    else:
        rand = random.sample(range(len(list)),3)
        plt.subplot(131)
        plt.imshow(list[rand[0]],cmap = 'gray')
        plt.subplot(132)
        plt.imshow(list[rand[1]],cmap = 'gray')
        plt.subplot(133)
        plt.imshow(list[rand[2]],cmap = 'gray')
        plt.show()

def dilate_picture(ndarray):
    #实现膨胀算法，增粗特征
    kernel = np.uint8(np.zeros((6,6)))
    kernel[:,:] = 1
    result = cv2.dilate(ndarray,kernel)
    return result

def resize_picture(ndarray):
    #统一的矩阵大小
    result = cv2.resize(ndarray,(50,50))
    #print result.shape
    return result


if __name__ == '__main__':
    data = read_as_list('./mouse.txt')
    list = list_to_ndarray(data)
    # make_to_binary(list)

    view_picture(list)

    result = []
    for i in list:
        t = resize_picture(dilate_picture(i))
        result.append(t)
    view_picture(result)





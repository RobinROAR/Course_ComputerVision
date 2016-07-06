#!/usr/bin/env python
# -*- coding:utf-8 -*-
# ~~~~~~~~~~~~~~~~~~~~~~~~
#  将矩阵转化为HOG特征
#  使用HOG特征进行分类
# Robin 2016.7
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Standard
import cPickle
# Third
import preprocess as ps
import numpy as np
import cv2
import


def get_hog(mat):
    # 将原始图片转化为HOG特征
    gx = cv2.Sobel(mat, cv2.CV_64F, 1, 0)  # x方向梯度
    gy = cv2.Sobel(mat, cv2.CV_64F, 0, 1)  # y方向梯度
    mag, ang = cv2.cartToPolar(gx, gy)  # 计算梯度方向和复制
    # quantizing binvalues in (0...16)
    bin_n = 16
    bins = np.int32(bin_n * ang / (2 * np.pi))
    bin_cells = bins[:10, :10], bins[10:, :10], bins[:10, 10:], bins[10:, 10:]
    mag_cells = mag[:10, :10], mag[10:, :10], mag[:10, 10:], mag[10:, 10:]
    hists = [np.bincount(b.ravel(), m.ravel(), bin_n) for b, m in zip(bin_cells, mag_cells)]
    hist = np.hstack(hists)
    # hist is a 64 bit vector
    print hist.shape
    return hist


if __name__ == '__main__':

    with open('./data/pictures.pickle', 'rb') as file:
        list = cPickle.load(file)

    # make_to_binary(list)

    # view_picture(list)


    for i in list:
        # print i.shape
        t = ps.resize_picture(ps.dilate_picture(i))
        get_hog(t)
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 19:50:04 2019

@author: McLaren
"""

import cv2 as cv
import numpy as np
import win32gui, win32ui, win32con, win32api
  
    
def match_template(temppath):
    img = window_capture()
    #img = cv.imread(imgpath)
    player_template = cv.imread(temppath)
    player = cv.matchTemplate(img, player_template, cv.TM_CCOEFF_NORMED)

    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(player)
    #当图片中有与模板匹配度超过90%的部分时：
    if max_val>0.9:
        #框选出目标，并标出中心点
        corner_loc = (max_loc[0] + player_template.shape[1], max_loc[1] +player_template.shape[0])
        player_spot = (max_loc[0] + int(player_template.shape[1]/2), max_loc[1] + int(player_template.shape[0]/2))
        cv.circle(img, player_spot, 10, (0, 255, 255), -1)
        cv.rectangle(img, max_loc, corner_loc, (0, 0, 255), 3)
        cv.namedWindow('FGO_MatchResult', cv.WINDOW_KEEPRATIO)
        cv.imshow("FGO_MatchResult", img)
        #显示结果0.5秒钟
        k = cv.waitKey(500)
        if k==-1:
            cv.destroyAllWindows()
        return True, player_spot
    else:
        return False, 0
    

def window_capture(filename='F:/FGO_Project/capture.jpg'):
    hwnd = win32gui.FindWindow("CHWindow",None) # 窗口的名称与类型
    # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    hwndDC = win32gui.GetWindowDC(hwnd)
    #获取句柄窗口的大小信息
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bot - top
    # 根据窗口的DC获取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # mfcDC创建可兼容的DC
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建bigmap准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 获取监控器信息
    # 为bitmap开辟空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    # 高度saveDC，将截图保存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)
    #saveBitMap.SaveBitmapFile(saveDC, filename)
    
    signedIntsArray = saveBitMap.GetBitmapBits(True)
    img = np.frombuffer(signedIntsArray, dtype = 'uint8')
    img.shape = (height, width, 4)
    img = cv.cvtColor(img, cv.COLOR_RGBA2RGB)

    #img = cv.imread(filename)
    #截取出ios屏幕区域，参数根据软件分辨率自行修改
    cropped = img[37:height-1, 1:width-1]  # 裁剪坐标为[y0:y1, x0:x1]
    #cv.imwrite(filename, cropped)
    return cropped

#k,l=match_template('F:/FGO_Project/Template/AP_recover.jpg')
#k=match_template('E:/FGO_Project/capture8.jpg','E:/FGO_Project/Template/Caster_sign.jpg')

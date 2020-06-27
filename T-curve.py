import math
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.Point import Point
import re, time, os, sys
import numpy as np

def square(x):
    return float(x*x)

def velPlan(dist, v_start, v_end, v_max, acc_max, vel_list):
    dt = 0.02
    # 计算边界
    vel_limit = 0.0
    vel_temp = 0.0
    vel_temp = math.sqrt((dist * 2 * acc_max + square(v_start) + square(v_end)) / 2.0)
    print("limit is %f" % vel_temp)
    # vel_temp = math.sqrt(math.fabs(float(square(v_start)) + float(square(v_end)) - 2.0 * float(acc_max) * float(dist)) / 2.0)
    print("acc dist is %f" % ((square(vel_temp) - square(v_start))/(2*acc_max)))
    print("dec dist is %f" % ((square(vel_temp) - square(v_end))/(2*acc_max)))
    if vel_temp < v_max:
        vel_limit = vel_temp
    else:
        vel_limit = v_max
    # 分段时间及距离
    acc_t = (vel_limit - v_start) / acc_max
    print(acc_t)
    acc_dist = v_start * acc_t + acc_max * square(acc_t) / 2
    # print(acc_dist)
    dec_t = (vel_limit - v_end) / acc_max
    print(dec_t)
    dec_dist = vel_limit * dec_t - acc_max * square(dec_t) / 2
    # print(dec_dist)
    constant_dist = dist - acc_dist - dec_dist
    # print(constant_dist)
    constant_t = constant_dist / vel_limit
    print(constant_t)
    # 细分速度
    tmp_t = 0
    tmp_v = v_start
    vel_list.append(v_start)
    tmp_t = tmp_t + dt
    while acc_t - tmp_t > 0:
        tmp_v = tmp_v + acc_max * dt
        if tmp_v <= vel_limit:
            vel_list.append(tmp_v)
        tmp_t = tmp_t + dt
        print(tmp_t)
    if (acc_t - tmp_t - dt) > 0:
        vel_list.append(vel_limit)
    tmp_t = 0
    while constant_t - tmp_t > 0:
        vel_list.append(vel_limit)
        tmp_t = tmp_t + dt
    if (constant_t - tmp_t - dt) > 0:
        vel_list.append(vel_limit)
    tmp_t = 0
    tmp_v = vel_limit
    while dec_t - tmp_t > 0:
        tmp_v = tmp_v - acc_max * dt
        vel_list.append(tmp_v)
        tmp_t = tmp_t + dt
    if (dec_t - tmp_t - dt) > 0:
        vel_list.append(v_end)

# data_str = open("D:\\code\\Scrolling_Ploter\\2-4.txt","r+")
# data_array = []
# data_t = [] 
# data_v = []
# for line in data_str.readlines():
#     print(line)
#     data_array = re.split("[|]", line)
#     data_t.append(float(data_array[0]))
#     data_v.append(float(data_array[1]))

win = pg.GraphicsWindow()
p = win.addPlot()
p.showGrid(x=True,y=True)
vel = []
velPlan(4, 0.02, 3, 5, 1, vel)
curve = p.plot(y = vel, pen="y", symbolBrush=(255,0,0), symbolPen='w')

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

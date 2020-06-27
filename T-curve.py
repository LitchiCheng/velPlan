def velPlan(dist, v_start, v_end, v_max, acc_max, vel_list):
    dt = 0.02
    if (v_max*v_max - v_start*v_start) / 2 * acc_max <= dist:
        print("acc and dec")
        acc_t = (v_max - v_start) / acc_max
        tmp_t = 0
        tmp_v = v_start
        vel_list.append(v_start)
        while tmp_t <= acc_t:
            tmp_v = tmp_v + acc_max*dt
            vel_list.append(tmp_v)
            tmp_t = tmp_t + dt
        acc_t_spare = acc_t - tmp_t
        if acc_t_spare:
            vel_list.append(v_max)
        #先判断减速是否完整
        dist_spare_with_dec_acc = dist - (v_max*v_max - v_end*v_end) / 2 * acc_max - ( (v_max*v_max -v_start*v_start) / 2 * acc_max)
        print(dist_spare_with_dec_acc)
        if dist_spare_with_dec_acc >= 0:
            print("has dec")
            while (dist_spare_with_dec_acc / v_max - dt) > 0:
                # print(dist_spare_with_dec_acc)
                dist_spare_with_dec_acc = dist_spare_with_dec_acc - v_max * dt
                vel_list.append(v_max)
            tmp_t = 0
            dec_t = (v_max - v_end) / acc_max
            tmp_v = v_max
            while tmp_t <= dec_t:
                tmp_v = tmp_v - acc_max*dt
                vel_list.append(tmp_v)
                tmp_t = tmp_t + dt
            dec_t_spare = dec_t - tmp_t
            if dec_t_spare:
                vel_list.append(v_end)          
    else:
        print("only acc")
        acc = (v_end*v_end - v_start*v_start) / 2 * dist
        vel_list.append(v_start)
        if acc > 0:
            acc_t = (v_end - v_start) / acc
            tmp_t = 0
            tmp_v = v_start
            while tmp_t < acc_t:
                tmp_v = tmp_v + acc*dt
                vel_list.append(tmp_v)
                tmp_t = tmp_t + dt
            acc_t_spare = acc_t - tmp_t
            if acc_t_spare:
                vel_list.append(v_end)
        elif acc == 0:
            dist_t = dist / v_start
            tmp_t = 0
            while tmp_t < dist_t:
                vel_list.append(v_start)
                tmp_t = tmp_t + dt
            dist_t_spare = dist_t - tmp_t
            if dist_t_spare:
                vel_list.append(v_end)

import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.Point import Point
import re, time, os, sys
import numpy as np

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
velPlan(1000, 0.02, 4, 5, 0.2, vel)
curve = p.plot(y = vel, pen="y", symbolBrush=(255,0,0), symbolPen='w')

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

            
# if __name__ == "__main__":
#     vel = []
#     velPlan(100, 0.02, 1, 5, 1, vel)
#     print(vel)
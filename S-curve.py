
'''
判断达到最大加速度时的距离
acc = jerk * dt
t2am = am / jerk
v2am = 0.5 * jerk * square(t2am)
s2am = 0.5 * am * square(t2am) = 0.5 * (0.5 * jerk * square(t2am)) * square(t2am) = 0.25 * jerk * squrare(square(t2am))
if s2am * 2 > dist:
    加速度
if s2am * 2 = dist:
    仅存在加加速和加减速阶段，最终速度是否大于vmax和是否等于vend
    if 2 * 0.5 * jerk * square(t2am) >= vmax or != vend:

if s2am * 2 < dist:
    存在加加速和加减速阶段，再分级讨论是否存在减减速和减加速阶段

'''
import math
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.Point import Point
import re, time, os, sys
import numpy as np

def square(x):
    return float(x*x)

def sampleVelocity(t_aa, t_ad, t_c, t_da, t_dd, v_start, v_end, v_max, vel_list, jerk, dt, have_constant):
    # 加加速
    vel_list.append(v_start)
    tmp_t = 0.0
    tmp_t = tmp_t + dt
    while tmp_t <= t_aa:
        vel_list.append(vel_list[0] + 0.5*jerk*square(tmp_t))
        tmp_t = tmp_t + dt
    print("aa vel is %f" % vel_list[-1])
    # 加减速
    tmp_t = t_ad
    v_last = vel_list[-1]
    while tmp_t >= 0:
        vel_list.append(2 * v_last - 0.5*jerk*square(tmp_t))
        tmp_t = tmp_t - dt
    print("ad vel is %f" % vel_list[-1])
    if have_constant:
        # 匀速
        tmp_t = 0.0
        while tmp_t <= t_c:
            vel_list.append(v_max)
            tmp_t = tmp_t + dt
        print("c vel is %f" % vel_list[-1])
    # 减减速
    tmp_t = 0.0
    v_last = vel_list[-1]
    while tmp_t <= t_da:
        vel_list.append(v_last - 0.5*jerk*square(tmp_t))
        tmp_t = tmp_t + dt
    print("dd vel is %f" % vel_list[-1])
    # 减加速
    tmp_t = t_da
    v_last = vel_list[-1]
    while tmp_t >= 0:
        vel_list.append( 0.5*jerk*square(tmp_t))
        tmp_t = tmp_t - dt
    print("da vel is %f" % vel_list[-1])

def velPlan(dist, v_start, v_end, v_max, acc_max, jerk, vel_list):
    dt = 0.002
    s_a = 0.0
    s_d = 0.0
    t_aa = 0.0
    t_ad = 0.0
    t_c = 0.0
    t_da = 0.0
    t_dd = 0.0
    if v_start == 0 and v_end == 0:
        s_a = v_max * math.sqrt(v_max/jerk)
        s_d = s_a
        if 2 * s_a <= dist:
            t_aa = t_ad = t_da = t_dd = math.sqrt(v_max/jerk)
            t_c = (dist - 2 * s_a) / v_max
            sampleVelocity(t_aa,t_ad,t_c,t_da,t_dd,v_start,v_end,v_max,vel_list,jerk,dt,True)
        elif 2 * s_a > dist:
            v_desire = (0.5 * dist * jerk) ** (1/3)
            t_aa = t_ad = t_da = t_dd = math.sqrt(v_desire/jerk)
            t_c = 0.0
            sampleVelocity(t_aa,t_ad,t_c,t_da,t_dd,v_start,v_end,v_max,vel_list,jerk,dt,False)
    else:
        s_a = (v_max + v_start) * math.sqrt((v_max - v_start) / jerk)
        s_d = (v_max + v_end) * math.sqrt((v_max - v_end) / jerk)
        if s_d + s_a <= dist:
            t_aa = t_ad = math.sqrt((v_max - v_start) / jerk)
            t_da = t_dd = math.sqrt((v_max - v_end) / jerk)
            t_c = (dist - s_a -s_d) / v_max
            sampleVelocity(t_aa,t_ad,t_c,t_da,t_dd,v_start,v_end,v_max,vel_list,jerk,dt,True)



win = pg.GraphicsWindow()
p = win.addPlot(1,0)
p.showGrid(x=True,y=True)
vel = []
velPlan(10, 0, 0, 10, 0.02, 1, vel)
curve = p.plot(y = vel, pen="y", symbolBrush=(255,0,0), symbolPen='w')
p1 = win.addPlot(2,0)
p1.showGrid(x=True,y=True)
vel = []
velPlan(50, 0, 0, 10, 0.02, 1, vel)
curve = p1.plot(y = vel, pen="y", symbolBrush=(255,0,0), symbolPen='w')

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

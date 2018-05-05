# -*- coding: utf-8 -*-

import numpy as np
# =============================================================================
# 场景和接入设置

nBS = 1          # 宏小区数目
Dis = 500        # 宏小区中心间距m
CL_exist=False   # 是否用簇
nCL=1            # 宏小区簇数目
nSM = 5         # 宏小区基站数目
nUE = 5         # 宏小区用户数目
nNt = 2          # 每个微基站天线数目
CL_RS =240       # 基站外围半径m
CL_RU =240       # 用户外围半径m
cl_min_Dist =50  # 簇之间最小间隔 
sm_min_Dist =20  # 微基站最小间距m
ue_sm_min_Dist = 10       # 用户基站最小间距m
mode=1                    # 接入方式       
if mode==0:               # mode 0：就近接入不接次近
    select_mode='min_dist'
    servUser=None         
elif mode==1:             # mode 1：就近接入，限接入数目，就近满接次近
    select_mode='min_dist'
    servUser=1            # 规定同一时刻允许接入的用户数，需满足 总nue<=总sm
else:                     # mode 2: 稳定匹配             需满足 总nue==总sm
    if nSM==nUE:
        select_mode='stable_match'
# =============================================================================
# 功率和路损参数

c=3e8       # c m/s
f=1e9       # 20MHZ
lamda=c/f   # 波长
d0=1        # 参考距离m
n=3.71      # 路径损耗因子
u_shadow=0  # 阴影衰落标准差dB
antGain=0   # 天线增益
pathLoss_re=20*np.log10((4*np.pi*d0)/lamda)  # 全向天线在参考距离d0处的路径损耗dB
P_sm_dbm = 30;                   #微基站发射功率dBm
P_sm=10**(P_sm_dbm/10)/1000      #微基站发射功率w
P_sigma = -95                    #接收端噪声功率dBm
P_sm=10**(P_sigma/10)/1000      #接收端噪声功率w
# path_Loss= pathLoss_re + 10*n*log10(d/d0) + u_shadow*np.random.rand(1) - antGain
# =============================================================================
# 任务参数

Tslot=60                 # 观测时长s
Ts=1                     # 帧长s
n_frame=int(Tslot/Ts)    # 帧数
Tms=0.01                 # 时隙长s
n_slot=int(Ts/Tms)      # 每帧时隙数
N_slot=n_frame*n_slot    # 总时隙数
B_Mbyte=60               # Bytes
B_bit=B_Mbyte*1024*1024*8# bits
# =============================================================================

# -*- coding: utf-8 -*-
from config import Dis,CL_RS,CL_RU,nUE,nSM,nBS,nCL,cl_min_Dist,sm_min_Dist,ue_sm_min_Dist,CL_exist
import numpy as np
from pathloss_slot import largeScaleFading

def cell_set(nBS,CL_exist=False):
     #  BS,
    bs_pos=[]
    bs_pos.append(complex(0.0))
    start=np.pi/6
    gap=  np.pi/3
    if nBS!=1 and nBS<=7:
        bs_pos.extend(list(map(lambda theta: Dis*np.exp(1j*theta),\
             [start+i*gap  for i in range(nBS-1)])))                 # pi/6, pi/6+1*pi/3, pi/6+2*pi/3
    bs_pos=np.array(bs_pos)
    CL_list=None
    # ========no cluster=====================================================================
    if not CL_exist:
    # sm: nBS,nSM
        SM_list=[]
        for ibs in range(nBS):
            sm_list=[]
            for ism in range(nSM):
                while 1:
                    sm_PosiTemp=(np.random.random(1)-0.5+1j*(np.random.random(1)-0.5))*CL_RS*2
                    sm_Posi=sm_PosiTemp+bs_pos[ibs]
                    if abs(sm_PosiTemp)<CL_RS and meet_min_dist(np.array(sm_list),sm_Posi,sm_min_Dist):
                        sm_list.append(list(sm_Posi)[0])
                        break
            SM_list.append(sm_list)  
    # user：nBS,nUE
        UE_list=[]
        for ibs in range(nBS):
            sm_list=SM_list[ibs]                                                        # 该小区所有微基站
            ue_list=[]
            for iue in range(nUE):
                while 1:
                    ue_PosiTemp=(np.random.random(1)-0.5+1j*(np.random.random(1)-0.5))*CL_RU*2
                    ue_Posi=ue_PosiTemp+bs_pos[ibs]
                    if abs(ue_PosiTemp)<CL_RS and meet_min_dist(np.array(sm_list),ue_Posi,ue_sm_min_Dist):
                        ue_list.append(list(ue_Posi)[0])
                        break
            UE_list.append(ue_list)
    # ========cluster based=====================================================================
    else:
        CL_list=[] # nBS,nCL
        x_Range = Dis*np.tan(np.pi/6)*3/2
        y_Range = Dis
        for ibs in range(nBS):
            restart=1                                                          #如果200次都没有撒好，完全从头撒
            while restart==1:
                cl_list=[]
                for icl in range(nCL):
                    cnt=0                                                      #撒200次后，break
                    while 1:
                        x_Posi = x_Range*(np.random.random(1)-2/3)
                        y_Posi = y_Range*(np.random.random(1)-0.5)
                        if y_Posi > x_Posi*np.tan(np.pi/3)+Dis:
                            x_Posi = x_Posi+x_Range
                            y_Posi = y_Posi-y_Range/2
                        elif y_Posi < -x_Posi*np.tan(np.pi/3)-Dis:
                            x_Posi = x_Posi+x_Range
                            y_Posi = y_Posi+y_Range/2
                        Dist = abs(x_Posi+1j*y_Posi)                           #簇中心与宏小区中心距离
                        if Dist < Dis/2- CL_RU:
                            cl_Posi= x_Posi+1j*y_Posi+bs_pos[ibs]
                            if meet_min_dist(np.array(cl_list),cl_Posi,cl_min_Dist):
                                cl_list.append(list(cl_Posi)[0])
                                finish = 1                                     #分下一个cl
                                restart = 0                                    
                                break
                            cnt = cnt+1                                        #cl分配失败次数+1
                            if cnt == 200:
                                finish = 0                                     #200还没跳出去，重来
                                break             
                    if finish == 0:                                            # 放弃这个cl
                        restart = 1                                            # 完全跳出这个循环，从这个ibs的第一个cl开始重新分
                        break
            CL_list.append(cl_list)
            
    # sm: nBS,nCL,nSM
        SM_list=[]
        for ibs in range(nBS):
            cl_sm_list=[]
            for icl in range(nCL):
                sm_list=[]
                for ism in range(nSM):
                    while 1:
                        sm_PosiTemp=(np.random.random(1)-0.5+1j*(np.random.random(1)-0.5))*CL_RS*2
                        sm_Posi=sm_PosiTemp+CL_list[ibs][icl]
                        if abs(sm_PosiTemp)<CL_RS and meet_min_dist(np.array(sm_list),sm_Posi,sm_min_Dist):
                            sm_list.append(list(sm_Posi)[0])
                            break
                cl_sm_list.append(sm_list)
            SM_list.append(cl_sm_list)
    # user：nBS,nUE
        UE_list=[]
        for ibs in range(nBS):
            cl_ue_list=[]
            for icl in range(nCL):
                sm_list=SM_list[ibs][icl]                                      # 该小区所有微基站
                ue_list=[]
                for iue in range(nUE):
                    while 1:
                        ue_PosiTemp=(np.random.random(1)-0.5+1j*(np.random.random(1)-0.5))*CL_RU*2
                        ue_Posi=ue_PosiTemp+CL_list[ibs][icl]
                        if abs(ue_PosiTemp)<CL_RU and meet_min_dist(np.array(sm_list),ue_Posi,ue_sm_min_Dist):
                            ue_list.append(list(ue_Posi)[0])
                            break
                cl_ue_list.append(ue_list)
            UE_list.append(cl_ue_list)
    return list(bs_pos),CL_list,SM_list,UE_list

# 是否满足用户基站，基站间最小距离
def meet_min_dist(old_pos,current_pos,min_dist):
    l=len(old_pos)
    if l==0:
        return True
    else:
        return np.sum(abs(old_pos-current_pos)>min_dist)==l
    
import matplotlib.pyplot as plt    

def plot(bs_pos,CL_list,SM_list,UE_list,CL_exist=True):
    if CL_exist:
        for ibs in range(nBS):
            vertex = bs_pos[ibs] + Dis*np.tan(np.pi/6)*np.exp(1j*np.pi/3*np.arange(7))
            plt.plot(vertex.real,vertex.imag)
            plt.text(bs_pos[ibs].real,bs_pos[ibs].imag,'BS{}'.format(ibs))
            for icl in range(nCL):
                #画出簇的位置
                vertex = CL_list[ibs][icl] + CL_RS*np.exp(1j*np.pi/10*np.arange(21))
                plt.plot(vertex.real,vertex.imag)
                for ism in range(nSM):
                    plt.plot(SM_list[ibs][icl][ism].real,SM_list[ibs][icl][ism].imag,'rD')
                    for iue in range(nUE):
                        plt.plot(UE_list[ibs][icl][iue].real,UE_list[ibs][icl][iue].imag,'b*')
    else:
        for ibs in range(nBS):
            vertex = bs_pos[ibs] + Dis*np.tan(np.pi/6)*np.exp(1j*np.pi/3*np.arange(7))
            plt.plot(vertex.real,vertex.imag)
            plt.text(bs_pos[ibs].real,bs_pos[ibs].imag,'BS{}'.format(ibs))
            for ism in range(nSM):
                plt.plot(SM_list[ibs][ism].real,SM_list[ibs][ism].imag,'rD')
                plt.text(SM_list[ibs][ism].real,SM_list[ibs][ism].imag,'SM{}'.format(ibs*nSM+ism))
            for iue in range(nUE):
                plt.plot(UE_list[ibs][iue].real,UE_list[ibs][iue].imag,'b*')
                plt.text(UE_list[ibs][iue].real,UE_list[ibs][iue].imag,'UE{}'.format(ibs*nUE+iue))
    plt.show()
    
    
bs_pos,CL_list,SM_list,UE_list=cell_set(nBS,CL_exist)
plot(bs_pos,CL_list,SM_list,UE_list,CL_exist) 
pathLoss,pathLossdB=largeScaleFading(SM_list,UE_list,CL_exist)
   

    
        
        
            
            

    

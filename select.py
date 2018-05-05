# -*- coding: utf-8 -*-
# 输出基站接入的用户编号
from config import *
def select(pathLoss,pathLossdB,select_mode,servUser):
    SM_dic={}
    SM_len={}
    max_nUE=0
    
    # 1 每个用户都选择距离自己最近的基站接入,基站若接入多用户，频分
    if select_mode=='min_dist':
        for iue in range(nUE):
            pathLossdB_list=list(pathLossdB[iue,:])              # iue与所有基站间路径损耗
            value=sorted(pathLossdB_list)
            index=[pathLossdB_list.index(i) for i in value]      # 排序
        # 1.1 基站同一时刻最多接入有限个用户                       # mode 1
            if servUser is not None:
                flag=0                                           # 立个flag,说：没有基站要我
                for i in range(len(index)):   
                    if SM_dic.get(index[i])==None:                 # 该基站还未接入任何用户
                        SM_select=[] 
                        flag=1                                   # 被打脸，被收留
                        break
                    else:
                        SM_select=SM_dic[index[i]]               # 基站i已有接入用户 
                        if len(SM_select)>=servUser:             # 基站i已满，到下一个i
                                continue                    
                        else:
                            flag=1                               # 被打脸，被收留
                            break
                SM_select.append(iue)                            # 加入基站i豪华套餐
                SM_dic[index[i]]=SM_select                       
                SM_len[index[i]]=len(SM_select)
                if len(SM_select)>max_nUE:
                    max_nUE=len(SM_select)
                if flag==0:                                      # 如果最终都满了，用户无处可去。
                    #print(' n_user more than n_sm*servUser !')
                    raise NameError(' n_user more than n_sm*servUser !')
        # 1.2 基站同一时刻不限制接入用户数目                       # mode 0
            else:
                if SM_dic.get(index[0])!=None:
                   SM_select=SM_dic[index[0]]
                   if len(SM_select)>max_nUE:
                       max_nUE=len(SM_select)
                else:
                    SM_select=[]
                SM_select.append(iue)
                SM_dic[index[0]]=SM_select
                SM_len[index[0]]=len(SM_select)
    # 2 稳定匹配,一用户一基站    O(n**2)
    else:
        if pathLoss.shape[0]==pathLoss.shape[1]:
            max_nUE=1
            # 建立prefer list
            UE_prefer=dict()
            for iue in range(nUE):
                pathLossdB_list=list(pathLossdB[iue,:])              # iue与所有基站间路径损耗
                value=sorted(pathLossdB_list)
                index=[pathLossdB_list.index(i) for i in value]      # 排序
                UE_prefer[iue]=index
                
            SM_prefer=dict()
            for ism in range(nSM):
                pathLossdB_list=list(pathLossdB[:,ism])              # iue与所有基站间路径损耗
                value=sorted(pathLossdB_list)
                index=[pathLossdB_list.index(i) for i in value]      # 排序
                SM_prefer[ism]=index
                
            freeman_list=list(range(nUE))                            # 记录每一轮没有配偶的boy.初始为全部男生
            man_propose_dict=dict()                                  # 记录每个男生已经求过婚的女生 在自己preferlist位置 
            for i in range(nUE):                      
                man_propose_dict[i]=0
                SM_len[i]=1
            
            while len(freeman_list)!=0:
                for iue in freeman_list:                             #每个还没有姑娘的男生
                    boy_prefer=UE_prefer[iue]                        # boy的 prefer list
                    g_start=man_propose_dict[iue]                    # 从start_gril开始
                    for g in boy_prefer[g_start:]:
                        if SM_dic.get(g)==None:                      # 该姑娘还未嫁人
                            SM_dic[g]=iue                            # 先找这个男孩处着
                            freeman_list.remove(iue)                 # 不是一个free man了
                            man_propose_dict[iue]=g_start+1          # 下次从新的girl开始
                            break
                        else:
                            enemy=SM_dic[g]                          # 姑娘已经心属enenmy
                            # compare him和enemy
                            g_prefer=SM_prefer[g]
                            if g_prefer.index(iue)<g_prefer.index(enemy):
                                SM_dic[g]=iue                        #恭喜boy,战胜情敌，让姑娘爱上自己
                                freeman_list.remove(iue)             # iue 不是一个free man了
                                man_propose_dict[iue]=g_start+1      # 下次从新的girl开始
                                freeman_list.append(enemy)           #  enenmy变单身
                                break
                            else:                                    # 挑战失败
                                continue                             # 向下一个女孩求婚，直到所有姑娘全求完，总会遇到一个
    return SM_dic,SM_len,max_nUE
            
SM_dic,SM_len,max_nUE=select(pathLoss,pathLossdB,select_mode,servUser)   # mode 2:返回的不是list         
            
            
        

        
    


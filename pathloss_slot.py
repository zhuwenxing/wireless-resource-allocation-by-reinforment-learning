from config import nUE,nSM,nBS,nCL,CL_exist,n,pathLoss_re,d0,u_shadow,antGain
import numpy as np
re=pathLoss_re
shadow=u_shadow*np.random.rand(1)
# 路径损耗
def largeScaleFading(sm_Posi,ue_Posi,CL_exist):
    pathLossdB=np.zeros([nBS*nUE,nBS*nSM])
    if not CL_exist:
        for ibs in range(nBS):
            for ism in range(nSM):
                for jbs in range(nBS):
                    for iue in range(nUE):               
                        dis=abs(sm_Posi[ibs][ism] - ue_Posi[jbs][iue])
                        pathLossdB[jbs*nUE+iue,ibs*nSM+ism]=re + 10*n*np.log10(dis/d0) + shadow - antGain
        pathLoss = 10**((-pathLossdB)/10)
    else:
        for ibs in range(nBS):
            for icl in range(nCL):
                for ism in range(nSM):
                    for jbs in range(nBS):
                        for jcl in range(nCL):
                            for iue in range(nUE):               
                                dis=abs(sm_Posi[ibs][icl][ism] - ue_Posi[jbs][jcl][iue])
                                pathLossdB[jbs*nUE*nCL+jcl*nUE+iue,ibs*nSM*nCL+icl*nSM+ism]=re + 10*n*np.log10(dis/d0) + shadow - antGain
        pathLoss = 10**((-pathLossdB)/10)
    return  pathLoss,pathLossdB
        


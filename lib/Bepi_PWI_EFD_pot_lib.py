"""
    BepiColombo Mio PWI EFD Pot: L1 QL -- 2025/7/26
"""
import numpy as np
import math

import sys
sys.path.append('./lib/')
import Bepi_PWI_EFD_lib  as bepi_lib

class struct:
    pass

# ---------------------------------------------------------------------
# --- EFD SPEC --------------------------------------------------------
# ---------------------------------------------------------------------
def efd_pot_read(cdf, mode_tlm):
    """
    input:  CDF
    return: data
    """
    # print(cdf)
    # print(cdf['Vu1_1hz'].attrs)
    # print(cdf['Vu1_1hz'].attrs['VALIDMAX'])

    data = struct()
    if mode_tlm=='l':       # L
        data.Vu1        = cdf['Vu1_1hz'][...]           # CDF_REAL4 [,]
        data.Vu2        = cdf['Vu2_1hz'][...]           # CDF_REAL4 [,]
        data.Vv1        = cdf['Vv1_1hz'][...]           # CDF_REAL4 [,]
        data.Vv2        = cdf['Vv2_1hz'][...]           # CDF_REAL4 [,]
        data.t_offset   = [0]
    elif mode_tlm=='m':     # M
        data.Vu1        = cdf['Vu1_8hz'][...]           # CDF_REAL4 [,8]
        data.Vu2        = cdf['Vu2_8hz'][...]           # CDF_REAL4 [,8]
        data.Vv1        = cdf['Vv1_8hz'][...]           # CDF_REAL4 [,8]
        data.Vv2        = cdf['Vv2_8hz'][...]           # CDF_REAL4 [,8]
        data.t_offset   = cdf['t_offset_8hz']
    else:                   # H
        data.Vu1        = cdf['Vu1_32hz'][...]          # CDF_REAL4 [,]
        data.Vu2        = cdf['Vu2_32hz'][...]          # CDF_REAL4 [,]
        data.Vv1        = cdf['Vv1_32hz'][...]          # CDF_REAL4 [,]
        data.Vv2        = cdf['Vv2_32hz'][...]          # CDF_REAL4 [,]
        data.t_offset   = cdf['t_offset_32hz']
    if mode_tlm!='h':       # L & M: from HK
        data.BIAS_LVL_U1= cdf['BIAS_LVL_U1'][...]       # CDF_REAL4 []      EWO HW-HK - B3 WPT1_BIAS
        data.BIAS_LVL_U2= cdf['BIAS_LVL_U2'][...]       # CDF_REAL4 []      EWO HW-HK - B4 WPT2_BIAS
        data.BIAS_LVL_V1= cdf['BIAS_LVL_V1'][...]       # CDF_REAL4 []      MEF HW-HK - B10-11 (BDAC1)
        data.BIAS_LVL_V2= cdf['BIAS_LVL_V2'][...]       # CDF_REAL4 []      MEF HW-HK - B12-13 (BDAC2)
        data.HK_WPT     = cdf['HK_WPT'][...]            # CDF_UINT1 [,8]    EWO HW-HK -  0- 8 B
        data.HK_MEF     = cdf['HK_MEF'][...]            # CDF_UINT1 [,10]   MEF HW-HK - 10-19 B

        data.EFD_Vu1_ENA= cdf['EFD_Vu1_ENA'][...]       # CDF_UINT1 []      PRE_U_PWR && PRE_U_LOOP && !PRE_U_CAL && PRE_V_PWR (Eu: PRE_U_PWR)
        data.EFD_Vu2_ENA= cdf['EFD_Vu2_ENA'][...]       # CDF_UINT1 []      
        data.EFD_Vv1_ENA= cdf['EFD_Vv1_ENA'][...]       # CDF_UINT1 []      PRE_V_PWR &&                          && PRE_V_PWR (Ev: PRE_V_PWR)    
        data.EFD_Vv2_ENA= cdf['EFD_Vv2_ENA'][...]       # CDF_UINT1 []      
        data.EFD_Hdump  = cdf['EFD_Hdump'][...]         # CDF_UINT1 []      
        data.EFD_sweep  = cdf['EFD_sweep'][...]         # CDF_UINT1 []      Slow-sweep (CAL) mode
        data.PRE_U_PWR  = cdf['PRE_U_PWR'][...]         # CDF_UINT1 []      EWO HK - B0 b1 (WPT-PRE)
        data.PRE_V_PWR  = cdf['PRE_V_PWR'][...]         # CDF_UINT1 []      MEF HK - B19 b6      
        data.PRE_U_CAL  = cdf['PRE_U_CAL'][...]         # CDF_UINT1 []      EWO HK - B0 b3 (WPT-CAL)
        data.PRE_V_CAL  = cdf['PRE_V_CAL'][...]         # CDF_UINT1 []      MEF HK - B19 b7
        data.PRE_U_LOOP = cdf['PRE_U_LOOP'][...]        # CDF_UINT1 []      EWO HK - B0 b6 (WPT-BIAS) & B1 b7 (EFD-FEEDBACK-LOOP) 
        data.AM2P_ENA   = cdf['AM2P_ENA'][...]          # CDF_UINT1 []      Gui_AM2P_start_TI < Gui_EFD_DPB_Ti[4] && Gui_EFD_DPB_Ti[0] < Gui_AM2P_end_TI   <<<
    #
    data.EFD_saturation = cdf['EFD_saturation'][...]    # CDF_UINT1 []      >30000, <30000
    data.EFD_spinrate   = cdf['EFD_spinrate'][...]      # CDF_REAL4 []
    data.EFD_spinphase  = cdf['EFD_spinphase'][...]     # CDF_REAL4 []
    data.epoch          = cdf['epoch'][...]             # CDF_TIME_TT2000 [208]
    data.EFD_TI         = cdf['EFD_TI'][...]           # CDF_UINT4 []

    """
    epoch_delta1
    epoch_delta2
    mdp_ti
    ap_id
    cat_id
    ccsds_hdr
    ewo_cnt
    lofo_id
    attr_id
    dr_id
    head_id
    fm_hdr
    cmp  
    """
    return data


def efd_pot_add(data, data1, mode_tlm):
    """
    input:  data, data1
    return: data
    """
    data.Vu1            = np.r_["0", data.Vu1,              data1.Vu1]
    data.Vu2            = np.r_["0", data.Vu2,              data1.Vu2]
    data.Vv1            = np.r_["0", data.Vv1,              data1.Vv1]
    data.Vv2            = np.r_["0", data.Vv2,              data1.Vv2]
    if mode_tlm!='h':       # L & M
        data.BIAS_LVL_U1= np.r_["0", data.BIAS_LVL_U1,      data1.BIAS_LVL_U1]
        data.BIAS_LVL_U2= np.r_["0", data.BIAS_LVL_U2,      data1.BIAS_LVL_U2]
        data.BIAS_LVL_V1= np.r_["0", data.BIAS_LVL_V1,      data1.BIAS_LVL_V1]
        data.BIAS_LVL_V2= np.r_["0", data.BIAS_LVL_V2,      data1.BIAS_LVL_V2]
        data.HK_WPT     = np.r_["0", data.HK_WPT,           data1.HK_WPT]
        data.HK_MEF     = np.r_["0", data.HK_MEF,           data1.HK_MEF]
        #
        data.EFD_Vu1_ENA= np.r_["0", data.EFD_Vu1_ENA,      data1.EFD_Vu1_ENA]
        data.EFD_Vu2_ENA= np.r_["0", data.EFD_Vu2_ENA,      data1.EFD_Vu2_ENA]
        data.EFD_Vv1_ENA= np.r_["0", data.EFD_Vv1_ENA,      data1.EFD_Vv1_ENA]
        data.EFD_Vv2_ENA= np.r_["0", data.EFD_Vv2_ENA,      data1.EFD_Vv2_ENA]
        #
        data.EFD_Hdump  = np.r_["0", data.EFD_Hdump,        data1.EFD_Hdump]
        data.EFD_sweep  = np.r_["0", data.EFD_sweep,        data1.EFD_sweep]
        data.PRE_U_PWR  = np.r_["0", data.PRE_U_PWR,        data1.PRE_U_PWR]
        data.PRE_V_PWR  = np.r_["0", data.PRE_V_PWR,        data1.PRE_V_PWR]
        data.PRE_U_CAL  = np.r_["0", data.PRE_U_CAL,        data1.PRE_U_CAL]
        data.PRE_V_CAL  = np.r_["0", data.PRE_V_CAL,        data1.PRE_V_CAL]
        data.PRE_U_LOOP = np.r_["0", data.PRE_U_LOOP,       data1.PRE_U_LOOP]
        data.AM2P_ENA   = np.r_["0", data.AM2P_ENA,         data1.AM2P_ENA]
    #
    data.EFD_saturation = np.r_["0", data.EFD_saturation,   data1.EFD_saturation]
    data.EFD_spinrate   = np.r_["0", data.EFD_spinrate,     data1.EFD_spinrate]
    data.EFD_spinphase  = np.r_["0", data.EFD_spinphase,    data1.EFD_spinphase]
    data.epoch          = np.r_["0", data.epoch,            data1.epoch]
    data.EFD_TI         = np.r_["0", data.EFD_TI,           data1.EFD_TI]

    return data


def efd_pot_shaping(data, cal_mode, mode_tlm, mode_ant):
    """
    input:  data
            cal_mode    [Power]     0: background          1: CAL           2: all
            mode_tlm    l, m, h
            mode_ant    # 0:both    1:U(WPT)    2:V(MEF)
    return: data
    """

    # Selection: CAL, N_ch, comp_mode
    if cal_mode < 2:
        print("       org:", data.Vu1.shape)
        index = np.where(data.PRE_U_CAL == cal_mode)
        data.Vu1            = data.Vu1           [index[0]]
        data.Vu2            = data.Vu2           [index[0]]
        data.Vv1            = data.Vv1           [index[0]]
        data.Vv2            = data.Vv2           [index[0]]
        data.BIAS_LVL_U1    = data.BIAS_LVL_U1   [index[0]]
        data.BIAS_LVL_U2    = data.BIAS_LVL_U2   [index[0]]
        data.BIAS_LVL_V1    = data.BIAS_LVL_V1   [index[0]]
        data.BIAS_LVL_V2    = data.BIAS_LVL_V2   [index[0]]
        data.HK_WPT         = data.HK_WPT        [index[0]]
        data.HK_MEF         = data.HK_MEF        [index[0]]
        #
        data.EFD_Vu1_ENA    = data.EFD_Vu1_ENA   [index[0]]
        data.EFD_Vu2_ENA    = data.EFD_Vu2_ENA   [index[0]]
        data.EFD_Vv1_ENA    = data.EFD_Vv1_ENA   [index[0]]
        data.EFD_Vv2_ENA    = data.EFD_Vv2_ENA   [index[0]]
        data.EFD_Hdump      = data.EFD_Hdump     [index[0]]
        data.EFD_saturation = data.EFD_saturation[index[0]]
        data.EFD_spinrate   = data.EFD_spinrate  [index[0]]
        data.EFD_spinphase  = data.EFD_spinphase [index[0]]
        data.EFD_sweep      = data.EFD_sweep     [index[0]]
        data.PRE_U_PWR      = data.PRE_U_PWR     [index[0]]
        data.PRE_V_PWR      = data.PRE_V_PWR     [index[0]]
        data.PRE_U_CAL      = data.PRE_U_CAL     [index[0]]
        data.PRE_V_CAL      = data.PRE_V_CAL     [index[0]]
        data.PRE_U_LOOP     = data.PRE_U_LOOP    [index[0]]
        data.AM2P_ENA       = data.AM2P_ENA      [index[0]]
        #
        data.epoch          = data.epoch         [index[0]]
        data.EFD_TI         = data.EFD_TI        [index[0]]
        #
        if cal_mode == 0:
            print("<only  BG>:", data.Vu1.shape)
        else:
            print("<only CAL>:", data.Vu1.shape)

    data.n_time = data.Vu1.shape[0]
    if mode_tlm != 'l': data.n_dt = data.Vu1.shape[1]
    else:               data.n_dt = 1

    # NAN: bias value
    if mode_tlm != 'h':
        index = np.where(data.BIAS_LVL_U1 < -1e30);     data.BIAS_LVL_U1[index[0]] = math.nan
        index = np.where(data.BIAS_LVL_U2 < -1e30);     data.BIAS_LVL_U2[index[0]] = math.nan
        index = np.where(data.BIAS_LVL_V1 < -1e30);     data.BIAS_LVL_V1[index[0]] = math.nan
        index = np.where(data.BIAS_LVL_V2 < -1e30);     data.BIAS_LVL_V2[index[0]] = math.nan

    # NAN: data value
    if mode_tlm != 'l':
        data.Vu1 = np.ravel(data.Vu1);      data.Vu2 = np.ravel(data.Vu2)
        data.Vv1 = np.ravel(data.Vv1);      data.Vv2 = np.ravel(data.Vv2)
    index = np.where(data.Vu1 < -1e30);     data.Vu1[index[0]] = math.nan
    index = np.where(data.Vu2 < -1e30);     data.Vu2[index[0]] = math.nan
    index = np.where(data.Vv1 < -1e30);     data.Vv1[index[0]] = math.nan
    index = np.where(data.Vv2 < -1e30);     data.Vv2[index[0]] = math.nan
    if mode_ant == 1:
        data.Vv1[:] = math.nan
        data.Vv2[:] = math.nan
    if mode_ant == 2:
        data.Vu1[:] = math.nan
        data.Vu2[:] = math.nan
    if mode_tlm != 'l':
        data.Vu1 = data.Vu1.reshape(data.n_time, data.n_dt)
        data.Vu2 = data.Vu2.reshape(data.n_time, data.n_dt)
        data.Vv1 = data.Vv1.reshape(data.n_time, data.n_dt)
        data.Vv2 = data.Vv2.reshape(data.n_time, data.n_dt)
    
    return data


def pot_nan(data, i):
    print("[gap]", data.epoch[i+1] - data.epoch[i], i, data.epoch[i], i+1, data.epoch[i+1])
    if (data.n_dt > 1):
        data.Vu1[i][:]   = math.nan;    data.Vu2[i][:]   = math.nan;    data.Vv1[i][:]   = math.nan;    data.Vv2[i][:]   = math.nan
        data.Vu1[i+1][:] = math.nan;    data.Vu2[i+1][:] = math.nan;    data.Vv1[i+1][:] = math.nan;    data.Vv2[i+1][:] = math.nan
    else:
        data.Vu1[i]      = math.nan;    data.Vu2[i]      = math.nan;    data.Vv1[i]      = math.nan;    data.Vv2[i]      = math.nan
        data.Vu1[i+1]    = math.nan;    data.Vu2[i+1]    = math.nan;    data.Vv1[i+1]    = math.nan;    data.Vv2[i+1]    = math.nan
    return


def pot_peak(pot, n_time0):
    n_sweep1 = 0;  n_sweep2 = n_time0//2;  n_sweep3 = n_time0-1

    peak_Vu1 = np.ravel(pot.Vu1);  peak_Vu2 = np.ravel(pot.Vu2)
    peak_Vv1 = np.ravel(pot.Vv1);  peak_Vv2 = np.ravel(pot.Vv2)
    p1_max, p1_min, p2_max, p2_min, p3_max, p3_min, p4_max, p4_min = bepi_lib.peak_data4(peak_Vu1, peak_Vu2, peak_Vv1, peak_Vv2)
    print("[ All   Peak]",
            "<Vu1>", '{:+.2e}'.format(p1_max), '{:+.2e}'.format(p1_min), 
            "<Vu2>", '{:+.2e}'.format(p2_max), '{:+.2e}'.format(p2_min), 
            "<Vv1>", '{:+.2e}'.format(p3_max), '{:+.2e}'.format(p3_min), 
            "<Vv2>", '{:+.2e}'.format(p4_max), '{:+.2e}'.format(p4_min) )
    
    peak_Vu1 = np.ravel(pot.Vu1[n_sweep1]);  peak_Vu2 = np.ravel(pot.Vu2[n_sweep1])
    peak_Vv1 = np.ravel(pot.Vv1[n_sweep1]);  peak_Vv2 = np.ravel(pot.Vv2[n_sweep1])
    p1_max, p1_min, p2_max, p2_min, p3_max, p3_min, p4_max, p4_min = bepi_lib.peak_data4(peak_Vu1, peak_Vu2, peak_Vv1, peak_Vv2)
    print("[", '{:5d} peak]'.format(n_sweep1), 
            "<Vu1>", '{:+.2e}'.format(p1_max), '{:+.2e}'.format(p1_min), 
            "<Vu2>", '{:+.2e}'.format(p2_max), '{:+.2e}'.format(p2_min), 
            "<Vv1>", '{:+.2e}'.format(p3_max), '{:+.2e}'.format(p3_min), 
            "<Vv2>", '{:+.2e}'.format(p4_max), '{:+.2e}'.format(p4_min) )

    peak_Vu1 = np.ravel(pot.Vu1[n_sweep2]);  peak_Vu2 = np.ravel(pot.Vu2[n_sweep2])
    peak_Vv1 = np.ravel(pot.Vv1[n_sweep2]);  peak_Vv2 = np.ravel(pot.Vv2[n_sweep2])
    p1_max, p1_min, p2_max, p2_min, p3_max, p3_min, p4_max, p4_min = bepi_lib.peak_data4(peak_Vu1, peak_Vu2, peak_Vv1, peak_Vv2)
    print("[", '{:5d} peak]'.format(n_sweep2),
            "<Vu1>", '{:+.2e}'.format(p1_max), '{:+.2e}'.format(p1_min), 
            "<Vu2>", '{:+.2e}'.format(p2_max), '{:+.2e}'.format(p2_min), 
            "<Vv1>", '{:+.2e}'.format(p3_max), '{:+.2e}'.format(p3_min), 
            "<Vv2>", '{:+.2e}'.format(p4_max), '{:+.2e}'.format(p4_min) )

    peak_Vu1 = np.ravel(pot.Vu1[n_sweep3]);  peak_Vu2 = np.ravel(pot.Vu2[n_sweep3])
    peak_Vv1 = np.ravel(pot.Vv1[n_sweep3]);  peak_Vv2 = np.ravel(pot.Vv2[n_sweep3])
    p1_max, p1_min, p2_max, p2_min, p3_max, p3_min, p4_max, p4_min = bepi_lib.peak_data4(peak_Vu1, peak_Vu2, peak_Vv1, peak_Vv2)
    print("[", '{:5d} peak]'.format(n_sweep3),
            "<Vu1>", '{:+.2e}'.format(p1_max), '{:+.2e}'.format(p1_min), 
            "<Vu2>", '{:+.2e}'.format(p2_max), '{:+.2e}'.format(p2_min), 
            "<Vv1>", '{:+.2e}'.format(p3_max), '{:+.2e}'.format(p3_min), 
            "<Vv2>", '{:+.2e}'.format(p4_max), '{:+.2e}'.format(p4_min) )
    return
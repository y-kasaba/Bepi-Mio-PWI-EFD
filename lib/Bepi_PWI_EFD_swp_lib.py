"""
    BepiColombo Mio PWI EFD Sweep: L1 QL -- 2025/11/5
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
def efd_swp_read(cdf, mode_ant):
    """
    input:  CDF
    return: data
    """
    data = struct()

    if mode_ant==1:
        data.Vu1           = cdf['Vx1_sweep'][...]          # CDF_REAL4 [,]
        data.Vu2           = cdf['Vx2_sweep'][...]          # CDF_REAL4 [,]
        data.WPT_Sweep_Tbl = cdf['EFD_X_SWP_TBL'][...]      # CDF_UINT4 []
    else:
        data.Vv1           = cdf['Vy1_sweep'][...]          # CDF_REAL4 [,]
        data.Vv2           = cdf['Vy2_sweep'][...]          # CDF_REAL4 [,]
    data.t_offset       = cdf['t_offset_1024hz'][...]
    data.sweep_ant      = cdf['sweep_ant'][...]             # CDF_UNIT1 []
    #
    data.EFD_saturation = cdf['EFD_saturation'][...]        # CDF_UINT1 []      >30000, <30000
    data.EFD_ti_index   = cdf['EFD_TI_INDEX'][...]          # CDF_UINT4 []
    data.EFD_ewo_counter= cdf['EFD_EWO_COUNTER'][...]       # CDF_UINT2 []
    data.EFD_TI         = cdf['EFD_TI'][...]                # CDF_UINT4 []
    data.epoch          = cdf['epoch'][...]                 # CDF_TIME_TT2000 [208]

    # quality flag [b16:E-saturated b17:POT-saturated b18:X_not-ENA b19:Y_not-ENA b20:X_not-biased b21:Y_not-biased b22:EFD_CAL_mode b23:X_ACAL_mode b24:AM2P_active]
    data.EFD_quality_flag = cdf['EFD_quality_flag'][...]            # CDF_UINT4 []
    data.EFD_U_ENA  = cdf['EFD_X_ENA'][...]                         # CDF_UINT1 []      EWO - B0/b1(WPT-PWR)=1 & B0/b7(WPT-DCAL)=0
    data.EFD_V_ENA  = cdf['EFD_Y_ENA'][...]                         # CDF_UINT1 []      MEF - HV > 74V
    data.BIAS_U     = cdf['BIAS_X'][...]                            # CDF_UINT1 []      EWO - B0/b6(WPT-BIAS)=1 & B1/b7(EFD-FB)=1 & B3-B4(BIAS1/2)!=0x80    
    data.BIAS_V     = cdf['BIAS_Y'][...]                            # CDF_UINT1 []      MEF - B10-13(BDAC1/2)!=0x8000 & B19 b4-5 =3
    data.EFD_CAL    = cdf['EFD_CAL'][...]                           # CDF_UINT1 []      EFD_CAL=1(slow-sweep)
    data.PRE_U_ACAL = cdf['PRE_X_ACAL'][...]                        # CDF_UINT1 []      EWO - B0/b3(WPT-ACAL)=1
    data.AM2P_ACT   = cdf['AM2P_ACT'][...]                          # CDF_UINT1 []      AM2P_stage=2-5
    data.BIAS_LVL_U1= cdf['BIAS_LVL_X1'][...]                       # CDF_REAL4 []      EWO HW-HK - B3 WPT1_BIAS
    data.BIAS_LVL_U2= cdf['BIAS_LVL_X2'][...]                       # CDF_REAL4 []      EWO HW-HK - B4 WPT2_BIAS
    data.BIAS_LVL_V1= cdf['BIAS_LVL_Y1'][...]                       # CDF_REAL4 []      MEF HW-HK - B10-11 (BDAC1)
    data.BIAS_LVL_V2= cdf['BIAS_LVL_Y2'][...]                       # CDF_REAL4 []      MEF HW-HK - B12-13 (BDAC2)
    data.BIAS_RAW_U1= cdf['BIAS_LVL_X1_raw'][...]                   # CDF_UINT1 []      EWO HW-HK - B3 WPT1_BIAS
    data.BIAS_RAW_U2= cdf['BIAS_LVL_X2_raw'][...]                   # CDF_UINT1 []      EWO HW-HK - B4 WPT2_BIAS
    data.BIAS_RAW_V1= cdf['BIAS_LVL_Y1_raw'][...]                   # CDF_UINT2 []      MEF HW-HK - B10-11 (BDAC1)
    data.BIAS_RAW_V2= cdf['BIAS_LVL_Y2_raw'][...]                   # CDF_UINT2 []      MEF HW-HK - B12-13 (BDAC2)
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
    t_offset_1024hz
    """
    return data


def efd_swp_add(data, data1, mode_ant):
    """
    input:  data, data1
    return: data
    """
    if mode_ant==1:
        data.Vu1            = np.r_["0", data.Vu1,              data1.Vu1]
        data.Vu2            = np.r_["0", data.Vu2,              data1.Vu2]
        data.WPT_Sweep_Tbl  = np.r_["0", data.WPT_Sweep_Tbl,    data1.WPT_Sweep_Tbl]
    else:
        data.Vv1            = np.r_["0", data.Vv1,              data1.Vv1]
        data.Vv2            = np.r_["0", data.Vv2,              data1.Vv2]
    #
    data.sweep_ant      = np.r_["0", data.sweep_ant,        data1.sweep_ant]
    data.EFD_saturation = np.r_["0", data.EFD_saturation,   data1.EFD_saturation]
    data.EFD_ti_index   = np.r_["0", data.EFD_ti_index,     data1.EFD_ti_index]
    data.EFD_ewo_counter= np.r_["0", data.EFD_ewo_counter,  data1.EFD_ewo_counter]
    data.EFD_TI         = np.r_["0", data.EFD_TI,           data1.EFD_TI]
    data.epoch          = np.r_["0", data.epoch,            data1.epoch]

    data.EFD_quality_flag= np.r_["0",data.EFD_quality_flag, data1.EFD_quality_flag]
    data.EFD_U_ENA      = np.r_["0", data.EFD_U_ENA,        data1.EFD_U_ENA]
    data.EFD_V_ENA      = np.r_["0", data.EFD_V_ENA,        data1.EFD_V_ENA]
    data.BIAS_U         = np.r_["0", data.BIAS_U,           data1.BIAS_U]
    data.BIAS_V         = np.r_["0", data.BIAS_V,           data1.BIAS_V]
    data.EFD_CAL        = np.r_["0", data.EFD_CAL,          data1.EFD_CAL]
    data.PRE_U_ACAL     = np.r_["0", data.PRE_U_ACAL,       data1.PRE_U_ACAL]
    data.AM2P_ACT       = np.r_["0", data.AM2P_ACT,         data1.AM2P_ACT]
    data.BIAS_LVL_U1    = np.r_["0", data.BIAS_LVL_U1,      data1.BIAS_LVL_U1]
    data.BIAS_LVL_U2    = np.r_["0", data.BIAS_LVL_U2,      data1.BIAS_LVL_U2]
    data.BIAS_LVL_V1    = np.r_["0", data.BIAS_LVL_V1,      data1.BIAS_LVL_V1]
    data.BIAS_LVL_V2    = np.r_["0", data.BIAS_LVL_V2,      data1.BIAS_LVL_V2]
    data.BIAS_RAW_U1    = np.r_["0", data.BIAS_RAW_U1,      data1.BIAS_RAW_U1]
    data.BIAS_RAW_U2    = np.r_["0", data.BIAS_RAW_U2,      data1.BIAS_RAW_U2]
    data.BIAS_RAW_V1    = np.r_["0", data.BIAS_RAW_V1,      data1.BIAS_RAW_V1]
    data.BIAS_RAW_V2    = np.r_["0", data.BIAS_RAW_V2,      data1.BIAS_RAW_V2]
    return data


def efd_swp_shaping(data, mode_ant):
    """
    input:  data
            cal_mode    [Power]     0: background          1: CAL           2: all
    return: data
    """
    # NAN: data value
    if mode_ant==1:
        data.n_time = data.Vu1.shape[0];        data.n_dt   = data.Vu1.shape[1]
        index = np.where(data.Vu1 < -1e30);     data.Vu1[index[0]] = math.nan
        index = np.where(data.Vu2 < -1e30);     data.Vu2[index[0]] = math.nan
        data.Vu1 = data.Vu1.reshape(data.n_time, data.n_dt)
        data.Vu2 = data.Vu2.reshape(data.n_time, data.n_dt)
    else:
        data.n_time = data.Vv1.shape[0];        data.n_dt   = data.Vv1.shape[1]
        index = np.where(data.Vv1 < -1e30);     data.Vv1[index[0]] = math.nan
        index = np.where(data.Vv2 < -1e30);     data.Vv2[index[0]] = math.nan
        data.Vv1 = data.Vv1.reshape(data.n_time, data.n_dt)
        data.Vv2 = data.Vv2.reshape(data.n_time, data.n_dt)
    
    return data


def swp_peak(pot, n_time0, mode_ant):
    n_sweep1 = 0;  n_sweep2 = n_time0//2;  n_sweep3 = n_time0-1

    if mode_ant==1:
        peak_Vu1 = np.ravel(pot.Vu1);  peak_Vu2 = np.ravel(pot.Vu2)
        p1_max, p1_min, p2_max, p2_min = bepi_lib.peak_data2(peak_Vu1, peak_Vu2)
        print("[ All   Peak]",
                "<Vu1>", '{:+.2e}'.format(p1_max), '{:+.2e}'.format(p1_min), 
                "<Vu2>", '{:+.2e}'.format(p2_max), '{:+.2e}'.format(p2_min) )
        peak_Vu1 = np.ravel(pot.Vu1[n_sweep1]);  peak_Vu2 = np.ravel(pot.Vu2[n_sweep1])

        p1_max, p1_min, p2_max, p2_min = bepi_lib.peak_data2(peak_Vu1, peak_Vu2)
        print("[", '{:5d} peak]'.format(n_sweep1), 
                "<Vu1>", '{:+.2e}'.format(p1_max), '{:+.2e}'.format(p1_min), 
                "<Vu2>", '{:+.2e}'.format(p2_max), '{:+.2e}'.format(p2_min) )

        peak_Vu1 = np.ravel(pot.Vu1[n_sweep2]);  peak_Vu2 = np.ravel(pot.Vu2[n_sweep2])
        p1_max, p1_min, p2_max, p2_min = bepi_lib.peak_data2(peak_Vu1, peak_Vu2)
        print("[", '{:5d} peak]'.format(n_sweep2),
                "<Vu1>", '{:+.2e}'.format(p1_max), '{:+.2e}'.format(p1_min), 
                "<Vu2>", '{:+.2e}'.format(p2_max), '{:+.2e}'.format(p2_min) )

        peak_Vu1 = np.ravel(pot.Vu1[n_sweep3]);  peak_Vu2 = np.ravel(pot.Vu2[n_sweep3])
        p1_max, p1_min, p2_max, p2_min = bepi_lib.peak_data2(peak_Vu1, peak_Vu2)
        print("[", '{:5d} peak]'.format(n_sweep3),
                "<Vu1>", '{:+.2e}'.format(p1_max), '{:+.2e}'.format(p1_min), 
                "<Vu2>", '{:+.2e}'.format(p2_max), '{:+.2e}'.format(p2_min) )
    else:
        peak_Vv1 = np.ravel(pot.Vv1);  peak_Vv2 = np.ravel(pot.Vv2)
        p3_max, p3_min, p4_max, p4_min = bepi_lib.peak_data2(peak_Vv1, peak_Vv2)
        print("[ All   Peak]",
                "<Vv1>", '{:+.2e}'.format(p3_max), '{:+.2e}'.format(p3_min), 
                "<Vv2>", '{:+.2e}'.format(p4_max), '{:+.2e}'.format(p4_min) )
        
        peak_Vv1 = np.ravel(pot.Vv1[n_sweep1]);  peak_Vv2 = np.ravel(pot.Vv2[n_sweep1])
        p3_max, p3_min, p4_max, p4_min = bepi_lib.peak_data2(peak_Vv1, peak_Vv2)
        print("[", '{:5d} peak]'.format(n_sweep1), 
                "<Vv1>", '{:+.2e}'.format(p3_max), '{:+.2e}'.format(p3_min), 
                "<Vv2>", '{:+.2e}'.format(p4_max), '{:+.2e}'.format(p4_min) )

        peak_Vv1 = np.ravel(pot.Vv1[n_sweep2]);  peak_Vv2 = np.ravel(pot.Vv2[n_sweep2])
        p3_max, p3_min, p4_max, p4_min = bepi_lib.peak_data2(peak_Vv1, peak_Vv2)
        print("[", '{:5d} peak]'.format(n_sweep2),
                "<Vv1>", '{:+.2e}'.format(p3_max), '{:+.2e}'.format(p3_min), 
                "<Vv2>", '{:+.2e}'.format(p4_max), '{:+.2e}'.format(p4_min) )

        peak_Vv1 = np.ravel(pot.Vv1[n_sweep3]);  peak_Vv2 = np.ravel(pot.Vv2[n_sweep3])
        p3_max, p3_min, p4_max, p4_min = bepi_lib.peak_data2(peak_Vv1, peak_Vv2)
        print("[", '{:5d} peak]'.format(n_sweep3),
                "<Vv1>", '{:+.2e}'.format(p3_max), '{:+.2e}'.format(p3_min), 
                "<Vv2>", '{:+.2e}'.format(p4_max), '{:+.2e}'.format(p4_min) )
    return
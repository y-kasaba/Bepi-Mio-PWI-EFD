"""
    BepiColombo Mio PWI EFD common lib -- 2025/11/11
"""
import numpy as np
import math

"""
    HK
"""
def status_read(cdf, data):
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
    """
    return data


def status_add(data, data1):
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


"""
    Peak
"""
def peak_spec2(data1, data2, freq, n_freq):
    p1_data = np.ravel(data1)
    if (~np.all(np.isnan(p1_data))):    
        p1_max = np.nanmax(p1_data);     f1_max = freq[np.nanargmax(p1_data) % n_freq]
    else:
        p1_max = math.nan;               f1_max = math.nan

    p2_data = np.ravel(data2)
    if (~np.all(np.isnan(p2_data))):
        p2_max = np.nanmax(p2_data);     f2_max = freq[np.nanargmax(p2_data) % n_freq]
    else:
        p2_max = math.nan;               f2_max = math.nan

    return  p1_max, f1_max, p2_max, f2_max


def peak_data2(data1, data2):
    p1_data = np.ravel(data1)
    if (~np.all(np.isnan(p1_data))):
        p1_max = np.nanmax(p1_data);     p1_min = np.nanmin(p1_data)
    else:
        p1_max = math.nan;               p1_min = math.nan

    p2_data = np.ravel(data2)
    if (~np.all(np.isnan(p2_data))):
        p2_max = np.nanmax(p2_data);     p2_min = np.nanmin(p2_data)
    else:
        p2_max = math.nan;               p2_min = math.nan

    return  p1_max, p1_min, p2_max, p2_min


def peak_data4(data1, data2, data3, data4):
    p1_data = np.ravel(data1)
    if (~np.all(np.isnan(p1_data))):
        p1_max = np.nanmax(p1_data);     p1_min = np.nanmin(p1_data)
    else:
        p1_max = math.nan;               p1_min = math.nan

    p2_data = np.ravel(data2)
    if (~np.all(np.isnan(p2_data))):
        p2_max = np.nanmax(p2_data);     p2_min = np.nanmin(p2_data)
    else:
        p2_max = math.nan;               p2_min = math.nan

    p3_data = np.ravel(data3)
    if (~np.all(np.isnan(p3_data))):
        p3_max = np.nanmax(p3_data);     p3_min = np.nanmin(p3_data)
    else:
        p3_max = math.nan;               p3_min = math.nan

    p4_data = np.ravel(data4)
    if (~np.all(np.isnan(p4_data))):
        p4_max = np.nanmax(p4_data);     p4_min = np.nanmin(p4_data)
    else:
        p4_max = math.nan;               p4_min = math.nan

    return  p1_max, p1_min, p2_max, p2_min, p3_max, p3_min, p4_max, p4_min
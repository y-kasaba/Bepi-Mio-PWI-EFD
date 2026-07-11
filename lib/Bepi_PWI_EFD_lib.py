"""
    BepiColombo Mio PWI EFD common lib -- 2026/7/11
"""
import numpy as np
import math

"""
    HK
"""
def status_read(cdf, data):
    # quality flag    b0: see Quality Note b1:Eclipse        b2:Maneuver     b3:MTQ
    #                 b8:U-CAL             b9:V-CAL         b10:DBSC-CAL    b11:LFSC-CAL 
    #                b16:E-saturated      b17:POT-saturated b18:U_not-ENA   b19:V_not-ENA b20:U_not-biased 
    #                b21:V_not-biased     b22:EFD_CAL_mode  b23:U_ACAL_mode b24:AM2P_active
    data.quality_flag = cdf['quality_flag'][...]                    # CDF_UINT4 []

    # quality level   0: Good
    #                 1: Minor     b0:Note          b3:MTQ          b10:DBSC-CAL      b11:LFSC-CAL      b23:U-ACAL  b24:AM2P-active
    #                 2: Major     b1:Eclipse       b2:Maneuver)    b20:U-non-biased  b21:V-non-biased
    #                 3: Bad	  b16:E-saturated  b17:U-saturated  b18:U-not-ENA     b19:V-not-ENA
    #                 9: Not-Sci   b8:U-CAL         b9:V-CAL        b22:EFD-CAL
    #                 10: To-be-qualified
    data.quality_level= cdf['quality_level'][...]                   # CDF_UINT1 []

    data.EFD_U_ENA  = cdf['EFD_U_ENA'][...]                         # CDF_UINT1 []      EWO - B0/b1(WPT-PWR)=1 & B0/b7(WPT-DCAL)=0
    data.EFD_V_ENA  = cdf['EFD_V_ENA'][...]                         # CDF_UINT1 []      MEF - HV > 74V
    data.BIAS_U     = cdf['BIAS_U'][...]                            # CDF_UINT1 []      EWO - B0/b6(WPT-BIAS)=1 & B1/b7(EFD-FB)=1 & B3-B4(BIAS1/2)!=0x80    
    data.BIAS_V     = cdf['BIAS_V'][...]                            # CDF_UINT1 []      MEF - B10-13(BDAC1/2)!=0x8000 & B19 b4-5 =3
    data.EFD_CAL    = cdf['EFD_CAL'][...]                           # CDF_UINT1 []      EFD_CAL=1(slow-sweep)
    data.PRE_U_ACAL = cdf['PRE_U_ACAL'][...]                        # CDF_UINT1 []      EWO - B0/b3(WPT-ACAL)=1
    data.AM2P_ACT   = cdf['AM2P_ACT'][...]                          # CDF_UINT1 []      AM2P_stage=2-5
    data.BIAS_LVL_U1= cdf['BIAS_LVL_U1'][...]                       # CDF_REAL4 []      EWO HW-HK - B3 WPT1_BIAS
    data.BIAS_LVL_U2= cdf['BIAS_LVL_U2'][...]                       # CDF_REAL4 []      EWO HW-HK - B4 WPT2_BIAS
    data.BIAS_LVL_V1= cdf['BIAS_LVL_V1'][...]                       # CDF_REAL4 []      MEF HW-HK - B10-11 (BDAC1)
    data.BIAS_LVL_V2= cdf['BIAS_LVL_V2'][...]                       # CDF_REAL4 []      MEF HW-HK - B12-13 (BDAC2)
    data.BIAS_RAW_U1= cdf['BIAS_LVL_U1_raw'][...]                   # CDF_UINT1 []      EWO HW-HK - B3 WPT1_BIAS
    data.BIAS_RAW_U2= cdf['BIAS_LVL_U2_raw'][...]                   # CDF_UINT1 []      EWO HW-HK - B4 WPT2_BIAS
    data.BIAS_RAW_V1= cdf['BIAS_LVL_V1_raw'][...]                   # CDF_UINT2 []      MEF HW-HK - B10-11 (BDAC1)
    data.BIAS_RAW_V2= cdf['BIAS_LVL_V2_raw'][...]                   # CDF_UINT2 []      MEF HW-HK - B12-13 (BDAC2)
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
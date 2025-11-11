"""
    BepiColombo Mio PWI EFD Spec: L1 QL -- 2025/11/11
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
def efd_spec_read(cdf, mode_tlm, mode_L):
    """
    input:  CDF
    return: data
    """
    data = struct()
    # print(cdf)

    if mode_tlm=='h':
        data.EuEu           = cdf['Ex_power'][...]          # CDF_REAL4 [208, 16]
        data.EvEv           = cdf['Ey_power'][...]          # CDF_REAL4 [208, 16]
        data.spec_freq      = cdf['spec_freq_50hz'][...]    # CDF_REAL4 [16]
    else:
        if mode_tlm=='l':
            if mode_L==0:
                data.EuEu   = cdf['Ex_power_ave'][...]          # CDF_REAL4 [208, 16]
                data.EvEv   = cdf['Ey_power_ave'][...]          # CDF_REAL4 [208, 16]
            else:
                data.EuEu   = cdf['Ex_power_peak'][...]         # CDF_REAL4 [208, 16]
                data.EvEv   = cdf['Ey_power_peak'][...]         # CDF_REAL4 [208, 16]
        else:
            data.EuEu       = cdf['Ex_power'][...]              # CDF_REAL4 [208, 16]
            data.EvEv       = cdf['Ey_power'][...]              # CDF_REAL4 [208, 16]
        data.spec_freq      = cdf['spec_freq'][...]         # CDF_REAL4 [16]
        data.spec_width     = cdf['spec_width'][...]        # CDF_REAL4 [16]

    # from HK
    data.EFD_saturation = cdf['EFD_saturation'][...]    # CDF_UINT1 [208]      >30000, <30000
    if mode_tlm!='h':
        data.EFD_Hdump      = cdf['EFD_HDUMP'][...]         # CDF_UINT1 []      Hdump=1
        data.EFD_delay      = cdf['EFD_DELAY'][...]         # CDF_REAL4 []
    data.EFD_spinrate   = cdf['spinrate'][...]          # CDF_REAL4 [208]
    data.EFD_spinphase  = cdf['spinphase'][...]         # CDF_REAL4 [208]
    data.EFD_TI         = cdf['EFD_TI'][...]            # CDF_UINT4 []
    data.epoch          = cdf['epoch'][...]             # CDF_TIME_TT2000 [208]

    bepi_lib.status_read(cdf, data)
    """
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


def efd_spec_add(data, data1):
    """
    input:  data, data1
    return: data
    """
    data.EuEu           = np.r_["0", data.EuEu,             data1.EuEu]
    data.EvEv           = np.r_["0", data.EvEv,             data1.EvEv]
    #
    data.EFD_Hdump      = np.r_["0", data.EFD_Hdump,        data1.EFD_Hdump]
    data.EFD_saturation = np.r_["0", data.EFD_saturation,   data1.EFD_saturation]
    data.EFD_spinrate   = np.r_["0", data.EFD_spinrate,     data1.EFD_spinrate]
    data.EFD_spinphase  = np.r_["0", data.EFD_spinphase,    data1.EFD_spinphase]
    data.EFD_TI         = np.r_["0", data.EFD_TI,           data1.EFD_TI]
    data.EFD_delay      = np.r_["0", data.EFD_delay,        data1.EFD_delay]
    data.epoch          = np.r_["0", data.epoch,            data1.epoch]

    bepi_lib.status_add(data, data1)
    """
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
    """
    return data


def efd_spec_shaping(data, cal_mode):
    """
    input:  data
            cal_mode    [Power]     0: background          1: CAL           2: all
    return: data
    """

    # Selection: CAL, N_ch, comp_mode
    if cal_mode<2:
        print("       org:", data.EuEu.shape)

        index = np.where(data.EFD_CAL == cal_mode)
        data.EuEu           = data.EuEu          [index[0]]
        data.EvEv           = data.EvEv          [index[0]]
        #
        data.EFD_Hdump      = data.EFD_Hdump     [index[0]]
        data.EFD_saturation = data.EFD_saturation[index[0]]
        data.EFD_spinrate   = data.EFD_spinrate  [index[0]]
        data.EFD_spinphase  = data.EFD_spinphase [index[0]]
        data.EFD_TI         = data.EFD_TI        [index[0]]
        data.EFD_delay      = data.EFD_delay     [index[0]]
        data.epoch          = data.epoch         [index[0]]
        #
        data.EFD_U_ENA  = data.EFD_U_ENA  [index[0]]
        data.EFD_V_ENA  = data.EFD_V_ENA  [index[0]]
        data.BIAS_U     = data.BIAS_U     [index[0]]
        data.BIAS_V     = data.BIAS_V     [index[0]]
        data.EFD_CAL    = data.EFD_CAL    [index[0]]
        data.PRE_U_ACAL = data.PRE_U_ACAL [index[0]]
        data.AM2P_ACT   = data.AM2P_ACT   [index[0]]
        data.BIAS_LVL_U1= data.BIAS_LVL_U1[index[0]]
        data.BIAS_LVL_U2= data.BIAS_LVL_U2[index[0]]
        data.BIAS_LVL_V1= data.BIAS_LVL_V1[index[0]]
        data.BIAS_LVL_V2= data.BIAS_LVL_V2[index[0]]
        data.BIAS_RAW_U1= data.BIAS_RAW_U1[index[0]]
        data.BIAS_RAW_U2= data.BIAS_RAW_U2[index[0]]
        data.BIAS_RAW_V1= data.BIAS_RAW_V1[index[0]]
        data.BIAS_RAW_V2= data.BIAS_RAW_V2[index[0]]

        if cal_mode == 0:
            print("<only  BG>:", data.EuEu.shape)
        else:
            print("<only CAL>:", data.EuEu.shape)

    data.n_time = data.EuEu.shape[0]
    data.n_freq = data.EuEu.shape[1]

    # NAN: bias value
    index = np.where(data.BIAS_LVL_U1 < -1e30);  data.BIAS_LVL_U1[index[0]] = math.nan
    index = np.where(data.BIAS_LVL_U2 < -1e30);  data.BIAS_LVL_U2[index[0]] = math.nan
    index = np.where(data.BIAS_LVL_V1 < -1e30);  data.BIAS_LVL_V1[index[0]] = math.nan
    index = np.where(data.BIAS_LVL_V2 < -1e30);  data.BIAS_LVL_V2[index[0]] = math.nan

    # NAN: data value
    data.EuEu = np.ravel(data.EuEu);      data.EvEv = np.ravel(data.EvEv)
    index = np.where(data.EuEu < -1e30);  data.EuEu[index[0]] = math.nan
    index = np.where(data.EvEv < -1e30);  data.EvEv[index[0]] = math.nan
    data.EuEu = data.EuEu.reshape(data.n_time, data.n_freq)
    data.EvEv = data.EvEv.reshape(data.n_time, data.n_freq)

    return data


def spec_nan(data, i):
    print("[gap]", data.epoch[i+1] - data.epoch[i], i, data.epoch[i], i+1, data.epoch[i+1])
    data.EuEu[i][:]   = math.nan;       data.EvEv[i][:]   = math.nan
    data.EuEu[i+1][:] = math.nan;       data.EvEv[i+1][:] = math.nan
    return


def spec_peak(spec, n_time0):
    n_sweep1 = 0;  n_sweep2 = n_time0//2;  n_sweep3 = n_time0-1

    peak_u = np.ravel(spec.EuEu);   peak_v = np.ravel(spec.EvEv)
    p1_max, f1_max, p2_max, f2_max = bepi_lib.peak_spec2(peak_u, peak_v, spec.freq, spec.n_freq)
    print("[ All   Peak]",
            "<Eu>", '{:+.2e}'.format(p1_max), '{:4.1f}'.format(f1_max), "Hz", 
          "\t<Ev>", '{:+.2e}'.format(p2_max), '{:4.1f}'.format(f2_max), "Hz")

    peak_u = np.ravel(spec.EuEu[n_sweep1]);   peak_v = np.ravel(spec.EvEv[n_sweep1])
    p1_max, f1_max, p2_max, f2_max = bepi_lib.peak_spec2(peak_u, peak_v, spec.freq, spec.n_freq)
    print("[", '{:5d} peak]'.format(n_sweep1), 
            "<Eu>", '{:+.2e}'.format(p1_max), '{:4.1f}'.format(f1_max), "Hz", 
          "\t<Ev>", '{:+.2e}'.format(p2_max), '{:4.1f}'.format(f2_max), "Hz")

    peak_u = np.ravel(spec.EuEu[n_sweep2]);   peak_v = np.ravel(spec.EvEv[n_sweep2])
    p1_max, f1_max, p2_max, f2_max = bepi_lib.peak_spec2(peak_u, peak_v, spec.freq, spec.n_freq)
    print("[", '{:5d} peak]'.format(n_sweep2), 
            "<Eu>", '{:+.2e}'.format(p1_max), '{:4.1f}'.format(f1_max), "Hz", 
          "\t<Ev>", '{:+.2e}'.format(p2_max), '{:4.1f}'.format(f2_max), "Hz")

    peak_u = np.ravel(spec.EuEu[n_sweep3]);   peak_v = np.ravel(spec.EvEv[n_sweep3])
    p1_max, f1_max, p2_max, f2_max = bepi_lib.peak_spec2(peak_u, peak_v, spec.freq, spec.n_freq)
    print("[", '{:5d} peak]'.format(n_sweep3), 
            "<Eu>", '{:+.2e}'.format(p1_max), '{:4.1f}'.format(f1_max), "Hz", 
          "\t<Ev>", '{:+.2e}'.format(p2_max), '{:4.1f}'.format(f2_max), "Hz")

    return
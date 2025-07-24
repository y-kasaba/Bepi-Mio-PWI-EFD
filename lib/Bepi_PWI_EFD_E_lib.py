"""
    BepiColombo Mio PWI EFD E-field: L1 QL -- 2025/7/23
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
def efd_E_read(cdf, mode_tlm):
    """
    input:  CDF
    return: data
    """
    data = struct()

    if mode_tlm=='l':       # L
        data.Eu         = cdf['Eu_4hz'][...]            # CDF_REAL4 [,8]
        data.Ev         = cdf['Ev_4hz'][...]            # CDF_REAL4 [,8]
    elif mode_tlm=='m':     # M
        data.Eu         = cdf['Eu_8hz'][...]            # CDF_REAL4 [,8]
        data.Ev         = cdf['Ev_8hz'][...]            # CDF_REAL4 [,8]
    else:                   # H
        data.Eu         = cdf['Eu_128hz'][...]          # CDF_REAL4 [,8]
        data.Ev         = cdf['Ev_128hz'][...]          # CDF_REAL4 [,8]
    if mode_tlm!='h':       # L & M
        data.EFD_Eu_ENA = cdf['EFD_Eu_ENA'][...]        # CDF_UINT1 []
        data.EFD_Ev_ENA = cdf['EFD_Ev_ENA'][...]        # CDF_UINT1 []
        data.EFD_Hdump  = cdf['EFD_Hdump'][...]         # CDF_UINT1 []
        data.EFD_sweep  = cdf['EFD_sweep'][...]         # CDF_UINT1 []
        data.PRE_U_PWR  = cdf['PRE_U_PWR'][...]         # CDF_UINT1 []
        data.PRE_V_PWR  = cdf['PRE_V_PWR'][...]         # CDF_UINT1 []
        data.PRE_U_CAL  = cdf['PRE_U_CAL'][...]         # CDF_UINT1 []
        data.PRE_V_CAL  = cdf['PRE_V_CAL'][...]         # CDF_UINT1 []
        data.PRE_U_LOOP = cdf['PRE_U_LOOP'][...]        # CDF_UINT1 []
        data.AM2P_ENA   = cdf['AM2P_ENA'][...]          # CDF_UINT1 []
    #
    data.EFD_saturation = cdf['EFD_saturation'][...]    # CDF_UINT1 []
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
    <M>
    t_offset_8hz
    <H>
    t_offset_32hz
    """
    return data


def efd_E_add(data, data1, mode_tlm):
    """
    input:  data, data1
    return: data
    """
    data.Eu             = np.r_["0", data.Eu,               data1.Eu]
    data.Ev             = np.r_["0", data.Ev,               data1.Ev]
    if mode_tlm!='h':       # L & M
        data.EFD_Eu_ENA = np.r_["0", data.EFD_Eu_ENA,       data1.EFD_Eu_ENA]
        data.EFD_Ev_ENA = np.r_["0", data.EFD_Ev_ENA,       data1.EFD_Ev_ENA]
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


def efd_E_shaping(data, cal_mode, mode_tlm):
    """
    input:  data
            cal_mode    [Power]     0: background          1: CAL           2: all
    return: data
    """

    # Selection: CAL, N_ch, comp_mode
    if cal_mode < 2:
        print("       org:", data.Eu.shape)
        index = np.where(data.PRE_U_CAL == cal_mode)
        data.Eu             = data.Eu            [index[0]]
        data.Ev             = data.Ev            [index[0]]
        #
        data.EFD_Eu_ENA    = data.EFD_Eu_ENA   [index[0]]
        data.EFD_Ev_ENA    = data.EFD_Ev_ENA   [index[0]]
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
            print("<only  BG>:", data.Eu.shape)
        else:
            print("<only CAL>:", data.Eu.shape)

    data.n_time = data.Eu.shape[0]
    data.n_dt = data.Eu.shape[1]

    # NAN: data value
    if mode_tlm != 'l':
        data.Eu = np.ravel(data.Eu);    data.Ev = np.ravel(data.Ev)
    index = np.where(data.Eu < -1e30);  data.Eu[index[0]] = math.nan
    index = np.where(data.Ev < -1e30);  data.Ev[index[0]] = math.nan
    if mode_tlm != 'l':
        data.Eu = data.Eu.reshape(data.n_time, data.n_dt)
        data.Ev = data.Ev.reshape(data.n_time, data.n_dt)
    
    return data


def E_nan(data, i):
    print("[gap]", data.epoch[i+1] - data.epoch[i], i, data.epoch[i], i+1, data.epoch[i+1])
    data.Eu[i][:]   = math.nan;    data.Ev[i][:]   = math.nan
    data.Eu[i+1][:] = math.nan;    data.Ev[i+1][:] = math.nan
    return


def E_peak(data, n_time0):
    n_sweep1 = 0;  n_sweep2 = n_time0//2;  n_sweep3 = n_time0-1

    peak_u = np.ravel(data.Eu);  peak_v = np.ravel(data.Ev)
    p1_max, p1_min, p2_max, p2_min = bepi_lib.peak_data2(peak_u, peak_v)
    print("[ All   Peak]",
            "<Eu>", '{:+.2e}'.format(p1_max), '{:+.2e}'.format(p1_min), 
          "\t<Ev>", '{:+.2e}'.format(p2_max), '{:+.2e}'.format(p2_min) )
    
    peak_u = np.ravel(data.Eu[n_sweep1]);  peak_v = np.ravel(data.Ev[n_sweep1])
    p1_max, p1_min, p2_max, p2_min = bepi_lib.peak_data2(peak_u, peak_v)
    print("[", '{:5d} peak]'.format(n_sweep1), 
            "<Eu>", '{:+.2e}'.format(p1_max), '{:+.2e}'.format(p1_min), 
          "\t<Ev>", '{:+.2e}'.format(p2_max), '{:+.2e}'.format(p2_min) )

    peak_u = np.ravel(data.Eu[n_sweep2]);  peak_v = np.ravel(data.Ev[n_sweep2])
    p1_max, p1_min, p2_max, p2_min = bepi_lib.peak_data2(peak_u, peak_v)
    print("[", '{:5d} peak]'.format(n_sweep2),
            "<Eu>", '{:+.2e}'.format(p1_max), '{:+.2e}'.format(p1_min), 
          "\t<Ev>", '{:+.2e}'.format(p2_max), '{:+.2e}'.format(p2_min) )

    peak_u = np.ravel(data.Eu[n_sweep3]);  peak_v = np.ravel(data.Ev[n_sweep3])
    p1_max, p1_min, p2_max, p2_min = bepi_lib.peak_data2(peak_u, peak_v)
    print("[", '{:5d} peak]'.format(n_sweep3),
            "<Eu>", '{:+.2e}'.format(p1_max), '{:+.2e}'.format(p1_min), 
          "\t<Ev>", '{:+.2e}'.format(p2_max), '{:+.2e}'.format(p2_min) )
    return
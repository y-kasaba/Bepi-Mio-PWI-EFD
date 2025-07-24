"""
    BepiColombo Mio PWI EFD Spec: L1 QL -- 2025/7/22
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

    if mode_tlm=='m':
        data.EuEu       = cdf['EuEu'][...]              # CDF_REAL4 [208, 16]
        data.EvEv       = cdf['EuEu'][...]              # CDF_REAL4 [208, 16]
    elif mode_tlm=='l':
        if mode_L==0:
            data.EuEu   = cdf['EuEu_ave'][...]          # CDF_REAL4 [208, 16]
            data.EvEv   = cdf['EvEv_ave'][...]          # CDF_REAL4 [208, 16]
        else:
            data.EuEu   = cdf['EuEu_peak'][...]         # CDF_REAL4 [208, 16]
            data.EvEv   = cdf['EvEv_peak'][...]         # CDF_REAL4 [208, 16]
    data.spec_freq      = cdf['spec_freq'][...]         # CDF_REAL4 [16]
    data.spec_width     = cdf['spec_width'][...]        # CDF_REAL4 [16]
    #
    data.EFD_Eu_ENA     = cdf['EFD_Eu_ENA'][...]        # CDF_UINT1 [208]
    data.EFD_Ev_ENA     = cdf['EFD_Ev_ENA'][...]        # CDF_UINT1 [208]
    data.EFD_Hdump      = cdf['EFD_Hdump'][...]         # CDF_UINT1 [208]
    data.EFD_saturation = cdf['EFD_saturation'][...]    # CDF_UINT1 [208]
    data.EFD_spinrate   = cdf['EFD_spinrate'][...]      # CDF_REAL4 [208]
    data.EFD_spinphase  = cdf['EFD_spinphase'][...]     # CDF_REAL4 [208]
    data.EFD_sweep      = cdf['EFD_sweep'][...]         # CDF_UINT1 [208]
    data.PRE_U_PWR      = cdf['PRE_U_PWR'][...]         # CDF_UINT1 [208]
    data.PRE_V_PWR      = cdf['PRE_V_PWR'][...]         # CDF_UINT1 [208]
    data.PRE_U_CAL      = cdf['PRE_U_CAL'][...]         # CDF_UINT1 [208]
    data.PRE_V_CAL      = cdf['PRE_V_CAL'][...]         # CDF_UINT1 [208]
    data.PRE_U_LOOP     = cdf['PRE_U_LOOP'][...]        # CDF_UINT1 [208]
    data.AM2P_ENA       = cdf['AM2P_ENA'][...]          # CDF_UINT1 [208]
    #
    data.epoch          = cdf['epoch'][...]             # CDF_TIME_TT2000 [208]
    data.EFD_TI         = cdf['EFD_TI'][...]            # CDF_UINT4 [208]

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
    data.EFD_Eu_ENA     = np.r_["0", data.EFD_Eu_ENA,       data1.EFD_Eu_ENA]
    data.EFD_Ev_ENA     = np.r_["0", data.EFD_Ev_ENA,       data1.EFD_Ev_ENA]
    data.EFD_Hdump      = np.r_["0", data.EFD_Hdump,        data1.EFD_Hdump]
    data.EFD_saturation = np.r_["0", data.EFD_saturation,   data1.EFD_saturation]
    data.EFD_spinrate   = np.r_["0", data.EFD_spinrate,     data1.EFD_spinrate]
    data.EFD_spinphase  = np.r_["0", data.EFD_spinphase,    data1.EFD_spinphase]
    data.EFD_sweep      = np.r_["0", data.EFD_sweep,        data1.EFD_sweep]
    data.PRE_U_PWR      = np.r_["0", data.PRE_U_PWR,        data1.PRE_U_PWR]
    data.PRE_V_PWR      = np.r_["0", data.PRE_V_PWR,        data1.PRE_V_PWR]
    data.PRE_U_CAL      = np.r_["0", data.PRE_U_CAL,        data1.PRE_U_CAL]
    data.PRE_V_CAL      = np.r_["0", data.PRE_V_CAL,        data1.PRE_V_CAL]
    data.PRE_U_LOOP     = np.r_["0", data.PRE_U_LOOP,       data1.PRE_U_LOOP]
    data.AM2P_ENA       = np.r_["0", data.AM2P_ENA,         data1.AM2P_ENA]
    #
    data.epoch          = np.r_["0", data.epoch,            data1.epoch]
    data.EFD_TI          = np.r_["0", data.EFD_TI,            data1.EFD_TI]

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

        index = np.where(data.PRE_U_CAL == cal_mode)

        data.EuEu           = data.EuEu          [index[0]]
        data.EvEv           = data.EvEv          [index[0]]
        data.spec_freq      = data.spec_freq     [index[0]]
        data.spec_width     = data.spec_width    [index[0]]
        #
        data.EFD_Eu_ENA     = data.EFD_Eu_ENA    [index[0]]
        data.EFD_Ev_ENA     = data.EFD_Ev_ENA    [index[0]]
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
        
        if cal_mode == 0:
            print("<only  BG>:", data.EuEu.shape)
        else:
            print("<only CAL>:", data.EuEu.shape)

    data.n_time = data.EuEu.shape[0]
    data.n_freq = data.EuEu.shape[1]

    # NAN: data value
    data.EuEu = np.ravel(data.EuEu);      data.EvEv = np.ravel(data.EvEv)
    index = np.where(data.EuEu < -1e30);  data.EuEu[index[0]] = math.nan
    index = np.where(data.EvEv < -1e30);  data.EvEv[index[0]] = math.nan
    data.EuEu = data.EuEu.reshape(data.n_time, data.n_freq)
    data.EvEv = data.EvEv.reshape(data.n_time, data.n_freq)

    return data


def spec_nan(data, i):
    print("[gap]", data.epoch[i+1] - data.epoch[i], i, data.epoch[i], i+1, data.epoch[i+1])
    data.EuEu[i][:]   = math.nan;  data.EvEv[i][:]   = math.nan
    data.EuEu[i+1][:] = math.nan;  data.EvEv[i+1][:] = math.nan
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
"""
    BepiColombo Mio PWI EFD Spec: L1 QL -- 2025/12/12
"""
import glob
import math
import os
import sys
import numpy as np

sys.path.append('./lib/')
import Bepi_PWI_EFD_lib  as bepi_lib

class struct:
    pass

def datalist(date_str, mode_str, mode_cdf):
    """
    input:  date_str        yyyymmdd: group read    others: file list
            mode_str        l / m / h
            cdf_mode        0:cdf   1:cdf_test
    return: data_dir
            data_list
    """
    yr_format = date_str[0:2]
    yr_str    = date_str[0:4]
    
    # *** Group read
    if yr_format=='20':
        if   mode_cdf==1:  data_dir = '/Users/D-Univ/data/data-Mio/cdf_test/EFD/L1/'       + yr_str + '/'
        elif mode_cdf==11: data_dir = '/Users/D-Univ/data/data-Mio/cdf_test/EFD/L1_prime/' + yr_str + '/'
        elif mode_cdf==10: data_dir = '/Users/D-Univ/data/data-Mio/cdf/EFD/L1_prime/'      + yr_str + '/'
        else:              data_dir = '/Users/D-Univ/data/data-Mio/cdf/EFD/L1/'            + yr_str + '/'
        
        data_name = 'bc_mmo_pwi-efd_l*_' + mode_str + '-spec_' + date_str + '*.cdf'
        if mode_str=='h':
            data_name = 'bc_mmo_pwi-efd_l*_' + mode_str + '-e_' + date_str + '*.cdf'
        cdf_file  = data_dir + data_name
        print(cdf_file)

        data_list = glob.glob(cdf_file)
        num_list = len(data_list)
        data_list.sort()
        for i in range(num_list):
            data_list[i] = os.path.split(data_list[i])[1]

    print(data_dir)
    print(data_list)
    return data_dir, data_list


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
        data.EuEu           = cdf['Ewpt_power'][...]          # CDF_REAL4 [208, 16]
        data.EvEv           = cdf['Emef_power'][...]          # CDF_REAL4 [208, 16]
        data.spec_freq      = cdf['spec_freq_50hz'][...]    # CDF_REAL4 [16]
    else:
        if mode_tlm=='l':
            if mode_L==0:
                data.EuEu   = cdf['Ewpt_power_ave'][...]          # CDF_REAL4 [208, 16]
                data.EvEv   = cdf['Emef_power_ave'][...]          # CDF_REAL4 [208, 16]
            else:
                data.EuEu   = cdf['Ewpt_power_peak'][...]         # CDF_REAL4 [208, 16]
                data.EvEv   = cdf['Emef_power_peak'][...]         # CDF_REAL4 [208, 16]
        else:
            data.EuEu       = cdf['Ewpt_power'][...]              # CDF_REAL4 [208, 16]
            data.EvEv       = cdf['Emef_power'][...]              # CDF_REAL4 [208, 16]
        data.spec_freq      = cdf['spec_freq'][...]         # CDF_REAL4 [16]
        data.spec_width     = cdf['spec_width'][...]        # CDF_REAL4 [16]

    # from HK
    data.EFD_saturation = cdf['EFD_saturation'][...]    # CDF_UINT1 [208]      >30000, <30000
    if mode_tlm!='h':
        data.EFD_Hdump      = cdf['EFD_HDUMP'][...]         # CDF_UINT1 []      Hdump=1
        data.EFD_delay      = cdf['EFD_DELAY'][...]         # CDF_REAL4 []
    data.EFD_spinrate   = cdf['spinperiod'][...]          # CDF_REAL4 [208]
    data.EFD_spinphase  = cdf['spinphase'][...]         # CDF_REAL4 [208]
    data.EFD_TI         = cdf['EFD_TI'][...]            # CDF_UINT4 []
    data.epoch          = cdf['epoch'][...]             # CDF_TIME_TT2000 [208]

    bepi_lib.status_read(cdf, data)
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
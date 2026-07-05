"""
    BepiColombo Mio PWI EFD E-field: L1 QL -- 2026/7/5
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
def efd_E_read(cdf, mode_tlm):
    """
    input:  CDF
    return: data
    """
    data = struct()

    if mode_tlm=='l':       # L
        data.Eu         = cdf['Eu_4hz'][...]                        # CDF_REAL4 [,4]
        data.Ev         = cdf['Ev_4hz'][...]                        # CDF_REAL4 [,4]
        data.spinphase2 = cdf['spinphase_4hz'][...]                 # CDF_REAL4 [,4]
        data.t_offset   = cdf['t_offset_4hz'][...]                  # CDF_REAL4 [4]
    elif mode_tlm=='m':     # M
        data.Eu         = cdf['Eu_8hz'][...]                        # CDF_REAL4 [,8]
        data.Ev         = cdf['Ev_8hz'][...]                        # CDF_REAL4 [,8]
        data.spinphase2 = cdf['spinphase_8hz'][...]                 # CDF_REAL4 [,8]   
        data.t_offset   = cdf['t_offset_8hz'][...]                  # CDF_REAL4 [8]
    else:                   # H
        data.Eu         = cdf['Eu_128hz'][...]                      # CDF_REAL4 [,128]
        data.Ev         = cdf['Ev_128hz'][...]                      # CDF_REAL4 [,128]
        data.spinphase2 = cdf['spinphase_128hz'][...]               # CDF_REAL4 [,128]
        data.t_offset   = cdf['t_offset_128hz'][...]                # CDF_REAL4 [128]
        data.EFD_TI_INDEX    = cdf['EFD_TI_INDEX_128hz'][...]       # CDF_UINT4 [,128]
        data.EFD_EWO_COUNTER = cdf['EFD_EWO_COUNTER_128hz'][...]    # CDF_UINT2 [,128]
        data.EFD_EWO_SIZE    = cdf['EFD_EWO_SIZE_128hz'][...]       # CDF_UINT2 [,128]
        data.EuEu       = cdf['Eu_power'][...]                      # CDF_REAL4 [,50]
        data.EvEv       = cdf['Ev_power'][...]                      # CDF_REAL4 [,50]
        data.EuEv_re    = cdf['EuEv_cross_re'][...]                 # CDF_REAL4 [,50]
        data.EuEv_im    = cdf['EuEv_cross_im'][...]                 # CDF_REAL4 [,50]
        data.spec_freq  = cdf['spec_freq_50hz'][...]                # CDF_REAL4 [50]
    if mode_tlm!='h':       # L & M: from HK
        data.EFD_Hdump  = cdf['EFD_HDUMP'][...]                     # CDF_UINT1 []      Hdump=1
        data.EFD_delay  = cdf['EFD_DELAY'][...]                     # CDF_REAL4 []
    data.EFD_saturation = cdf['EFD_saturation'][...]                # CDF_UINT1 []      >30000, <30000
    data.EFD_spinrate   = cdf['spinperiod'][...]                    # CDF_REAL4 []
    data.EFD_spinphase  = cdf['spinphase'][...]                     # CDF_REAL4 []
    data.EFD_TI         = cdf['EFD_TI'][...]                        # CDF_UINT4 []
    data.epoch          = cdf['epoch'][...]                         # CDF_TIME_TT2000 []

    bepi_lib.status_read(cdf, data)
    return data


def efd_E_add(data, data1, mode_tlm):
    """
    input:  data, data1
    return: data
    """
    data.Eu             = np.r_["0", data.Eu,               data1.Eu]
    data.Ev             = np.r_["0", data.Ev,               data1.Ev]
    data.spinphase2     = np.r_["0", data.spinphase2,       data1.spinphase2]
    if mode_tlm!='h':       # L & M
        data.EFD_Hdump  = np.r_["0", data.EFD_Hdump,        data1.EFD_Hdump]
        data.EFD_delay  = np.r_["0", data.EFD_delay,        data1.EFD_delay]
    else:
        data.EuEu           = np.r_["0", data.EuEu,             data1.EuEu]
        data.EvEv           = np.r_["0", data.EvEv,             data1.EvEv]
        data.EuEv_re        = np.r_["0", data.EuEv_re,          data1.EuEv_re]
        data.EuEv_im        = np.r_["0", data.EuEv_im,          data1.EuEv_im]
        data.EFD_TI_INDEX   = np.r_["0", data.EFD_TI_INDEX,     data1.EFD_TI_INDEX]
        data.EFD_EWO_COUNTER= np.r_["0", data.EFD_EWO_COUNTER,  data1.EFD_EWO_COUNTER]
        data.EFD_SIZE       = np.r_["0", data.EFD_SIZE,         data1.EFD_SIZE]
    data.EFD_saturation = np.r_["0", data.EFD_saturation,   data1.EFD_saturation]
    data.EFD_spinrate   = np.r_["0", data.EFD_spinrate,     data1.EFD_spinrate]
    data.EFD_spinphase  = np.r_["0", data.EFD_spinphase,    data1.EFD_spinphase]
    data.EFD_TI         = np.r_["0", data.EFD_TI,           data1.EFD_TI]
    data.epoch          = np.r_["0", data.epoch,            data1.epoch]
    #
    bepi_lib.status_add(data, data1)
    return data


def efd_E_shaping(data, cal_mode, mode_tlm, mode_ant):
    """
    input:  data
            cal_mode    [Power]     0: background          1: CAL           2: all
            mode_ant    # 0:both    1:U(WPT)    2:V(MEF)
    return: data
    """

    # Selection: CAL, N_ch, comp_mode
    if cal_mode < 2:
        print("       org:", data.Eu.shape)
        index = np.where(data.EFD_CAL == cal_mode)
        data.Eu             = data.Eu           [index[0]]
        data.Ev             = data.Ev           [index[0]]
        data.spinphase2     = data.spinphase2   [index[0]]
        #
        if mode_tlm!='h':       # L & M
            data.EFD_Hdump  = data.EFD_Hdump    [index[0]]
            data.EFD_delay  = data.EFD_delay    [index[0]]
        else:
            data.EuEu           = data.EuEu     [index[0]]
            data.EvEv           = data.EvEv     [index[0]]
            data.EuEv_re        = data.EuEv_re  [index[0]]
            data.EuEv_im        = data.EuEv_im  [index[0]]
            data.EFD_TI_INDEX   = data.EFD_TI_INDEX   [index[0]]
            data.EFD_EWO_COUNTER= data.EFD_EWO_COUNTER[index[0]]
            data.EFD_SIZE       = data.EFD_SIZE       [index[0]]
        data.EFD_saturation = data.EFD_saturation[index[0]]
        data.EFD_spinrate   = data.EFD_spinrate [index[0]]
        data.EFD_spinphase  = data.EFD_spinphase[index[0]]
        data.EFD_TI         = data.EFD_TI       [index[0]]
        data.epoch          = data.epoch        [index[0]]
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
            print("<only  BG>:", data.Eu.shape)
        else:
            print("<only CAL>:", data.Eu.shape)

    data.n_time = data.Eu.shape[0]
    data.n_dt   = data.Eu.shape[1]

    # NAN: HK calue
    index = np.where(data.BIAS_LVL_U1 < -1e30);  data.BIAS_LVL_U1[index[0]] = math.nan
    index = np.where(data.BIAS_LVL_U2 < -1e30);  data.BIAS_LVL_U2[index[0]] = math.nan
    index = np.where(data.BIAS_LVL_V1 < -1e30);  data.BIAS_LVL_V1[index[0]] = math.nan
    index = np.where(data.BIAS_LVL_V2 < -1e30);  data.BIAS_LVL_V2[index[0]] = math.nan
    index = np.where(data.spinphase2  < -1e30);  data.spinphase2 [index[0]] = math.nan

    # NAN: data value
    data.Eu = np.ravel(data.Eu);        data.Ev = np.ravel(data.Ev)
    index = np.where(data.Eu < -1e30);  data.Eu[index[0]] = math.nan
    index = np.where(data.Ev < -1e30);  data.Ev[index[0]] = math.nan
    if mode_ant == 1:
        data.Ev[:] = math.nan
    if mode_ant == 2:
        data.Eu[:] = math.nan
    data.Eu = data.Eu.reshape(data.n_time, data.n_dt)
    data.Ev = data.Ev.reshape(data.n_time, data.n_dt)
    return data


def E_nan(data, i):
    print("[gap]", data.epoch[i+1] - data.epoch[i], i, data.epoch[i], i+1, data.epoch[i+1])
    data.Eu[i][:]      = math.nan;  data.Ev[i][:]   = math.nan;  data.spinphase2[i][:] = math.nan;
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
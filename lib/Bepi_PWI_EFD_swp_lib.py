"""
    BepiColombo Mio PWI EFD Sweep: L1 QL -- 2026/7/5
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

def datalist(date_str, mode_cdf, mode_ant):
    """
    input:  date_str        yyyymmdd: group read    others: file list
            mode_cdf        0:cdf       1:cdf_test
            mode_ant        # 1:U(WPT)  2:V(MEF)
    return: data_dir
            data_list
    """
    yr_format = date_str[0:2]
    yr_str    = date_str[0:4]
    if mode_ant==1: ant_str = 'wpt'
    else:           ant_str = 'mef'

    # *** Group read
    if yr_format=='20':
        if   mode_cdf==1:  data_dir = '/Users/D-Univ/data/data-Mio/cdf_test/EFD/L1/'       + yr_str + '/'
        elif mode_cdf==11: data_dir = '/Users/D-Univ/data/data-Mio/cdf_test/EFD/L1_prime/' + yr_str + '/'
        elif mode_cdf==10: data_dir = '/Users/D-Univ/data/data-Mio/cdf/EFD/L1_prime/'      + yr_str + '/'
        else:              data_dir = '/Users/D-Univ/data/data-Mio/cdf/EFD/L1/'            + yr_str + '/'

        data_name = 'bc_mmo_pwi-efd_l*_swp-' + ant_str + '_' + date_str + '*.cdf'
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
def efd_swp_read(cdf, mode_ant):
    """
    input:  CDF
    return: data
    """
    data = struct()

    if mode_ant==1:
        data.Vu1           = cdf['Vu1_sweep'][...]          # CDF_REAL4 [,]
        data.Vu2           = cdf['Vu2_sweep'][...]          # CDF_REAL4 [,]
        data.WPT_Sweep_Tbl = cdf['EFD_U_SWP_TBL'][...]      # CDF_UINT4 []
    else:
        data.Vv1           = cdf['Vv1_sweep'][...]          # CDF_REAL4 [,]
        data.Vv2           = cdf['Vv2_sweep'][...]          # CDF_REAL4 [,]
    data.t_offset       = cdf['t_offset_1024hz'][...]
    data.sweep_ant      = cdf['sweep_ant'][...]             # CDF_UNIT1 []
    #
    data.EFD_saturation = cdf['EFD_saturation'][...]        # CDF_UINT1 []      >30000, <30000
    data.EFD_ti_index   = cdf['EFD_TI_INDEX'][...]          # CDF_UINT4 []
    data.EFD_ewo_counter= cdf['EFD_EWO_COUNTER'][...]       # CDF_UINT2 []
    data.EFD_TI         = cdf['EFD_TI'][...]                # CDF_UINT4 []
    data.epoch          = cdf['epoch'][...]                 # CDF_TIME_TT2000 [208]

    bepi_lib.status_read(cdf, data)
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

    bepi_lib.status_add(data, data1)
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
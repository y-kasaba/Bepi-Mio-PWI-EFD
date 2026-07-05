"""
    Susanoo Solar Wind lib -- 2026/3/30
"""
import datetime
import numpy as np
import os
from spacepy import pycdf

# ---------------------------------------------------------
# Susanoo Solar Wind
# ---------------------------------------------------------
def name_solarwind_data(YYYY, MM, DD, str_object):
    # CDF version --- Please check and correct if needed
    s_ver = 'v01.01'        

    s_CDF_dir  = str_object + '/' + YYYY + '/' + MM + '/'
    s_CDF_file = 'susanoo_sw_' + str_object + '_5m_' + YYYY + MM + DD + '_' + s_ver + '.cdf'
    return  s_CDF_dir, s_CDF_file


def read(Epoch0_min, Epoch0_max, data_dir, str_object, mode_download):
    class struct:
        pass
    solarwind = struct()
    solarwind.num = 0

    Epoch_min = datetime.datetime.strptime(Epoch0_min[0:10], "%Y-%m-%d")     # Start epoch
    Epoch_max = datetime.datetime.strptime(Epoch0_max[0:10], "%Y-%m-%d")     # End   epoch
    Epoch_len = Epoch_max - Epoch_min;   print('[CDF]', Epoch_len.days+1, 'days      (', Epoch0_min[0:10], '-', Epoch0_max[0:10],  ')\n')
    Epoch     = Epoch_min

    for i in range (Epoch_len.days+1):
        str_Epoch = Epoch.strftime('%Y-%m-%d ')
        solarwind1 = read_solarwind(str_Epoch, data_dir, str_object, mode_download)
        if solarwind1.num > 0:
            if solarwind.num == 0:  
                solarwind = solarwind1
            else:
                solarwind = solarwind_add(solarwind, solarwind1)
        Epoch = Epoch + datetime.timedelta(days=1)
        print(i+1, str_Epoch, solarwind.num)

    print(" [density] ", solarwind.dens[0],  "\t\t\t\t", solarwind.dens[-1],  "\t\t\t\t\t\t", solarwind.dens.shape)
    print("[pressure] ", solarwind.pre[0],   "\t\t\t\t", solarwind.pre[-1],   "\t\t\t\t\t\t", solarwind.pre.shape)
    print("[velocity] ", solarwind.swvv[0],  "\t",       solarwind.swvv[-1],  "\t",           solarwind.swvv.shape)
    print("       [B] ", solarwind.imfb[0],  "\t",       solarwind.imfb[-1],  "\t\t\t",       solarwind.imfb.shape)
    # print("   [epoch] ", solarwind.epoch[0], "\t\t",     solarwind.epoch[-1], "\t\t\t\t",     solarwind.epoch.shape)
    return  solarwind


def read_solarwind(Epoch, data_dir, str_object, mode_download):
    class struct:
        pass

    solarwind1     = struct()
    solarwind1.num = 0
    Epoch_YYYY = Epoch[0:4];  Epoch_MM = Epoch[5:7];  Epoch_DD = Epoch[8:10]

    ##################################################################################################################################################
    # (1) download CDF using wget 
    #       https://chs.isee.nagoya-u.ac.jp/data/chs/simulation/susanoo/data/cdf/
    #       (object)/(YYYY)/(MM)/
    #       susanoo_sw_(object)_5m_(YYYY)(MM)(DD)_v01.01.cdf        << Please check & correct !
    ##################################################################################################################################################
    s_CDF_dir, s_CDF_file = name_solarwind_data(Epoch_YYYY, Epoch_MM, Epoch_DD, str_object)
    d_CDF_dir  = data_dir  + s_CDF_dir
    d_CDF_file = d_CDF_dir + s_CDF_file
    s_CDF_file = 'https://chs.isee.nagoya-u.ac.jp/data/chs/simulation/susanoo/data/cdf/' + s_CDF_dir + s_CDF_file
    if mode_download != 0:
        print('CDF file (source):', s_CDF_file)
        print('CDF directory    :', d_CDF_dir)
        os.system('wget -N -P ' + d_CDF_dir + ' ' + s_CDF_file)
        print('CDF file (local) :', d_CDF_file)

    ##################################################################################################################################################
    # (2) read CDF
    ##################################################################################################################################################
    try:
        with open(d_CDF_file, 'r') as f:
            f.close()
    except FileNotFoundError:
        print("***ERROR*** Susanoo file - not found:", d_CDF_file)
        return solarwind1

    # Decode Susanoo data
    with open(d_CDF_file, 'r') as f:
        cdf = pycdf.CDF(d_CDF_file)
        solarwind1.dens  = cdf['dens'][...];            # print("dens:", solarwind1.dens)   # dens:  Density  (1/cc)        CDF_FLOAT [288]
        solarwind1.pre   = cdf['pre'][...];             # print("pre:",  solarwind1.pre)    # pre:   Pressure (dyn/cm2)     CDF_FLOAT [288]
        solarwind1.swvv  = cdf['swvv'][...];            # print("swvv:", solarwind1.swvv)   # swvv:  Velocity X/Y/Z (km/s)  CDF_FLOAT [288, 3]
        solarwind1.imfb  = cdf['imfb'][...];            # print("imfb:", solarwind1.imfb)   # imfb:  B X/Y/Z (nT)           CDF_FLOAT [288, 3]
        solarwind1.epoch = cdf['epoch'][...];           # print("epoch:", solarwind1.epoch) # epoch:                        CDF_TIME_TT2000 [288]
        solarwind1.num   = solarwind1.epoch.shape[0];   # print("num:", solarwind1.num)     # data number per day (5-min interval)
    return solarwind1


def solarwind_add(solarwind, solarwind1):
    solarwind.dens  = np.r_["0", solarwind.dens,  solarwind1.dens]
    solarwind.pre   = np.r_["0", solarwind.pre,   solarwind1.pre]
    solarwind.swvv  = np.r_["0", solarwind.swvv,  solarwind1.swvv]
    solarwind.imfb  = np.r_["0", solarwind.imfb,  solarwind1.imfb]
    solarwind.epoch = np.r_["0", solarwind.epoch, solarwind1.epoch]
    solarwind.num   = solarwind.num + solarwind1.num
    return solarwind
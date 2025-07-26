"""
    BepiColombo Mio PWI EFD Pot: L1 data list -- 2025/7/26
"""
import glob
import os

def datalist(date_str, mode_str, cdf_mode):
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
        if cdf_mode==0:  data_dir  = '/Users/user/D-Univ/data/data-Mio/cdf/EFD/L1/'      + yr_str + '/'
        else:            data_dir  = '/Users/user/D-Univ/data/data-Mio/cdf_test/EFD/L1/' + yr_str + '/'

        data_name = 'bc_mmo_pwi-efd_l1_' + mode_str + '-pot_' + date_str + '*.cdf'
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
"""
    BepiColombo Mio PWI EFD E-field: L1 data list -- 2025/8/11
"""
import glob
import os

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
        if   mode_cdf==1:  data_dir = '/Users/user/D-Univ/data/data-Mio/cdf_test/EFD/L1/'       + yr_str + '/'
        elif mode_cdf==11: data_dir = '/Users/user/D-Univ/data/data-Mio/cdf_test/EFD/L1_prime/' + yr_str + '/'
        elif mode_cdf==10: data_dir = '/Users/user/D-Univ/data/data-Mio/cdf/EFD/L1_prime/'      + yr_str + '/'
        else:              data_dir = '/Users/user/D-Univ/data/data-Mio/cdf/EFD/L1/'            + yr_str + '/'

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
"""
    BepiColombo Mio PWI EFD Sweep: L1 data list -- 2025/7/24
"""
import glob
import os

def datalist(date_str, cdf_mode):
    """
    input:  date_str        yyyymmdd: group read    others: file list
        cdf_mode        0:cdf   1:cdf_test
    return: data_dir
        data_list
    """
    yr_format = date_str[0:2]
    yr_str    = date_str[0:4]
    
    # *** Group read
    if yr_format=='20':
        if cdf_mode==0: data_dir  = '/Users/user/D-Univ/data/data-Mio/cdf/EFD/L1/'      + yr_str + '/'
        else:           data_dir  = '/Users/user/D-Univ/data/data-Mio/cdf_test/EFD/L1/' + yr_str + '/'

        data_name = 'bc_mmo_pwi-efd_l1_swp_' + date_str + '*.cdf'
        cdf_file  = data_dir + data_name
        print(cdf_file)

        data_list = glob.glob(cdf_file)
        num_list = len(data_list)
        data_list.sort()
        for i in range(num_list):
            data_list[i] = os.path.split(data_list[i])[1]
    else:
        # **** TEST ****
        data_dir  = '/Users/user/D-Univ/data/data-Mio/cdf/EFD/L1/2025/'
        data_list = [
            'L1/2025/bc_mmo_pwi-efd_l1_swp_20250605_r01-v00-00.cdf',      # 20250605-06:  Initial Check DryRun #1
            'L1/2025/bc_mmo_pwi-efd_l1_swp_20250606_r01-v00-00.cdf',
            'L1/2025/bc_mmo_pwi-efd_l1_swp_20250625_r01-v00-00.cdf',      # 20250625:     Initial Check DryRun #2
        ]
        """
        """

        # **** FLIGHT ****
        """
        data_dir  = '/Users/user/D-Univ/data/data-Mio/cdf/EFD/L1/2025/'
        data_list = [
            'bc_mmo_pwi-efd_l1_swp_20250410_r01-v00-00.cdf',    # 20250410  Check        
        ]
        data_dir  = '/Users/user/D-Univ/data/data-Mio/cdf/EFD/L1/2024/'
        data_list = [
            'bc_mmo_pwi-efd_l1_swp_20240409_r01-v00-00.cdf',    # 20240409  Check
        ]
        data_dir  = '/Users/user/D-Univ/data/data-Mio/cdf/EFD/L1/2023/'
        data_list = [
            'bc_mmo_pwi-efd_l1_swp_20230522_r01-v00-00.cdf',    # 20230522  Check
            'bc_mmo_pwi-efd_l1_swp_20231026_r01-v00-00.cdf',    # 20231026  Check
            'bc_mmo_pwi-efd_l1_swp_20231106_r01-v00-00.cdf',    # 20231106  Check
        ]
        data_dir  = '/Users/user/D-Univ/data/data-Mio/cdf/EFD/L1/2022/'
        data_list = [
            'bc_mmo_pwi-efd_l1_swp_20220311_r01-v00-00.cdf',    # 20220311  Check
            'bc_mmo_pwi-efd_l1_swp_20220517_r01-v00-00.cdf',    # 20220517  Check
            'bc_mmo_pwi-efd_l1_swp_20221107_r01-v00-00.cdf',    # 20221107  Check
        ]
        data_dir  = '/Users/user/D-Univ/data/data-Mio/cdf/EFD/L1/2021/'
        data_list = [
            'bc_mmo_pwi-efd_l1_swp_20210617_r01-v00-00.cdf',    # 20210617  Check
            'bc_mmo_pwi-efd_l1_swp_20211124_r01-v00-00.cdf',    # 20211124  Check
        ]
        data_dir  = '/Users/user/D-Univ/data/data-Mio/cdf/EFD/L1/2020/'
        data_list = [
            'bc_mmo_pwi-efd_l1_swp_20200304_r01-v00-00.cdf',    # 20200304  Check
            'bc_mmo_pwi-efd_l1_swp_20201217_r01-v00-00.cdf',    # 20201217  Check
        ]
        data_dir  = '/Users/user/D-Univ/data/data-Mio/cdf/EFD/L1/2019/'
        data_list = [
            'bc_mmo_pwi-efd_l1_swp_20190630_r01-v00-00.cdf',    # 20190630-0701 
            'bc_mmo_pwi-efd_l1_swp_20190802_r01-v00-00.cdf',    # 20190802  Check
            'bc_mmo_pwi-efd_l1_swp_20190805_r01-v00-00.cdf',    # 20190805-7:   WPT latch release
            'bc_mmo_pwi-efd_l1_swp_20190807_r01-v00-00.cdf',
            'bc_mmo_pwi-efd_l1_swp_20191210_r01-v00-00.cdf',    # 20192110  Check
        ]
        """
    print(data_dir)
    print(data_list)
    return data_dir, data_list
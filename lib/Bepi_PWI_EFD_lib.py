"""
    BepiColombo Mio PWI EFD common lib -- 2025/7/23
"""
import numpy as np
import math


def peak_spec2(data1, data2, freq, n_freq):
    p1_data = np.ravel(data1)
    if (~np.all(np.isnan(p1_data))):    
        p1_max = np.nanmax(p1_data);     f1_max = freq[np.nanargmax(p1_data) % n_freq]
    else:
        p1_max = math.nan;               f1_max = math.nan

    p2_data = np.ravel(data2)
    if (~np.all(np.isnan(p2_data))):
        p2_max = np.nanmax(p2_data);     f2_max = freq[np.nanargmax(p2_data) % n_freq]
    else:
        p2_max = math.nan;               f2_max = math.nan

    return  p1_max, f1_max, p2_max, f2_max


def peak_data2(data1, data2):
    p1_data = np.ravel(data1)
    if (~np.all(np.isnan(p1_data))):
        p1_max = np.nanmax(p1_data);     p1_min = np.nanmin(p1_data)
    else:
        p1_max = math.nan;               p1_min = math.nan

    p2_data = np.ravel(data2)
    if (~np.all(np.isnan(p2_data))):
        p2_max = np.nanmax(p2_data);     p2_min = np.nanmin(p2_data)
    else:
        p2_max = math.nan;               p2_min = math.nan

    return  p1_max, p1_min, p2_max, p2_min


def peak_data4(data1, data2, data3, data4):
    p1_data = np.ravel(data1)
    if (~np.all(np.isnan(p1_data))):
        p1_max = np.nanmax(p1_data);     p1_min = np.nanmin(p1_data)
    else:
        p1_max = math.nan;               p1_min = math.nan

    p2_data = np.ravel(data2)
    if (~np.all(np.isnan(p2_data))):
        p2_max = np.nanmax(p2_data);     p2_min = np.nanmin(p2_data)
    else:
        p2_max = math.nan;               p2_min = math.nan

    p3_data = np.ravel(data3)
    if (~np.all(np.isnan(p3_data))):
        p3_max = np.nanmax(p3_data);     p3_min = np.nanmin(p3_data)
    else:
        p3_max = math.nan;               p3_min = math.nan

    p4_data = np.ravel(data4)
    if (~np.all(np.isnan(p4_data))):
        p4_max = np.nanmax(p4_data);     p4_min = np.nanmin(p4_data)
    else:
        p4_max = math.nan;               p4_min = math.nan

    return  p1_max, p1_min, p2_max, p2_min, p3_max, p3_min, p4_max, p4_min
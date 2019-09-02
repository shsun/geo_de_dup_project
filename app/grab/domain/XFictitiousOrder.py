#!/usr/bin/python
# -*- coding: UTF-8 -*-

class XFictitiousOrder(object):
    """
    虚拟车辆订单信息表（需要被抢的单子）
    需要按订单仓库形式提供，省市区，目的地，取货仓库，大品种，小品种，重量，类似于智能分货的输出，（取货地个数，卸货地个数）
    """

    order = -1
    address_no = -1
    # 省,市,区/县,乡镇
    province_name = None
    citey_name = None
    district_name = None
    town_name = None

    # 详细地址（拼接省市区）
    full_name = None

    # 详细地址(PROD地址)
    full_name_prod = None

    # 经度, 纬度
    longitude = -1
    latitude = -1

    # 标准地址
    std_addr = None

    # 标准地址是否新地址, 1 dicate yes, 0 indicate no, otherwise unknown.
    is_new_std_addr = None

    def __init__(self, p_line=None, p_date=None):
        pass

    def toString(self):
        return ''

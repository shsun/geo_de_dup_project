#!/usr/bin/python
# -*- coding: UTF-8 -*-

class LALPctStrategy(object):
    """
    Latitude and Longitude
    """

    def __init__(self):
        pass

    def compare(self, p_address_dict_a=None, p_address_dict_b=None):
        """我第一个想法是简单的，首先现有地址几乎都有经纬度，我想通过对经纬度的比较，相差百分之一或更小以内的视为同一地址，否则视为两个地址，将地址重复的去掉。
        生成出地址库。当新地址收录时，通过正向地址编码到高德或百度得到经纬度再与已有经纬度进行匹配比较
        :param p_address_dict_a:
        :param p_address_dict_b:
        :return:
        """
        try:
            delta_longitude = abs(p_address_dict_a['经度'] - p_address_dict_b['经度'])
            delta_latitude = abs(p_address_dict_a['纬度'] - p_address_dict_b['纬度'])

            pct_longitude = delta_longitude / p_address_dict_a['经度']
            pct_latitude = delta_latitude / p_address_dict_a['纬度']

            rst = pct_longitude <= 0.01 and pct_latitude <= 0.01
        except Exception as e:
            pct_longitude = 1
            pct_latitude = 1
            rst = False
        return rst

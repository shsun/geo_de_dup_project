#!/usr/bin/python
# -*- coding: UTF-8 -*-

import math
from math import pi, cos, sin


class GEODistanceStrategy(object):
    """
    计算两个经纬度之间的距离(python算法)
    https://www.cnblogs.com/lgh344902118/p/7490795.html
    """
    EARTH_REDIUS = 6378.137

    def __init__(self):
        pass

    def rad(self, d):
        try:
            r = float(d) * float(pi) / float(180.0)
        except Exception as e:
            r = 1
        return r

    def getDistance(self, lat1, lng1, lat2, lng2):
        radLat1 = self.rad(lat1)
        radLat2 = self.rad(lat2)
        a = radLat1 - radLat2
        b = self.rad(lng1) - self.rad(lng2)
        s = 2 * math.asin(math.sqrt(math.pow(sin(a / 2), 2) + cos(radLat1) * cos(radLat2) * math.pow(sin(b / 2), 2)))
        s = s * GEODistanceStrategy.EARTH_REDIUS
        return s

    def cal_physical_distance(self, p_address_dict_A=None, p_address_dict_B=None):
        """
        计算出来的结果单位为米

        :param p_address_dict_A:
        :param p_address_dict_B:
        :return:
        """
        s = self.getDistance(p_address_dict_A['纬度'], p_address_dict_A['经度'], p_address_dict_B['纬度'], p_address_dict_B['经度'])
        return s * 1000

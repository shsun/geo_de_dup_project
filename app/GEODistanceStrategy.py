#!/usr/bin/python
# -*- coding: UTF-8 -*-

import math
from math import pi, cos, sin


class GEODistanceStrategy(object):
    """
    计算两个经纬度之间的距离(python算法)
    https://www.cnblogs.com/lgh344902118/p/7490795.html
    """

    def __init__(self):
        pass

    def _rad(self, d):
        try:
            r = float(d) * float(pi) / float(180.0)
        except Exception as e:
            r = 1
        return r

    def _getDistance(self, lat1, lng1, lat2, lng2):
        EARTH_RADIUS = 6371.393
        radLat1 = self._rad(lat1)
        radLat2 = self._rad(lat2)
        a = radLat1 - radLat2
        b = self._rad(lng1) - self._rad(lng2)
        s = 2 * math.asin(math.sqrt(math.pow(sin(a / 2), 2) + cos(radLat1) * cos(radLat2) * math.pow(sin(b / 2), 2)))
        s = s * EARTH_RADIUS
        return s

    def compare(self, p_address_dict_a=None, p_address_dict_b=None):
        """小于等于指定距离(MIN_DISTANCE), 则认为 这两个点是同一个地址
        :param p_address_dict_a:
        :param p_address_dict_b:
        :return:
        """


        s = self._getDistance(p_address_dict_a['纬度'], p_address_dict_a['经度'], p_address_dict_b['纬度'],
                              p_address_dict_b['经度'])
        rst = s * 1000 <= 200
        return rst

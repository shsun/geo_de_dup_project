#!/usr/bin/python
# -*- coding: UTF-8 -*-
import difflib
import math
from math import pi, cos, sin


class StringDiffStrategy(object):
    """
    计算两个经纬度之间的距离(python算法)
    https://www.cnblogs.com/lgh344902118/p/7490795.html
    """
    EARTH_REDIUS = 6378.137

    def __init__(self):
        pass

    def cal_diff(self, p_address_dict_A=None, p_address_dict_B=None):
        """
        计算出来的结果单位为米

        :param p_address_dict_A:
        :param p_address_dict_B:
        :return:详细地址（拼接省市区）匹配度; 详细地址(PROD地址) 匹配度
        """

        # excel_title = ['序号', '地址编号', '省份', '城市', '区/县', '乡', '详细地址（拼接省市区）', '详细地址(PROD地址)', '经度', '纬度', '标准地址', '标准地址是否新地址']

        query_str = p_address_dict_A['详细地址（拼接省市区）']
        s1 = p_address_dict_B['详细地址（拼接省市区）']
        r1 = difflib.SequenceMatcher(None, query_str, s1).quick_ratio()

        # query_str = p_address_dict_A['详细地址(PROD地址)']
        # s1 = p_address_dict_B['详细地址(PROD地址)']
        # r2 = difflib.SequenceMatcher(None, query_str, s1).quick_ratio()
        r2 = 1

        # 详细地址（拼接省市区）匹配度
        # 详细地址(PROD地址) 匹配度

        return r1, r2

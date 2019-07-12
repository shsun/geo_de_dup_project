#!/usr/bin/python
# -*- coding: UTF-8 -*-
import difflib
import math
from math import pi, cos, sin

from app.XUtils import XUtils


class StringDiffStrategy(object):
    """
    """

    def __init__(self):
        pass

    def compare(self, p_address_dict_a=None, p_address_dict_b=None):
        """判断'详细地址（拼接省市区）'的相似度, 大于等于 0.8,则认为是同一个地址

        :param p_address_dict_a:
        :param p_address_dict_b:
        :return:详细地址（拼接省市区）匹配度; 详细地址(PROD地址) 匹配度
        """

        #    excel_title = ['序号', '地址编号', '省份', '城市', '区/县', '乡', '详细地址（拼接省市区）', '详细地址(PROD地址)', '经度', '纬度', '标准地址', '标准地址是否新地址']
        # query_str = str(p_address_dict_a['详细地址（拼接省市区）'])
        # s1 = str(p_address_dict_b['详细地址（拼接省市区）'])
        query_str = XUtils.remove_noise(p_address_dict=p_address_dict_a, p_key='详细地址（拼接省市区）')
        s1 = XUtils.remove_noise(p_address_dict=p_address_dict_b, p_key='详细地址（拼接省市区）')

        r1 = difflib.SequenceMatcher(None, query_str, s1).quick_ratio()

        try:
            # query_str = p_address_dict_a['详细地址(PROD地址)']
            # s1 = p_address_dict_b['详细地址(PROD地址)']
            query_str = XUtils.remove_noise(p_address_dict=p_address_dict_a, p_key='详细地址(PROD地址)')
            s1 = XUtils.remove_noise(p_address_dict=p_address_dict_b, p_key='详细地址(PROD地址)')
            r2 = difflib.SequenceMatcher(None, query_str, s1).quick_ratio()
        except Exception as e:
            r2 = 1.0
        # 详细地址（拼接省市区）匹配度
        # 详细地址(PROD地址) 匹配度

        # NOTE 看这里
        return r1 >= 0.8 and r2 >= 0.8

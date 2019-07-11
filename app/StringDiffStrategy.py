#!/usr/bin/python
# -*- coding: UTF-8 -*-
import difflib
import math
from math import pi, cos, sin


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
        query_str = p_address_dict_a['详细地址（拼接省市区）']
        s1 = p_address_dict_b['详细地址（拼接省市区）']
        r1 = difflib.SequenceMatcher(None, query_str, s1).quick_ratio()

        try:
            query_str = p_address_dict_a['详细地址(PROD地址)']
            s1 = p_address_dict_b['详细地址(PROD地址)']
            r2 = difflib.SequenceMatcher(None, query_str, s1).quick_ratio()
        except Exception as e:
            r2 = 1.0
        # 详细地址（拼接省市区）匹配度
        # 详细地址(PROD地址) 匹配度

        return r1 >= 0.8 and r2 >= 0.8
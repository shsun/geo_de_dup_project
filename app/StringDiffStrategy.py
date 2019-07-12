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

        #    excel_title = ['序号', '地址编号', '省份', '城市', '区/县', '乡', '详细地址（拼接省市区）', '详细地址(PROD地址)', '经度', '纬度', '标准地址', '标准地址是否新地址']
        # query_str = str(p_address_dict_a['详细地址（拼接省市区）'])
        # s1 = str(p_address_dict_b['详细地址（拼接省市区）'])
        query_str = self._remove_noise(p_address_dict=p_address_dict_a, p_key='详细地址（拼接省市区）')
        s1 = self._remove_noise(p_address_dict=p_address_dict_b, p_key='详细地址（拼接省市区）')

        r1 = difflib.SequenceMatcher(None, query_str, s1).quick_ratio()

        try:
            # query_str = p_address_dict_a['详细地址(PROD地址)']
            # s1 = p_address_dict_b['详细地址(PROD地址)']
            query_str = self._remove_noise(p_address_dict=p_address_dict_a, p_key='详细地址(PROD地址)')
            s1 = self._remove_noise(p_address_dict=p_address_dict_b, p_key='详细地址(PROD地址)')
            r2 = difflib.SequenceMatcher(None, query_str, s1).quick_ratio()
        except Exception as e:
            r2 = 1.0
        # 详细地址（拼接省市区）匹配度
        # 详细地址(PROD地址) 匹配度

        return r1 >= 0.8 and r2 >= 0.8

    def _remove_noise(self, p_address_dict=None, p_key=None):
        """ 丢弃噪音数据
        比如省市县啥的， 就不应该参与比较， 这个没意义
        :param p_address_dict:
        :param p_key:
        :return:
        """
        province_name = p_address_dict['省份'] if p_address_dict['省份'] is not None else ''
        city_name = p_address_dict['城市'] if p_address_dict['城市'] is not None else ''
        district_name = p_address_dict['区/县'] if p_address_dict['区/县'] is not None else ''
        town_name = p_address_dict['乡'] if p_address_dict['乡'] is not None else ''
        s = str(p_address_dict[p_key]).replace(province_name, '').replace(city_name, '').replace(district_name, '').replace(town_name, '')
        return s

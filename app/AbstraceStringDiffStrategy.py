#!/usr/bin/python
# -*- coding: UTF-8 -*-
import difflib

from app.XUtils import XUtils


class AbstractStringDiffStrategy:
    """
    """
    G_60 = 0.6
    G_70 = 0.7
    G_80 = 0.8
    G_90 = 0.9
    G_100 = 1.0

    def __init__(self):
        pass

    def compare(self, p_address_dict_a=None, p_address_dict_b=None):
        """判断'详细地址（拼接省市区）'的相似度, 大于等于 0.8,则认为是同一个地址

        :param p_address_dict_a:
        :param p_address_dict_b:
        :return:详细地址（拼接省市区）匹配度; 详细地址(PROD地址) 匹配度
        """

        rst = True
        #    excel_title = ['序号', '地址编号', '省份', '城市', '区/县', '乡', '详细地址（拼接省市区）', '详细地址(PROD地址)', '经度', '纬度', '标准地址', '标准地址是否新地址']
        # query_str = str(p_address_dict_a['详细地址（拼接省市区）'])
        # s1 = str(p_address_dict_b['详细地址（拼接省市区）'])

        is_the_same_province = p_address_dict_a['省份'] == p_address_dict_b['省份']
        is_the_same_city = p_address_dict_a['城市'] == p_address_dict_b['城市']
        is_the_same_district = p_address_dict_a['区/县'] == p_address_dict_b['区/县']
        is_the_same_town = p_address_dict_a['乡'] == p_address_dict_b['乡']

        # 如果 '省份', '城市', '区/县' 任一个不匹配，则认为不是一个地址; 后面就完全没必要进行字符串相似度对比
        # NOTE 比如
        # NOTE 山东省济南市和平区幸福路1号
        # NOTE 山东省泰安市和平区幸福路1号
        # NOTE 这个要简单去噪音， 就会认为是同一个地址， 实际不是一个地址
        if is_the_same_province is False or is_the_same_city is False or is_the_same_district is False:
            rst = False

        return rst

    def has_the_same_tel_no(self, p_address_dict_a=None, p_address_dict_b=None, p_key=None):
        """判断是否有同一个手机号码
        :param p_address_dict_a:
        :param p_address_dict_b:
        :param p_key:
        :return:
        """
        rst = False
        mobile_1_list = XUtils.fetch_all_mobiles(p_text=p_address_dict_a[p_key])
        mobile_2_list = XUtils.fetch_all_mobiles(p_text=p_address_dict_b[p_key])
        mobile_list = mobile_1_list + mobile_2_list
        mobile_set = set(mobile_list)
        for item in mobile_set:
            if mobile_list.count(item) > 1:
                rst = True
                break
        return rst

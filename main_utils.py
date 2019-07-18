#!/usr/bin/env python
# -*- coding: utf-8 -*-
import warnings, datetime, pprint, sys, os, os.path, xlrd, xlwt

from app.GEODistanceStrategy import GEODistanceStrategy
from app.AddressStringDiffStrategy import AddressStringDiffStrategy
from app.LALPctStrategy import LALPctStrategy
from app.AddressCosineSimilarityStrategy import AddressCosineSimilarityStrategy
from app.XUtils import XUtils

# sys.setdefaultencoding('utf8')
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


def fetch_max_length_item(p_excel_sub_list=None):
    # '详细地址（拼接省市区）'
    rst = None
    # 然后在生成表三，从表2中每一个重复标号的，选取详细地址最长字符的作为表3的地址
    max_len = 0
    for tmp_new_dict in p_excel_sub_list:
        tmp_len = len(tmp_new_dict['详细地址（拼接省市区）'])
        if tmp_len > max_len:
            max_len = tmp_len
            rst = tmp_new_dict
    return rst


def contains(p_new_excel_list=None, p_old_dict=None):
    """
    判断
    :param p_new_excel_list:
    :param p_old_dict:
    :return: rst为true的时候表示能够在p_new_excel_list找到兄弟节点， 否则找不到兄弟节点。 (所谓兄弟节点就是指着这2个点认为是同一个地址), brother_dict是p_old_dict的兄弟节点.
    """
    rst = False
    brother_dict = None
    for tmp_new_dict in p_new_excel_list:

        # Note 利用余弦相似度公式计算两字符串的相似性 (相似度达到0.8则认为是一个地址，否则是2个不同地址, 这个0.8我是随便写的, 可修改)
        # rst_cos_sim = CosineSimilarityStrategy().compare(p_address_dict_a=tmp_new_dict, p_address_dict_b=p_old_dict)

        # NOTE 通过对经纬度的比较，相差百分之一或更小以内的视为同一地址，否则视为两个地址
        # rst_lal = LALPctStrategy().compare(p_address_dict_a=tmp_new_dict, p_address_dict_b=p_old_dict)

        # Note 根据距离来判断(200米)
        match_distance, real_distance = GEODistanceStrategy().compare(p_address_dict_a=tmp_new_dict, p_address_dict_b=p_old_dict)

        # Note 计算字符匹配度
        # 详细地址（拼接省市区）匹配度; 详细地址(PROD地址) 匹配度
        rst_str_diff, sim_string = AddressStringDiffStrategy().compare(p_address_dict_a=tmp_new_dict, p_address_dict_b=p_old_dict)

        # Note 看这里 ................................... 加权系数, 可以调. 因为字符串匹配更优, 所以权重大一些, 此处需要人工去调
        FACTOR = 0.75

        # 计算根据距离算出来的相似度. 其中x是求大圆算出来的距离， 即2个点的真实距离
        x = real_distance
        b = (500 - x) / 500
        # 现在算法有一个挺严重的问题就是sim=FACTER*a+（1-FACTER）*b这里，这里b有可能负的太厉害了，我建议在b那里做一个判定，b<-1的话，b直接就等于-1，或者改成-2之类的
        # b还影响匹配度， 但是影响程度非常低
        if b < -1:
            b = -1

        # a是字符串相似度, b是距离相似度
        a = sim_string
        sim = FACTOR * a + (1 - FACTOR) * b

        # rst = match_distance is True and rst_str_diff is True
        # NOTE 看这里  ...................... 此处也需要人为调整
        rst = sim >= 0.6

        if rst is True:
            brother_dict = tmp_new_dict
            break
    return rst, brother_dict

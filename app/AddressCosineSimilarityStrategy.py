#!/usr/bin/python
# -*- coding: UTF-8 -*-
import numpy as np
import re
import warnings
from app.XUtils import XUtils

from app.AbstraceStringDiffStrategy import AbstractStringDiffStrategy


class AddressCosineSimilarityStrategy(AbstractStringDiffStrategy):
    """
    利用余弦相似度公式计算两字符串的相似性
    https://blog.csdn.net/weixin_44208569/article/details/90315904
    """

    def __init__(self):
        super(AddressCosineSimilarityStrategy, self).__init__()
        pass

    def compare(self, p_address_dict_a=None, p_address_dict_b=None):
        """
        :param p_address_dict_a:
        :param p_address_dict_b:
        :return:
        """
        # s1 = "hi，今天温度是12摄氏度。"
        # s2 = "hello，今天温度很高。"

        # s1 = p_address_dict_a['详细地址（拼接省市区）']
        # s2 = p_address_dict_b['详细地址（拼接省市区）']

        # 详细地址（拼接省市区）匹配度
        P_KEY = '详细地址（拼接省市区）'

        # 修改原始数据，丢弃掉空格，特殊字符串(物理丢弃)
        p_address_dict_a[P_KEY] = XUtils.remove_noise_empty_punctuation(p_address_dict=p_address_dict_a, p_key=P_KEY)
        p_address_dict_b[P_KEY] = XUtils.remove_noise_empty_punctuation(p_address_dict=p_address_dict_b, p_key=P_KEY)

        # 丢弃省市县(内存中丢弃, 不篡改之前数据)
        s1 = XUtils.remove_noise_province_city_district(p_address_dict=p_address_dict_a, p_key=P_KEY)
        s2 = XUtils.remove_noise_province_city_district(p_address_dict=p_address_dict_b, p_key=P_KEY)

        # 例如有的地址叫国储八三二，有的地址叫国储832, 统一处理为国储832, 以提升匹配度
        s1 = XUtils.convert_chinese_numerals_2_arabic_numerals(p_str=s1)
        s2 = XUtils.convert_chinese_numerals_2_arabic_numerals(p_str=s2)

        vec1, vec2 = self.get_word_vector(s1, s2)
        dist1 = self.cos_dist(vec1, vec2)

        # Note 看这里 此处认为相似度达到0.8才是同一个地址， 这个数字可以改
        rst = dist1 >= AddressCosineSimilarityStrategy.G_80

        if rst is True:
            rst = super(AddressCosineSimilarityStrategy, self).compare(p_address_dict_a=p_address_dict_a, p_address_dict_b=p_address_dict_b)

        return rst

    def get_word_vector(self, s1, s2):
        """
        :param s1: 句子1
        :param s2: 句子2
        :return: 返回中英文句子切分后的向量
        """

        # 把句子按字分开，中文按字分，英文按单词，数字按空格
        regEx = re.compile('[\\W]*')
        res = re.compile(r"([\u4e00-\u9fa5])")

        p1 = regEx.split(s1.lower())
        str1_list = []
        for str in p1:
            if res.split(str) == None:
                str1_list.append(str)
            else:
                ret = res.split(str)
                for ch in ret:
                    str1_list.append(ch)
        # print(str1_list)

        p2 = regEx.split(s2.lower())
        str2_list = []
        for str in p2:
            if res.split(str) == None:
                str2_list.append(str)
            else:
                ret = res.split(str)
                for ch in ret:
                    str2_list.append(ch)
        # print(str2_list)

        list_word1 = [w for w in str1_list if len(w.strip()) > 0]  # 去掉为空的字符
        list_word2 = [w for w in str2_list if len(w.strip()) > 0]  # 去掉为空的字符
        # print(list_word1, list_word2)

        # 列出所有的词,取并集
        key_word = list(set(list_word1 + list_word2))
        # print(key_word)
        # 给定形状和类型的用0填充的矩阵存储向量
        word_vector1 = np.zeros(len(key_word))
        word_vector2 = np.zeros(len(key_word))

        # 计算词频
        # 依次确定向量的每个位置的值
        for i in range(len(key_word)):
            # 遍历key_word中每个词在句子中的出现次数
            for j in range(len(list_word1)):
                if key_word[i] == list_word1[j]:
                    word_vector1[i] += 1
            for k in range(len(list_word2)):
                if key_word[i] == list_word2[k]:
                    word_vector2[i] += 1

        # 输出向量
        # print(word_vector1)
        # print(word_vector2)
        return word_vector1, word_vector2

    def cos_dist(self, vec1, vec2):
        """
        :param vec1: 向量1
        :param vec2: 向量2
        :return: 返回两个向量的余弦相似度
        """
        dist1 = float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
        return dist1

#!/usr/bin/python
# -*- coding: UTF-8 -*-
import difflib

from app.XUtils import XUtils

from app.AbstraceStringDiffStrategy import AbstractStringDiffStrategy


class AddressStringDiffStrategy(AbstractStringDiffStrategy):
    """
    """

    def __init__(self):
        super(AddressStringDiffStrategy, self).__init__()
        pass

    def compare(self, p_address_dict_a=None, p_address_dict_b=None):
        """判断'详细地址（拼接省市区）'的相似度, 大于等于 0.8,则认为是同一个地址

        :param p_address_dict_a:
        :param p_address_dict_b:
        :return:详细地址（拼接省市区）匹配度; 详细地址(PROD地址) 匹配度
        """
        # 详细地址（拼接省市区）匹配度
        query_str = XUtils.remove_noise(p_address_dict=p_address_dict_a, p_key='详细地址（拼接省市区）')
        s1 = XUtils.remove_noise(p_address_dict=p_address_dict_b, p_key='详细地址（拼接省市区）')
        r1 = difflib.SequenceMatcher(None, query_str, s1).quick_ratio()
        # Note 如果分数介于60~80分, 则再给一次机会, 如果具有相同手机号码，则认为是同一个地址
        if r1 < AddressStringDiffStrategy.G_80 and r1 >= AddressStringDiffStrategy.G_60:
            with_same_tel_no = self.has_the_same_tel_no(p_address_dict_a=p_address_dict_a, p_address_dict_b=p_address_dict_b, p_key='详细地址（拼接省市区）')
            r1 = AddressStringDiffStrategy.G_100 if with_same_tel_no else r1

        # 详细地址(PROD地址) 匹配度
        try:
            # query_str = p_address_dict_a['详细地址(PROD地址)']
            # s1 = p_address_dict_b['详细地址(PROD地址)']
            query_str = XUtils.remove_noise(p_address_dict=p_address_dict_a, p_key='详细地址(PROD地址)')
            s1 = XUtils.remove_noise(p_address_dict=p_address_dict_b, p_key='详细地址(PROD地址)')
            r2 = difflib.SequenceMatcher(None, query_str, s1).quick_ratio()
            # Note 如果分数介于60~80分, 则再给一次机会, 如果具有相同手机号码，则认为是同一个地址
            if r2 < AddressStringDiffStrategy.G_80 and r2 >= AddressStringDiffStrategy.G_60:
                with_same_tel_no = self.has_the_same_tel_no(p_address_dict_a=p_address_dict_a, p_address_dict_b=p_address_dict_b, p_key='详细地址(PROD地址)')
                r2 = AddressStringDiffStrategy.G_100 if with_same_tel_no else r2
        except Exception as e:
            r2 = AddressStringDiffStrategy.G_100
        # NOTE 看这里
        rst = r1 >= AddressStringDiffStrategy.G_80 and r2 >= AddressStringDiffStrategy.G_80

        #
        if rst is True:
            rst = super(AddressStringDiffStrategy, self).compare(p_address_dict_a=p_address_dict_a, p_address_dict_b=p_address_dict_b)

        return rst

#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import pprint, sys, os, os.path, xlrd, xlwt, random

from app.XUtils import XUtils

import re

import re

from app.StringDiffStrategy import StringDiffStrategy

# 自定义获取文本手机号函数
def get_findAll_mobiles(text):
    """
    :param text: 文本
    :return: 返回手机号列表
    """
    mobiles = re.findall(r"1\d{10}", text)
    return mobiles


if __name__ == '__main__':
    telNumber = 'Suppose my Phone No. is 13426096674'
    m = XUtils.fetch_all_mobiles(p_text=telNumber)

    print(m)

    StringDiffStrategy().compare()

    sys.exit(0)

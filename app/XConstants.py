#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import pprint, sys, re, os, os.path, xlrd, xlwt
import json
import urllib.request
from urllib import parse


class XConstants(object):
    G_DIGIT_DICT = {'零': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}

    # Note 看这里 ................................... ALPHA、BETA系数, 可以调. 因为字符串匹配更优, 所以权重大一些, 此处需要人工去调
    ALPHA = 0.75
    #
    BETA = 0.6

    # 再计算b =（500 - X） / 500, Note 此处的500也作为一个参数，允许调整，见XConstants.FIXED_DISTANCE
    FIXED_DISTANCE = 500

    RGE = 0.6

    FOO_BAR = '......................................'

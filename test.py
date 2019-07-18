#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import pprint, sys, os, os.path, xlrd, xlwt, random, re

from app.XUtils import XUtils

if __name__ == '__main__':
    print(XUtils.convert_chinese_numerals_2_arabic_numerals_4_str(p_str='国储八三二'))
    print(XUtils.convert_chinese_numerals_2_arabic_numerals_4_str(p_str='国储八三三三三三三三三三三二'))
    print(XUtils.convert_chinese_numerals_2_arabic_numerals_4_str(p_str='国储832'))

    print(XUtils.convert_chinese_numerals_2_arabic_numerals_4_str(p_str='八三二国储'))
    print(XUtils.convert_chinese_numerals_2_arabic_numerals_4_str(p_str='八三二'))

    print(XUtils.convert_chinese_numerals_2_arabic_numerals_4_str(p_str='八三国储二'))

    print(XUtils.convert_chinese_numerals_2_arabic_numerals_4_str(p_str=''))

    sys.exit(0)

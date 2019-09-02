#!/usr/bin/env python
# -*- coding: utf-8 -*-
import warnings, datetime, pprint, sys, os, os.path, xlrd, xlwt

# sys.setdefaultencoding('utf8')
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


def main(p_args):
    """

    :param p_args:
    :return:
    """
    print('\n程序执行完毕 !!! DONE DONE DONE DONE DONE DONE DONE DONE DONE DONE DONE')
    return 0


if __name__ == '__main__':
    # NOTE 程序入口
    warnings.filterwarnings('ignore')

    rst = main(sys.argv)

    sys.exit(rst)

#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import pprint, sys, os, os.path, xlrd, xlwt, random

from app.XUtils import XUtils

"""
1. 丢弃坏数据150条后，会生成一个 receiving_address_input_1_ok.xls, 即完全正确的数据
2. 生成2份excel, 1份是100条，用于后续做增量测试； 另外一份作为存量(即表1)
"""


def main(p_args):
    # Note 看这里 如果想做50个增量， 就把这个100改成50
    G_INCREMENT_SIZE = int(input('请输入样本数(必须是正整数):'))

    print('\n\n样本数为========>>%d\n' % (G_INCREMENT_SIZE))

    excel_title = ['序号', '地址编号', '省份', '城市', '区/县', '乡', '详细地址（拼接省市区）', '详细地址(PROD地址)', '经度', '纬度', '标准地址', '标准地址是否新地址']

    # 1. 读取地址信息
    old_excel_list = XUtils.excel_to_list(p_read_excel_file_path='./resources/receiving_address_input_1.xlsx',
                                          p_sheet_name='Sheet1',
                                          p_excel_title_list=excel_title)
    old_len = len(old_excel_list)
    print('\n最原始的数据总条数old_excel_list length=====>>%d' % (old_len))
    err_num = 0
    tmp_old_excel_list = []
    for tmp_dict in old_excel_list:
        if XUtils.has_valid_lat_lng(tmp_dict):
            tmp_old_excel_list.append(tmp_dict)
        else:
            err_num += 1
    old_excel_list = tmp_old_excel_list
    print('\n经纬度数据有问题的数据条数  invalid data num======>>%d' % (err_num))
    print('\n真实参与处理的数据条数(即抛弃了非法数据后) old_excel_list length=====>> (%d - %d) = %d\n' % (
        old_len, err_num, len(old_excel_list)))

    XUtils.process_and_dump_2_excel(p_excel_title=excel_title, p_new_excel_list=old_excel_list,
                                    p_new_file='./resources/receiving_address_input_1_ok.xls')

    # 增量
    increment_list = []
    while len(increment_list) < G_INCREMENT_SIZE:
        random_index = random.randint(0, len(old_excel_list) - 1)
        tmp_dict = old_excel_list.pop(random_index)
        increment_list.append(tmp_dict)
    # 存量(即表1)
    stock_list = old_excel_list

    print('存量 increment_list.length===>%d' % (len(increment_list)))
    print('删除了存量后的表1 stock_list.length===>%d' % (len(stock_list)))

    XUtils.process_and_dump_2_excel(p_excel_title=excel_title, p_new_excel_list=stock_list,
                                    p_new_file='./resources/receiving_address_stock_1_ok.xls')

    XUtils.process_and_dump_2_excel(p_excel_title=excel_title, p_new_excel_list=increment_list,
                                    p_new_file='./resources/receiving_address_increment_1_ok.xls')

    return 0


if __name__ == '__main__':
    # NOTE 程序入口

    # 115.951342, 36.504032

    # 维度, 经度
    # lat, lng = XUtils.findlogandlat('山东省聊城市东昌府区聊城市嘉明经济开发区嘉和路1号')

    sys.exit(main(sys.argv))

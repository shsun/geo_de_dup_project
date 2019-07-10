#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import pprint, sys, os, os.path, xlrd, xlwt

from app.XUtils import XUtils


def main(p_args):
    excel_title = ['序号', '地址编号', '省份', '城市', '区/县', '乡', '详细地址（拼接省市区）', '详细地址(PROD地址)', '经度', '纬度', '标准地址', '标准地址是否新地址']

    # 1. 读取地址信息
    old_excel_list = XUtils.excel_to_list(p_read_excel_file_path='./resources/receiving_address_input_1.xlsx',
                                          p_sheet_name='Sheet1',
                                          p_excel_title_list=excel_title)
    old_len = len(old_excel_list)
    print('\n最原始的数据总条数old_excel_list length=====>>%d' % (old_len))
    err_num = 0
    final_err_num = 0
    tmp_old_excel_list = []
    for tmp_dict in old_excel_list:
        skip = False
        try:
            a = 1.0 / tmp_dict['经度']
            a = 1.0 / tmp_dict['纬度']
        except Exception as e:
            err_num += 1
            # 维度, 经度
            lat, lng = XUtils.findlogandlat(tmp_dict['详细地址（拼接省市区）'])
            if lat != 0.0 and lng != 0.0:
                tmp_dict['纬度'] = lat
                tmp_dict['经度'] = lng
            else:
                final_err_num += 1
                skip = True
            print('err_num=%d addr=%s, lat=%f lng=%f' % (err_num, tmp_dict['详细地址（拼接省市区）'], lat, lng))
        if skip is False:
            tmp_old_excel_list.append(tmp_dict)
    old_excel_list = tmp_old_excel_list
    print('\n经纬度数据有问题的数据条数  invalid data num======>>%d' % (err_num))
    print('\n利用百度地图API纠正的数据条数=======>>%d,   无法纠正的数据条数======>>%d' % ((err_num - final_err_num), final_err_num))

    process_and_dump_2_excel(p_excel_title=excel_title, p_new_excel_list=old_excel_list,
                             p_new_file='./resources/receiving_address_input_1_correct_150_via_baidu.xls')

    return 0


def process_and_dump_2_excel(p_excel_title=None, p_new_excel_list=None, p_new_file=None):
    stus = [p_excel_title]
    for tmp_dict in p_new_excel_list:
        arr = []
        for title in p_excel_title:
            value = tmp_dict[title]
            arr.append(value)
        stus.append(arr)

    if os.path.exists(p_new_file):
        os.remove(p_new_file)
    success = XUtils.dict_to_excel(p_write_excel_file_path=p_new_file, p_sheet_name='Sheet1', p_dict_content=stus,
                                   p_excel_title_list=p_excel_title)


if __name__ == '__main__':
    # NOTE 程序入口

    # 115.951342, 36.504032

    # 维度, 经度
    # lat, lng = XUtils.findlogandlat('山东省聊城市东昌府区聊城市嘉明经济开发区嘉和路1号')

    sys.exit(main(sys.argv))

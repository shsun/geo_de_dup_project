#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# **************************************************************************************
# 			                      ______
# 			                   .-"      "-.
# 			                  /    OMG     \
# 			                 |              |
# 			                 |,  .-.  .-.  ,|
# 			                 | )(__/  \__)( |
# 			                 |/     /\     \|
# 			       (@_       (_     ^^     _)
# 			  _     ) \_______\__|IIIIII|__/__________________________
# 			 (_)@8@8{}<________|-\IIIIII/-|___________________________>
# 			        )_/        \          /
# 			       (@           `--------`
#
# **************************************************************************************

import sys, os, os.path, xlrd, xlwt

from app.GEODistanceStrategy import GEODistanceStrategy
from app.StringDiffStrategy import StringDiffStrategy
from app.LALPctStrategy import LALPctStrategy
from app.XUtils import XUtils


def contains(p_new_excel_list=None, p_old_dict=None):
    """
    判断
    :param p_new_excel_list:
    :param p_old_dict:
    :return:
    """
    rst = False
    for tmp_new_dict in p_new_excel_list:

        # NOTE 通过对经纬度的比较，相差百分之一或更小以内的视为同一地址，否则视为两个地址
        # rst = LALPctStrategy().compare(p_address_dict_a=tmp_new_dict, p_address_dict_b=p_old_dict)

        # Note 根据距离来判断(200米)
        rst = GEODistanceStrategy().compare(p_address_dict_a=tmp_new_dict, p_address_dict_b=p_old_dict)

        # Note 计算字符匹配度
        # 详细地址（拼接省市区）匹配度; 详细地址(PROD地址) 匹配度
        # rst = StringDiffStrategy().compare(p_address_dict_a=tmp_new_dict, p_address_dict_b=p_old_dict)

        if rst is True:
            break
    return rst


def main(p_args):
    excel_title = ['序号', '地址编号', '省份', '城市', '区/县', '乡', '详细地址（拼接省市区）', '详细地址(PROD地址)', '经度', '纬度', '标准地址', '标准地址是否新地址']

    # 1. 读取地址信息
    old_excel_list = XUtils.excel_to_list(p_read_excel_file_path='./resources/receiving_address_input_1.xlsx',
                                          p_sheet_name='Sheet1',
                                          p_excel_title_list=excel_title)
    print('\n老数据总条数old_excel_list length=====>>%d' % (len(old_excel_list)))
    # 2. 丢弃经纬度有问题的数据, 只留下经纬度正确的数据
    err_num = 0
    tmp_old_excel_list = []
    for tmp_dict in old_excel_list:
        try:
            a = 1.0 / tmp_dict['经度']
            a = 1.0 / tmp_dict['纬度']
            tmp_old_excel_list.append(tmp_dict)
        except Exception as e:
            err_num += 1
    old_excel_list = tmp_old_excel_list
    print('\n经纬度数据有问题的数据条数  invalid data num======>>%d\n' % (err_num))

    # Note 最重要的一步
    # Note 3. 去重, 将去重后的数据存入new_excel_list中
    # Note 对老数据循环, 挨个去和新数据内的所有数据逐个对比, 如果在new_list内找到了, 则认为是同一地址, 否则认为是不同地址, 不同地址则添加到new_excel_list内
    # Note 所以这里是两层循环
    # Note
    new_excel_list = []
    for tmp_dict in old_excel_list:
        rst = contains(p_new_excel_list=new_excel_list, p_old_dict=tmp_dict)
        if rst is False:
            new_excel_list.append(tmp_dict)
    print('\n去重后的新数据条数final new_excel_list length=====>>%d' % (len(new_excel_list)))

    # 4. 对去重后的数据进行处理
    stus = [excel_title]
    for tmp_dict in new_excel_list:
        arr = []
        for title in excel_title:
            value = tmp_dict[title]
            arr.append(value)
        stus.append(arr)

    # 5. 将去重后的数据写入新excel
    new_file = './resources/receiving_address_output_1.xls'
    if os.path.exists(new_file):
        os.remove(new_file)
    success = XUtils.dict_to_excel(p_write_excel_file_path=new_file, p_sheet_name='Sheet1', p_dict_content=stus,
                                   p_excel_title_list=excel_title)

    print('程序执行完毕 !!! DONE DONE DONE DONE DONE DONE DONE DONE DONE DONE DONE')
    return 0


if __name__ == '__main__':
    # NOTE 程序入口
    sys.exit(main(sys.argv))

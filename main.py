#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import sys, os, os.path, xlrd, xlwt

from app.GEODistanceStrategy import GEODistanceStrategy
from app.StringDiffStrategy import StringDiffStrategy
from app.LALPctStrategy import LALPctStrategy


def read_excel(file):
    """
    读入excel文件
    :rtype : object
    :param file:
    :return: 数据对象
    """
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as err:
        print(err)


def excel_to_list(p_read_excel_file_path=None, p_sheet_name=None, p_excel_title_list=None):
    """
    :rtype : object
    :return list
    """
    my_list = []
    data = read_excel(p_read_excel_file_path)
    table = data.sheet_by_name(p_sheet_name)
    for i in range(1, table.nrows):
        row_content = table.row_values(i, 0, table.ncols)
        dict_column = dict(zip(p_excel_title_list, row_content))
        # dict_column['经度'] = float(dict_column['经度'])
        # dict_column['纬度'] = float(dict_column['纬度'])
        # for (k, v) in dict_column.items():
        #     print(k)
        my_list.append(dict_column)
    return my_list


def dict_to_excel(p_write_excel_file_path=None, p_sheet_name=None, p_dict_content=None, p_excel_title_list=None):
    """
    将字典写入excel中
    :type dict_content: object dict
    excel_title 列标题
    """
    book = xlwt.Workbook()
    sheet = book.add_sheet(p_sheet_name)
    row_index = 0
    for stu in p_dict_content:
        col_index = 0
        for value in stu:
            sheet.write(row_index, col_index, value)
            col_index += 1
        row_index += 1
    book.save(p_write_excel_file_path)
    return True


def contains(p_list=None, p_dict=None):
    """

    :param p_list:
    :param p_dict:
    :return:
    """
    rst = False
    for obj in p_list:

        rst = LALPctStrategy().compare(p_address_dict_a=obj, p_address_dict_b=p_dict)

        # Note 根据距离来判断(200米)
        rst = GEODistanceStrategy().compare(p_address_dict_a=obj, p_address_dict_b=p_dict)

        # Note 计算字符匹配度
        # 详细地址（拼接省市区）匹配度; 详细地址(PROD地址) 匹配度
        rst = StringDiffStrategy().compare(p_address_dict_a=obj, p_address_dict_b=p_dict)

        # Note 此处代码逻辑很重要
        # if distance <= 200:
        #     # if distance <= 100 and r1 >= 0.8 and r2 >= 0.8:
        #     rst = True

        if rst is True:
            break
    return rst


def main(p_args):
    excel_title = ['序号', '地址编号', '省份', '城市', '区/县', '乡', '详细地址（拼接省市区）', '详细地址(PROD地址)', '经度', '纬度', '标准地址', '标准地址是否新地址']

    old_excel_list = excel_to_list(p_read_excel_file_path='./resources/receiving_address_input_1.xlsx',
                                   p_sheet_name='Sheet1',
                                   p_excel_title_list=excel_title)
    new_excel_list = []

    print('\n老数据总条数old_excel_list length=====>>%d' % (len(old_excel_list)))

    # 1. 丢弃经纬度有问题的数据, 只留下经纬度正确的数据
    err_num = 0
    tmp_old_excel_list = []
    for tmp in old_excel_list:
        try:
            a = 1.0 / tmp['经度']
            a = 1.0 / tmp['纬度']
            tmp_old_excel_list.append(tmp)
        except Exception as e:
            err_num += 1
    old_excel_list = tmp_old_excel_list
    print('\n经纬度数据有问题的数据条数  invalid data num======>>%d\n' % (err_num))

    # Note
    for tmp in old_excel_list:
        if contains(p_list=new_excel_list, p_dict=tmp) is False:
            new_excel_list.append(tmp)

    print('\n去重后的新数据条数final new_excel_list length=====>>%d' % (len(new_excel_list)))

    stus = [excel_title]
    for tmp in new_excel_list:
        arr = []
        for title in excel_title:
            value = tmp[title]
            arr.append(value)
        stus.append(arr)

    #
    new_file = './resources/receiving_address_output_1.xls'
    if os.path.exists(new_file):
        os.remove(new_file)
    success = dict_to_excel(p_write_excel_file_path=new_file, p_sheet_name='Sheet1', p_dict_content=stus,
                            p_excel_title_list=excel_title)

    print('DONE DONE DONE DONE DONE DONE DONE DONE DONE DONE DONE DONE DONE DONE DONE DONE !!!!!!!!!!!!!!!!!!!!!!!!!!!')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))

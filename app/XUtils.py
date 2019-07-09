#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import sys, os, os.path, xlrd, xlwt


class XUtils(object):

    @staticmethod
    def read_excel(p_read_excel_file_path=None):
        """
        读入excel文件
        :rtype : object
        :param p_read_excel_file_path:
        :return: 数据对象
        """
        try:
            data = xlrd.open_workbook(p_read_excel_file_path)
            return data
        except Exception as err:
            print(err)

    @staticmethod
    def excel_to_list(p_read_excel_file_path=None, p_sheet_name=None, p_excel_title_list=None):
        """
        :rtype : object
        :return list
        """
        my_list = []
        data = XUtils.read_excel(p_read_excel_file_path=p_read_excel_file_path)
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

    @staticmethod
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

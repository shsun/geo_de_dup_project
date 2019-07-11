#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import pprint, sys, os, os.path, xlrd, xlwt
import json
import urllib.request
from urllib import parse


class XUtils(object):

    @staticmethod
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

    @staticmethod
    def findlogandlat(full_address):
        """

        :param full_address:
        :return:
        """
        query = {
            'key': 'lD4KiCvXfGho6afGao2ztKXiUq9rQNmZ',
            'address': full_address,
            'output': 'json',
        }

        base = 'http://api.map.baidu.com/geocoder?'
        url = base + parse.urlencode(query)

        doc = urllib.request.urlopen(url)
        s = doc.read().decode('utf-8')
        try:
            jsonData = json.loads(s)
            lat = jsonData['result']['location']['lat']
            lng = jsonData['result']['location']['lng']
        except Exception as e:
            lat = 0.0
            lng = 0.0
        return lat, lng

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

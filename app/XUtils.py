#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import pprint, sys, re, os, os.path, xlrd, xlwt
import json
import urllib.request
from urllib import parse


class XUtils(object):
    G_DIGIT_DICT = {'零': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}

    @staticmethod
    def has_valid_lat_lng(p_address_dict=None):
        """

        :param p_address_dict:
        :return:
        """
        rst = False
        try:
            a = 1.0 / p_address_dict['经度']
            a = 1.0 / p_address_dict['纬度']
            rst = True
        except Exception as e:
            rst = False
        return rst

    @staticmethod
    def convert_chinese_numerals_2_arabic_numerals_for_dict(p_address_dict=None, p_key=None):
        p_str = p_address_dict[p_key]
        return XUtils.convert_chinese_numerals_2_arabic_numerals_4_str(p_str=p_str)

    @staticmethod
    def convert_chinese_numerals_2_arabic_numerals_4_str(p_str=None):
        """ 将汉字数字转换为阿拉伯数字

        :param p_str:
        :return:
        """
        result = ''
        for i in range(0, len(p_str)):
            tmp_char = p_str[i]
            if tmp_char in XUtils.G_DIGIT_DICT.keys():
                tmp_char = XUtils.G_DIGIT_DICT[tmp_char]
            result = result + str(tmp_char)
        return result

    @staticmethod
    def remove_noise_province_city_district(p_address_dict=None, p_key=None):
        """ 丢弃噪音数据
        比如省市县啥的， 就不应该参与比较， 这个没意义
        :param p_address_dict:
        :param p_key:
        :return:
        """
        province_name = p_address_dict['省份'] if p_address_dict['省份'] is not None else ''
        city_name = p_address_dict['城市'] if p_address_dict['城市'] is not None else ''
        district_name = p_address_dict['区/县'] if p_address_dict['区/县'] is not None else ''
        town_name = p_address_dict['乡'] if p_address_dict['乡'] is not None else ''
        # 去除噪音数据(省市县)
        s = p_address_dict[p_key]
        s = s.replace(province_name, '').replace(city_name, '').replace(district_name, '').replace(town_name, '')
        return s

    @staticmethod
    def remove_noise_empty_punctuation(p_address_dict=None, p_key=None):
        """ 丢弃噪音数据
        :param p_address_dict:
        :param p_key:
        :return:
        """
        #
        # 去除噪音数据(空格, 标点符号...)
        s = str(p_address_dict[p_key])
        s = XUtils.trim(s)
        s = XUtils.remove_punctuation(s)
        return s

    @staticmethod
    def remove_punctuation(text):
        """删除标点符号
        :param text:
        :return:
        """
        punctuation = '!,;:?"\''
        text = re.sub(r'[{}]+'.format(punctuation), '', text)
        return text.strip().lower()

    @staticmethod
    def trim(str):
        newstr = ''
        for ch in str:  # 遍历每一个字符串
            if ch != ' ':
                newstr = newstr + ch
        return newstr

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

    @staticmethod
    def fetch_all_mobiles(p_text=None):
        """
        :param p_text: 文本
        :return: 返回手机号列表
        """
        if p_text is None:
            mobiles = []
        else:
            mobiles = re.findall(r"1\d{10}", p_text)
        return mobiles

    @staticmethod
    def fetch_all_emails(p_text=None):
        """
        :param text: 文本
        :return: 返回电子邮件列表
        """
        if p_text is None:
            emails = []
        else:
            emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", p_text)
        return emails

    @staticmethod
    def fetch_all_urls(p_text=None):
        """
        :param text: 文本
        :return: 返回url列表
        """
        if p_text is None:
            urls = []
        else:
            urls = re.findall(r"(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)|([a-zA-Z]+.\w+\.+[a-zA-Z0-9\/_]+)", p_text)
            urls = list(sum(urls, ()))
            urls = [x for x in urls if x != '']
        return urls

    @staticmethod
    def fetch_all_ips(p_text=None):
        """
        :param text: 文本
        :return: 返回ip列表
        """
        if p_text is None:
            ips = []
        else:
            ips = re.findall(r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b", p_text)
        return ips

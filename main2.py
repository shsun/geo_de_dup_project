#!/usr/bin/env python
# -*- coding: utf-8 -*-
import warnings, datetime, pprint, sys, os, os.path, xlrd, xlwt

from app.GEODistanceStrategy import GEODistanceStrategy
from app.AddressStringDiffStrategy import AddressStringDiffStrategy
from app.LALPctStrategy import LALPctStrategy
from app.AddressCosineSimilarityStrategy import AddressCosineSimilarityStrategy
from app.XUtils import XUtils

from main_utils import fetch_max_length_item, contains

# sys.setdefaultencoding('utf8')
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

"""
1. 增量
"""


def main(p_args):
    start = datetime.datetime.now()

    excel_title = ['group_id', '序号', '地址编号', '省份', '城市', '区/县', '乡', '详细地址（拼接省市区）', '详细地址(PROD地址)', '经度', '纬度', '标准地址', '标准地址是否新地址']

    # 存量表2，该表示由main1.py生成的
    EXCEL_TABLE1 = './resources/receiving_address_group_by_1.xls'
    new_excel_dict_grouped = {}
    new_excel_list_grouped = XUtils.excel_to_list(p_read_excel_file_path=EXCEL_TABLE1,
                                                  p_sheet_name='Sheet1',
                                                  p_excel_title_list=excel_title)
    # 分组, 将同一组的元素放到一个list内, 形成一个dict, 该dict的key为group_id_value
    for tmp_dict in new_excel_list_grouped:
        group_id_value = tmp_dict['group_id']
        if group_id_value not in new_excel_dict_grouped.keys():
            new_excel_dict_grouped[group_id_value] = []
        new_excel_dict_grouped[group_id_value].append(tmp_dict)
    
    # 存量表3，该表示由main1.py生成的， 此步主要是希望算出最大的group_id(即有多少个group)
    EXCEL_TABLE1 = './resources/receiving_address_filtered_1.xls'
    old_excel_list = XUtils.excel_to_list(p_read_excel_file_path=EXCEL_TABLE1,
                                          p_sheet_name='Sheet1',
                                          p_excel_title_list=excel_title)
    group_id = len(old_excel_list)

    # 7. 读取增量excel(实际excel中就一条) 至 old_excel_list 中
    excel_title.remove('group_id')
    # NOTE 看过来
    # EXCEL_TABLE_INCREMENT = './resources/receiving_address_increment_1.xlsx'
    EXCEL_TABLE_INCREMENT = './resources/receiving_address_increment_1_ok.xls'
    old_excel_list = XUtils.excel_to_list(p_read_excel_file_path=EXCEL_TABLE_INCREMENT,
                                          p_sheet_name='Sheet1',
                                          p_excel_title_list=excel_title)
    print('\n增量数据条数 old_excel_list length=====>>%d\n' % (len(old_excel_list)))
    increment_list_match_success = []
    brother_in_table3_of_increment_list = []
    increment_list_match_failed = []
    should_create_new_group_4_increment = False
    excel_title.insert(0, 'group_id')
    for tmp_dict in old_excel_list:
        rst, brother_dict = contains(p_new_excel_list=new_excel_list_grouped, p_old_dict=tmp_dict)
        if rst is False:
            tmp_dict['标准地址'] = '匹配失败'

            group_id += 1
            tmp_dict['group_id'] = group_id

            # 需要进表2的数据
            new_excel_list_grouped.append(tmp_dict)
            # 建立小组
            new_excel_dict_grouped[str(group_id)] = []
            new_excel_dict_grouped[str(tmp_dict['group_id'])].append(tmp_dict)
            #
            increment_list_match_failed.append(tmp_dict)
            should_create_new_group_4_increment = True
        else:
            tmp_dict['标准地址'] = '匹配成功'
            tmp_dict['group_id'] = brother_dict['group_id']
            increment_list_match_success.append(tmp_dict)
            pass

    new_excel_list_filtered = []
    new_excel_dict_filtered = {}
    # Note 注意， 这个value是一个list
    for (key, value) in new_excel_dict_grouped.items():
        rst = fetch_max_length_item(p_excel_sub_list=value)
        new_excel_list_filtered.append(rst)
        new_excel_dict_filtered[rst['group_id']] = rst

    #
    for tmp_dict in increment_list_match_success:
        brother_in_table3 = new_excel_dict_filtered[tmp_dict['group_id']]
        brother_in_table3['标准地址是否新地址'] = '我是存量'
        # print('表三中对应的地址信息如下=====>>:')
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(brother_in_table3)
        brother_in_table3_of_increment_list.append(brother_in_table3)

    # TODO 最后100条测试数据，匹配成功的，看看能否将数据输出成Excel，就是，前几列信息匹配成功的增量数据，然后后几列是匹配到的表三数据
    print('\n增量匹配成功的数据条数 increment_list_match_success length=====>>%d\n' % (len(increment_list_match_success)))
    print('\n增量匹配成功的兄弟们 brother_in_table3_of_increment_list length=====>>%d\n' % (
        len(brother_in_table3_of_increment_list)))
    print('\n增量匹配失败的数据条数 increment_list_match_success length=====>>%d\n' % (len(increment_list_match_failed)))

    sorted_list = sorted(increment_list_match_success, key=lambda x: x['group_id'], reverse=False)
    XUtils.process_and_dump_2_excel(p_excel_title=excel_title, p_new_excel_list=sorted_list,
                                    p_new_file='./resources/receiving_address_increment_match_success.xls')

    sorted_list = sorted(brother_in_table3_of_increment_list, key=lambda x: x['group_id'], reverse=False)
    XUtils.process_and_dump_2_excel(p_excel_title=excel_title, p_new_excel_list=sorted_list,
                                    p_new_file='./resources/receiving_address_increment_brother_in_table3.xls')

    sorted_list = sorted(increment_list_match_failed, key=lambda x: x['group_id'], reverse=False)
    XUtils.process_and_dump_2_excel(p_excel_title=excel_title, p_new_excel_list=sorted_list,
                                    p_new_file='./resources/receiving_address_increment_match_failed.xls')
    #
    increment_list_match_success.extend(brother_in_table3_of_increment_list)
    sorted_list = sorted(increment_list_match_success, key=lambda x: x['group_id'], reverse=False)
    XUtils.process_and_dump_2_excel(p_excel_title=excel_title, p_new_excel_list=sorted_list,
                                    p_new_file='./resources/receiving_address_compare.xls')

    # 8. 对去重后的数据进行处理并写入excel
    if should_create_new_group_4_increment:
        sorted_list = sorted(new_excel_list_grouped, key=lambda x: x['group_id'], reverse=False)
        XUtils.process_and_dump_2_excel(p_excel_title=excel_title, p_new_excel_list=sorted_list,
                                        p_new_file='./resources/receiving_address_group_by_2.xls')
        sorted_list = sorted(new_excel_list_filtered, key=lambda x: x['group_id'], reverse=False)
        XUtils.process_and_dump_2_excel(p_excel_title=excel_title, p_new_excel_list=sorted_list,
                                        p_new_file='./resources/receiving_address_filtered_2.xls')

    end = datetime.datetime.now()
    print('\n\n----------------->增量耗时 cost time<-----------------')
    print(end - start)

    print('\n程序执行完毕 !!! DONE DONE DONE DONE DONE DONE DONE DONE DONE DONE DONE')
    return 0


if __name__ == '__main__':
    # NOTE 程序入口
    warnings.filterwarnings('ignore')

    rst = main(sys.argv)

    sys.exit(rst)

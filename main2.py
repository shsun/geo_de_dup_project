#!/usr/bin/env python
# -*- coding: utf-8 -*-
import warnings, datetime, pprint, sys, os, os.path, xlrd, xlwt

from app.XUtils import XUtils
from app.XConstants import XConstants
from main_utils import fetch_max_length_item, contains

# sys.setdefaultencoding('utf8')
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

"""
1. 增量
"""


def main(p_args):
    start = datetime.datetime.now()

    excel_title = ['group_id', '序号', '地址编号', '省份', '城市', '区/县', '乡', '详细地址（拼接省市区）', '详细地址(PROD地址)', '经度', '纬度', '标准地址', '标准地址是否新地址']

    # 存量表2，该表示由main1.py生成的 (标准地址库)
    EXCEL_TABLE1 = './resources/receiving_address_group_by_1.xls'
    new_excel_dict_grouped = {}
    new_excel_list_grouped = XUtils.excel_to_list(p_read_excel_file_path=EXCEL_TABLE1,
                                                  p_sheet_name='Sheet1',
                                                  p_excel_title_list=excel_title)
    # 分组, 将同一组的元素放到一个sub-list内, 形成一个dict, 该dict的key为group_id_value
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
    i = 0
    for tmp_dict in old_excel_list:
        i += 1
        rst, brother_dict, sim = contains(p_new_excel_list=new_excel_list_grouped, p_old_dict=tmp_dict)
        tmp_dict['sim'] = sim
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

        # 再加上一行判定标准, 这一行的sim值那里填上我们判定的beta(该系数可以调，初始值是0.6)
        dummy_dict = {}
        for tmp_title in excel_title:
            dummy_dict[tmp_title] = '0'
        dummy_dict['sim'] = XConstants.BETA

        # 表4
        # 生成表4
        # 表4就是标准地址库加上一列sim值
        # 再加上一行判定标准，这一行的sim值那里填上我们的判定值β0.6
        excel_title.insert(0, 'sim')
        sorted_list = sorted(new_excel_list_grouped, key=lambda x: x['sim'], reverse=True)
        sorted_list.insert(0, dummy_dict)
        XUtils.process_and_dump_2_excel(p_excel_title=excel_title, p_new_excel_list=sorted_list,
                                        p_new_file='./resources/table_%d_4.xls' % (i))
        # 表5
        # 对表4进行排序，sim值由大到小
        # 然后输出前十个数据加上0.6判定标准那行的数据. 这时我们有几种情况
        #
        # 1.    前十名都大于0.6，这时输出结果就是前10名在前十行，第十一行就是判定标准0.6那一行
        #
        # 2.    识别成功，前十名都是合格的，人工自己选择）
        #       前十名都小于0.6，这时输出结果就是第一行是判定标准0.6那一行，2到11行是前十名（这是就是认为匹配失败，前十名只能用做参考）
        #
        # 3.    前十名有一部分大于0.6，有一部分小于0.6，准确来说应该就9个地址吧，因为前十名包含了0.6，所以这时输出的就是大于0.6的是合格的，人工选择，小于0.6的不合格，只能参考
        #
        sorted_list.remove(dummy_dict)
        top_10 = sorted_list[:9]
        sorted_list = sorted(top_10, key=lambda x: x['sim'], reverse=True)

        # 我的意思是加一个Beta2 = 0.8，sim2 = (1 + sim) / 2



        # 1. 前十名都大于XConstants.BETA2_RED_LINE，这时输出结果就是前10名在前十行，第十一行就是判定标准0.6那一行
        # if sorted_list[-1] > XConstants.BETA:
        #     sorted_list.append(dummy_dict)


        sorted_list.insert(0, dummy_dict)
        sorted_list.insert(0, tmp_dict)
        
        XUtils.process_and_dump_2_excel(p_excel_title=excel_title, p_new_excel_list=sorted_list,
                                        p_new_file='./resources/table_%d_5.xls' % (i))
        excel_title.remove('sim')

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

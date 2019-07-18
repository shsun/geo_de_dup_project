#!/usr/bin/env python
# -*- coding: utf-8 -*-
import warnings, datetime, time, pprint, sys, os, os.path, xlrd, xlwt
from app.XUtils import XUtils
from main_utils import fetch_max_length_item, contains

# sys.setdefaultencoding('utf8')
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

"""
1. 存量
"""


def main(p_args):
    global g_contains_execute_times
    global g_contains_cost_time

    g_contains_execute_times = 0
    g_contains_cost_time = 0

    start = datetime.datetime.now()

    excel_title = ['序号', '地址编号', '省份', '城市', '区/县', '乡', '详细地址（拼接省市区）', '详细地址(PROD地址)', '经度', '纬度', '标准地址', '标准地址是否新地址']

    # 1. 读取地址信息 NOTE 看这里
    # EXCEL_TABLE1 = './resources/receiving_address_input_1.xlsx'
    EXCEL_TABLE1 = './resources/receiving_address_stock_1_ok.xls'
    old_excel_list = XUtils.excel_to_list(p_read_excel_file_path=EXCEL_TABLE1,
                                          p_sheet_name='Sheet1',
                                          p_excel_title_list=excel_title)
    old_len = len(old_excel_list)
    print('\n表1数据总条数old_excel_list length=====>>%d' % (old_len))
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
    print('\n经纬度数据有问题的数据条数  invalid data num======>>%d' % (err_num))
    print('\n真实参与处理的数据条数(即抛弃了非法数据后) old_excel_list length=====>> (%d - %d) = %d\n' % (
        old_len, err_num, len(old_excel_list)))

    # Note 3.
    # Note 总共生成两个表，算上原始表就有三个
    # Note 假如说第一个数据进来，直接就扔到第二个表里，给他一个编号1.第二个进来跟第一个比较，然后没匹配上扔到表2给他一个编号2.第三个进来了，跟前两个比较，
    # Note 假如说匹配到了1，我们给他也扔到表2里给编号1。。。这样的话表2就会有4636-150个数据，但是每一数据都有一个编号。然后在根据这个编号顺序排一下，这样就把相同的归在一起了
    # Note 这个是把相同/类似的地址 编一个相同的号，  相当于分组
    new_excel_dict_grouped = {}
    new_excel_list_grouped = []
    group_id = 0
    for tmp_dict in old_excel_list:

        time_start = time.time()
        rst, brother_dict, sim = contains(p_new_excel_list=new_excel_list_grouped, p_old_dict=tmp_dict)
        time_end = time.time()

        g_contains_execute_times += 1
        g_contains_cost_time += (time_end - time_start)

        if rst is False:
            group_id += 1
            # 建立小组
            new_excel_dict_grouped[str(group_id)] = []
            # Note 加一列数据group_id
            tmp_dict['group_id'] = group_id
        else:
            # Note 此处要非常注意， 应该使用它兄弟的group_id, 而不是使用最新的group_id
            tmp_dict['group_id'] = brother_dict['group_id']
        new_excel_list_grouped.append(tmp_dict)
        # Note 分组, 同一小组的记录具有相同group_id
        new_excel_dict_grouped[str(tmp_dict['group_id'])].append(tmp_dict)

    print('\n组数 group_id=====>>%d' % (group_id))
    print('\n分组后的新数据条数 new_excel_list_grouped length=====>>%d\n' % (len(new_excel_list_grouped)))

    # 4. 对分组后的数据进行处理并写入excel
    # Note 加一列标题group_id
    excel_title.insert(0, 'group_id')
    sorted_list = sorted(new_excel_list_grouped, key=lambda x: x['group_id'], reverse=False)
    XUtils.process_and_dump_2_excel(p_excel_title=excel_title, p_new_excel_list=sorted_list,
                                    p_new_file='./resources/receiving_address_group_by_1.xls')

    # Note 最重要的一步
    # Note 5. 去重, 将去重后的数据存入new_excel_list_filtered中
    # Note 对老数据循环, 挨个去和新数据内的所有数据逐个对比, 如果在new_list内找到了, 则认为是同一地址, 否则认为是不同地址, 不同地址则添加到new_excel_list内
    # Note 所以这里是两层循环
    # Note
    # Note 然后在生成表三，从表2中每一个重复标号的，选取详细地址最长字符的作为表3的地址
    new_excel_list_filtered = []
    new_excel_dict_filtered = {}
    # Note 注意， 这个value是一个list
    for (key, value) in new_excel_dict_grouped.items():
        rst = fetch_max_length_item(p_excel_sub_list=value)
        new_excel_list_filtered.append(rst)
        new_excel_dict_filtered[rst['group_id']] = rst

    print('\n去重后的新数据条数 new_excel_list_filtered length=====>>%d\n' % (len(new_excel_list_filtered)))

    # 6. 对去重后的数据进行处理并写入excel
    sorted_list = sorted(new_excel_list_filtered, key=lambda x: x['group_id'], reverse=False)
    XUtils.process_and_dump_2_excel(p_excel_title=excel_title, p_new_excel_list=sorted_list,
                                    p_new_file='./resources/receiving_address_filtered_1.xls')

    print('\n\n----------------->g_contains_cost_time<-----------------')
    print(g_contains_execute_times)
    print(g_contains_cost_time)
    print(g_contains_cost_time / g_contains_execute_times)

    end = datetime.datetime.now()
    print('\n\n----------------->增量耗时 cost time<-----------------')
    print(end - start)
    start = datetime.datetime.now()

    print('\n程序执行完毕 !!! DONE DONE DONE DONE DONE DONE DONE DONE DONE DONE DONE')
    return 0


if __name__ == '__main__':
    # NOTE 程序入口
    warnings.filterwarnings('ignore')

    rst = main(sys.argv)

    sys.exit(rst)

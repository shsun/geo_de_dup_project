#!/usr/bin/env python
# -*- coding: utf-8 -*-
import warnings, datetime, pprint, sys, os, os.path, xlrd, xlwt

from app.GEODistanceStrategy import GEODistanceStrategy
from app.AddressStringDiffStrategy import AddressStringDiffStrategy
from app.LALPctStrategy import LALPctStrategy
from app.AddressCosineSimilarityStrategy import AddressCosineSimilarityStrategy
from app.XUtils import XUtils

# sys.setdefaultencoding('utf8')
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


"""
1. 存量
"""


def fetch_max_length_item(p_excel_sub_list=None):
    # '详细地址（拼接省市区）'
    rst = None
    # 然后在生成表三，从表2中每一个重复标号的，选取详细地址最长字符的作为表3的地址
    max_len = 0
    for tmp_new_dict in p_excel_sub_list:
        tmp_len = len(tmp_new_dict['详细地址（拼接省市区）'])
        if tmp_len > max_len:
            max_len = tmp_len
            rst = tmp_new_dict
    return rst


def contains(p_new_excel_list=None, p_old_dict=None):
    """
    判断
    :param p_new_excel_list:
    :param p_old_dict:
    :return: rst为true的时候表示能够在p_new_excel_list找到兄弟节点， 否则找不到兄弟节点。 (所谓兄弟节点就是指着这2个点认为是同一个地址), brother_dict是p_old_dict的兄弟节点.
    """
    rst = False
    brother_dict = None
    for tmp_new_dict in p_new_excel_list:

        # Note 利用余弦相似度公式计算两字符串的相似性 (相似度达到0.8则认为是一个地址，否则是2个不同地址, 这个0.8我是随便写的, 可修改)
        # rst_cos_sim = CosineSimilarityStrategy().compare(p_address_dict_a=tmp_new_dict, p_address_dict_b=p_old_dict)

        # NOTE 通过对经纬度的比较，相差百分之一或更小以内的视为同一地址，否则视为两个地址
        # rst_lal = LALPctStrategy().compare(p_address_dict_a=tmp_new_dict, p_address_dict_b=p_old_dict)

        # Note 根据距离来判断(200米)
        match_distance, real_distance = GEODistanceStrategy().compare(p_address_dict_a=tmp_new_dict, p_address_dict_b=p_old_dict)

        # Note 计算字符匹配度
        # 详细地址（拼接省市区）匹配度; 详细地址(PROD地址) 匹配度
        rst_str_diff, sim_string = AddressStringDiffStrategy().compare(p_address_dict_a=tmp_new_dict, p_address_dict_b=p_old_dict)

        # Note 看这里 ................................... 加权系数, 可以调. 因为字符串匹配更优, 所以权重大一些, 此处需要人工去调
        FACTOR = 0.75

        # 计算根据距离算出来的相似度. 其中x是求大圆算出来的距离， 即2个点的真实距离
        x = real_distance
        b = (500 - x) / 500

        # a是字符串相似度, b是距离相似度
        a = sim_string
        sim = FACTOR * a + (1 - FACTOR) * b

        # rst = match_distance is True and rst_str_diff is True
        # NOTE 看这里  ...................... 此处也需要人为调整
        rst = sim >= 0.6

        if rst is True:
            brother_dict = tmp_new_dict
            break
    return rst, brother_dict


def main(p_args):
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
        rst, brother_dict = contains(p_new_excel_list=new_excel_list_grouped, p_old_dict=tmp_dict)
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

    end = datetime.datetime.now()
    print('\n\n----------------->存量耗时 cost time<-----------------')
    print(end - start)
    start = datetime.datetime.now()

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

#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import pymysql.cursors
import time
import sys
from app.XUtils import XUtils

G_DB_CONF = {'MYSQL_HOST': '47.99.118.183', 'MYSQL_USER': 'root', 'MYSQL_PASSWD': '', 'MYSQL_DB': 'db_sys', 'MYSQL_CHARSET': 'utf8mb4'}
G_DB_CONF['MYSQL_DB'] = None
# NOTE 数据库密码通过命令行参数传递过来， 以免泄露密码
if len(sys.argv) > 1:
    G_DB_CONF['MYSQL_PASSWD'] = sys.argv[1]


def fetch_last_one_record_by_time(p_alter_time_start: int = None, p_alter_time_end: int = None) -> (bool, list):
    """
    小表选取最后一个记录

    从小表中选取指定时间段的最后一条记录
    :return:
    """
    success = False
    rst = []
    global G_DB_CONF

    try:
        conn = pymysql.connect(host=G_DB_CONF['MYSQL_HOST'],
                               user=G_DB_CONF['MYSQL_USER'],
                               password=G_DB_CONF['MYSQL_PASSWD'],
                               db=G_DB_CONF['MYSQL_DB'],
                               charset=G_DB_CONF['MYSQL_CHARSET'],
                               cursorclass=pymysql.cursors.DictCursor)
        conn.autocommit(1)
        cursor = conn.cursor()
        #
        start_time = time.time()
        biz_params = (p_alter_time_start, p_alter_time_end)
        try:
            # FIXME 上面那个最原始的SQL报语法错误， 所以我删除了 and STATUS not in ('D']
            biz_sql = """
                        select * 
                        from (
                           select tab.*
                           from (
                           (select outbound_warehouse as outbound_warehouse,
                               order_number as order_number,
                               can_send_weight as can_send_weight,
                               can_send_number as can_send_number,
                               can_send_date as can_send_date,
                               momentum_number as momentum_number,
                               momentum_weight as momentum_weight,
                               commodity as commodity
                            from db_trans_plan.t_notice_stockinfo)
                            union
                           (SELECT s.DELIWAREHOUSE as outbound_warehouse,
                               s.ORITEMNUM as order_number,
                               s.CANSENDWEIGHT as can_send_weight,
                               s.CANSENDNUMBER as can_send_number,
                               s.AlTERTIME as can_send_date,
                               s.WAINTFORDELNUMBER as momentum_number,
                               s.WAINTFORDELWEIGHT as momentum_weight,
                               s.COMMODITYNAME as commodity
                            FROM(
                              SELECT *
                              FROM db_inter.bclp_can_be_send_amount_copy1 
                              where ALTERTIME>%s and ALTERTIME<%s
                              and STATUS not in ('D')) as s
                           ) )as tab
                           order by tab.can_send_date desc
                        )  t
                        group by t.outbound_warehouse,REPLACE(t.order_number,'-','')
                    """
            cursor.execute(biz_sql, biz_params)
            # r = cursor.fetchone()
            results = cursor.fetchall()
            if results is not None:
                for r in results:
                    tmp_record = dict()
                    tmp_record['outbound_warehouse'] = r.get('outbound_warehouse')
                    tmp_record['order_number'] = r.get('order_number')
                    tmp_record['can_send_weight'] = r.get('can_send_weight')
                    tmp_record['can_send_number'] = r.get('can_send_number')
                    tmp_record['can_send_date'] = r.get('can_send_date')
                    tmp_record['momentum_number'] = r.get('momentum_number')
                    tmp_record['momentum_weight'] = r.get('momentum_weight')
                    tmp_record['commodity'] = r.get('commodity')
                    rst.append(tmp_record)
                success = True
            else:
                success = False
        except Exception as e:
            print('exception %s' % (str(e)), file=sys.stderr)
            success = False

        end_time = time.time()
        print('======spend time: %s' % (round(end_time - start_time, 2)))

        cursor.close()
    except Exception as e:
        print('exception %s' % (str(e)), file=sys.stderr)
        success = False

    return success, rst


def update_inventory_table_by(p_new_value_dict={}):
    """
    更新大表
    :return:
    """
    try:
        conn = pymysql.connect(host=G_DB_CONF['MYSQL_HOST'],
                               user=G_DB_CONF['MYSQL_USER'],
                               password=G_DB_CONF['MYSQL_PASSWD'],
                               db=G_DB_CONF['MYSQL_DB'],
                               charset=G_DB_CONF['MYSQL_CHARSET'],
                               cursorclass=pymysql.cursors.DictCursor)
        conn.autocommit(1)
        cursor = conn.cursor()
        #
        """
        小表列的含义，
        
        DELIWAREHOUSE 仓库名，
        ORITEMNUM 订单号（就是相当于刚刚的品种），
        
        CANSENDWEIGHT 可发重量，
        CANSENDNUMBER 可发数量，
        WAINTFORDELNUMBER 待发数量
        WAINTFORDELWEIGHT 待发重量（相当于库存）
        
        这四个字段(可发两个待发两个)直接覆盖大表
        
        仓库名与订单号是要匹配的
        """

        # 大表的订单号没有中间的-，小表的ORITEMNUM订单号有一个-
        new_oritemnum = (p_new_value_dict['ORITEMNUM']).replace('-', '')
        # NOTE
        biz_params = (p_new_value_dict['CANSENDWEIGHT'],
                      p_new_value_dict['CANSENDNUMBER'],
                      p_new_value_dict['WAINTFORDELNUMBER'],
                      p_new_value_dict['WAINTFORDELWEIGHT'],
                      p_new_value_dict['DELIWAREHOUSE'],
                      new_oritemnum)

        biz_sql = """
                    update 
                    db_trans_plan 
                    set 
                    CANSENDWEIGHT=%s, 
                    CANSENDNUMBER=%s,
                    WAINTFORDELNUMBER=%s, 
                    WAINTFORDELWEIGHT=%s 
                    where 
                    1=1 and
                    DELIWAREHOUSE=%s and
                    ORITEMNUM=%s
                    """
        # cursor.execute(biz_sql, biz_params)
        cursor.close()
    except Exception as e:
        print('exception %s' % (str(e)), file=sys.stderr)


def main(p_args):
    success, list = fetch_last_one_record_by_time(p_alter_time_start=20190702080000, p_alter_time_end=20190702150000)
    excel_title = ['outbound_warehouse', 'order_number', 'can_send_weight', 'can_send_number', 'can_send_date', 'momentum_number', 'momentum_weight', 'commodity']
    XUtils.process_and_dump_2_excel(p_excel_title=excel_title, p_new_excel_list=list,
                                    p_new_file='./resources/snapshot.xls')

    EXCEL_TABLE1 = './resources/snapshot.xls'
    old_excel_list = XUtils.excel_to_list(p_read_excel_file_path=EXCEL_TABLE1,
                                          p_sheet_name='Sheet1',
                                          p_excel_title_list=excel_title)

    # if success:
    #     update_inventory_table_by(p_new_value_dict=record)

    return 0


if __name__ == '__main__':
    # NOTE 程序入口
    sys.exit(main(sys.argv))

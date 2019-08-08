#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import pymysql.cursors
import time
import sys
import random

# FIXME 需要修改一下这些用户密码啥的
G_DB_CONF = {'MYSQL_HOST': '127.0.0.1', 'MYSQL_USER': 'root', 'MYSQL_PASSWD': '123456', 'MYSQL_DB': 'db_name??????????', 'MYSQL_CHARSET': 'utf8mb4'}


def fetch_last_one_record_by_time(p_alter_time_start=None, p_alter_time_end=None):
    """
    小表选取最后一个记录

    从小表中选取指定时间段的最后一条记录
    :return:
    """
    success = False
    rst = {}
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
            # NOTE 小表选取最后一个记录
            biz_sql = """
                            SELECT  s.DELIWAREHOUSE as DELIWAREHOUSE,
                            s.ORITEMNUM as ORITEMNUM,
                             s.CANSENDWEIGHT as CANSENDWEIGHT,
                            s.CANSENDNUMBER as CANSENDNUMBER,
                             s.AlTERTIME as ALTERTIME,
                             s.WAINTFORDELNUMBER as WAINTFORDELNUMBER,
                             s.WAINTFORDELWEIGHT as WAINTFORDELWEIGHT
                        FROM(SELECT *
                        FROM db_inter.bclp_can_be_send_amount_copy1 s
                        where ALTERTIME>%s and ALTERTIME<%s
                        and STATUS not in ('D']
                        order by ALTERTIME desc) as s
                        GROUP BY s.ORITEMNUM, s.DELIWAREHOUSE
                    """
            cursor.execute(biz_sql, biz_params)
            r = cursor.fetchone()
            if r is not None:
                rst['DELIWAREHOUSE'] = r.get('DELIWAREHOUSE')
                rst['ORITEMNUM'] = r.get('ORITEMNUM')
                rst['CANSENDWEIGHT'] = r.get('CANSENDWEIGHT')
                rst['CANSENDNUMBER'] = r.get('CANSENDNUMBER')
                rst['ALTERTIME'] = r.get('ALTERTIME')
                rst['WAINTFORDELNUMBER'] = r.get('WAINTFORDELNUMBER')
                rst['WAINTFORDELWEIGHT'] = r.get('WAINTFORDELWEIGHT')
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
        # NOTE
        biz_params = (p_new_value_dict['CANSENDWEIGHT'],
                      p_new_value_dict['CANSENDNUMBER'],
                      p_new_value_dict['WAINTFORDELNUMBER'],
                      p_new_value_dict['WAINTFORDELWEIGHT'],
                      p_new_value_dict['DELIWAREHOUSE'],
                      p_new_value_dict['ORITEMNUM'])

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
        cursor.execute(biz_sql, biz_params)
        cursor.close()
    except Exception as e:
        print('exception %s' % (str(e)), file=sys.stderr)


def main(p_args):
    success, record = fetch_last_one_record_by_time(p_alter_time_start=20190702080000, p_alter_time_end=20190702150000)
    if success:
        update_inventory_table_by(p_new_value_dict=record)

    return 0


if __name__ == '__main__':
    # NOTE 程序入口
    sys.exit(main(sys.argv))

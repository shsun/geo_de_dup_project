# !/usr/bin/python
# -*- coding: UTF-8 -*-

class XFictitiousSnatchBillMark(object):
    """

    开发服构建虚拟历史抢单表 db_inter.fictitious_snatch_bill_mark
    需要提供抢单成功的与流单的数据，包括流向（省市区），大品种，总价格，总重量，单价=总价格/总重量，抢单总时长，抢单的初始总价，抢单成功时的在线人数
    如果包含两个大品种则需要按照两个大品种的重量总价格记录为两条数据

    """

    def __init__(self, p_historical_avg_unit_price_of_last_month=None, p_theoryUPDefaultCalculateStrategy=None):
        """

        :param p_line:
        :param p_date:
        """
        # super(XOriginUPAbstractCalculateStrategy, self).__init__()
        pass

    def calculate(self):
        """

        :return:
        """
        return 1

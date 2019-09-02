# !/usr/bin/python
# -*- coding: UTF-8 -*-

class XFictitiousUnitPrice(object):
    """

    虚拟单价表db_inter.fictitious_unit_price

    需要提供，每个区对应八个大品种的单价信息，元每吨CNY / t，需要一个变化范围与均值（或最大分布）（小品种直接匹配?）

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

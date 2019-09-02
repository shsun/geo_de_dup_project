#!/usr/bin/python
# -*- coding: UTF-8 -*-


from app.grab.up_calculate_strategy.origin.XOriginalUPDefaultCalculateStrategy import XOriginalUPDefaultCalculateStrategy
from app.grab.up_calculate_strategy.theory.XTheoryUPDefaultCalculateStrategy import XTheoryUPDefaultCalculateStrategy


class XUPDescriptor(object):
    # 过去一个月某流向上的某产品的均价
    # select average(unit_price) from table where 1 = 1 and route = 1 and goods_category_id = 1
    historical_unit_price_of_last_month = -1
    # origin Unit Price被我限制了一下上下限问题，不让它超过一个上下限
    min_unit_price_of_last_month = -1
    max_unit_price_of_last_month = -1

    # 合理单价(理论单价是我心理能接受的最高成交价格), 就是我这次抢单过程中我理论上应该再这个价格停止。 暂时认为是一个固定数字100，后续有具体的算法求该值 = 100
    # Origin Total Price <= Theory Unit Price 这个关系
    theoryUPDefaultCalculateStrategy = None

    # 抢单过程的实际出价(起始价格), 然后每四分钟提高一点点, 每次增加历史单价的2%
    # 理论单价是我这次预期的成交价格, 但我不能一开始就定价定成它
    # 所以我现在要定一个稍微低一点的价格, 这样有可能我会以更低的价格出手
    # 然后我每次加价是历史单价的百分之3
    # 我期望是在第2次也就是加价6%时成交, 这样我初始单价就设置成理论成交价减去历史价的6%
    originUPCalculateStrategy = None

    def __init__(self, p_line=None, p_date=None):
        """

        :param p_line:
        :param p_date:
        """
        #
        self.historical_unit_price_of_last_month = -1
        self.min_unit_price_of_last_month = self.historical_unit_price_of_last_month * 1.00
        self.max_unit_price_of_last_month = self.historical_unit_price_of_last_month * 1.25
        #
        self.originUPCalculateStrategy = XOriginalUPDefaultCalculateStrategy()
        self.theoryUPDefaultCalculateStrategy = XTheoryUPDefaultCalculateStrategy()

    def toString(self):
        # self.originUP = self.originUPCalculateStrategy.calculate()

        return ''

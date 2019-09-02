#!/usr/bin/python
# -*- coding: UTF-8 -*-

from app.grab.up_calculate_strategy.origin.XOriginUPAbstractCalculateStrategy import XOriginUPAbstractCalculateStrategy


class XOriginalUPDefaultCalculateStrategy(XOriginUPAbstractCalculateStrategy):
    order = -1

    def __init__(self, p_line=None, p_date=None):
        """

        :param p_line:
        :param p_date:
        """
        super(XOriginUPAbstractCalculateStrategy, self).__init__()

        pass

    def calculate(self):
        """

        :return:
        """


        """
        
        
// 其现实意义是啥???
// 理论单价是我这次预期的成交价格, 但我不能一开始就定价定成它
// 所以我现在要定一个稍微低一点的价格, 这样有可能我会以更低的价格出手
// 然后我每次加价是历史单价的百分之3
// 我期望是在第2次也就是加价6%时成交, 这样我初始单价就设置成理论成交价减去历史价的6%
tmp = max( (theory_unit_price + historical_avg_unit_price_of_last_month)/2, theory_unit_price - historical_avg_unit_price_of_last_month * 0.06)
origin_unit_price = min( tmp, historical_avg_unit_price_of_last_month * 1.10)

        """

        return 100

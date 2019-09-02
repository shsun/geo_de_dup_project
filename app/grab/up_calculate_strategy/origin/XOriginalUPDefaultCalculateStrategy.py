#!/usr/bin/python
# -*- coding: UTF-8 -*-

from app.grab.up_calculate_strategy.origin.XOriginUPAbstractCalculateStrategy import XOriginUPAbstractCalculateStrategy
from app.grab.up_calculate_strategy.theory.XTheoryUPAbstractCalculateStrategy import XTheoryUPAbstractCalculateStrategy
from app.grab.up_calculate_strategy.theory.XTheoryUPDefaultCalculateStrategy import XTheoryUPDefaultCalculateStrategy


class XOriginalUPDefaultCalculateStrategy(XOriginUPAbstractCalculateStrategy):
    """
    理论单价是我这次预期的成交价格, 但我不能一开始就定价定成它
    所以我现在要定一个稍微低一点的价格, 这样有可能我会以更低的价格出手
    然后我每次加价是历史单价的百分之3
    我期望是在第2次也就是加价6%时成交, 这样我初始单价就设置成理论成交价减去历史价的6%
    tmp = max( (theory_unit_price + historical_avg_unit_price_of_last_month)/2, theory_unit_price - historical_avg_unit_price_of_last_month * 0.06)
    origin_unit_price = min( tmp, historical_avg_unit_price_of_last_month * 1.10)
    """
    #
    theoryUPDefaultCalculateStrategy = None
    #
    historical_avg_unit_price_of_last_month = -1

    def __init__(self, p_historical_avg_unit_price_of_last_month=None, p_theory_unit_price=None):
        """

        :param p_line:
        :param p_date:
        """
        super(XOriginUPAbstractCalculateStrategy, self).__init__()

        self.historical_avg_unit_price_of_last_month = p_historical_avg_unit_price_of_last_month
        self.theoryUPDefaultCalculateStrategy = XTheoryUPAbstractCalculateStrategy()

    def calculate(self):
        """

        :return:
        """
        theory_unit_price = self.theoryUPDefaultCalculateStrategy.calculate()
        tmp = max((theory_unit_price + self.historical_avg_unit_price_of_last_month) / 2, theory_unit_price - self.historical_avg_unit_price_of_last_month * 0.06)
        origin_unit_price = min(tmp, self.historical_avg_unit_price_of_last_month * 1.10)
        return origin_unit_price

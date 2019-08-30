#!/usr/bin/python
# -*- coding: UTF-8 -*-


from app.grab.origin_up_calculate_strategy.XOriginUPAbstractCalculateStrategy import XOriginUPAbstractCalculateStrategy
from app.grab.origin_up_calculate_strategy.XOriginalUPDefaultCalculateStrategy import XOriginalUPDefaultCalculateStrategy


class XUPDescriptor(object):
    #
    historical_unit_price_of_last_month = -1

    min_unit_price_of_last_month = -1
    max_unit_price_of_last_month = -1

    originUPCalculateStrategy = None

    def __init__(self, p_line=None, p_date=None):
        """

        :param p_line:
        :param p_date:
        """
        self.setOriginalUPCalculateStrategy(XOriginalUPDefaultCalculateStrategy())
        #
        self.historical_unit_price_of_last_month = -1
        self.min_unit_price_of_last_month = self.historical_unit_price_of_last_month
        self.max_unit_price_of_last_month = self.historical_unit_price_of_last_month * 1.10

    def setOriginalUPCalculateStrategy(self, p_originUPCalculateStrategy=None):
        """

        :param p_originUPCalculateStrategy:
        :return:
        """
        self.originUPCalculateStrategy = p_originUPCalculateStrategy

    def toString(self):
        # self.originUP = self.originUPCalculateStrategy.calculate()

        return ''

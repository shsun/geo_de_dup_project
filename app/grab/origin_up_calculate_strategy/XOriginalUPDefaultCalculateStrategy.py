#!/usr/bin/python
# -*- coding: UTF-8 -*-

from app.grab.origin_up_calculate_strategy.XOriginUPAbstractCalculateStrategy import XOriginUPAbstractCalculateStrategy


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
        return 100

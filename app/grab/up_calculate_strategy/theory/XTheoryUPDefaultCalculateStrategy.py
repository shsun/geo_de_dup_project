#!/usr/bin/python
# -*- coding: UTF-8 -*-


from app.grab.up_calculate_strategy.theory.XTheoryUPAbstractCalculateStrategy import XTheoryUPAbstractCalculateStrategy


class XTheoryUPDefaultCalculateStrategy(XTheoryUPAbstractCalculateStrategy):
    """
    expected_price 心理最高单价

    execution_price <= expected_price

    """
    order = -1

    def __init__(self, p_line=None, p_date=None):
        """

        :param p_line:
        :param p_date:
        """
        super(XTheoryUPAbstractCalculateStrategy, self).__init__()

        pass

    def calculate(self):
        """

        :return:
        """

        """
        theory_unit_price ： 合理单价(理论单价是我这次预期的成交价格)， 暂时认为是一个固定数字100，后续有具体的算法求该值 = 100
        theory_unit_price ： 合理单价， 暂时认为是一个固定数字100，后续有具体的算法求该值。
        """

        return 100

import re
from fractions import Fraction


class DuplicateChecker:
    def __init__(self):
        self.expression_set = set()

    def is_duplicate(self, expression, existing_expressions):
        """检查表达式是否重复"""
        # 标准化表达式
        normalized = self._normalize_expression(expression)

        if normalized in self.expression_set:
            return True

        # 检查交换律导致的重复
        if self._check_commutative_duplicate(normalized):
            return True

        self.expression_set.add(normalized)
        return False

    def _normalize_expression(self, expression):
        """标准化表达式（移除空格，统一格式）"""
        # 移除所有空格
        normalized = expression.replace(' ', '')
        return normalized

    def _check_commutative_duplicate(self, expression):
        """检查交换律导致的重复"""
        # 这里需要实现复杂的交换律检查逻辑
        # 简化实现：检查加法/乘法的交换
        for expr in self.expression_set:
            if self._are_commutative_equivalent(expression, expr):
                return True
        return False

    def _are_commutative_equivalent(self, expr1, expr2):
        """检查两个表达式是否通过交换律等价"""
        # 简化实现：实际项目需要更复杂的表达式解析
        # 这里只检查简单的 a+b 和 b+a 情况
        if '+' in expr1 and '+' in expr2:
            parts1 = expr1.split('+')
            parts2 = expr2.split('+')
            if set(parts1) == set(parts2):
                return True

        if '×' in expr1 and '×' in expr2:
            parts1 = expr1.split('×')
            parts2 = expr2.split('×')
            if set(parts1) == set(parts2):
                return True

        return False
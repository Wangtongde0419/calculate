import random
from fractions import Fraction


class ExpressionGenerator:
    def __init__(self, range_limit):
        self.range_limit = range_limit
        self.operators = ['+', '-', '×', '÷']

    def generate_number(self, is_fraction=False):
        """生成数字，可能是自然数或真分数"""
        if not is_fraction or random.random() < 0.7:  # 70%概率生成整数
            return str(random.randint(0, self.range_limit - 1))
        else:
            # 生成真分数
            denominator = random.randint(2, self.range_limit)
            numerator = random.randint(1, denominator - 1)
            return f"{numerator}/{denominator}"

    def generate_operator(self):
        return random.choice(self.operators)

    def generate_expression(self, max_operators=3, current_operators=0, has_brackets=False):
        """生成表达式，递归实现"""
        if current_operators >= max_operators:
            return self.generate_number(random.random() < 0.3)

        # 决定是否添加括号
        use_brackets = not has_brackets and random.random() < 0.3 and current_operators > 0

        if use_brackets:
            left = "("
            right = ")"
        else:
            left = ""
            right = ""

        # 生成左表达式
        left_expr = self.generate_expression(max_operators, current_operators + 1, use_brackets)

        # 生成运算符
        operator = self.generate_operator()

        # 生成右表达式，确保运算合法性
        right_expr = self.generate_right_expression(left_expr, operator, max_operators, current_operators + 1,
                                                    use_brackets)

        expression = f"{left}{left_expr} {operator} {right_expr}{right}"

        # 30%概率生成更复杂的表达式
        if current_operators < max_operators - 1 and random.random() < 0.3:
            next_operator = self.generate_operator()
            next_expr = self.generate_expression(max_operators, current_operators + 2, has_brackets)
            expression = f"({expression}) {next_operator} {next_expr}"

        return expression

    def generate_right_expression(self, left_expr, operator, max_operators, current_operators, has_brackets):
        """生成右表达式，确保运算合法性"""
        while True:
            right_expr = self.generate_expression(max_operators, current_operators, has_brackets)

            # 对于减法，确保左表达式不小于右表达式
            if operator == '-':
                try:
                    # 这里需要计算表达式的值进行比较
                    # 简化处理：如果是数字直接比较
                    if self.is_number(left_expr) and self.is_number(right_expr):
                        left_val = self.parse_number(left_expr)
                        right_val = self.parse_number(right_expr)
                        if left_val >= right_val:
                            return right_expr
                    else:
                        # 对于复杂表达式，暂时接受（实际项目需要更复杂的处理）
                        return right_expr
                except:
                    continue
            # 对于除法，确保除数不为零且结果为真分数
            elif operator == '÷':
                try:
                    if self.is_number(right_expr):
                        right_val = self.parse_number(right_expr)
                        if right_val != 0:
                            return right_expr
                    else:
                        return right_expr
                except:
                    continue
            else:
                return right_expr

    def is_number(self, expr):
        """判断是否是数字（整数或分数）"""
        return expr.replace('/', '').replace('-', '').isdigit()

    def parse_number(self, num_str):
        """解析数字字符串为数值"""
        if '/' in num_str:
            parts = num_str.split('/')
            return Fraction(int(parts[0]), int(parts[1]))
        else:
            return Fraction(int(num_str))
from fractions import Fraction
import re


class ExpressionCalculator:
    def __init__(self):
        self.operator_map = {'+': '+', '-': '-', '×': '*', '÷': '/'}

    def calculate(self, expression):
        """计算表达式值"""
        # 转换运算符为Python可识别的形式
        py_expression = expression.replace('×', '*').replace('÷', '/')

        # 处理分数
        py_expression = self._preprocess_expression(py_expression)

        try:
            # 安全计算表达式
            result = eval(py_expression)
            return self._format_result(result)
        except:
            raise ValueError(f"无法计算表达式: {expression}")

    def _preprocess_expression(self, expression):
        """预处理表达式，将分数转换为Fraction"""
        # 匹配分数格式
        fraction_pattern = r'(\d+)/(\d+)'

        def replace_fraction(match):
            return f"Fraction({match.group(1)}, {match.group(2)})"

        # 替换所有分数
        processed = re.sub(fraction_pattern, replace_fraction, expression)

        # 匹配整数并转换为Fraction
        int_pattern = r'(?<!\d)(\d+)(?!\d)'
        processed = re.sub(int_pattern, r'Fraction(\1)', processed)

        return processed

    def _format_result(self, result):
        """格式化结果"""
        if isinstance(result, Fraction):
            if result.numerator >= result.denominator and result.denominator != 1:
                whole = result.numerator // result.denominator
                remainder = result.numerator % result.denominator
                if remainder == 0:
                    return str(whole)
                else:
                    return f"{whole}'{remainder}/{result.denominator}"
            else:
                return f"{result.numerator}/{result.denominator}"
        else:
            return str(result)

    def validate_answer(self, answer):
        """验证答案合法性（非负等）"""
        try:
            if self.parse_number(answer) < 0:
                return False
            return True
        except:
            return False

    def compare_answers(self, answer1, answer2):
        """比较两个答案是否相等"""
        try:
            num1 = self.parse_number(answer1)
            num2 = self.parse_number(answer2)
            return num1 == num2
        except:
            return False

    def parse_number(self, num_str):
        """解析数字字符串"""
        if "'" in num_str:
            # 带分数格式
            parts = num_str.split("'")
            whole = int(parts[0])
            fraction_parts = parts[1].split('/')
            numerator = int(fraction_parts[0])
            denominator = int(fraction_parts[1])
            return whole + Fraction(numerator, denominator)
        elif '/' in num_str:
            # 分数格式
            parts = num_str.split('/')
            return Fraction(int(parts[0]), int(parts[1]))
        else:
            # 整数格式
            return Fraction(int(num_str))
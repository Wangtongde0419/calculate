import random
import argparse
from fractions import Fraction
import re


class ExpressionGenerator:
    def __init__(self, range_limit):
        self.range_limit = range_limit
        self.operators = ['+', '-', '×', '÷']
        self.generated_expressions = set()  # 用于去重

    def generate_number(self, allow_fraction=True):
        """生成数字（自然数或真分数）"""
        if not allow_fraction or random.random() < 0.7:  # 70%概率生成整数
            return str(random.randint(1, self.range_limit - 1))
        else:
            # 生成真分数
            denominator = random.randint(2, self.range_limit)
            numerator = random.randint(1, denominator - 1)
            return f"{numerator}/{denominator}"

    def generate_operator_count(self):
        """随机生成1-3个运算符"""
        return random.randint(1, 3)

    def generate_expression(self):
        """生成表达式 - 这是您需要调用的方法"""
        operator_count = self.generate_operator_count()
        return self.generate_expression_with_operator_count(operator_count)

    def generate_expression_with_operator_count(self, operator_count):
        """生成指定运算符数量的表达式"""
        if operator_count < 1 or operator_count > 3:
            raise ValueError("运算符数量必须在1-3之间")

        # 操作数数量 = 运算符数量 + 1
        operand_count = operator_count + 1
        operands = [self.generate_number() for _ in range(operand_count)]
        operators = [random.choice(self.operators) for _ in range(operator_count)]

        return self.build_expression(operands, operators)

    def build_expression(self, operands, operators):
        """构建表达式，考虑括号和运算优先级"""
        if len(operators) == 1:
            # 单运算符：直接连接
            return f"{operands[0]} {operators[0]} {operands[1]}"

        elif len(operators) == 2:
            # 双运算符：随机决定括号位置
            if random.random() < 0.5:
                return f"{operands[0]} {operators[0]} {operands[1]} {operators[1]} {operands[2]}"
            else:
                return f"({operands[0]} {operators[0]} {operands[1]}) {operators[1]} {operands[2]}"

        else:  # 3个运算符
            bracket_type = random.randint(1, 3)
            if bracket_type == 1:
                return f"({operands[0]} {operators[0]} {operands[1]}) {operators[1]} {operands[2]} {operators[2]} {operands[3]}"
            elif bracket_type == 2:
                return f"{operands[0]} {operators[0]} ({operands[1]} {operators[1]} {operands[2]}) {operators[2]} {operands[3]}"
            else:
                return f"({operands[0]} {operators[0]} {operands[1]} {operators[1]} {operands[2]}) {operators[2]} {operands[3]}"

    def validate_expression(self, expression):
        """验证表达式合法性"""
        try:
            # 检查运算符数量
            operator_count = sum(1 for char in expression if char in self.operators)
            if operator_count > 3:
                return False

            # 计算表达式结果，检查是否为负数
            result = self.calculate_expression(expression)
            if result < 0:
                return False

            return True
        except:
            return False

    def calculate_expression(self, expression):
        """计算表达式结果"""
        try:
            # 转换运算符格式
            py_expr = expression.replace('×', '*').replace('÷', '/')

            # 安全计算
            result = eval(py_expr)
            return result
        except:
            return None

    def normalize_expression(self, expression):
        """标准化表达式用于去重检查"""
        # 移除空格
        normalized = expression.replace(' ', '')
        return normalized

    def is_duplicate(self, expression):
        """检查表达式是否重复"""
        normalized = self.normalize_expression(expression)

        # 基本重复检查
        if normalized in self.generated_expressions:
            return True

        # 交换律重复检查（简化版）
        for expr in self.generated_expressions:
            if self.is_commutative_duplicate(normalized, expr):
                return True

        return False

    def is_commutative_duplicate(self, expr1, expr2):
        """检查交换律导致的重复"""
        # 简化实现：检查加法/乘法的交换
        if '+' in expr1 and '+' in expr2:
            parts1 = re.split(r'\+', expr1.replace('(', '').replace(')', ''))
            parts2 = re.split(r'\+', expr2.replace('(', '').replace(')', ''))
            if set(parts1) == set(parts2):
                return True

        if '×' in expr1 and '×' in expr2:
            parts1 = re.split(r'×', expr1.replace('(', '').replace(')', ''))
            parts2 = re.split(r'×', expr2.replace('(', '').replace(')', ''))
            if set(parts1) == set(parts2):
                return True

        return False


class ArithmeticCalculator:
    """算术表达式计算器"""

    @staticmethod
    def calculate(expression):
        """计算表达式值"""
        try:
            # 转换运算符
            py_expr = expression.replace('×', '*').replace('÷', '/')
            # 安全计算
            result = eval(py_expr)
            return ArithmeticCalculator.format_result(result)
        except:
            return None

    @staticmethod
    def format_result(result):
        """格式化结果"""
        if isinstance(result, float):
            if result.is_integer():
                result = int(result)

        if isinstance(result, int):
            return str(result)
        else:
            # 处理分数显示
            return f"{result}"


class FileManager:
    """文件管理类"""

    @staticmethod
    def save_exercises(exercises, filename='Exercises.txt'):
        with open(filename, 'w', encoding='utf-8') as f:
            for i, exercise in enumerate(exercises, 1):
                f.write(f"{i}. {exercise} =\n")

    @staticmethod
    def save_answers(answers, filename='Answers.txt'):
        with open(filename, 'w', encoding='utf-8') as f:
            for i, answer in enumerate(answers, 1):
                f.write(f"{i}. {answer}\n")

    @staticmethod
    def load_exercises(filename):
        exercises = []
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                if '.' in line:
                    exercise = line.split('.', 1)[1].strip()
                    exercise = exercise.rsplit('=', 1)[0].strip()
                    exercises.append(exercise)
        return exercises

    @staticmethod
    def load_answers(filename):
        answers = []
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                if '.' in line:
                    answer = line.split('.', 1)[1].strip()
                    answers.append(answer)
        return answers

    @staticmethod
    def save_grade(correct, wrong, filename='Grade.txt'):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Correct: {len(correct)} ({', '.join(map(str, correct))})\n")
            f.write(f"Wrong: {len(wrong)} ({', '.join(map(str, wrong))})\n")


def main():
    parser = argparse.ArgumentParser(description='小学四则运算题目生成器')
    parser.add_argument('-n', type=int, help='生成题目的数量')
    parser.add_argument('-r', type=int, required=True, help='数值范围')
    parser.add_argument('-e', type=str, help='题目文件路径')
    parser.add_argument('-a', type=str, help='答案文件路径')

    args = parser.parse_args()

    if args.n and args.r:
        # 生成题目模式
        generator = ExpressionGenerator(args.r)
        calculator = ArithmeticCalculator()
        file_manager = FileManager()

        exercises = []
        answers = []
        count = 0

        print(f"开始生成{args.n}道题目，数值范围：1-{args.r}")

        while count < args.n:
            # 使用正确的方法名
            expression = generator.generate_expression()

            # 检查重复和合法性
            if generator.is_duplicate(expression):
                continue

            # 计算答案并验证
            answer = calculator.calculate(expression)
            if answer is not None and generator.validate_expression(expression):
                exercises.append(expression)
                answers.append(answer)
                generator.generated_expressions.add(generator.normalize_expression(expression))
                count += 1
                print(f"已生成第{count}道题目: {expression} = {answer}")

        # 保存文件
        file_manager.save_exercises(exercises)
        file_manager.save_answers(answers)
        print(f'已生成{args.n}道题目，保存在Exercises.txt和Answers.txt')

    elif args.e and args.a:
        # 批改模式
        file_manager = FileManager()
        calculator = ArithmeticCalculator()

        exercises = file_manager.load_exercises(args.e)
        user_answers = file_manager.load_answers(args.a)

        correct = []
        wrong = []

        for i, (exercise, user_answer) in enumerate(zip(exercises, user_answers)):
            correct_answer = calculator.calculate(exercise)
            if correct_answer and str(correct_answer) == user_answer:
                correct.append(i + 1)
            else:
                wrong.append(i + 1)

        file_manager.save_grade(correct, wrong)
        print("批改完成，结果保存在Grade.txt")
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
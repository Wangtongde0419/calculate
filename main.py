import random
import argparse
from fractions import Fraction
import re


class ExpressionGenerator:
    def __init__(self, range_limit):
        self.range_limit = range_limit
        self.operators = ['+', '-', '×', '÷']
        self.generated_expressions = set()

    def generate_number(self, allow_fraction=True):
        if not allow_fraction or random.random() < 0.7:
            return str(random.randint(1, self.range_limit - 1))
        else:
            denominator = random.randint(2, self.range_limit)
            numerator = random.randint(1, denominator - 1)
            return f"{numerator}/{denominator}"

    def generate_operator_count(self):
        return random.randint(1, 3)

    def generate_expression(self):
        operator_count = self.generate_operator_count()
        return self.generate_expression_with_operator_count(operator_count)

    def generate_expression_with_operator_count(self, operator_count):
        if operator_count < 1 or operator_count > 3:
            raise ValueError("运算符数量必须在1-3之间")

        operand_count = operator_count + 1
        operands = [self.generate_number() for _ in range(operand_count)]
        operators = [random.choice(self.operators) for _ in range(operator_count)]

        expression = self.build_expression_with_validation(operands, operators)
        return expression

    def build_expression_with_validation(self, operands, operators, max_attempts=100):
        for attempt in range(max_attempts):
            expression = self.build_expression(operands, operators)
            if self.validate_expression(expression):
                return expression
            operators = [random.choice(self.operators) for _ in range(len(operators))]
        return self.build_expression(operands, operators)

    def build_expression(self, operands, operators):
        if len(operators) == 1:
            return f"{operands[0]} {operators[0]} {operands[1]}"
        elif len(operators) == 2:
            if random.random() < 0.5:
                return f"{operands[0]} {operators[0]} {operands[1]} {operators[1]} {operands[2]}"
            else:
                return f"({operands[0]} {operators[0]} {operands[1]}) {operators[1]} {operands[2]}"
        else:
            bracket_type = random.randint(1, 3)
            if bracket_type == 1:
                return f"({operands[0]} {operators[0]} {operands[1]}) {operators[1]} {operands[2]} {operators[2]} {operands[3]}"
            elif bracket_type == 2:
                return f"{operands[0]} {operators[0]} ({operands[1]} {operators[1]} {operands[2]}) {operators[2]} {operands[3]}"
            else:
                return f"({operands[0]} {operators[0]} {operands[1]} {operators[1]} {operands[2]}) {operators[2]} {operands[3]}"

    def validate_expression(self, expression):
        try:
            operator_count = sum(1 for char in expression if char in self.operators)
            if operator_count > 3:
                return False

            result = self.calculate_expression(expression)
            if result is None or result < 0:
                return False

            if not self.validate_division_results(expression, result):
                return False

            return True
        except:
            return False

    def validate_division_results(self, expression, result):
        divisions = re.findall(r'(\S+)\s*÷\s*(\S+)', expression)
        for left, right in divisions:
            try:
                left_val = self.parse_fraction(left)
                right_val = self.parse_fraction(right)
                if right_val == 0:
                    return False
                division_result = left_val / right_val
                if division_result >= 1 and division_result.denominator != 1:
                    return False
            except:
                continue
        return True

    def calculate_expression(self, expression):
        try:
            py_expr = self.convert_to_python_expression(expression)
            result = eval(py_expr, {"Fraction": Fraction, "__builtins__": {}})
            return result
        except:
            return None

    def convert_to_python_expression(self, expression):
        py_expr = expression.replace('×', '*').replace('÷', '/')

        def replace_number(match):
            num_str = match.group()
            if '/' in num_str:
                parts = num_str.split('/')
                return f"Fraction({parts[0]}, {parts[1]})"
            else:
                return f"Fraction({num_str})"

        py_expr = re.sub(r'\b\d+\b', replace_number, py_expr)
        py_expr = re.sub(r'\b\d+/\d+\b', replace_number, py_expr)

        return py_expr

    def parse_fraction(self, num_str):
        if '/' in num_str:
            parts = num_str.split('/')
            return Fraction(int(parts[0]), int(parts[1]))
        else:
            return Fraction(int(num_str))

    def normalize_expression(self, expression):
        return expression.replace(' ', '')

    def is_duplicate(self, expression):
        normalized = self.normalize_expression(expression)
        if normalized in self.generated_expressions:
            return True
        for expr in self.generated_expressions:
            if self.is_commutative_duplicate(normalized, expr):
                return True
        return False

    def is_commutative_duplicate(self, expr1, expr2):
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
    @staticmethod
    def calculate(expression):
        try:
            py_expr = expression.replace('×', '*').replace('÷', '/')

            def replace_number(match):
                num_str = match.group()
                if '/' in num_str:
                    parts = num_str.split('/')
                    return f"Fraction({parts[0]}, {parts[1]})"
                else:
                    return f"Fraction({num_str})"

            py_expr = re.sub(r'\b\d+\b', replace_number, py_expr)
            py_expr = re.sub(r'\b\d+/\d+\b', replace_number, py_expr)

            result = eval(py_expr, {"Fraction": Fraction, "__builtins__": {}})
            return ArithmeticCalculator.format_fraction(result)
        except Exception as e:
            print(f"计算错误: {expression}, 错误: {e}")
            return None

    @staticmethod
    def format_fraction(value):
        if isinstance(value, Fraction):
            if value.denominator == 1:
                return str(value.numerator)

            if value.numerator >= value.denominator:
                whole = value.numerator // value.denominator
                remainder = value.numerator % value.denominator
                if remainder == 0:
                    return str(whole)
                else:
                    return f"{whole}'{remainder}/{value.denominator}"
            else:
                return f"{value.numerator}/{value.denominator}"
        elif isinstance(value, int):
            return str(value)
        else:
            try:
                frac = Fraction(value).limit_denominator()
                return ArithmeticCalculator.format_fraction(frac)
            except:
                return str(value)

    @staticmethod
    def compare_answers(answer1, answer2):
        try:
            def parse_answer(ans):
                if "'" in ans:
                    parts = ans.split("'")
                    whole = int(parts[0])
                    frac_parts = parts[1].split('/')
                    return whole + Fraction(int(frac_parts[0]), int(frac_parts[1]))
                elif '/' in ans:
                    parts = ans.split('/')
                    return Fraction(int(parts[0]), int(parts[1]))
                else:
                    return Fraction(int(ans))

            val1 = parse_answer(answer1)
            val2 = parse_answer(answer2)
            return val1 == val2
        except:
            return False


class FileManager:
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
    parser.add_argument('-r', type=int, help='数值范围')  # 移除了 required=True
    parser.add_argument('-e', type=str, help='题目文件路径')
    parser.add_argument('-a', type=str, help='答案文件路径')

    args = parser.parse_args()

    # 验证参数组合的合法性
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
            expression = generator.generate_expression()

            if generator.is_duplicate(expression):
                continue

            answer = calculator.calculate(expression)
            if answer is not None and generator.validate_expression(expression):
                exercises.append(expression)
                answers.append(answer)
                generator.generated_expressions.add(generator.normalize_expression(expression))
                count += 1

        file_manager.save_exercises(exercises)
        file_manager.save_answers(answers)
        print(f'生成完成！题目保存在Exercises.txt，答案保存在Answers.txt')

    elif args.e and args.a:
        # 批改模式：不需要 -r 参数
        file_manager = FileManager()
        calculator = ArithmeticCalculator()

        exercises = file_manager.load_exercises(args.e)
        user_answers = file_manager.load_answers(args.a)

        correct = []
        wrong = []

        for i, (exercise, user_answer) in enumerate(zip(exercises, user_answers)):
            correct_answer = calculator.calculate(exercise)
            if correct_answer and calculator.compare_answers(user_answer, correct_answer):
                correct.append(i + 1)
            else:
                wrong.append(i + 1)

        file_manager.save_grade(correct, wrong)
        print("批改完成！结果保存在Grade.txt")

    else:
        # 参数不完整时的错误提示
        if args.e and not args.a:
            print("错误：使用 -e 参数时必须同时提供 -a 参数")
        elif args.a and not args.e:
            print("错误：使用 -a 参数时必须同时提供 -e 参数")
        elif args.n and not args.r:
            print("错误：使用 -n 参数时必须同时提供 -r 参数")
        else:
            parser.print_help()


if __name__ == '__main__':
    main()
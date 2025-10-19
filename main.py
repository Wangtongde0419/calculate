#!/usr/bin/env python3
import argparse
import sys
from generator import ExpressionGenerator
from calculator import ExpressionCalculator
from file_io import FileManager
from validator import DuplicateChecker


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
        calculator = ExpressionCalculator()
        duplicate_checker = DuplicateChecker()
        file_manager = FileManager()

        exercises = []
        answers = []
        count = 0

        while count < args.n:
            # 生成表达式
            expression = generator.generate_expression()

            # 检查重复
            if duplicate_checker.is_duplicate(expression, exercises):
                continue

            # 计算答案
            try:
                answer = calculator.calculate(expression)
                # 验证答案合法性
                if calculator.validate_answer(answer):
                    exercises.append(expression)
                    answers.append(answer)
                    count += 1
            except:
                continue

        # 保存文件
        file_manager.save_exercises(exercises, 'Exercises.txt')
        file_manager.save_answers(answers, 'Answers.txt')
        print(f'已生成{args.n}道题目，保存在Exercises.txt和Answers.txt')

    elif args.e and args.a:
        # 批改模式
        file_manager = FileManager()
        exercises = file_manager.load_exercises(args.e)
        answers = file_manager.load_answers(args.a)

        correct = []
        wrong = []

        calculator = ExpressionCalculator()
        for i, (exercise, user_answer) in enumerate(zip(exercises, answers)):
            try:
                correct_answer = calculator.calculate(exercise)
                if calculator.compare_answers(user_answer, correct_answer):
                    correct.append(i + 1)
                else:
                    wrong.append(i + 1)
            except:
                wrong.append(i + 1)

        # 生成统计结果
        result = f"Correct: {len(correct)} {correct}\nWrong: {len(wrong)} {wrong}"
        file_manager.save_grade(result, 'Grade.txt')
        print("批改完成，结果保存在Grade.txt")
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
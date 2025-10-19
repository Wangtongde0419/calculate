class FileManager:
    @staticmethod
    def save_exercises(exercises, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            for i, exercise in enumerate(exercises, 1):
                f.write(f"{i}. {exercise} = \n")

    @staticmethod
    def save_answers(answers, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            for i, answer in enumerate(answers, 1):
                f.write(f"{i}. {answer}\n")

    @staticmethod
    def load_exercises(filename):
        exercises = []
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                # 移除题号，提取表达式
                exercise = line.split('.', 1)[1].strip()
                exercise = exercise.rsplit('=', 1)[0].strip()
                exercises.append(exercise)
        return exercises

    @staticmethod
    def load_answers(filename):
        answers = []
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                answer = line.split('.', 1)[1].strip()
                answers.append(answer)
        return answers

    @staticmethod
    def save_grade(grade_info, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(grade_info)
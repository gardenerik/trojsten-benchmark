from bench.problems import Problem


class RubricGrader:
    def get_prompt(self, problem: Problem, rubric: str, solution: str) -> list[str]:
        raise NotImplementedError()

    def get_points(self, response: str) -> float:
        raise NotImplementedError()

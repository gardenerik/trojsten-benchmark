from bench.problems import Problem


class Rubricer:
    def get_prompt(self, problem: Problem) -> list[str]:
        raise NotImplementedError()

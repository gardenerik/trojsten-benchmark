from bench.problems import Problem
from bench.rubricers import Rubricer


class SlovakRubricer(Rubricer):
    def get_prompt(self, problem: Problem) -> list[str]:
        return [
            f"{problem.solution}\n"
            "Z uvedeného vzorového riešenia vytvor stupnicu na hodnotenie riešení,"
            "pričom maximálny počet bodov, ktoré môžeš za riešenie udeliť je 10."
        ]


class EnglishRubricer(Rubricer):
    def get_prompt(self, problem: Problem) -> list[str]:
        if problem.competition.startswith("ksp"):
            return [
                f"```\n{problem.solution}\n```\n\n"
                "From the provided sample solution, create a rubric to evaluate "
                "solutions. A maximum of 10 points can be awarded for the "
                "solution. You only grade the description of the algorithm, no "
                "code. The description should contain description of the idea, "
                "data structures, algorithm, reasoning for correctnes of the "
                "solution and estimation of space and time complexity. "
                "Make sure your rubric contains all details that are needed to "
                "determine correctness of a student's solution."
            ]

        return [
            f"```\n{problem.solution}\n```\n\n"
            "From the provided sample solution, create a rubric to evaluate "
            "solutions. A maximum of 10 points can be awarded for the solution. "
            "Make sure your rubric contains all details that are needed to "
            "determine correctness of a student's solution, including all "
            "relevant equations or numeric results."
        ]

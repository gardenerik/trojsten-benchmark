import re

from bench.graders import RubricGrader
from bench.problems import Problem


class V1Grader(RubricGrader):
    def get_points(self, response: str) -> float:
        rex = re.compile(r"POINTS: ?(\d+(?:\.\d+)?)")
        match = rex.search(response)
        if not match:
            raise ValueError("Model returned invalid grading.")

        return float(match.group(1))


class SlovakRubricGrader(V1Grader):
    def get_prompt(self, problem: Problem, rubric: str, solution: str) -> list[str]:
        return [
            f"Hodnotiaca stupnica:\n{rubric}",
            (
                f"Študentovo riešenie:\n{solution}\n"
                "Na základe uvedenej hodnotiacej stupnice oboduj toto riešenie najviac "
                "10timi bodmi. Svoje rozhodnutie v krátkosti zdôvodni. Svoju odpoveď "
                "ukonči textom POINTS: a počtom udelených bodov."
            ),
        ]


class EnglishRubricGrader(V1Grader):
    def get_prompt(self, problem: Problem, rubric: str, solution: str) -> list[str]:
        return [
            (
                f"# Grading rubric:\n```\n{rubric}\n```\n\n"
                f"# Student's solution:\n```\n{solution}\n```\n\n"
                "Based on the above grading rubric, score this solution with a maximum of "
                "10 points. Feel free to assign partial points. Briefly justify your "
                "decision, indicating for each point in the rubric whether or not the "
                "student has met it. End your answer with the text POINTS: and the number "
                "of points awarded, even if zero."
            )
        ]

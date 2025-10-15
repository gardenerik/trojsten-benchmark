from bench.models import Prompt
from bench.problems import Problem
from bench.solvers import MultiPromptSolver


class DualPromptGeneratedKnowledge(MultiPromptSolver):
    def get_prompt_stage(
        self, problem: Problem, stage: int, previous: list[Prompt]
    ) -> list[Prompt] | None:
        if stage >= 2:
            return None

        if stage == 0:
            return [
                Prompt(
                    f"```\n{problem.problem}\n```\n\nDescribe all concepts and ideas required to solve this problem."
                )
            ]

        if stage == 1:
            competition = problem.competition

            if competition.startswith("ksp"):
                return [
                    Prompt(
                        "Write an description of an algorithm to solve the problem. "
                        "Your solution should contain clear descriptions of the ideas, algorithms and data structures used. "
                        "You should also justify the correctness of your solution and include an estimation of space and time complexity."
                    )
                ]

            add = ""
            if competition.startswith("fks"):
                add = "If doing an experiment is necessary to solve the problem, please generate the data and experiment results. "

            return [
                Prompt(
                    "Solve the given problem. It should be clear from your answer how you "
                    f"arrived at your result. {add}"
                )
            ]

from bench.problems import Problem
from bench.solvers import Solver


class SlovakSolver(Solver):
    def get_prompt(self, problem: Problem) -> list[str]:
        return [
            f"{problem.problem}\n"
            "Z tvojej odpovede by malo byť jasné, ako si sa k výsledku dostal. Ak "
            "má úloha číslené riešenie, ukonči svoju odpoveď textom ANS: "
            "a číselnou hodnotou bez jednotky. Ak úloha číslené riešenie nemá, "
            "neuvádzaj ANS: vôbec."
        ]


class ZeroshotV1EnglishSolver(Solver):
    def get_prompt(self, problem: Problem) -> list[str]:
        if problem.competition.startswith("ksp"):
            return [
                f"```\n{problem.problem}\n```\n\n"
                "Write an description of an algorithm to solve the given problem. "
                "Your solution should contain clear descritpions of the ideas, algorithms and data structures used. "
                "You should also justify the correctness of your solution and include an estimation of space and time complexity."
            ]

        add = ""
        if problem.competition.startswith("fks"):
            add = "If doing an experiment is necessary to solve the problem, please generate the data and experiment results. "

        return [
            f"```\n{problem.problem}\n```\n\n"
            "Solve the given problem. It should be clear from your answer how you "
            f"arrived at your result. {add}If the problem has a numerical solution, end "
            "your answer with ANS: and the numerical value without any units. "
            "If the problem does not have a numerical solution, do not output ANS: "
            "at all."
        ]

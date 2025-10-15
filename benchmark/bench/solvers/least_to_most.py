from bench.models import Prompt
from bench.problems import Problem
from bench.solvers import ModelMisbehaviourException, MultiPromptSolver


class LeastToMostSolver(MultiPromptSolver):
    def get_prompt_stage(
        self, problem: Problem, stage: int, previous: list[Prompt]
    ) -> list[Prompt] | None:
        if stage == 0:
            return [
                Prompt(
                    f"```\n{problem.problem}\n```\n\n"
                    "Plan out all the subproblems that you need to solve before solving this problem. "
                    "You will be graded based on how clear your process and ideas are. "
                    "If the problem requires writing code, don't write any, it won't be graded, only your description of the algorithm. "
                    "If the problem requires measuring experiments, generate random placeholder data instead. "
                    'Write one step on a line prefixed with "- ". Do not introduce additional line breaks. For example: \n'
                    "- This would be the first step.\nDo not output more than 7 subproblems."
                )
            ]

        if stage >= 1:
            steps = previous[1].message.split("\n")
            steps = list(filter(lambda x: x.strip() != "", steps))
            if len(steps) > 7:
                raise ModelMisbehaviourException(
                    f"Model was asked to provide up to than 7 subproblems, but it provided {len(steps)}."
                )

            step_index = stage - 1
            if len(steps) == step_index:
                ins = ""
                if problem.competition.startswith("ksp"):
                    ins = (
                        "Write an description of an algorithm to solve the problem. "
                        "Your solution should contain clear descriptions of the ideas, algorithms and data structures used. "
                        "You should also justify the correctness of your solution and include an estimation of space and time complexity. "
                    )

                return [
                    Prompt(
                        "Now, conclude your solution by summarising all your steps, ideas, equations, justify your decisions and state the final answer. "
                        f"{ins}"
                        "Only this part will be graded, so make sure to include everything you deem necessary to understand your solution."
                    )
                ]
            if len(steps) + 1 == step_index:
                return None

            return [
                Prompt(
                    f"Now, solve this subproblem: {steps[step_index].strip().removeprefix('- ')}"
                )
            ]

import abc
from dataclasses import dataclass, field

from bench.models import LanguageModel, Prompt
from bench.problems import Problem


@dataclass
class SolverOutput:
    solution: str
    messages: list[Prompt] = field(default_factory=list)


class BaseSolver(abc.ABC):
    @abc.abstractmethod
    def solve(self, problem: Problem, model: LanguageModel) -> SolverOutput:
        raise NotImplementedError


class ModelMisbehaviourException(Exception):
    pass


class Solver(BaseSolver):
    def solve(self, problem: Problem, model: LanguageModel) -> SolverOutput:
        solve_prompt = self.get_prompt(problem)
        solution = model.send_prompt(solve_prompt)
        return SolverOutput(
            solution, [Prompt(p) for p in solve_prompt] + [Prompt(solution, True)]
        )

    def get_prompt(self, problem: Problem) -> list[str]:
        raise NotImplementedError()


class MultiPromptSolver(BaseSolver):
    def solve(self, problem: Problem, model: LanguageModel) -> SolverOutput:
        prompts = []
        stage = 0
        last_output = ""

        while True:
            next_prompt = self.get_prompt_stage(problem, stage, prompts)
            if not next_prompt:
                break

            prompts.extend(next_prompt)
            stage += 1

            last_output = model.send_prompt(prompts)
            prompts.append(Prompt(last_output, assistant=True))

        return SolverOutput(last_output, prompts)

    def get_prompt_stage(
        self, problem: Problem, stage: int, previous: list[Prompt]
    ) -> list[Prompt] | None:
        raise NotImplementedError()

from pathlib import Path
import csv

from plumbum import colors

from bench.models import (
    LanguageModel,
    GPT35Turbo,
    GPT4Turbo,
    GPT4,
    AzureGPT4,
    AzureGPT35Turbo,
    AzureGPT35Turbo16k,
    AzureGPT4o,
    Llama370b,
    Phi3Mini,
    Phi3Medium,
    Prompt,
    Qwen3,
)
from bench.problems import Problem
from bench.solvers import BaseSolver
from bench.solvers.generated_knowledge import GeneratedKnowledgeSolver
from bench.solvers.dualprompt_generated_knowledge import DualPromptGeneratedKnowledge
from bench.solvers.least_to_most import LeastToMostSolver
from bench.solvers.zeroshot_cot import ZeroshotCoTSolver
from bench.solvers.zeroshot_v1 import ZeroshotV1EnglishSolver


def print_prompt(prompt: list[str]):
    print(colors.blue | "PROMPT:")
    print((colors.orange1 | "\n *** (message delimiter) *** \n").join(prompt))
    print(colors.darkgray | "-" * 30)


def print_response(resp: str):
    print(colors.blue | "RESPONSE:")
    print(resp)
    print(colors.darkgray | "-" * 30)


def prompts_to_string(prompts: list[Prompt]) -> str:
    output = []

    for prompt in prompts:
        site = "MODEL" if prompt.assistant else "USER"
        output.append(f"------ {site} ------")
        output.append(prompt.message)

    return "\n".join(output)


def get_model(name: str) -> LanguageModel:
    models = {
        "gpt-3.5-turbo": GPT35Turbo,
        "gpt-4-turbo": GPT4Turbo,
        "gpt-4": GPT4,
        "azure-gpt-3.5-turbo": AzureGPT35Turbo,
        "azure-gpt-3.5-turbo-16k": AzureGPT35Turbo16k,
        "azure-gpt-4": AzureGPT4,
        "azure-gpt-4o": AzureGPT4o,
        "llama3:70b": Llama370b,
        "qwen3:32b": Qwen3,
        "phi3:mini": Phi3Mini,
        "phi3:medium": Phi3Medium,
    }

    if name not in models:
        raise ValueError(f"Unknown model '{name}'")

    return models[name]()


def get_solver(name: str) -> BaseSolver:
    models = {
        "zs-v1-en": ZeroshotV1EnglishSolver,
        "zs-cot": ZeroshotCoTSolver,
        "dual-gk": DualPromptGeneratedKnowledge,
        "gk": GeneratedKnowledgeSolver,
        "ltm": LeastToMostSolver,
    }

    if name not in models:
        raise ValueError(f"Unknown solver '{name}'")

    return models[name]()


def get_problems(infile: str) -> list[Problem]:
    with open(infile) as f:
        problems = []
        reader = csv.reader(infile)

        for row in reader:
            id, competition, problem, solution, difficulty = row
            difficulty = int(difficulty)
            problems.append(Problem(id, competition, problem, solution, difficulty))

    return problems

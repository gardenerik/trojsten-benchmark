import os
from pathlib import Path

from plumbum import colors

from bench.models import GPT4Turbo, AzureGPT4
from bench.problems import Problem
from bench.rubricers.zeroshot_v1 import EnglishRubricer


def get_rubric(problem: Problem) -> str:
    if os.environ.get("USE_AZURE") == "1":
        model = AzureGPT4()
    else:
        model = GPT4Turbo()

    prompt = EnglishRubricer().get_prompt(problem)
    prefix = "gpt4-v1"

    rubric_dir = Path("storage/rubrics") / prefix / problem.competition
    rubric_dir.mkdir(exist_ok=True, parents=True)
    rubric_file = rubric_dir / problem.id

    if rubric_file.exists():
        return rubric_file.read_text()

    print(colors.LightYellow | f"WARN: Generating rubric for {problem.id}")

    try:
        rubric = model.send_prompt(prompt)
    except Exception as e:
        print(colors.red | f"ERROR: {problem.id} {e}")
        return ""

    rubric_file.write_text(rubric)
    return rubric

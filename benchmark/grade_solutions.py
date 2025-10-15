import csv
import os
import sys
import time
from pathlib import Path

from plumbum import colors
from tqdm.contrib.concurrent import thread_map

from bench.graders.zeroshot_v1 import EnglishRubricGrader
from bench.models import GPT4Turbo, AzureGPT4
from bench.problems import Problem
from bench.rubric_tools import get_rubric
from bench.utils import get_problems


if len(sys.argv) != 3:
    print("Usage: [list] [prefix]")
    exit(1)

list_name = sys.argv[1]

problems = get_problems(list_name)

prefix = sys.argv[2]

if os.environ.get("USE_AZURE") == "1":
    grader_model = AzureGPT4()
else:
    grader_model = GPT4Turbo()
grader = EnglishRubricGrader()

solution_dir = Path("storage/solutions") / prefix / problems[0].competition
grading_dir = Path("storage/grading") / prefix / problems[0].competition
grading_dir.mkdir(parents=True, exist_ok=True)


def grade(problem: Problem):
    if (grading_dir / problem.id).exists():
        time.sleep(0.1)
        try:
            pts = grader.get_points((grading_dir / problem.id).read_text())
            return problem.id, pts
        except ValueError:
            return problem.id, None

    rubric = get_rubric(problem)
    try:
        solution = (solution_dir / problem.id).read_text()
    except FileNotFoundError:
        print(colors.red | f"ERROR: {problem.id} solution not found")
        return problem.id, None

    output = grading_dir / problem.id
    if output.exists():
        print(colors.LightYellow | f"Problem {problem.id} is already graded, SKIPPING.")
        grading = output.read_text()
    else:
        try:
            grader_prompt = grader.get_prompt(problem, rubric, solution)
            grading = grader_model.send_prompt(grader_prompt)
            output.write_text(grading)
        except Exception as e:
            print(colors.red | f"ERROR: {problem.id} error while solving {e}")
            return problem.id, None

    try:
        pts = grader.get_points(grading)
        return problem.id, pts
    except ValueError:
        return problem.id, None


results = thread_map(grade, problems, max_workers=8)

for problem, pts in results:
    if pts is None:
        print(colors.LightYellow | f"{problem}: no points provided by grader")
    else:
        print(colors.LightGreen | f"{problem}: {pts} pts")

with grading_dir.with_suffix(".csv").open("w") as f:
    w = csv.writer(f)
    w.writerow(["problem", "points"])
    for problem, pts in results:
        w.writerow([problem, str(pts)])

print(len(results))

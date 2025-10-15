import sys
from pathlib import Path
import time

from plumbum import colors
from tqdm.contrib.concurrent import thread_map

from bench.problems import Problem
from bench.utils import get_problems, get_model, get_solver, prompts_to_string

if len(sys.argv) != 5:
    print("Usage: [list] [prefix] [model] [solver]")
    exit(1)

list_name = sys.argv[1]
problems = get_problems(list_name)

prefix = sys.argv[2]
solver_model = get_model(sys.argv[3])
solver = get_solver(sys.argv[4])

output_dir = Path("storage/solutions") / prefix


def generate_solution(problem: Problem):
    try:
        output = output_dir / problem.competition / problem.id
        if output.exists():
            print(
                colors.LightYellow
                | f"Problem {problem.id} is already solved, SKIPPING."
            )
            time.sleep(0.01)  # This is here just to let TQDM update.
            return

        result = solver.solve(problem, solver_model)

        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(result.solution)

        output.with_suffix(".prompts").write_text(prompts_to_string(result.messages))
    except Exception as e:
        print(colors.red | f"ERROR: {problem.id} {e}")
        return


print(colors.red | "> Generating solutions.")
thread_map(generate_solution, problems, max_workers=2)

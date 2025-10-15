import sys

from plumbum import colors
from tqdm.contrib.concurrent import thread_map

from bench.rubric_tools import get_rubric
from bench.utils import get_problems

if len(sys.argv) != 2:
    print("Usage: [list]")
    exit(1)

list_name = sys.argv[1]
problems = get_problems(list_name)

print(colors.red | "> Generating grading rubrics.")
thread_map(get_rubric, problems, max_workers=4)

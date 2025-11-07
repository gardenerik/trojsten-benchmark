<div align="center">
  <h1>Trojsten Benchmark</h1>
  <p>Evaluating LLM Problem-Solving in Slovak STEM Competition Problems</p>
</div>

- **Paper**: [EMNLP 2025](https://aclanthology.org/2025.emnlp-main.1779/)
- **Authors**: Adam Zahradník, Marek Šuppa
- **Repository**:
  [github.com/gardenerik/trojsten-benchmark](https://github.com/gardenerik/trojsten-benchmark)
- **Contact**: [adam@zahradnik.xyz](mailto:adam@zahradnik.xyz)

## Abstract

Large language models show promising performance on reasoning tasks, yet evaluation
methods for low-resource languages remain limited, particularly for complex STEM
problem-solving. We introduce Trojsten Benchmark, a Slovak-language dataset of 1,108
high-school competition problems with reference solutions across mathematics, physics,
and programming, and a rubric-based LLM grading framework. Using GPT-4 to generate
rubrics and grade solutions, we observe 1.05 average absolute deviation from human
graders (5-point scale), while benchmarking GPT-3.5-Turbo, GPT-4, GPT-4o, and
open-weight models (Llama 3, Phi-3). We quantify multistep reasoning performance
by difficulty, show consistent underperformance on harder items, and demonstrate
language sensitivity: accuracy drops on English translations of Slovak statements,
evidencing challenges beyond translation. Trojsten Benchmark complements
English-centric math datasets (e.g., MATH, GSM8K) by targeting open-response,
rubric-gradable reasoning under low-resource linguistic framing. We release code
and data to enable reproducible evaluation and human-aligned auto-grading for STEM
in under-served languages.

## Basic Usage

**Generate LLM Solutions:**

```bash
python generate_solutions.py [list] [prefix] [model] [solver]

# Example:
python generate_solutions.py fks_test experiment1 gpt4 zeroshot_cot
```

**Generate Evaluation Rubrics:**

```bash
python generate_rubrics.py [list] [prefix] [model]

# Example:
python generate_rubrics.py fks_test experiment1 gpt4
```

**Grade Generated Solutions:**

```bash
python grade_solutions.py [list] [prefix] [grader] [rubricer]

# Example:
python grade_solutions.py fks_test experiment1 zeroshot_v1 zeroshot_v1
```

**Available Solvers:**

- `zeroshot_v1`: Basic zero-shot approach
- `zeroshot_cot`: Zero-shot with chain-of-thought reasoning
- `generated_knowledge`: Uses generated knowledge for problem solving
- `dualprompt_generated_knowledge`: Dual prompt generated knowledge
- `least_to_most`: Least-to-most problem decomposition

**Models Supported:**

- OpenAI GPT models (`gpt4`, `gpt3.5-turbo`)
- Azure OpenAI deployments
- Custom model configurations

## Data Format

Each problem in the dataset is stored in a CSV with the following columns:

```csv
id,competition,problem,solution,difficulty
```

**Example:**

```csv
1b56d285f84b378c,fks,"Sme na vysokom strome...","Zamyslime sa nad tym...",3
```

**Fields:**

- `id`: Unique problem identifier
- `competition`: Competition type (fks, kms, ksp)
- `problem`: Problem statement in Slovak
- `solution`: Detailed solution explanation
- `difficulty`: Numeric difficulty rating

## Citation

```
@inproceedings{zahradnik-suppa-2025-trojsten,
    title = "Trojsten Benchmark: Evaluating {LLM} Problem-Solving in {S}lovak {STEM} Competition Problems",
    author = "Zahradn{\'i}k, Adam  and
      Suppa, Marek",
    editor = "Christodoulopoulos, Christos  and
      Chakraborty, Tanmoy  and
      Rose, Carolyn  and
      Peng, Violet",
    booktitle = "Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing",
    month = nov,
    year = "2025",
    address = "Suzhou, China",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2025.emnlp-main.1779/",
    pages = "35094--35109",
    ISBN = "979-8-89176-332-6",
    abstract = "Large language models show promising performance on reasoning tasks, yet evaluation methods for low-resource languages remain limited, particularly for complex STEM problem-solving. We introduce Trojsten Benchmark, a Slovak-language dataset of 1,108 high-school competition problems with reference solutions across mathematics, physics, and programming, and a rubric-based LLM grading framework. Using GPT-4 to generate rubrics and grade solutions, we observe 1.05 average absolute deviation from human graders (5-point scale), while benchmarking GPT-3.5-Turbo, GPT-4, GPT-4o, and open-weight models (Llama 3, Phi-3). We quantify multistep reasoning performance by difficulty, show consistent underperformance on harder items, and demonstrate language sensitivity: accuracy drops on English translations of Slovak statements, evidencing challenges beyond translation. Trojsten Benchmark complements English-centric math datasets (e.g., MATH, GSM8K) by targeting open-response, rubric-gradable reasoning under low-resource linguistic framing. We release code and data to enable reproducible evaluation and human-aligned auto-grading for STEM in under-served languages."
}
```

## License

This project is part of academic research. Please contact the authors for usage information.

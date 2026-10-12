# Milestone 1 experiments

Run these commands from the project root with Python 3.10 or later:

```text
python -B Milestone1/test_correctness.py
python -B Milestone1/benchmark.py > Milestone1/benchmark_tables.txt
```

The test suite uses seed 4533 and checks 100,000 valid random cases per program against an independent dynamic programming reference. It checks jump lengths, arrival at the last panel, and the reported landing cost.

The benchmark also uses seed 4533. It validates every generated input before timing. It records 20 trials per configuration, each using a different random input. Each recorded timing is the average per call over a batch of 50 calls for Program 1 or 5 calls for Program 2, after a warmup call. Input generation, validation, and file writing are outside the timed block.

`timings.csv` contains all 400 trial timings. `results.json` contains the means, sample standard deviations, fitted constants, and runtime environment. `inputs/` contains one stdin example for each of the 20 configurations. Within a varying k trial, each program reuses the same costs across all five k values.

The fitted curves use least squares with zero intercept. For work values x and measured means y, the fitted constant is sum(x*y)/sum(x*x). Program 1 uses x=n/k. Program 2 uses x=n.

The benchmark prints the LaTeX data tables used by the report. After a new run, update the embedded tables and numerical observations together. The random inputs are reproducible from the seed. Runtimes depend on the machine and its workload.

These files support the experiments. Upload only program1.py and program2.py to the Gradescope code submission.

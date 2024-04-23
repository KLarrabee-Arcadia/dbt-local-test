# dbt example

This is an example of a fully local setup using Docker to run dbt tests against a spark/hudi backend.

First run Spark & Hudi (along with the Thrift server for dbt to authenticate against):

```bash
❯ docker compose up -d spark-hudi
```

Then run DBT tests using Spark as the backend:

```bash
❯ docker compose up dbt-spark

[+] Running 1/0
 ✔ Container dbt-elt-example-dbt-spark-1  Created                                                                                                                0.0s
Attaching to dbt-elt-example-dbt-spark-1
dbt-elt-example-dbt-spark-1  | 20:25:37  Running with dbt=1.7.10
dbt-elt-example-dbt-spark-1  | 20:25:37  Warning: No packages were found in packages.yml
dbt-elt-example-dbt-spark-1  | 20:25:37  Warning: No packages were found in packages.yml
dbt-elt-example-dbt-spark-1  | 20:25:38  Running with dbt=1.7.10
dbt-elt-example-dbt-spark-1  | 20:25:38  Registered adapter: spark=1.7.1
dbt-elt-example-dbt-spark-1  | 20:25:38  Unable to do partial parsing because profile has changed
dbt-elt-example-dbt-spark-1  | 20:25:38  Found 1 model, 1 seed, 5 tests, 0 sources, 0 exposures, 0 metrics, 439 macros, 0 groups, 0 semantic models
dbt-elt-example-dbt-spark-1  | 20:25:38
dbt-elt-example-dbt-spark-1  | 20:25:49  Concurrency: 1 threads (target='dev')
dbt-elt-example-dbt-spark-1  | 20:25:49
dbt-elt-example-dbt-spark-1  | 20:25:49  1 of 7 START seed file dbt.customer_base ....................................... [RUN]
dbt-elt-example-dbt-spark-1  | 20:25:56  1 of 7 OK loaded seed file dbt.customer_base ................................... [INSERT 599 in 7.01s]
dbt-elt-example-dbt-spark-1  | 20:25:56  2 of 7 START test not_null_customer_base_customer_id ........................... [RUN]
dbt-elt-example-dbt-spark-1  | 20:25:56  2 of 7 PASS not_null_customer_base_customer_id ................................. [PASS in 0.13s]
dbt-elt-example-dbt-spark-1  | 20:25:56  3 of 7 START test not_null_customer_base_store_id .............................. [RUN]
dbt-elt-example-dbt-spark-1  | 20:25:56  3 of 7 PASS not_null_customer_base_store_id .................................... [PASS in 0.13s]
dbt-elt-example-dbt-spark-1  | 20:25:56  4 of 7 START sql view model dbt.int_customers_per_store ........................ [RUN]
dbt-elt-example-dbt-spark-1  | 20:25:56  4 of 7 OK created sql view model dbt.int_customers_per_store ................... [OK in 0.09s]
dbt-elt-example-dbt-spark-1  | 20:25:56  5 of 7 START test not_null_int_customers_per_store_store_id .................... [RUN]
dbt-elt-example-dbt-spark-1  | 20:25:56  5 of 7 PASS not_null_int_customers_per_store_store_id .......................... [PASS in 0.18s]
dbt-elt-example-dbt-spark-1  | 20:25:56  6 of 7 START test not_null_int_customers_per_store_total_customers ............. [RUN]
dbt-elt-example-dbt-spark-1  | 20:25:56  6 of 7 PASS not_null_int_customers_per_store_total_customers ................... [PASS in 0.08s]
dbt-elt-example-dbt-spark-1  | 20:25:56  7 of 7 START test unique_int_customers_per_store_store_id ...................... [RUN]
dbt-elt-example-dbt-spark-1  | 20:25:56  7 of 7 PASS unique_int_customers_per_store_store_id ............................ [PASS in 0.19s]
dbt-elt-example-dbt-spark-1  | 20:26:01
dbt-elt-example-dbt-spark-1  | 20:26:01  Finished running 1 seed, 5 tests, 1 view model in 0 hours 0 minutes and 23.08 seconds (23.08s).
dbt-elt-example-dbt-spark-1  | 20:26:01
dbt-elt-example-dbt-spark-1  | 20:26:01  Completed successfully
dbt-elt-example-dbt-spark-1  | 20:26:01
dbt-elt-example-dbt-spark-1  | 20:26:01  Done. PASS=7 WARN=0 ERROR=0 SKIP=0 TOTAL=7
dbt-elt-example-dbt-spark-1 exited with code 0
```

The `dbt_spark_example` file structure was originally created (when this previously had `dbt-core` and `dbt-spark` installed in a
Poetry virtualenv) via:

```bash
❯ poetry run dbt init dbt_spark
```

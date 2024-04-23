# dbt example

Based on https://towardsdatascience.com/create-local-dbt-project-e12c31bd3992

Builds and runs tests using Postgres:

```
❯ docker compose up dbt

[+] Running 4/0
 ✔ Network dbt-elt-example_default                                                                                                                         Created                                                                 0.0s
 ✔ Container dbt-elt-example-postgres-1                                                                                                                    Created                                                                 0.0s
 ! postgres The requested image's platform (linux/amd64) does not match the detected host platform (linux/arm64/v8) and no specific platform was requested                                                                         0.0s
 ✔ Container dbt                                                                                                                                           Created                                                                 0.0s
dbt  | 15:44:00  Running with dbt=1.3.1
dbt  | 15:44:00  Warning: No packages were found in packages.yml
dbt  | 15:44:01  Running with dbt=1.3.1
dbt  | 15:44:01  Unable to do partial parsing because profile has changed
dbt  | 15:44:02  Found 3 models, 8 tests, 0 snapshots, 0 analyses, 289 macros, 0 operations, 1 seed file, 1 source, 0 exposures, 0 metrics
dbt  | 15:44:02
dbt  | 15:44:12  Concurrency: 1 threads (target='dev')
dbt  | 15:44:12
dbt  | 15:44:12  1 of 12 START sql view model dbt.stg_payment ................................... [RUN]
dbt  | 15:44:12  1 of 12 OK created sql view model dbt.stg_payment .............................. [CREATE VIEW in 0.10s]
dbt  | 15:44:12  2 of 12 START seed file dbt.customer_base ...................................... [RUN]
dbt  | 15:44:18  2 of 12 OK loaded seed file dbt.customer_base .................................. [INSERT 599 in 5.56s]
dbt  | 15:44:18  3 of 12 START test not_null_stg_payment_customer_id ............................ [RUN]
dbt  | 15:44:18  3 of 12 PASS not_null_stg_payment_customer_id .................................. [PASS in 0.06s]
dbt  | 15:44:18  4 of 12 START test not_null_stg_payment_payment_id ............................. [RUN]
dbt  | 15:44:18  4 of 12 PASS not_null_stg_payment_payment_id ................................... [PASS in 0.05s]
dbt  | 15:44:18  5 of 12 START test unique_stg_payment_payment_id ............................... [RUN]
dbt  | 15:44:18  5 of 12 PASS unique_stg_payment_payment_id ..................................... [PASS in 0.09s]
dbt  | 15:44:18  6 of 12 START test not_null_customer_base_customer_id .......................... [RUN]
dbt  | 15:44:18  6 of 12 PASS not_null_customer_base_customer_id ................................ [PASS in 0.05s]
dbt  | 15:44:18  7 of 12 START test not_null_customer_base_store_id ............................. [RUN]
dbt  | 15:44:18  7 of 12 PASS not_null_customer_base_store_id ................................... [PASS in 0.05s]
dbt  | 15:44:18  8 of 12 START sql view model dbt.int_revenue_by_date ........................... [RUN]
dbt  | 15:44:18  8 of 12 OK created sql view model dbt.int_revenue_by_date ...................... [CREATE VIEW in 0.06s]
dbt  | 15:44:18  9 of 12 START sql view model dbt.int_customers_per_store ....................... [RUN]
dbt  | 15:44:18  9 of 12 OK created sql view model dbt.int_customers_per_store .................. [CREATE VIEW in 0.06s]
dbt  | 15:44:18  10 of 12 START test not_null_int_customers_per_store_store_id .................. [RUN]
dbt  | 15:44:18  10 of 12 PASS not_null_int_customers_per_store_store_id ........................ [PASS in 0.05s]
dbt  | 15:44:18  11 of 12 START test not_null_int_customers_per_store_total_customers ........... [RUN]
dbt  | 15:44:18  11 of 12 PASS not_null_int_customers_per_store_total_customers ................. [PASS in 0.05s]
dbt  | 15:44:18  12 of 12 START test unique_int_customers_per_store_store_id .................... [RUN]
dbt  | 15:44:18  12 of 12 PASS unique_int_customers_per_store_store_id .......................... [PASS in 0.05s]
dbt  | 15:44:18
dbt  | 15:44:18  Finished running 3 view models, 1 seed, 8 tests in 0 hours 0 minutes and 16.62 seconds (16.62s).
dbt  | 15:44:18
dbt  | 15:44:18  Completed successfully
dbt  | 15:44:18
dbt  | 15:44:18  Done. PASS=12 WARN=0 ERROR=0 SKIP=0 TOTAL=12
```

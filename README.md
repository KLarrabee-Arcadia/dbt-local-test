# dbt example

This is an example of a fully local setup using Docker to run dbt tests against a hudi backend.
It includes first seeding data from a CSV into a table and then creating a model that references the seeded table.

## Setup

First run Derby/Hudi (along with the Thrift server for dbt to authenticate against):

```bash
❯ docker compose up -d spark-hudi
```

Then run DBT tests using Spark as the backend:

```bash
❯ docker compose up dbt-spark

[+] Running 1/0
 ✔ Container dbt-elt-example-dbt-spark-1  Created                                                                                                                0.0s
Attaching to dbt-elt-example-dbt-spark-1
dbt-elt-example-dbt-spark-1  | 19:42:44  Running with dbt=1.7.10
dbt-elt-example-dbt-spark-1  | 19:42:44  Warning: No packages were found in packages.yml
dbt-elt-example-dbt-spark-1  | 19:42:44  Warning: No packages were found in packages.yml
dbt-elt-example-dbt-spark-1  | 19:42:45  Running with dbt=1.7.10
dbt-elt-example-dbt-spark-1  | 19:42:45  Registered adapter: spark=1.7.1
dbt-elt-example-dbt-spark-1  | 19:42:45  Found 1 model, 1 seed, 5 tests, 0 sources, 0 exposures, 0 metrics, 439 macros, 0 groups, 0 semantic models
dbt-elt-example-dbt-spark-1  | 19:42:45
dbt-elt-example-dbt-spark-1  | 19:42:47  Concurrency: 1 threads (target='dev')
dbt-elt-example-dbt-spark-1  | 19:42:47
dbt-elt-example-dbt-spark-1  | 19:42:47  1 of 7 START seed file hudi_dbt.customer_base .................................. [RUN]
dbt-elt-example-dbt-spark-1  | 19:42:50  1 of 7 OK loaded seed file hudi_dbt.customer_base .............................. [INSERT 599 in 3.38s]
dbt-elt-example-dbt-spark-1  | 19:42:50  2 of 7 START test not_null_customer_base_customer_id ........................... [RUN]
dbt-elt-example-dbt-spark-1  | 19:42:56  2 of 7 PASS not_null_customer_base_customer_id ................................. [PASS in 5.59s]
dbt-elt-example-dbt-spark-1  | 19:42:56  3 of 7 START test not_null_customer_base_store_id .............................. [RUN]
dbt-elt-example-dbt-spark-1  | 19:42:56  3 of 7 PASS not_null_customer_base_store_id .................................... [PASS in 0.20s]
dbt-elt-example-dbt-spark-1  | 19:42:56  4 of 7 START sql view model hudi_dbt.int_customers_per_store ................... [RUN]
dbt-elt-example-dbt-spark-1  | 19:42:56  4 of 7 OK created sql view model hudi_dbt.int_customers_per_store .............. [OK in 0.14s]
dbt-elt-example-dbt-spark-1  | 19:42:56  5 of 7 START test not_null_int_customers_per_store_store_id .................... [RUN]
dbt-elt-example-dbt-spark-1  | 19:42:56  5 of 7 PASS not_null_int_customers_per_store_store_id .......................... [PASS in 0.31s]
dbt-elt-example-dbt-spark-1  | 19:42:56  6 of 7 START test not_null_int_customers_per_store_total_customers ............. [RUN]
dbt-elt-example-dbt-spark-1  | 19:42:56  6 of 7 PASS not_null_int_customers_per_store_total_customers ................... [PASS in 0.16s]
dbt-elt-example-dbt-spark-1  | 19:42:56  7 of 7 START test unique_int_customers_per_store_store_id ...................... [RUN]
dbt-elt-example-dbt-spark-1  | 19:42:57  7 of 7 PASS unique_int_customers_per_store_store_id ............................ [PASS in 0.33s]
dbt-elt-example-dbt-spark-1  | 19:43:02
dbt-elt-example-dbt-spark-1  | 19:43:02  Finished running 1 seed, 5 tests, 1 view model in 0 hours 0 minutes and 16.84 seconds (16.84s).
dbt-elt-example-dbt-spark-1  | 19:43:02
dbt-elt-example-dbt-spark-1  | 19:43:02  Completed successfully
dbt-elt-example-dbt-spark-1  | 19:43:02
dbt-elt-example-dbt-spark-1  | 19:43:02  Done. PASS=7 WARN=0 ERROR=0 SKIP=0 TOTAL=7
dbt-elt-example-dbt-spark-1 exited with code 0
```

The `dbt_spark_example` file structure was originally created (when this previously had `dbt-core` and `dbt-spark` installed in a
Poetry virtualenv) via:

```bash
❯ poetry run dbt init dbt_spark
```

Much of the Dockerfile & `run.sh` script effectively came from: https://github.com/apache/hudi/blob/master/hudi-examples/hudi-examples-dbt/README.md

## Testing

After running the `dbt` tests, you can inspect the Hudi tables manually inside the running `spark_hudi` service.

1. `exec` into the running container:

```bash
❯ docker exec -it $(docker ps | grep spark-hudi | awk '{print $1}') /bin/bash
```

2. Run `beeline` to enter its interactive prompt:

```bash
root@7b4f96b751e1:/opt/spark/work-dir# $SPARK_HOME/bin/beeline
```

3. Connect to the Thrift server:

```
Beeline version 2.3.9 by Apache Hive

beeline> !connect jdbc:hive2://localhost:10000
```

4. Now press `<enter>` twice to bypass username & password authentication:

```
Connecting to jdbc:hive2://localhost:10000
Enter username for jdbc:hive2://localhost:10000:
Enter password for jdbc:hive2://localhost:10000:
```

5. After connecting, `use` the appropriate schema defined in `dbt_project.yml`:

```
Connected to: Spark SQL (version 3.4.1)
Driver: Hive JDBC (version 2.3.9)
Transaction isolation: TRANSACTION_REPEATABLE_READ
0: jdbc:hive2://localhost:10000> use hudi_dbt;
```

6. Now query to your heart's content:

```
0: jdbc:hive2://localhost:10000> select * from customer_base limit 10;
+--------------+-----------+-------------+------------+-------------------------------------+-------------+-------------+--------------+------------------------+---------+
| customer_id  | store_id  | first_name  | last_name  |                email                | address_id  | activebool  | create_date  |      last_update       | active  |
+--------------+-----------+-------------+------------+-------------------------------------+-------------+-------------+--------------+------------------------+---------+
| 100          | 1         | ROBIN       | HAYES      | ROBIN.HAYES@sakilacustomer.org      | 104         | t           | 2006-02-14   | 2006-02-15 09:57:20.0  | 1       |
| 101          | 1         | PEGGY       | MYERS      | PEGGY.MYERS@sakilacustomer.org      | 105         | t           | 2006-02-14   | 2006-02-15 09:57:20.0  | 1       |
| 102          | 1         | CRYSTAL     | FORD       | CRYSTAL.FORD@sakilacustomer.org     | 106         | t           | 2006-02-14   | 2006-02-15 09:57:20.0  | 1       |
| 103          | 1         | GLADYS      | HAMILTON   | GLADYS.HAMILTON@sakilacustomer.org  | 107         | t           | 2006-02-14   | 2006-02-15 09:57:20.0  | 1       |
| 104          | 1         | RITA        | GRAHAM     | RITA.GRAHAM@sakilacustomer.org      | 108         | t           | 2006-02-14   | 2006-02-15 09:57:20.0  | 1       |
| 105          | 1         | DAWN        | SULLIVAN   | DAWN.SULLIVAN@sakilacustomer.org    | 109         | t           | 2006-02-14   | 2006-02-15 09:57:20.0  | 1       |
| 106          | 1         | CONNIE      | WALLACE    | CONNIE.WALLACE@sakilacustomer.org   | 110         | t           | 2006-02-14   | 2006-02-15 09:57:20.0  | 1       |
| 107          | 1         | FLORENCE    | WOODS      | FLORENCE.WOODS@sakilacustomer.org   | 111         | t           | 2006-02-14   | 2006-02-15 09:57:20.0  | 1       |
| 108          | 1         | TRACY       | COLE       | TRACY.COLE@sakilacustomer.org       | 112         | t           | 2006-02-14   | 2006-02-15 09:57:20.0  | 1       |
| 109          | 2         | EDNA        | WEST       | EDNA.WEST@sakilacustomer.org        | 113         | t           | 2006-02-14   | 2006-02-15 09:57:20.0  | 1       |
+--------------+-----------+-------------+------------+-------------------------------------+-------------+-------------+--------------+------------------------+---------+


0: jdbc:hive2://localhost:10000> select * from int_customers_per_store;
+-----------+------------------+
| store_id  | total_customers  |
+-----------+------------------+
| 1         | 326              |
| 2         | 273              |
+-----------+------------------+
```

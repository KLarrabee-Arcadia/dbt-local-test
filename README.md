# dbt example

This is an example of a fully local setup using Docker to run dbt tests against a hudi backend.
It includes first seeding data from a CSV into a table and then creating a model that references the seeded table.

## Setup

First run Derby/Hudi (along with the Thrift server for dbt to authenticate against):

First, run the `hudi` service. This includes Spark, a Derby server,
and a Thrift server configured to use Derby as its metastore and Hudi
as its warehouse.

```bash
❯ docker compose up -d hudi
```

> This will additionally create a `hudi_sources.payment` table and seed it with
> a few hundred records, to aid in testing DBT models configured against external sources.


Next DBT tests:

```bash
❯ docker compose up dbt
[+] Running 1/0
 ✔ Container dbt-elt-example-dbt-1  Created                                                                                                           0.0s
Attaching to dbt-elt-example-dbt-1
dbt-elt-example-dbt-1  | 17:42:27  Running with dbt=1.7.10
dbt-elt-example-dbt-1  | 17:42:27  Warning: No packages were found in packages.yml
dbt-elt-example-dbt-1  | 17:42:27  Warning: No packages were found in packages.yml
dbt-elt-example-dbt-1  | 17:42:28  Running with dbt=1.7.10
dbt-elt-example-dbt-1  | 17:42:28  Registered adapter: spark=1.7.1
dbt-elt-example-dbt-1  | 17:42:28  [WARNING]: Configuration paths exist in your dbt_project.yml file which do not apply to any resources.
dbt-elt-example-dbt-1  | There are 1 unused configuration paths:
dbt-elt-example-dbt-1  | - models.int_customers_per_store
dbt-elt-example-dbt-1  | 17:42:28  Found 2 models, 1 seed, 8 tests, 1 source, 0 exposures, 0 metrics, 439 macros, 0 groups, 0 semantic models
dbt-elt-example-dbt-1  | 17:42:28
dbt-elt-example-dbt-1  | 17:42:30  Concurrency: 1 threads (target='dev')
dbt-elt-example-dbt-1  | 17:42:30
dbt-elt-example-dbt-1  | 17:42:30  1 of 11 START sql view model hudi_dbt.stg_payment .............................. [RUN]
dbt-elt-example-dbt-1  | 17:42:30  1 of 11 OK created sql view model hudi_dbt.stg_payment ......................... [OK in 0.43s]
dbt-elt-example-dbt-1  | 17:42:30  2 of 11 START seed file hudi_dbt.customer_base ................................. [RUN]
dbt-elt-example-dbt-1  | 17:42:38  2 of 11 OK loaded seed file hudi_dbt.customer_base ............................. [INSERT 599 in 8.13s]
dbt-elt-example-dbt-1  | 17:42:38  3 of 11 START test not_null_stg_payment_customer_id ............................ [RUN]
dbt-elt-example-dbt-1  | 17:42:39  3 of 11 PASS not_null_stg_payment_customer_id .................................. [PASS in 0.63s]
dbt-elt-example-dbt-1  | 17:42:39  4 of 11 START test not_null_stg_payment_payment_id ............................. [RUN]
dbt-elt-example-dbt-1  | 17:42:39  4 of 11 PASS not_null_stg_payment_payment_id ................................... [PASS in 0.19s]
dbt-elt-example-dbt-1  | 17:42:39  5 of 11 START test unique_stg_payment_payment_id ............................... [RUN]
dbt-elt-example-dbt-1  | 17:42:39  5 of 11 PASS unique_stg_payment_payment_id ..................................... [PASS in 0.44s]
dbt-elt-example-dbt-1  | 17:42:39  6 of 11 START test not_null_customer_base_customer_id .......................... [RUN]
dbt-elt-example-dbt-1  | 17:42:40  6 of 11 PASS not_null_customer_base_customer_id ................................ [PASS in 0.22s]
dbt-elt-example-dbt-1  | 17:42:40  7 of 11 START test not_null_customer_base_store_id ............................. [RUN]
dbt-elt-example-dbt-1  | 17:42:40  7 of 11 PASS not_null_customer_base_store_id ................................... [PASS in 0.17s]
dbt-elt-example-dbt-1  | 17:42:40  8 of 11 START sql view model hudi_dbt.int_customers_per_store .................. [RUN]
dbt-elt-example-dbt-1  | 17:42:40  8 of 11 OK created sql view model hudi_dbt.int_customers_per_store ............. [OK in 0.10s]
dbt-elt-example-dbt-1  | 17:42:40  9 of 11 START test not_null_int_customers_per_store_store_id ................... [RUN]
dbt-elt-example-dbt-1  | 17:42:40  9 of 11 PASS not_null_int_customers_per_store_store_id ......................... [PASS in 0.21s]
dbt-elt-example-dbt-1  | 17:42:40  10 of 11 START test not_null_int_customers_per_store_total_customers ........... [RUN]
dbt-elt-example-dbt-1  | 17:42:40  10 of 11 PASS not_null_int_customers_per_store_total_customers ................. [PASS in 0.15s]
dbt-elt-example-dbt-1  | 17:42:40  11 of 11 START test unique_int_customers_per_store_store_id .................... [RUN]
dbt-elt-example-dbt-1  | 17:42:40  11 of 11 PASS unique_int_customers_per_store_store_id .......................... [PASS in 0.23s]
dbt-elt-example-dbt-1  | 17:42:46
dbt-elt-example-dbt-1  | 17:42:46  Finished running 2 view models, 1 seed, 8 tests in 0 hours 0 minutes and 17.52 seconds (17.52s).
dbt-elt-example-dbt-1  | 17:42:46
dbt-elt-example-dbt-1  | 17:42:46  Completed successfully
dbt-elt-example-dbt-1  | 17:42:46
dbt-elt-example-dbt-1  | 17:42:46  Done. PASS=11 WARN=0 ERROR=0 SKIP=0 TOTAL=11
dbt-elt-example-dbt-1 exited with code 0
```

## Testing

After running the `dbt` tests, you can inspect the Hudi tables manually inside the running `hudi` service.

1. `exec` into the running container:

```bash
❯ docker exec -it $(docker ps | grep hudi | awk '{print $1}') /bin/bash
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

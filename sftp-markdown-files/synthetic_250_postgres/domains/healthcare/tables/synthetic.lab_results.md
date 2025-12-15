# lab_results

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The "synthetic.lab_results" table in the "synthetic_250_postgres" database is intended to store information related to laboratory results, as indicated by its name, with "result_id" serving as the primary key. Although it has no defined column data or sample rows, its role can be inferred as capturing detailed laboratory outcomes, possibly linked to other data entities via two unspecified foreign key relationships. The absence of referencing tables and further information limits a detailed understanding of its interactions and dependencies within the data model.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| result_id | integer | NO | This column uniquely identifies each entry in laboratory results, serving as a sequential record number. |
| order_id | integer | NO | A unique identifier linking laboratory test results to specific orders, ensuring result traceability within the medical testing process. Represents a key component for matching completed tests with their originating requests. |
| test_id | integer | NO | Purpose unclear from available data. |
| result_value | character varying | YES | Purpose unclear from available data. |
| result_unit | character varying | YES | The column likely records the units of measurement for laboratory test results. Purpose unclear from available data. |
| reference_range | character varying | YES | Purpose unclear from available data. |
| abnormal_flag | character varying | YES | The column likely indicates whether a lab test result is considered abnormal, but the specific details are unclear from the available data. |
| collected_date | timestamp without time zone | YES | This represents the date and time when a laboratory sample was collected. Purpose unclear from available data. |
| resulted_date | timestamp without time zone | YES | The column records the date and time when laboratory results were finalized or entered into the system. Purpose unclear from available data. |
| status | character varying | YES | Purpose unclear from available data. |
| created_at | timestamp without time zone | YES | This column records the date and time when each lab result entry was created. Purpose unclear from available data. |
| updated_at | timestamp without time zone | YES | This column likely captures the date and time when a lab result record was last modified, helping track changes over time. Purpose unclear from available data. |

## Primary Key

`result_id`

## Foreign Keys

- `order_id` → `synthetic.lab_orders.order_id`
- `test_id` → `synthetic.lab_tests.test_id`

## Indexes

- `lab_results_pkey`: CREATE UNIQUE INDEX lab_results_pkey ON synthetic.lab_results USING btree (result_id)

*Generated at: 2025-12-14T23:41:40.365Z*
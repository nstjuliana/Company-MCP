# time_off_balances

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The "synthetic.time_off_balances" table maintains information on employee leave balances for different leave types within specific fiscal years, capturing the hours accrued, used, and carried over. Its primary key, "balance_id", uniquely identifies each record, and it references employee data via a foreign key, suggesting a connection to an employee-related table. Although no tables reference this one, its role is likely to track and manage time-off balances for employees over time.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| balance_id | integer | NO | This column represents a unique identifier for each record in the time off balances table, sequentially assigned to track different time off balance entries. |
| employee_id | integer | NO | This column uniquely identifies each employee's record in the context of tracking time off balances. It serves as a reference to associate specific time off information with the correct employee. |
| leave_type | character varying | NO | Purpose unclear from available data. |
| fiscal_year | integer | NO | This column represents the year when the time-off balance applies within the organization's fiscal operations. Based on sample values, it typically refers to future periods, suggesting planning or projection of time-off balances. |
| hours_accrued | numeric | YES | This column represents the amount of time off that an employee has accrued, measured in hours. The values indicate varying balances of unused or accumulated time off for individuals within an organization. |
| hours_used | numeric | YES | This column represents the total amount of time-off hours that have been utilized by an individual or entity within an unspecified timeframe. Purpose unclear from available data. |
| hours_carried_over | numeric | YES | This column represents the number of time-off hours an employee has carried over from previous periods. The values indicate varying balances reflecting the specific hours available to employees for future time off. |
| created_at | timestamp without time zone | YES | This column captures the date and time when each record was initially created in the time off balances table. It primarily reflects when an entry was added, defaulting to the current timestamp at the moment of creation. |
| updated_at | timestamp without time zone | YES | This column records the date and time when the time-off balance record was last updated. The timestamp defaults to the current time when the record is updated, indicating the most recent modification. |

## Primary Key

`balance_id`

## Foreign Keys

- `employee_id` → `synthetic.employees.employee_id`

## Indexes

- `time_off_balances_pkey`: CREATE UNIQUE INDEX time_off_balances_pkey ON synthetic.time_off_balances USING btree (balance_id)

## Sample Data

| balance_id | employee_id | leave_type | fiscal_year | hours_accrued | hours_used | hours_carried_over | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 49 | Thus fight catch serious later they. | 2020 | 203.56 | 549.22 | 927.67 | Sat Dec 13 2025 03:19:55 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:19:55 GMT-0600 (Central Stan... |
| 2 | 29 | Much article agent. | 2025 | 484.71 | 28.87 | 630.02 | Sat Dec 13 2025 03:19:55 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:19:55 GMT-0600 (Central Stan... |
| 3 | 16 | Federal idea share property. | 2025 | 158.38 | 550.84 | 552.25 | Sat Dec 13 2025 03:19:55 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:19:55 GMT-0600 (Central Stan... |
| 4 | 6 | Outside interest tough character. | 2021 | 992.26 | 912.93 | 461.45 | Sat Dec 13 2025 03:19:55 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:19:55 GMT-0600 (Central Stan... |
| 5 | 8 | Great require else so so interest great analysis. | 2025 | 832.14 | 498.38 | 716.60 | Sat Dec 13 2025 03:19:55 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:19:55 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:41:10.284Z*
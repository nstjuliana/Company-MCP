# salary_history

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `salary_history` table records changes in salary for employees over time, identified uniquely by `salary_history_id`, with details such as the salary amount and currency, effective and end dates, and reasons for changes. It includes an `employee_id` to associate salary records with specific employees and has foreign key relationships to undefined entities, indicating possible links with other employee or salary management tables. This table plays a role in tracking historical compensation data for audit purposes and payroll adjustments.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| salary_history_id | integer | NO | This column represents a unique identifier for each entry in the salary history, ensuring each record is distinct. It is auto-incremented sequentially to differentiate between individual historical salary records. |
| employee_id | integer | NO | This column represents unique identifiers for employees in the salary history record. It is used to associate salary data with specific employees. |
| effective_date | date | NO | This column represents the date when a particular salary arrangement becomes active. It ensures historical accuracy by marking the start of each salary record's validity period. |
| end_date | date | YES | This column represents the date when an individual's salary arrangement or employment contract is scheduled to end within the company. The purpose is to track the conclusion of salary commitments, but the exact context of usage is unclear from the available data. |
| salary_amount | numeric | NO | This column represents monetary amounts associated with employee salaries. Purpose unclear from available data. |
| currency | character varying | YES | This column indicates the currency in which salaries have been recorded, reflecting international monetary units such as Euros, US dollars, and British pounds. It suggests that the salary history data can involve multiple currencies, predominantly EUR, USD, and GBP. |
| change_reason | character varying | YES | Purpose unclear from available data. The sample values appear to be random, fragmented phrases lacking a clear thematic connection or context. |
| approved_by | integer | YES | This column likely represents the unique identifier of a person or entity responsible for approving salary changes. The specific role or capacity of this approver is unclear from the available data. |
| created_at | timestamp without time zone | YES | This column records the date and time when a salary history entry was created, using the current timestamp by default. Purpose unclear from available data. |
| updated_at | timestamp without time zone | YES | This column records the date and time when a salary history entry was last updated. The default value ensures that it captures the current timestamp when an update is made, though it may not always be populated. |

## Primary Key

`salary_history_id`

## Foreign Keys

- `approved_by` → `synthetic.employees.employee_id`
- `employee_id` → `synthetic.employees.employee_id`

## Indexes

- `salary_history_pkey`: CREATE UNIQUE INDEX salary_history_pkey ON synthetic.salary_history USING btree (salary_history_id)

## Sample Data

| salary_history_id | employee_id | effective_date | end_date | salary_amount | currency | change_reason | approved_by | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 48 | Sat Nov 22 2025 00:00:00 GMT-0600 (Central Stan... | Wed Dec 11 2024 00:00:00 GMT-0600 (Central Stan... | 8109.39 | EUR | Send born college include fund tree somebody de... | 11 | Sat Dec 13 2025 03:19:41 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:19:41 GMT-0600 (Central Stan... |
| 2 | 45 | Sun Sep 08 2024 00:00:00 GMT-0500 (Central Dayl... | Mon Sep 02 2024 00:00:00 GMT-0500 (Central Dayl... | 1089.88 | USD | War citizen plant little key. Child source camp... | 31 | Sat Dec 13 2025 03:19:41 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:19:41 GMT-0600 (Central Stan... |
| 3 | 15 | Tue Aug 26 2025 00:00:00 GMT-0500 (Central Dayl... | Sun Jul 28 2024 00:00:00 GMT-0500 (Central Dayl... | 2003.73 | EUR | Garden reach state cover board discussion. Mayb... | 23 | Sat Dec 13 2025 03:19:41 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:19:41 GMT-0600 (Central Stan... |
| 4 | 20 | Sat Dec 16 2023 00:00:00 GMT-0600 (Central Stan... | Wed Oct 29 2025 00:00:00 GMT-0500 (Central Dayl... | 8207.16 | USD | Government south window short affect region. Pr... | 15 | Sat Dec 13 2025 03:19:41 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:19:41 GMT-0600 (Central Stan... |
| 5 | 2 | Tue Dec 02 2025 00:00:00 GMT-0600 (Central Stan... | Wed Feb 12 2025 00:00:00 GMT-0600 (Central Stan... | 6603.73 | EUR | Argue garden Mrs just. Book care seek foot simple. | 22 | Sat Dec 13 2025 03:19:41 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:19:41 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:41:04.604Z*
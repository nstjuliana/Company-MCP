# project_budgets

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.project_budgets` table captures financial details related to project budgeting, including the allocation and utilization of funds across various categories. It records the budgeted and actual amounts, providing insights into financial performance via variance calculations. The table is linked to another entity through the `project_id` foreign key, suggesting its role in tracking budgetary metrics within broader project management processes.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| budget_id | integer | NO | This column likely serves as a unique identifier for each project budget entry, ensuring that each budget can be distinctly referenced. The sequential nature of the sample values suggests it is used to maintain the order of budget records within the system. |
| project_id | integer | NO | This column represents unique identifiers assigned to various projects, ensuring each project is distinctly tracked within the database. |
| category | character varying | YES | This column likely represents descriptive text or labels associated with project budget categories. Purpose unclear from available data. |
| budgeted_amount | numeric | NO | This column represents the allocated financial resources for various projects within the organization. It quantifies the expected expenditure in monetary terms for each project. |
| actual_amount | numeric | YES | This column represents the monetary amount that has been actually spent or used in various projects. The values reflect real expenditure figures that may vary project by project. |
| variance | numeric | YES | This column represents the differences in budgeted versus actual expenditures for various projects. Purpose unclear from available data. |
| created_at | timestamp without time zone | YES | This column records the date and time when a project budget entry was created. Purpose unclear from available data. |
| updated_at | timestamp without time zone | YES | This column records the date and time when each project budget entry was last modified. It reflects updates in the system and defaults to the current timestamp when the entry is created or changed. |

## Primary Key

`budget_id`

## Foreign Keys

- `project_id` → `synthetic.pm_projects.project_id`

## Indexes

- `project_budgets_pkey`: CREATE UNIQUE INDEX project_budgets_pkey ON synthetic.project_budgets USING btree (budget_id)

## Sample Data

| budget_id | project_id | category | budgeted_amount | actual_amount | variance | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 72 | Force feeling total practice. Peace their crime... | 5477.63 | 1314.64 | 852.42 | Sat Dec 13 2025 03:13:31 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:13:31 GMT-0600 (Central Stan... |
| 2 | 72 | Produce study practice radio into. Question ans... | 8942.61 | 7624.92 | 45.94 | Sat Dec 13 2025 03:13:31 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:13:31 GMT-0600 (Central Stan... |
| 3 | 91 | Laugh cause agent edge push take. Sign go help ... | 7841.06 | 4601.22 | 124.24 | Sat Dec 13 2025 03:13:31 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:13:31 GMT-0600 (Central Stan... |
| 4 | 61 | Success much husband risk tell. Plan woman sout... | 4418.45 | 16.75 | 958.03 | Sat Dec 13 2025 03:13:31 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:13:31 GMT-0600 (Central Stan... |
| 5 | 63 | From consider view fine far development first. ... | 9956.98 | 9094.98 | 882.15 | Sat Dec 13 2025 03:13:31 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:13:31 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:42:09.263Z*
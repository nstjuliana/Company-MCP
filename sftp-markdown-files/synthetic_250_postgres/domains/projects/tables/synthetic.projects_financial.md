# projects_financial

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.projects_financial` table represents the financial details of projects, each uniquely identified by `project_id`. It holds data such as project name, client identification, timelines, budgeted versus actual amounts, status, and billing type, reflecting the financial lifecycle of diverse projects. Despite having no direct relationships with other tables, it plays a critical role in tracking and managing the financial aspects of projects within the database.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| project_id | integer | NO | This column uniquely identifies each project within the financial records of the company, ensuring each project can be individually tracked and referenced. |
| project_code | character varying | YES | This column appears to represent unique alphanumeric identifiers assigned to various projects. Purpose unclear from available data. |
| project_name | character varying | NO | This column represents the titles or names assigned to various projects within the context of financial management, capturing diverse thematic descriptions. Purpose unclear from available data. |
| client_id | integer | YES | This column represents a unique identifier for clients associated with financial projects, allowing for the differentiation and tracking of financial dealings with individual clients. Purpose unclear from available data beyond serving as a client reference. |
| start_date | date | YES | This column records the date when a financial project begins, reflecting start dates occurring between 2024 and 2025. The dates accommodate both standard and daylight saving time adjustments within the Central Time Zone. |
| end_date | date | YES | This column represents the date on which a project is scheduled to conclude or terminate. Its purpose is to track the planned completion timeframe for financial projects, allowing for flexibility as it can remain unspecified if undetermined. |
| budgeted_amount | numeric | YES | This column represents the planned monetary resources allocated for specific projects within an organization. It reflects varying levels of funding necessary for different projects as indicated by the diverse sample values. |
| actual_amount | numeric | YES | This column represents the actual monetary amounts related to financial transactions or budget allocations within projects, expressed in a currency format. The values appear to depict financial figures that could represent expenditures, revenues, or costs associated with projects. |
| status | character varying | YES | This column represents the current state or progress of a project, indicating whether it is active, inactive, completed, or pending. It provides insight into the project's lifecycle status at a given point in time, with "active" set as the default. |
| billing_type | character varying | YES | Purpose unclear from available data. |
| created_at | timestamp without time zone | YES | This column represents the date and time at which a financial project record was created. Purpose unclear from available data, but the timestamps suggest it records the project's initial creation time in the system. |
| updated_at | timestamp without time zone | YES | This column records the date and time when an entry in the financial projects table was last updated. It defaults to the current timestamp if unspecified, but the specific business purpose remains unclear from the available data. |

## Primary Key

`project_id`

## Indexes

- `projects_financial_pkey`: CREATE UNIQUE INDEX projects_financial_pkey ON synthetic.projects_financial USING btree (project_id)
- `projects_financial_project_code_key`: CREATE UNIQUE INDEX projects_financial_project_code_key ON synthetic.projects_financial USING btree (project_code)

## Sample Data

| project_id | project_code | project_name | client_id | start_date | end_date | budgeted_amount | actual_amount | status | billing_type | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | MFXNQIRLND | Action guess decision scene plant cup. Indeed r... | 6769 | Sat Nov 09 2024 00:00:00 GMT-0600 (Central Stan... | Sat Jan 20 2024 00:00:00 GMT-0600 (Central Stan... | 5500.79 | 85438.55 | inactive | find | Sat Dec 13 2025 02:55:10 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:10 GMT-0600 (Central Stan... |
| 2 | WOYWTZRJSH | Total he put memory article. Learn perhaps real... | 3282 | Wed Apr 10 2024 00:00:00 GMT-0500 (Central Dayl... | Wed Mar 05 2025 00:00:00 GMT-0600 (Central Stan... | 34332.72 | 98720.44 | completed | nothing | Sat Dec 13 2025 02:55:10 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:10 GMT-0600 (Central Stan... |
| 3 | MVNYUHNWAU | Reality imagine according glass high perform. O... | 2347 | Fri Nov 22 2024 00:00:00 GMT-0600 (Central Stan... | Sun Jan 19 2025 00:00:00 GMT-0600 (Central Stan... | 31706.71 | 71595.28 | active | dinner | Sat Dec 13 2025 02:55:10 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:10 GMT-0600 (Central Stan... |
| 4 | NEMFGNBYZK | Program because themselves training. It always ... | 7989 | Thu Jan 09 2025 00:00:00 GMT-0600 (Central Stan... | Fri Jul 19 2024 00:00:00 GMT-0500 (Central Dayl... | 33329.68 | 98665.37 | pending | mother | Sat Dec 13 2025 02:55:10 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:10 GMT-0600 (Central Stan... |
| 5 | EUQHXJZAXN | Let wind question will mission. Be wonder likel... | 951 | Thu Dec 04 2025 00:00:00 GMT-0600 (Central Stan... | Mon Jun 02 2025 00:00:00 GMT-0500 (Central Dayl... | 570.88 | 27425.43 | inactive | front | Sat Dec 13 2025 02:55:10 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:10 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:42:16.306Z*
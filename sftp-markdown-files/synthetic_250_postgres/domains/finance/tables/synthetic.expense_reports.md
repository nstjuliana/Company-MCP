# expense_reports

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.expense_reports` table represents the collection of expense reports filed by employees within an organization, with each report uniquely identified by the `report_id`. The table includes essential details about each report such as the employee who filed it (`employee_id`), the title, submission date, total amount and currency, status, as well as information about approval, including the approver and approval date. It references key information from other unidentified tables, likely those containing employee and approver details, emphasizing its role in tracking and managing financial report submissions and approvals.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| report_id | integer | NO | This column represents unique identifiers assigned incrementally to individual expense reports within the system, ensuring that each report can be distinctly recognized. |
| employee_id | integer | NO | Represents a unique identifier for employees associated with expense reports. Purpose unclear from available data. |
| report_title | character varying | YES | This column appears to contain titles or brief descriptions summarizing or naming individual expense reports. The purpose of the phrases seems to be to create a simple reference or theme for the expense reports, although the exact context or relevance is unclear from the available data. |
| submission_date | date | YES | This column represents the date on which an expense report was submitted. It may indicate a process interaction timeframe, with submissions potentially spanning a variety of dates throughout the year. |
| total_amount | numeric | YES | This column represents the monetary amounts associated with individual expense reports. The values indicate various totals, which suggest it may capture the overall cost recorded in financial records submitted for reimbursement or accounting purposes. |
| currency | character varying | YES | This column specifies the currency in which expenses are reported, such as British Pounds (GBP), US Dollars (USD), and Euros (EUR). It indicates the monetary unit applicable to each expense record. |
| status | character varying | YES | This column indicates the current state of an expense report, signifying whether it is active, inactive, or pending. The default status is pending, suggesting a report is awaiting further action or review. |
| approved_by | integer | YES | This column likely identifies an individual, such as a manager or administrator, who approves expense reports, using an integer that corresponds to a specific ID. The purpose of mapping these values to specific roles or individuals is unclear from the available data. |
| approved_date | date | YES | This column records the date on which an expense report was approved. The approval dates range across various months and years, indicating a timeline for expense approval activities. |
| notes | text | YES | This column contains free-form textual comments or descriptions that accompany expense reports and provide additional context or miscellaneous details related to the expenses. Purpose unclear from available data. |
| created_at | timestamp without time zone | YES | This column indicates the date and time when an expense report was initially created. The purpose of tracking this timestamp is likely for monitoring or record-keeping of expense report submissions. |
| updated_at | timestamp without time zone | YES | This column records the date and time when an expense report was last modified. It is used to track updates to records within the expense reports. |

## Primary Key

`report_id`

## Foreign Keys

- `approved_by` → `synthetic.employees.employee_id`
- `employee_id` → `synthetic.employees.employee_id`

## Indexes

- `expense_reports_pkey`: CREATE UNIQUE INDEX expense_reports_pkey ON synthetic.expense_reports USING btree (report_id)

## Sample Data

| report_id | employee_id | report_title | submission_date | total_amount | currency | status | approved_by | approved_date | notes | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 47 | Economy free at without lawyer. | Sat May 04 2024 00:00:00 GMT-0500 (Central Dayl... | 4621.61 | GBP | active | 29 | Mon Jun 23 2025 00:00:00 GMT-0500 (Central Dayl... | Morning after at year institution city. Visit i... | Sat Dec 13 2025 03:20:41 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:20:41 GMT-0600 (Central Stan... |
| 2 | 19 | Chance record trouble show. | Mon Jun 10 2024 00:00:00 GMT-0500 (Central Dayl... | 8314.51 | USD | inactive | 44 | Sun Jul 27 2025 00:00:00 GMT-0500 (Central Dayl... | Total similar although put believe. Blue month ... | Sat Dec 13 2025 03:20:41 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:20:41 GMT-0600 (Central Stan... |
| 3 | 32 | Result authority next evening similar. | Tue Jan 21 2025 00:00:00 GMT-0600 (Central Stan... | 1400.40 | EUR | active | 17 | Mon Sep 15 2025 00:00:00 GMT-0500 (Central Dayl... | Language so few program true. Special thus midd... | Sat Dec 13 2025 03:20:41 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:20:41 GMT-0600 (Central Stan... |
| 4 | 43 | Economic road miss adult middle. | Wed Jul 23 2025 00:00:00 GMT-0500 (Central Dayl... | 1549.89 | EUR | inactive | 5 | Fri Feb 28 2025 00:00:00 GMT-0600 (Central Stan... | Table training meet national environmental cover. | Sat Dec 13 2025 03:20:41 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:20:41 GMT-0600 (Central Stan... |
| 5 | 29 | Republican agent yes. | Sun Jan 19 2025 00:00:00 GMT-0600 (Central Stan... | 9907.10 | EUR | pending | 26 | Thu Jun 05 2025 00:00:00 GMT-0500 (Central Dayl... | Heavy we determine whatever million statement. | Sat Dec 13 2025 03:20:41 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:20:41 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:40:15.379Z*
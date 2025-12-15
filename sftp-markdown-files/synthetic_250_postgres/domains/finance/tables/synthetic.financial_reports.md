# financial_reports

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.financial_reports` table stores detailed records of financial reports, each uniquely identified by the primary key `report_id`, including attributes such as the report’s name, type, and associated time period. It references an unspecified external table through a yet undefined relationship, and it logs metadata like creation and update timestamps alongside generating user data. The table's role in the data model is to serve as a repository for financial document information, likely utilized for reporting and auditing purposes, though it is not directly linked or referenced by any other table.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| report_id | integer | NO | This column represents a unique identifier for each financial report within the dataset, ensuring each entry can be distinctly referenced and retrieved. |
| report_name | character varying | NO | This column contains descriptive titles for various financial reports, likely used to identify or categorize the contents of the reports in the context of financial decision-making or policy discussion. Specific details of the reports' topics or their intended audience are unclear from the available data. |
| report_type | character varying | YES | Purpose unclear from available data. |
| period_id | integer | YES | This column likely represents an identifier for specific reporting periods within financial reports, helping to distinguish between different time frames or cycles. Purpose unclear from available data. |
| generated_date | timestamp without time zone | YES | This column records the date and time when the financial report was created, reflecting various dates primarily in Central Time. The purpose of capturing these timestamps is not explicit from the available data. |
| generated_by | integer | YES | This column likely identifies the user or system responsible for creating or submitting the financial report. The specific identification is represented by unique integer IDs, but further context is needed to determine their exact meaning. |
| parameters | jsonb | YES | Purpose unclear from available data. |
| file_path | character varying | YES | Purpose unclear from available data. The sample values appear to contain fragmented text strings with no evident consistent pattern or identifiable business context. |
| created_at | timestamp without time zone | YES | This column records the date and time when a financial report entry is created or logged in the system. The default value suggests it captures the moment a report is recorded unless otherwise specified. |
| updated_at | timestamp without time zone | YES | This column records the date and time when the financial report data was last updated. Purpose is unclear from available data as all sample values show the same timestamp. |

## Primary Key

`report_id`

## Foreign Keys

- `period_id` → `synthetic.fiscal_periods.period_id`

## Indexes

- `financial_reports_pkey`: CREATE UNIQUE INDEX financial_reports_pkey ON synthetic.financial_reports USING btree (report_id)

## Sample Data

| report_id | report_name | report_type | period_id | generated_date | generated_by | parameters | file_path | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Per son son radio factor seven. Tax policy part... | I | 44 | Tue Jun 18 2024 13:03:18 GMT-0500 (Central Dayl... | 6951 | [object Object] | Wear why his. Radio see those not table involve... | Sat Dec 13 2025 02:55:20 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:20 GMT-0600 (Central Stan... |
| 2 | Name significant city seem answer nation today.... | test | 7 | Tue May 13 2025 09:22:07 GMT-0500 (Central Dayl... | 3369 | [object Object] | Firm main mean money nothing project.
Space ear... | Sat Dec 13 2025 02:55:20 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:20 GMT-0600 (Central Stan... |
| 3 | Land movement decision leader nice account. Mee... | while | 35 | Mon Oct 06 2025 13:29:48 GMT-0500 (Central Dayl... | 7131 | [object Object] | Hit green prove whether. Organization song rese... | Sat Dec 13 2025 02:55:20 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:20 GMT-0600 (Central Stan... |
| 4 | Return child station only number guy you.
Land ... | care | 42 | Fri Jan 19 2024 09:09:06 GMT-0600 (Central Stan... | 1182 | [object Object] | Card meet help program simply high. Line possib... | Sat Dec 13 2025 02:55:20 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:20 GMT-0600 (Central Stan... |
| 5 | Skill at young. Four hotel example never become... | including | 48 | Sat Nov 09 2024 16:30:41 GMT-0600 (Central Stan... | 2520 | [object Object] | History ago individual a main almost of want. D... | Sat Dec 13 2025 02:55:20 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:20 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:40:14.438Z*
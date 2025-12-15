# pm_projects

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.pm_projects` table represents project management data, capturing essential details such as project identification (`project_id`), timeline (including `start_date`, `target_end_date`, and `actual_end_date`), and financials (`budget` and `actual_cost`). Although the table references another entity, the specific foreign key relationship is undefined, suggesting it may relate to a broader portfolio or resource management context. As a core table in the data model for managing projects, it tracks project performance indicators like status, priority, and percentage completion along with metadata timestamps for creation and updates.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| project_id | integer | NO | This column represents a unique identifier assigned to each project within the synthetic project management system. It ensures each project can be distinctly referenced. |
| project_code | character varying | YES | This column likely holds unique identifiers for projects, represented as sequences of uppercase letters. Purpose unclear from available data. |
| project_name | character varying | NO | The column represents descriptive and varied names or titles associated with different projects, often involving multiple concepts or themes. Purpose unclear from available data. |
| portfolio_id | integer | YES | This column likely identifies the portfolio associated with a project, with each integer representing a distinct portfolio's identifier. Purpose unclear from available data. |
| description | text | YES | This column contains narrative summaries or explanations related to various projects, possibly describing objectives, status, or contextual background. The exact purpose of these descriptions is unclear from the available data. |
| start_date | date | YES | This column records the initiation date of a project, indicating when it is scheduled to begin or actually commenced. Dates are expressed in Central Time, reflecting whether they occur during Daylight Saving Time or Standard Time. |
| target_end_date | date | YES | This column represents the projected completion date for projects within the project management system. The specific dates indicate when each project is expected to be finished, with flexibility for this date to be unspecified if not yet determined. |
| actual_end_date | date | YES | This column records the actual completion dates of various projects, capturing when the project tasks were finished. The values indicate dates in both Central Standard and Central Daylight time zones, reflecting project end dates throughout different times of the year. |
| status | character varying | YES | This column indicates the current phase or condition of a project, which could be in the planning, currently active, completed, inactive, or cancelled state. The default value suggests most projects initially start in the planning phase. |
| priority | character varying | YES | Purpose unclear from available data; sample values suggest a mix of abstract phrases, making it difficult to ascertain a concrete business meaning. |
| project_manager_id | integer | YES | This column likely identifies individuals designated as project managers, each associated with unique numeric identifiers. The purpose of these identifiers is to link specific projects with their respective managers. |
| budget | numeric | YES | This column represents the financial allocation assigned for various projects, denoted in monetary units. Purpose unclear from available data. |
| actual_cost | numeric | YES | This column represents the real financial expenditure incurred on various projects. The amounts reflect monetary values that vary significantly, indicating varying project scopes or expenses. |
| percent_complete | integer | YES | This column indicates the extent to which a project has been completed, expressed as a percentage. A value of 0 signifies no progress, while a value of 100 denotes full completion. |
| created_at | timestamp without time zone | YES | This column records the date and time when a project was initially created within the system. It automatically defaults to the current timestamp upon project creation, indicating the origin time of projects. |
| updated_at | timestamp without time zone | YES | This column records the timestamp of when each project was last updated. The purpose of the data captured here is to track the most recent changes or modifications made to project details. |

## Primary Key

`project_id`

## Foreign Keys

- `portfolio_id` → `synthetic.project_portfolio.portfolio_id`

## Indexes

- `pm_projects_pkey`: CREATE UNIQUE INDEX pm_projects_pkey ON synthetic.pm_projects USING btree (project_id)
- `pm_projects_project_code_key`: CREATE UNIQUE INDEX pm_projects_project_code_key ON synthetic.pm_projects USING btree (project_code)

## Sample Data

| project_id | project_code | project_name | portfolio_id | description | start_date | target_end_date | actual_end_date | status | priority | project_manager_id | budget | actual_cost | percent_complete | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SSDRFWWLCK | Finish official relationship feeling benefit na... | 50 | Quality prove trial rich family. | Fri Apr 26 2024 00:00:00 GMT-0500 (Central Dayl... | Wed Jul 10 2024 00:00:00 GMT-0500 (Central Dayl... | Fri Sep 12 2025 00:00:00 GMT-0500 (Central Dayl... | inactive | Return million yet. | 4824 | 78074.76 | 77649.25 | 55 | Sat Dec 13 2025 02:59:52 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:59:52 GMT-0600 (Central Stan... |
| 2 | VZSQCHBADB | Detail yourself election.
Hour role top among.
... | 26 | Newspaper too woman sit floor. Unit own front p... | Thu Oct 30 2025 00:00:00 GMT-0500 (Central Dayl... | Tue Mar 12 2024 00:00:00 GMT-0500 (Central Dayl... | Sun Aug 24 2025 00:00:00 GMT-0500 (Central Dayl... | cancelled | Trial finally. | 9173 | 96066.74 | 5571.77 | 79 | Sat Dec 13 2025 02:59:52 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:59:52 GMT-0600 (Central Stan... |
| 3 | XUTZZXYZSD | Major image recently challenge to tough foreign... | 45 | Door something culture everything measure clear... | Fri Dec 15 2023 00:00:00 GMT-0600 (Central Stan... | Fri May 10 2024 00:00:00 GMT-0500 (Central Dayl... | Sun Dec 15 2024 00:00:00 GMT-0600 (Central Stan... | active | Western ok. | 9141 | 47350.46 | 39859.58 | 15 | Sat Dec 13 2025 02:59:52 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:59:52 GMT-0600 (Central Stan... |
| 4 | ZJLPLHQDHG | Event answer easy scene close current. Value sp... | 30 | So buy fill now medical respond. Drop wide oil ... | Sat Oct 04 2025 00:00:00 GMT-0500 (Central Dayl... | Sat Aug 03 2024 00:00:00 GMT-0500 (Central Dayl... | Fri Mar 08 2024 00:00:00 GMT-0600 (Central Stan... | completed | Day condition short. | 501 | 64229.40 | 17474.07 | 27 | Sat Dec 13 2025 02:59:52 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:59:52 GMT-0600 (Central Stan... |
| 5 | BMQTPZHPKG | National eat response might catch term. Blood w... | 20 | Condition audience push push something church. ... | Mon Nov 04 2024 00:00:00 GMT-0600 (Central Stan... | Tue Nov 26 2024 00:00:00 GMT-0600 (Central Stan... | Mon Mar 04 2024 00:00:00 GMT-0600 (Central Stan... | cancelled | Involve business. | 3738 | 52047.38 | 22117.70 | 85 | Sat Dec 13 2025 02:59:52 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:59:52 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:39:23.379Z*
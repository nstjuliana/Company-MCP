# BUDGETS_148

**Database:** synthetic_250_snowflake
**Schema:** SYNTHETIC
**Description:** The SYNTHETIC.BUDGETS_148 table represents budgetary records, each uniquely identifiable by the primary key BUDGET_ID. It captures various attributes, such as the name and description of the budget, associated dates (SOCIAL_168_ATTR_0 and EVENT_168_ATTR_3), contact information (EMAIL_168_ATTR_1), and possibly other related activities or metadata (e.g., WEBINAR_168_ATTR_2), along with tracking details like creation timestamp (CREATED_AT) and version number. This table seems to function independently within the data model, as it lacks direct relationships with other tables in terms of foreign key constraints.

**Row Count:** 10

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| BUDGET_ID | NUMBER | NO | This column represents a unique identifier for each budget entry within the table. The values suggest sequential numbering of distinct budget records. |
| NAME | TEXT | YES | This column represents a sequential identifier for budget entries in the dataset. Each entry is labeled numerically, suggesting the identifier's primary function is to distinguish between different budget records. |
| DESCRIPTION | TEXT | NO | This column contains unique identifiers or labels for individual records within the BUDGETS_148 table, providing a descriptive text for each budget entry. The purpose of these descriptions is unclear from the available data. |
| SOCIAL_168_ATTR_0 | DATE | NO | Purpose unclear from available data. The column contains dates likely related to business or financial events, but the specific context is not discernible from the information provided. |
| EMAIL_168_ATTR_1 | TEXT | YES | This column contains email addresses likely associated with users, potentially identifying contact information for individuals related to budget entries. Purpose unclear from available data. |
| WEBINAR_168_ATTR_2 | TEXT | YES | Purpose unclear from available data. |
| EVENT_168_ATTR_3 | TIMESTAMP_NTZ | YES | This column likely records the date and time of events related to the budget records. Purpose unclear from available data. |
| WEBINAR_168_ATTR_4 | NUMBER | YES | The column appears to represent categorized identifiers associated with a particular aspect of webinars, likely indicating specific attributes or types related to the budget of these webinars. Purpose unclear from available data. |
| CREATED_AT | TIMESTAMP_NTZ | NO | This column records the exact date and time when a budget entry was created, ensuring accurate tracking of budget records. It is automatically populated with the current timestamp at the time of record creation and cannot be left empty. |
| VERSION | NUMBER | NO | This column represents sequential versioning identifiers used to track iterations of budget data, ensuring version control and historical accuracy. The numeric values suggest a linear progression of versions over time. |

## Primary Key

`BUDGET_ID`

## Sample Data

| BUDGET_ID | NAME | DESCRIPTION | SOCIAL_168_ATTR_0 | EMAIL_168_ATTR_1 | WEBINAR_168_ATTR_2 | EVENT_168_ATTR_3 | WEBINAR_168_ATTR_4 | CREATED_AT | VERSION |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | BUDGETS_148 1 | Description for BUDGETS_148 1 | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | user1@example.com | Sample WEBINAR_168_ATTR_2 1 | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | null | Fri Dec 12 2025 11:25:41 GMT-0600 (Central Stan... | 100 |
| 2 | BUDGETS_148 2 | Description for BUDGETS_148 2 | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... | user2@example.com | Sample WEBINAR_168_ATTR_2 2 | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... | 101 | Fri Dec 12 2025 11:25:41 GMT-0600 (Central Stan... | 101 |
| 3 | BUDGETS_148 3 | Description for BUDGETS_148 3 | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... | user3@example.com | Sample WEBINAR_168_ATTR_2 3 | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... | 102 | Fri Dec 12 2025 11:25:41 GMT-0600 (Central Stan... | 102 |
| 4 | BUDGETS_148 4 | Description for BUDGETS_148 4 | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... | user4@example.com | Sample WEBINAR_168_ATTR_2 4 | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... | null | Fri Dec 12 2025 11:25:41 GMT-0600 (Central Stan... | 103 |
| 5 | BUDGETS_148 5 | Description for BUDGETS_148 5 | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... | user5@example.com | Sample WEBINAR_168_ATTR_2 5 | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... | 104 | Fri Dec 12 2025 11:25:41 GMT-0600 (Central Stan... | 104 |

*Generated at: 2025-12-14T23:43:50.303Z*
# fiscal_periods

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.fiscal_periods` table represents a business entity detailing specific fiscal periods, identified uniquely by `period_id`, and includes attributes such as `period_name`, `fiscal_year`, `period_number`, and date ranges (`start_date` and `end_date`). It tracks the status of the fiscal period through the `is_closed` and `closed_date` fields, with timestamps for record management (`created_at` and `updated_at`). As this table has no relationships with other tables, it serves as an isolated reference point for fiscal period information within the data model.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| period_id | integer | NO | This column represents a unique identifier for each fiscal period in the dataset. The sequence of positive integers suggests it is used to sequentially distinguish each fiscal period within the table. |
| period_name | character varying | NO | Purpose unclear from available data. The sample values do not provide sufficient information to discern the business context or meaning. |
| fiscal_year | integer | NO | This column represents the specific calendar year associated with each fiscal period record within the given dataset. It appears to track distinct years in which financial activities or reports are organized. |
| period_number | integer | NO | The values likely represent unique identifiers for different fiscal periods within an organization's calendar. Purpose unclear from available data. |
| start_date | date | NO | This column represents the starting dates of various fiscal periods, likely used for financial or accounting purposes within a specific organization. The dates are consistent with typical fiscal period start dates, such as the beginning of a quarter or fiscal year. |
| end_date | date | NO | This column represents the final date of a fiscal period, indicating when it concludes. The dates reflect variations in daylight saving time and regular time adjustments, suggesting the periods cover different time zones. |
| is_closed | boolean | YES | Indicates whether a fiscal period has been concluded or is still ongoing. A value of true suggests the period is closed, while false indicates it remains open. |
| closed_date | date | YES | This column likely represents the date on which a fiscal period is officially concluded or closed. Purpose unclear from available data. |
| created_at | timestamp without time zone | YES | This column records the exact time and date when a fiscal period entry was created. Purpose unclear from available data. |
| updated_at | timestamp without time zone | YES | This column records the date and time when each fiscal period entry was last modified or updated. Purpose unclear from available data. |

## Primary Key

`period_id`

## Indexes

- `fiscal_periods_pkey`: CREATE UNIQUE INDEX fiscal_periods_pkey ON synthetic.fiscal_periods USING btree (period_id)

## Sample Data

| period_id | period_name | fiscal_year | period_number | start_date | end_date | is_closed | closed_date | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Sure form wonder carry. | 2022 | 9660 | Thu Jan 04 2024 00:00:00 GMT-0600 (Central Stan... | Wed Aug 07 2024 00:00:00 GMT-0500 (Central Dayl... | false | Thu Jan 18 2024 00:00:00 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:16 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:16 GMT-0600 (Central Stan... |
| 2 | Support single history. | 2020 | 3181 | Sun Jan 21 2024 00:00:00 GMT-0600 (Central Stan... | Sun Sep 21 2025 00:00:00 GMT-0500 (Central Dayl... | false | Sat Jan 06 2024 00:00:00 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:16 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:16 GMT-0600 (Central Stan... |
| 3 | Mind visit election kid serve. | 2021 | 5913 | Wed May 29 2024 00:00:00 GMT-0500 (Central Dayl... | Mon Feb 03 2025 00:00:00 GMT-0600 (Central Stan... | true | Wed Nov 19 2025 00:00:00 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:16 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:16 GMT-0600 (Central Stan... |
| 4 | Page bit blue most watch her attack. | 2022 | 232 | Fri Jan 10 2025 00:00:00 GMT-0600 (Central Stan... | Fri Jun 14 2024 00:00:00 GMT-0500 (Central Dayl... | true | Sun Jul 13 2025 00:00:00 GMT-0500 (Central Dayl... | Sat Dec 13 2025 02:54:16 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:16 GMT-0600 (Central Stan... |
| 5 | Grow attack beautiful total. | 2022 | 746 | Tue Jun 10 2025 00:00:00 GMT-0500 (Central Dayl... | Thu Feb 06 2025 00:00:00 GMT-0600 (Central Stan... | true | Thu Apr 11 2024 00:00:00 GMT-0500 (Central Dayl... | Sat Dec 13 2025 02:54:16 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:16 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:40:02.165Z*
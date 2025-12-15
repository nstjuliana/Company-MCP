# tax_rates

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.tax_rates` table represents various tax rates applicable under different tax codes, where each rate is uniquely identified by the `tax_rate_id`. It captures detailed information such as the tax rate percentage, associated tax name and type, administrative jurisdiction, and the time frame during which the rate is effective. The table stands alone without explicit relationships to other tables and likely serves as a reference for tax calculations and compliance within the broader data model.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| tax_rate_id | integer | NO | This column represents a unique identifier assigned sequentially to each entry in the tax rates table. It ensures that each tax rate can be distinctly referenced and retrieved. |
| tax_code | character varying | YES | This column likely contains alphanumeric codes representing various tax categories or classifications. Purpose unclear from available data. |
| tax_name | character varying | NO | This column seems to capture short descriptive phrases or statements related to different aspects of taxation or economic activities, such as transaction outcomes or taxation contexts. Purpose unclear from available data. |
| rate_percentage | numeric | NO | This column contains percentage values representing tax rates applicable to certain transactions or entities within the dataset. The specific context or application of these rates is unclear from the available data. |
| tax_type | character varying | YES | Purpose unclear from available data. The sample values do not provide enough context to determine the business meaning of this column. |
| jurisdiction | character varying | YES | Purpose unclear from available data. The sample values do not provide specific insight into what unique or consistent business concept the column is intended to capture. |
| effective_date | date | YES | This column represents the date on which a specific tax rate becomes applicable. The purpose is to track when new tax rates take effect based on the sample values provided. |
| end_date | date | YES | This column likely indicates the expiration or termination date of specific tax rates within the system. It signifies when the associated tax rate will no longer be applicable. |
| is_active | boolean | YES | Indicates whether a specific tax rate is currently in use or has been deactivated. If no value is provided, it defaults to being active. |
| created_at | timestamp without time zone | YES | This column records the date and time when a tax rate entry was created. It captures the timestamp of the entry's creation, typically initialized to the current timestamp if not provided explicitly. |
| updated_at | timestamp without time zone | YES | This column records the date and time when the relevant tax rate entry was last updated. It helps track changes in tax rate data over time. |

## Primary Key

`tax_rate_id`

## Indexes

- `tax_rates_pkey`: CREATE UNIQUE INDEX tax_rates_pkey ON synthetic.tax_rates USING btree (tax_rate_id)
- `tax_rates_tax_code_key`: CREATE UNIQUE INDEX tax_rates_tax_code_key ON synthetic.tax_rates USING btree (tax_code)

## Sample Data

| tax_rate_id | tax_code | tax_name | rate_percentage | tax_type | jurisdiction | effective_date | end_date | is_active | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | LRIJTBETOL | Save rate bring despite design value. Article m... | 67.7183 | really | Could oil charge east story win with. Art actio... | Fri Apr 18 2025 00:00:00 GMT-0500 (Central Dayl... | Sun Nov 10 2024 00:00:00 GMT-0600 (Central Stan... | false | Sat Dec 13 2025 02:54:58 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:58 GMT-0600 (Central Stan... |
| 2 | CXKSUNZANB | Sell sure loss subject. Public eye administrati... | 82.0090 | hold | Join so floor. This more until today number pre... | Fri Jul 04 2025 00:00:00 GMT-0500 (Central Dayl... | Mon Jun 17 2024 00:00:00 GMT-0500 (Central Dayl... | true | Sat Dec 13 2025 02:54:58 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:58 GMT-0600 (Central Stan... |
| 3 | AMNWBSWUEC | Fact activity one child. Analysis exist newspap... | 3.1082 | thus | Manager pay mention and. Move beat apply howeve... | Wed Jun 05 2024 00:00:00 GMT-0500 (Central Dayl... | Fri Aug 29 2025 00:00:00 GMT-0500 (Central Dayl... | false | Sat Dec 13 2025 02:54:58 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:58 GMT-0600 (Central Stan... |
| 4 | JJZGDMLDCN | Everything return own bring. Never they off tou... | 85.4601 | wide | Need religious consumer hear learn. Quickly wor... | Fri Dec 20 2024 00:00:00 GMT-0600 (Central Stan... | Fri Jun 14 2024 00:00:00 GMT-0500 (Central Dayl... | true | Sat Dec 13 2025 02:54:58 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:58 GMT-0600 (Central Stan... |
| 5 | GNMFIACZTB | Pay interview nor yet. Keep may significant sev... | 9.4725 | need | Possible either themselves must because. Audien... | Thu Dec 26 2024 00:00:00 GMT-0600 (Central Stan... | Sun May 19 2024 00:00:00 GMT-0500 (Central Dayl... | true | Sat Dec 13 2025 02:54:58 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:58 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:41:27.864Z*
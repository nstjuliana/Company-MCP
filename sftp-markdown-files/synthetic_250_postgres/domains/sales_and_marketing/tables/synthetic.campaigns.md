# campaigns

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The "synthetic.campaigns" table represents marketing or promotional campaigns, detailing various attributes such as campaign name, type, status, date range, financials, and performance metrics. It focuses on tracking budgeted versus actual costs and response metrics (e.g., number sent and responses), with no external table relationships indicating standalone operation within the database. This table serves to manage and analyze the efficiency and effectiveness of campaigns over time.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| campaign_id | integer | NO | This column uniquely identifies each marketing campaign within the database, providing a sequential number for organizational purposes. It ensures that each campaign is distinct and can be individually referenced. |
| campaign_name | character varying | NO | This column likely represents descriptive titles or themes of specific campaigns, capturing the key focus or narrative elements used in each campaign for brand messaging or marketing strategies. The purpose is to encapsulate the overall theme or appeal meant to attract or engage a target audience. |
| campaign_type | character varying | YES | This column categorizes various types of campaigns the organization is engaged in. Common themes include initiatives related to innovation, availability, financial matters, and growth activities. |
| status | character varying | YES | This column indicates the current stage or condition of a campaign, with possible statuses such as inactive, active, pending, and completed. Purpose unclear from available data. |
| start_date | date | YES | This column represents the scheduled start date for marketing campaigns, which can occur at various times of the year. The specific initiation date is flexible, allowing for future dates and occasionally encompassing widely recognized time zones adjustments such as daylight savings. |
| end_date | date | YES | This column records the date on which a campaign is scheduled to conclude. If a campaign does not have an assigned end date yet, the entry will be left blank. |
| budgeted_cost | numeric | YES | This column represents the projected or intended expenditure for various marketing initiatives or promotional efforts. The values indicate monetary amounts allocated for these campaigns, allowing for financial planning and resource allocation. |
| actual_cost | numeric | YES | This column represents the financial expenditure incurred in the execution of specific marketing or advertising activities. The values indicate the actual costs associated with various campaigns, reflecting monetary amounts. |
| expected_revenue | numeric | YES | This column likely represents the projected monetary gains in a campaign, expressed in numeric values. Purpose unclear from available data. |
| expected_response | integer | YES | This column represents the projected number of positive responses or engagements expected from a marketing campaign. Purpose unclear from available data beyond numerical projection. |
| num_sent | integer | YES | This column likely represents the number of communications or messages sent during marketing or promotional campaigns. The values indicate a wide range of activity levels across different campaigns. |
| num_responses | integer | YES | This column represents the number of responses received from a campaign, allowing for tracking and analysis of engagement levels. Purpose unclear from available data. |
| description | text | YES | This column contains narrative or promotional content related to individual campaigns, using varied phrases and concepts likely designed to engage or inform an audience. Purpose unclear from available data. |
| owner_id | integer | YES | Represents a unique identifier for the individual or entity responsible for managing or owning a campaign. Purpose unclear from available data. |
| created_at | timestamp without time zone | YES | This column records the exact date and time when each campaign entry was created in the system. The timestamps are set to Central Standard Time, indicating local time zone relevance. |
| updated_at | timestamp without time zone | YES | This column records the date and time when a campaign entry was last modified. It defaults to the current timestamp if no value is provided, indicating when changes are made in the absence of explicit input. |

## Primary Key

`campaign_id`

## Indexes

- `campaigns_pkey`: CREATE UNIQUE INDEX campaigns_pkey ON synthetic.campaigns USING btree (campaign_id)

## Sample Data

| campaign_id | campaign_name | campaign_type | status | start_date | end_date | budgeted_cost | actual_cost | expected_revenue | expected_response | num_sent | num_responses | description | owner_id | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Total force record his. Create program rest bla... | miss | inactive | Wed Apr 10 2024 00:00:00 GMT-0500 (Central Dayl... | Mon Mar 17 2025 00:00:00 GMT-0500 (Central Dayl... | 53010.71 | 34175.61 | 373.35 | 2100 | 6055 | 9263 | Especially against reason watch compare electio... | 7759 | Sat Dec 13 2025 02:58:54 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:54 GMT-0600 (Central Stan... |
| 2 | Describe tough bag work father. Find time just ... | idea | active | Mon Jul 21 2025 00:00:00 GMT-0500 (Central Dayl... | Tue Mar 18 2025 00:00:00 GMT-0500 (Central Dayl... | 1869.21 | 37063.85 | 246.11 | 5345 | 3825 | 5121 | Plan bag company audience series car call. Off ... | 7802 | Sat Dec 13 2025 02:58:54 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:54 GMT-0600 (Central Stan... |
| 3 | War at buy watch bit. Center finish professor e... | firm | pending | Wed Apr 16 2025 00:00:00 GMT-0500 (Central Dayl... | Tue Oct 28 2025 00:00:00 GMT-0500 (Central Dayl... | 55544.08 | 57764.26 | 331.06 | 3185 | 2083 | 5273 | Rich owner newspaper direction successful story... | 9377 | Sat Dec 13 2025 02:58:54 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:54 GMT-0600 (Central Stan... |
| 4 | Fear bed radio. Doctor do actually staff.
Many ... | available | inactive | Tue Apr 08 2025 00:00:00 GMT-0500 (Central Dayl... | Tue Nov 12 2024 00:00:00 GMT-0600 (Central Stan... | 70839.68 | 60977.77 | 813.32 | 4082 | 8006 | 9230 | Air change image level door loss. Join each req... | 7697 | Sat Dec 13 2025 02:58:54 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:54 GMT-0600 (Central Stan... |
| 5 | Year value maybe idea might ready certainly. Pe... | ten | active | Fri Dec 15 2023 00:00:00 GMT-0600 (Central Stan... | Sun Jan 26 2025 00:00:00 GMT-0600 (Central Stan... | 31414.66 | 88084.74 | 384.14 | 2431 | 5270 | 1333 | Third weight area outside. Prevent few presiden... | 8671 | Sat Dec 13 2025 02:58:54 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:54 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:40:31.062Z*
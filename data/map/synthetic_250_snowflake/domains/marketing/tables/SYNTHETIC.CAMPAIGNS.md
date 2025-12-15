# CAMPAIGNS

**Database:** synthetic_250_snowflake
**Schema:** SYNTHETIC
**Description:** The SYNTHETIC.CAMPAIGNS table represents a business entity that manages marketing campaigns, with each campaign identified uniquely by the CAMPAIGN_ID. Key details include the campaign's name, start and end dates, with fields for budget and other campaign attributes such as EMAIL_131_ATTR_0, EVENT_131_ATTR_1, and AD_131_ATTR_2, which suggest this table tracks various campaign-specific characteristics or metrics. This table stands isolated in terms of relationships as it neither references nor is referenced by any other tables, making it primarily a standalone representation of campaign information in the database.

**Row Count:** 10

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| CAMPAIGN_ID | NUMBER | NO | This column represents a unique identifier for each campaign within the dataset. It ensures that each campaign can be distinctly recognized and referenced. |
| NAME | TEXT | NO | This column represents the identifier for different campaigns, likely enumerated or named in a sequential manner. Purpose unclear from available data. |
| START_DATE | DATE | YES | This column likely records the scheduled start date for marketing campaigns within the organization. The data reflects a specific future date and time zone, indicating when a campaign is set to commence. |
| END_DATE | DATE | YES | This column indicates the planned or actual end date for each campaign. It reflects the date when a campaign may conclude or the period it covers ends, with an absence of a date signifying that the end has not been determined. |
| BUDGET | NUMBER | YES | This column represents the monetary allocation for various marketing campaigns. Actual budgets can vary and are not mandatory for every campaign. |
| EMAIL_131_ATTR_0 | NUMBER | YES | This column represents a numerically coded attribute related to email campaigns. The specific purpose of these codes is unclear from the available data. |
| EVENT_131_ATTR_1 | TEXT | YES | Purpose unclear from available data. |
| AD_131_ATTR_2 | TEXT | YES | Purpose unclear from available data. |

## Primary Key

`CAMPAIGN_ID`

## Sample Data

| CAMPAIGN_ID | NAME | START_DATE | END_DATE | BUDGET | EMAIL_131_ATTR_0 | EVENT_131_ATTR_1 | AD_131_ATTR_2 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | CAMPAIGNS 1 | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | Sat Jan 10 2026 18:00:00 GMT-0600 (Central Stan... | null | null | Sample EVENT_131_ATTR_1 1 | Sample AD_131_ATTR_2 1 |
| 2 | CAMPAIGNS 2 | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | Sun Jan 11 2026 18:00:00 GMT-0600 (Central Stan... | 101 | 101 | Sample EVENT_131_ATTR_1 2 | Sample AD_131_ATTR_2 2 |
| 3 | CAMPAIGNS 3 | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | Mon Jan 12 2026 18:00:00 GMT-0600 (Central Stan... | 102 | 102 | Sample EVENT_131_ATTR_1 3 | Sample AD_131_ATTR_2 3 |
| 4 | CAMPAIGNS 4 | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | Tue Jan 13 2026 18:00:00 GMT-0600 (Central Stan... | null | null | Sample EVENT_131_ATTR_1 4 | Sample AD_131_ATTR_2 4 |
| 5 | CAMPAIGNS 5 | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | Wed Jan 14 2026 18:00:00 GMT-0600 (Central Stan... | 104 | 104 | Sample EVENT_131_ATTR_1 5 | Sample AD_131_ATTR_2 5 |

*Generated at: 2025-12-14T23:42:37.012Z*
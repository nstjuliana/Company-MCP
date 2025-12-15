# ANALYTICS

**Database:** synthetic_250_snowflake
**Schema:** SYNTHETIC
**Description:** The SYNTHETIC.ANALYTICS table represents an analytics entity in the "synthetic_250_snowflake" database, capturing various attributes related to events, campaigns, webinars, and emails as indicated by the column names like EVENT_138_ATTR_0, CAMPAIGN_138_ATTR_1, and EMAIL_138_ATTR_5. The table does not have relationships with other tables, suggesting it serves as a standalone entity for analytical purposes within the data model. The primary key, ANALYTIC_ID, uniquely identifies each record, providing essential details such as creation timestamps and descriptions.

**Row Count:** 10

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| ANALYTIC_ID | NUMBER | NO | This column uniquely identifies each entry or record within the analytics table, serving as a sequential count or reference number. |
| NAME | TEXT | NO | This column likely categorizes or enumerates analytics instances or reports within a sequential framework. Each entry appears to identify a unique analytics record in a series. |
| DESCRIPTION | TEXT | YES | This column contains brief textual summaries or identifiers for analytics entries, indicating they are part of a sequential series. Purpose unclear from available data. |
| EVENT_138_ATTR_0 | TIMESTAMP_NTZ | YES | This column likely represents the date and time of specific events or activities, possibly tracking when they are scheduled to occur or have occurred. Purpose unclear from available data. |
| CAMPAIGN_138_ATTR_1 | TEXT | NO | Purpose unclear from available data. |
| WEBINAR_138_ATTR_2 | TEXT | NO | Purpose unclear from available data. |
| WEBINAR_138_ATTR_3 | DATE | YES | This column likely records the scheduled dates for a series of webinars occurring in December 2025. Purpose unclear from available data regarding the significance of "138_ATTR_3". |
| EVENT_138_ATTR_4 | TEXT | YES | Purpose unclear from available data. |
| EMAIL_138_ATTR_5 | TIMESTAMP_NTZ | NO | This column represents a sequence of dates and times, likely corresponding to scheduled events or transactions occurring in the Central Standard Time zone. Purpose unclear from available data. |
| CREATED_AT | TIMESTAMP_NTZ | NO | This column records the exact date and time when each entry in the ANALYTICS table is created, with each timestamp reflecting the Central Standard Time zone. Purpose unclear from available data. |

## Primary Key

`ANALYTIC_ID`

## Sample Data

| ANALYTIC_ID | NAME | DESCRIPTION | EVENT_138_ATTR_0 | CAMPAIGN_138_ATTR_1 | WEBINAR_138_ATTR_2 | WEBINAR_138_ATTR_3 | EVENT_138_ATTR_4 | EMAIL_138_ATTR_5 | CREATED_AT |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ANALYTICS 1 | Description for ANALYTICS 1 | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | Sample CAMPAIGN_138_ATTR_1 1 | Sample WEBINAR_138_ATTR_2 1 | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | Sample EVENT_138_ATTR_4 1 | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | Fri Dec 12 2025 11:25:25 GMT-0600 (Central Stan... |
| 2 | ANALYTICS 2 | Description for ANALYTICS 2 | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... | Sample CAMPAIGN_138_ATTR_1 2 | Sample WEBINAR_138_ATTR_2 2 | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... | Sample EVENT_138_ATTR_4 2 | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... | Fri Dec 12 2025 11:25:25 GMT-0600 (Central Stan... |
| 3 | ANALYTICS 3 | Description for ANALYTICS 3 | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... | Sample CAMPAIGN_138_ATTR_1 3 | Sample WEBINAR_138_ATTR_2 3 | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... | Sample EVENT_138_ATTR_4 3 | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... | Fri Dec 12 2025 11:25:25 GMT-0600 (Central Stan... |
| 4 | ANALYTICS 4 | Description for ANALYTICS 4 | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... | Sample CAMPAIGN_138_ATTR_1 4 | Sample WEBINAR_138_ATTR_2 4 | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... | Sample EVENT_138_ATTR_4 4 | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... | Fri Dec 12 2025 11:25:25 GMT-0600 (Central Stan... |
| 5 | ANALYTICS 5 | Description for ANALYTICS 5 | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... | Sample CAMPAIGN_138_ATTR_1 5 | Sample WEBINAR_138_ATTR_2 5 | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... | Sample EVENT_138_ATTR_4 5 | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... | Fri Dec 12 2025 11:25:25 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:43:17.013Z*
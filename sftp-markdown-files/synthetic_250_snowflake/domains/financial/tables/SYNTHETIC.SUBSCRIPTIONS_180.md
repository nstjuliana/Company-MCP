# SUBSCRIPTIONS_180

**Database:** synthetic_250_snowflake
**Schema:** SYNTHETIC
**Description:** The SYNTHETIC.SUBSCRIPTIONS_180 table represents a collection of subscription records, each uniquely identified by the SUBSCRIPTION_ID primary key. It includes details such as the subscription name, description, specific attributes, and status, with no foreign key relationships to other tables in the database. This table appears to function as a standalone entity, potentially tracking subscription elements and their characteristics over time, as indicated by fields like UPDATED_AT and STATUS.

**Row Count:** 10

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| SUBSCRIPTION_ID | NUMBER | NO | This column represents a unique identifier assigned to each subscription in the database. It ensures that each subscription can be distinctly recognized and referenced. |
| NAME | TEXT | NO | The column identifies individual subscriptions with a unique label based on a sequence pattern "SUBSCRIPTIONS_180" followed by a distinguishing number. Purpose unclear from available data. |
| DESCRIPTION | TEXT | NO | Purpose unclear from available data; sample values suggest this column contains sequentially numbered descriptions related to subscription entries. |
| QUERY_200_ATTR_0 | DATE | YES | The data represents specific dates related to subscription activity or events occurring on or around each date. Purpose unclear from available data. |
| VISUALIZATION_200_ATTR_1 | NUMBER | YES | Purpose unclear from available data. |
| KPI_200_ATTR_2 | TEXT | NO | Purpose unclear from available data. |
| DASHBOARD_200_ATTR_3 | NUMBER | YES | Purpose unclear from available data. |
| VISUALIZATION_200_ATTR_4 | TEXT | YES | Purpose unclear from available data. |
| KPI_200_ATTR_5 | DATE | NO | The column represents a series of consecutive calendar dates in December 2025, likely related to subscription events or milestones occurring daily. The exact business purpose of these dates is unclear from the available data. |
| DASHBOARD_200_ATTR_6 | TEXT | YES | Purpose unclear from available data. |
| UPDATED_AT | TIMESTAMP_NTZ | YES | This column records the date and time when a subscription was last updated, typically logged in the Central Standard Time zone. The purpose of tracking these updates is to maintain a timeline of changes to subscription information. |
| STATUS | TEXT | YES | This column likely indicates the current membership status of a subscription. The repeated presence of "ACTIVE" suggests it is used to denote active or ongoing subscriptions. |

## Primary Key

`SUBSCRIPTION_ID`

## Sample Data

| SUBSCRIPTION_ID | NAME | DESCRIPTION | QUERY_200_ATTR_0 | VISUALIZATION_200_ATTR_1 | KPI_200_ATTR_2 | DASHBOARD_200_ATTR_3 | VISUALIZATION_200_ATTR_4 | KPI_200_ATTR_5 | DASHBOARD_200_ATTR_6 | UPDATED_AT | STATUS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SUBSCRIPTIONS_180 1 | Description for SUBSCRIPTIONS_180 1 | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | null | Sample KPI_200_ATTR_2 1 | null | Sample VISUALIZATION_200_ATTR_4 1 | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | Sample DASHBOARD_200_ATTR_6 1 | Sat Jan 10 2026 18:00:00 GMT-0600 (Central Stan... | ACTIVE |
| 2 | SUBSCRIPTIONS_180 2 | Description for SUBSCRIPTIONS_180 2 | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... | 101 | Sample KPI_200_ATTR_2 2 | 101 | Sample VISUALIZATION_200_ATTR_4 2 | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... | Sample DASHBOARD_200_ATTR_6 2 | Sun Jan 11 2026 18:00:00 GMT-0600 (Central Stan... | ACTIVE |
| 3 | SUBSCRIPTIONS_180 3 | Description for SUBSCRIPTIONS_180 3 | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... | 102 | Sample KPI_200_ATTR_2 3 | 102 | Sample VISUALIZATION_200_ATTR_4 3 | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... | Sample DASHBOARD_200_ATTR_6 3 | Mon Jan 12 2026 18:00:00 GMT-0600 (Central Stan... | ACTIVE |
| 4 | SUBSCRIPTIONS_180 4 | Description for SUBSCRIPTIONS_180 4 | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... | null | Sample KPI_200_ATTR_2 4 | null | Sample VISUALIZATION_200_ATTR_4 4 | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... | Sample DASHBOARD_200_ATTR_6 4 | Tue Jan 13 2026 18:00:00 GMT-0600 (Central Stan... | ACTIVE |
| 5 | SUBSCRIPTIONS_180 5 | Description for SUBSCRIPTIONS_180 5 | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... | 104 | Sample KPI_200_ATTR_2 5 | 104 | Sample VISUALIZATION_200_ATTR_4 5 | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... | Sample DASHBOARD_200_ATTR_6 5 | Wed Jan 14 2026 18:00:00 GMT-0600 (Central Stan... | ACTIVE |

*Generated at: 2025-12-14T23:43:51.225Z*
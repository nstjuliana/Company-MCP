# LEADS_140

**Database:** synthetic_250_snowflake
**Schema:** SYNTHETIC
**Description:** The SYNTHETIC.LEADS_140 table stores information about leads, which are potential opportunities or contacts that the business may pursue, identified by a unique LEAD_ID. Each row captures details such as the lead’s name, description, event attributes, campaign attributes, update timestamp, and current status, with no direct relationships to other tables, indicating it’s a standalone entity in the data model. The presence of timestamp and status columns suggests the table helps track the lifecycle of a lead from creation through to its latest update.

**Row Count:** 10

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| LEAD_ID | NUMBER | NO | This column uniquely identifies each lead in the dataset, serving as a sequential identifier to differentiate between individual lead records. |
| NAME | TEXT | NO | Purpose unclear from available data. |
| DESCRIPTION | TEXT | YES | This column contains textual descriptions associated with specific entries in the LEADS_140 table. Each description appears to provide a unique identifier for the corresponding lead entry. |
| SOCIAL_160_ATTR_0 | NUMBER | YES | This column appears to represent a specific attribute or category related to social interactions or media, indicated by a set of possible numeric identifiers. Purpose unclear from available data. |
| EVENT_160_ATTR_1 | TEXT | NO | Purpose unclear from available data. Sample values do not provide insight into business context or meaning. |
| EVENT_160_ATTR_2 | DATE | YES | This column likely records scheduled or anticipated event dates occurring in mid-December 2025, as evidenced by the sequential daily values within that period. Purpose unclear from available data. |
| CAMPAIGN_160_ATTR_3 | TEXT | YES | Purpose unclear from available data. |
| UPDATED_AT | TIMESTAMP_NTZ | YES | This column represents the date and time when a record was last updated, reflecting changes made to entries in the database. The precise purpose of the timestamp regarding business practices is unclear from the available data. |
| STATUS | TEXT | YES | This field indicates the operational state of a lead, reflecting that it is currently active. Purpose unclear from available data if it supports other statuses. |

## Primary Key

`LEAD_ID`

## Sample Data

| LEAD_ID | NAME | DESCRIPTION | SOCIAL_160_ATTR_0 | EVENT_160_ATTR_1 | EVENT_160_ATTR_2 | CAMPAIGN_160_ATTR_3 | UPDATED_AT | STATUS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | LEADS_140 1 | Description for LEADS_140 1 | null | Sample EVENT_160_ATTR_1 1 | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | Sample CAMPAIGN_160_ATTR_3 1 | Sat Jan 10 2026 18:00:00 GMT-0600 (Central Stan... | ACTIVE |
| 2 | LEADS_140 2 | Description for LEADS_140 2 | 101 | Sample EVENT_160_ATTR_1 2 | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... | Sample CAMPAIGN_160_ATTR_3 2 | Sun Jan 11 2026 18:00:00 GMT-0600 (Central Stan... | ACTIVE |
| 3 | LEADS_140 3 | Description for LEADS_140 3 | 102 | Sample EVENT_160_ATTR_1 3 | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... | Sample CAMPAIGN_160_ATTR_3 3 | Mon Jan 12 2026 18:00:00 GMT-0600 (Central Stan... | ACTIVE |
| 4 | LEADS_140 4 | Description for LEADS_140 4 | null | Sample EVENT_160_ATTR_1 4 | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... | Sample CAMPAIGN_160_ATTR_3 4 | Tue Jan 13 2026 18:00:00 GMT-0600 (Central Stan... | ACTIVE |
| 5 | LEADS_140 5 | Description for LEADS_140 5 | 104 | Sample EVENT_160_ATTR_1 5 | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... | Sample CAMPAIGN_160_ATTR_3 5 | Wed Jan 14 2026 18:00:00 GMT-0600 (Central Stan... | ACTIVE |

*Generated at: 2025-12-14T23:39:50.486Z*
# SCHEDULES_147

**Database:** synthetic_250_snowflake
**Schema:** SYNTHETIC
**Description:** The "SYNTHETIC.SCHEDULES_147" table represents a schedule entity, potentially used to organize or manage webinar events. It contains columns for schedule identification, descriptive details, and associated attributes such as a webinar date, an active status, an email contact, and a campaign identifier. With no foreign or referenced keys, this table appears to function as an isolated entity within the data model rather than being integrated with other tables.

**Row Count:** 10

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| SCHEDULE_ID | NUMBER | NO | This column represents a unique identifier assigned to each schedule entry in the system. The values increment sequentially and are essential for distinguishing between different schedules. |
| NAME | TEXT | YES | This column appears to hold identifiers for schedule instances, likely denoting a sequence or versioning of schedules within a broader set. Purpose unclear from available data beyond indicating a numbered sequence. |
| DESCRIPTION | TEXT | YES | This column provides brief textual descriptions associated with individual schedules within the synthetic dataset. Purpose unclear from available data. |
| WEBINAR_167_ATTR_0 | TIMESTAMP_NTZ | YES | This column records the scheduled start times and dates for a series of webinars, with each entry reflecting the local Central Standard Time. Purpose beyond capturing webinar scheduling information is unclear from available data. |
| AD_167_ATTR_1 | BOOLEAN | YES | Purpose unclear from available data. |
| EMAIL_167_ATTR_2 | TEXT | YES | This column stores email addresses, likely used to identify or contact individuals associated with the schedules in the table. Purpose unclear from available data. |
| CAMPAIGN_167_ATTR_3 | NUMBER | NO | The sequence of numbers suggests that this column likely represents a unique identifier or code associated with specific attributes of a campaign in a scheduling context. Purpose unclear from available data. |

## Primary Key

`SCHEDULE_ID`

## Sample Data

| SCHEDULE_ID | NAME | DESCRIPTION | WEBINAR_167_ATTR_0 | AD_167_ATTR_1 | EMAIL_167_ATTR_2 | CAMPAIGN_167_ATTR_3 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | SCHEDULES_147 1 | Description for SCHEDULES_147 1 | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | true | user1@example.com | 100 |
| 2 | SCHEDULES_147 2 | Description for SCHEDULES_147 2 | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... | false | user2@example.com | 101 |
| 3 | SCHEDULES_147 3 | Description for SCHEDULES_147 3 | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... | true | user3@example.com | 102 |
| 4 | SCHEDULES_147 4 | Description for SCHEDULES_147 4 | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... | false | user4@example.com | 103 |
| 5 | SCHEDULES_147 5 | Description for SCHEDULES_147 5 | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... | true | user5@example.com | 104 |

*Generated at: 2025-12-14T23:39:48.992Z*
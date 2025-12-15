# SCHEDULES_179

**Database:** synthetic_250_snowflake
**Schema:** SYNTHETIC
**Description:** The table 'SCHEDULES_179' in the 'synthetic_250_snowflake' database represents scheduled entities characterized by specific attributes such as a unique identifier, name, description, and various date and string metrics related to visualization, dashboard, and key performance indicators (KPIs). With no foreign keys or external references, this table functions as an isolated dataset storing meta-information about scheduled events. The primary key, SCHEDULE_ID, ensures each schedule entry is distinct and traceable.

**Row Count:** 10

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| SCHEDULE_ID | NUMBER | NO | This column represents a unique identifier for each schedule entry within the database, ensuring that each schedule can be distinctly referenced. Purpose unclear from available data beyond identifying individual schedules. |
| NAME | TEXT | NO | This column appears to list unique schedule identifiers composed of a fixed base text followed by a numeric sequence. Purpose unclear from available data. |
| DESCRIPTION | TEXT | NO | This column contains descriptive identifiers for items in the SCHEDULES_179 table, uniquely distinguishing each schedule with a specific numeric suffix. The purpose of these descriptions is unclear from the available data. |
| QUERY_199_ATTR_0 | NUMBER | NO | This column likely represents a sequential identifier or index for scheduling entries, as indicated by the continuous series of numerical values. |
| VISUALIZATION_199_ATTR_1 | TEXT | YES | Purpose unclear from available data. |
| DASHBOARD_199_ATTR_2 | DATE | NO | This column represents the scheduled dates for a recurring event or activity, occurring daily starting from December 11, 2025. The format suggests a focus on specific days with time detail included, aligning with Central Standard Time. |
| METRIC_199_ATTR_3 | TEXT | YES | Purpose unclear from available data. |
| METRIC_199_ATTR_4 | DATE | NO | This column represents scheduled dates for specific events or activities that occur consecutively day by day. The dates indicate when an event is set to happen, though its exact nature is unclear from the available data. |
| KPI_199_ATTR_5 | TEXT | YES | Purpose unclear from available data. |
| KPI_199_ATTR_6 | TIMESTAMP_NTZ | NO | This column represents scheduled dates and times, likely used for tracking or planning purposes, as evidenced by the sequential daily timestamps. Purpose unclear from available data. |

## Primary Key

`SCHEDULE_ID`

## Sample Data

| SCHEDULE_ID | NAME | DESCRIPTION | QUERY_199_ATTR_0 | VISUALIZATION_199_ATTR_1 | DASHBOARD_199_ATTR_2 | METRIC_199_ATTR_3 | METRIC_199_ATTR_4 | KPI_199_ATTR_5 | KPI_199_ATTR_6 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SCHEDULES_179 1 | Description for SCHEDULES_179 1 | 100 | Sample VISUALIZATION_199_ATTR_1 1 | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | Sample METRIC_199_ATTR_3 1 | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | Sample KPI_199_ATTR_5 1 | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... |
| 2 | SCHEDULES_179 2 | Description for SCHEDULES_179 2 | 101 | Sample VISUALIZATION_199_ATTR_1 2 | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... | Sample METRIC_199_ATTR_3 2 | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... | Sample KPI_199_ATTR_5 2 | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... |
| 3 | SCHEDULES_179 3 | Description for SCHEDULES_179 3 | 102 | Sample VISUALIZATION_199_ATTR_1 3 | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... | Sample METRIC_199_ATTR_3 3 | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... | Sample KPI_199_ATTR_5 3 | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... |
| 4 | SCHEDULES_179 4 | Description for SCHEDULES_179 4 | 103 | Sample VISUALIZATION_199_ATTR_1 4 | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... | Sample METRIC_199_ATTR_3 4 | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... | Sample KPI_199_ATTR_5 4 | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... |
| 5 | SCHEDULES_179 5 | Description for SCHEDULES_179 5 | 104 | Sample VISUALIZATION_199_ATTR_1 5 | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... | Sample METRIC_199_ATTR_3 5 | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... | Sample KPI_199_ATTR_5 5 | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:39:49.424Z*
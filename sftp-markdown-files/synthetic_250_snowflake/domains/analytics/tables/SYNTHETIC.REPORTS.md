# REPORTS

**Database:** synthetic_250_snowflake
**Schema:** SYNTHETIC
**Description:** The SYNTHETIC.REPORTS table represents reports within a specific business context, capturing their identifiers, names, types, creation dates, and various attributes related to the report and its metrics. It serves as a standalone entity with no direct relationships to other tables, holding essential details about each report for analytical or operational purposes. The attributes like REPORT_171_ATTR_0, DASHBOARD_171_ATTR_2, and METRIC_171_ATTR_3 suggest a granular level of detail related to reports and potentially dashboards or metrics associated with them.

**Row Count:** 10

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| REPORT_ID | NUMBER | NO | This column represents the unique identifier assigned to each report entry, ensuring distinction and traceability within the system. Purpose unclear from available data. |
| NAME | TEXT | NO | This column likely represents a categorization or labeling system for sequentially numbered report entities. Each entry seems to designate a distinct report identified by its unique numeric identifier. |
| TYPE | TEXT | YES | This column indicates the status of a report, consistently showing a status of "ACTIVE." Purpose unclear from available data. |
| CREATED_DATE | DATE | NO | This column represents the specific date when an entry was created within the reports system, with each date reflecting the consistent daily creation of new entries. Purpose unclear from available data. |
| REPORT_171_ATTR_0 | TEXT | YES | Purpose unclear from available data. The sample values suggest sequential labeling or categorization. |
| DASHBOARD_171_ATTR_1 | NUMBER | YES | This column likely represents an attribute associated with specific dashboard entries or reports, which are numerically identified. Purpose unclear from available data. |
| DASHBOARD_171_ATTR_2 | TEXT | YES | Purpose unclear from available data. The sample values suggest it is a placeholder or label for a sequence of entries. |
| METRIC_171_ATTR_3 | TEXT | YES | Purpose unclear from available data. The sample values do not provide specific contextual information about what this attribute represents in business terms. |
| CREATED_AT | TIMESTAMP_NTZ | NO | This column records the date and time when a report was generated, serving as a timestamp for the creation event. Each entry reflects the exact moment of report creation in Central Standard Time, with no entry left empty. |

## Primary Key

`REPORT_ID`

## Sample Data

| REPORT_ID | NAME | TYPE | CREATED_DATE | REPORT_171_ATTR_0 | DASHBOARD_171_ATTR_1 | DASHBOARD_171_ATTR_2 | METRIC_171_ATTR_3 | CREATED_AT |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | REPORTS 1 | ACTIVE | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | Sample REPORT_171_ATTR_0 1 | null | Sample DASHBOARD_171_ATTR_2 1 | Sample METRIC_171_ATTR_3 1 | Fri Dec 12 2025 11:27:09 GMT-0600 (Central Stan... |
| 2 | REPORTS 2 | ACTIVE | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... | Sample REPORT_171_ATTR_0 2 | 101 | Sample DASHBOARD_171_ATTR_2 2 | Sample METRIC_171_ATTR_3 2 | Fri Dec 12 2025 11:27:09 GMT-0600 (Central Stan... |
| 3 | REPORTS 3 | ACTIVE | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... | Sample REPORT_171_ATTR_0 3 | 102 | Sample DASHBOARD_171_ATTR_2 3 | Sample METRIC_171_ATTR_3 3 | Fri Dec 12 2025 11:27:09 GMT-0600 (Central Stan... |
| 4 | REPORTS 4 | ACTIVE | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... | Sample REPORT_171_ATTR_0 4 | null | Sample DASHBOARD_171_ATTR_2 4 | Sample METRIC_171_ATTR_3 4 | Fri Dec 12 2025 11:27:09 GMT-0600 (Central Stan... |
| 5 | REPORTS 5 | ACTIVE | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... | Sample REPORT_171_ATTR_0 5 | 104 | Sample DASHBOARD_171_ATTR_2 5 | Sample METRIC_171_ATTR_3 5 | Fri Dec 12 2025 11:27:09 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:43:17.022Z*
# DASHBOARDS

**Database:** synthetic_250_snowflake
**Schema:** SYNTHETIC
**Description:** The SYNTHETIC.DASHBOARDS table represents a collection of dashboard configurations, each uniquely identified by the DASHBOARD_ID, which serves as the primary key. The table stores details about each dashboard including its name, a description, visualization attributes, and associated metrics, as illustrated by columns such as NAME, DESCRIPTION, VISUALIZATION_172_ATTR_0, and METRIC_172_ATTR_1. Since there are no foreign keys or relationships with other tables, this table appears to stand independently within the data model, acting as a repository for dashboard-related metadata.

**Row Count:** 10

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| DASHBOARD_ID | NUMBER | NO | This column represents a unique identifier assigned to each entry within the dashboards table, ensuring each dashboard can be distinctly referenced. |
| NAME | TEXT | NO | This column represents the names of individual dashboards within a system, uniquely identifying each dashboard in a sequence. Purpose unclear from available data. |
| DESCRIPTION | TEXT | YES | This column contains textual descriptions or labels that provide insights or identifiers for different dashboard entries within the table. Each value appears to be a generic description linked to a numerical sequence for dashboards, though the specific purpose of each description is unclear from the sample values. |
| VISUALIZATION_172_ATTR_0 | DATE | YES | This column likely represents a series of consecutive dates, possibly related to scheduled events or data updates. Purpose unclear from available data. |
| METRIC_172_ATTR_1 | TEXT | NO | Purpose unclear from available data. |
| METRIC_172_ATTR_2 | NUMBER | YES | Purpose unclear from available data, but the values suggest a sequential or categorical arrangement that might be used for classification or identification within the context of dashboards. |
| VISUALIZATION_172_ATTR_3 | BOOLEAN | YES | This column likely indicates a binary setting or feature toggle for a certain aspect of a dashboard visualization, potentially turning a specific attribute on or off. Purpose unclear from available data. |

## Primary Key

`DASHBOARD_ID`

## Sample Data

| DASHBOARD_ID | NAME | DESCRIPTION | VISUALIZATION_172_ATTR_0 | METRIC_172_ATTR_1 | METRIC_172_ATTR_2 | VISUALIZATION_172_ATTR_3 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | DASHBOARDS 1 | Description for DASHBOARDS 1 | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | Sample METRIC_172_ATTR_1 1 | null | true |
| 2 | DASHBOARDS 2 | Description for DASHBOARDS 2 | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... | Sample METRIC_172_ATTR_1 2 | 101 | false |
| 3 | DASHBOARDS 3 | Description for DASHBOARDS 3 | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... | Sample METRIC_172_ATTR_1 3 | 102 | true |
| 4 | DASHBOARDS 4 | Description for DASHBOARDS 4 | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... | Sample METRIC_172_ATTR_1 4 | null | false |
| 5 | DASHBOARDS 5 | Description for DASHBOARDS 5 | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... | Sample METRIC_172_ATTR_1 5 | 104 | true |

*Generated at: 2025-12-14T23:43:17.372Z*
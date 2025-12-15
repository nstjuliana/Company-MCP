# FILTERS

**Database:** synthetic_250_snowflake
**Schema:** SYNTHETIC
**Description:** The SYNTHETIC.FILTERS table represents a collection of filter configurations, identified uniquely by FILTER_ID, used within a dashboard or data visualization context. Each filter configuration includes a name, description, and various attributes (DASHBOARD_178_ATTR_0, VISUALIZATION_178_ATTR_1, QUERY_178_ATTR_2, and VISUALIZATION_178_ATTR_3), indicating its integration and application within specific visualizations or queries. This table operates independently within the database, as it neither references nor is referenced by other tables, suggesting it serves as a standalone repository of filters for dashboard functionalities.

**Row Count:** 10

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| FILTER_ID | NUMBER | NO | This column represents a unique identifier for individual filters within the database, ensuring each entry can be distinctly recognized and accessed. Purpose unclear from available data beyond identifying filters. |
| NAME | TEXT | NO | This column appears to represent a sequential naming system or identifiers for a set of filters, labeled numerically. Purpose unclear from available data. |
| DESCRIPTION | TEXT | YES | This column contains textual descriptions or identifiers related to specific filters used within the dataset. The exact purpose of these descriptions is unclear from the available data. |
| DASHBOARD_178_ATTR_0 | NUMBER | NO | This column represents a sequential identifier or code associated with a specific entity or record in the dashboard filter. Purpose unclear from available data. |
| VISUALIZATION_178_ATTR_1 | TEXT | YES | Purpose unclear from available data. |
| QUERY_178_ATTR_2 | DATE | YES | This column likely represents scheduled or recurring date entries around mid-December 2025, presumably related to a specific filter event or process. Purpose unclear from available data. |
| VISUALIZATION_178_ATTR_3 | NUMBER | YES | This column appears to store a set of numerical identifiers used for categorizing or filtering data in a visualization context. Purpose unclear from available data. |

## Primary Key

`FILTER_ID`

## Sample Data

| FILTER_ID | NAME | DESCRIPTION | DASHBOARD_178_ATTR_0 | VISUALIZATION_178_ATTR_1 | QUERY_178_ATTR_2 | VISUALIZATION_178_ATTR_3 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | FILTERS 1 | Description for FILTERS 1 | 100 | Sample VISUALIZATION_178_ATTR_1 1 | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | null |
| 2 | FILTERS 2 | Description for FILTERS 2 | 101 | Sample VISUALIZATION_178_ATTR_1 2 | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... | 101 |
| 3 | FILTERS 3 | Description for FILTERS 3 | 102 | Sample VISUALIZATION_178_ATTR_1 3 | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... | 102 |
| 4 | FILTERS 4 | Description for FILTERS 4 | 103 | Sample VISUALIZATION_178_ATTR_1 4 | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... | null |
| 5 | FILTERS 5 | Description for FILTERS 5 | 104 | Sample VISUALIZATION_178_ATTR_1 5 | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... | 104 |

*Generated at: 2025-12-14T23:39:44.095Z*
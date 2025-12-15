# DATA_SOURCES

**Database:** synthetic_250_snowflake
**Schema:** SYNTHETIC
**Description:** The "SYNTHETIC.DATA_SOURCES" table represents a collection of data sources, each uniquely identified by the primary key column "DATA_SOURCE_ID". It includes metadata such as name, description, and attributes related to metrics, visualizations, queries, and key performance indicators, with timestamps to track updates and versions. The table operates independently within the data model, as it does not have foreign key relationships to or from other tables.

**Row Count:** 10

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| DATA_SOURCE_ID | NUMBER | NO | This column uniquely identifies each entry in the data sources table, serving as a primary identifier. The purpose of these identifiers is to distinguish different data sources within the dataset. |
| NAME | TEXT | NO | This column likely represents identifiers or labels for individual data sources within a larger dataset. Each value sequentially names a data source, denoting its position or version in a series. |
| DESCRIPTION | TEXT | YES | This column contains brief textual descriptions associated with various data sources, likely explaining their purpose or characteristics. The purpose of each description remains generic as reflected in the sample values provided. |
| METRIC_175_ATTR_0 | DATE | NO | This column represents a sequence of consecutive dates likely associated with a timeline or schedule-driven metric in the data source. The precise business purpose of these dates is unclear from the available data. |
| VISUALIZATION_175_ATTR_1 | NUMBER | YES | This field appears to store numerical identifiers related to visualization attributes, possibly indicating different visualization types or configurations. The specific purpose of these identifiers is unclear from the available data. |
| QUERY_175_ATTR_2 | BOOLEAN | YES | Purpose unclear from available data. |
| KPI_175_ATTR_3 | TIMESTAMP_NTZ | YES | This column likely records the timestamp associated with a specific event or action occurring at 6:00 PM over consecutive days. The purpose of these timestamps in the business context is unclear from the available data. |
| UPDATED_AT | TIMESTAMP_NTZ | YES | This column records the date and time when entries in the data source are last updated. The timestamps reflect updates occurring consistently around the same time each day. |
| VERSION | NUMBER | NO | This column represents the sequential iteration or release level of data sources, starting at a default version of 1 and increasing incrementally. The values indicate different stages or updates to the data source over time. |

## Primary Key

`DATA_SOURCE_ID`

## Sample Data

| DATA_SOURCE_ID | NAME | DESCRIPTION | METRIC_175_ATTR_0 | VISUALIZATION_175_ATTR_1 | QUERY_175_ATTR_2 | KPI_175_ATTR_3 | UPDATED_AT | VERSION |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | DATA_SOURCES 1 | Description for DATA_SOURCES 1 | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | null | true | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | Sat Jan 10 2026 18:00:00 GMT-0600 (Central Stan... | 100 |
| 2 | DATA_SOURCES 2 | Description for DATA_SOURCES 2 | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... | 101 | false | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... | Sun Jan 11 2026 18:00:00 GMT-0600 (Central Stan... | 101 |
| 3 | DATA_SOURCES 3 | Description for DATA_SOURCES 3 | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... | 102 | true | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... | Mon Jan 12 2026 18:00:00 GMT-0600 (Central Stan... | 102 |
| 4 | DATA_SOURCES 4 | Description for DATA_SOURCES 4 | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... | null | false | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... | Tue Jan 13 2026 18:00:00 GMT-0600 (Central Stan... | 103 |
| 5 | DATA_SOURCES 5 | Description for DATA_SOURCES 5 | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... | 104 | true | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... | Wed Jan 14 2026 18:00:00 GMT-0600 (Central Stan... | 104 |

*Generated at: 2025-12-14T23:39:44.262Z*
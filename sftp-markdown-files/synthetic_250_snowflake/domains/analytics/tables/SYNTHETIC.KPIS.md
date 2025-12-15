# KPIS

**Database:** synthetic_250_snowflake
**Schema:** SYNTHETIC
**Description:** The SYNTHETIC.KPIS table stores key performance indicators (KPIs) details, with each KPI uniquely identified by KPI_ID. It includes attributes related to the KPI's visualization and reporting properties, such as flags, numeric values, strings, and timestamps. This table stands alone in the data model, as it neither references nor is referenced by other tables, serving as a self-contained repository for KPI definitions and metadata.

**Row Count:** 10

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| KPI_ID | NUMBER | NO | This column represents unique identifiers for specific key performance indicators (KPIs) used in the business context. Each value corresponds to a distinct KPI tracked within the system. |
| NAME | TEXT | NO | This column represents distinct identifiers or labels for KPI entities within the dataset, serving as a clear and simple naming convention to differentiate various key performance indicators. Purpose unclear from available data beyond serving as a distinct label. |
| DESCRIPTION | TEXT | YES | This column contains textual descriptions explaining individual Key Performance Indicators (KPIs) in the KPIS table, contextualizing their significance or characteristics. |
| VISUALIZATION_174_ATTR_0 | BOOLEAN | YES | The column likely indicates whether a particular KPI visualization attribute is enabled or active. Purpose unclear from available data. |
| VISUALIZATION_174_ATTR_1 | NUMBER | NO | This column appears to represent a sequential or categorical identifier within a dataset, but its specific business purpose is unclear from the available data. |
| KPI_174_ATTR_2 | TEXT | YES | Purpose unclear from available data. |
| KPI_174_ATTR_3 | TEXT | NO | Purpose unclear from available data. The sample values do not provide enough context to determine the business meaning. |
| REPORT_174_ATTR_4 | NUMBER | YES | This column appears to store numerical identifiers or codes potentially linked to specific business metrics or attributes, as evidenced by the sample sequential values provided. Purpose unclear from available data. |
| REPORT_174_ATTR_5 | NUMBER | NO | Purpose unclear from available data. |
| VISUALIZATION_174_ATTR_6 | TIMESTAMP_NTZ | NO | This column represents specific dates and times related to key performance indicator events or data points within the system, with entries reflecting daily timestamps. Purpose unclear from available data. |
| CREATED_AT | TIMESTAMP_NTZ | NO | Represents the date and time records were created in the KPIS table, with each entry timestamped at the moment of creation. The specific timing indicates synchronized recording of entries. |

## Primary Key

`KPI_ID`

## Sample Data

| KPI_ID | NAME | DESCRIPTION | VISUALIZATION_174_ATTR_0 | VISUALIZATION_174_ATTR_1 | KPI_174_ATTR_2 | KPI_174_ATTR_3 | REPORT_174_ATTR_4 | REPORT_174_ATTR_5 | VISUALIZATION_174_ATTR_6 | CREATED_AT |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | KPIS 1 | Description for KPIS 1 | true | 100 | Sample KPI_174_ATTR_2 1 | Sample KPI_174_ATTR_3 1 | null | 100 | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | Fri Dec 12 2025 11:26:35 GMT-0600 (Central Stan... |
| 2 | KPIS 2 | Description for KPIS 2 | false | 101 | Sample KPI_174_ATTR_2 2 | Sample KPI_174_ATTR_3 2 | 101 | 101 | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... | Fri Dec 12 2025 11:26:35 GMT-0600 (Central Stan... |
| 3 | KPIS 3 | Description for KPIS 3 | true | 102 | Sample KPI_174_ATTR_2 3 | Sample KPI_174_ATTR_3 3 | 102 | 102 | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... | Fri Dec 12 2025 11:26:35 GMT-0600 (Central Stan... |
| 4 | KPIS 4 | Description for KPIS 4 | false | 103 | Sample KPI_174_ATTR_2 4 | Sample KPI_174_ATTR_3 4 | null | 103 | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... | Fri Dec 12 2025 11:26:35 GMT-0600 (Central Stan... |
| 5 | KPIS 5 | Description for KPIS 5 | true | 104 | Sample KPI_174_ATTR_2 5 | Sample KPI_174_ATTR_3 5 | 104 | 104 | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... | Fri Dec 12 2025 11:26:35 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:43:18.468Z*
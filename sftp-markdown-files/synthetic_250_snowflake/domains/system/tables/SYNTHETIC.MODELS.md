# MODELS

**Database:** synthetic_250_snowflake
**Schema:** SYNTHETIC
**Description:** The SYNTHETIC.MODELS table represents a collection of models characterized by their unique identifiers (MODEL_ID) along with their names and descriptions. It includes various metrics and attributes related to the models, such as timestamps and boolean indicators, but it does not participate in any relationships with other tables, either as a foreign key or being referenced by others. Thus, this table likely serves as a standalone entity for storing and managing detailed model information within the data warehouse.

**Row Count:** 10

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| MODEL_ID | NUMBER | NO | This column likely represents a unique identifier assigned to each model record in the system. These identifiers distinguish between various models within the dataset. |
| NAME | TEXT | NO | This column represents a sequential naming convention used to identify distinct models. Purpose unclear from available data. |
| DESCRIPTION | TEXT | YES | This column contains text descriptions providing specific details or attributes related to individual models within the records. Each entry supplements the corresponding model with contextual or identifying information. |
| METRIC_184_ATTR_0 | TIMESTAMP_NTZ | NO | This column records specific date and time entries that occur consecutively on a daily basis, each at 6:00 PM Central Standard Time. Purpose unclear from available data. |
| METRIC_184_ATTR_1 | NUMBER | YES | Purpose unclear from available data. Sample values suggest it may represent some form of coded metric or identifier, but further context is required for accurate interpretation. |
| METRIC_184_ATTR_2 | DATE | YES | This column appears to represent specific dates related to events or records within the context of a model's lifecycle or activities. Purpose unclear from available data. |
| DASHBOARD_184_ATTR_3 | NUMBER | YES | This column appears to represent a specific attribute or identifier related to a dashboard model, potentially used for categorization or classification, but its exact purpose is unclear from the available data. |
| REPORT_184_ATTR_4 | BOOLEAN | YES | The column appears to indicate a binary status or condition associated with a report, where the status can be either true or false. Purpose unclear from available data. |
| KPI_184_ATTR_5 | TIMESTAMP_NTZ | NO | This column captures specific dates and times in December 2025, potentially related to scheduled or recurring events or milestones. The pattern of consecutive daily timestamps suggests it may track daily occurrences or checkpoints. |

## Primary Key

`MODEL_ID`

## Sample Data

| MODEL_ID | NAME | DESCRIPTION | METRIC_184_ATTR_0 | METRIC_184_ATTR_1 | METRIC_184_ATTR_2 | DASHBOARD_184_ATTR_3 | REPORT_184_ATTR_4 | KPI_184_ATTR_5 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | MODELS 1 | Description for MODELS 1 | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | null | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | null | true | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... |
| 2 | MODELS 2 | Description for MODELS 2 | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... | 101 | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... | 101 | false | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... |
| 3 | MODELS 3 | Description for MODELS 3 | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... | 102 | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... | 102 | true | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... |
| 4 | MODELS 4 | Description for MODELS 4 | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... | null | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... | null | false | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... |
| 5 | MODELS 5 | Description for MODELS 5 | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... | 104 | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... | 104 | true | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:39:48.992Z*
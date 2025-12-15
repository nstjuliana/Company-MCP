# PERFORMANCE_METRICS

**Database:** synthetic_250_snowflake
**Schema:** SYNTHETIC
**Description:** The PERFORMANCE_METRICS table in the synthetic_250_snowflake database represents a collection of metrics related to various performance attributes such as campaign, social, and webinar activities. Each row uniquely identified by the PERFORMANCE_METRIC_ID holds descriptive and specific attributes, indicating specific interactions or results from these activities. As there are no foreign keys or references to other tables, this table functions as a standalone entity within the data model, providing detailed insights into performance metrics for different channels.

**Row Count:** 10

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| PERFORMANCE_METRIC_ID | NUMBER | NO | This column likely serves as a unique identifier for individual performance metrics within the table. The purpose is to distinguish and reference specific metrics in the dataset. |
| NAME | TEXT | NO | This column represents a sequence of identifiers for different performance metrics, where each identifier is distinguished by a numeric suffix. These identifiers likely serve as labels for categorizing or referencing specific set metrics within performance data sets. |
| DESCRIPTION | TEXT | YES | This column contains text descriptions associated with specific performance metrics, providing additional context or details for each metric. Each entry corresponds to a numbered performance metric for identification. |
| CAMPAIGN_149_ATTR_0 | BOOLEAN | YES | The column indicates whether a specific attribute within campaign 149 is active or relevant. Purpose unclear from available data. |
| SOCIAL_149_ATTR_1 | TEXT | YES | Purpose unclear from available data. |
| WEBINAR_149_ATTR_2 | TEXT | YES | Purpose unclear from available data. |
| SOCIAL_149_ATTR_3 | TEXT | NO | Purpose unclear from available data. |

## Primary Key

`PERFORMANCE_METRIC_ID`

## Sample Data

| PERFORMANCE_METRIC_ID | NAME | DESCRIPTION | CAMPAIGN_149_ATTR_0 | SOCIAL_149_ATTR_1 | WEBINAR_149_ATTR_2 | SOCIAL_149_ATTR_3 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | PERFORMANCE_METRICS 1 | Description for PERFORMANCE_METRICS 1 | true | Sample SOCIAL_149_ATTR_1 1 | Sample WEBINAR_149_ATTR_2 1 | Sample SOCIAL_149_ATTR_3 1 |
| 2 | PERFORMANCE_METRICS 2 | Description for PERFORMANCE_METRICS 2 | false | Sample SOCIAL_149_ATTR_1 2 | Sample WEBINAR_149_ATTR_2 2 | Sample SOCIAL_149_ATTR_3 2 |
| 3 | PERFORMANCE_METRICS 3 | Description for PERFORMANCE_METRICS 3 | true | Sample SOCIAL_149_ATTR_1 3 | Sample WEBINAR_149_ATTR_2 3 | Sample SOCIAL_149_ATTR_3 3 |
| 4 | PERFORMANCE_METRICS 4 | Description for PERFORMANCE_METRICS 4 | false | Sample SOCIAL_149_ATTR_1 4 | Sample WEBINAR_149_ATTR_2 4 | Sample SOCIAL_149_ATTR_3 4 |
| 5 | PERFORMANCE_METRICS 5 | Description for PERFORMANCE_METRICS 5 | true | Sample SOCIAL_149_ATTR_1 5 | Sample WEBINAR_149_ATTR_2 5 | Sample SOCIAL_149_ATTR_3 5 |

*Generated at: 2025-12-14T23:43:16.401Z*
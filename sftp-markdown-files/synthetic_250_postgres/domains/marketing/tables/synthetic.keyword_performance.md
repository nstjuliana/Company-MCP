# keyword_performance

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.keyword_performance` table appears to represent business data related to the performance metrics of specific keywords, likely in a marketing or search engine optimization context. The primary key is `kw_perf_id`, which uniquely identifies each record within the table, indicating it potentially serves as a detailed record of keyword performance data but lacks relationship-specific details due to missing column names and foreign key references. The table presently has no rows, so its specific attributes and relationships within the data model remain undefined.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| kw_perf_id | integer | NO | This column uniquely identifies each record in the keyword performance table, ensuring that every entry has a distinct identifier for tracking and analysis purposes. |
| keyword_id | integer | NO | Purpose unclear from available data. |
| date | date | NO | This column likely captures the specific day on which the keyword performance data was recorded or is relevant. It ensures the time-specific tracking of keyword performance metrics. |
| impressions | integer | YES | Represents the number of times a keyword was displayed to users. Purpose unclear from available data. |
| clicks | integer | YES | This column likely tracks the number of times users have selected or engaged with a keyword from the table. The default value of 0 suggests that no interactions have occurred if the field remains empty. |
| conversions | integer | YES | This column likely represents the number of successful actions or outcomes achieved, such as sales or registrations, resulting from a keyword campaign. Purpose unclear from available data due to lack of sample values. |
| spend | numeric | YES | Represents the monetary expenditure associated with keyword marketing activities within the performance dataset. Purpose unclear from available data. |
| avg_position | numeric | YES | This column likely represents the average rank or position of keywords in search results or other performance metrics. Purpose unclear from available data. |
| created_at | timestamp without time zone | YES | This field records the date and time when a keyword performance entry is created or logged, potentially indicating when the associated data was initially captured or added to the system. |
| updated_at | timestamp without time zone | YES | This column likely indicates the last time a record in the keyword performance table was updated, reflecting the most recent changes to the data relevant to keyword analysis. |

## Primary Key

`kw_perf_id`

## Foreign Keys

- `keyword_id` → `synthetic.keywords.keyword_id`

## Indexes

- `keyword_performance_pkey`: CREATE UNIQUE INDEX keyword_performance_pkey ON synthetic.keyword_performance USING btree (kw_perf_id)

*Generated at: 2025-12-14T23:43:23.850Z*
# ad_performance

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The table "synthetic.ad_performance" represents the performance metrics of advertisements, with each entry uniquely identified by the "performance_id" primary key. Although there are no defined relationships, it may serve as a central entity for storing performance data, potentially referencing other tables for more specific details per advertisement. Without column names or data, specific metrics and their roles remain unspecified.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| performance_id | integer | NO | This column uniquely identifies each record of advertisement performance data, ensuring that each entry can be separately tracked and referenced within the dataset. |
| ad_id | integer | NO | This column uniquely identifies each advertisement within the ad performance data. Purpose unclear from available data. |
| date | date | NO | This column records the specific day associated with the performance metrics of advertising campaigns. It ensures that each performance entry is tied to a precise date for accurate tracking and analysis over time. |
| impressions | integer | YES | This column likely tracks the number of times an advertisement is displayed to users. Purpose unclear from available data beyond measuring ad visibility. |
| clicks | integer | YES | The column represents the number of times an advertisement has been clicked by users. It may contain missing values, indicating that the click count is not always recorded. |
| conversions | integer | YES | This column likely tracks the number of successful customer actions resulting from advertisements, such as purchases or sign-ups. It reflects business outcomes attributed to ad campaigns. |
| spend | numeric | YES | The column represents the amount of financial resources allocated to advertising activities, which can be left unspecified if zero. Purpose unclear from available data. |
| cpc | numeric | YES | Purpose unclear from available data. |
| cpm | numeric | YES | Purpose unclear from available data. |
| ctr | numeric | YES | Purpose unclear from available data. |
| conversion_rate | numeric | YES | This column likely quantifies the proportion of successful outcomes or actions in relation to the total number of interactions within an advertising context. Purpose unclear from available data. |
| created_at | timestamp without time zone | YES | This column records the date and time when a record in the ad performance table was created, indicating the inception of the data entry. It helps in tracking the timing of ad performance reports for analysis and auditing purposes. |
| updated_at | timestamp without time zone | YES | Indicates the most recent date and time this advertisement performance record was updated. Purpose unclear from available data due to lack of sample values. |

## Primary Key

`performance_id`

## Foreign Keys

- `ad_id` → `synthetic.ads.ad_id`

## Indexes

- `ad_performance_pkey`: CREATE UNIQUE INDEX ad_performance_pkey ON synthetic.ad_performance USING btree (performance_id)

*Generated at: 2025-12-14T23:40:30.467Z*
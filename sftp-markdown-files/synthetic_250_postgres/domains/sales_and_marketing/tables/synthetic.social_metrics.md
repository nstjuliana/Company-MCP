# social_metrics

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.social_metrics` table is designed to track various metrics related to social interactions, with `metric_id` serving as the unique identifier for each metric in the dataset. Although no specific column names or sample data are available, the table is part of a larger schema in the `synthetic_250_postgres` database and does not currently have any rows or defined relationships to other tables. It appears to play a role in capturing and organizing unspecified social metric data within this synthetic dataset, but without additional context or data, its precise function remains unspecified.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| metric_id | integer | NO | This column uniquely identifies individual social metrics records within the table. Purpose unclear from available data. |
| post_id | integer | NO | This column uniquely identifies each post within the social metrics dataset. It is a mandatory field likely used to associate specific metrics with individual posts. |
| recorded_at | timestamp without time zone | YES | The purpose of this column is unclear from available data due to the absence of sample values. |
| impressions | integer | YES | This column likely represents the number of times a social media post or advertisement has been displayed to users. Purpose unclear from available data. |
| reach | integer | YES | This column likely measures the potential audience size exposed to social media content or campaigns, representing the number of unique individuals reached. Purpose unclear from available data. |
| likes | integer | YES | Represents the number of positive acknowledgments or approvals received on a social media post. The total count may be absent if it wasn't recorded. |
| comments | integer | YES | This column indicates the number of user comments related to a particular social media post or entity. The value can be missing, and it defaults to zero when unspecified. |
| shares | integer | YES | The column represents the number of times a piece of content has been shared across social platforms. If no data is available, it defaults to indicating no shares. |
| clicks | integer | YES | The column likely quantifies user engagements or interactions on social media content within the dataset. Purpose unclear from available data, as sample values were not provided. |
| engagement_rate | numeric | YES | Purpose unclear from available data. |
| created_at | timestamp without time zone | YES | This column captures the date and time when a record was created within the social metrics table. The specific business context or significance of this timestamp is unclear from the available data. |
| updated_at | timestamp without time zone | YES | This column records the date and time when a record in the social metrics table was last modified. It is updated automatically to the current timestamp each time a modification occurs, ensuring changes are tracked chronologically. |

## Primary Key

`metric_id`

## Foreign Keys

- `post_id` → `synthetic.social_posts.post_id`

## Indexes

- `social_metrics_pkey`: CREATE UNIQUE INDEX social_metrics_pkey ON synthetic.social_metrics USING btree (metric_id)

*Generated at: 2025-12-14T23:40:39.175Z*
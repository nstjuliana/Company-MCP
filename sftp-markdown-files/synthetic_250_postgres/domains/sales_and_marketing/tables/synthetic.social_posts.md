# social_posts

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.social_posts` table represents social media posts created for marketing campaigns, capturing details such as the post's content, associated media, and status. Each post is uniquely identified by a `post_id` and is linked to an `account_id` and `campaign_id`, indicating which account created the post and which campaign it belongs to, although the specific tables these foreign keys reference are not defined. The table likely plays a role in tracking and managing the lifecycle of social media post content, including scheduling (`scheduled_at`) and publishing date (`published_at`), across different platforms within a marketing system.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| post_id | integer | NO | This column represents a unique identifier assigned sequentially to each social media post within the system, ensuring each post can be distinctly recognized and accessed. |
| account_id | integer | NO | This column uniquely identifies each user account associated with social media posts. Each integer is a distinct identifier, essential for linking posts to specific users. |
| campaign_id | integer | YES | This column represents an identifier for marketing or promotional campaigns associated with social posts. Purpose unclear from available data as there are no specific patterns or ranges in the sample values. |
| content | text | YES | This column contains narrative or thematic text entries that appear to represent segments of larger written pieces, potentially capturing concepts or thoughts on various topics. Purpose unclear from available data. |
| media_url | character varying | YES | This column contains URLs that likely point to media content associated with social media posts, such as images, videos, or other resources shared in the posts. The purpose of these URLs is to enrich the post's content visually or contextually. |
| scheduled_at | timestamp without time zone | YES | This column represents the date and time a social media post is scheduled to be published. The time zone information indicates schedules are planned according to either Central Daylight Time or Central Standard Time. |
| published_at | timestamp without time zone | YES | This column represents the date and time when a social media post was published, as indicated by the sample values showing specific timestamps of various days in 2024 and 2025. The purpose is to track when each post was publicly shared or went live. |
| status | character varying | YES | This column represents the current state of a social media post, indicating whether it is 'pending', 'active', or 'inactive'. The default state of 'draft' suggests that posts may transition through different statuses during their lifecycle. |
| platform_post_id | character varying | YES | Purpose unclear from available data. The sample values do not clearly indicate a specific business-related function. |
| created_at | timestamp without time zone | YES | This column records the date and time when a social media post was created, based on the current timestamp at the moment of data entry. The timestamp does not include a time zone, but local time context is provided by sample values indicating Central Standard Time. |
| updated_at | timestamp without time zone | YES | This column records the date and time when a social media post in the database was last modified. The presence of the current timestamp as the default suggests it automatically updates to reflect the current time whenever changes are made to the post. |

## Primary Key

`post_id`

## Foreign Keys

- `account_id` → `synthetic.social_accounts.account_id`
- `campaign_id` → `synthetic.marketing_campaigns.campaign_id`

## Indexes

- `social_posts_pkey`: CREATE UNIQUE INDEX social_posts_pkey ON synthetic.social_posts USING btree (post_id)

## Sample Data

| post_id | account_id | campaign_id | content | media_url | scheduled_at | published_at | status | platform_post_id | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 38 | 36 | Ago stage ten side people. Total either seat gr... | https://mcdonald.com/ | Tue Sep 16 2025 11:53:40 GMT-0500 (Central Dayl... | Mon Jan 27 2025 06:24:25 GMT-0600 (Central Stan... | pending | Generation expect argue Mrs. Financial class Co... | Sat Dec 13 2025 03:14:36 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:36 GMT-0600 (Central Stan... |
| 2 | 22 | 43 | Describe owner can million push soldier prove. ... | http://moore.com/ | Tue Jan 09 2024 00:29:24 GMT-0600 (Central Stan... | Sat Jul 05 2025 06:01:26 GMT-0500 (Central Dayl... | active | Consumer can tell western these. Nice gas surfa... | Sat Dec 13 2025 03:14:36 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:36 GMT-0600 (Central Stan... |
| 3 | 27 | 23 | Listen half dream for gas peace many. Place rol... | https://www.schmitt.com/ | Sun Nov 02 2025 14:41:40 GMT-0600 (Central Stan... | Fri Jul 05 2024 09:57:56 GMT-0500 (Central Dayl... | pending | Win debate young west season receive. Table let... | Sat Dec 13 2025 03:14:36 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:36 GMT-0600 (Central Stan... |
| 4 | 49 | 28 | Kid really art fall. Important suffer physical ... | https://www.strickland.info/ | Mon Oct 06 2025 12:29:34 GMT-0500 (Central Dayl... | Wed Jun 19 2024 20:20:14 GMT-0500 (Central Dayl... | pending | Go determine help. | Sat Dec 13 2025 03:14:36 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:36 GMT-0600 (Central Stan... |
| 5 | 4 | 19 | Weight enough civil. Never senior interesting c... | https://barker.biz/ | Sat Nov 02 2024 03:36:57 GMT-0500 (Central Dayl... | Fri Apr 11 2025 23:46:43 GMT-0500 (Central Dayl... | pending | Mother play during rock type hope whole. | Sat Dec 13 2025 03:14:36 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:36 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:40:39.494Z*
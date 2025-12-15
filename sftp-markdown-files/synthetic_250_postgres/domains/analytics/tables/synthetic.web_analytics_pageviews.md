# web_analytics_pageviews

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.web_analytics_pageviews` table represents pageview records for a web analytics system, capturing individual page view events within user sessions. The table is uniquely identified by `pageview_id` and includes details such as `session_id`, `page_url`, `page_title`, `timestamp`, `time_on_page_seconds`, and `referrer`, allowing analysis of how users interact with web content. While this table lacks defined foreign key relationships, its role is likely central to tracking user engagement per session on web pages.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| pageview_id | integer | NO | This column uniquely identifies each individual pageview event within the web analytics system. It is used to track and differentiate user interactions with web pages consistently. |
| session_id | integer | NO | This column represents a unique identifier for each user session on the website, ensuring that page views within the same session can be tracked together. Each number corresponds to a different session, allowing for analysis of user engagement patterns. |
| page_url | character varying | YES | This column represents the URLs of web pages that have been viewed by users. It includes a mix of domain names and protocols, indicating the use of both secure (HTTPS) and non-secure (HTTP) connections to various websites. |
| page_title | character varying | YES | This column likely represents the titles assigned to web pages that are visited and recorded in analytics, reflecting a variety of contexts, such as events, relationships, and environmental themes. Purpose unclear from available data. |
| timestamp | timestamp without time zone | YES | This column records the date and time when a pageview occurs on a website, adjusted for Central Daylight Time. Purpose unclear from available data. |
| time_on_page_seconds | integer | YES | This column represents the duration in seconds that a user spent on a webpage during a single visit. These values can help assess user engagement with online content. |
| referrer | character varying | YES | Purpose unclear from available data. The column appears to store fragmented phrases or sentences with no evident pattern or meaning. |
| created_at | timestamp without time zone | YES | This column captures the date and time when a web page view event was recorded in the system. It defaults to the current timestamp at the moment of record creation, indicating when the view occurred. |
| updated_at | timestamp without time zone | YES | This column captures the precise moment when each record on webpage views was most recently updated or modified. Purpose unclear from available data regarding the nature or source of these updates. |

## Primary Key

`pageview_id`

## Foreign Keys

- `session_id` → `synthetic.web_analytics_sessions.session_id`

## Indexes

- `web_analytics_pageviews_pkey`: CREATE UNIQUE INDEX web_analytics_pageviews_pkey ON synthetic.web_analytics_pageviews USING btree (pageview_id)

## Sample Data

| pageview_id | session_id | page_url | page_title | timestamp | time_on_page_seconds | referrer | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 38 | http://www.rodriguez-reeves.com/ | Effort trip relationship. | Wed Jul 30 2025 08:33:28 GMT-0500 (Central Dayl... | 147 | Dream break hour individual low future station ... | Sat Dec 13 2025 03:14:26 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:26 GMT-0600 (Central Stan... |
| 2 | 15 | https://cruz.com/ | Area fast environmental. | Fri Oct 24 2025 00:46:40 GMT-0500 (Central Dayl... | 473 | Image politics push cut about cut. Moment creat... | Sat Dec 13 2025 03:14:26 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:26 GMT-0600 (Central Stan... |
| 3 | 41 | https://adams.org/ | Garden same. | Sun Oct 05 2025 19:41:18 GMT-0500 (Central Dayl... | 261 | Which option over car. Short record soldier kno... | Sat Dec 13 2025 03:14:26 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:26 GMT-0600 (Central Stan... |
| 4 | 30 | https://soto.com/ | Always rock tonight soldier. | Fri Aug 09 2024 21:59:31 GMT-0500 (Central Dayl... | 262 | Establish build support child concern. | Sat Dec 13 2025 03:14:26 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:26 GMT-0600 (Central Stan... |
| 5 | 43 | https://www.alvarado.com/ | Husband sometimes force shake. | Wed Sep 24 2025 00:13:13 GMT-0500 (Central Dayl... | 10 | Huge once argue ahead she pull history. | Sat Dec 13 2025 03:14:26 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:26 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:44:08.173Z*
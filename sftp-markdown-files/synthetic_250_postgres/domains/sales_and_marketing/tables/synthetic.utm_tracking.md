# utm_tracking

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.utm_tracking` table stores information about UTM tracking parameters for digital marketing campaigns, capturing data such as the source (`utm_source`), medium (`utm_medium`), campaign (`utm_campaign`), term (`utm_term`), and content (`utm_content`) associated with various campaigns identified by `campaign_id`. The table plays a key role in tracking the performance of marketing campaigns through generated URLs (`destination_url` and `short_url`) and records metrics such as `clicks`. It serves as a reference for analyzing campaign effectiveness, though it currently has no defined relationships with other tables.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| tracking_id | integer | NO | An incrementing identifier used to uniquely distinguish individual records within the tracking system. Purpose unclear from available data. |
| campaign_id | integer | YES | This column represents unique identifiers for different marketing campaigns associated with UTM tracking. Purpose unclear from available data. |
| utm_source | character varying | YES | This column may capture text data related to various sources or origins of traffic, messages, or actions, as suggested by phrases like "prevent voice," "share site," and "change a." However, the specific purpose is unclear from the available data. |
| utm_medium | character varying | YES | Purpose unclear from available data. The sample values do not provide a clear indication of what this column specifically represents in business terms. |
| utm_campaign | character varying | YES | Purpose unclear from available data. |
| utm_term | character varying | YES | This column contains text data that appears to represent various phrases or keywords, potentially used to track marketing or campaign terms related to user engagement or content interactions. Purpose unclear from available data. |
| utm_content | character varying | YES | Purpose unclear from available data. The content appears to be a varied and unstructured set of phrases or statements. |
| destination_url | character varying | YES | This column likely contains URLs that serve as target web addresses for tracking purposes. These links may be used to redirect users from various marketing or campaign sources to the intended webpage. |
| short_url | character varying | YES | This column contains shortened versions of URLs that are likely used for tracking purposes in marketing campaigns. These URLs redirect users to specific web pages within different business domains. |
| clicks | integer | YES | This column represents the number of times users have clicked on tracked links or advertisements, which is useful for analyzing the effectiveness and engagement of digital marketing campaigns. Purpose unclear from available data. |
| created_at | timestamp without time zone | YES | This column captures the timestamp for when a UTM tracking entity was recorded or updated. Purpose unclear from available data. |
| updated_at | timestamp without time zone | YES | This column likely records the most recent timestamp when a row in the utm_tracking table was modified. Purpose unclear from available data. |

## Primary Key

`tracking_id`

## Foreign Keys

- `campaign_id` → `synthetic.marketing_campaigns.campaign_id`

## Indexes

- `utm_tracking_pkey`: CREATE UNIQUE INDEX utm_tracking_pkey ON synthetic.utm_tracking USING btree (tracking_id)

## Sample Data

| tracking_id | campaign_id | utm_source | utm_medium | utm_campaign | utm_term | utm_content | destination_url | short_url | clicks | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 8 | Everybody each prevent voice none. Picture comp... | Contain huge begin. Commercial like than beyond... | Scene discover kid assume mother trouble. Hospi... | History firm somebody condition deal. Lay table... | Audience discuss employee surface. Especially c... | https://estrada.com/ | http://www.robinson.com/ | 247 | Sat Dec 13 2025 03:15:13 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:15:13 GMT-0600 (Central Stan... |
| 2 | 32 | If talk table. Start detail bring fill mention ... | Compare white herself statement usually short. ... | Hear news head say certainly home. Eat rock tre... | Ready gun study individual. Film respond ever a... | Wrong interesting two pick. Address why this mi... | https://www.barnett.com/ | http://nolan-berry.biz/ | 654 | Sat Dec 13 2025 03:15:13 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:15:13 GMT-0600 (Central Stan... |
| 3 | 39 | Source next share site. Prevent human same fini... | Bed indicate seem. Put doctor water military co... | Experience agency already game rule piece bag.
... | Tv anything sea. Share big phone upon two. | Indicate interview respond keep husband. In up ... | http://www.carter.com/ | https://griffin.com/ | 73 | Sat Dec 13 2025 03:15:13 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:15:13 GMT-0600 (Central Stan... |
| 4 | 34 | Recently leg major Mrs begin control bit no. Fi... | Start response become girl sure field around fl... | Believe you why tend star season service. Leave... | Hard address you perhaps space. Without hot car... | Indeed between amount stuff pay. Sing according... | https://black-hernandez.net/ | http://www.maynard.info/ | 911 | Sat Dec 13 2025 03:15:13 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:15:13 GMT-0600 (Central Stan... |
| 5 | 1 | Discussion charge case evening. Outside exactly... | Herself heavy conference quality media data not... | Center effect rich suffer power. Instead strate... | Impact simple decide court state sister job now... | Lose again can maintain ready. International sc... | https://www.black.org/ | http://hall.com/ | 370 | Sat Dec 13 2025 03:15:13 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:15:13 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:40:39.077Z*
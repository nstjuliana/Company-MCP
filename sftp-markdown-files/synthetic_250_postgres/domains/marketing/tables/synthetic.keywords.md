# keywords

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The "synthetic.keywords" table represents keywords associated with advertising campaigns, where each entry identifies a unique keyword linked to an ad group, its match type, bid amount, quality score, and status within the campaign lifecycle. The table references another table through the "ad_group_id" to associate keywords with specific ad groups, but no further table information is specified. Its role in the data model likely includes facilitating keyword performance tracking and optimization by providing essential details like bid amounts and quality scores.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| keyword_id | integer | NO | This column represents a unique identifier for each keyword within the dataset, incrementing sequentially to distinguish individual records. Purpose unclear from available data. |
| ad_group_id | integer | YES | This column appears to represent identifier numbers for groups related to advertisements. Purpose unclear from available data. |
| keyword | character varying | NO | This column contains descriptive phrases or sentences, likely used for categorizing or identifying various topics or themes within records. Purpose unclear from available data. |
| match_type | character varying | YES | Purpose unclear from available data. |
| bid_amount | numeric | YES | This column represents the monetary amount associated with bids, potentially indicating the cost or price for keywords in marketing or advertising auctions. The purpose is to track or analyze variations in bid amounts across different instances or campaigns. |
| quality_score | integer | YES | This column represents a numerical evaluation of the quality associated with each keyword in a table, with higher scores indicating better quality. The purpose or criteria for determining the quality score are unclear from the available data. |
| status | character varying | YES | This column indicates the current state of a keyword, showing whether it's in use ('active'), temporarily on hold ('pending'), or not in use ('inactive'). Purpose unclear from available data. |
| created_at | timestamp without time zone | YES | This column represents the date and time when a record in the keywords table was created or logged. It defaults to the current timestamp if no value is provided, but it may also be left empty. |
| updated_at | timestamp without time zone | YES | This column records the last update date and time for the keyword entries in the dataset. It indicates when the data was most recently modified or confirmed. |

## Primary Key

`keyword_id`

## Foreign Keys

- `ad_group_id` → `synthetic.ad_groups.ad_group_id`

## Indexes

- `keywords_pkey`: CREATE UNIQUE INDEX keywords_pkey ON synthetic.keywords USING btree (keyword_id)

## Sample Data

| keyword_id | ad_group_id | keyword | match_type | bid_amount | quality_score | status | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 40 | Field executive structure clearly. Quite thing ... | Technology message wind outside line. | 6380.91 | 957 | pending | Sat Dec 13 2025 03:14:56 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:56 GMT-0600 (Central Stan... |
| 2 | 31 | Assume all international middle me cup includin... | Concern professor score first what my hundred. | 6596.25 | 17 | active | Sat Dec 13 2025 03:14:56 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:56 GMT-0600 (Central Stan... |
| 3 | 35 | Walk carry back tough thank step quality. | Maintain around make subject response guess term. | 5520.92 | 13 | active | Sat Dec 13 2025 03:14:56 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:56 GMT-0600 (Central Stan... |
| 4 | 34 | Hair north ready hand officer behavior. Describ... | Majority field skill drop Mr. | 7224.71 | 549 | inactive | Sat Dec 13 2025 03:14:56 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:56 GMT-0600 (Central Stan... |
| 5 | 2 | Different defense happen fill. Throughout perso... | This realize suggest less. | 5027.14 | 715 | pending | Sat Dec 13 2025 03:14:56 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:56 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:43:23.557Z*
# ad_groups

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The "synthetic.ad_groups" table represents individual groups of advertisements associated with advertising campaigns, where each group is identified by a unique "ad_group_id" and linked to an "ad_campaign_id." This table holds critical details including the ad group name, targeting information, bid amount, status, and timestamps for creation and updates. The table's role in the data model is to detail and manage each ad group's attributes and configurations within broader ad campaigns, evidenced by its primary key and linkage to ad campaigns through foreign key relationships.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| ad_group_id | integer | NO | This column represents the unique identifier for each advertising group within the dataset, with values incrementing sequentially. |
| ad_campaign_id | integer | NO | This column represents a unique identifier associated with advertising campaigns, linking ad groups to specific campaigns in the business context. Each number corresponds to a distinct campaign managed in the ad system. |
| ad_group_name | character varying | NO | The column represents descriptive labels or titles assigned to different groups of advertisements. The names appear to be varied and creative, possibly reflecting campaign themes or slogans. |
| targeting | jsonb | YES | Purpose unclear from available data. |
| bid_amount | numeric | YES | This column represents the monetary value allocated for a payment or offering associated with ad groups, likely indicating the budget or financial investment intended per instance. Purpose unclear from available data regarding the exact role or context of these financial values within ad group operations. |
| status | character varying | YES | This column indicates the current state of advertising groups, typically identifying their operational status as 'active', 'inactive', or 'pending'. It helps monitor and manage the workflow and engagement of these advertising groups. |
| created_at | timestamp without time zone | YES | This column records the date and time when an advertisement group was created, defaulting to the current timestamp. Purpose and further distinguishing characteristics are unclear from available data. |
| updated_at | timestamp without time zone | YES | This column logs the date and time of the last update made to an entry in the advertising groups. The timestamp indicates when any changes were last recorded in these specific data records. |

## Primary Key

`ad_group_id`

## Foreign Keys

- `ad_campaign_id` → `synthetic.ad_campaigns.ad_campaign_id`

## Indexes

- `ad_groups_pkey`: CREATE UNIQUE INDEX ad_groups_pkey ON synthetic.ad_groups USING btree (ad_group_id)

## Sample Data

| ad_group_id | ad_campaign_id | ad_group_name | targeting | bid_amount | status | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 34 | Executive may person college. Yard ahead stay s... | [object Object] | 1538.62 | active | Sat Dec 13 2025 03:14:46 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:46 GMT-0600 (Central Stan... |
| 2 | 11 | Focus summer true set they. | [object Object] | 3233.38 | pending | Sat Dec 13 2025 03:14:46 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:46 GMT-0600 (Central Stan... |
| 3 | 15 | Cell benefit letter house. Easy though size. | [object Object] | 3466.77 | pending | Sat Dec 13 2025 03:14:46 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:46 GMT-0600 (Central Stan... |
| 4 | 19 | Join data exist statement spring speech brother... | [object Object] | 8460.88 | inactive | Sat Dec 13 2025 03:14:46 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:46 GMT-0600 (Central Stan... |
| 5 | 13 | Later later know brother. Cost left member hers... | [object Object] | 6354.22 | pending | Sat Dec 13 2025 03:14:46 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:46 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:40:29.808Z*
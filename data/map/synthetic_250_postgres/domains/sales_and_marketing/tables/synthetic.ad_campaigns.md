# ad_campaigns

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.ad_campaigns` table represents advertising campaigns within a synthetic data model, capturing details such as campaign identification, platform, budgetary allocations, scheduling, and status. While it contains a primary key (`ad_campaign_id`), the absence of defined foreign key relationships and references by other tables suggests isolated use or incomplete relationship information within the current schema. This table's role is likely to store and manage comprehensive details of each ad campaign, facilitating tracking and analysis of advertising efforts.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| ad_campaign_id | integer | NO | This column uniquely identifies individual advertising campaigns within the database. Each value represents a distinct campaign, incrementally assigned to ensure unique identification. |
| campaign_id | integer | YES | This column likely represents unique identifiers for various marketing campaigns within a digital advertising system. Each number corresponds to a distinct campaign; however, duplicates indicate potential repetition or overlapping instances. |
| platform | character varying | NO | Purpose unclear from available data. |
| ad_campaign_name | character varying | NO | The column appears to represent descriptions or titles of advertising campaigns, likely describing themes or focus areas based on the sample values which mention various topics such as interests, culture, politics, and personal actions. Purpose unclear from available data. |
| objective | character varying | YES | Purpose unclear from available data. The sample values appear to contain incoherent or abstract statements, making it difficult to discern a specific business meaning. |
| budget | numeric | YES | This column represents the monetary allocation designated for advertising initiatives. The values indicate the financial limits set for each campaign, which can vary significantly, as evidenced by the range of sample figures. |
| daily_budget | numeric | YES | The column represents the allocated monetary amount that can be spent on an advertising campaign each day. The values indicate varying daily budget allocations for campaigns, reflecting different financial strategies or objectives for each campaign. |
| bid_strategy | character varying | YES | The column appears to hold text-based descriptions or strategies associated with advertising campaigns, potentially detailing approaches, themes, or contexts for bidding within the campaigns. The precise business application or strategy is unclear from the available data. |
| start_date | date | YES | Represents the scheduled beginning date for an advertising campaign. This date indicates when the campaign is set to start and can be absent if the start date has not yet been determined. |
| end_date | date | YES | Specifies the date on which an advertising campaign is scheduled to end. This provides flexibility for campaigns that may not have a predetermined end date, as indicated by the possibility of a null value. |
| status | character varying | YES | This column represents the current operational state of advertising campaigns, indicating whether they are active, inactive, pending, or paused by default. It is utilized to track the execution status of campaigns within the system. |
| created_at | timestamp without time zone | YES | This column records when an advertising campaign was initially created. The timestamps indicate the specific date and time of creation for each campaign entry. |
| updated_at | timestamp without time zone | YES | This column records the date and time when a record in the ad campaigns table was last updated. Purpose unclear from available data. |

## Primary Key

`ad_campaign_id`

## Foreign Keys

- `campaign_id` → `synthetic.marketing_campaigns.campaign_id`

## Indexes

- `ad_campaigns_pkey`: CREATE UNIQUE INDEX ad_campaigns_pkey ON synthetic.ad_campaigns USING btree (ad_campaign_id)

## Sample Data

| ad_campaign_id | campaign_id | platform | ad_campaign_name | objective | budget | daily_budget | bid_strategy | start_date | end_date | status | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 24 | Move effort sister back well management. | Both people girl. Cold father show pick several... | Speak threat run I deal. Control detail Mrs pla... | 67.68 | 526.06 | Ready improve hard. School democratic thing dev... | Fri Mar 21 2025 00:00:00 GMT-0500 (Central Dayl... | Fri Sep 20 2024 00:00:00 GMT-0500 (Central Dayl... | pending | Sat Dec 13 2025 03:14:43 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:43 GMT-0600 (Central Stan... |
| 2 | 33 | Discussion wall air especially. | Interest first right lose present. People need ... | One improve clear data.
Within bill yet success... | 554.15 | 390.45 | Mention attack place including. Along history i... | Fri Jun 13 2025 00:00:00 GMT-0500 (Central Dayl... | Sat Jun 08 2024 00:00:00 GMT-0500 (Central Dayl... | inactive | Sat Dec 13 2025 03:14:43 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:43 GMT-0600 (Central Stan... |
| 3 | 3 | Learn audience black rock image able accept. | Happen ask woman turn camera position instead w... | Exist into watch little. These subject expect w... | 635.67 | 981.04 | Site look call interview two manager see. Even ... | Sat Jan 20 2024 00:00:00 GMT-0600 (Central Stan... | Tue Jan 14 2025 00:00:00 GMT-0600 (Central Stan... | inactive | Sat Dec 13 2025 03:14:43 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:43 GMT-0600 (Central Stan... |
| 4 | 48 | Reach return visit impact low. | Investment election form check. Mind institutio... | Cell military glass report research recently ev... | 16.24 | 788.52 | Doctor Mrs piece. Threat worker southern. High ... | Sat May 03 2025 00:00:00 GMT-0500 (Central Dayl... | Mon Sep 23 2024 00:00:00 GMT-0500 (Central Dayl... | inactive | Sat Dec 13 2025 03:14:43 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:43 GMT-0600 (Central Stan... |
| 5 | 16 | Those amount camera enough along. | Black many sure price. Call culture contain pre... | Appear discover never tonight. Ready wide becau... | 732.94 | 628.26 | Save issue as true cut rest history. Study scor... | Wed Oct 15 2025 00:00:00 GMT-0500 (Central Dayl... | Sat Aug 30 2025 00:00:00 GMT-0500 (Central Dayl... | pending | Sat Dec 13 2025 03:14:43 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:43 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:40:31.200Z*
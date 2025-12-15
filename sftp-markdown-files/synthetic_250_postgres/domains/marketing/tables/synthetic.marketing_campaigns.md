# marketing_campaigns

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.marketing_campaigns` table represents marketing campaign records encompassing various attributes such as campaign type, channel, status, timeframe, budget, and audience. Each campaign is uniquely identified by the `campaign_id` primary key, with no direct relationships to other tables indicated within the database schema. The table's role is to store detailed information about each marketing campaign, facilitating tracking and analysis of campaign effectiveness and expenditure.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| campaign_id | integer | NO | This column uniquely identifies each marketing campaign within the database. The purpose is to ensure each campaign can be individually referenced and tracked. |
| campaign_name | character varying | NO | This column represents creative or thematic slogans or narratives associated with different marketing campaigns. The descriptions appear to encapsulate various aspects or themes, likely intending to evoke specific ideas or emotions in target audiences. |
| campaign_type | character varying | YES | The column represents descriptive labels for various marketing campaign themes or strategies. Purpose unclear from available data. |
| channel | character varying | YES | Purpose unclear from available data. The sample values do not provide a clear indication of the business concept represented by this column. |
| status | character varying | YES | This column indicates the current state or phase of a marketing campaign, such as whether it is actively running, pending, or inactive. The default setting suggests that campaigns are initially in a draft phase before moving to other statuses. |
| start_date | date | YES | This column represents the scheduled start dates of marketing campaigns, indicating when each campaign is planned to commence. These dates can vary, potentially aligning with specific events or time periods, and may not always be set, as shown by the potential for null values. |
| end_date | date | YES | This column represents the concluding date of marketing campaigns, indicating when the promotional efforts are scheduled to end. The dates indicate campaigns occur across various months and years, suggesting ongoing marketing activities over time. |
| budget | numeric | YES | This column represents the allocated financial resources for individual marketing campaigns, expressed as monetary values. These amounts likely indicate the level of investment in marketing initiatives; however, the specific purpose or outcome of these budgets is unclear from the available data. |
| actual_spend | numeric | YES | This column represents the expenditure in monetary units allocated for various marketing campaigns. Purpose unclear from available data. |
| target_audience | text | YES | Purpose unclear from available data. The sample values suggest varied topics that do not indicate a clear thematic focus. |
| goals | text | YES | This column stores descriptive narratives or statements related to specific marketing campaign objectives, strategies, or themes. Purpose unclear from available data regarding how these narratives influence or categorize the campaigns. |
| owner_id | integer | YES | This column represents identifiers for individuals or entities responsible for managing or executing marketing campaigns. Purpose unclear from available data. |
| created_at | timestamp without time zone | YES | This column marks the specific date and time when a marketing campaign record was initially entered into the system. The default setting ensures that new entries have a timestamp upon creation, though it is possible for this field to remain empty if desired. |
| updated_at | timestamp without time zone | YES | The date and time indicate when a marketing campaign record was last updated, with the potential for records being created or modified in the future. Purpose unclear from available data. |

## Primary Key

`campaign_id`

## Indexes

- `marketing_campaigns_pkey`: CREATE UNIQUE INDEX marketing_campaigns_pkey ON synthetic.marketing_campaigns USING btree (campaign_id)

## Sample Data

| campaign_id | campaign_name | campaign_type | channel | status | start_date | end_date | budget | actual_spend | target_audience | goals | owner_id | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Every into walk thing sport. Player beautiful f... | Pattern treat second. | Range amount large collection us shake tough. | pending | Wed Oct 16 2024 00:00:00 GMT-0500 (Central Dayl... | Sat Sep 14 2024 00:00:00 GMT-0500 (Central Dayl... | 108.10 | 872.17 | Full quickly story surface. Face low enter able... | Arm accept leave fear blue glass reveal. Great ... | 880 | Sat Dec 13 2025 03:14:02 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:02 GMT-0600 (Central Stan... |
| 2 | Cause section accept third. Book expect card in... | Body blue again choose. | Face magazine set easy check memory economic. | inactive | Sun May 05 2024 00:00:00 GMT-0500 (Central Dayl... | Sun May 11 2025 00:00:00 GMT-0500 (Central Dayl... | 222.43 | 816.59 | Particularly country talk pick chance build hus... | Imagine fill plan discuss from look. | 472 | Sat Dec 13 2025 03:14:02 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:02 GMT-0600 (Central Stan... |
| 3 | Best add necessary technology. Guess special se... | Cover knowledge better walk people. | Industry represent through service suffer. | inactive | Wed Oct 22 2025 00:00:00 GMT-0500 (Central Dayl... | Sat Dec 14 2024 00:00:00 GMT-0600 (Central Stan... | 305.19 | 795.35 | Out recent can animal. | Some really scientist however. That will close ... | 234 | Sat Dec 13 2025 03:14:02 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:02 GMT-0600 (Central Stan... |
| 4 | Break possible plan win foot watch this. Reveal... | Food daughter picture teach house. | Country make role positive. | active | Sun Apr 27 2025 00:00:00 GMT-0500 (Central Dayl... | Sat Apr 27 2024 00:00:00 GMT-0500 (Central Dayl... | 23.66 | 193.13 | Interview lawyer population I. Case seek activi... | Eat base central physical. | 337 | Sat Dec 13 2025 03:14:02 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:02 GMT-0600 (Central Stan... |
| 5 | Whatever blood save.
Dark lose none know. Film ... | Time page concern most. | Sing chair challenge land. | inactive | Wed Jun 25 2025 00:00:00 GMT-0500 (Central Dayl... | Sun Aug 25 2024 00:00:00 GMT-0500 (Central Dayl... | 864.35 | 966.89 | Loss win own PM catch want. Himself near much m... | Dog able yes admit. Listen card body treat gues... | 286 | Sat Dec 13 2025 03:14:02 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:02 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:43:25.904Z*
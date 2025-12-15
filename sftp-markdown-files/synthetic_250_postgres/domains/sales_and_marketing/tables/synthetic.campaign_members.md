# campaign_members

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.campaign_members` table represents entities that are involved in marketing campaigns, identified by a unique `member_id`. Each member is associated with a specific `campaign_id` and optionally linked to leads through `lead_id` and contacts through `contact_id`, capturing their `status` and response dates in the campaign lifecycle. Though it has foreign key placeholders indicating relationships with other tables, the lack of details limits further relationship insights.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| member_id | integer | NO | This column represents a unique identifier assigned to each member involved in a campaign. It sequentially increases for each additional member added. |
| campaign_id | integer | NO | This column represents the unique identifiers for different marketing or promotional campaigns. It is used to associate members with specific campaigns they are part of. |
| lead_id | integer | YES | A unique identifier for each individual lead related to various campaigns. Purpose unclear from available data. |
| contact_id | integer | YES | Purpose unclear from available data. |
| status | character varying | YES | This column represents the current standing or progress of individuals within a campaign, indicating whether they are active, pending, inactive, cancelled, or completed. Purpose unclear from available data. |
| responded_date | date | YES | This column records the dates on which campaign members responded to a campaign, with values ranging across various dates and time zones. Purpose unclear from available data. |
| first_responded_date | date | YES | The column records the date when a campaign member first responded to a campaign. This information is used to track engagement timelines across different time zones, as evidenced by the sample dates provided with their respective Central Time indicators. |
| created_at | timestamp without time zone | YES | This column records the date and time when an entry was created in the campaign members table. The purpose or additional context of this timestamp is unclear from the available data. |
| updated_at | timestamp without time zone | YES | This column captures the most recent time at which an entry within the campaign members table was modified. It may not always be filled since it's optional, but defaults to the current time when unspecified. |

## Primary Key

`member_id`

## Foreign Keys

- `campaign_id` → `synthetic.campaigns.campaign_id`
- `contact_id` → `synthetic.contacts.contact_id`
- `lead_id` → `synthetic.leads.lead_id`

## Indexes

- `campaign_members_pkey`: CREATE UNIQUE INDEX campaign_members_pkey ON synthetic.campaign_members USING btree (member_id)

## Sample Data

| member_id | campaign_id | lead_id | contact_id | status | responded_date | first_responded_date | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 43 | 11 | null | inactive | Sun Aug 31 2025 00:00:00 GMT-0500 (Central Dayl... | Fri Feb 07 2025 00:00:00 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:57 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:57 GMT-0600 (Central Stan... |
| 2 | 44 | 46 | null | pending | Mon Dec 30 2024 00:00:00 GMT-0600 (Central Stan... | Mon Aug 19 2024 00:00:00 GMT-0500 (Central Dayl... | Sat Dec 13 2025 02:58:57 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:57 GMT-0600 (Central Stan... |
| 3 | 32 | 8 | null | pending | Tue May 14 2024 00:00:00 GMT-0500 (Central Dayl... | Sun Apr 27 2025 00:00:00 GMT-0500 (Central Dayl... | Sat Dec 13 2025 02:58:57 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:57 GMT-0600 (Central Stan... |
| 4 | 47 | 24 | null | cancelled | Wed Dec 03 2025 00:00:00 GMT-0600 (Central Stan... | Sat Dec 28 2024 00:00:00 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:57 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:57 GMT-0600 (Central Stan... |
| 5 | 26 | 34 | null | completed | Fri Mar 01 2024 00:00:00 GMT-0600 (Central Stan... | Tue May 20 2025 00:00:00 GMT-0500 (Central Dayl... | Sat Dec 13 2025 02:58:57 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:57 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:40:29.734Z*
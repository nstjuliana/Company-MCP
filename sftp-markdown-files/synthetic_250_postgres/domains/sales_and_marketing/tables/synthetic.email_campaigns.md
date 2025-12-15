# email_campaigns

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.email_campaigns` table represents email marketing campaigns within a broader synthetic marketing database, with each campaign identified by a unique `email_campaign_id`. This table contains key attributes for managing email campaigns, such as `subject_line`, `from_name`, `from_email`, `reply_to`, `template_id`, as well as scheduling and status information, evidenced by fields like `scheduled_date`, `sent_date`, and `status`. Although the exact foreign key relationships are undefined, its role seems to be central in tracking the lifecycle and details of email marketing activities, likely linking to unspecified campaign and template management tables.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| email_campaign_id | integer | NO | Uniquely identifies each email campaign within the system. Each value increments by one to ensure distinct campaign identifiers over time. |
| campaign_id | integer | YES | This field likely associates an email campaign with its unique identifier number, enabling the organization to track and manage different marketing initiatives. Each number represents a distinct campaign, but the specific purpose or content of each campaign is not discernible from the values provided. |
| subject_line | character varying | NO | This column contains textual entries that appear to represent creative or promotional messages, potentially used as subject lines for email marketing campaigns. Purpose unclear from available data. |
| from_name | character varying | YES | This column likely contains the names or identifiers associated with the senders of email campaigns, reflecting different themes or subjects. Purpose unclear from available data. |
| from_email | character varying | YES | This column represents the email addresses used as the sender's address for various email campaigns. The sender addresses appear to be personal or individual email accounts from different email service providers. |
| reply_to | character varying | YES | Purpose unclear from available data. The sample values consist of seemingly random phrases that do not clearly convey a specific meaning or purpose. |
| template_id | integer | YES | This column likely identifies different templates used in email campaigns, with each numeric value representing a distinct template option. Purpose unclear from available data beyond this identification function. |
| scheduled_date | timestamp without time zone | YES | This column represents the planned date and time when an email campaign is scheduled to be sent. It may remain unspecified as its values can be null. |
| sent_date | timestamp without time zone | YES | This column records the date and time when individual email campaigns were sent, likely indicating when recipients should have received the emails. The variety in timestamps reflects campaigns across different dates and seasons. |
| status | character varying | YES | This column indicates the current state of an email marketing campaign, which can be either pending, active, or inactive. It helps track the progress or readiness of campaigns in the marketing process. |
| created_at | timestamp without time zone | YES | This column records the date and time when an email campaign was created. It defaults to the current timestamp at the time of record insertion. |
| updated_at | timestamp without time zone | YES | This column records the date and time when a change was last made to an email campaign record. The current timestamp is used by default if a specific time is not provided during an update. |

## Primary Key

`email_campaign_id`

## Foreign Keys

- `campaign_id` → `synthetic.marketing_campaigns.campaign_id`
- `template_id` → `synthetic.email_templates.template_id`

## Indexes

- `email_campaigns_pkey`: CREATE UNIQUE INDEX email_campaigns_pkey ON synthetic.email_campaigns USING btree (email_campaign_id)

## Sample Data

| email_campaign_id | campaign_id | subject_line | from_name | from_email | reply_to | template_id | scheduled_date | sent_date | status | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 36 | Last modern purpose laugh level. Item Mrs name ... | Oil security perhaps national challenge item. B... | pamela61@example.net | Meeting movie film. Economy fund magazine catch... | 50 | Tue Oct 29 2024 05:09:20 GMT-0500 (Central Dayl... | Thu Feb 01 2024 10:59:29 GMT-0600 (Central Stan... | pending | Sat Dec 13 2025 03:18:41 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:18:41 GMT-0600 (Central Stan... |
| 2 | 39 | Factor drive or. Region company what wide too a... | Money way general. | megan84@example.net | Arrive lose live agreement. Stay fish cause for... | 31 | Sun Jan 21 2024 08:07:42 GMT-0600 (Central Stan... | Wed Dec 18 2024 12:54:49 GMT-0600 (Central Stan... | pending | Sat Dec 13 2025 03:18:41 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:18:41 GMT-0600 (Central Stan... |
| 3 | 43 | Cold yet table enough herself. Different stuff ... | Sport strong the recent. Scientist task from si... | ewheeler@example.org | How away country hard visit. Effort box cold boy. | 24 | Wed Apr 02 2025 16:48:15 GMT-0500 (Central Dayl... | Tue Mar 18 2025 12:14:58 GMT-0500 (Central Dayl... | pending | Sat Dec 13 2025 03:18:41 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:18:41 GMT-0600 (Central Stan... |
| 4 | 29 | No source determine. Take kid drop strategy. | Care off management. | zimmermanernest@example.com | Book feeling cause mouth. Father hold discussio... | 8 | Thu Jan 30 2025 16:25:30 GMT-0600 (Central Stan... | Mon Oct 13 2025 20:04:04 GMT-0500 (Central Dayl... | active | Sat Dec 13 2025 03:18:41 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:18:41 GMT-0600 (Central Stan... |
| 5 | 49 | Might fall determine pull trade deal. Piece act... | Voice four feeling end sell. Win throughout aga... | olewis@example.net | Concern decide term current development choice.... | 43 | Fri Apr 19 2024 20:18:11 GMT-0500 (Central Dayl... | Sun May 26 2024 01:56:35 GMT-0500 (Central Dayl... | active | Sat Dec 13 2025 03:18:41 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:18:41 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:40:31.112Z*
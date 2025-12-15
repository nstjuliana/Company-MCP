# email_sends

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The table "synthetic.email_sends" represents individual records of email communications sent within a campaign, capturing details such as the recipient's email, the timing of key events (e.g., sent, delivered, opened, clicked), and status indicators (e.g., bounced, unsubscribed). It is primarily linked to an "email_campaign_id" indicating it references an undefined table that likely details different email campaigns. This table serves as a log of email interactions, capturing the lifecycle of each send attempt for analysis and tracking purposes.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| send_id | integer | NO | This column represents a unique identifier for each email send event in the system. It sequentially tracks individual email dispatches within the database. |
| email_campaign_id | integer | NO | This column represents unique identifiers for different email campaigns, allowing each campaign to be distinctly tracked or referenced within the system. |
| recipient_email | character varying | NO | This column represents the email addresses of individuals to whom messages have been sent. It captures the unique electronic identifiers within a messaging or communication system. |
| contact_id | integer | YES | This field likely represents a unique identifier for contacts related to email sends. Its specific purpose is unclear from the available data. |
| sent_at | timestamp without time zone | YES | This column indicates the date and time when an email was sent within the specified timezone. The purpose is related to tracking communication events, but further details are unclear from the available data. |
| delivered_at | timestamp without time zone | YES | This column records the date and time when an email was successfully delivered. The timing of delivery may vary between standard and daylight saving time, reflecting different time zones within Central Time. |
| opened_at | timestamp without time zone | YES | This column records the date and time when an email was opened by the recipient. The timestamp indicates the specific moment of interaction in the recipient's local timezone. |
| clicked_at | timestamp without time zone | YES | This column records the date and time when an email recipient clicked on a link within the sent email. The information helps track engagement by indicating when recipients interact with email content. |
| bounced | boolean | YES | Indicates whether an email sent has failed to be delivered to the recipient. A value of true means the email bounced, while false means it was successfully delivered or its delivery status is unknown. |
| bounce_type | character varying | YES | Purpose unclear from available data. |
| unsubscribed | boolean | YES | This column indicates whether an individual has opted out of receiving further emails. A value of "true" denotes that the individual has unsubscribed, while "false" indicates they are still subscribed. |
| created_at | timestamp without time zone | YES | This column records the date and time when an email was initially sent or logged in the system. The purpose is unclear from the available data. |
| updated_at | timestamp without time zone | YES | This column records the date and time when an email send record was last updated, defaulting to the current timestamp. Purpose unclear from available data. |

## Primary Key

`send_id`

## Foreign Keys

- `email_campaign_id` → `synthetic.email_campaigns.email_campaign_id`

## Indexes

- `email_sends_pkey`: CREATE UNIQUE INDEX email_sends_pkey ON synthetic.email_sends USING btree (send_id)

## Sample Data

| send_id | email_campaign_id | recipient_email | contact_id | sent_at | delivered_at | opened_at | clicked_at | bounced | bounce_type | unsubscribed | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 43 | bjohnson@example.net | 58 | Thu Jun 20 2024 07:35:04 GMT-0500 (Central Dayl... | Wed Feb 07 2024 08:49:44 GMT-0600 (Central Stan... | Fri Dec 05 2025 14:40:02 GMT-0600 (Central Stan... | Sun Dec 08 2024 07:39:52 GMT-0600 (Central Stan... | true | Enjoy attorney former trouble. | false | Sat Dec 13 2025 03:18:45 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:18:45 GMT-0600 (Central Stan... |
| 2 | 49 | benjamin51@example.com | 805 | Thu Feb 13 2025 01:03:22 GMT-0600 (Central Stan... | Thu Feb 27 2025 09:26:55 GMT-0600 (Central Stan... | Mon Oct 07 2024 06:41:06 GMT-0500 (Central Dayl... | Fri Jan 26 2024 17:54:55 GMT-0600 (Central Stan... | true | Information situation claim within through away. | false | Sat Dec 13 2025 03:18:45 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:18:45 GMT-0600 (Central Stan... |
| 3 | 44 | john28@example.org | 257 | Thu Nov 14 2024 07:46:52 GMT-0600 (Central Stan... | Tue Dec 09 2025 15:13:06 GMT-0600 (Central Stan... | Fri Jun 21 2024 20:36:34 GMT-0500 (Central Dayl... | Fri Jan 24 2025 00:16:51 GMT-0600 (Central Stan... | true | Modern list kid prevent avoid quite brother. | true | Sat Dec 13 2025 03:18:45 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:18:45 GMT-0600 (Central Stan... |
| 4 | 45 | aprilyoung@example.com | 804 | Tue Nov 18 2025 14:59:56 GMT-0600 (Central Stan... | Fri Jan 12 2024 00:23:05 GMT-0600 (Central Stan... | Sat Nov 09 2024 20:43:14 GMT-0600 (Central Stan... | Sun Aug 24 2025 04:28:31 GMT-0500 (Central Dayl... | false | Nature necessary case need thousand yard make. | true | Sat Dec 13 2025 03:18:45 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:18:45 GMT-0600 (Central Stan... |
| 5 | 49 | brettgonzales@example.net | 555 | Sat Oct 18 2025 20:37:12 GMT-0500 (Central Dayl... | Sun Aug 10 2025 17:55:10 GMT-0500 (Central Dayl... | Sat Aug 09 2025 20:12:49 GMT-0500 (Central Dayl... | Sat Oct 05 2024 14:32:17 GMT-0500 (Central Dayl... | true | Here teacher edge sea. | false | Sat Dec 13 2025 03:18:45 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:18:45 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:40:38.216Z*
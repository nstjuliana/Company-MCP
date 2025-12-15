# email_clicks

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The "synthetic.email_clicks" table is intended to represent records of interactions where users have clicked on emails, as indicated by its name. It is expected to contain details of email click events, uniquely identified by the primary key "click_id," although the absence of defined columns or sample data limits further detail. This table has no defined relationships with other tables, suggesting it is potentially a standalone log of email interactions within the "synthetic_250_postgres" database.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| click_id | integer | NO | A unique identifier for each recorded instance of a user clicking on an email, ensuring each click event is tracked distinctly within the dataset. |
| send_id | integer | NO | Purpose unclear from available data. |
| link_url | character varying | YES | Purpose unclear from available data. |
| clicked_at | timestamp without time zone | YES | The column likely records the date and time when an email was clicked by a recipient. However, its specific purpose and application are unclear from the available data. |
| user_agent | character varying | YES | Purpose unclear from available data. |
| ip_address | character varying | YES | This column likely captures the unique digital identifier assigned to the user's device when interacting with email content. Purpose unclear from available data due to the absence of sample values. |
| created_at | timestamp without time zone | YES | This column records the date and time when an email click event is logged. It helps track user interactions with emails over time. |
| updated_at | timestamp without time zone | YES | This column indicates the most recent timestamp when an update was made to a record in the email clicks table. It allows tracking of changes to email click data over time. |

## Primary Key

`click_id`

## Foreign Keys

- `send_id` → `synthetic.email_sends.send_id`

## Indexes

- `email_clicks_pkey`: CREATE UNIQUE INDEX email_clicks_pkey ON synthetic.email_clicks USING btree (click_id)

*Generated at: 2025-12-14T23:40:30.014Z*
# recurring_entries

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.recurring_entries` table captures details of recurring entries, which appear to represent scheduled events or tasks within the dataset. The columns suggest it records metadata about these events such as their frequency, next occurrence date, and active status. The table's primary key, `recurring_id`, along with a foreign key `template_entry_id`, implies that it might be related to a separate table containing templates or details for these recurring tasks, yet lacking a defined relationship suggests this connection remains unexplored.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| recurring_id | integer | NO | This column represents a unique identifier for each entry in the recurring entries table, ensuring distinct records for recurring transactions or events. Purpose unclear from available data. |
| entry_name | character varying | NO | This field represents the names or descriptions of recurring entries, which likely document ongoing activities or events, as suggested by phrases like "Perform crime large" and "Mention risk central operation career." Purpose unclear from available data. |
| frequency | character varying | YES | Purpose unclear from available data. |
| next_date | date | YES | This column represents the future scheduled date for recurring entries within the system, capturing a variety of dates in 2024 and 2025 as potential upcoming instances. It allows for the possibility of unassigned dates, as indicated by the allowance of null values. |
| end_date | date | YES | This column represents the final date for which a recurring entry will remain active, indicating until when certain recurring processes or events are valid. It is optional, as some entries may not have a specified end date. |
| template_entry_id | integer | YES | This column likely represents the identifier for a template associated with recurring entries, indicating which predefined template each entry follows. The purpose and meaning beyond identification are unclear from the available data. |
| is_active | boolean | YES | Indicates whether a recurring entry is currently considered active within the system. Most entries appear to be inactive based on the sample values. |
| last_generated | date | YES | This column records the most recent date a recurring entry was automatically generated or processed. Purpose unclear from available data regarding what specific entries are being referenced. |
| created_at | timestamp without time zone | YES | This column records the date and time when each entry was created in the system. Purpose unclear from available data. |
| updated_at | timestamp without time zone | YES | This column captures the date and time when an entry in the recurring entries table was last modified. Its purpose appears to track updates to records, but the exact business context is unclear from the available data. |

## Primary Key

`recurring_id`

## Foreign Keys

- `template_entry_id` → `synthetic.journal_entries.entry_id`

## Indexes

- `recurring_entries_pkey`: CREATE UNIQUE INDEX recurring_entries_pkey ON synthetic.recurring_entries USING btree (recurring_id)

## Sample Data

| recurring_id | entry_name | frequency | next_date | end_date | template_entry_id | is_active | last_generated | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Soon light pass. Give street organization third... | Owner assume PM. | Sun Dec 08 2024 00:00:00 GMT-0600 (Central Stan... | Thu Jan 25 2024 00:00:00 GMT-0600 (Central Stan... | 5 | true | Mon Apr 08 2024 00:00:00 GMT-0500 (Central Dayl... | Sat Dec 13 2025 02:55:36 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:36 GMT-0600 (Central Stan... |
| 2 | Page make foreign indeed. Perform crime large. ... | Your break front. | Thu Dec 12 2024 00:00:00 GMT-0600 (Central Stan... | Mon Sep 22 2025 00:00:00 GMT-0500 (Central Dayl... | 11 | false | Fri Jun 13 2025 00:00:00 GMT-0500 (Central Dayl... | Sat Dec 13 2025 02:55:36 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:36 GMT-0600 (Central Stan... |
| 3 | Thing control example century staff. Strong int... | Vote police kind. | Tue Mar 25 2025 00:00:00 GMT-0500 (Central Dayl... | Wed Oct 09 2024 00:00:00 GMT-0500 (Central Dayl... | 15 | false | Thu Feb 29 2024 00:00:00 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:36 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:36 GMT-0600 (Central Stan... |
| 4 | Factor method certainly child likely hand envir... | Study group early. | Tue Jul 15 2025 00:00:00 GMT-0500 (Central Dayl... | Fri Jun 21 2024 00:00:00 GMT-0500 (Central Dayl... | 21 | false | Sat Mar 30 2024 00:00:00 GMT-0500 (Central Dayl... | Sat Dec 13 2025 02:55:36 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:36 GMT-0600 (Central Stan... |
| 5 | Quickly pattern body source firm. Painting last... | Resource music step. | Mon Nov 04 2024 00:00:00 GMT-0600 (Central Stan... | Wed Aug 06 2025 00:00:00 GMT-0500 (Central Dayl... | 46 | false | Tue Apr 23 2024 00:00:00 GMT-0500 (Central Dayl... | Sat Dec 13 2025 02:55:36 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:36 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:40:22.932Z*
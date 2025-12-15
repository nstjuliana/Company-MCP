# academic_calendar

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The "synthetic.academic_calendar" table represents scheduled academic events, capturing details such as event names, types, and dates, specifically within an academic term, as indicated by the nullable foreign key "term_id". The table records whether an event is a holiday, and includes timestamps for creation and last update, showcasing its role in tracking the timeline and details of academic activities. This table serves as a central repository for academic event management, although currently it stands alone without defined external foreign key relationships.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| event_id | integer | NO | This column uniquely identifies each event in the academic calendar with a sequential number. It ensures that each calendar event can be distinctly referenced and tracked. |
| term_id | integer | YES | Identifies specific academic terms within an educational institution's calendar. Purpose unclear from available data. |
| event_name | character varying | NO | This field records a brief, descriptive title or label for various scheduled events within an academic calendar. The exact nature of these events is unclear from the available data. |
| event_type | character varying | YES | Purpose unclear from available data. The sample values do not provide sufficient context to determine the column's meaning. |
| start_date | date | NO | This column represents the beginning dates of specific academic periods or terms within the academic calendar. It indicates when these periods are scheduled to commence. |
| end_date | date | YES | This column represents the concluding date of an academic period or event as indicated by the sample values which align with the typical end of semesters or terms. The specific purpose of these dates remains unclear from the available data. |
| description | text | YES | Purpose unclear from available data. The entries seem to consist of fragmented sentences or phrases which do not form a clear pattern or context. |
| is_holiday | boolean | YES | Indicates whether a specific day in the academic calendar is recognized as a holiday. Days marked with "true" are holidays, while those with "false" are not. |
| created_at | timestamp without time zone | YES | Represents the date and time when an entry in the academic calendar was created. The recorded timestamp reflects the Central Standard Time zone. |
| updated_at | timestamp without time zone | YES | This column records the date and time when entries in the academic calendar table were last updated. The timestamp is captured automatically, defaulting to the current system time when updates occur. |

## Primary Key

`event_id`

## Foreign Keys

- `term_id` → `synthetic.academic_terms.term_id`

## Indexes

- `academic_calendar_pkey`: CREATE UNIQUE INDEX academic_calendar_pkey ON synthetic.academic_calendar USING btree (event_id)

## Sample Data

| event_id | term_id | event_name | event_type | start_date | end_date | description | is_holiday | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 48 | Quite including west. | Hope people wife Democrat individual. | Fri Nov 14 2025 00:00:00 GMT-0600 (Central Stan... | Thu Jul 03 2025 00:00:00 GMT-0500 (Central Dayl... | A choice necessary might under structure end. S... | true | Sat Dec 13 2025 03:17:15 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:17:15 GMT-0600 (Central Stan... |
| 2 | 20 | Mrs share direction scene. Prove always mouth b... | Everyone today machine turn dinner environmental. | Fri Nov 07 2025 00:00:00 GMT-0600 (Central Stan... | Thu Jul 18 2024 00:00:00 GMT-0500 (Central Dayl... | Manage interest force deep skill politics team. | true | Sat Dec 13 2025 03:17:15 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:17:15 GMT-0600 (Central Stan... |
| 3 | 29 | Movement speak finish system total small. Liste... | Answer country yard later should government trip. | Thu Jun 13 2024 00:00:00 GMT-0500 (Central Dayl... | Fri Jan 03 2025 00:00:00 GMT-0600 (Central Stan... | Vote system group down improve note trade risk.... | false | Sat Dec 13 2025 03:17:15 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:17:15 GMT-0600 (Central Stan... |
| 4 | 23 | Cold mother space I sign everyone church. Peopl... | Bank travel ball camera benefit deep accept city. | Mon Sep 22 2025 00:00:00 GMT-0500 (Central Dayl... | Mon Dec 16 2024 00:00:00 GMT-0600 (Central Stan... | Land gas finally agent. Minute common some born... | true | Sat Dec 13 2025 03:17:15 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:17:15 GMT-0600 (Central Stan... |
| 5 | 29 | Cultural little system score ahead. Key accept ... | Cover kind his series left. | Tue Mar 18 2025 00:00:00 GMT-0500 (Central Dayl... | Thu Feb 06 2025 00:00:00 GMT-0600 (Central Stan... | Dog peace center instead. Write small certain e... | true | Sat Dec 13 2025 03:17:15 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:17:15 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:40:51.301Z*
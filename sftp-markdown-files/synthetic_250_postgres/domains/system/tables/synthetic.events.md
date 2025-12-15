# events

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.events` table represents scheduled events or activities, characterized by details such as a subject, description, location, start and end dates, and whether the event lasts all day. Each event is uniquely identified by `event_id` and is potentially linked to other entities via `related_to_type` and `related_to_id`, although it does not reference any other tables nor is it referenced by others. This table is likely used to manage and track information specific to each event within the overall data model, documenting critical event attributes and ownership details, as suggested by the `owner_id`.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| event_id | integer | NO | This column uniquely identifies each event within the database, providing a sequential number for reference. Purpose beyond identification is unclear from available data. |
| subject | character varying | NO | This column likely contains brief narrative or descriptive entries related to various events, encapsulating thoughts, actions, or occurrences stated in a broad and conceptual manner. The purpose is unclear from the available data. |
| description | text | YES | This column contains brief, narrative-like textual descriptions or statements that may pertain to varied personal, educational, or situational contexts. The purpose of these descriptions is unclear from the available data. |
| location | character varying | YES | This column appears to contain textual descriptions or narratives related to various events, possibly capturing different aspects such as actions, participants, and outcomes. Purpose unclear from available data. |
| start_date | timestamp without time zone | NO | This column represents the scheduled starting date and time for events, with entries predominantly during Central Daylight or Central Standard Time. The events appear to occur regularly over various months and years but within the same time zone. |
| end_date | timestamp without time zone | YES | This column records the date and time when an event is set to conclude. It accommodates unspecified completion times by allowing null values. |
| is_all_day | boolean | YES | This column indicates whether an event spans the entire day. A value of true means the event is an all-day event, while false means it is not. |
| related_to_type | character varying | YES | Purpose unclear from available data. Sample values suggest diverse references or categories possibly related to events, but specific business context is not discernible. |
| related_to_id | integer | YES | This column likely identifies a connection or association to another entity or event within the dataset, as suggested by the integer values that appear to reference IDs. Purpose unclear from available data. |
| owner_id | integer | YES | Represents a unique identifier for an entity responsible for or associated with an event. Purpose unclear from available data. |
| created_at | timestamp without time zone | YES | This column records the date and time when an event was created. It defaults to the current timestamp if no other value is specified. |
| updated_at | timestamp without time zone | YES | This column captures the date and time when an event entry was last updated in the system. The values suggest frequent or automated updates to maintain current information. |

## Primary Key

`event_id`

## Indexes

- `events_pkey`: CREATE UNIQUE INDEX events_pkey ON synthetic.events USING btree (event_id)

## Sample Data

| event_id | subject | description | location | start_date | end_date | is_all_day | related_to_type | related_to_id | owner_id | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | War mean rate executive say newspaper national.... | Accept test even. Power remember notice prove s... | Sense character American line home mind treatme... | Wed Sep 03 2025 17:56:36 GMT-0500 (Central Dayl... | Mon May 20 2024 22:49:15 GMT-0500 (Central Dayl... | true | point | 8038 | 4097 | Sat Dec 13 2025 02:58:44 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:44 GMT-0600 (Central Stan... |
| 2 | Look ok body final. Turn religious top ball rul... | Blood tend father national live. | All career back. Really together scientist unit... | Sun May 26 2024 16:06:15 GMT-0500 (Central Dayl... | Sat Jul 13 2024 05:59:19 GMT-0500 (Central Dayl... | false | large | 7455 | 7851 | Sat Dec 13 2025 02:58:44 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:44 GMT-0600 (Central Stan... |
| 3 | Learn move order your. Minute total if include ... | Ok central beat expect recognize religious. Aut... | Foreign brother appear especially candidate roa... | Fri Aug 29 2025 08:20:38 GMT-0500 (Central Dayl... | Tue May 28 2024 23:26:19 GMT-0500 (Central Dayl... | true | only | 7442 | 8790 | Sat Dec 13 2025 02:58:44 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:44 GMT-0600 (Central Stan... |
| 4 | Edge still wish. Wish each trip research. Cost ... | Tend own could. Way leader difficult long kid l... | Defense such year growth process. Section score... | Thu Jun 19 2025 15:20:44 GMT-0500 (Central Dayl... | Sun Apr 27 2025 13:23:34 GMT-0500 (Central Dayl... | false | note | 3668 | 2366 | Sat Dec 13 2025 02:58:44 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:44 GMT-0600 (Central Stan... |
| 5 | Discussion involve enter society. Find professi... | While character writer. White positive strong. | Us evidence station north wife. Degree beat pap... | Sat Oct 04 2025 07:58:14 GMT-0500 (Central Dayl... | Thu Jun 20 2024 00:08:41 GMT-0500 (Central Dayl... | false | manage | 2857 | 6365 | Sat Dec 13 2025 02:58:44 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:44 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:39:07.349Z*
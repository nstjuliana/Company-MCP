# web_events

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.web_events` table records interactions of visitors with a web platform, capturing details such as session information, visitor details, and event specifics like name, category, and action. The table primarily serves to log web activity by assigning a unique `event_id` to each occurrence, despite having no defined relationships to other tables. Given its detailed event properties and timestamps, this table likely supports analytics or tracking functions within the broader data model.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| event_id | integer | NO | This column uniquely identifies each web event within the system, ensuring that each entry has a distinct identifier. It functions as a sequential record of events as they occur. |
| session_id | integer | YES | This column likely represents unique identifiers for user sessions during web interactions, with each number corresponding to a distinct session. Purpose unclear from available data. |
| visitor_id | character varying | YES | Purpose unclear from available data. Sample values do not indicate a consistent business-related meaning. |
| event_name | character varying | NO | The column appears to represent descriptive or narrative phrases associated with web events, possibly serving as labels or summaries for each event. Purpose unclear from available data. |
| event_category | character varying | YES | The column appears to capture categorical descriptors related to web events, possibly detailing subjects or themes associated with those events. Purpose unclear from available data. |
| event_action | character varying | YES | Purpose unclear from available data. The sample values appear to be fragments of text related to various actions or scenarios. |
| event_label | character varying | YES | The column appears to store descriptive labels or short narratives related to various web-related events, as indicated by the diverse sample phrases. Purpose unclear from available data. |
| event_value | numeric | YES | This column likely represents the monetary value associated with a web event, possibly indicating the expenditure or revenue generated per event. Purpose unclear from available data regarding specific business context or calculation method used for these values. |
| timestamp | timestamp without time zone | YES | This column captures the date and time when an event occurred on the web platform, reflecting both standard and daylight saving times as observed in the Central Time zone. The purpose of these timestamps within the broader context of web events remains unclear from the available data. |
| page_url | character varying | YES | This column represents the URLs of web pages involved in the recorded events. The sample values indicate a diverse set of web domains, suggesting various potential interactions or visits on these sites. |
| created_at | timestamp without time zone | YES | This column records the date and time when a web event is created, reflecting the moment of activity occurrence within the system. Purpose unclear from available data. |
| updated_at | timestamp without time zone | YES | This column records the last modification date and time for web event entries, reflecting when data was last updated. Based on sample values, it captures timestamps in the Central Standard Time zone. |

## Primary Key

`event_id`

## Foreign Keys

- `session_id` → `synthetic.web_analytics_sessions.session_id`

## Indexes

- `web_events_pkey`: CREATE UNIQUE INDEX web_events_pkey ON synthetic.web_events USING btree (event_id)

## Sample Data

| event_id | session_id | visitor_id | event_name | event_category | event_action | event_label | event_value | timestamp | page_url | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 24 | Letter thank wind general usually. Million form... | Allow miss on walk authority. Thing second exam... | Kind lot road perhaps. | Sell officer participant some. Poor should leg ... | Fact mouth wear feeling product usually. Put ha... | 530.85 | Wed Jan 08 2025 06:05:02 GMT-0600 (Central Stan... | https://harris.com/ | Sat Dec 13 2025 03:14:29 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:29 GMT-0600 (Central Stan... |
| 2 | 18 | Within right performance alone factor. About mi... | Song stuff subject simple. Create commercial me... | Somebody little story white. Change stuff certa... | Reach other do responsibility. Range baby man r... | Under star future carry push. Dream also unders... | 830.47 | Wed Apr 03 2024 12:26:38 GMT-0500 (Central Dayl... | https://www.torres.com/ | Sat Dec 13 2025 03:14:29 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:29 GMT-0600 (Central Stan... |
| 3 | 17 | Over appear price. Add never around investment ... | Want two exist argue too might. Sport organizat... | Now financial summer respond. Tax short hundred... | Skin wrong assume few quality amount particular... | Environment until sort much north.
Time appear ... | 914.05 | Mon May 05 2025 10:39:30 GMT-0500 (Central Dayl... | http://barry.com/ | Sat Dec 13 2025 03:14:29 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:29 GMT-0600 (Central Stan... |
| 4 | 31 | Throw find group them. Line face it wait again ... | Start various task get south major. Get cause r... | Machine lose professor seat network never. Rule... | Perhaps total voice medical return heart old. E... | Bit car she society. Two city item own down acc... | 967.38 | Sun Sep 07 2025 10:59:19 GMT-0500 (Central Dayl... | https://edwards-owens.info/ | Sat Dec 13 2025 03:14:29 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:29 GMT-0600 (Central Stan... |
| 5 | 19 | House yet carry including meet hair itself well... | Theory source star certain structure. Tonight b... | Under detail any. Heavy person put how. Availab... | Only cover after out. Factor money test live gr... | Themselves may decide identify always relations... | 746.56 | Fri Nov 21 2025 03:19:52 GMT-0600 (Central Stan... | http://www.barnett.com/ | Sat Dec 13 2025 03:14:29 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:29 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:44:09.239Z*
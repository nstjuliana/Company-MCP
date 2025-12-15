# event_attendees

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.event_attendees` table represents a record of individuals who are attending various events. Each entry includes details such as the attendee's ID, associated event ID, email, and participation status, along with timestamps for record creation and updates. This table primarily serves to track attendance information and is related to events and potentially contacts through the `event_id` and `contact_id`, although specific table relationships are not defined here.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| attendee_id | integer | NO | This column uniquely identifies each individual attending an event within the system, ensuring a distinct identity for every attendee. Each sequential integer value signifies a separate attendee entry in the database. |
| event_id | integer | NO | This column represents the unique identifiers for events that attendees are associated with in the system. Each value corresponds to a specific event attendees are assigned to attend. |
| contact_id | integer | YES | Purpose unclear from available data. |
| user_id | integer | YES | This column represents the identifiers assigned to individual users who are associated with event attendance. Each value indicates a unique user involved in the events tracked by the system. |
| email | character varying | YES | This column stores the email addresses of individuals attending an event, which can belong to various domains such as example.com, example.org, and example.net. The list includes both individual names and generic structures indicating contact information for event communication. |
| status | character varying | YES | This column represents the current state of an event attendee's participation, such as whether they have completed their involvement, have ongoing activities, or have canceled their attendance. It helps in tracking the participation status of each attendee in the event process. |
| created_at | timestamp without time zone | YES | This column records the date and time when an event attendee's record was created in the system. The exact purpose within the business process is unclear from the available data. |
| updated_at | timestamp without time zone | YES | This column captures the last modified date and time for each event attendee record, indicating when updates were made. Purpose unclear from available data. |

## Primary Key

`attendee_id`

## Foreign Keys

- `contact_id` → `synthetic.contacts.contact_id`
- `event_id` → `synthetic.events.event_id`

## Indexes

- `event_attendees_pkey`: CREATE UNIQUE INDEX event_attendees_pkey ON synthetic.event_attendees USING btree (attendee_id)

## Sample Data

| attendee_id | event_id | contact_id | user_id | email | status | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 37 | null | 2980 | zthompson@example.com | completed | Sat Dec 13 2025 02:58:48 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:48 GMT-0600 (Central Stan... |
| 2 | 2 | null | 8058 | hcaldwell@example.org | cancelled | Sat Dec 13 2025 02:58:48 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:48 GMT-0600 (Central Stan... |
| 3 | 23 | null | 5567 | christinereed@example.org | active | Sat Dec 13 2025 02:58:48 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:48 GMT-0600 (Central Stan... |
| 4 | 24 | null | 1129 | gpowell@example.com | inactive | Sat Dec 13 2025 02:58:48 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:48 GMT-0600 (Central Stan... |
| 5 | 9 | null | 4917 | olarson@example.org | completed | Sat Dec 13 2025 02:58:48 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:48 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:39:05.401Z*
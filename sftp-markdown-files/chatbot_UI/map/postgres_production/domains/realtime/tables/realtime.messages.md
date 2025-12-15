# messages

**Database:** postgres_production
**Schema:** realtime
**Description:** I cannot provide a meaningful semantic description for this table as the column information is missing or incomplete (showing only commas), no sample data is available, and there are no relationships to other tables. Without column names, data types, or sample values, it's impossible to determine what business entity this table represents or its role in the data model beyond the inference that it's likely related to real-time messaging functionality based on the schema and table name.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| topic | text | NO | Purpose unclear from available data. This appears to store textual identifiers or categories for real-time messaging, but without sample values the specific business meaning cannot be determined. |
| extension | text | NO | Purpose unclear from available data. This appears to be a required text field within the realtime messaging system, but without sample values or additional context, the specific business meaning cannot be determined. |
| payload | jsonb | YES | Purpose unclear from available data. Contains structured data associated with real-time messages, but specific content and business meaning cannot be determined without sample values. |
| event | text | YES | Purpose unclear from available data. Appears to store textual identifiers or descriptors related to real-time messaging activities. |
| private | boolean | YES | Indicates whether a message is intended for private communication rather than public or group visibility. Controls the access level and visibility scope of the message content. |
| updated_at | timestamp without time zone | NO | Records the moment when a real-time message record was last modified in the system. Automatically captures the current timestamp whenever any changes are made to the message data. |
| inserted_at | timestamp without time zone | NO | Records the exact moment when a real-time message was created and added to the system. Automatically captures the timestamp at insertion to track message chronology and enable time-based operations. |
| id | uuid | NO | A system-generated unique identifier that distinguishes each real-time message record from all others in the system. This serves as the primary reference key for tracking and retrieving individual message instances. |

## Primary Key

`id, inserted_at`

## Indexes

- `messages_inserted_at_topic_index`: CREATE INDEX messages_inserted_at_topic_index ON ONLY realtime.messages USING btree (inserted_at DESC, topic) WHERE ((extension = 'broadcast'::text) AND (private IS TRUE))
- `messages_pkey`: CREATE UNIQUE INDEX messages_pkey ON ONLY realtime.messages USING btree (id, inserted_at)

*Generated at: 2025-12-11T22:51:45.650Z*
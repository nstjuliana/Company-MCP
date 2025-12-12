# subscription

**Database:** postgres_production
**Schema:** realtime
**Description:** Based on the available information, this table appears to represent subscription entities within a realtime system, likely tracking active connections or subscriptions for real-time data streaming or notifications. The table has 7 columns with an 'id' primary key, suggesting it stores subscription records with associated metadata. However, without column details or sample data, the specific subscription attributes and business logic cannot be determined.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | bigint | NO | Purpose unclear from available data. Likely serves as a unique identifier for subscription records based on standard database conventions. |
| subscription_id | uuid | NO | A unique identifier that distinguishes each individual subscription record within the realtime subscription system. Purpose unclear from available data due to lack of sample values. |
| entity | regclass | NO | Purpose unclear from available data. The regclass data type suggests this stores references to database objects like tables or views, but without sample values or additional context, the specific business meaning cannot be determined. |
| filters | ARRAY | NO | Purpose unclear from available data. Contains an array of user-defined filter criteria with an empty array as the default value. |
| claims | jsonb | NO | Purpose unclear from available data. Stores structured authentication or authorization attributes in JSON format that cannot be null. |
| claims_role | regrole | NO | Purpose unclear from available data. The column appears to store database role information related to subscription claims, but without sample values or additional context, the specific business meaning cannot be determined. |
| created_at | timestamp without time zone | NO | Records the exact moment when a realtime subscription was established in the system. Automatically captures the current UTC timestamp upon creation and cannot be left empty. |

## Primary Key

`id`

## Indexes

- `ix_realtime_subscription_entity`: CREATE INDEX ix_realtime_subscription_entity ON realtime.subscription USING btree (entity)
- `pk_subscription`: CREATE UNIQUE INDEX pk_subscription ON realtime.subscription USING btree (id)
- `subscription_subscription_id_entity_filters_key`: CREATE UNIQUE INDEX subscription_subscription_id_entity_filters_key ON realtime.subscription USING btree (subscription_id, entity, filters)

*Generated at: 2025-12-11T22:51:45.725Z*
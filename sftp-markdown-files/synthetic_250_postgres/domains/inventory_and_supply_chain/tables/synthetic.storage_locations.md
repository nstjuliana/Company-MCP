# storage_locations

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The "synthetic.storage_locations" table appears to represent a business entity related to storage locations within a system, identified uniquely by the "location_id" primary key. Without access to column names or sample data, specific attributes and their functions remain undefined, and the table's connections to other database tables through foreign keys are not specified. As the table currently contains no rows and no references to other tables, its precise role in the broader data model is indeterminate beyond its potential to hold data about various storage locations.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| location_id | integer | NO | This column serves as a unique identifier for storage locations within the database. The purpose is unclear from available data beyond uniquely distinguishing each location entry. |
| zone_id | integer | NO | Purpose unclear from available data. |
| location_code | character varying | NO | Purpose unclear from available data. |
| aisle | character varying | YES | Purpose unclear from available data. |
| rack | character varying | YES | Purpose unclear from available data. |
| shelf | character varying | YES | Purpose unclear from available data. |
| bin | character varying | YES | Purpose unclear from available data. |
| max_weight_kg | numeric | YES | This column likely represents the maximum allowable weight, in kilograms, for items stored at a specific location. Purpose unclear from available data. |
| max_volume_cbm | numeric | YES | This column likely represents the maximum storage capacity of a location in cubic meters for managing inventory or goods. Purpose unclear from available data. |
| is_available | boolean | YES | Indicates whether a storage location is currently available for use. The default status assumes availability unless specified otherwise. |
| created_at | timestamp without time zone | YES | This column records the date and time when a storage location record is initially created, capturing the system-generated timestamp of the event. Purpose unclear from available data. |
| updated_at | timestamp without time zone | YES | This column indicates the date and time when a storage location record was last modified. Its default value suggests it records the current timestamp upon any change if no other value is provided. |

## Primary Key

`location_id`

## Foreign Keys

- `zone_id` → `synthetic.warehouse_zones.zone_id`

## Indexes

- `storage_locations_pkey`: CREATE UNIQUE INDEX storage_locations_pkey ON synthetic.storage_locations USING btree (location_id)

*Generated at: 2025-12-14T23:42:47.750Z*
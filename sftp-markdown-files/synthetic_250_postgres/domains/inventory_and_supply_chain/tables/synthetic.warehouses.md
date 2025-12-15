# warehouses

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The "synthetic.warehouses" table represents a collection of warehouse entities within the database "synthetic_250_postgres," uniquely identified by the primary key "warehouse_id." As the table contains no rows or column information and has no foreign key relationships, it serves as a standalone entity, possibly intended to house data about warehouses in the context of synthetic data modeling. Without any connections to other tables, the role of this table in the data model is isolated and indeterminate based on the available metadata.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| warehouse_id | integer | NO | Unique identifier assigned to each warehouse, ensuring every entry in the table can be distinctly recognized. Purpose unclear from available data. |
| warehouse_code | character varying | NO | Purpose unclear from available data. |
| warehouse_name | character varying | NO | The column represents the name assigned to each warehouse, serving as a unique identifier within the warehouse database. Purpose unclear from available data. |
| address_line1 | character varying | YES | This column likely represents a part of the physical location or address associated with a warehouse, capturing the primary line of address information. Purpose unclear from available data. |
| city | character varying | YES | This field represents the city location for the various warehouses in the system. Purpose unclear from available data. |
| state | character varying | YES | This column represents the location state associated with the warehouses, which helps identify their geographical regions. Purpose unclear from available data. |
| country | character varying | YES | This column identifies the country associated with each warehouse. Purpose unclear from available data. |
| postal_code | character varying | YES | This column likely represents the postal identification number associated with each warehouse location, useful for addressing and geographical categorization. Purpose unclear from available data due to absence of sample values. |
| capacity_sqft | integer | YES | Specifies the storage capacity of a warehouse measured in square feet, which can be undefined for some entries. |
| is_active | boolean | YES | Indicates whether a warehouse is currently operational or not, with a default assumption as operational unless specified otherwise. |
| manager_id | integer | YES | The column likely designates the identification number of the individual responsible for managing warehouse operations. Purpose unclear from available data due to the absence of sample values. |
| created_at | timestamp without time zone | YES | This column records the date and time when a warehouse record is initially created, aiding in tracking the establishment history of entries. It may enhance reporting and auditing processes by supplying temporal context. |
| updated_at | timestamp without time zone | YES | Records the date and time when each warehouse entry was last updated. This timestamp facilitates tracking changes to warehouse information over time. |

## Primary Key

`warehouse_id`

## Indexes

- `warehouses_pkey`: CREATE UNIQUE INDEX warehouses_pkey ON synthetic.warehouses USING btree (warehouse_id)
- `warehouses_warehouse_code_key`: CREATE UNIQUE INDEX warehouses_warehouse_code_key ON synthetic.warehouses USING btree (warehouse_code)

*Generated at: 2025-12-14T23:42:48.958Z*
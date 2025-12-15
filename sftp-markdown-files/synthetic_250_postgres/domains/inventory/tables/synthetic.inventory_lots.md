# inventory_lots

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.inventory_lots` table in the `synthetic_250_postgres` database represents inventory lot details, uniquely identified by the primary key `lot_id`. Despite lacking explicit column names or sample data, it is designed to store aggregated details about inventory lots, likely contributing to the inventory management domain. An undefined foreign key hints at a potential linkage to another table, which may represent broader inventory or warehouse information, although this relationship remains unspecified.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| lot_id | integer | NO | This unique numeric identifier is assigned to each inventory batch or lot to track and manage stock within the inventory system. |
| inventory_id | integer | NO | Purpose unclear from available data. |
| lot_number | character varying | NO | Purpose unclear from available data. |
| quantity | integer | NO | Represents the number of units available for a specific inventory lot in the system. Purpose unclear from available data. |
| manufacture_date | date | YES | This column indicates the calendar date on which a specific inventory item was produced. The purpose of this information is unclear from the available data. |
| expiry_date | date | YES | Represents the date when the inventory item is no longer considered usable or effective. Purpose unclear from available data. |
| received_date | date | YES | This column likely records the date when inventory lots are received, contributing to tracking inventory movement and stock management. Purpose unclear from available data. |
| cost_per_unit | numeric | YES | This column likely represents the monetary expense associated with each individual unit of inventory. Purpose unclear from available data due to lack of sample values. |
| created_at | timestamp without time zone | YES | This column records the date and time when each inventory lot entry was created. It captures the initial creation timestamp, likely serving as a record for tracking inventory lot additions over time. |
| updated_at | timestamp without time zone | YES | Records the date and time when an inventory lot's information was last updated. |

## Primary Key

`lot_id`

## Foreign Keys

- `inventory_id` → `synthetic.inventory_items.inventory_id`

## Indexes

- `inventory_lots_pkey`: CREATE UNIQUE INDEX inventory_lots_pkey ON synthetic.inventory_lots USING btree (lot_id)

*Generated at: 2025-12-14T23:42:23.736Z*
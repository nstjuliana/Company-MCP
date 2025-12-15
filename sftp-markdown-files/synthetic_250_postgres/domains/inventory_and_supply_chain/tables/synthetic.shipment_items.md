# shipment_items

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The "synthetic.shipment_items" table is intended to represent individual items within a shipment, uniquely identified by the primary key "shipment_item_id". Although no column names or sample data are available, the table is designed to reference other entities, suggesting relationships with at least two undefined external tables. Despite having no rows or specific data, the table likely plays a crucial role in tracking and managing shipment components within the database.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| shipment_item_id | integer | NO | A unique identifier assigned to each item in a shipment. It ensures that each item can be individually referenced and tracked within the shipment records. |
| shipment_id | integer | NO | This column represents a unique identifier that links individual shipment items to their respective shipments, ensuring items are correctly associated with specific shipment records. |
| order_item_id | integer | NO | Purpose unclear from available data. |
| quantity_shipped | integer | NO | This column indicates the number of units for each specific item included in a shipment, representing how many of these items were dispatched to their destination. |
| created_at | timestamp without time zone | YES | This column captures the date and time when a shipment item record was initially created, aligning with when the data entry occurs. If not explicitly provided, it defaults to the current timestamp at the point of entry. |
| updated_at | timestamp without time zone | YES | This column likely records the last date and time when a shipment item entry was modified. It helps track changes and updates to shipment items over time. |

## Primary Key

`shipment_item_id`

## Foreign Keys

- `order_item_id` → `synthetic.order_items.order_item_id`
- `shipment_id` → `synthetic.shipments.shipment_id`

## Indexes

- `shipment_items_pkey`: CREATE UNIQUE INDEX shipment_items_pkey ON synthetic.shipment_items USING btree (shipment_item_id)

*Generated at: 2025-12-14T23:42:46.342Z*
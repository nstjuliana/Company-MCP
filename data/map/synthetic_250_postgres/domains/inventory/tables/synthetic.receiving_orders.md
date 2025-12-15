# receiving_orders

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The "synthetic.receiving_orders" table is intended to represent business transactions where products or goods are received, likely within a larger supply chain or inventory management system, although it currently contains no data. The primary key, "receiving_id," ensures unique identification for each receiving order. The table is linked to at least two other entities through unspecified foreign keys, signifying its role in associating receiving operations with details or events in other areas of the business process.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| receiving_id | integer | NO | This column serves as a unique identifier for each order recorded in the receiving orders table. It is automatically generated and incremented for new entries. |
| receiving_number | character varying | YES | Purpose unclear from available data. |
| po_id | integer | YES | Purpose unclear from available data. |
| warehouse_id | integer | NO | This column likely identifies the specific warehouse associated with each receiving order. Each entry in the column corresponds to a unique warehouse location necessary for the logistical processing of orders. |
| received_date | timestamp without time zone | NO | This column indicates the specific date and time when an order was successfully received. It is instrumental in tracking the completion of order deliveries. |
| status | character varying | YES | This column likely indicates the current progress or state of receiving orders within a business's workflow. The default value suggests new records start as pending until further updates. |
| received_by | integer | YES | This column likely identifies the employee or individual responsible for receiving the order. Purpose unclear from available data. |
| notes | text | YES | Purpose unclear from available data. |
| created_at | timestamp without time zone | YES | This column records the date and time when an entry is initially created in the context of receiving orders. The exact purpose of tracking this timestamp is unclear from the available data. |
| updated_at | timestamp without time zone | YES | This column indicates the latest time when a record in the receiving orders table was modified. It helps in tracking the most recent updates to the order information. |

## Primary Key

`receiving_id`

## Foreign Keys

- `po_id` → `synthetic.purchase_orders.po_id`
- `warehouse_id` → `synthetic.warehouses.warehouse_id`

## Indexes

- `receiving_orders_pkey`: CREATE UNIQUE INDEX receiving_orders_pkey ON synthetic.receiving_orders USING btree (receiving_id)
- `receiving_orders_receiving_number_key`: CREATE UNIQUE INDEX receiving_orders_receiving_number_key ON synthetic.receiving_orders USING btree (receiving_number)

*Generated at: 2025-12-14T23:42:23.170Z*
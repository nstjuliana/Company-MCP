# receiving_lines

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The "synthetic.receiving_lines" table appears to represent individual line items involved in a receiving process within a broader business operation, as indicated by the primary key "receiving_line_id." Although specific column details and sample data are unavailable, the table likely captures distinct aspects of received goods or transactions. It has foreign key relationships to unspecified entities, suggesting integration with other parts of the database model, though it currently holds no data or documented interactions with other tables.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| receiving_line_id | integer | NO | Unique identifier for each entry within the receiving lines records, ensuring each record is distinct. |
| receiving_id | integer | NO | Purpose unclear from available data. |
| po_line_id | integer | YES | Purpose unclear from available data. |
| product_id | integer | NO | Identifies the specific product associated with each receiving transaction line, playing a key role in inventory management by tracking incoming goods. |
| quantity_received | integer | NO | This column captures the count of items successfully received in a shipment or delivery. It reflects the actual number of goods received as part of inventory management processes. |
| quantity_accepted | integer | YES | The column likely indicates the number of items successfully accepted during a receiving transaction. These may come in various contexts such as inventory management or supply chain operations, but the specific purpose is unclear from the available data. |
| quantity_rejected | integer | YES | This column indicates the count of items that did not meet quality standards or specifications in a particular receiving transaction. It reflects rejected items during inventory or logistics processes. |
| location_id | integer | YES | Purpose unclear from available data. |
| lot_number | character varying | YES | Purpose unclear from available data. |
| created_at | timestamp without time zone | YES | This column indicates the date and time when a record within the receiving lines table was created, with a default setting to capture the present timestamp upon entry. It allows for records to exist without this information being populated initially. |
| updated_at | timestamp without time zone | YES | This column likely indicates the date and time when each entry in the receiving lines table was last modified. It helps track changes to records for auditing or synchronization purposes. |

## Primary Key

`receiving_line_id`

## Foreign Keys

- `location_id` → `synthetic.storage_locations.location_id`
- `po_line_id` → `synthetic.purchase_order_lines.po_line_id`
- `receiving_id` → `synthetic.receiving_orders.receiving_id`

## Indexes

- `receiving_lines_pkey`: CREATE UNIQUE INDEX receiving_lines_pkey ON synthetic.receiving_lines USING btree (receiving_line_id)

*Generated at: 2025-12-14T23:42:25.179Z*
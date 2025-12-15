# purchase_order_lines

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.purchase_order_lines` table is designed to hold individual line items of a purchase order, each identified by a unique `po_line_id`. It possesses a foreign key relationship that is undefined, suggesting it might link to another table, potentially to reference broader order or item details. The absence of rows and columns limits detailed analysis, but the table likely plays a role in itemizing components of purchase orders within the broader database schema.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| po_line_id | integer | NO | This column uniquely identifies each line item within a purchase order, ensuring each entry is distinguishable within the context of order processing. |
| po_id | integer | NO | This column likely serves as a unique identifier for each purchase order line entry. Purpose unclear from available data. |
| product_id | integer | NO | This column represents the unique identifier assigned to each product associated with purchase order lines in the system. Purpose unclear from available data. |
| quantity_ordered | integer | NO | This column represents the total number of each item requested in individual purchase order line entries. Each entry is mandatory and must specify a whole number indicating the amount ordered. |
| quantity_received | integer | YES | This column indicates the number of items that have been received against a specific purchase order line. The default value suggests that no items are initially recorded as received until updated. |
| unit_cost | numeric | NO | Purpose unclear from available data. |
| line_total | numeric | YES | The column likely represents the total amount for a line item within a purchase order, which may be used to calculate the overall order cost. |
| created_at | timestamp without time zone | YES | This column records the date and time when a purchase order line was initially created. The inclusion of a default timestamp suggests it captures the moment of entry into the system. |
| updated_at | timestamp without time zone | YES | This column likely records the date and time when a change or update was made to the purchase order line entry. It captures the most recent modification timestamp, assuming no explicit overrides were applied. |

## Primary Key

`po_line_id`

## Foreign Keys

- `po_id` → `synthetic.purchase_orders.po_id`

## Indexes

- `purchase_order_lines_pkey`: CREATE UNIQUE INDEX purchase_order_lines_pkey ON synthetic.purchase_order_lines USING btree (po_line_id)

*Generated at: 2025-12-14T23:41:19.962Z*
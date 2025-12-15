# stock_transfer_lines

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.stock_transfer_lines` table appears to represent the details of individual line items involved in stock transfer transactions, identified uniquely by `transfer_line_id`. The table does not currently hold data and lacks defined column names or relationships, limiting detailed insight into its specific role or connections within the database. Nevertheless, it potentially functions as a component in a broader inventory management or logistics system, documenting each item in a stock transfer operation.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| transfer_line_id | integer | NO | This column uniquely identifies each line item or entry within the context of stock transfers, ensuring that each transfer line can be distinctly referenced and tracked in the system. |
| transfer_id | integer | NO | Purpose unclear from available data. |
| product_id | integer | NO | This column uniquely identifies each product involved in stock transfers. Purpose unclear from available data. |
| quantity | integer | NO | This column represents the number of items being moved or transferred in a specific transaction. It is a required field for tracking item quantities in stock transfer operations. |
| from_location_id | integer | YES | Purpose unclear from available data. |
| to_location_id | integer | YES | Destination identifier for a stock transfer, indicating where the stock is being moved to. Purpose unclear from available data. |
| created_at | timestamp without time zone | YES | This column indicates the date and time when a stock transfer line was created, capturing the moment of entry into the system. Purpose unclear from available data. |
| updated_at | timestamp without time zone | YES | Indicates the most recent date and time when a stock transfer record was updated, reflecting the currency of information within the system. |

## Primary Key

`transfer_line_id`

## Foreign Keys

- `from_location_id` → `synthetic.storage_locations.location_id`
- `to_location_id` → `synthetic.storage_locations.location_id`
- `transfer_id` → `synthetic.stock_transfers.transfer_id`

## Indexes

- `stock_transfer_lines_pkey`: CREATE UNIQUE INDEX stock_transfer_lines_pkey ON synthetic.stock_transfer_lines USING btree (transfer_line_id)

*Generated at: 2025-12-14T23:42:47.750Z*
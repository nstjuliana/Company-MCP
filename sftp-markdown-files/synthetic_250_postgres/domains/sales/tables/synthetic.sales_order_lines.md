# sales_order_lines

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.sales_order_lines` table represents individual line items within sales orders, capturing each item’s specifics such as product, quantity, unit price, and discounts applied, as indicated by columns like `product_id`, `quantity`, and `unit_price`. It references another table for sales order details through the `sales_order_id` column, indicating its role in detailing each component of a multi-item sales transaction. The table is designed to enable tracking of the specifics of each sale line, as seen in the sample values like product names and the financial calculations involved in discounts and totals.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| so_line_id | integer | NO | This column uniquely identifies each line item within a sales order. Each value is a sequential identifier starting from one. |
| sales_order_id | integer | NO | This column represents a unique identifier assigned to each sales order line to track individual transactions within the synthetic sales order system. The purpose is to ensure each sales order line can be distinctly recognized and referenced. |
| product_id | integer | YES | This column likely represents identifiers for different products associated with sales order lines. Purpose unclear from available data. |
| product_name | character varying | YES | This column likely represents descriptions or notes related to various products in sales order lines, capturing contextual or promotional information about each item. The specific purpose of these entries is unclear from the available data. |
| quantity | numeric | NO | This column represents the quantity of items associated with each line in a sales order, expressed in numerical values. The specific unit of measurement for these quantities is not specified within the available data. |
| unit_price | numeric | NO | This column represents the price charged per individual unit of a product or service associated with a sales order line item. The sample values suggest relatively high-priced items, possibly indicating a business dealing in luxury or high-value products. |
| discount | numeric | YES | This column represents the monetary value deducted from the total sales order amount as a discount for each order line. It accounts for the reduction in price granted to enhance sales or accommodate customer agreements. |
| line_total | numeric | YES | This column represents the monetary total amount of an individual sales order line, reflecting the total cost associated with a particular order item. The values denote the accumulated cost in a currency format within a sales transaction, contributing to the overall order value. |
| created_at | timestamp without time zone | YES | This column records the date and time when each sales order line was created. Purpose unclear from available data. |
| updated_at | timestamp without time zone | YES | This column records the date and time when a sales order line was last updated. The consistent sample values suggest it may be used to track changes or modifications to the order details. |

## Primary Key

`so_line_id`

## Foreign Keys

- `sales_order_id` → `synthetic.sales_orders.sales_order_id`

## Indexes

- `sales_order_lines_pkey`: CREATE UNIQUE INDEX sales_order_lines_pkey ON synthetic.sales_order_lines USING btree (so_line_id)

## Sample Data

| so_line_id | sales_order_id | product_id | product_name | quantity | unit_price | discount | line_total | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 44 | 32 | Evidence new line could. Board movie sister boo... | 241.94 | 4892.98 | 446.10 | 960.52 | Sat Dec 13 2025 03:18:34 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:18:34 GMT-0600 (Central Stan... |
| 2 | 31 | 601 | Upon ask environment. Financial sense section. ... | 551.33 | 3449.05 | 837.65 | 258.66 | Sat Dec 13 2025 03:18:34 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:18:34 GMT-0600 (Central Stan... |
| 3 | 45 | 93 | Market career simple score. | 285.07 | 3871.79 | 162.91 | 572.26 | Sat Dec 13 2025 03:18:34 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:18:34 GMT-0600 (Central Stan... |
| 4 | 14 | 878 | Garden according agent partner show pay ball. | 221.35 | 2258.87 | 206.73 | 651.59 | Sat Dec 13 2025 03:18:34 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:18:34 GMT-0600 (Central Stan... |
| 5 | 33 | 21 | Actually issue stage in. Practice as cell surfa... | 864.63 | 9671.71 | 682.20 | 474.10 | Sat Dec 13 2025 03:18:34 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:18:34 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:42:01.206Z*
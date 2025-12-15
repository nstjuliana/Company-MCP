# reorder_rules

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.reorder_rules` table defines parameters for restocking products, with each rule associated with a specific `product_id`, indicating when and how much to reorder based on `reorder_point`, `reorder_quantity`, `safety_stock`, and `max_stock` levels. The table captures the operational aspect of inventory management, although the relationship columns suggest it references another table which is not defined. The presence of columns like `lead_time_days`, `is_active`, and timestamps (`created_at`, `updated_at`) further detail the mechanism and status of each reorder rule.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| rule_id | integer | NO | This column represents a unique identifier for each reorder rule in the system, ensuring that each rule can be distinctly referenced. It increments sequentially with each new rule entry. |
| product_id | integer | NO | This column uniquely identifies products for which reorder rules are applied. Each integer corresponds to a specific product. |
| warehouse_id | integer | YES | Purpose unclear from available data. |
| reorder_point | integer | NO | This column represents the inventory threshold at which a reorder is triggered, indicating the minimum quantity level of a product before replenishment is necessary. The sample values suggest varying reorder points, which may correspond to different demand rates or stock levels for each product. |
| reorder_quantity | integer | NO | The column represents the quantity of items to be reordered when inventory levels reach a specified trigger point. It ensures that a predefined stock level is maintained by replenishing items using the listed quantities. |
| safety_stock | integer | YES | Represents the buffer inventory level maintained to prevent stockouts, expressed in units. This value can be adjusted according to demand fluctuations to optimize inventory management. |
| max_stock | integer | YES | This column likely represents the maximum allowable stock quantity for a particular item before a reorder is considered necessary. The purpose of this column is to help manage inventory levels and avoid overstocking. |
| lead_time_days | integer | YES | This column represents the number of days required to replenish inventory after an order is placed. The purpose of this timing information within reorder operations is unclear from the available data. |
| is_active | boolean | YES | Indicates whether a reorder rule is currently active or not. This status is optional and defaults to being active. |
| created_at | timestamp without time zone | YES | This column indicates the date and time when a record was created in the reorder rules table. The values suggest that the initial timestamp is automatically set to the current date and time when a record is inserted. |
| updated_at | timestamp without time zone | YES | This column records the most recent date and time a reorder rule was modified or confirmed. Purpose unclear from available data. |

## Primary Key

`rule_id`

## Foreign Keys

- `warehouse_id` → `synthetic.warehouses.warehouse_id`

## Indexes

- `reorder_rules_pkey`: CREATE UNIQUE INDEX reorder_rules_pkey ON synthetic.reorder_rules USING btree (rule_id)

## Sample Data

| rule_id | product_id | warehouse_id | reorder_point | reorder_quantity | safety_stock | max_stock | lead_time_days | is_active | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 4190 | null | 6602 | 33 | 9361 | 1288 | 21 | false | Sat Dec 13 2025 02:58:22 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:22 GMT-0600 (Central Stan... |
| 2 | 9197 | null | 5658 | 85 | 3401 | 8677 | 12 | false | Sat Dec 13 2025 02:58:22 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:22 GMT-0600 (Central Stan... |
| 3 | 4782 | null | 5167 | 462 | 7658 | 485 | 5 | true | Sat Dec 13 2025 02:58:22 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:22 GMT-0600 (Central Stan... |
| 4 | 5762 | null | 9256 | 441 | 6806 | 384 | 25 | false | Sat Dec 13 2025 02:58:22 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:22 GMT-0600 (Central Stan... |
| 5 | 9117 | null | 8041 | 240 | 6149 | 8808 | 5 | false | Sat Dec 13 2025 02:58:22 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:22 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:42:29.647Z*
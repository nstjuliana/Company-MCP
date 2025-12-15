# pack_orders

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.pack_orders` table represents the packing operations associated with orders in a logistics or warehouse management system. Each row corresponds to a unique packing instance identified by `pack_id`, capturing details such as the `pack_number`, `order_id`, `status`, `packed_by`, and timestamps like `packed_at`, `created_at`, and `updated_at`. While the table references the `order_id` suggesting a link to an orders table, it serves as a detailed log for tracking the packing progress and related attributes like `total_weight_kg` and `num_packages`.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| pack_id | integer | NO | This column uniquely identifies each order in the packaging process. Each value is a sequential identifier, ensuring that every order is distinct within the system. |
| pack_number | character varying | YES | This column likely represents unique identifiers assigned to individual orders in a packaging process. Each value serves as a distinct reference number for tracking or managing packaged orders. |
| pick_id | integer | YES | Purpose unclear from available data. |
| order_id | integer | YES | This column represents a unique identifier assigned to each order within the packaging department, allowing for tracking and management of orders. Purpose unclear from available data. |
| status | character varying | YES | This column indicates the current state of an order within the packing process, with possible states including pending, completed, inactive, and cancelled. These states likely reflect the progress or outcome of order handling. |
| packed_by | integer | YES | This column likely identifies employees or agents responsible for packing orders using unique numeric identifiers. Purpose unclear from available data. |
| packed_at | timestamp without time zone | YES | This column records the date and time when an order was packed, reflecting various instances of order processing throughout different times of the year. The exact time zone context may vary as it is not stored with the data itself. |
| total_weight_kg | numeric | YES | This column represents the aggregate weight of items within a package order expressed in kilograms. Purpose unclear from available data. |
| num_packages | integer | YES | This column likely represents the quantity of packages involved in individual orders within a packaging process. The values indicate large numbers typically ranging from a few thousand to several thousand, suggesting substantial orders. |
| created_at | timestamp without time zone | YES | This column indicates the date and time when a pack order was created. Purpose unclear from available data. |
| updated_at | timestamp without time zone | YES | This column records the date and time when a pack order in the synthetic.pack_orders table was last updated. The information indicates all recorded values fall on the same specific date and time, December 13, 2025, suggesting this may reflect either a test dataset or batch update scenario. |

## Primary Key

`pack_id`

## Foreign Keys

- `pick_id` → `synthetic.pick_orders.pick_id`

## Indexes

- `pack_orders_pack_number_key`: CREATE UNIQUE INDEX pack_orders_pack_number_key ON synthetic.pack_orders USING btree (pack_number)
- `pack_orders_pkey`: CREATE UNIQUE INDEX pack_orders_pkey ON synthetic.pack_orders USING btree (pack_id)

## Sample Data

| pack_id | pack_number | pick_id | order_id | status | packed_by | packed_at | total_weight_kg | num_packages | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 87686242641094578917 | null | 8811 | completed | 5424 | Mon Jan 13 2025 11:07:01 GMT-0600 (Central Stan... | 9.562 | 7680 | Sat Dec 13 2025 02:58:15 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:15 GMT-0600 (Central Stan... |
| 2 | 34671690986345536448 | null | 9740 | inactive | 1094 | Fri Jul 11 2025 09:01:08 GMT-0500 (Central Dayl... | 35.110 | 9162 | Sat Dec 13 2025 02:58:15 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:15 GMT-0600 (Central Stan... |
| 3 | 03010047188754967430 | null | 3704 | pending | 232 | Fri May 31 2024 07:26:44 GMT-0500 (Central Dayl... | 92.795 | 4499 | Sat Dec 13 2025 02:58:15 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:15 GMT-0600 (Central Stan... |
| 4 | 88982050858785263355 | null | 4657 | completed | 9576 | Fri Oct 03 2025 21:59:12 GMT-0500 (Central Dayl... | 72.959 | 6018 | Sat Dec 13 2025 02:58:15 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:15 GMT-0600 (Central Stan... |
| 5 | 07327502551807377954 | null | 6608 | pending | 9194 | Sun May 05 2024 17:32:05 GMT-0500 (Central Dayl... | 54.148 | 3320 | Sat Dec 13 2025 02:58:15 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:15 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:39:22.529Z*
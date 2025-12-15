# abc_analysis

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.abc_analysis` table represents an ABC analysis of inventory in a business context, categorizing products based on their annual usage value and cumulative percentage. Each entry in the table is uniquely identified by `analysis_id` and includes attributes such as `product_id`, `warehouse_id`, and `classification` among others, highlighting the operational aspects of inventory classification. While it contains a foreign key relating to an undefined table, the absence of defined relationships or references suggests its use as a standalone analytical tool for assessing inventory value and performance.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| analysis_id | integer | NO | This column designates a unique identifier for each entry within the table, ensuring each analysis instance is distinctly recognized. The purpose is to sequentially number entries for tracking and reference. |
| product_id | integer | NO | This column represents a unique identifier for products involved in an ABC analysis. Each integer corresponds to a specific product being evaluated. |
| warehouse_id | integer | YES | This column likely represents a unique identifier for different warehouse locations associated with ABC analysis. Purpose unclear from available data. |
| analysis_date | date | NO | This column captures the specific date on which an ABC analysis was conducted, providing a chronological reference for analysis activities within the synthetic dataset. The dates reflect various times throughout different years, suggesting that analyses occur on multiple occasions annually. |
| classification | character varying | YES | This column appears to categorize or classify records using single-character codes, suggesting a system of grouping or identifying certain aspects of the data. Purpose unclear from available data. |
| annual_usage_value | numeric | YES | This column represents the total annual financial consumption or expenditure attributed to an entity within an ABC analysis framework, typically measured in a monetary unit, such as dollars. Purpose unclear from available data. |
| cumulative_percentage | numeric | YES | This column represents the cumulative percentage of a certain measurable attribute, likely summing up incremental contributions or values, possibly in the context of an analysis such as inventory, sales, or performance tracking. The exact purpose or the context of the cumulative data is unclear from the available information. |
| created_at | timestamp without time zone | YES | This column records the date and time when a record was created in the abc_analysis table, defaulting to the current timestamp at the time of record insertion. Purpose unclear from available data. |
| updated_at | timestamp without time zone | YES | This column records the date and time when a record in the abc_analysis table was last updated. It reflects changes made to a record, with the default time being the current time at the moment of the update. |

## Primary Key

`analysis_id`

## Foreign Keys

- `warehouse_id` → `synthetic.warehouses.warehouse_id`

## Indexes

- `abc_analysis_pkey`: CREATE UNIQUE INDEX abc_analysis_pkey ON synthetic.abc_analysis USING btree (analysis_id)

## Sample Data

| analysis_id | product_id | warehouse_id | analysis_date | classification | annual_usage_value | cumulative_percentage | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 130 | null | Wed Aug 13 2025 00:00:00 GMT-0500 (Central Dayl... | N | 637.87 | 752.790 | Sat Dec 13 2025 03:10:16 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:10:16 GMT-0600 (Central Stan... |
| 2 | 106 | null | Wed Aug 28 2024 00:00:00 GMT-0500 (Central Dayl... | X | 872.72 | 574.060 | Sat Dec 13 2025 03:10:16 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:10:16 GMT-0600 (Central Stan... |
| 3 | 481 | null | Tue Feb 27 2024 00:00:00 GMT-0600 (Central Stan... | f | 478.71 | 340.710 | Sat Dec 13 2025 03:10:16 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:10:16 GMT-0600 (Central Stan... |
| 4 | 989 | null | Sat Apr 19 2025 00:00:00 GMT-0500 (Central Dayl... | Q | 51.38 | 941.060 | Sat Dec 13 2025 03:10:16 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:10:16 GMT-0600 (Central Stan... |
| 5 | 490 | null | Fri Dec 06 2024 00:00:00 GMT-0600 (Central Stan... | a | 114.09 | 65.340 | Sat Dec 13 2025 03:10:16 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:10:16 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:39:05.095Z*
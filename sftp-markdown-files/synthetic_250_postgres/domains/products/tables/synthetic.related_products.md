# related_products

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.related_products` table represents relationships between products, identifying how different products are related, such as through ownership indicated by the `relation_type` column. It uses `product_id` and `related_product_id` to establish these connections, with `relation_id` serving as the primary key. Despite the lack of explicitly defined foreign keys, this table likely plays a crucial role in organizing product associations within the data model, accommodating functions like product recommendations or bundling.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| relation_id | integer | NO | This column serves as a unique identifier for each relationship within the related products dataset, ensuring that each relationship is distinctly tracked. Each integer represents a specific relationship entry, crucial for managing product associations. |
| product_id | integer | NO | This column represents unique identifiers for products associated with each entry in the related_products table. It ensures the correct linking of related products within the dataset. |
| related_product_id | integer | NO | Each value denotes an identifier for a product that is associated with another product in some manner, such as being a complementary or alternative option. Purpose unclear from available data. |
| relation_type | character varying | YES | Purpose unclear from available data. |
| sort_order | integer | YES | This column likely represents the order or priority in which related products are displayed or processed, with lower numbers indicating higher precedence. Purpose unclear from available data. |
| created_at | timestamp without time zone | YES | This column indicates the date and time when a record related to product associations was first added to the system. The timestamp defaults to the current time, suggesting its use for tracking when entries are created. |
| updated_at | timestamp without time zone | YES | This column records the date and time when a record in the "related_products" table was last updated, typically denoting the latest modification or system update. The presence of a default timestamp suggests it automatically logs the current date and time upon record creation or update. |

## Primary Key

`relation_id`

## Foreign Keys

- `product_id` → `synthetic.products.product_id`
- `related_product_id` → `synthetic.products.product_id`

## Indexes

- `related_products_pkey`: CREATE UNIQUE INDEX related_products_pkey ON synthetic.related_products USING btree (relation_id)

## Sample Data

| relation_id | product_id | related_product_id | relation_type | sort_order | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 40 | 14 | owner | 3917 | Sat Dec 13 2025 02:56:56 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:56 GMT-0600 (Central Stan... |
| 2 | 31 | 48 | hear | 5432 | Sat Dec 13 2025 02:56:56 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:56 GMT-0600 (Central Stan... |
| 3 | 48 | 25 | plant | 3364 | Sat Dec 13 2025 02:56:56 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:56 GMT-0600 (Central Stan... |
| 4 | 26 | 12 | since | 111 | Sat Dec 13 2025 02:56:56 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:56 GMT-0600 (Central Stan... |
| 5 | 24 | 1 | so | 1209 | Sat Dec 13 2025 02:56:56 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:56 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:38:57.197Z*
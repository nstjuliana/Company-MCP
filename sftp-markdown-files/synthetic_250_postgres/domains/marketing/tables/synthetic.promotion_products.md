# promotion_products

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.promotion_products` table captures the relationship between promotions and products, indicating which products are part of specific promotions. Each record is identified by a primary key, `promo_product_id`, and includes references to `promotion_id`, `product_id`, and `category_id`, alongside timestamps of creation and updates. While the table includes foreign keys, their specific relationships aren't defined, implying this table primarily facilitates the association between promotions and products without explicit linkage to other entities.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| promo_product_id | integer | NO | This column uniquely identifies each promotion product in a sequential manner, serving as a primary reference within the promotion products table. |
| promotion_id | integer | NO | Represents unique identifiers for promotions associated with products, used to link products to specific promotional campaigns. Purpose unclear from available data. |
| product_id | integer | YES | This field likely identifies individual products promoted within a business context, represented by unique numerical identifiers. Purpose unclear from available data. |
| category_id | integer | YES | This column represents an identifier for different product categories associated with various promotions. Each integer corresponds to a specific category within the promotional context, though the exact meanings of the categories are unclear from the available data. |
| created_at | timestamp without time zone | YES | This column records the date and time when a product associated with a promotion was initially created or added to the system. The default setting suggests it automatically logs the current date and time upon entry creation. |
| updated_at | timestamp without time zone | YES | This column records the date and time when an entry in the promotion_products table was last updated. Purpose unclear from available data. |

## Primary Key

`promo_product_id`

## Foreign Keys

- `category_id` → `synthetic.product_categories.category_id`
- `product_id` → `synthetic.products.product_id`
- `promotion_id` → `synthetic.promotions.promotion_id`

## Indexes

- `promotion_products_pkey`: CREATE UNIQUE INDEX promotion_products_pkey ON synthetic.promotion_products USING btree (promo_product_id)

## Sample Data

| promo_product_id | promotion_id | product_id | category_id | created_at | updated_at |
| --- | --- | --- | --- | --- | --- |
| 1 | 49 | 28 | 17 | Sat Dec 13 2025 02:57:09 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:57:09 GMT-0600 (Central Stan... |
| 2 | 50 | 49 | 47 | Sat Dec 13 2025 02:57:09 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:57:09 GMT-0600 (Central Stan... |
| 3 | 23 | 33 | 46 | Sat Dec 13 2025 02:57:09 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:57:09 GMT-0600 (Central Stan... |
| 4 | 32 | 41 | 45 | Sat Dec 13 2025 02:57:09 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:57:09 GMT-0600 (Central Stan... |
| 5 | 24 | 45 | 4 | Sat Dec 13 2025 02:57:09 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:57:09 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:43:23.943Z*
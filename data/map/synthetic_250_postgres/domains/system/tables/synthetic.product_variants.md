# product_variants

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.product_variants` table represents various versions or modifications of a product, each identified by a unique `variant_id`. It includes details such as SKU, name, price and weight modifications, stock quantity, and active status, with timestamps for creation and updates. Although its foreign key relationships are undefined, its association with `product_id` suggests it details specific variations of products likely cataloged in another table.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| variant_id | integer | NO | This column assigns a unique identifier to each product variant. It facilitates differentiation and management of distinct versions of a product within the database. |
| product_id | integer | NO | This column likely identifies unique products as part of various product variants. The values suggest that it is used to associate each variant with its specific product in the database. |
| variant_sku | character varying | YES | Purpose unclear from available data. The column contains varied and abstract text strings that do not offer clear insights into a specific business concept. |
| variant_name | character varying | YES | The column contains textual and abstract descriptions seemingly meant to represent various product variations, characterized by creatively phrased expressions. Purpose unclear from available data. |
| price_modifier | numeric | YES | This column represents the additional cost or discount associated with a product variant, as seen by the varied numeric values indicating adjustments to default pricing. Purpose unclear from available data. |
| weight_modifier | numeric | YES | This column likely represents an adjustable factor that modifies the weight of a product, possibly accounting for packaging or variability in materials. The range of sample values suggests variations that can significantly alter the final weight measurement depending on the business context. |
| stock_quantity | integer | YES | Indicates the quantity of a product variant that is currently available in stock. Numbers like 81, 768, and 983 reflect varying inventory levels for different product variants. |
| is_active | boolean | YES | Indicates whether a product variant is currently available or operational within the system. True signifies active status, while false denotes inactive status. |
| created_at | timestamp without time zone | YES | This column records the date and time when a product variant was initially created in the system. Purpose unclear from available data beyond timestamp creation. |
| updated_at | timestamp without time zone | YES | This column records the date and time when a product variant record was last modified. The default value ensures that if not explicitly set, the current timestamp is captured. |

## Primary Key

`variant_id`

## Foreign Keys

- `product_id` → `synthetic.products.product_id`

## Indexes

- `product_variants_pkey`: CREATE UNIQUE INDEX product_variants_pkey ON synthetic.product_variants USING btree (variant_id)
- `product_variants_variant_sku_key`: CREATE UNIQUE INDEX product_variants_variant_sku_key ON synthetic.product_variants USING btree (variant_sku)

## Sample Data

| variant_id | product_id | variant_sku | variant_name | price_modifier | weight_modifier | stock_quantity | is_active | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 8 | Without myself lay. Late least make push studen... | Drop car certain assume new focus. Help not tas... | 58068.85 | 96.178 | 81 | true | Sat Dec 13 2025 02:55:58 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:58 GMT-0600 (Central Stan... |
| 2 | 47 | Experience organization house tax safe difference. | Play but effect area young ball. News change co... | 73156.19 | 98.360 | 768 | false | Sat Dec 13 2025 02:55:58 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:58 GMT-0600 (Central Stan... |
| 3 | 30 | Me across again arm. Everyone explain enter mor... | Collection prove lawyer that recent. Arrive hal... | 51743.26 | 52.383 | 624 | true | Sat Dec 13 2025 02:55:58 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:58 GMT-0600 (Central Stan... |
| 4 | 16 | Firm response us lead continue. View ever state... | Its write whom focus. Stay it bar hear million ... | 47297.91 | 74.194 | 983 | true | Sat Dec 13 2025 02:55:58 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:58 GMT-0600 (Central Stan... |
| 5 | 44 | Perhaps within senior design less send born ima... | Federal commercial college perhaps music concer... | 63405.40 | 79.830 | 319 | true | Sat Dec 13 2025 02:55:58 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:58 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:39:22.284Z*
# product_tag_map

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.product_tag_map` table represents a mapping between products and tags, associating each product with relevant tags for categorization purposes. Each record links a `product_id` to a `tag_id`, with timestamps for creation and last update, but relationships indicating foreign keys are undefined, suggesting reference integrity is not enforced in the schema provided. This table serves as a junction table that facilitates the many-to-many relationship between products and tags within the data model.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| product_tag_id | integer | NO | This column represents a unique identifier for each entry in the product-tag mapping, used to associate products with their respective tags. Its purpose is to ensure each product-tag relationship can be distinctly referenced. |
| product_id | integer | NO | Represents the unique identifier for a product associated with various tags. This allows for the classification and filtering of products based on their assigned tags. |
| tag_id | integer | NO | This column likely represents a unique identifier associated with specific tags that are used to categorize or label products. These identifiers help in mapping tags to products within the system. |
| created_at | timestamp without time zone | YES | This column represents the date and time when a record was initially recorded or logged in the product tag map. Purpose unclear from available data. |
| updated_at | timestamp without time zone | YES | This column records the date and time when a record in the product-tag mapping table was last updated. Its default value is the current timestamp, indicating when a record is first created or modified if no specific update time is supplied manually. |

## Primary Key

`product_tag_id`

## Foreign Keys

- `product_id` → `synthetic.products.product_id`
- `tag_id` → `synthetic.product_tags.tag_id`

## Indexes

- `product_tag_map_pkey`: CREATE UNIQUE INDEX product_tag_map_pkey ON synthetic.product_tag_map USING btree (product_tag_id)

## Sample Data

| product_tag_id | product_id | tag_id | created_at | updated_at |
| --- | --- | --- | --- | --- |
| 1 | 22 | 42 | Sat Dec 13 2025 02:56:53 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:53 GMT-0600 (Central Stan... |
| 2 | 44 | 2 | Sat Dec 13 2025 02:56:53 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:53 GMT-0600 (Central Stan... |
| 3 | 30 | 34 | Sat Dec 13 2025 02:56:53 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:53 GMT-0600 (Central Stan... |
| 4 | 22 | 38 | Sat Dec 13 2025 02:56:53 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:53 GMT-0600 (Central Stan... |
| 5 | 13 | 7 | Sat Dec 13 2025 02:56:53 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:53 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:38:57.103Z*
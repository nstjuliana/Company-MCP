# product_attribute_values

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The table "synthetic.product_attribute_values" captures specific attribute values associated with products, identified by unique "value_id" keys. Each entry links a "product_id" to an "attribute_id" with a corresponding "attribute_value," while tracking its creation and last update timestamps. Although it references undefined foreign keys suggesting relationships to unspecified tables, it primarily serves as a detail-oriented table providing expanded descriptive data for products in the broader synthetic database.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| value_id | integer | NO | This column represents a unique identifier for each record within the product attribute values table, ensuring each entry is distinct and can be referenced individually. It is essential for maintaining data integrity and tracking specific attribute values linked to products. |
| product_id | integer | NO | This column likely contains identifiers corresponding to different products, serving as a reference to associate each product with its specific attributes within the data set. Purpose unclear from available data. |
| attribute_id | integer | NO | This column represents identifiers for specific attributes associated with products. It serves as a reference to link each attribute value to a particular attribute definition within the product system. |
| attribute_value | character varying | YES | This column contains detailed textual descriptions or narratives related to various product attributes, likely serving as marketing copy or descriptions for different product aspects. The entries appear to be verbose and diverse, highlighting different features or qualities. |
| created_at | timestamp without time zone | YES | This column records the timestamp for when a product attribute value was created or logged in the system. It is initialized with the current system time upon creation, but its purpose in the broader business context is unclear from the available data. |
| updated_at | timestamp without time zone | YES | This column records the date and time when a product attribute's information was last updated. It reflects the most recent modification timestamp, indicating potentially when changes were made to the product attribute details. |

## Primary Key

`value_id`

## Foreign Keys

- `attribute_id` → `synthetic.product_attributes.attribute_id`
- `product_id` → `synthetic.products.product_id`

## Indexes

- `product_attribute_values_pkey`: CREATE UNIQUE INDEX product_attribute_values_pkey ON synthetic.product_attribute_values USING btree (value_id)

## Sample Data

| value_id | product_id | attribute_id | attribute_value | created_at | updated_at |
| --- | --- | --- | --- | --- | --- |
| 1 | 6 | 46 | Beautiful sport lead power identify. Available ... | Sat Dec 13 2025 02:56:07 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:07 GMT-0600 (Central Stan... |
| 2 | 42 | 38 | Hospital resource any series note board often. ... | Sat Dec 13 2025 02:56:07 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:07 GMT-0600 (Central Stan... |
| 3 | 19 | 27 | Simply would change nice back every. To so cost... | Sat Dec 13 2025 02:56:07 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:07 GMT-0600 (Central Stan... |
| 4 | 45 | 50 | Might activity more. Try person while say anyon... | Sat Dec 13 2025 02:56:07 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:07 GMT-0600 (Central Stan... |
| 5 | 31 | 45 | Stage certain road staff.
West value gas push g... | Sat Dec 13 2025 02:56:07 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:07 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:38:56.833Z*
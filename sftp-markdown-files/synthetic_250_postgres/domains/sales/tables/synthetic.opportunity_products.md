# opportunity_products

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.opportunity_products` table represents the products associated with a specific sales opportunity, capturing details like product, quantity, unit price, discount, and total price. The primary key, `op_product_id`, uniquely identifies each product entry linked to an `opportunity_id`, with `product_id` specifying the product involved. This table appears to support calculating revenue forecasts and analyzing the composition of sales opportunities but does not explicitly have defined foreign key relationships in the provided data.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| op_product_id | integer | NO | This column represents a unique identifier for each product associated with specific business opportunities. Each identifier is automatically assigned in a sequential manner. |
| opportunity_id | integer | NO | This column identifies unique business opportunities associated with product offerings. Each value represents a distinct opportunity to sell or promote products to potential clients or partners. |
| product_id | integer | YES | This column appears to represent identifiers for various products associated with business opportunities. Purpose unclear from available data. |
| product_name | character varying | YES | This column appears to represent descriptions or narratives related to varying products, likely offering detailed contextual information or promotional content. The purpose is unclear from available data as the sample values are broad and varied. |
| quantity | numeric | YES | The column represents the amount of a particular product associated with a sales opportunity, expressed as a numeric value. Purpose unclear from available data. |
| unit_price | numeric | YES | This column represents the monetary value per unit of a product associated with different business opportunities. It reflects the price set for individual units within various sales opportunities. |
| discount | numeric | YES | This column represents the monetary amount discounted on opportunity products, as evidenced by the sample values which indicate notable reductions from original prices. The range of values suggests variation in discount levels likely corresponding to different promotional strategies or product-specific incentives. |
| total_price | numeric | YES | Represents the total cost associated with the products linked to a business opportunity, expressed numerically. The figures indicate various monetary values related to distinct business transactions. |
| description | text | YES | Summarizes key attributes, events, or concepts associated with products in relation to opportunities, highlighting interactions, influences, and strategic elements. Purpose unclear from available data. |
| created_at | timestamp without time zone | YES | This column records the date and time when a product opportunity is created. It captures the creation timestamp in relation to the Central Standard Time zone. |
| updated_at | timestamp without time zone | YES | This column indicates the date and time when records in the opportunity_products table were last modified. The entries are automatically set to the current time if no specific update is provided. |

## Primary Key

`op_product_id`

## Foreign Keys

- `opportunity_id` → `synthetic.opportunities.opportunity_id`

## Indexes

- `opportunity_products_pkey`: CREATE UNIQUE INDEX opportunity_products_pkey ON synthetic.opportunity_products USING btree (op_product_id)

## Sample Data

| op_product_id | opportunity_id | product_id | product_name | quantity | unit_price | discount | total_price | description | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 16 | 7 | Provide seat eight teach leader. Tell baby thin... | 260.79 | 2362.86 | 753.76 | 9540.81 | Important relationship manage among very. A cau... | Sat Dec 13 2025 03:18:21 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:18:21 GMT-0600 (Central Stan... |
| 2 | 20 | 597 | Military me move around claim defense.
Whose so... | 722.88 | 124.24 | 653.68 | 6930.76 | American audience oil. Whom understand late min... | Sat Dec 13 2025 03:18:21 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:18:21 GMT-0600 (Central Stan... |
| 3 | 4 | 684 | Send discussion off wide never everybody. Blue ... | 118.22 | 3075.00 | 405.42 | 5030.18 | Sense over teacher add family. | Sat Dec 13 2025 03:18:21 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:18:21 GMT-0600 (Central Stan... |
| 4 | 46 | 789 | Thus sit story admit. Nor stand like design lea... | 310.98 | 1182.98 | 916.13 | 2957.43 | Bag for development station black spend meeting... | Sat Dec 13 2025 03:18:21 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:18:21 GMT-0600 (Central Stan... |
| 5 | 40 | 227 | Carry region them professor need care almost di... | 219.13 | 1344.35 | 153.19 | 7479.87 | Organization poor entire others. Her game they ... | Sat Dec 13 2025 03:18:21 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:18:21 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:41:56.271Z*
# product_bundles

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.product_bundles` table represents collections of products that are offered together at a discounted rate, identified uniquely by the `bundle_id` and associated with individual products via the `bundle_product_id`. The table includes details such as the percentage discount applied to each bundle (`discount_percentage`), its activation status (`is_active`), and timestamps for the bundle's creation and most recent update (`created_at` and `updated_at`). This table likely serves as a link between products and promotional offers, although no direct foreign key relationships to other tables are defined.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| bundle_id | integer | NO | This column uniquely identifies each product bundle within the synthetic company's offerings. Purpose unclear from available data. |
| bundle_product_id | integer | NO | This column likely represents unique identifiers for products included in various bundles offered by a business. Each value corresponds to a distinct product that is part of a larger collection. |
| discount_percentage | numeric | YES | This column represents the percentage discount offered on product bundles, indicating the reduction from the original price. The values suggest varying levels of discounts that can be applied to bundled products, with the possibility of no discount being applied if not specified. |
| is_active | boolean | YES | This column indicates whether a product bundle is currently active or not. "True" suggests the bundle is active, while "False" implies it is inactive, although the specific criteria for activation are not detailed. |
| created_at | timestamp without time zone | YES | This column records the date and time when a product bundle is created in the system, with a default value set to the current timestamp if not otherwise specified. The purpose or specific business use within the product bundles table remains unclear from the available data. |
| updated_at | timestamp without time zone | YES | This column records the last modification date and time for entries in the product bundles, potentially reflecting updates or changes made to bundle details. The default setting to the current timestamp implies it captures the update moment automatically, but the specific business context for its use is unclear from the available data. |

## Primary Key

`bundle_id`

## Foreign Keys

- `bundle_product_id` → `synthetic.products.product_id`

## Indexes

- `product_bundles_pkey`: CREATE UNIQUE INDEX product_bundles_pkey ON synthetic.product_bundles USING btree (bundle_id)

## Sample Data

| bundle_id | bundle_product_id | discount_percentage | is_active | created_at | updated_at |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 46.53 | false | Sat Dec 13 2025 02:56:59 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:59 GMT-0600 (Central Stan... |
| 2 | 28 | 45.12 | false | Sat Dec 13 2025 02:56:59 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:59 GMT-0600 (Central Stan... |
| 3 | 27 | 36.75 | false | Sat Dec 13 2025 02:56:59 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:59 GMT-0600 (Central Stan... |
| 4 | 21 | 27.30 | true | Sat Dec 13 2025 02:56:59 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:59 GMT-0600 (Central Stan... |
| 5 | 12 | 44.17 | false | Sat Dec 13 2025 02:56:59 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:59 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:39:22.208Z*
# bundle_items

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.bundle_items` table represents individual items that are part of a bundle, where each row specifies a product included in a bundle along with the quantity and whether it is required. This table serves a role in the data model as a linking entity that associates `bundle_id` and `product_id`, facilitating the management of product bundles, but lacks defined foreign key constraints to show direct relationships to other tables. The presence of timestamps `created_at` and `updated_at` indicates the table's role in tracking item configuration changes over time within a bundle.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| bundle_item_id | integer | NO | This column uniquely identifies each item within a bundle, serving as a sequential identifier for records in the table. It ensures each bundle item is distinct and can be tracked individually. |
| bundle_id | integer | NO | This column represents a unique identifier assigned to individual bundles, which may consist of multiple items grouped together for sale or promotional purposes. Each number signifies a distinct bundle within the collection. |
| product_id | integer | NO | This column contains identifiers for individual products included in a bundle. It serves to distinguish different products within the bundle offerings of the business. |
| quantity | integer | NO | This column represents the count of individual items included in a bundle. It indicates how many items are present within each bundle, with no bundles having less than one item. |
| is_required | boolean | YES | Indicates whether an item in the bundle is mandatory or optional for its inclusion. The majority of sample values suggest that most items are not required. |
| created_at | timestamp without time zone | YES | This column denotes the date and time when a record within the bundle_items table was created. It typically defaults to the current timestamp when a new record is inserted. |
| updated_at | timestamp without time zone | YES | This column records the date and time when an item in the bundle was last updated. It is used to track changes or modifications to the bundle items, with values defaulting to the current timestamp if not specified. |

## Primary Key

`bundle_item_id`

## Foreign Keys

- `bundle_id` → `synthetic.product_bundles.bundle_id`
- `product_id` → `synthetic.products.product_id`

## Indexes

- `bundle_items_pkey`: CREATE UNIQUE INDEX bundle_items_pkey ON synthetic.bundle_items USING btree (bundle_item_id)

## Sample Data

| bundle_item_id | bundle_id | product_id | quantity | is_required | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 18 | 13 | 7 | true | Sat Dec 13 2025 02:57:02 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:57:02 GMT-0600 (Central Stan... |
| 2 | 29 | 5 | 844 | false | Sat Dec 13 2025 02:57:02 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:57:02 GMT-0600 (Central Stan... |
| 3 | 39 | 16 | 538 | false | Sat Dec 13 2025 02:57:02 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:57:02 GMT-0600 (Central Stan... |
| 4 | 37 | 32 | 471 | false | Sat Dec 13 2025 02:57:02 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:57:02 GMT-0600 (Central Stan... |
| 5 | 37 | 3 | 754 | true | Sat Dec 13 2025 02:57:02 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:57:02 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:42:22.923Z*
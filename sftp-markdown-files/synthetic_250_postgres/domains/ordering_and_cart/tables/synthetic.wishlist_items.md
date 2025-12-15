# wishlist_items

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.wishlist_items` table represents individual items added to a user's wishlist, including a unique `wishlist_item_id`, associated with `wishlist_id`, `product_id`, and optionally `variant_id`. Each entry records when the item was `added_at` and includes `notes`, with timestamps for `created_at` and `updated_at` to track changes. Although specific foreign key relationships are undefined, the table plays a crucial role in linking product selections within wishlists to user interactions or preferences.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| wishlist_item_id | integer | NO | This column represents a unique identifier assigned sequentially to each item added to a user's wishlist. Its values ensure that each entry in the wishlist is distinct and can be individually referenced. |
| wishlist_id | integer | NO | This column represents the unique identifier for individual entries within a user's wishlist, ensuring each item can be distinctly associated with a specific wishlist. |
| product_id | integer | NO | This column represents unique identifiers for products that users have added to their wishlists. Each value corresponds to a specific product selected by a user for future reference or purchase. |
| variant_id | integer | YES | This column represents unique identifiers for product variants that customers have added to their wishlist. Purpose unclear from available data. |
| added_at | timestamp without time zone | YES | This column indicates when an item was added to a user's wishlist. It records the date and time of addition, defaulting to the current moment if no other value is provided. |
| notes | character varying | YES | This column contains text notes or comments associated with wishlist items, capturing diverse thoughts or additional details that users might apply to each listing. The purpose or context of these notes is unclear from the sample data provided. |
| created_at | timestamp without time zone | YES | This timestamp records the date and time when an item was added to the wishlist. It defaults to the current time when no value is provided. |
| updated_at | timestamp without time zone | YES | This column records the date and time when a wishlist item was last modified or updated. It defaults to the current timestamp if not otherwise specified. |

## Primary Key

`wishlist_item_id`

## Foreign Keys

- `product_id` → `synthetic.products.product_id`
- `variant_id` → `synthetic.product_variants.variant_id`
- `wishlist_id` → `synthetic.wishlists.wishlist_id`

## Indexes

- `wishlist_items_pkey`: CREATE UNIQUE INDEX wishlist_items_pkey ON synthetic.wishlist_items USING btree (wishlist_item_id)

## Sample Data

| wishlist_item_id | wishlist_id | product_id | variant_id | added_at | notes | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 17 | 16 | 40 | Mon Jun 09 2025 04:13:40 GMT-0500 (Central Dayl... | Right that short friend together bill range. Of... | Sat Dec 13 2025 02:56:34 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:34 GMT-0600 (Central Stan... |
| 2 | 29 | 16 | 24 | Sat Dec 21 2024 15:33:47 GMT-0600 (Central Stan... | Daughter own this economy one. Store left song ... | Sat Dec 13 2025 02:56:34 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:34 GMT-0600 (Central Stan... |
| 3 | 38 | 44 | 42 | Sat Jul 19 2025 02:56:17 GMT-0500 (Central Dayl... | Military national without newspaper want for. P... | Sat Dec 13 2025 02:56:34 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:34 GMT-0600 (Central Stan... |
| 4 | 30 | 6 | 1 | Wed Jul 17 2024 15:16:53 GMT-0500 (Central Dayl... | Hold itself scene summer appear participant mis... | Sat Dec 13 2025 02:56:34 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:34 GMT-0600 (Central Stan... |
| 5 | 31 | 9 | 21 | Sat Nov 08 2025 09:22:59 GMT-0600 (Central Stan... | Theory team training different TV evening. Capi... | Sat Dec 13 2025 02:56:34 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:34 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:44:58.986Z*
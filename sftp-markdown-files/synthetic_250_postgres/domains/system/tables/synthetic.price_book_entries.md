# price_book_entries

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The "synthetic.price_book_entries" table represents entries in a pricing catalog, with each entry identified by a unique "entry_id" and includes details such as the associated "price_book_id" and "product_id." Each entry specifies a "unit_price" and tracks its status with "is_active," alongside timestamp columns "created_at" and "updated_at" for record management. This table plays a role in the data model by linking specific product pricing information to price books, although its specific relationships with other tables are unspecified.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| entry_id | integer | NO | This column represents a unique identifier assigned incrementally to each entry in the price book. It serves as a primary key to distinguish individual records within the table. |
| price_book_id | integer | NO | This column represents a unique identifier for each entry within the associated pricing catalog or list. It serves as a reference to link specific price book entries to their corresponding price books. |
| product_id | integer | NO | This column uniquely identifies products within the price book entries, ensuring each product can be distinctly referenced. These numerical identifiers are critical for tracking and managing pricing information related to specific products. |
| unit_price | numeric | NO | This column represents the price assigned to individual items or services when entered into the price book. It ensures precise billing or cost tracking, with values typically ranging from several thousand to tens of thousands of currency units. |
| is_active | boolean | YES | This column indicates whether an entry in the price book is currently active or inactive, with "true" signaling active status and "false" signaling inactive status. The column allows for entries to be inactive by default if not otherwise specified. |
| created_at | timestamp without time zone | YES | The column records the date and time of when an entry in the price book was created, defaulting to the current timestamp. It captures the moment an entry is added, serving as a timestamp for creation events. |
| updated_at | timestamp without time zone | YES | This column likely records the date and time when a price book entry was last updated, reflecting changes to pricing data. The entries demonstrate a uniform update timestamp, possibly indicating a bulk update process rather than individual entry changes. |

## Primary Key

`entry_id`

## Foreign Keys

- `price_book_id` → `synthetic.price_books.price_book_id`

## Indexes

- `price_book_entries_pkey`: CREATE UNIQUE INDEX price_book_entries_pkey ON synthetic.price_book_entries USING btree (entry_id)

## Sample Data

| entry_id | price_book_id | product_id | unit_price | is_active | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 31 | 555 | 36484.51 | false | Sat Dec 13 2025 02:59:20 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:59:20 GMT-0600 (Central Stan... |
| 2 | 13 | 5654 | 6698.93 | true | Sat Dec 13 2025 02:59:20 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:59:20 GMT-0600 (Central Stan... |
| 3 | 17 | 6383 | 18737.59 | false | Sat Dec 13 2025 02:59:20 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:59:20 GMT-0600 (Central Stan... |
| 4 | 30 | 6513 | 78394.11 | false | Sat Dec 13 2025 02:59:20 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:59:20 GMT-0600 (Central Stan... |
| 5 | 29 | 2178 | 81596.54 | false | Sat Dec 13 2025 02:59:20 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:59:20 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:39:21.998Z*
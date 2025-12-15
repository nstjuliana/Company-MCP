# content_category_map

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.content_category_map` table represents the association between content items and their associated categories, as identified by the `content_id` and `category_id` columns. The primary key, `map_id`, uniquely identifies each mapping, with timestamp columns `created_at` and `updated_at` indicating record history. This table serves as a junction table in the database, facilitating many-to-many relationships between content and categories, though its foreign key relationships are not defined.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| map_id | integer | NO | This column represents a unique identifier for each entry in the content-category mapping, ensuring that each association between content and category is distinct. Its sequential numeric values indicate its role in tracking or indexing these associations. |
| content_id | integer | NO | This identifier associates a piece of content with various categories, facilitating content classification. The purpose of this mapping in business terms is unclear from the available data. |
| category_id | integer | NO | This column likely represents identifiers associated with different content categories, mapping content to specific category IDs for organizational purposes. The sequential integers suggest that each number uniquely distinguishes a particular category. |
| created_at | timestamp without time zone | YES | This column records the date and time when a record in the content_category_map table was created. The timestamp typically uses the current time by default, but it is not mandatory to have a value for each entry. |
| updated_at | timestamp without time zone | YES | This column records the date and time when a record in the content category map table was last updated. The purpose is unclear from the available data. |

## Primary Key

`map_id`

## Foreign Keys

- `category_id` → `synthetic.content_categories.category_id`
- `content_id` → `synthetic.content_pieces.content_id`

## Indexes

- `content_category_map_pkey`: CREATE UNIQUE INDEX content_category_map_pkey ON synthetic.content_category_map USING btree (map_id)

## Sample Data

| map_id | content_id | category_id | created_at | updated_at |
| --- | --- | --- | --- | --- |
| 1 | 6 | 46 | Sat Dec 13 2025 03:15:10 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:15:10 GMT-0600 (Central Stan... |
| 2 | 7 | 1 | Sat Dec 13 2025 03:15:10 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:15:10 GMT-0600 (Central Stan... |
| 3 | 14 | 31 | Sat Dec 13 2025 03:15:10 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:15:10 GMT-0600 (Central Stan... |
| 4 | 5 | 9 | Sat Dec 13 2025 03:15:10 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:15:10 GMT-0600 (Central Stan... |
| 5 | 38 | 15 | Sat Dec 13 2025 03:15:10 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:15:10 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:44:14.254Z*
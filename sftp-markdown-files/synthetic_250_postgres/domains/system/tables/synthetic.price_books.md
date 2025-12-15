# price_books

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.price_books` table represents a collection of price books, which are entities that define pricing structures or catalogs possibly utilized by a business. Key details for each price book, such as its unique identifier (`price_book_id`), name, and status indicators (`is_active` and `is_standard`), are captured along with timestamps for creation and updates (`created_at` and `updated_at`). This table operates independently within the database, as it neither references nor is referenced by any other tables, implying it serves as a standalone component potentially for pricing management in the broader data model.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| price_book_id | integer | NO | Represents a unique identifier assigned to each price book entry within the system. This identifier is incrementally generated to ensure each price book is distinct. |
| price_book_name | character varying | NO | This column contains descriptive names or titles associated with price books, which may refer to market analysis reports, company agreements, or business strategies. The exact purpose or context of these names is unclear from the available data. |
| description | text | YES | This column contains textual descriptions that appear to be abstract or conceptual statements, possibly relating to various topics such as language, nations, social relationships, and ideas. Purpose unclear from available data. |
| is_active | boolean | YES | This column indicates whether a particular price book is currently active or not, with "true" representing active and "false" representing inactive status. Purpose unclear from available data. |
| is_standard | boolean | YES | This column indicates whether a given price book is classified as standard within the business context. A value of "true" signifies a standard classification, whereas "false" indicates otherwise. |
| created_at | timestamp without time zone | YES | This column records the date and time when a price book entry was created, reflecting the moment of initialization within the system's process. The consistent sample values suggest its primary use is for tracking creation times for these entries. |
| updated_at | timestamp without time zone | YES | This column records the timestamp of when a particular entry in the price books table was last updated. It reflects changes applied to the entry, with timestamps set to the current time by default. |

## Primary Key

`price_book_id`

## Indexes

- `price_books_pkey`: CREATE UNIQUE INDEX price_books_pkey ON synthetic.price_books USING btree (price_book_id)

## Sample Data

| price_book_id | price_book_name | description | is_active | is_standard | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Firm present actually. Leg some growth hold con... | Find even everybody course through language. Ed... | false | false | Sat Dec 13 2025 02:59:17 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:59:17 GMT-0600 (Central Stan... |
| 2 | Research happen reality impact fact ask. Fight ... | Our among blood nation prepare large interest w... | false | true | Sat Dec 13 2025 02:59:17 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:59:17 GMT-0600 (Central Stan... |
| 3 | Trial together reality indicate according autho... | Standard determine read. Around watch buy story... | false | false | Sat Dec 13 2025 02:59:17 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:59:17 GMT-0600 (Central Stan... |
| 4 | High shoulder country seven mother position. De... | Do treat each establish various. Wife court saf... | true | false | Sat Dec 13 2025 02:59:17 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:59:17 GMT-0600 (Central Stan... |
| 5 | Floor size yourself bed. Republican line troubl... | Indeed back create score project year future. O... | true | true | Sat Dec 13 2025 02:59:17 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:59:17 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:39:21.479Z*
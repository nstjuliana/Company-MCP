# wishlists

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The "synthetic.wishlists" table represents customer wishlists, where each wishlist is uniquely identified by a "wishlist_id" and associated with a "customer_id" indicating its owner. The table includes attributes such as "wishlist_name" for the title of the wishlist, whether it is "is_public" for visibility, and timestamps "created_at" and "updated_at" to track changes. This table is primarily used to manage data for customer wishlists but currently does not explicitly reference or connect with other tables through defined relationships.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| wishlist_id | integer | NO | This column uniquely identifies each wishlist within the system, incrementing with each new entry. It serves as a primary key to track individual wishlists. |
| customer_id | integer | NO | This column represents the unique identifier for different customers who have created wishlists. Each number corresponds to a distinct customer. |
| wishlist_name | character varying | YES | The column represents custom names given to collections or lists of desired items or entities, presumably created by users. Purpose unclear from available data. |
| is_public | boolean | YES | Indicates whether a wishlist is publicly accessible or not. A value of true means the wishlist can be viewed by others, while false signifies it is private. |
| created_at | timestamp without time zone | YES | This column records the date and time when each wishlist entry was created, reflecting the instance in the standard time zone of the creator. The default value suggests that it logs the creation timestamp automatically, though entries can be updated to null. |
| updated_at | timestamp without time zone | YES | This column records the most recent date and time when a wishlist record was updated. It reflects changes or modifications made to the wishlist entries. |

## Primary Key

`wishlist_id`

## Foreign Keys

- `customer_id` → `synthetic.customers.customer_id`

## Indexes

- `wishlists_pkey`: CREATE UNIQUE INDEX wishlists_pkey ON synthetic.wishlists USING btree (wishlist_id)

## Sample Data

| wishlist_id | customer_id | wishlist_name | is_public | created_at | updated_at |
| --- | --- | --- | --- | --- | --- |
| 1 | 7 | Forward step election government society hospit... | true | Sat Dec 13 2025 02:56:29 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:29 GMT-0600 (Central Stan... |
| 2 | 45 | Name voice always soldier stock. Account over d... | false | Sat Dec 13 2025 02:56:29 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:29 GMT-0600 (Central Stan... |
| 3 | 33 | Live staff total get finish apply trial.
Water ... | true | Sat Dec 13 2025 02:56:29 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:29 GMT-0600 (Central Stan... |
| 4 | 23 | Its half report already wind provide once someo... | false | Sat Dec 13 2025 02:56:29 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:29 GMT-0600 (Central Stan... |
| 5 | 39 | Trial whom machine song example. Product whole ... | false | Sat Dec 13 2025 02:56:29 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:29 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:44:30.756Z*
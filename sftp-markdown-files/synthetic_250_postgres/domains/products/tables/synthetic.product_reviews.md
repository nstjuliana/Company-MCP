# product_reviews

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The "synthetic.product_reviews" table captures customer feedback on products, with each review uniquely identified by "review_id". It includes details such as "product_id", "customer_id", "rating", "title", "review_text", and other attributes like "is_verified_purchase", indicative of the purchase status, and "helpful_votes" for community feedback. While it refers to unspecified foreign keys and is standalone with no tables referencing it, the table plays a crucial role in presenting insights into customer satisfaction and product performance within the data model.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| review_id | integer | NO | This column uniquely identifies each product review entry within the database, ensuring each review can be distinctly referenced. It is automatically incremented to maintain unique identifiers for new entries. |
| product_id | integer | NO | This column represents unique identifiers assigned to products for which reviews have been submitted. Each value corresponds to a specific product within a catalog, as indicated by the different numerical values. |
| customer_id | integer | YES | This column likely represents a unique identifier assigned to each customer who has submitted a product review. Purpose unclear from available data. |
| rating | integer | NO | This column represents customer-rated feedback scores for products, reflecting varying levels of satisfaction or quality with values ranging from 1 to 5. The scores suggest a system where a higher number indicates a more favorable review. |
| title | character varying | YES | This column contains brief summaries or highlights for individual product reviews. These entries often consist of short, fragmented statements that hint at themes or key points from the reviews. |
| review_text | text | YES | This column contains customer reviews or feedback related to products, generally expressed as sequences of thoughts or experiences. The content varies significantly, implying comments on different aspects such as usage, opinions, and personal insights about products. |
| is_verified_purchase | boolean | YES | This column indicates whether a product review is associated with a verified purchase, helping to differentiate authentic feedback from potentially unauthenticated reviews. The presence of both true and false values suggests some reviews are verified, while others are not. |
| is_approved | boolean | YES | This column indicates whether a product review has been approved for publication or not. A value of true suggests the review is approved, whereas false indicates it is not approved; however, its specific use in business processes is unclear from the provided data. |
| helpful_votes | integer | YES | This column likely represents the number of users who found a particular product review helpful, given that the sample values are varying integers. The purpose of collecting this data is to gauge the perceived usefulness of customer feedback for potential buyers. |
| created_at | timestamp without time zone | YES | This column captures the date and time when a product review was created. The timestamps suggest that reviews are recorded in a standardized format but the specific purpose for this data is unclear from the available values. |
| updated_at | timestamp without time zone | YES | This column records the date and time when a product review was last modified. It reflects updates in the reviews, allowing tracking of changes over time. |

## Primary Key

`review_id`

## Foreign Keys

- `customer_id` → `synthetic.customers.customer_id`
- `product_id` → `synthetic.products.product_id`

## Indexes

- `product_reviews_pkey`: CREATE UNIQUE INDEX product_reviews_pkey ON synthetic.product_reviews USING btree (review_id)

## Sample Data

| review_id | product_id | customer_id | rating | title | review_text | is_verified_purchase | is_approved | helpful_votes | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 14 | 34 | 1 | Stuff middle long claim bring. | Focus discuss eight arm several. Today must pro... | false | false | 8871 | Sat Dec 13 2025 02:56:16 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:16 GMT-0600 (Central Stan... |
| 2 | 9 | 31 | 3 | Rule too others. | Happen money free involve worry who. Both cup f... | false | false | 352 | Sat Dec 13 2025 02:56:16 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:16 GMT-0600 (Central Stan... |
| 3 | 19 | 13 | 1 | Want forward. | Ground amount method go. Action continue career... | true | true | 8514 | Sat Dec 13 2025 02:56:16 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:16 GMT-0600 (Central Stan... |
| 4 | 42 | 22 | 4 | Six visit. | Worry nice draw area. Change trip base task mil... | false | false | 7966 | Sat Dec 13 2025 02:56:16 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:16 GMT-0600 (Central Stan... |
| 5 | 38 | 43 | 5 | Family condition indeed girl. | Music wait strategy history. Measure not educat... | false | false | 4983 | Sat Dec 13 2025 02:56:16 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:16 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:38:58.564Z*
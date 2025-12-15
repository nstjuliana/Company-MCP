# PRODUCTS_186

**Database:** synthetic_250_snowflake
**Schema:** SYNTHETIC
**Description:** The SYNTHETIC.PRODUCTS_186 table represents a collection of product records, each identified uniquely by a PRODUCT_ID, and includes attributes such as SKU, NAME, PRICE, CATEGORY_ID, and various timestamp and textual attributes resembling review and wishlist metadata. This table appears to operate independently within the data model since it has no defined relationships with other tables. The presence of product-related metadata fields suggests it might be used for tracking or cataloging product data potentially in a retail or inventory context.

**Row Count:** 10

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| PRODUCT_ID | NUMBER | NO | This column uniquely identifies each product within the product dataset to ensure accurate tracking and referencing. The values are sequential identifiers that distinguish each item without implying any hierarchy or sequence in the product catalog. |
| SKU | TEXT | YES | This column holds unique identifiers commonly used in business to track and manage individual products in a catalog or inventory. Purpose unclear from available data beyond representing product identifiers. |
| NAME | TEXT | NO | This column contains sequentially numbered identifiers for products, suggesting they are part of a series or list of items within a specific context. Purpose unclear from available data. |
| PRICE | NUMBER | NO | This column represents the cost associated with individual products listed in the dataset. Purpose unclear from available data. |
| CATEGORY_ID | NUMBER | YES | This column likely represents distinct categories or classifications of products within the dataset. Each number corresponds to a specific product category, though their precise meanings are not detailed in the available data. |
| REVIEW_206_ATTR_0 | TIMESTAMP_NTZ | NO | This column captures the specific date and time a product review was created, referenced in Central Standard Time. Each timestamp indicates when a review entry was logged within the system. |
| RATING_206_ATTR_1 | TEXT | YES | This column appears to represent a categorical rating attribute associated with products, with values ranging from 1 to 10. Purpose unclear from available data. |
| CHECKOUT_206_ATTR_2 | NUMBER | YES | Purpose unclear from available data. |
| WISHLIST_206_ATTR_3 | TIMESTAMP_NTZ | NO | This column records the precise date and time a certain event or action related to the wishlist occurred, consistently capturing the current timestamp at the time of entry. Purpose unclear from available data. |
| REVIEW_206_ATTR_4 | TIMESTAMP_NTZ | YES | This column likely represents the date and time when a product review-related event occurred. Purpose unclear from available data as the specific nature of the event is not specified. |
| WISHLIST_206_ATTR_5 | NUMBER | YES | This column appears to be related to specific attributes or identifiers associated with a wishlist feature in a product database. Each number may represent a distinct product or a category of products that are wished for by users. |

## Primary Key

`PRODUCT_ID`

## Sample Data

| PRODUCT_ID | SKU | NAME | PRICE | CATEGORY_ID | REVIEW_206_ATTR_0 | RATING_206_ATTR_1 | CHECKOUT_206_ATTR_2 | WISHLIST_206_ATTR_3 | REVIEW_206_ATTR_4 | WISHLIST_206_ATTR_5 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Sample SKU 1 | PRODUCTS_186 1 | 100 | 1 | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | Sample RATING_206_ATTR_1 1 | null | Fri Dec 12 2025 11:26:57 GMT-0600 (Central Stan... | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | null |
| 2 | Sample SKU 2 | PRODUCTS_186 2 | 101 | 2 | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... | Sample RATING_206_ATTR_1 2 | 101 | Fri Dec 12 2025 11:26:57 GMT-0600 (Central Stan... | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... | 101 |
| 3 | Sample SKU 3 | PRODUCTS_186 3 | 102 | 3 | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... | Sample RATING_206_ATTR_1 3 | 102 | Fri Dec 12 2025 11:26:57 GMT-0600 (Central Stan... | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... | 102 |
| 4 | Sample SKU 4 | PRODUCTS_186 4 | 103 | 4 | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... | Sample RATING_206_ATTR_1 4 | null | Fri Dec 12 2025 11:26:57 GMT-0600 (Central Stan... | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... | null |
| 5 | Sample SKU 5 | PRODUCTS_186 5 | 104 | 5 | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... | Sample RATING_206_ATTR_1 5 | 104 | Fri Dec 12 2025 11:26:57 GMT-0600 (Central Stan... | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... | 104 |

*Generated at: 2025-12-14T23:43:57.350Z*
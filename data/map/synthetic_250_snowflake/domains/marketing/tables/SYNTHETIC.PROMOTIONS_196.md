# PROMOTIONS_196

**Database:** synthetic_250_snowflake
**Schema:** SYNTHETIC
**Description:** The SYNTHETIC.PROMOTIONS_196 table represents promotional campaigns within the database, identifiable by a unique PROMOTION_ID. It stores details such as the promotion's name, description, associated dates, and attributes relevant to wishlist, shipping, cart, and review contexts. This table functions independently without explicit foreign key relationships, suggesting it may serve as a standalone reference for promotions.

**Row Count:** 10

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| PROMOTION_ID | NUMBER | NO | This column represents the unique identifier assigned to each promotion in the system, serving as a sequential number to differentiate promotional entries. Its purpose is to ensure each promotion can be individually referenced and managed. |
| NAME | TEXT | NO | This column represents identifiers for different promotion campaigns in a sequential format. Each value denotes a distinct promotion labeled with a numeric suffix. |
| DESCRIPTION | TEXT | YES | This column contains textual descriptions associated with specific records in the promotions table. Purpose unclear from available data. |
| WISHLIST_216_ATTR_0 | DATE | NO | This column likely records the dates associated with specific wishlist activities or events within a promotional context, occurring in mid-December 2025. Purpose unclear from available data. |
| SHIPPING_216_ATTR_1 | NUMBER | YES | Represents a code identifying a shipping-related attribute associated with promotions. Purpose unclear from available data. |
| CART_216_ATTR_2 | NUMBER | YES | Purpose unclear from available data. |
| REVIEW_216_ATTR_3 | DATE | YES | This column likely records the scheduled review dates for promotions. The dates are consecutive and suggest a systematic review process. |
| RATING_216_ATTR_4 | BOOLEAN | YES | Indicates whether a specific criterion or attribute related to promotions is met or not. Purpose unclear from available data. |
| RATING_216_ATTR_5 | TEXT | NO | This column appears to represent numerical ratings related to a specific aspect of a promotion, with values ranging from 1 to 10. The purpose of these ratings in business terms is unclear from the available data. |
| REVIEW_216_ATTR_6 | NUMBER | YES | This column likely represents a categorical rating or identifier used in reviews or assessments, where each number corresponds to a specific category or value. Purpose unclear from available data beyond indicating distinct classifications. |
| CREATED_AT | TIMESTAMP_NTZ | NO | This column records the date and time when each promotion was created, using the system's current timestamp at the moment of creation. It provides a precise historical reference for the timing of promotional events. |

## Primary Key

`PROMOTION_ID`

## Sample Data

| PROMOTION_ID | NAME | DESCRIPTION | WISHLIST_216_ATTR_0 | SHIPPING_216_ATTR_1 | CART_216_ATTR_2 | REVIEW_216_ATTR_3 | RATING_216_ATTR_4 | RATING_216_ATTR_5 | REVIEW_216_ATTR_6 | CREATED_AT |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | PROMOTIONS_196 1 | Description for PROMOTIONS_196 1 | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | null | null | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | true | Sample RATING_216_ATTR_5 1 | null | Fri Dec 12 2025 11:26:59 GMT-0600 (Central Stan... |
| 2 | PROMOTIONS_196 2 | Description for PROMOTIONS_196 2 | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... | 101 | 101 | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... | false | Sample RATING_216_ATTR_5 2 | 101 | Fri Dec 12 2025 11:26:59 GMT-0600 (Central Stan... |
| 3 | PROMOTIONS_196 3 | Description for PROMOTIONS_196 3 | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... | 102 | 102 | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... | true | Sample RATING_216_ATTR_5 3 | 102 | Fri Dec 12 2025 11:26:59 GMT-0600 (Central Stan... |
| 4 | PROMOTIONS_196 4 | Description for PROMOTIONS_196 4 | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... | null | null | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... | false | Sample RATING_216_ATTR_5 4 | null | Fri Dec 12 2025 11:26:59 GMT-0600 (Central Stan... |
| 5 | PROMOTIONS_196 5 | Description for PROMOTIONS_196 5 | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... | 104 | 104 | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... | true | Sample RATING_216_ATTR_5 5 | 104 | Fri Dec 12 2025 11:26:59 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:42:35.088Z*
# CART_ITEMS

**Database:** synthetic_250_snowflake
**Schema:** SYNTHETIC
**Description:** The `SYNTHETIC.CART_ITEMS` table represents individual items within a shopping cart, identifiable by the primary key `CART_ITEM_ID`. This table is isolated with no external relationships, indicating its role as a standalone entity in the data model. The columns encapsulate item-specific attributes such as name, description, ratings, reviews, and shipping information, as seen in the sample row provided.

**Row Count:** 10

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| CART_ITEM_ID | NUMBER | NO | This column represents a unique identifier assigned to each item within a customer's shopping cart, ensuring each item can be distinctly referenced and managed. |
| NAME | TEXT | NO | This column represents the unique identifiers assigned to individual items within a shopping cart, denoted by sequential numeric labels. Purpose unclear from available data. |
| DESCRIPTION | TEXT | YES | This column contains descriptive information or identifiers related to items within a shopping cart. Each entry provides a unique label or summary for individual cart items. |
| RATING_188_ATTR_0 | TEXT | NO | This column appears to represent a rating metric or score, potentially evaluating an aspect of items in the cart, with values ranging from 1 to 10. Purpose unclear from available data. |
| REVIEW_188_ATTR_1 | DATE | YES | This column contains dates that may represent an event or milestone related to review activities occurring in December 2025. Purpose unclear from available data. |
| REVIEW_188_ATTR_2 | NUMBER | YES | Purpose unclear from available data. The sample values suggest a categorical identifier or reference code, but no specific business meaning can be determined. |
| SHIPPING_188_ATTR_3 | BOOLEAN | YES | This column indicates whether a specific condition or attribute related to shipping for items in the cart is met. The purpose of the specific attribute is unclear from the available data. |
| CART_188_ATTR_4 | TEXT | NO | Purpose unclear from available data. The sample values suggest a sequential or enumerative pattern, but do not provide specific business context. |
| RATING_188_ATTR_5 | TIMESTAMP_NTZ | YES | Purpose unclear from available data. The column contains timestamp values, but the specific business context or event these timestamps represent is not evident. |

## Primary Key

`CART_ITEM_ID`

## Sample Data

| CART_ITEM_ID | NAME | DESCRIPTION | RATING_188_ATTR_0 | REVIEW_188_ATTR_1 | REVIEW_188_ATTR_2 | SHIPPING_188_ATTR_3 | CART_188_ATTR_4 | RATING_188_ATTR_5 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | CART_ITEMS 1 | Description for CART_ITEMS 1 | Sample RATING_188_ATTR_0 1 | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | null | true | Sample CART_188_ATTR_4 1 | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... |
| 2 | CART_ITEMS 2 | Description for CART_ITEMS 2 | Sample RATING_188_ATTR_0 2 | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... | 101 | false | Sample CART_188_ATTR_4 2 | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... |
| 3 | CART_ITEMS 3 | Description for CART_ITEMS 3 | Sample RATING_188_ATTR_0 3 | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... | 102 | true | Sample CART_188_ATTR_4 3 | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... |
| 4 | CART_ITEMS 4 | Description for CART_ITEMS 4 | Sample RATING_188_ATTR_0 4 | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... | null | false | Sample CART_188_ATTR_4 4 | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... |
| 5 | CART_ITEMS 5 | Description for CART_ITEMS 5 | Sample RATING_188_ATTR_0 5 | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... | 104 | true | Sample CART_188_ATTR_4 5 | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:44:01.686Z*
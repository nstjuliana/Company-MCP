# DISCOUNTS_198

**Database:** synthetic_250_snowflake
**Schema:** SYNTHETIC
**Description:** The "DISCOUNTS_198" table in the "synthetic_250_snowflake" database represents a collection of discount records, uniquely identified by the "DISCOUNT_ID" primary key. Each record includes descriptive details such as "NAME" and "DESCRIPTION", along with additional attributes for shipping and cart/wishlist dates and references. The table operates independently within the data model, as it neither references nor is referenced by other tables.

**Row Count:** 10

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| DISCOUNT_ID | NUMBER | NO | A unique identifier assigned to each discount record, ensuring distinct tracking and reference of discounts within the dataset. Purpose unclear from available data. |
| NAME | TEXT | NO | This column identifies discount categories or entries with sequential numbering, indicating they are part of a series within the dataset. Purpose unclear from available data. |
| DESCRIPTION | TEXT | NO | This column contains sequentially numbered descriptions for records in the DISCOUNTS_198 table, likely serving as placeholder text without conveying specific discount details. Purpose unclear from available data. |
| SHIPPING_218_ATTR_0 | TEXT | NO | Purpose unclear from available data. |
| CART_218_ATTR_1 | DATE | YES | This column appears to represent a date associated with specific transactions or events in a shopping cart, likely indicating when these occurred or are scheduled to occur. Purpose unclear from available data beyond representing dates. |
| WISHLIST_218_ATTR_2 | DATE | NO | This column represents the specific date for an event or action related to a wishlist, occurring sequentially from December 11, 2025. Purpose unclear from available data. |
| WISHLIST_218_ATTR_3 | TEXT | YES | Purpose unclear from available data. |

## Primary Key

`DISCOUNT_ID`

## Sample Data

| DISCOUNT_ID | NAME | DESCRIPTION | SHIPPING_218_ATTR_0 | CART_218_ATTR_1 | WISHLIST_218_ATTR_2 | WISHLIST_218_ATTR_3 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | DISCOUNTS_198 1 | Description for DISCOUNTS_198 1 | Sample SHIPPING_218_ATTR_0 1 | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | Sample WISHLIST_218_ATTR_3 1 |
| 2 | DISCOUNTS_198 2 | Description for DISCOUNTS_198 2 | Sample SHIPPING_218_ATTR_0 2 | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... | Sample WISHLIST_218_ATTR_3 2 |
| 3 | DISCOUNTS_198 3 | Description for DISCOUNTS_198 3 | Sample SHIPPING_218_ATTR_0 3 | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... | Sample WISHLIST_218_ATTR_3 3 |
| 4 | DISCOUNTS_198 4 | Description for DISCOUNTS_198 4 | Sample SHIPPING_218_ATTR_0 4 | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... | Sample WISHLIST_218_ATTR_3 4 |
| 5 | DISCOUNTS_198 5 | Description for DISCOUNTS_198 5 | Sample SHIPPING_218_ATTR_0 5 | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... | Sample WISHLIST_218_ATTR_3 5 |

*Generated at: 2025-12-14T23:39:43.480Z*
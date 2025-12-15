# WISHLISTS

**Database:** synthetic_250_snowflake
**Schema:** SYNTHETIC
**Description:** The SYNTHETIC.WISHLISTS table represents a business entity associated with storing information about individual wishlists, potentially for an e-commerce context, with each entry uniquely identified by a WISHLIST_ID. The table records details such as names, descriptions, significant dates, amounts, and possibly shipping-related attributes. With no defined relationships to other tables, it appears to function independently within the data model, likely serving as a standalone repository for wishlist information without direct ties to other entities.

**Row Count:** 10

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| WISHLIST_ID | NUMBER | NO | This column likely serves as a unique identifier for individual wishlists within the system. Each value corresponds to a distinct wishlist, ensuring differentiation between records. |
| NAME | TEXT | NO | This column represents the names assigned to different wishlists, sequentially numbered. The naming pattern suggests these are generic or placeholder names for organizing wishlist entries. |
| DESCRIPTION | TEXT | YES | The column contains descriptions detailing various wishlists, each seemingly tagged with a unique identifier or sequence, such as "1" or "2." Purpose unclear from available data beyond distinguishing different wishlist entries. |
| SHIPPING_193_ATTR_0 | TEXT | YES | Purpose unclear from available data. The sample values suggest a placeholder or a non-descriptive entry rather than a meaningful business term. |
| WISHLIST_193_ATTR_1 | TIMESTAMP_NTZ | NO | This column likely represents a series of dates and times associated with specific events or actions related to wishlists. Each entry is a non-null timestamp indicating when these events or actions are scheduled or recorded. |
| CHECKOUT_193_ATTR_2 | TIMESTAMP_NTZ | YES | This column likely records the timestamp of a specific event or action associated with customer wishlists, capturing when a certain aspect of the checkout process occurred, such as an update or a completed action. The purpose is unclear beyond this timeframe. |
| WISHLIST_193_ATTR_3 | NUMBER | NO | The column likely indicates a sequentially assigned identifier or code related to individual wishlists. The specific purpose of the numeric values is unclear from the available data. |
| CHECKOUT_193_ATTR_4 | NUMBER | YES | This column likely represents a categorical attribute related to the checkout process in a wishlist context, with sample values suggesting a sequential or categorial identifier. Purpose unclear from available data. |
| RATING_193_ATTR_5 | DATE | YES | This column appears to store dates associated with specific ratings in customer wishlists. Purpose unclear from available data. |
| REVIEW_193_ATTR_6 | NUMBER | YES | Purpose unclear from available data. |

## Primary Key

`WISHLIST_ID`

## Sample Data

| WISHLIST_ID | NAME | DESCRIPTION | SHIPPING_193_ATTR_0 | WISHLIST_193_ATTR_1 | CHECKOUT_193_ATTR_2 | WISHLIST_193_ATTR_3 | CHECKOUT_193_ATTR_4 | RATING_193_ATTR_5 | REVIEW_193_ATTR_6 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | WISHLISTS 1 | Description for WISHLISTS 1 | Sample SHIPPING_193_ATTR_0 1 | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | 100 | null | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | null |
| 2 | WISHLISTS 2 | Description for WISHLISTS 2 | Sample SHIPPING_193_ATTR_0 2 | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... | 101 | 101 | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... | 101 |
| 3 | WISHLISTS 3 | Description for WISHLISTS 3 | Sample SHIPPING_193_ATTR_0 3 | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... | 102 | 102 | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... | 102 |
| 4 | WISHLISTS 4 | Description for WISHLISTS 4 | Sample SHIPPING_193_ATTR_0 4 | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... | 103 | null | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... | null |
| 5 | WISHLISTS 5 | Description for WISHLISTS 5 | Sample SHIPPING_193_ATTR_0 5 | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... | 104 | 104 | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... | 104 |

*Generated at: 2025-12-14T23:44:02.453Z*
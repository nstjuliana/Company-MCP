# SHIPPING_ADDRESSES

**Database:** synthetic_250_snowflake
**Schema:** SYNTHETIC
**Description:** The SYNTHETIC.SHIPPING_ADDRESSES table stores data related to shipping addresses, including a unique identifier (SHIPPING_ADDRESSE_ID), descriptive information (NAME and DESCRIPTION), and various attributes that might be associated with customer interactions such as wishlist preferences, cart details, and ratings over time. Although the table has no explicit foreign key relationships to other tables, it appears to serve as a standalone repository within the data model for managing and potentially analyzing specific address-related attributes necessary for processing shipments. The presence of timestamps and status indicators suggests its role in maintaining a historical record of address updates and tracking the activity statuses of shipping addresses.

**Row Count:** 10

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| SHIPPING_ADDRESSE_ID | NUMBER | NO | This column represents a unique identifier for each shipping address entry in the system. Each number is assigned sequentially to differentiate between various shipping addresses. |
| NAME | TEXT | NO | Purpose unclear from available data. The column appears to hold sequential identifiers, but their exact business role is not evident. |
| DESCRIPTION | TEXT | YES | This column contains descriptive text associated with specific shipping addresses, potentially to elaborate on details or unique aspects of each address entry. Purpose unclear from available data. |
| WISHLIST_190_ATTR_0 | NUMBER | YES | Purpose unclear from available data; the column contains numerical codes which might be associated with specific wishlist attributes or categories. |
| WISHLIST_190_ATTR_1 | TEXT | YES | Purpose unclear from available data. The column appears to contain placeholder text associated with a wishlist attribute, but its specific function or meaning is not evident. |
| CART_190_ATTR_2 | NUMBER | YES | Purpose unclear from available data. |
| RATING_190_ATTR_3 | NUMBER | YES | This column appears to represent a rating or score associated with a shipping address, based on the numerical sample values provided. Purpose unclear from available data. |
| CART_190_ATTR_4 | TEXT | YES | Purpose unclear from available data. |
| SHIPPING_190_ATTR_5 | DATE | NO | This column likely represents the expected date of delivery for shipments, as indicated by the recurring sequence of consecutive dates. The dates suggest a schedule or timeline for package arrivals. |
| RATING_190_ATTR_6 | TEXT | YES | Purpose unclear from available data. |
| UPDATED_AT | TIMESTAMP_NTZ | YES | This column records the date and time when the shipping address information was last updated. The purpose of these updates is to ensure the data reflects any recent changes or corrections. |
| STATUS | TEXT | YES | This column likely indicates the current operational state of shipping addresses, reflecting whether they are currently in use or not. Purpose unclear from available data as only one value, "ACTIVE," is provided. |

## Primary Key

`SHIPPING_ADDRESSE_ID`

## Sample Data

| SHIPPING_ADDRESSE_ID | NAME | DESCRIPTION | WISHLIST_190_ATTR_0 | WISHLIST_190_ATTR_1 | CART_190_ATTR_2 | RATING_190_ATTR_3 | CART_190_ATTR_4 | SHIPPING_190_ATTR_5 | RATING_190_ATTR_6 | UPDATED_AT | STATUS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SHIPPING_ADDRESSES 1 | Description for SHIPPING_ADDRESSES 1 | null | Sample WISHLIST_190_ATTR_1 1 | null | null | Sample CART_190_ATTR_4 1 | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | Sample RATING_190_ATTR_6 1 | Sat Jan 10 2026 18:00:00 GMT-0600 (Central Stan... | ACTIVE |
| 2 | SHIPPING_ADDRESSES 2 | Description for SHIPPING_ADDRESSES 2 | 101 | Sample WISHLIST_190_ATTR_1 2 | 101 | 101 | Sample CART_190_ATTR_4 2 | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... | Sample RATING_190_ATTR_6 2 | Sun Jan 11 2026 18:00:00 GMT-0600 (Central Stan... | ACTIVE |
| 3 | SHIPPING_ADDRESSES 3 | Description for SHIPPING_ADDRESSES 3 | 102 | Sample WISHLIST_190_ATTR_1 3 | 102 | 102 | Sample CART_190_ATTR_4 3 | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... | Sample RATING_190_ATTR_6 3 | Mon Jan 12 2026 18:00:00 GMT-0600 (Central Stan... | ACTIVE |
| 4 | SHIPPING_ADDRESSES 4 | Description for SHIPPING_ADDRESSES 4 | null | Sample WISHLIST_190_ATTR_1 4 | null | null | Sample CART_190_ATTR_4 4 | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... | Sample RATING_190_ATTR_6 4 | Tue Jan 13 2026 18:00:00 GMT-0600 (Central Stan... | ACTIVE |
| 5 | SHIPPING_ADDRESSES 5 | Description for SHIPPING_ADDRESSES 5 | 104 | Sample WISHLIST_190_ATTR_1 5 | 104 | 104 | Sample CART_190_ATTR_4 5 | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... | Sample RATING_190_ATTR_6 5 | Wed Jan 14 2026 18:00:00 GMT-0600 (Central Stan... | ACTIVE |

*Generated at: 2025-12-14T23:39:49.806Z*
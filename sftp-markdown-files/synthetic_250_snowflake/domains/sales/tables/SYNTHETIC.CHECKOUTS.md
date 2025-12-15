# CHECKOUTS

**Database:** synthetic_250_snowflake
**Schema:** SYNTHETIC
**Description:** The SYNTHETIC.CHECKOUTS table appears to represent transactions or processed orders within a system, identified uniquely by the CHECKOUT_ID primary key. The table includes a variety of attributes potentially associated with shipping, carts, and wishlists, as indicated by column names like SHIPPING_189_ATTR_1 and CART_189_ATTR_2; these likely store metadata or status details regarding each checkout process. As there are no foreign keys or references to or from other tables, this table likely serves as an isolated record of checkout events, capturing key aspects of each transaction's creation and versioning.

**Row Count:** 10

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| CHECKOUT_ID | NUMBER | NO | This column uniquely identifies each individual checkout transaction within the system. It assigns a sequential number to ensure that each transaction can be distinctly referenced. |
| NAME | TEXT | NO | This column represents a sequence or identifier for checkout records, indicating individual checkout instances such as "CHECKOUTS 1" and "CHECKOUTS 2". The purpose beyond labeling sequence is unclear from the available data. |
| DESCRIPTION | TEXT | YES | This column contains a text description of specific checkout transactions, each uniquely identified and sequentially labeled. Purpose unclear from available data. |
| SHIPPING_189_ATTR_0 | NUMBER | YES | This column likely represents a categorical identifier for specific shipping attributes or methods associated with customer checkouts. Purpose unclear from available data. |
| SHIPPING_189_ATTR_1 | NUMBER | NO | This column appears to represent a code or identifier associated with shipping attributes for checkouts. Purpose unclear from available data. |
| CART_189_ATTR_2 | NUMBER | NO | This column likely represents a sequence or identifier related to checkout cart attributes. Purpose unclear from available data. |
| CART_189_ATTR_3 | NUMBER | YES | Purpose unclear from available data. |
| CART_189_ATTR_4 | BOOLEAN | NO | This column likely indicates whether a specific condition or feature associated with a shopping cart is fulfilled or active. Purpose unclear from available data beyond indicating a binary status. |
| WISHLIST_189_ATTR_5 | NUMBER | NO | Purpose unclear from available data. |
| WISHLIST_189_ATTR_6 | NUMBER | NO | Purpose unclear from available data. The column contains sequential numeric values. |
| CREATED_AT | TIMESTAMP_NTZ | NO | This column records the exact date and time when a checkout transaction was created. It captures the information in a standardized timestamp format without timezone information. |
| VERSION | NUMBER | NO | The column represents a sequential identifier used to track changes or updates associated with each row in the checkouts table, ensuring data consistency and integrity. Each increment in the value suggests a new version of the data related to the checkout transaction. |

## Primary Key

`CHECKOUT_ID`

## Sample Data

| CHECKOUT_ID | NAME | DESCRIPTION | SHIPPING_189_ATTR_0 | SHIPPING_189_ATTR_1 | CART_189_ATTR_2 | CART_189_ATTR_3 | CART_189_ATTR_4 | WISHLIST_189_ATTR_5 | WISHLIST_189_ATTR_6 | CREATED_AT | VERSION |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | CHECKOUTS 1 | Description for CHECKOUTS 1 | null | 100 | 100 | null | true | 100 | 100 | Fri Dec 12 2025 11:25:57 GMT-0600 (Central Stan... | 100 |
| 2 | CHECKOUTS 2 | Description for CHECKOUTS 2 | 101 | 101 | 101 | 101 | false | 101 | 101 | Fri Dec 12 2025 11:25:57 GMT-0600 (Central Stan... | 101 |
| 3 | CHECKOUTS 3 | Description for CHECKOUTS 3 | 102 | 102 | 102 | 102 | true | 102 | 102 | Fri Dec 12 2025 11:25:57 GMT-0600 (Central Stan... | 102 |
| 4 | CHECKOUTS 4 | Description for CHECKOUTS 4 | null | 103 | 103 | null | false | 103 | 103 | Fri Dec 12 2025 11:25:57 GMT-0600 (Central Stan... | 103 |
| 5 | CHECKOUTS 5 | Description for CHECKOUTS 5 | 104 | 104 | 104 | 104 | true | 104 | 104 | Fri Dec 12 2025 11:25:57 GMT-0600 (Central Stan... | 104 |

*Generated at: 2025-12-14T23:44:04.339Z*
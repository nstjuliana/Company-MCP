# SUPPLIERS_205

**Database:** synthetic_250_snowflake
**Schema:** SYNTHETIC
**Description:** The SYNTHETIC.SUPPLIERS_205 table represents supplier entities within a synthetic database designed to simulate a business environment. It captures essential attributes of suppliers, including their unique identifier (SUPPLIER_ID), name, description, and several customizable attributes related to e-commerce activities such as shipping, rating, and checkout. With no explicit relationships to other tables, this table likely serves as an isolated dataset, detailing supplier information for analytical or simulation purposes.

**Row Count:** 10

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| SUPPLIER_ID | NUMBER | NO | This column uniquely identifies each supplier within the system. It ensures that each supplier can be distinctly referenced. |
| NAME | TEXT | NO | This column seems to store identifiers or labels for suppliers, possibly in a sequential format. Purpose unclear from available data. |
| DESCRIPTION | TEXT | NO | This column contains generic descriptions for supplier entries in the SUPPLIERS_205 table. Purpose unclear from available data. |
| CART_225_ATTR_0 | NUMBER | YES | Purpose unclear from available data. |
| SHIPPING_225_ATTR_1 | BOOLEAN | YES | Purpose unclear from available data. |
| RATING_225_ATTR_2 | TEXT | YES | This column likely represents a qualitative assessment or feedback rating associated with suppliers, expressed using a series of predefined categorical text labels. Purpose unclear from available data. |
| CHECKOUT_225_ATTR_3 | TEXT | YES | Purpose unclear from available data. |
| WISHLIST_225_ATTR_4 | NUMBER | YES | This column likely represents a distinct classification or categorization code for suppliers, as indicated by numerical values that suggest different categories or identifiers. Purpose unclear from available data. |
| CART_225_ATTR_5 | NUMBER | YES | This column likely represents a categorical or identifier attribute related to suppliers, with values that may correspond to specific categories or codes assigned to them. Purpose unclear from available data. |
| CREATED_AT | TIMESTAMP_NTZ | NO | This column records the exact date and time when a supplier entry was created. It defaults to the current time at the moment of entry creation and is not intended to be left empty. |
| UPDATED_AT | TIMESTAMP_NTZ | YES | This column records the date and time when a supplier's information was last updated. The timestamps indicate updates typically occur daily around 6:00 PM Central Standard Time. |

## Primary Key

`SUPPLIER_ID`

## Sample Data

| SUPPLIER_ID | NAME | DESCRIPTION | CART_225_ATTR_0 | SHIPPING_225_ATTR_1 | RATING_225_ATTR_2 | CHECKOUT_225_ATTR_3 | WISHLIST_225_ATTR_4 | CART_225_ATTR_5 | CREATED_AT | UPDATED_AT |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SUPPLIERS_205 1 | Description for SUPPLIERS_205 1 | null | true | Sample RATING_225_ATTR_2 1 | Sample CHECKOUT_225_ATTR_3 1 | null | null | Fri Dec 12 2025 11:27:33 GMT-0600 (Central Stan... | Sat Jan 10 2026 18:00:00 GMT-0600 (Central Stan... |
| 2 | SUPPLIERS_205 2 | Description for SUPPLIERS_205 2 | 101 | false | Sample RATING_225_ATTR_2 2 | Sample CHECKOUT_225_ATTR_3 2 | 101 | 101 | Fri Dec 12 2025 11:27:33 GMT-0600 (Central Stan... | Sun Jan 11 2026 18:00:00 GMT-0600 (Central Stan... |
| 3 | SUPPLIERS_205 3 | Description for SUPPLIERS_205 3 | 102 | true | Sample RATING_225_ATTR_2 3 | Sample CHECKOUT_225_ATTR_3 3 | 102 | 102 | Fri Dec 12 2025 11:27:33 GMT-0600 (Central Stan... | Mon Jan 12 2026 18:00:00 GMT-0600 (Central Stan... |
| 4 | SUPPLIERS_205 4 | Description for SUPPLIERS_205 4 | null | false | Sample RATING_225_ATTR_2 4 | Sample CHECKOUT_225_ATTR_3 4 | null | null | Fri Dec 12 2025 11:27:33 GMT-0600 (Central Stan... | Tue Jan 13 2026 18:00:00 GMT-0600 (Central Stan... |
| 5 | SUPPLIERS_205 5 | Description for SUPPLIERS_205 5 | 104 | true | Sample RATING_225_ATTR_2 5 | Sample CHECKOUT_225_ATTR_3 5 | 104 | 104 | Fri Dec 12 2025 11:27:33 GMT-0600 (Central Stan... | Wed Jan 14 2026 18:00:00 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:43:56.087Z*
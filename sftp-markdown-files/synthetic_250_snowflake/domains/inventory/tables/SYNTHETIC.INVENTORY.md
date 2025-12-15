# INVENTORY

**Database:** synthetic_250_snowflake
**Schema:** SYNTHETIC
**Description:** The SYNTHETIC.INVENTORY table represents a collection of inventory items, each uniquely identified by the INVENTOR_ID, with details such as name, description, and relevant attributes (e.g., REVIEW_195_ATTR_0, CART_195_ATTR_1) that describe various review, cart, checkout, and shipping characteristics. The table is self-contained with no defined relationships to other tables, suggesting a focus on standalone record-keeping or integration with external systems via other means. Its primary role in the data model seems to be storing basic inventory metadata and tracking time-stamped actions through CREATED_AT and UPDATED_AT columns.

**Row Count:** 10

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| INVENTOR_ID | NUMBER | NO | This column represents a unique identifier for individuals in the inventory system. Purpose unclear from available data. |
| NAME | TEXT | NO | This column represents unique identifiers for each inventory item, likely labeling them in a sequential manner. The purpose of these labels is unclear from the available data. |
| DESCRIPTION | TEXT | YES | This column holds textual descriptions of inventory items, enumerated in sequence. Each description uniquely identifies an inventory item by specifying its corresponding inventory number. |
| REVIEW_195_ATTR_0 | NUMBER | NO | This column likely represents an identifier or sequence number for inventory reviews, as indicated by the sequential numeric sample values. Its purpose beyond this sequencing is unclear from the available data. |
| CART_195_ATTR_1 | TIMESTAMP_NTZ | YES | This column represents a repeated, sequential timestamp likely indicating daily occurrences related to inventory activities. Specific business purpose is unclear from available data. |
| CART_195_ATTR_2 | BOOLEAN | NO | This column likely indicates a binary attribute related to the inventory, where each entry represents a true or false state. The exact purpose of this attribute is unclear from the available data. |
| REVIEW_195_ATTR_3 | NUMBER | YES | Purpose unclear from available data. The column appears to contain numerical identifiers or codes. |
| CHECKOUT_195_ATTR_4 | NUMBER | NO | This column records sequential identification numbers assigned during the checkout process for inventory items. The purpose of these specific IDs within the broader inventory management context is unclear from the available data. |
| SHIPPING_195_ATTR_5 | NUMBER | YES | This column likely represents a categorical identifier related to a specific attribute of shipping, possibly indicating a type or status. Purpose unclear from available data. |
| CREATED_AT | TIMESTAMP_NTZ | NO | This column records the exact date and time when an inventory record was created, capturing the moment in Central Standard Time. It is automatically populated with the current timestamp when a new entry is added to the table, ensuring accurate tracking of inventory data creation. |
| UPDATED_AT | TIMESTAMP_NTZ | YES | This column represents the date and time when an inventory record was last modified. The timestamps indicate updates occurred daily around 6:00 PM Central Standard Time. |

## Primary Key

`INVENTOR_ID`

## Sample Data

| INVENTOR_ID | NAME | DESCRIPTION | REVIEW_195_ATTR_0 | CART_195_ATTR_1 | CART_195_ATTR_2 | REVIEW_195_ATTR_3 | CHECKOUT_195_ATTR_4 | SHIPPING_195_ATTR_5 | CREATED_AT | UPDATED_AT |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | INVENTORY 1 | Description for INVENTORY 1 | 100 | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | true | null | 100 | null | Fri Dec 12 2025 11:26:32 GMT-0600 (Central Stan... | Sat Jan 10 2026 18:00:00 GMT-0600 (Central Stan... |
| 2 | INVENTORY 2 | Description for INVENTORY 2 | 101 | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... | false | 101 | 101 | 101 | Fri Dec 12 2025 11:26:32 GMT-0600 (Central Stan... | Sun Jan 11 2026 18:00:00 GMT-0600 (Central Stan... |
| 3 | INVENTORY 3 | Description for INVENTORY 3 | 102 | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... | true | 102 | 102 | 102 | Fri Dec 12 2025 11:26:32 GMT-0600 (Central Stan... | Mon Jan 12 2026 18:00:00 GMT-0600 (Central Stan... |
| 4 | INVENTORY 4 | Description for INVENTORY 4 | 103 | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... | false | null | 103 | null | Fri Dec 12 2025 11:26:32 GMT-0600 (Central Stan... | Tue Jan 13 2026 18:00:00 GMT-0600 (Central Stan... |
| 5 | INVENTORY 5 | Description for INVENTORY 5 | 104 | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... | true | 104 | 104 | 104 | Fri Dec 12 2025 11:26:32 GMT-0600 (Central Stan... | Wed Jan 14 2026 18:00:00 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:43:57.512Z*
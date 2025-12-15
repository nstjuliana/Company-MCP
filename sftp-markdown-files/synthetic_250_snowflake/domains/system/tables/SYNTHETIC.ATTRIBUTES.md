# ATTRIBUTES

**Database:** synthetic_250_snowflake
**Schema:** SYNTHETIC
**Description:** The `SYNTHETIC.ATTRIBUTES` table represents a collection of attribute information with specific details such as names, descriptions, and various distinct attribute types like `WISHLIST` and `CHECKOUT`, each noted by unique suffixes. This table appears to store configurable or descriptive properties potentially relevant to products or categories in a system, but with no explicit foreign key relationships, it seems to serve as an isolated entity for referencing attributes. The primary key `ATTRIBUTE_ID` uniquely identifies each attribute entry, and timestamps in `CREATED_AT` suggest tracking the record creation date.

**Row Count:** 10

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| ATTRIBUTE_ID | NUMBER | NO | This column represents a unique identifier for distinct attributes within the dataset. Purpose unclear from available data. |
| NAME | TEXT | NO | This column appears to represent a sequence or index identifying individual attributes or features within the dataset. Each value likely serves as a unique identifier or label for a specific element within the attributes table. |
| DESCRIPTION | TEXT | YES | This column contains textual descriptions providing additional context or information about specific attributes within the table. Each entry corresponds to a unique attribute and offers a brief explanation or identifier. |
| WISHLIST_201_ATTR_0 | BOOLEAN | NO | This column indicates whether a certain attribute is part of a user's wishlist, likely used to mark or track preferences. Without additional context, the specific attribute it refers to remains unclear from the available data. |
| CHECKOUT_201_ATTR_1 | NUMBER | YES | This column likely represents a numerical attribute related to a checkout process, with most values in the low 100s. The purpose is unclear from the available data. |
| WISHLIST_201_ATTR_2 | TEXT | YES | Purpose unclear from available data. The sample values do not provide sufficient context for a meaningful business description. |
| RATING_201_ATTR_3 | NUMBER | YES | This column appears to represent a categorical rating scale with values starting from 101, potentially indicating different levels or categories of an attribute. The specific nature or criteria of these ratings is unclear from the available data. |
| CHECKOUT_201_ATTR_4 | BOOLEAN | YES | This column likely indicates the presence or absence of a specific attribute related to a checkout process. Based on the sample values, it denotes a binary decision or state, such as whether a condition is satisfied or an option is enabled. |
| CREATED_AT | TIMESTAMP_NTZ | NO | This column records the date and time when an attribute entry was created, using the current timestamp setting. It ensures precise tracking of when each record was initially added to the database. |

## Primary Key

`ATTRIBUTE_ID`

## Sample Data

| ATTRIBUTE_ID | NAME | DESCRIPTION | WISHLIST_201_ATTR_0 | CHECKOUT_201_ATTR_1 | WISHLIST_201_ATTR_2 | RATING_201_ATTR_3 | CHECKOUT_201_ATTR_4 | CREATED_AT |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ATTRIBUTES 1 | Description for ATTRIBUTES 1 | true | null | Sample WISHLIST_201_ATTR_2 1 | null | true | Fri Dec 12 2025 11:25:31 GMT-0600 (Central Stan... |
| 2 | ATTRIBUTES 2 | Description for ATTRIBUTES 2 | false | 101 | Sample WISHLIST_201_ATTR_2 2 | 101 | false | Fri Dec 12 2025 11:25:31 GMT-0600 (Central Stan... |
| 3 | ATTRIBUTES 3 | Description for ATTRIBUTES 3 | true | 102 | Sample WISHLIST_201_ATTR_2 3 | 102 | true | Fri Dec 12 2025 11:25:31 GMT-0600 (Central Stan... |
| 4 | ATTRIBUTES 4 | Description for ATTRIBUTES 4 | false | null | Sample WISHLIST_201_ATTR_2 4 | null | false | Fri Dec 12 2025 11:25:31 GMT-0600 (Central Stan... |
| 5 | ATTRIBUTES 5 | Description for ATTRIBUTES 5 | true | 104 | Sample WISHLIST_201_ATTR_2 5 | 104 | true | Fri Dec 12 2025 11:25:31 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:39:39.901Z*
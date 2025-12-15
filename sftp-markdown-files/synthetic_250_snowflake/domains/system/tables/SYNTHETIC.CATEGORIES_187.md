# CATEGORIES_187

**Database:** synthetic_250_snowflake
**Schema:** SYNTHETIC
**Description:** The SYNTHETIC.CATEGORIES_187 table represents a category entity, identified by the primary key CATEGORIE_ID, which includes descriptive information such as name and description. It appears to capture metadata about categories, including attributes like ratings and shipping dates, which may be pertinent for analytical or descriptive purposes. The table operates independently within the database as there are no relational constraints with other tables, indicating its use as a standalone reference or classification entity.

**Row Count:** 10

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| CATEGORIE_ID | NUMBER | NO | This column represents unique identifiers assigned to different categories within the system, ensuring each category can be distinctly referenced. The numbers appear to sequentially identify each category item. |
| NAME | TEXT | YES | This column likely categorizes entries numerically, as suggested by sequential labeling in sample values. Its specific business purpose is unclear from the available data. |
| DESCRIPTION | TEXT | NO | This column contains descriptive text entries detailing different categories within the synthetic dataset. Each entry uniquely identifies and provides information about a category in the CATEGORIES_187 table. |
| REVIEW_207_ATTR_0 | TIMESTAMP_NTZ | YES | This column likely records the date and time when a particular event or review related to categories occurs. The exact purpose of these timestamps is unclear from the available data. |
| RATING_207_ATTR_1 | TEXT | YES | This column appears to represent a rating attribute for categories, utilizing a text format to list rating values from 1 to 10. Purpose unclear from available data. |
| RATING_207_ATTR_2 | NUMBER | NO | This column likely represents a categorical or sequential series of ratings or identifiers within a certain category context, incrementing in value. Purpose unclear from available data. |
| SHIPPING_207_ATTR_3 | DATE | NO | This column likely represents scheduled shipping dates, indicating when items are expected to be shipped. The dates are consecutive, suggesting a daily schedule in a standard time zone. |
| CREATED_AT | TIMESTAMP_NTZ | NO | This column records the exact date and time when a category entry was created. It reflects the moment of entry creation in the Central Standard Time zone. |

## Primary Key

`CATEGORIE_ID`

## Sample Data

| CATEGORIE_ID | NAME | DESCRIPTION | REVIEW_207_ATTR_0 | RATING_207_ATTR_1 | RATING_207_ATTR_2 | SHIPPING_207_ATTR_3 | CREATED_AT |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | CATEGORIES_187 1 | Description for CATEGORIES_187 1 | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | Sample RATING_207_ATTR_1 1 | 100 | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | Fri Dec 12 2025 11:25:53 GMT-0600 (Central Stan... |
| 2 | CATEGORIES_187 2 | Description for CATEGORIES_187 2 | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... | Sample RATING_207_ATTR_1 2 | 101 | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... | Fri Dec 12 2025 11:25:53 GMT-0600 (Central Stan... |
| 3 | CATEGORIES_187 3 | Description for CATEGORIES_187 3 | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... | Sample RATING_207_ATTR_1 3 | 102 | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... | Fri Dec 12 2025 11:25:53 GMT-0600 (Central Stan... |
| 4 | CATEGORIES_187 4 | Description for CATEGORIES_187 4 | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... | Sample RATING_207_ATTR_1 4 | 103 | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... | Fri Dec 12 2025 11:25:53 GMT-0600 (Central Stan... |
| 5 | CATEGORIES_187 5 | Description for CATEGORIES_187 5 | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... | Sample RATING_207_ATTR_1 5 | 104 | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... | Fri Dec 12 2025 11:25:53 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:39:38.243Z*
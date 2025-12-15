# RATINGS

**Database:** synthetic_250_snowflake
**Schema:** SYNTHETIC
**Description:** The SYNTHETIC.RATINGS table captures rating-related data, uniquely identified by RATING_ID, and is a standalone entity with no defined relationships to other tables. The table seems to track information about specific ratings, including descriptive elements and attributes related to shipping and checkout processes, as evidenced by columns like NAME, DESCRIPTION, and various attributes prefixed with "CHECKOUT" and "SHIPPING." It plays a role in organizing and storing details regarding ratings, likely in the context of products or services, evidenced by DATE-related and BOOLEAN columns indicating status and timestamps.

**Row Count:** 10

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| RATING_ID | NUMBER | NO | This column represents a unique identifier for each rating entry in the ratings table. Each number corresponds to a distinct rating record. |
| NAME | TEXT | NO | This column represents a categorization or enumeration of different rating identifiers, expressed sequentially from 1 to 10. Each value suggests an identifier that may correspond to an entry or group within a broader rating system. |
| DESCRIPTION | TEXT | YES | This column provides textual explanations or details related to individual ratings, most likely intended to offer context or additional information about each rating entry. The specific purpose or nature of these descriptions is unclear from the available data. |
| CHECKOUT_192_ATTR_0 | BOOLEAN | YES | This column represents a binary indicator related to a checkout attribute, possibly recording a condition or action's presence or absence during the checkout process. Purpose unclear from available data. |
| SHIPPING_192_ATTR_1 | TIMESTAMP_NTZ | YES | Purpose unclear from available data. The column appears to store timestamps within the Central Standard Time zone, possibly indicating dates and times related to an unspecified event. |
| SHIPPING_192_ATTR_2 | BOOLEAN | YES | This column indicates whether a particular attribute of shipping is met or not for a given rating, with possible outcomes being true or false. Purpose unclear from available data. |
| RATING_192_ATTR_3 | BOOLEAN | YES | This column indicates a binary condition related to an attribute of ratings, marking it as either true or false. Purpose unclear from available data. |
| RATING_192_ATTR_4 | TEXT | YES | The column likely represents a categorization or evaluation metric numbered sequentially, as indicated by the sample values. Purpose unclear from available data. |
| SHIPPING_192_ATTR_5 | DATE | NO | This column likely represents scheduled shipping dates for deliveries, as evidenced by the sequential daily values. The non-nullable status indicates that every record must have an assigned shipping date. |
| CREATED_AT | TIMESTAMP_NTZ | NO | This column records the exact date and time when a new entry is added to the ratings table. It ensures that each rating is timestamped at the moment of its creation, using the local Central Standard Time zone. |

## Primary Key

`RATING_ID`

## Sample Data

| RATING_ID | NAME | DESCRIPTION | CHECKOUT_192_ATTR_0 | SHIPPING_192_ATTR_1 | SHIPPING_192_ATTR_2 | RATING_192_ATTR_3 | RATING_192_ATTR_4 | SHIPPING_192_ATTR_5 | CREATED_AT |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | RATINGS 1 | Description for RATINGS 1 | true | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | true | true | Sample RATING_192_ATTR_4 1 | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | Fri Dec 12 2025 11:27:05 GMT-0600 (Central Stan... |
| 2 | RATINGS 2 | Description for RATINGS 2 | false | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... | false | false | Sample RATING_192_ATTR_4 2 | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... | Fri Dec 12 2025 11:27:05 GMT-0600 (Central Stan... |
| 3 | RATINGS 3 | Description for RATINGS 3 | true | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... | true | true | Sample RATING_192_ATTR_4 3 | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... | Fri Dec 12 2025 11:27:05 GMT-0600 (Central Stan... |
| 4 | RATINGS 4 | Description for RATINGS 4 | false | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... | false | false | Sample RATING_192_ATTR_4 4 | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... | Fri Dec 12 2025 11:27:05 GMT-0600 (Central Stan... |
| 5 | RATINGS 5 | Description for RATINGS 5 | true | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... | true | true | Sample RATING_192_ATTR_4 5 | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... | Fri Dec 12 2025 11:27:05 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:42:57.787Z*
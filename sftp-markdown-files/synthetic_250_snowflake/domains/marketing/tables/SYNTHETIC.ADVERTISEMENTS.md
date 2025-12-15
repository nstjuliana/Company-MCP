# ADVERTISEMENTS

**Database:** synthetic_250_snowflake
**Schema:** SYNTHETIC
**Description:** The SYNTHETIC.ADVERTISEMENTS table represents a business entity modeling advertisement details, uniquely identified by the ADVERTISEMENT_ID primary key. It includes attributes such as names, descriptions, and metadata like email and event dates, but it lacks defined relationships with other tables. This table serves as an isolated component in the data model, focusing on storing and detailing advertisement-specific information.

**Row Count:** 10

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| ADVERTISEMENT_ID | NUMBER | NO | This column represents a unique identifier assigned to each advertisement record in the database, ensuring each advertisement can be individually referenced and managed. Purpose unclear from available data. |
| NAME | TEXT | NO | This column likely represents unique identifiers for different advertisements, designated with a sequential numbering system. Purpose unclear from available data beyond enumeration of advertisements. |
| DESCRIPTION | TEXT | YES | This column contains brief textual descriptions associated with individual advertisement records. Each description provides a unique identifier for advertisements, as demonstrated by the sample values. |
| AD_132_ATTR_0 | NUMBER | YES | This column likely represents a numeric identifier or code associated with different types of advertisements. Purpose unclear from available data. |
| EMAIL_132_ATTR_1 | TEXT | NO | This column stores email addresses associated with advertisements. These emails likely belong to users involved in the advertisement process, possibly as contacts or recipients. |
| EVENT_132_ATTR_2 | DATE | NO | This column represents specific dates associated with events in the advertisement data. Each date indicates a point in time relevant to the occurrence or scheduling of an advertisement event. |
| EMAIL_132_ATTR_3 | NUMBER | NO | This column likely represents a sequential identifier or code associated with email-related attributes or events in the advertisements context. Purpose unclear from available data. |
| EVENT_132_ATTR_4 | BOOLEAN | YES | Indicates whether a specific condition or event related to advertisements has occurred. Purpose unclear from available data. |
| CAMPAIGN_132_ATTR_5 | NUMBER | YES | This column likely represents an attribute or identifier associated with a specific campaign within the advertisement database, as indicated by the sequential sample numeric values. Purpose unclear from available data. |
| CREATED_AT | TIMESTAMP_NTZ | NO | This column records the exact date and time when an advertisement entry is created in the system. It captures the creation timestamp automatically, ensuring the record reflects its initiation moment. |

## Primary Key

`ADVERTISEMENT_ID`

## Sample Data

| ADVERTISEMENT_ID | NAME | DESCRIPTION | AD_132_ATTR_0 | EMAIL_132_ATTR_1 | EVENT_132_ATTR_2 | EMAIL_132_ATTR_3 | EVENT_132_ATTR_4 | CAMPAIGN_132_ATTR_5 | CREATED_AT |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ADVERTISEMENTS 1 | Description for ADVERTISEMENTS 1 | null | user1@example.com | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | 100 | true | null | Fri Dec 12 2025 11:25:17 GMT-0600 (Central Stan... |
| 2 | ADVERTISEMENTS 2 | Description for ADVERTISEMENTS 2 | 101 | user2@example.com | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... | 101 | false | 101 | Fri Dec 12 2025 11:25:17 GMT-0600 (Central Stan... |
| 3 | ADVERTISEMENTS 3 | Description for ADVERTISEMENTS 3 | 102 | user3@example.com | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... | 102 | true | 102 | Fri Dec 12 2025 11:25:17 GMT-0600 (Central Stan... |
| 4 | ADVERTISEMENTS 4 | Description for ADVERTISEMENTS 4 | null | user4@example.com | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... | 103 | false | null | Fri Dec 12 2025 11:25:17 GMT-0600 (Central Stan... |
| 5 | ADVERTISEMENTS 5 | Description for ADVERTISEMENTS 5 | 104 | user5@example.com | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... | 104 | true | 104 | Fri Dec 12 2025 11:25:17 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:42:34.681Z*
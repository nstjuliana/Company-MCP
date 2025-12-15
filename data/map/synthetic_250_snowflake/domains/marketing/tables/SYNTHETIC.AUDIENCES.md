# AUDIENCES

**Database:** synthetic_250_snowflake
**Schema:** SYNTHETIC
**Description:** The `SYNTHETIC.AUDIENCES` table represents a collection of audience entities, characterized by unique identifiers (`AUDIENCE_ID`), names, and descriptions. It captures various attributes related to audiences, such as event participation dates and engagement through media like webinars and emails. This table functions independently within the data model without foreign key relationships, indicating it likely serves as a foundational or standalone dataset for audience-related analysis or operations.

**Row Count:** 10

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| AUDIENCE_ID | NUMBER | NO | This column represents unique identifiers assigned to each audience entry within the database, ensuring each audience can be distinctly referenced. |
| NAME | TEXT | NO | This column represents distinct audience segments labeled sequentially. Purpose unclear from available data. |
| DESCRIPTION | TEXT | YES | This column contains narrative details or summaries for different audience segments. Each entry provides a textual description that likely relates to specific characteristics or identifiers of various audiences. |
| AD_142_ATTR_0 | TEXT | YES | Purpose unclear from available data. |
| WEBINAR_142_ATTR_1 | BOOLEAN | YES | This column likely indicates a binary status or participation related to webinar or event number 142 for each audience member. Purpose unclear from available data. |
| EVENT_142_ATTR_2 | DATE | NO | This column represents the specific date associated with a particular event for audiences, consistently occurring at an evening time in the Central Standard Time zone. It seems to track consecutive daily events in December 2025. |
| EMAIL_142_ATTR_3 | BOOLEAN | NO | The column likely indicates a binary status or condition related to an audience, such as whether a particular criterion or attribute is present or fulfilled. Purpose unclear from available data. |

## Primary Key

`AUDIENCE_ID`

## Sample Data

| AUDIENCE_ID | NAME | DESCRIPTION | AD_142_ATTR_0 | WEBINAR_142_ATTR_1 | EVENT_142_ATTR_2 | EMAIL_142_ATTR_3 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | AUDIENCES 1 | Description for AUDIENCES 1 | Sample AD_142_ATTR_0 1 | true | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | true |
| 2 | AUDIENCES 2 | Description for AUDIENCES 2 | Sample AD_142_ATTR_0 2 | false | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... | false |
| 3 | AUDIENCES 3 | Description for AUDIENCES 3 | Sample AD_142_ATTR_0 3 | true | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... | true |
| 4 | AUDIENCES 4 | Description for AUDIENCES 4 | Sample AD_142_ATTR_0 4 | false | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... | false |
| 5 | AUDIENCES 5 | Description for AUDIENCES 5 | Sample AD_142_ATTR_0 5 | true | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... | true |

*Generated at: 2025-12-14T23:42:34.597Z*
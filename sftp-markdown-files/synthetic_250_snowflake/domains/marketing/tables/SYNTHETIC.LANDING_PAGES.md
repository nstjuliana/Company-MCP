# LANDING_PAGES

**Database:** synthetic_250_snowflake
**Schema:** SYNTHETIC
**Description:** The "SYNTHETIC.LANDING_PAGES" table represents a collection of landing pages, each uniquely identified by the "LANDING_PAGE_ID" and described by fields such as "NAME," "DESCRIPTION," and attributes related to webinars, events, and social aspects. It operates independently within the data model, with no foreign key relationships linking it to other tables. The table's role is focused on storing and categorizing key information about different landing pages, including their creation date as indicated by the "CREATED_AT" column.

**Row Count:** 10

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| LANDING_PAGE_ID | NUMBER | NO | This column likely serves as a unique identifier for each landing page in the system. Purpose unclear from available data. |
| NAME | TEXT | NO | This column represents the identification or designation of different landing pages within a system, sequentially numbered for organization or tracking purposes. The purpose of these landing pages is unclear from the available data. |
| DESCRIPTION | TEXT | YES | This column contains textual descriptions of various landing pages, each uniquely identified by a number, indicating specific content or features related to the respective landing page. Purpose unclear from available data. |
| WEBINAR_144_ATTR_0 | BOOLEAN | NO | Purpose unclear from available data. |
| EVENT_144_ATTR_1 | TEXT | YES | Purpose unclear from available data. |
| SOCIAL_144_ATTR_2 | TEXT | YES | Purpose unclear from available data. |
| CREATED_AT | TIMESTAMP_NTZ | NO | This column records the exact date and time when a landing page was created. Purpose unclear from available data. |

## Primary Key

`LANDING_PAGE_ID`

## Sample Data

| LANDING_PAGE_ID | NAME | DESCRIPTION | WEBINAR_144_ATTR_0 | EVENT_144_ATTR_1 | SOCIAL_144_ATTR_2 | CREATED_AT |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | LANDING_PAGES 1 | Description for LANDING_PAGES 1 | true | Sample EVENT_144_ATTR_1 1 | Sample SOCIAL_144_ATTR_2 1 | Fri Dec 12 2025 11:26:38 GMT-0600 (Central Stan... |
| 2 | LANDING_PAGES 2 | Description for LANDING_PAGES 2 | false | Sample EVENT_144_ATTR_1 2 | Sample SOCIAL_144_ATTR_2 2 | Fri Dec 12 2025 11:26:38 GMT-0600 (Central Stan... |
| 3 | LANDING_PAGES 3 | Description for LANDING_PAGES 3 | true | Sample EVENT_144_ATTR_1 3 | Sample SOCIAL_144_ATTR_2 3 | Fri Dec 12 2025 11:26:38 GMT-0600 (Central Stan... |
| 4 | LANDING_PAGES 4 | Description for LANDING_PAGES 4 | false | Sample EVENT_144_ATTR_1 4 | Sample SOCIAL_144_ATTR_2 4 | Fri Dec 12 2025 11:26:38 GMT-0600 (Central Stan... |
| 5 | LANDING_PAGES 5 | Description for LANDING_PAGES 5 | true | Sample EVENT_144_ATTR_1 5 | Sample SOCIAL_144_ATTR_2 5 | Fri Dec 12 2025 11:26:38 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:42:34.277Z*
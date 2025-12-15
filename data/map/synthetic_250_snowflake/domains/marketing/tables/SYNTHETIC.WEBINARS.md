# WEBINARS

**Database:** synthetic_250_snowflake
**Schema:** SYNTHETIC
**Description:** The table SYNTHETIC.WEBINARS represents a collection of webinar records, each uniquely identified by the WEBINAR_ID primary key. Each entry in the table provides details about a specific webinar, including its name and description, along with several attribute fields (such as CAMPAIGN_136_ATTR_0 and WEBINAR_136_ATTR_1) possibly used for categorization or additional configuration. As there are no foreign keys or references from other tables, this table appears to function independently within the database, primarily serving as a repository of webinar information.

**Row Count:** 10

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| WEBINAR_ID | NUMBER | NO | This column uniquely identifies each webinar in the database. The sequential numeric values suggest that it tracks the order in which webinars are recorded. |
| NAME | TEXT | NO | This column represents the naming or labeling of different webinars, indicated by their sequential numbering. It appears to reflect a series or catalog of webinar events. |
| DESCRIPTION | TEXT | YES | This column contains textual summaries or titles for specific webinars, likely indicating their content or topic. Purpose unclear from available data. |
| CAMPAIGN_136_ATTR_0 | BOOLEAN | NO | This column indicates whether a specific attribute related to campaign 136 was present during webinars. It consistently captures a yes or no condition for each instance. |
| WEBINAR_136_ATTR_1 | TEXT | NO | Purpose unclear from available data. |
| CAMPAIGN_136_ATTR_2 | TEXT | YES | Purpose unclear from available data. |
| WEBINAR_136_ATTR_3 | BOOLEAN | YES | This column likely indicates a binary status or preference associated with webinars, such as availability or a specific feature being enabled or disabled. Purpose unclear from available data. |

## Primary Key

`WEBINAR_ID`

## Sample Data

| WEBINAR_ID | NAME | DESCRIPTION | CAMPAIGN_136_ATTR_0 | WEBINAR_136_ATTR_1 | CAMPAIGN_136_ATTR_2 | WEBINAR_136_ATTR_3 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | WEBINARS 1 | Description for WEBINARS 1 | true | Sample WEBINAR_136_ATTR_1 1 | Sample CAMPAIGN_136_ATTR_2 1 | true |
| 2 | WEBINARS 2 | Description for WEBINARS 2 | false | Sample WEBINAR_136_ATTR_1 2 | Sample CAMPAIGN_136_ATTR_2 2 | false |
| 3 | WEBINARS 3 | Description for WEBINARS 3 | true | Sample WEBINAR_136_ATTR_1 3 | Sample CAMPAIGN_136_ATTR_2 3 | true |
| 4 | WEBINARS 4 | Description for WEBINARS 4 | false | Sample WEBINAR_136_ATTR_1 4 | Sample CAMPAIGN_136_ATTR_2 4 | false |
| 5 | WEBINARS 5 | Description for WEBINARS 5 | true | Sample WEBINAR_136_ATTR_1 5 | Sample CAMPAIGN_136_ATTR_2 5 | true |

*Generated at: 2025-12-14T23:42:40.780Z*
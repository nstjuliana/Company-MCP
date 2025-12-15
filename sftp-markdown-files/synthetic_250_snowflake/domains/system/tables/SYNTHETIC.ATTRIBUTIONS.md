# ATTRIBUTIONS

**Database:** synthetic_250_snowflake
**Schema:** SYNTHETIC
**Description:** The SYNTHETIC.ATTRIBUTIONS table represents a business entity for tracking various types of attributions, including attributes related to advertising campaigns, webinars, social interactions, and email engagements, with each record uniquely identified by ATTRIBUTION_ID. This table contains metadata such as creation and update timestamps and current status but does not directly reference or is referenced by other tables, indicating it may serve as an isolated set of descriptors or identifiers within the data model. Through its diverse attributes, the table provides a comprehensive view of different points of attribution related to marketing activities.

**Row Count:** 10

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| ATTRIBUTION_ID | NUMBER | NO | This column likely represents a unique identifier assigned sequentially to each record in the attributions dataset. It ensures that each attribution entry is distinct and can be individually referenced. |
| NAME | TEXT | NO | This column represents a sequential identifier or label for various attributions within the dataset. The purpose of these identifiers is to distinctly categorize each attribution entry. |
| DESCRIPTION | TEXT | YES | This column contains brief textual descriptions or labels for attribution entries, each providing identification or commentary related to a specific attribution instance. Purpose unclear from available data beyond denoting individual attribution details. |
| AD_150_ATTR_0 | NUMBER | YES | This column likely represents unique identifiers assigned to specific attributions or transactions. Purpose unclear from available data. |
| WEBINAR_150_ATTR_1 | NUMBER | YES | This column represents identifiers for specific webinar-related attributions, potentially corresponding to different webinar sessions or categories. Purpose unclear from available data. |
| WEBINAR_150_ATTR_2 | NUMBER | YES | Purpose unclear from available data. |
| SOCIAL_150_ATTR_3 | TEXT | YES | Purpose unclear from available data. |
| EMAIL_150_ATTR_4 | NUMBER | YES | This column represents a numerical code associated with a specific email attribution. Its precise role within business operations is unclear from the available data. |
| CREATED_AT | TIMESTAMP_NTZ | NO | This column stores the exact date and time when each record in the attributions table was created, capturing the creation timestamp for tracking the timeline of data entries. The values are automatically set to the current timestamp when a record is created, ensuring accurate chronological documentation. |
| UPDATED_AT | TIMESTAMP_NTZ | YES | This column records the date and time when an attribution record was last updated. The values indicate time-stamped updates localized to the Central Standard Time zone. |
| STATUS | TEXT | YES | This column likely indicates the current operational state or availability of an item or process within the context of the attribution system. Based on the sample values, the primary state appears to be 'active'. |

## Primary Key

`ATTRIBUTION_ID`

## Sample Data

| ATTRIBUTION_ID | NAME | DESCRIPTION | AD_150_ATTR_0 | WEBINAR_150_ATTR_1 | WEBINAR_150_ATTR_2 | SOCIAL_150_ATTR_3 | EMAIL_150_ATTR_4 | CREATED_AT | UPDATED_AT | STATUS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ATTRIBUTIONS 1 | Description for ATTRIBUTIONS 1 | null | null | null | Sample SOCIAL_150_ATTR_3 1 | null | Fri Dec 12 2025 11:25:33 GMT-0600 (Central Stan... | Sat Jan 10 2026 18:00:00 GMT-0600 (Central Stan... | ACTIVE |
| 2 | ATTRIBUTIONS 2 | Description for ATTRIBUTIONS 2 | 101 | 101 | 101 | Sample SOCIAL_150_ATTR_3 2 | 101 | Fri Dec 12 2025 11:25:33 GMT-0600 (Central Stan... | Sun Jan 11 2026 18:00:00 GMT-0600 (Central Stan... | ACTIVE |
| 3 | ATTRIBUTIONS 3 | Description for ATTRIBUTIONS 3 | 102 | 102 | 102 | Sample SOCIAL_150_ATTR_3 3 | 102 | Fri Dec 12 2025 11:25:33 GMT-0600 (Central Stan... | Mon Jan 12 2026 18:00:00 GMT-0600 (Central Stan... | ACTIVE |
| 4 | ATTRIBUTIONS 4 | Description for ATTRIBUTIONS 4 | null | null | null | Sample SOCIAL_150_ATTR_3 4 | null | Fri Dec 12 2025 11:25:33 GMT-0600 (Central Stan... | Tue Jan 13 2026 18:00:00 GMT-0600 (Central Stan... | ACTIVE |
| 5 | ATTRIBUTIONS 5 | Description for ATTRIBUTIONS 5 | 104 | 104 | 104 | Sample SOCIAL_150_ATTR_3 5 | 104 | Fri Dec 12 2025 11:25:33 GMT-0600 (Central Stan... | Wed Jan 14 2026 18:00:00 GMT-0600 (Central Stan... | ACTIVE |

*Generated at: 2025-12-14T23:39:39.725Z*
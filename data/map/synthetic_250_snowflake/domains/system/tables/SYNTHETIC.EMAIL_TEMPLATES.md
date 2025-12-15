# EMAIL_TEMPLATES

**Database:** synthetic_250_snowflake
**Schema:** SYNTHETIC
**Description:** The "SYNTHETIC.EMAIL_TEMPLATES" table represents a collection of predefined email templates, each uniquely identified by the primary key "EMAIL_TEMPLATE_ID." It captures essential attributes for email campaigns, including template names, descriptions, and specific attributes related to webinars and campaigns, but lacks direct relationships with other tables. The table serves as a standalone resource in the data model for managing and customizing email communications within the system.

**Row Count:** 10

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| EMAIL_TEMPLATE_ID | NUMBER | NO | This column uniquely identifies each email template within the system, serving as a sequential tracker for template organization. Purpose unclear from available data. |
| NAME | TEXT | NO | This column appears to represent a sequential identifier or a name for email templates, possibly indicating a version or distinct template variation within a series. Purpose unclear from available data beyond serving as an identifier for templates. |
| DESCRIPTION | TEXT | YES | This column contains textual descriptions or identifiers for individual email templates used within the system. Each entry provides a unique description associated with a specific email template. |
| WEBINAR_133_ATTR_0 | TEXT | YES | Purpose unclear from available data. |
| WEBINAR_133_ATTR_1 | NUMBER | NO | This column represents a code or identifier associated with specific attributes of a webinar, possibly relating to its configuration or settings. Purpose unclear from available data. |
| CAMPAIGN_133_ATTR_2 | TIMESTAMP_NTZ | NO | This column likely represents scheduled dates and times for sending email campaigns associated with a specific promotion or event. Purpose unclear from available data. |
| EVENT_133_ATTR_3 | NUMBER | YES | The column appears to represent a set of predefined event codes associated with email template actions or triggers. Purpose unclear from available data. |
| EVENT_133_ATTR_4 | NUMBER | YES | Purpose unclear from available data. |
| VERSION | NUMBER | NO | This column represents the sequential versioning of email templates, indicating updates or revisions. Each number implies a new iteration or modification, ensuring email templates are kept current. |

## Primary Key

`EMAIL_TEMPLATE_ID`

## Sample Data

| EMAIL_TEMPLATE_ID | NAME | DESCRIPTION | WEBINAR_133_ATTR_0 | WEBINAR_133_ATTR_1 | CAMPAIGN_133_ATTR_2 | EVENT_133_ATTR_3 | EVENT_133_ATTR_4 | VERSION |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | EMAIL_TEMPLATES 1 | Description for EMAIL_TEMPLATES 1 | Sample WEBINAR_133_ATTR_0 1 | 100 | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | null | null | 100 |
| 2 | EMAIL_TEMPLATES 2 | Description for EMAIL_TEMPLATES 2 | Sample WEBINAR_133_ATTR_0 2 | 101 | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... | 101 | 101 | 101 |
| 3 | EMAIL_TEMPLATES 3 | Description for EMAIL_TEMPLATES 3 | Sample WEBINAR_133_ATTR_0 3 | 102 | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... | 102 | 102 | 102 |
| 4 | EMAIL_TEMPLATES 4 | Description for EMAIL_TEMPLATES 4 | Sample WEBINAR_133_ATTR_0 4 | 103 | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... | null | null | 103 |
| 5 | EMAIL_TEMPLATES 5 | Description for EMAIL_TEMPLATES 5 | Sample WEBINAR_133_ATTR_0 5 | 104 | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... | 104 | 104 | 104 |

*Generated at: 2025-12-14T23:39:43.414Z*
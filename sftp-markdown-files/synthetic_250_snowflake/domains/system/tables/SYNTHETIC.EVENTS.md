# EVENTS

**Database:** synthetic_250_snowflake
**Schema:** SYNTHETIC
**Description:** The SYNTHETIC.EVENTS table represents a collection of event records, uniquely identified by the primary key EVENT_ID, containing metadata such as the event's name, description, and specific attributes related to marketing campaigns, advertisements, social elements, webinars, emails, and other event-specific metrics. With no foreign key relationships, it operates independently within the data model, primarily focusing on storing and tracking information about individual events and their attributes, creation, and update timestamps. The sample row indicates a versatile framework for capturing diverse aspects of events, including various engagement channels and scheduling details.

**Row Count:** 10

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| EVENT_ID | NUMBER | NO | This column represents a unique identifier for each event within the synthetic events dataset, ensuring each entry can be distinctly recognized. The sequential numbering suggests it tracks the order of event entries. |
| NAME | TEXT | NO | This column represents identifiers for a sequence of events, with each entry corresponding to a specific event number. Purpose unclear from available data. |
| DESCRIPTION | TEXT | YES | This column likely contains text descriptions associated with each event, providing additional details or context for the events listed in the table. Purpose unclear from available data. |
| CAMPAIGN_135_ATTR_0 | TEXT | NO | Purpose unclear from available data. |
| AD_135_ATTR_1 | NUMBER | YES | Purpose unclear from available data. |
| SOCIAL_135_ATTR_2 | NUMBER | YES | This column represents a categorical attribute relating to a specific aspect of social events, potentially indicating different types or categories within that context. Purpose unclear from available data. |
| WEBINAR_135_ATTR_3 | BOOLEAN | NO | This column indicates whether a specific condition related to the event has been met. Purpose unclear from available data. |
| EMAIL_135_ATTR_4 | NUMBER | YES | This column appears to represent a numerical attribute associated with an email event, possibly indicating different categories or priorities related to the event. Purpose unclear from available data. |
| EVENT_135_ATTR_5 | NUMBER | NO | This column represents a sequential or categorical attribute of an event, with values ranging from 100 to 109. Purpose unclear from available data. |
| EVENT_135_ATTR_6 | DATE | YES | This column records the date associated with specific events, likely representing scheduled or planned occurrences, given the sequential and consistent nature of the dates. Purpose unclear from available data. |
| CREATED_AT | TIMESTAMP_NTZ | NO | This column records the exact moment when each event entry is created, automatically capturing the current timestamp. It ensures events have a precise creation time for tracking and chronological ordering. |
| UPDATED_AT | TIMESTAMP_NTZ | YES | This column likely represents the date and time when each event entry was last updated. It records timestamps in Central Standard Time, suggesting updates occur in a consistent time zone. |

## Primary Key

`EVENT_ID`

## Sample Data

| EVENT_ID | NAME | DESCRIPTION | CAMPAIGN_135_ATTR_0 | AD_135_ATTR_1 | SOCIAL_135_ATTR_2 | WEBINAR_135_ATTR_3 | EMAIL_135_ATTR_4 | EVENT_135_ATTR_5 | EVENT_135_ATTR_6 | CREATED_AT | UPDATED_AT |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | EVENTS 1 | Description for EVENTS 1 | Sample CAMPAIGN_135_ATTR_0 1 | null | null | true | null | 100 | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | Fri Dec 12 2025 11:26:19 GMT-0600 (Central Stan... | Sat Jan 10 2026 18:00:00 GMT-0600 (Central Stan... |
| 2 | EVENTS 2 | Description for EVENTS 2 | Sample CAMPAIGN_135_ATTR_0 2 | 101 | 101 | false | 101 | 101 | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... | Fri Dec 12 2025 11:26:19 GMT-0600 (Central Stan... | Sun Jan 11 2026 18:00:00 GMT-0600 (Central Stan... |
| 3 | EVENTS 3 | Description for EVENTS 3 | Sample CAMPAIGN_135_ATTR_0 3 | 102 | 102 | true | 102 | 102 | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... | Fri Dec 12 2025 11:26:19 GMT-0600 (Central Stan... | Mon Jan 12 2026 18:00:00 GMT-0600 (Central Stan... |
| 4 | EVENTS 4 | Description for EVENTS 4 | Sample CAMPAIGN_135_ATTR_0 4 | null | null | false | null | 103 | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... | Fri Dec 12 2025 11:26:19 GMT-0600 (Central Stan... | Tue Jan 13 2026 18:00:00 GMT-0600 (Central Stan... |
| 5 | EVENTS 5 | Description for EVENTS 5 | Sample CAMPAIGN_135_ATTR_0 5 | 104 | 104 | true | 104 | 104 | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... | Fri Dec 12 2025 11:26:19 GMT-0600 (Central Stan... | Wed Jan 14 2026 18:00:00 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:39:45.075Z*
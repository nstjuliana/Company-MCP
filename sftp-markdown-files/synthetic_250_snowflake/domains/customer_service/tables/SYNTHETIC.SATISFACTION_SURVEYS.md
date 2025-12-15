# SATISFACTION_SURVEYS

**Database:** synthetic_250_snowflake
**Schema:** SYNTHETIC
**Description:** The "SYNTHETIC.SATISFACTION_SURVEYS" table represents survey data intended to gauge customer satisfaction levels based on various interactions and escalations. Each entry is uniquely identified by the primary key "SATISFACTION_SURVEY_ID" and includes details such as interaction descriptions, escalation dates, and case handling updates. With no foreign key relationships, the table appears to function independently within the database, serving as a repository for distinct satisfaction survey outcomes.

**Row Count:** 10

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| SATISFACTION_SURVEY_ID | NUMBER | NO | This column represents unique identifiers for individual entries in a satisfaction survey dataset. Each number corresponds to a different survey response. |
| NAME | TEXT | NO | This column represents a sequential identifier or label for satisfaction surveys. Each value denotes a different instance of a survey without specific details about its content or purpose. |
| DESCRIPTION | TEXT | YES | Purpose unclear from available data. The sample values indicate a sequential labeling pattern rather than descriptive information about satisfaction surveys. |
| KNOWLEDGE_155_ATTR_0 | NUMBER | YES | This column appears to represent categorical data related to a survey metric, potentially serving as a code or identifier for different levels or attributes of knowledge. Purpose unclear from available data. |
| SURVEY_155_ATTR_1 | BOOLEAN | NO | This column records a binary response indicating the presence or absence of a specific attribute in a satisfaction survey. The exact nature of the attribute is unclear from the available data. |
| INTERACTION_155_ATTR_2 | TEXT | YES | Purpose unclear from available data. Sample values are generic and do not provide context for the column's content. |
| ESCALATION_155_ATTR_3 | TIMESTAMP_NTZ | YES | This column records the date and time of specific escalation-related events related to satisfaction surveys. Purpose unclear from available data as the context of these timestamps is not provided. |
| KNOWLEDGE_155_ATTR_4 | DATE | NO | Purpose unclear from available data. |
| ESCALATION_155_ATTR_5 | TEXT | NO | Purpose unclear from available data. |
| CASE_155_ATTR_6 | TIMESTAMP_NTZ | YES | This column likely represents the dates and times when satisfaction surveys were completed or recorded, as indicated by the consistent daily timestamps shown in the sample values. Purpose unclear from available data beyond indicating survey-related timing. |
| UPDATED_AT | TIMESTAMP_NTZ | YES | This column records the date and time when entries in the satisfaction surveys table were last updated. The timestamps are consistently set in the Central Standard Time zone. |

## Primary Key

`SATISFACTION_SURVEY_ID`

## Sample Data

| SATISFACTION_SURVEY_ID | NAME | DESCRIPTION | KNOWLEDGE_155_ATTR_0 | SURVEY_155_ATTR_1 | INTERACTION_155_ATTR_2 | ESCALATION_155_ATTR_3 | KNOWLEDGE_155_ATTR_4 | ESCALATION_155_ATTR_5 | CASE_155_ATTR_6 | UPDATED_AT |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SATISFACTION_SURVEYS 1 | Description for SATISFACTION_SURVEYS 1 | null | true | Sample INTERACTION_155_ATTR_2 1 | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | Sample ESCALATION_155_ATTR_5 1 | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | Sat Jan 10 2026 18:00:00 GMT-0600 (Central Stan... |
| 2 | SATISFACTION_SURVEYS 2 | Description for SATISFACTION_SURVEYS 2 | 101 | false | Sample INTERACTION_155_ATTR_2 2 | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... | Sample ESCALATION_155_ATTR_5 2 | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... | Sun Jan 11 2026 18:00:00 GMT-0600 (Central Stan... |
| 3 | SATISFACTION_SURVEYS 3 | Description for SATISFACTION_SURVEYS 3 | 102 | true | Sample INTERACTION_155_ATTR_2 3 | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... | Sample ESCALATION_155_ATTR_5 3 | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... | Mon Jan 12 2026 18:00:00 GMT-0600 (Central Stan... |
| 4 | SATISFACTION_SURVEYS 4 | Description for SATISFACTION_SURVEYS 4 | null | false | Sample INTERACTION_155_ATTR_2 4 | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... | Sample ESCALATION_155_ATTR_5 4 | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... | Tue Jan 13 2026 18:00:00 GMT-0600 (Central Stan... |
| 5 | SATISFACTION_SURVEYS 5 | Description for SATISFACTION_SURVEYS 5 | 104 | true | Sample INTERACTION_155_ATTR_2 5 | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... | Sample ESCALATION_155_ATTR_5 5 | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... | Wed Jan 14 2026 18:00:00 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:42:55.019Z*
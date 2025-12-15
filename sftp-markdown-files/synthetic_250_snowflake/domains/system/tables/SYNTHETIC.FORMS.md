# FORMS

**Database:** synthetic_250_snowflake
**Schema:** SYNTHETIC
**Description:** The SYNTHETIC.FORMS table represents a collection of forms within the synthetic_250_snowflake database, where each entry includes identifiers, descriptive information, timestamps, and various attributes that appear to be configurable or relevant to different contexts (e.g., social, advertisement, event). The primary key, FORM_ID, uniquely identifies each form, underpinning its purpose as a singular form entry within this database. Without foreign key relationships, this table operates independently, likely serving as a standalone source of form data without direct connections to other tables.

**Row Count:** 10

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| FORM_ID | NUMBER | NO | This column uniquely identifies each form within the system, serving as a sequential identifier for record-keeping purposes. |
| NAME | TEXT | NO | This column represents distinct identifiers for forms in a sequenced format, suggesting each entry denotes a separate form labeled with a numerical suffix. Purpose unclear from available data. |
| DESCRIPTION | TEXT | YES | This column provides textual descriptions associated with each form in the FORMS table. It contains summaries or explanations pertinent to the individual forms, with the potential to include unique or identifying details specific to each form. |
| SOCIAL_145_ATTR_0 | NUMBER | NO | This column likely represents sequential identifiers or codes associated with specific social entities or activities, but its exact application is purpose unclear from available data. |
| AD_145_ATTR_1 | NUMBER | YES | Purpose unclear from available data. The column stores numeric values with a default of 11, but the sample lacks context for a precise business interpretation. |
| EVENT_145_ATTR_2 | NUMBER | YES | The column appears to represent a categorical identifier or code possibly associated with specific types of events or actions. The context or purpose of these identifiers is unclear from the available data. |
| AD_145_ATTR_3 | TIMESTAMP_NTZ | YES | Purpose unclear from available data. The column contains timestamp values without additional context. |
| AD_145_ATTR_4 | BOOLEAN | YES | Purpose unclear from available data. |
| UPDATED_AT | TIMESTAMP_NTZ | YES | This column records the specific date and time when an entry in the forms table was last updated. The purpose of tracking this timestamp is unclear from the available data. |

## Primary Key

`FORM_ID`

## Sample Data

| FORM_ID | NAME | DESCRIPTION | SOCIAL_145_ATTR_0 | AD_145_ATTR_1 | EVENT_145_ATTR_2 | AD_145_ATTR_3 | AD_145_ATTR_4 | UPDATED_AT |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | FORMS 1 | Description for FORMS 1 | 100 | null | null | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | true | Sat Jan 10 2026 18:00:00 GMT-0600 (Central Stan... |
| 2 | FORMS 2 | Description for FORMS 2 | 101 | 101 | 101 | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... | false | Sun Jan 11 2026 18:00:00 GMT-0600 (Central Stan... |
| 3 | FORMS 3 | Description for FORMS 3 | 102 | 102 | 102 | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... | true | Mon Jan 12 2026 18:00:00 GMT-0600 (Central Stan... |
| 4 | FORMS 4 | Description for FORMS 4 | 103 | null | null | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... | false | Tue Jan 13 2026 18:00:00 GMT-0600 (Central Stan... |
| 5 | FORMS 5 | Description for FORMS 5 | 104 | 104 | 104 | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... | true | Wed Jan 14 2026 18:00:00 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:39:43.952Z*
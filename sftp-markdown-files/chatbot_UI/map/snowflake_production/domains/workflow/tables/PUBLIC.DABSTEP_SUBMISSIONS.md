# DABSTEP_SUBMISSIONS

**Database:** snowflake_production
**Schema:** PUBLIC
**Description:** The DABSTEP_SUBMISSIONS table stores submission records for tasks completed by agents, capturing their answers along with metadata including the assigned agent, model family, and organization details. Each submission is uniquely identified by a SUBMISSION_ID and links to a specific TASK_ID, with tracking information such as submission date, repository URL, and validation status. This table appears to serve as a central logging mechanism for agent-based task completion activities, possibly in an AI or automated system evaluation context.

**Row Count:** 574,507

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| TASK_ID | TEXT | YES | Identifier that references specific tasks or assignments within the system. Based on the sequential numeric values, this appears to track individual task instances that submissions are associated with. |
| AGENT_ANSWER | TEXT | YES | Based on the sample data showing only "Not Applicable" values, this appears to store responses or answers provided by an agent in a submission system, though the specific nature of these responses is unclear from the available data. The consistent "Not Applicable" values suggest this field may be used when agent input is not required or relevant for certain submission types. |
| SUBMISSION_ID | TEXT | YES | Based on the sample values showing repeated "1-1" entries, this appears to be an identifier that tracks individual submissions within the DABSTEP system using a hyphenated format. Purpose unclear from available data due to identical sample values. |
| AGENT_NAME | TEXT | YES | Purpose unclear from available data. All sample values are identical (1), which could represent a default identifier, boolean flag, or placeholder value, but the specific business meaning cannot be determined from this uniform dataset. |
| MODEL_FAMILY | TEXT | YES | Purpose unclear from available data. All sample values show the numeric value "2" which provides insufficient context to determine what model family classification or categorization this represents. |
| ORGANISATION | TEXT | YES | Based on the sample values showing repeated "user j1n9zhe" entries, this appears to store user identifiers or usernames associated with submissions in the DABSTEP system. However, the exact business purpose and relationship to organizational structure is unclear from the available data. |
| REPO_URL | TEXT | YES | Purpose unclear from available data, as all sample values are empty or null. |
| DATE | TEXT | YES | Records the submission date for DABSTEP entries in DD-MM-YYYY format. Based on the sample data, all entries appear to be submitted on the same date in July 2025. |
| VALIDATED | BOOLEAN | YES | Indicates whether a submission has passed validation checks or meets required criteria. Based on the sample data showing only false values, most submissions have not yet been validated or have failed validation. |

## Sample Data

| TASK_ID | AGENT_ANSWER | SUBMISSION_ID | AGENT_NAME | MODEL_FAMILY | ORGANISATION | REPO_URL | DATE | VALIDATED |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Not Applicable | 1-1 | 1 | 2 | 1 | user j1n9zhe |  | 13-07-2025 | false |
| 2 | Not Applicable | 1-1 | 1 | 2 | 1 | user j1n9zhe |  | 13-07-2025 | false |
| 3 | Not Applicable | 1-1 | 1 | 2 | 1 | user j1n9zhe |  | 13-07-2025 | false |
| 4 | Not Applicable | 1-1 | 1 | 2 | 1 | user j1n9zhe |  | 13-07-2025 | false |
| 5 | Not Applicable | 1-1 | 1 | 2 | 1 | user j1n9zhe |  | 13-07-2025 | false |

*Generated at: 2025-12-11T22:51:57.844Z*
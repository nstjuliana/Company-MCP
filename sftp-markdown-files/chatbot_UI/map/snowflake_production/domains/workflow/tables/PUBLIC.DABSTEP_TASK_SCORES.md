# DABSTEP_TASK_SCORES

**Database:** snowflake_production
**Schema:** PUBLIC
**Description:** This table represents task scoring results for what appears to be an AI agent evaluation system, storing performance assessments across different difficulty levels. Each record captures whether an agent successfully completed a specific task (identified by TASK_ID) within a submission (SUBMISSION_ID), along with the difficulty level and the agent's response. The table serves as a fact table for tracking agent performance metrics, with no apparent relationships to other tables in the current schema.

**Row Count:** 577,800

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| SUBMISSION_ID | TEXT | YES | Identifier for task submissions, appearing to use a hyphenated format that may indicate task number and attempt number. Based on the sample data showing repeated "1-1" values, this likely references the first attempt at the first task across multiple records. |
| TASK_ID | TEXT | YES | A unique identifier that distinguishes individual tasks within the scoring system. Based on the sequential numeric values, this appears to reference specific tasks that are being evaluated or assessed. |
| SCORE | BOOLEAN | YES | Indicates whether a task received a passing or successful evaluation, with all observed instances showing unsuccessful outcomes. Purpose unclear from available data due to limited sample diversity. |
| LEVEL | TEXT | YES | Indicates the difficulty level of a task, with "easy" being the observed difficulty rating. Based on the available data, this appears to categorize tasks by their complexity or challenge level. |
| AGENT_ANSWER | TEXT | YES | Stores responses provided by an automated agent or system during task evaluation processes. Based on the sample data, this field currently contains standardized "Not Applicable" values indicating either the agent did not provide answers or the responses were not relevant to the scored tasks. |

## Sample Data

| SUBMISSION_ID | TASK_ID | SCORE | LEVEL | AGENT_ANSWER |
| --- | --- | --- | --- | --- |
| 1-1 | 1 | false | easy | Not Applicable |
| 1-1 | 2 | false | easy | Not Applicable |
| 1-1 | 3 | false | easy | Not Applicable |
| 1-1 | 4 | false | easy | Not Applicable |
| 1-1 | 5 | false | easy | Not Applicable |

*Generated at: 2025-12-11T22:51:55.600Z*
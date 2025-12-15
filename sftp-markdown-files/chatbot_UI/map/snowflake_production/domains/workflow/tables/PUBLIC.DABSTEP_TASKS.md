# DABSTEP_TASKS

**Database:** snowflake_production
**Schema:** PUBLIC
**Description:** This table represents a collection of analytical tasks or questions, likely used for testing or evaluation purposes, with each record containing a unique task identifier, a business question requiring calculation, the corresponding answer, and associated guidelines for completion. The table appears to store tasks of varying difficulty levels that involve financial calculations, as evidenced by the sample question about calculating fees in euros for a specific store and date. Given its standalone nature with no foreign key relationships, this table likely serves as a reference or configuration table for a task management or assessment system within the broader data model.

**Row Count:** 450

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| TASK_ID | TEXT | YES | A unique identifier that distinguishes individual tasks within the system. Based on the sample values, this appears to be a numeric identifier stored as text, ranging from four-digit numbers in the 1000-2000+ range. |
| QUESTION | TEXT | YES | Contains natural language queries requesting specific business analytics and data retrieval operations, typically involving financial metrics, fee calculations, merchant analysis, and transaction data across various time periods. These appear to be user-submitted questions or tasks for a data analysis system to process and answer. |
| ANSWER | TEXT | YES | Purpose unclear from available data. All sample values are empty or null, providing no indication of what type of answer or response this field is intended to store. |
| GUIDELINES | TEXT | YES | Instructions that specify the required format and presentation style for task responses, including requirements for numerical precision, list formatting, and result grouping. |
| LEVEL | TEXT | YES | Indicates the difficulty rating or complexity level assigned to tasks, with "hard" being one of the available difficulty classifications. |

## Sample Data

| TASK_ID | QUESTION | ANSWER | GUIDELINES | LEVEL |
| --- | --- | --- | --- | --- |
| 1712 | For the 12th of the year 2023, what is the tota... |  | Answer must be just a number rounded to 2 decim... | hard |
| 1810 | What were the applicable Fee IDs for Rafa_AI in... |  | Answer must be a list of values in comma separa... | hard |
| 1741 | What are the applicable fee IDs for Belles_cook... |  | Answer must be a list of values in comma separa... | hard |
| 1480 | What is the fee ID or IDs that apply to account... |  | Answer must be a list of values in comma separa... | hard |
| 1234 | What is the average transaction value grouped b... |  | Present your results broken down by grouping an... | hard |

*Generated at: 2025-12-11T22:51:56.476Z*
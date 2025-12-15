# AUTOMATION_RULES

**Database:** synthetic_250_snowflake
**Schema:** SYNTHETIC
**Description:** The SYNTHETIC.AUTOMATION_RULES table represents a set of automation rules with each rule uniquely identified by the primary key AUTOMATION_RULE_ID. The table lacks direct relationships with other tables, indicating standalone use within the data model to manage or define automation processes or conditions, as suggested by the boolean attributes such as EVENT_146_ATTR_2. These attributes, alongside the NAME and DESCRIPTION columns, imply configuration settings or conditions that trigger certain automated actions or events.

**Row Count:** 10

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| AUTOMATION_RULE_ID | NUMBER | NO | This column uniquely identifies each automation rule within the automation rules table, as indicated by its sequence of numerical values. |
| NAME | TEXT | NO | This column represents a sequence of identifiers for different automation rules within the system. Each entry appears to uniquely identify a rule by its order or designation number. |
| DESCRIPTION | TEXT | YES | This column provides textual descriptions for individual automation rules, offering details that help users understand the purpose or functionality of each rule. Purpose beyond providing basic descriptions is unclear from the available data. |
| EMAIL_146_ATTR_0 | NUMBER | YES | Purpose unclear from available data. |
| AD_146_ATTR_1 | NUMBER | YES | Purpose unclear from available data. The column contains numerical values with a common pattern but lacks sufficient context for a definitive business interpretation. |
| EVENT_146_ATTR_2 | BOOLEAN | YES | This column indicates a binary condition related to automation rules, such as whether a specific event attribute condition is met. Purpose unclear from available data. |
| AD_146_ATTR_3 | BOOLEAN | NO | The column indicates whether a specific condition within an automation rule is met or not. It expresses a binary outcome for automation logic, showing either a true or false state. |
| EVENT_146_ATTR_4 | BOOLEAN | YES | Purpose unclear from available data. |

## Primary Key

`AUTOMATION_RULE_ID`

## Sample Data

| AUTOMATION_RULE_ID | NAME | DESCRIPTION | EMAIL_146_ATTR_0 | AD_146_ATTR_1 | EVENT_146_ATTR_2 | AD_146_ATTR_3 | EVENT_146_ATTR_4 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | AUTOMATION_RULES 1 | Description for AUTOMATION_RULES 1 | null | null | true | true | true |
| 2 | AUTOMATION_RULES 2 | Description for AUTOMATION_RULES 2 | 101 | 101 | false | false | false |
| 3 | AUTOMATION_RULES 3 | Description for AUTOMATION_RULES 3 | 102 | 102 | true | true | true |
| 4 | AUTOMATION_RULES 4 | Description for AUTOMATION_RULES 4 | null | null | false | false | false |
| 5 | AUTOMATION_RULES 5 | Description for AUTOMATION_RULES 5 | 104 | 104 | true | true | true |

*Generated at: 2025-12-14T23:45:04.294Z*
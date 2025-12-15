# AGENTS

**Database:** synthetic_250_snowflake
**Schema:** SYNTHETIC
**Description:** The SYNTHETIC.AGENTS table represents a collection of agents, each uniquely identified by a primary key AGENT_ID, with attributes indicating their knowledge, interactions, and ticket handling capabilities. The table is focused on capturing data related to various attributes of these agents, such as their name, description, and specific interaction or ticket handling attributes, without referencing or being referenced by any other tables. It serves as a standalone record of agent information with timestamps marking when each entry was created.

**Row Count:** 10

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| AGENT_ID | NUMBER | NO | This column uniquely identifies each agent within the system with a distinct numerical identifier. Purpose unclear from available data. |
| NAME | TEXT | NO | This column likely represents identifiers or labels for agents in a series or sequence, indicated by the numbered format of the sample values. Purpose unclear from available data. |
| DESCRIPTION | TEXT | YES | This column contains textual descriptions associated with agents, likely indicating their roles or characteristics. The specific nature or purpose of the descriptions remains unclear from the available data. |
| KNOWLEDGE_159_ATTR_0 | BOOLEAN | YES | Purpose unclear from available data. |
| INTERACTION_159_ATTR_1 | TEXT | YES | Purpose unclear from available data. The sample values suggest sequential identifiers or placeholders, but their actual meaning or usage is not evident. |
| TICKET_159_ATTR_2 | BOOLEAN | YES | This column likely indicates a binary status or condition related to a certain attribute within an agent's ticket, where the values are either true or false. Purpose unclear from available data. |
| TICKET_159_ATTR_3 | TEXT | NO | Purpose unclear from available data. |
| KNOWLEDGE_159_ATTR_4 | TEXT | YES | Purpose unclear from available data. The sample values do not provide sufficient context for determining the business relevance of this column. |
| CREATED_AT | TIMESTAMP_NTZ | NO | This column records the exact date and time when an entry for an agent is created in the database. It reflects the Central Standard Time zone and is automatically filled with the current timestamp at the time of creation. |

## Primary Key

`AGENT_ID`

## Sample Data

| AGENT_ID | NAME | DESCRIPTION | KNOWLEDGE_159_ATTR_0 | INTERACTION_159_ATTR_1 | TICKET_159_ATTR_2 | TICKET_159_ATTR_3 | KNOWLEDGE_159_ATTR_4 | CREATED_AT |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | AGENTS 1 | Description for AGENTS 1 | true | Sample INTERACTION_159_ATTR_1 1 | true | Sample TICKET_159_ATTR_3 1 | Sample KNOWLEDGE_159_ATTR_4 1 | Fri Dec 12 2025 11:25:19 GMT-0600 (Central Stan... |
| 2 | AGENTS 2 | Description for AGENTS 2 | false | Sample INTERACTION_159_ATTR_1 2 | false | Sample TICKET_159_ATTR_3 2 | Sample KNOWLEDGE_159_ATTR_4 2 | Fri Dec 12 2025 11:25:19 GMT-0600 (Central Stan... |
| 3 | AGENTS 3 | Description for AGENTS 3 | true | Sample INTERACTION_159_ATTR_1 3 | true | Sample TICKET_159_ATTR_3 3 | Sample KNOWLEDGE_159_ATTR_4 3 | Fri Dec 12 2025 11:25:19 GMT-0600 (Central Stan... |
| 4 | AGENTS 4 | Description for AGENTS 4 | false | Sample INTERACTION_159_ATTR_1 4 | false | Sample TICKET_159_ATTR_3 4 | Sample KNOWLEDGE_159_ATTR_4 4 | Fri Dec 12 2025 11:25:19 GMT-0600 (Central Stan... |
| 5 | AGENTS 5 | Description for AGENTS 5 | true | Sample INTERACTION_159_ATTR_1 5 | true | Sample TICKET_159_ATTR_3 5 | Sample KNOWLEDGE_159_ATTR_4 5 | Fri Dec 12 2025 11:25:19 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:44:26.126Z*
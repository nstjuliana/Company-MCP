# currencies

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.currencies` table represents a collection of currency information, with each row uniquely identified by the `currency_code`. Key columns include `currency_name`, `symbol`, `decimal_places`, and `is_active`, which capture the essential attributes of each currency, such as its name, symbol representation, numerical precision, and active status. The table does not reference or is referenced by other tables, suggesting it serves as a standalone entity within the database model for managing and maintaining currency data attributes.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| currency_code | character varying | NO | This column represents unique codes used to identify different synthetic or hypothetical currencies within a dataset. Each code is an abbreviation assigned to a specific currency for distinguishing it from other currencies in the table. |
| currency_name | character varying | NO | This column represents the names of different currencies, such as Canadian Dollar, Japanese Yen, US Dollar, Euro, and British Pound, used for financial transactions. It ensures that each currency is clearly identified by its standard abbreviation. |
| symbol | character varying | YES | Purpose unclear from available data. Sample values do not provide sufficient context to determine a specific business representation. |
| decimal_places | integer | YES | Purpose unclear from available data. |
| is_active | boolean | YES | This field indicates the current status of a currency, with true representing that the currency is active and false indicating it is not currently active. The absence of additional information prevents further elaboration on its business context. |
| created_at | timestamp without time zone | YES | This column records the date and time when a record in the currencies table was initially created in the database. Purpose unclear from available data. |
| updated_at | timestamp without time zone | YES | This column records the last date and time when information related to currencies was updated, using the current timestamp as the default value. Purpose unclear from available data. |

## Primary Key

`currency_code`

## Indexes

- `currencies_pkey`: CREATE UNIQUE INDEX currencies_pkey ON synthetic.currencies USING btree (currency_code)

## Sample Data

| currency_code | currency_name | symbol | decimal_places | is_active | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| BNB | CAD | Address. | 3085 | false | Sat Dec 13 2025 02:55:01 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:01 GMT-0600 (Central Stan... |
| VSO | CAD | Station. | 5064 | true | Sat Dec 13 2025 02:55:01 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:01 GMT-0600 (Central Stan... |
| CEB | JPY | Put ask. | 622 | true | Sat Dec 13 2025 02:55:01 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:01 GMT-0600 (Central Stan... |
| CUB | USD | Sing. | 3812 | true | Sat Dec 13 2025 02:55:01 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:01 GMT-0600 (Central Stan... |
| DPC | USD | Serve. | 8626 | false | Sat Dec 13 2025 02:55:01 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:01 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:41:19.426Z*
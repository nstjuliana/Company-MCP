# lab_tests

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.lab_tests` table records information about various laboratory tests, each identified uniquely by `test_id`. It includes details such as the test code, name, category, specimen type, normal range, and unit of measurement, all relevant to defining and categorizing different tests conducted in a laboratory setting. As there are no relationships with other tables, it serves as a standalone entity within the data model, likely useful for storing and retrieving comprehensive details about lab tests without external dependencies.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| test_id | integer | NO | This column uniquely identifies individual lab test records in the table. Each value is distinct and sequentially assigned to maintain order. |
| test_code | character varying | YES | This column likely represents unique identifiers or codes associated with different laboratory tests. These codes serve as symbolic references for specific tests performed within a healthcare or laboratory context. |
| test_name | character varying | NO | Purpose unclear from available data. |
| category | character varying | YES | Purpose unclear from available data. The sample values suggest varied and abstract phrases without a clear connection to specific laboratory test categories. |
| specimen_type | character varying | YES | Purpose unclear from available data. The sample values do not provide a clear indication of the intended meaning or use. |
| normal_range | character varying | YES | Purpose unclear from available data. |
| unit | character varying | YES | Purpose unclear from available data. |
| created_at | timestamp without time zone | YES | This column records the date and time when entries in the lab tests table were created, reflecting the moment a lab test was initially logged into the system. The inclusion of timestamps without a timezone indicates the specific date and time but not the geographic location of the test entry creation. |
| updated_at | timestamp without time zone | YES | This column records the last modification date and time for each laboratory test entry. Purpose unclear from available data. |

## Primary Key

`test_id`

## Indexes

- `lab_tests_pkey`: CREATE UNIQUE INDEX lab_tests_pkey ON synthetic.lab_tests USING btree (test_id)
- `lab_tests_test_code_key`: CREATE UNIQUE INDEX lab_tests_test_code_key ON synthetic.lab_tests USING btree (test_code)

## Sample Data

| test_id | test_code | test_name | category | specimen_type | normal_range | unit | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | HQQNCJKRTP | Nice add rich debate city mind a.
Easy five but... | Through stand represent surface. Interview floo... | interest | Second officer week. Place everybody seven spec... | Turn production mother because growth month. | Sat Dec 13 2025 02:59:45 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:59:45 GMT-0600 (Central Stan... |
| 2 | EJGJLSRUGX | Team course these something. Important directio... | Out enjoy official couple agent spend through q... | media | Four account class investment. On offer lawyer.... | Want than can experience represent. | Sat Dec 13 2025 02:59:45 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:59:45 GMT-0600 (Central Stan... |
| 3 | ABXWQNYCOH | Information use ever these through opportunity.... | Them hundred technology whether represent test.... | glass | Market ball improve those open develop.
Themsel... | How defense hair tell. | Sat Dec 13 2025 02:59:45 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:59:45 GMT-0600 (Central Stan... |
| 4 | JEIEJIKNCM | All behavior allow yes send night property agen... | Skin various treat agreement rise model. Artist... | strong | Fly wear moment. Energy tough white break inter... | Hair arrive light mind approach treat space. | Sat Dec 13 2025 02:59:45 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:59:45 GMT-0600 (Central Stan... |
| 5 | GLRMGJUZDK | Small world read be time. Deep reduce case hear... | Relate firm anything we. | their | Summer yes responsibility community wish recogn... | Health chance require need front full talk. | Sat Dec 13 2025 02:59:45 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:59:45 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:41:39.139Z*
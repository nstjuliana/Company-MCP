# one_time_tokens

**Database:** postgres_production
**Schema:** auth
**Description:** I cannot provide an accurate semantic description for this table as the column information is missing or incomplete (showing only commas), no sample data is available, and there are no foreign key relationships documented. Without visibility into the actual column names and their data types, any description would be pure speculation rather than being grounded in the available evidence.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | uuid | NO | Serves as the primary identifier that uniquely distinguishes each one-time authentication token record within the system. Purpose unclear from available data due to lack of sample values. |
| user_id | uuid | NO | Identifies the specific user account that a one-time authentication token belongs to. Links each temporary token to its owner for security and access control purposes. |
| token_type | USER-DEFINED | NO | Categorizes the specific type of temporary authentication token being issued, such as for password reset, email verification, or account activation purposes. Purpose unclear from available data due to lack of sample values. |
| token_hash | text | NO | A cryptographically hashed representation of a one-time authentication token used for secure user verification or password reset processes. This stores the irreversible hash value rather than the plain text token for security purposes. |
| relates_to | text | NO | Purpose unclear from available data. Without sample values or additional context, the specific business meaning of this required text field in the authentication token table cannot be determined. |
| created_at | timestamp without time zone | NO | Records the exact moment when a one-time authentication token was generated in the system. This timestamp enables token expiration validation and audit tracking for security purposes. |
| updated_at | timestamp without time zone | NO | Records when each one-time authentication token was last modified, automatically set to the current timestamp whenever the token record is updated. |

## Primary Key

`id`

## Indexes

- `one_time_tokens_pkey`: CREATE UNIQUE INDEX one_time_tokens_pkey ON auth.one_time_tokens USING btree (id)
- `one_time_tokens_relates_to_hash_idx`: CREATE INDEX one_time_tokens_relates_to_hash_idx ON auth.one_time_tokens USING hash (relates_to)
- `one_time_tokens_token_hash_hash_idx`: CREATE INDEX one_time_tokens_token_hash_hash_idx ON auth.one_time_tokens USING hash (token_hash)
- `one_time_tokens_user_id_token_type_key`: CREATE UNIQUE INDEX one_time_tokens_user_id_token_type_key ON auth.one_time_tokens USING btree (user_id, token_type)

*Generated at: 2025-12-11T22:50:47.056Z*
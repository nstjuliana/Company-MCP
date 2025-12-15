# ssl_certificates

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.ssl_certificates` table represents records of SSL certificates, capturing details such as the domain associated with the certificate, the issuing authority, issuance and expiry dates, and the current status of the certificate. The primary key is `cert_id`, and while there are no foreign key relationships, the table appears to track the lifecycle of SSL certificates, likely for managing web security compliance. The `server_id` suggests a linkage to server entities, although not explicitly connected through this schema, indicating the certificates' assignment to specific servers.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| cert_id | integer | NO | Uniquely identifies each SSL certificate in the system. The purpose is to ensure each certificate is distinct and can be referenced independently. |
| domain | character varying | NO | Purpose unclear from available data. |
| issuer | character varying | YES | Purpose unclear from available data. |
| issued_date | date | YES | This column records the date on which an SSL certificate was issued. The purpose of the issuance data is to track the starting point of an SSL certificate's validity period. |
| expiry_date | date | YES | This data represents the expiration dates of SSL certificates within the system, indicating when each certificate will no longer be valid. The dates are in the future, suggesting upcoming expirations that may require renewal or replacement actions. |
| cert_type | character varying | YES | Purpose unclear from available data. |
| server_id | integer | YES | This column identifies different servers associated with SSL certificates, with each integer representing a unique server. Its purpose remains unclear beyond indicating server identifiers. |
| status | character varying | YES | Indicates the current operational state of an SSL certificate, categorizing it as active, inactive, or pending. Purpose unclear from available data. |
| created_at | timestamp without time zone | YES | This column records the date and time when each SSL certificate record was initially created. Purpose unclear from available data. |
| updated_at | timestamp without time zone | YES | This column tracks the date and time when the information regarding SSL certificates was last updated. Purpose unclear from available data. |

## Primary Key

`cert_id`

## Indexes

- `ssl_certificates_pkey`: CREATE UNIQUE INDEX ssl_certificates_pkey ON synthetic.ssl_certificates USING btree (cert_id)

## Sample Data

| cert_id | domain | issuer | issued_date | expiry_date | cert_type | server_id | status | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Turn appear this pull official. Only training i... | Majority each risk instead lot attack. Hear kit... | Wed Dec 04 2024 00:00:00 GMT-0600 (Central Stan... | Sat Mar 02 2024 00:00:00 GMT-0600 (Central Stan... | Bar player quality might. | 1 | active | Sat Dec 13 2025 03:16:37 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:16:37 GMT-0600 (Central Stan... |
| 2 | Partner door although thought last general last... | Hundred ahead interest range seven lose. | Sat Mar 01 2025 00:00:00 GMT-0600 (Central Stan... | Fri Sep 26 2025 00:00:00 GMT-0500 (Central Dayl... | Morning sing take instead reduce box owner. | 2 | inactive | Sat Dec 13 2025 03:16:37 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:16:37 GMT-0600 (Central Stan... |
| 3 | Those it before myself all stay contain force. | Us operation she certain capital get. They dark... | Wed May 08 2024 00:00:00 GMT-0500 (Central Dayl... | Thu May 01 2025 00:00:00 GMT-0500 (Central Dayl... | Hundred authority career word throw. | 2 | pending | Sat Dec 13 2025 03:16:37 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:16:37 GMT-0600 (Central Stan... |
| 4 | Painting return big. Style know policy. | Medical we animal cup. Test daughter defense re... | Sun Jul 27 2025 00:00:00 GMT-0500 (Central Dayl... | Fri Apr 12 2024 00:00:00 GMT-0500 (Central Dayl... | Actually environment practice southern six. | 1 | pending | Sat Dec 13 2025 03:16:37 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:16:37 GMT-0600 (Central Stan... |
| 5 | Threat participant wall late PM less. Continue ... | Ask then also claim or six. Fear result blue na... | Wed Sep 11 2024 00:00:00 GMT-0500 (Central Dayl... | Sun Apr 28 2024 00:00:00 GMT-0500 (Central Dayl... | Other radio ok that. | 1 | pending | Sat Dec 13 2025 03:16:37 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:16:37 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:39:30.698Z*
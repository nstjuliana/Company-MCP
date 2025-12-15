# secrets

**Database:** postgres_production
**Schema:** vault
**Description:** The vault.secrets table represents a secure storage mechanism for sensitive information within the application, featuring an encrypted secret column designed to safely persist confidential data to disk. As indicated by its placement in the vault schema and the database comment emphasizing encryption, this table serves as a centralized repository for managing sensitive data with security controls. The table currently operates independently without foreign key relationships, suggesting it functions as a standalone secure vault component within the broader data architecture.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | uuid | NO | Serves as the primary identifier for each secret stored in the vault system. Automatically assigned upon creation to uniquely distinguish individual secret records. |
| name | text | YES | Purpose unclear from available data. Likely stores a human-readable identifier or label for secrets within the vault system. |
| description | text | NO | Purpose unclear from available data. Contains text content that provides additional information about vault secrets, with empty string as the default value. |
| secret | text | NO | Purpose unclear from available data. Contains confidential information stored within the vault system, but the specific nature or format cannot be determined without sample values. |
| key_id | uuid | YES | References the encryption key used to protect the secret's encrypted data, enabling key rotation and cryptographic operations within the vault system. |
| nonce | bytea | YES | A cryptographic value used to ensure uniqueness and prevent replay attacks when encrypting or decrypting secret data. Generated automatically by the vault's deterministic encryption system to provide additional security for stored secrets. |
| created_at | timestamp with time zone | NO | Records the exact moment when each secret entry was first added to the vault system. This timestamp enables audit trails and helps track the lifecycle of stored secrets. |
| updated_at | timestamp with time zone | NO | Records the date and time when a secret entry was last modified. This timestamp is automatically set to the current time whenever changes are made to the secret record. |

## Primary Key

`id`

## Indexes

- `secrets_name_idx`: CREATE UNIQUE INDEX secrets_name_idx ON vault.secrets USING btree (name) WHERE (name IS NOT NULL)
- `secrets_pkey`: CREATE UNIQUE INDEX secrets_pkey ON vault.secrets USING btree (id)

*Generated at: 2025-12-11T22:52:05.691Z*
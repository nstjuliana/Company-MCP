# users

**Database:** postgres_production
**Schema:** auth
**Description:** This table represents the core user authentication entity within a secure schema, storing login credentials and user account data for the application's authentication system. Based on the database comment indicating it stores "user login data within a secure schema," this table serves as the foundational user management component for controlling access to the system. The table currently has no relationships with other tables and contains no data, suggesting it may be part of a newly initialized authentication system or a standalone user management module.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| instance_id | uuid | YES | Purpose unclear from available data. Could represent a unique identifier for a specific deployment, tenant, or service instance within a multi-tenant authentication system. |
| id | uuid | NO | Uniquely identifies each user account within the authentication system. Serves as the primary reference for linking user data across the application. |
| aud | character varying | YES | Purpose unclear from available data. The column appears to be related to user authentication but without sample values or additional context, its specific business meaning cannot be determined. |
| role | character varying | YES | Purpose unclear from available data. Likely stores user authorization levels or access permissions within the authentication system. |
| email | character varying | YES | Purpose unclear from available data. Likely stores contact information for user accounts, but cannot be confirmed without sample values or additional context. |
| encrypted_password | character varying | YES | Stores the hashed and encrypted version of a user's login password for authentication purposes. Contains the secure representation of the password that cannot be reversed to reveal the original plaintext value. |
| email_confirmed_at | timestamp with time zone | YES | Records the exact date and time when a user verified their email address through the confirmation process. Remains empty until the user completes email verification, indicating unconfirmed accounts. |
| invited_at | timestamp with time zone | YES | Records the date and time when a user received an invitation to join the system. Purpose unclear from available data due to lack of sample values. |
| confirmation_token | character varying | YES | A unique token sent to users via email to verify their account registration or email address changes. Used in the authentication workflow to confirm user identity before activating account access. |
| confirmation_sent_at | timestamp with time zone | YES | Records the timestamp when an email confirmation was sent to the user as part of the account verification process. Purpose unclear from available data due to lack of sample values. |
| recovery_token | character varying | YES | Stores a temporary token used to authenticate and authorize password reset requests for user accounts. When present, this token allows users to securely change their password through the recovery process. |
| recovery_sent_at | timestamp with time zone | YES | Records the timestamp when a password recovery email or notification was last sent to the user. Used to track recovery attempt timing and potentially implement rate limiting or audit trails for account recovery processes. |
| email_change_token_new | character varying | YES | Stores a temporary token used to verify and authorize pending email address changes for user accounts. This token is likely generated when a user initiates an email change process and must be validated before the new email address becomes active. |
| email_change | character varying | YES | Purpose unclear from available data. Likely stores a new email address during the process of updating a user's primary email address. |
| email_change_sent_at | timestamp with time zone | YES | Records the timestamp when an email change confirmation message was sent to a user. Tracks when the system last attempted to deliver email verification for pending email address updates. |
| last_sign_in_at | timestamp with time zone | YES | Records the exact date and time when the user most recently successfully authenticated and signed into the system. Used to track user login activity and session management. |
| raw_app_meta_data | jsonb | YES | Purpose unclear from available data. Appears to store application-specific metadata in a flexible JSON structure, but without sample values the specific business meaning cannot be determined. |
| raw_user_meta_data | jsonb | YES | Purpose unclear from available data. Appears to store additional user information in a flexible JSON structure that supplements the standard user profile fields. |
| is_super_admin | boolean | YES | Indicates whether a user has the highest level of administrative privileges within the system. Purpose unclear from available data due to lack of sample values. |
| created_at | timestamp with time zone | YES | Records the date and time when a user account was initially established in the system. Purpose unclear from available data due to lack of sample values. |
| updated_at | timestamp with time zone | YES | Records when a user account was last modified or updated. Since no sample values are available and no database comment is provided, the specific update triggers and business rules cannot be determined from the available data. |
| phone | text | YES | Purpose unclear from available data. Likely stores contact telephone numbers for user accounts, but cannot be confirmed without sample values. |
| phone_confirmed_at | timestamp with time zone | YES | Records the exact moment when a user successfully verified their phone number through the confirmation process. Remains empty until phone verification is completed. |
| phone_change | text | YES | Stores a new phone number that a user has requested to change to, but has not yet been verified or activated. This field temporarily holds the pending phone number during the phone number change process. |
| phone_change_token | character varying | YES | A temporary security token used to verify and authorize changes to a user's phone number during the phone number update process. This token ensures that phone number modifications are authenticated and prevents unauthorized changes to user contact information. |
| phone_change_sent_at | timestamp with time zone | YES | Records the timestamp when a phone number change confirmation message was sent to the user. Tracks the delivery timing of phone verification communications during the phone update process. |
| confirmed_at | timestamp with time zone | YES | Records the date and time when a user's account was verified or activated through the confirmation process. A null value indicates the user has not yet completed account confirmation. |
| email_change_token_current | character varying | YES | Stores a temporary token used to validate and authorize a user's request to change their email address. This token is active during the email change process and likely gets cleared once the email change is confirmed or cancelled. |
| email_change_confirm_status | smallint | YES | Tracks the confirmation status of a pending email address change request using numeric codes. Purpose unclear from available data due to lack of sample values to determine specific status meanings. |
| banned_until | timestamp with time zone | YES | Specifies the date and time when a user's ban or suspension will be lifted, allowing them to regain access to the system. When null, indicates the user is either not banned or has a permanent ban. |
| reauthentication_token | character varying | YES | Stores a temporary security token used to verify a user's identity during sensitive operations that require additional authentication beyond the initial login. This token is likely generated when users need to re-confirm their credentials for actions like password changes or account modifications. |
| reauthentication_sent_at | timestamp with time zone | YES | Records when a reauthentication request was most recently sent to the user. Used to track timing of security verification prompts that require users to confirm their identity before accessing sensitive features. |
| is_sso_user | boolean | NO | Indicates whether a user account was created through Single Sign-On (SSO) authentication rather than traditional registration. When true, the account is allowed to have duplicate email addresses that would otherwise be restricted. |
| deleted_at | timestamp with time zone | YES | Records the date and time when a user account was soft deleted from the system. When populated, indicates the account is marked as deleted but data is retained for audit or recovery purposes. |
| is_anonymous | boolean | NO | Indicates whether the user account represents an anonymous or guest user rather than a registered user with identified credentials. Controls access permissions and features available to users who have not completed full registration or authentication. |

## Primary Key

`id`

## Indexes

- `confirmation_token_idx`: CREATE UNIQUE INDEX confirmation_token_idx ON auth.users USING btree (confirmation_token) WHERE ((confirmation_token)::text !~ '^[0-9 ]*$'::text)
- `email_change_token_current_idx`: CREATE UNIQUE INDEX email_change_token_current_idx ON auth.users USING btree (email_change_token_current) WHERE ((email_change_token_current)::text !~ '^[0-9 ]*$'::text)
- `email_change_token_new_idx`: CREATE UNIQUE INDEX email_change_token_new_idx ON auth.users USING btree (email_change_token_new) WHERE ((email_change_token_new)::text !~ '^[0-9 ]*$'::text)
- `reauthentication_token_idx`: CREATE UNIQUE INDEX reauthentication_token_idx ON auth.users USING btree (reauthentication_token) WHERE ((reauthentication_token)::text !~ '^[0-9 ]*$'::text)
- `recovery_token_idx`: CREATE UNIQUE INDEX recovery_token_idx ON auth.users USING btree (recovery_token) WHERE ((recovery_token)::text !~ '^[0-9 ]*$'::text)
- `users_email_partial_key`: CREATE UNIQUE INDEX users_email_partial_key ON auth.users USING btree (email) WHERE (is_sso_user = false)
- `users_instance_id_email_idx`: CREATE INDEX users_instance_id_email_idx ON auth.users USING btree (instance_id, lower((email)::text))
- `users_instance_id_idx`: CREATE INDEX users_instance_id_idx ON auth.users USING btree (instance_id)
- `users_is_anonymous_idx`: CREATE INDEX users_is_anonymous_idx ON auth.users USING btree (is_anonymous)
- `users_phone_key`: CREATE UNIQUE INDEX users_phone_key ON auth.users USING btree (phone)
- `users_pkey`: CREATE UNIQUE INDEX users_pkey ON auth.users USING btree (id)

*Generated at: 2025-12-11T22:51:06.767Z*
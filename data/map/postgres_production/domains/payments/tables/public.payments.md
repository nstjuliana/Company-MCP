# payments

**Database:** postgres_production
**Schema:** public
**Description:** This table represents payment transactions processed through a payment system, storing detailed information about each transaction including merchant details, card information, transaction amounts, and fraud detection results. The table captures both successful and failed payment attempts with geographic data (issuing country, acquirer country, IP country) and device information for risk assessment and fraud prevention. Based on the large row count (138K+ records) and comprehensive transaction attributes, this appears to be a central fact table in a payment processing data model that logs all payment events with their associated metadata and security flags.

**Row Count:** 138,236

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| payment_id | character varying | NO | A unique identifier assigned to each payment transaction, formatted as an 11-digit numeric string. Based on the sequential nature of the sample values, this appears to be a system-generated reference number used to track individual payment records. |
| merchant_id | character varying | YES | Identifies the business or organization that received the payment, with examples including fitness centers, retail stores, golf clubs, and AI services. Based on the sample data, merchants appear to be categorized by business type with descriptive naming conventions. |
| card_brand | character varying | YES | Identifies the payment card processing network or brand used for the transaction. Based on sample values, this appears to track various payment processors including GlobalCard, SwiftCharge, TransactPlus, and NexPay. |
| transaction_amount | numeric | YES | The monetary value of individual payment transactions processed through the system. Based on the sample values, amounts typically range from under $30 to several hundred dollars. |
| issuing_country | character varying | YES | Stores the two-letter country code indicating the nation where the payment method or financial instrument was issued. Based on the sample data, this includes European countries such as Netherlands, Sweden, Spain, Belgium, and Italy. |
| device_type | character varying | YES | Records the operating system or platform type of the device used to process the payment transaction. Values include mobile platforms like Android and iOS, desktop systems like Linux, and a catch-all category for unspecified devices. |
| shopper_interaction | character varying | YES | Indicates the type of interaction channel through which the customer completed their purchase transaction. Based on the sample data, this captures whether the payment was processed through an online commerce platform or at a physical point-of-sale terminal. |
| card_bin | character varying | YES | Contains the first 4-6 digits of payment card numbers, which identify the issuing bank and card type. Used for payment processing validation and fraud detection without storing complete card details. |
| is_fraudulent | boolean | YES | Indicates whether a payment transaction has been identified or flagged as fraudulent activity. Based on the sample data, the vast majority of payments are legitimate with occasional instances of detected fraud. |
| is_refused | boolean | YES | Indicates whether a payment transaction has been declined or rejected by the payment processor or financial institution. Based on the sample data, all observed payments appear to have been successfully processed without refusal. |
| aci | character varying | YES | Based on the sample values (F, D, C, G, E), this appears to be a classification or status code system using single letters to categorize payments. Purpose unclear from available data without additional context about what each letter code represents. |
| acquirer_country_code | character varying | YES | Stores the two-letter country code identifying the country where the payment acquirer (the financial institution processing the payment) is located. Based on the sample values, this includes countries such as the Netherlands, United States, and Italy. |
| ip_country | character varying | YES | Contains two-letter country codes indicating the geographic location associated with the IP address used during payment processing. Based on the sample data, this appears to track European countries where payment transactions originated. |
| created_at | timestamp without time zone | YES | Records the exact date and time when each payment record was initially created in the system. Automatically captures the moment of record insertion to maintain an audit trail of payment entry timing. |

## Primary Key

`payment_id`

## Indexes

- `idx_payments_card_brand`: CREATE INDEX idx_payments_card_brand ON public.payments USING btree (card_brand)
- `idx_payments_merchant_id`: CREATE INDEX idx_payments_merchant_id ON public.payments USING btree (merchant_id)
- `payments_pkey`: CREATE UNIQUE INDEX payments_pkey ON public.payments USING btree (payment_id)

## Sample Data

| payment_id | merchant_id | card_brand | transaction_amount | issuing_country | device_type | shopper_interaction | card_bin | is_fraudulent | is_refused | aci | acquirer_country_code | ip_country | created_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 10000636248 | Crossfit_Hanna | GlobalCard | 58.66 | NL | Linux | Ecommerce | 4571 | false | false | F | NL | BE | Tue Dec 09 2025 21:39:28 GMT-0600 (Central Stan... |
| 10001482390 | Belles_cookbook_store | GlobalCard | 36.62 | SE | Android | Ecommerce | 4556 | false | false | D | US | SE | Tue Dec 09 2025 21:39:28 GMT-0600 (Central Stan... |
| 10001579064 | Golfclub_Baron_Friso | GlobalCard | 130.67 | ES | Other | POS | 4556 | false | false | C | IT | ES | Tue Dec 09 2025 21:39:28 GMT-0600 (Central Stan... |
| 10002494026 | Crossfit_Hanna | SwiftCharge | 229.73 | BE | Android | Ecommerce | 4916 | false | false | F | NL | BE | Tue Dec 09 2025 21:39:28 GMT-0600 (Central Stan... |
| 10002671296 | Golfclub_Baron_Friso | TransactPlus | 748.91 | IT | Android | Ecommerce | 4891 | false | false | D | IT | BE | Tue Dec 09 2025 21:39:28 GMT-0600 (Central Stan... |

*Generated at: 2025-12-11T22:51:39.178Z*
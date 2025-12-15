# DABSTEP_PAYMENTS

**Database:** snowflake_production
**Schema:** PUBLIC
**Description:** This table represents payment transaction records processed through a payment service provider, capturing detailed information about each payment attempt including merchant details, card information, geographical data, and transaction outcomes. The table serves as a comprehensive transaction log that tracks payment processing events with temporal attributes (year, hour, minute, day of year), fraud indicators (HAS_FRAUDULENT_DISPUTE), and payment method details (card scheme, BIN, issuing country). Based on the column structure and sample data, this appears to be a fact table in a payments analytics data model, storing transactional events for reporting and fraud analysis purposes.

**Row Count:** 138,236

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| PSP_REFERENCE | TEXT | YES | Unique identifier assigned by a payment service provider to track individual payment transactions. Contains numeric reference codes that allow the payment processor to locate and manage specific payment records in their system. |
| MERCHANT | TEXT | YES | Contains the name or identifier of the business establishment that processed the payment transaction. Based on the sample data, this includes various types of merchants such as fitness centers, retail stores, and recreational facilities. |
| CARD_SCHEME | TEXT | YES | Identifies the payment card network or processing scheme used for the transaction, such as NexPay, GlobalCard, SwiftCharge, or TransactPlus. This field categorizes payments by their underlying card processing infrastructure or brand. |
| YEAR | NUMBER | YES | Records the calendar year when payment transactions occurred or were processed. Based on the sample data, all payments shown are from 2023. |
| HOUR_OF_DAY | NUMBER | YES | Represents the hour within a 24-hour day (0-23) when a payment transaction occurred. Based on the sample values, payments are processed throughout various hours of the day and night. |
| MINUTE_OF_HOUR | NUMBER | YES | Represents the minute component (0-59) of the hour when a payment transaction occurred. Based on the sample values, this captures the precise timing of payment events throughout each hour. |
| DAY_OF_YEAR | NUMBER | YES | Represents the sequential day number within a calendar year, ranging from 1 to 365/366. Based on the sample values, this tracks when payment transactions occurred throughout the year. |
| IS_CREDIT | BOOLEAN | YES | Indicates whether a payment transaction represents a credit to an account versus a debit. Based on the sample data, approximately half of the payment transactions are credits while the other half are debits. |
| EUR_AMOUNT | FLOAT | YES | Represents the monetary value of payments denominated in Euros. Based on the sample values ranging from approximately 13 to 238 Euros, this appears to capture transaction amounts of varying sizes. |
| IP_COUNTRY | TEXT | YES | Contains two-letter country codes indicating the geographic location associated with the IP address used during payment transactions. Based on the sample data, this includes European countries such as Sweden (SE), Netherlands (NL), and Luxembourg (LU). |
| ISSUING_COUNTRY | TEXT | YES | Contains two-letter country codes indicating the country where payment instruments or accounts were issued. Based on the sample values, this includes European countries such as Sweden (SE), Netherlands (NL), Luxembourg (LU), and Belgium (BE). |
| DEVICE_TYPE | TEXT | YES | Records the operating system or platform type of the device used during payment transactions. Captures major desktop and mobile platforms including Windows, Linux, MacOS, iOS, and Android. |
| IP_ADDRESS | TEXT | YES | Contains encoded or hashed identifiers that appear to be obfuscated representations of network addresses or client identifiers associated with payment transactions. The values are consistently formatted as base64-like strings, with some entries being empty. |
| EMAIL_ADDRESS | TEXT | YES | Contains encoded or hashed identifiers that appear to be obfuscated email addresses or user account references within the payment processing system. Purpose unclear from available data due to the encrypted nature of the values. |
| CARD_NUMBER | TEXT | YES | Stores encrypted or hashed representations of payment card numbers used for transaction processing. The values appear to be encoded identifiers that mask the actual card digits for security purposes. |
| SHOPPER_INTERACTION | TEXT | YES | Indicates the type of interaction or channel through which the shopper engaged during the payment process. Based on the sample data, this appears to primarily capture e-commerce transactions conducted through online channels. |
| CARD_BIN | TEXT | YES | Contains the first 4-6 digits of payment card numbers that identify the issuing bank or financial institution. These numeric codes are used for payment processing and fraud detection purposes. |
| HAS_FRAUDULENT_DISPUTE | BOOLEAN | YES | Indicates whether a payment has been subject to a dispute that was determined to be fraudulent in nature. Based on the sample data, the vast majority of payments do not have fraudulent disputes associated with them. |
| IS_REFUSED_BY_ADYEN | BOOLEAN | YES | Indicates whether a payment transaction was declined or rejected by the Adyen payment processing platform. Based on the sample data showing all false values, this tracks rejection status with true likely representing refused payments and false representing accepted or non-refused payments. |
| ACI | TEXT | YES | Based on the sample values showing single letter codes (F, D, G), this appears to be a categorical classification or status indicator with at least three distinct categories. Purpose unclear from available data without additional context about what these letter codes represent in the payment processing domain. |
| ACQUIRER_COUNTRY | TEXT | YES | Stores the two-letter country code representing the country where the payment acquirer (the financial institution processing the payment) is located. Based on the sample data, this includes countries such as Netherlands (NL), United States (US), and Italy (IT). |

## Sample Data

| PSP_REFERENCE | MERCHANT | CARD_SCHEME | YEAR | HOUR_OF_DAY | MINUTE_OF_HOUR | DAY_OF_YEAR | IS_CREDIT | EUR_AMOUNT | IP_COUNTRY | ISSUING_COUNTRY | DEVICE_TYPE | IP_ADDRESS | EMAIL_ADDRESS | CARD_NUMBER | SHOPPER_INTERACTION | CARD_BIN | HAS_FRAUDULENT_DISPUTE | IS_REFUSED_BY_ADYEN | ACI | ACQUIRER_COUNTRY |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 20034594130 | Crossfit_Hanna | NexPay | 2023 | 16 | 21 | 12 | false | 151.74 | SE | SE | Windows | pKPYzJqqwB8TdpY0jiAeQw | 0AKXyaTjW7H4m1hOWmOKBQ | uRofX46FuLUrSOTz8AW5UQ | Ecommerce | 4802 | false | false | F | NL |
| 36926127356 | Crossfit_Hanna | NexPay | 2023 | 23 | 58 | 75 | false | 45.7 | NL | NL | Linux | uzUknOkIqExYsWv4X14GUg | _Gm8at1k2ojYAM_wSEptNw | 6vqQ89zfCeFk6s4VOoWZFQ | Ecommerce | 4920 | false | false | F | NL |
| 31114608278 | Belles_cookbook_store | GlobalCard | 2023 | 4 | 30 | 96 | false | 14.11 | NL | NL | MacOS | 3VO1v_RndDg6jzEiPjfvoQ |  | EmxSN8-GXQw3RG_2v7xKxQ | Ecommerce | 4571 | false | false | F | US |
| 68442235288 | Crossfit_Hanna | NexPay | 2023 | 3 | 5 | 77 | true | 238.42 | LU | LU | iOS | 3qbuXGoFldniCC6r1X8K0Q | 5VW_2O6ku_0p_fLLwuC1vw | wG2VTvj2TfVG-NRDzifMHw | Ecommerce | 4017 | false | false | D | NL |
| 81404384199 | Crossfit_Hanna | NexPay | 2023 | 17 | 30 | 83 | false | 67.13 | NL | NL | Windows | 9WMJJdgtop6jkkyerxMvuQ | Alb1iUIxIqlW8YUeYVGTzg | 0khzuCj7aQ1e51S5vWR8gg | Ecommerce | 4532 | false | false | F | NL |

*Generated at: 2025-12-11T22:52:19.213Z*
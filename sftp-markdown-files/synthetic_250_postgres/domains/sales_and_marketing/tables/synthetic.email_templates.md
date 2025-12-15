# email_templates

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The "synthetic.email_templates" table represents a repository of email templates, each uniquely identified by a "template_id", designed for communication purposes. It stores detailed elements of each email template, such as the "template_name", "subject", and the contents in both HTML ("html_content") and plain text ("text_content") formats, alongside metadata like "category", "is_active" status, and timestamps for creation and updates. The absence of foreign key relationships indicates that the table functions independently within the database, primarily serving as a resource for other processes or systems that create or manage automated emails.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| template_id | integer | NO | This column serves as a unique identifier for each email template within the system. It ensures that each template can be distinctly referenced and managed. |
| template_name | character varying | NO | This column contains titles or headings used for email templates. These titles appear to be brief and varied, possibly reflecting different subjects or themes for the emails. |
| subject | character varying | YES | This column appears to contain the subject lines used in email templates, which include a variety of themes and contexts, likely intended to capture attention or convey a specific message. Purpose details for individual subject lines are unclear from the available data. |
| html_content | text | YES | Contains the HTML-based content intended for use within email templates. This content likely forms the main body or parts of the visual layout for emails. |
| text_content | text | YES | The column contains the body text of email templates, which appear to consist of diverse, disjointed phrases likely intended as placeholders or randomly generated content. Purpose unclear from available data. |
| category | character varying | YES | This column likely categorizes email templates based on various thematic or contextual elements, such as content type or intended audience. Purpose unclear from available data. |
| is_active | boolean | YES | Indicates whether an email template is currently active or inactive. Defaults to active unless specified otherwise. |
| created_at | timestamp without time zone | YES | This column records the date and time when an email template was created. The value defaults to the current timestamp, indicating the initial creation moment is captured automatically if no other timestamp is provided. |
| updated_at | timestamp without time zone | YES | This column records the date and time when an email template was last modified. It allows for tracking updates without timezone information, with current timestamps being the default for modifications. |

## Primary Key

`template_id`

## Indexes

- `email_templates_pkey`: CREATE UNIQUE INDEX email_templates_pkey ON synthetic.email_templates USING btree (template_id)

## Sample Data

| template_id | template_name | subject | html_content | text_content | category | is_active | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Increase within free have. Dog these man when o... | Beyond you bank always a two. Today station mak... | Weight fill president spring individual us. Pro... | Executive four floor dream. Itself but popular ... | Prevent hair hospital generation any subject so... | false | Sat Dec 13 2025 03:14:05 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:05 GMT-0600 (Central Stan... |
| 2 | Rate bag positive. Again candidate see election... | Accept mission event some simply could. Draw in... | Able decision book recent including game langua... | Process quite kitchen cut play deal. Could prog... | Modern data book expert exist computer shoulder... | false | Sat Dec 13 2025 03:14:05 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:05 GMT-0600 (Central Stan... |
| 3 | Ready even probably son second. As whatever blu... | Here person three foot. Ground serve mouth mana... | Threat throw behavior type partner behavior eco... | Somebody thought beyond mean director. Everyone... | Scene run cultural decide car. Article last pea... | true | Sat Dec 13 2025 03:14:05 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:05 GMT-0600 (Central Stan... |
| 4 | Cultural far significant. Until themselves brea... | Much base modern behavior end. Carry condition ... | Base close score. | Bar couple well better. Positive arm piece why ... | May small fire light medical. Ago out able end ... | false | Sat Dec 13 2025 03:14:05 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:05 GMT-0600 (Central Stan... |
| 5 | Create responsibility could positive hundred dr... | Cost small return. Future raise family where tr... | Million store every rise care particular recent... | Rock southern south bed represent lawyer. Retur... | Describe if follow difficult think talk rich. T... | false | Sat Dec 13 2025 03:14:05 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:05 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:40:37.814Z*

import json
import ollama


MODEL_NAME = "qwen2.5:7b"

REQUIRED_FIELDS = [
    "Agreement Value",
    "Agreement Start Date",
    "Agreement End Date",
    "Renewal Notice (Days)",
    "Party One",
    "Party Two",
]



SYSTEM_PROMPT = """
You are an AI system that extracts metadata from rental
agreements using the meaning and context of the document.

Extract exactly six fields.

1. AGREEMENT VALUE
Extract the monthly rent amount payable by the tenant.
Do not extract security deposits, advances, maintenance
charges, or penalties.
Return a number, or null if not found.

2. AGREEMENT START DATE
Extract the date when the rental agreement period begins.
Look for phrases such as:
- commencing from
- starting from
- beginning on
- date of tenancy
- effective from

If the agreement states that it is made or executed on a
date and the rental period begins from that date, use it.
Do not automatically use a later signature date when an
earlier commencement date is explicitly stated.
Return DD.MM.YYYY or null.

3. AGREEMENT END DATE
Extract an explicitly stated expiry or ending date of the
rental agreement period.
Look for phrases such as:
- ending on
- expires on
- valid until
- terminates on
- period ending

Do not calculate an end date from the duration.
Return DD.MM.YYYY or null if no explicit date is available.

4. RENEWAL NOTICE (DAYS)
Extract the notice period stated in the agreement for
giving advance notice about renewal, non-renewal, or
ending/vacating the tenancy.
Look for explicit notice periods such as 15 days,
one month, two months, or three months.
Do not confuse the notice period with the agreement
duration.
Convert explicitly stated months into days using
30 days per month.
Return a number or null if no notice period is stated.

5. PARTY ONE
Extract the actual first contracting party, normally the
landlord, lessor, or owner.
Include all jointly named owners.
Return only the contracting party's name.
Do not include titles, father's names, spouse's names,
addresses, occupations, or unrelated details.
Do not include witnesses or occupants.

6. PARTY TWO
Extract the actual second contracting party, normally the
tenant, lessee, or resident.
Include all jointly named tenants.
Return only the contracting party's name.
Do not include titles, father's names, spouse's names,
addresses, occupations, or unrelated details.
Do not include witnesses or unrelated occupants.

GENERAL RULES:
- Read the complete document before extracting.
- Identify parties by their contractual roles, not just
  by the order in which names appear.
- Distinguish contracting parties from witnesses,
  family members, and additional occupants.
- Preserve the actual spelling and initials of names.
- Do not add information that is not in the document.
- If a field cannot be established confidently, return null.
- Do not calculate or invent missing values.
- Return exactly six fields.
- Return valid JSON only.
- Use numbers for Agreement Value and Renewal Notice.
- Use DD.MM.YYYY for dates.
- Use null for unavailable values.
"""


def extract_metadata(document_text):

    if not document_text or not document_text.strip():
        raise ValueError("Document text is empty.")

    user_prompt = f"""
Extract the six required metadata fields from the
following rental agreement.

Read the complete document and use the context of
the agreement to identify the correct information.

Do not include explanations or additional fields.

DOCUMENT TEXT:

{document_text}

Return this JSON structure:

{{
    "Agreement Value": null,
    "Agreement Start Date": null,
    "Agreement End Date": null,
    "Renewal Notice (Days)": null,
    "Party One": null,
    "Party Two": null
}}
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        format="json",
        options={"temperature": 0},
    )

    result = json.loads(response["message"]["content"])

    if not isinstance(result, dict):
        raise ValueError("AI response is not a JSON object.")

    return {
        field: result.get(field)
        for field in REQUIRED_FIELDS
    }

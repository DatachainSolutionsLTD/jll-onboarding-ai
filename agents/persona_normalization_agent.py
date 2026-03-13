from openai import OpenAI

client = OpenAI()


def normalize_persona(job_title):

    prompt = f"""
You are an enterprise HR persona classification system.

Convert the following job title into one of these personas:

Facilities Manager
Finance Manager
IT Operations
HR Business Partner
Sales Executive
Executive Leadership

Return ONLY the persona name.

Job Title:
{job_title}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "You classify enterprise job titles into personas."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    persona = response.choices[0].message.content.strip()

    return persona
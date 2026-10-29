
x1='''Merit scholarship
Students who secure a CGPA of 9.0 or above in the previous academic year receive a 50% waiver on
the tuition amount for the next year. Students with a CGPA between 8.5 and 8.99 receive a 25%
waiver. The student must have no backlog subjects and must meet the 75% attendance requirement.
Need-based scholarship
Students whose family income is below Rs. 3,00,000 per year may apply for a 30% waiver on the
tuition amount. An income certificate issued within the last six months must be attached to the
application.
How to apply
Applications are submitted on the student portal by 31 August each year, with attested copies of mark
sheets and the required certificates. A student cannot receive both the merit and the need-based
scholarship in the same year; the higher of the two is applied. Sports quota scholarships are handled
separately by the Physical Education department.'''
from dotenv import load_dotenv
from pathlib import Path
from google import genai
import os
from google.genai import types
print("start")
print("Loading .env...", flush=True)
load_dotenv(Path(__file__).with_name(".env"), override=True)
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY was not found in .env")
print("Creating Gemini client...", flush=True)
client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(timeout=120_000),
)
print("Sending request to Gemini...", flush=True)
response = client.interactions.create(
    model="gemini-3.5-flash",
    input=(
        "Answer only from the text below. If the answer is not there, say not found.\n\n"
        +x1+
        "\n\nQuestion 1: how to get a merit scholarship?"
        "\n\nQuestion 2: what is the name of the headmaster?"
    ),
)
print("Got response:", flush=True)
print(response.output_text)
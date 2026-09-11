from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

client = OpenAI()

def summarize_paper(title, abstract):

    prompt = f"""
    You are an astronomy research assistant.

    Return ONLY valid JSON.

    {{
      "main_result": "",
      "why_it_matters": "",
      "teaching_level": "",
      "topics": [],
      "research_tags": [],
      "priority": "",
      "classroom_use": ""
    }}
    
    For research_tags, choose any applicable tags from:

    - Cataclysmic Variables
    - Dwarf Novae
    - Novae
    - Variable Stars
    - White Dwarfs
    - Binary Stars
    - Accretion Disks
    - Time Domain Astronomy
    - TESS
    - Gaia

    Only include tags that are clearly relevant.

    Title:
    {title}

    Abstract:
    {abstract}
    """

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
    )

        clean_text = response.output_text

        clean_text = clean_text.replace("```json", "")
        clean_text = clean_text.replace("```", "")
        clean_text = clean_text.strip()

        return json.loads(clean_text)

    except Exception as e:
        return f"SUMMARY ERROR: {e}"
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
      "why_blake_should_read_this": "",
      "research_priority": "",
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

    Only assign "Cataclysmic Variables" when the paper
    explicitly studies cataclysmic variables, dwarf novae,
    nova-like variables, novae, CV populations, CV evolution,
    or accreting white dwarf binaries.

    Do not assign "Cataclysmic Variables" merely because a paper
    mentions binaries, white dwarfs, compact objects, or variability.

    Title:
    {title}

    Abstract:
    {abstract}
    
    For why_blake_should_read_this:

    Assume the reader is an astronomy instructor whose
    research interests include:

    - Cataclysmic Variables
    - Variable Stars
    - White Dwarfs
    - Binary Stars
    - Accretion Disks
    - Time Domain Astronomy

    Provide 1-3 sentences describing why this paper
    may be relevant to those interests.
    
    For research_priority:

    Assume the reader's research interests are:

    - Cataclysmic Variables
    - Dwarf Novae
    - Novae
    - Variable Stars
    - White Dwarfs
    - Binary Stars
    - Accretion Disks
    - Time Domain Astronomy

    Return exactly one of:

    Must Read
    Worth Reading
    Background Reading
    Not Relevant

    Choose Must Read only for papers that are directly relevant
    to cataclysmic variables, dwarf novae, novae, accretion
    physics, or closely related binary evolution.
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
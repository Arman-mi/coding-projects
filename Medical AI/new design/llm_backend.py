# llm_backend.py — pluggable LLM parser using strict JSON schema
# Env:
#   USE_LLM=1
#   LLM_PROVIDER=openai|anthropic
#   OPENAI_API_KEY=...   OPENAI_MODEL=gpt-4o-mini
#   ANTHROPIC_API_KEY=...  ANTHROPIC_MODEL=claude-3-5-sonnet-latest

from typing import Dict, Any, Optional
import os, json
from dotenv import load_dotenv

load_dotenv()  # loads .env if present

try:
    from pydantic import BaseModel
except Exception:
    BaseModel = object

class ParsedActionModel(BaseModel):
    action_type: str
    free_text: str
    symptom: Optional[str] = None
    body_region: Optional[str] = None
    duration: Optional[str] = None
    severity: Optional[str] = None
    test_name: Optional[str] = None
    intervention: Optional[str] = None
    confidence: float = 0.6
    def to_dict(self) -> Dict[str, Any]:
        d = getattr(self, "model_dump", None)
        d = d() if d else self.__dict__
        return {k:v for k,v in d.items() if v is not None}

SCHEMA_JSON = {
  "type": "object",
  "additionalProperties": False,
  "required": ["action_type", "free_text", "confidence"],
  "properties": {
    "action_type": {"type": "string", "enum": ["vitals_request","history","ros","physical_exam","diagnostic","intervention","management","meta"]},
    "free_text": {"type": "string"},
    "symptom": {"type": "string"},
    "body_region": {"type": "string"},
    "duration": {"type": "string"},
    "severity": {"type": "string"},
    "test_name": {"type": "string"},
    "intervention": {"type": "string"},
    "confidence": {"type": "number", "minimum": 0, "maximum": 1}
  }
}

SYSTEM_INSTRUCTIONS = """You are an EMT sim action parser.
Map the user's message into ONE JSON object that matches the JSON Schema exactly.
- 'onset/LKW' => action_type=history, symptom="onset time"
- vitals phrasing => action_type=vitals_request
- diagnostics (ECG/glucose) => action_type=diagnostic and set test_name
- interventions (aspirin/epinephrine/oxygen/albuterol) => action_type=intervention and set intervention
- 'stroke alert' => action_type=management
Set confidence to 0.9 if clear, else 0.6. Return ONLY valid JSON.
-Prefer a specific action_type from: vitals_request | history | ros | physical_exam | diagnostic | intervention | management.
- Only use "meta" if the message is chit-chat or genuinely unrelated to the simulation.
- When the user asks an open-ended probe like "Where does it hurt?", emit history with symptom="pain location
"""

def _openai_parse(text: str) -> Dict[str, Any]:
    from openai import OpenAI
    client = OpenAI()
    resp = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[{"role":"system","content":SYSTEM_INSTRUCTIONS},
                  {"role":"user","content":text}],
        response_format={
            "type":"json_schema",
            "json_schema":{"name":"ParsedAction","schema":SCHEMA_JSON,"strict":True}
        },
        temperature=0
    )
    data = json.loads(resp.choices[0].message.content)
    return ParsedActionModel(**data).to_dict()

def _anthropic_parse(text: str) -> Dict[str, Any]:
    import anthropic
    client = anthropic.Anthropic()
    tools = [{
        "name":"emit_parsed_action",
        "description":"Return the parsed action object",
        "input_schema": SCHEMA_JSON
    }]
    msg = client.messages.create(
        model=os.getenv("ANTHROPIC_MODEL","claude-3-5-sonnet-latest"),
        system=SYSTEM_INSTRUCTIONS,
        tools=tools,
        max_tokens=512,
        messages=[{"role":"user","content":text}]
    )
    tool = next((b for b in msg.content if getattr(b,"type","")== "tool_use"), None)
    if not tool:
        return ParsedActionModel(action_type="meta", free_text=text, confidence=0.4).to_dict()
    return ParsedActionModel(**tool.input).to_dict()

def llm_parse_action(text: str) -> Dict[str, Any]:
    provider = (os.getenv("LLM_PROVIDER") or "openai").lower()
    try:
        return _anthropic_parse(text) if provider=="anthropic" else _openai_parse(text)
    except Exception:
        # Fail-soft: fall back to heuristic parser upstream
        return ParsedActionModel(action_type="meta", free_text=text, confidence=0.4).to_dict()

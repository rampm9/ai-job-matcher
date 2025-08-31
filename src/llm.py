import os, json, time
from typing import Dict, Any
from openai import OpenAI, APIConnectionError, RateLimitError, APIStatusError

FALLBACK_JD = {
  "title":"Unknown","seniority":"Senior","location_policy":"",
  "required_skills":[],"nice_to_have_skills":[],
  "responsibilities":[],"must_have_experience":[],
  "domain":[],"education_required":"","certifications_required":[],
  "visa_or_timezone":"","constraints":{"hard_blocks":[]}
}
FALLBACK_CV = {
  "name":"Unknown","location":"","titles":[],"skills":[],
  "experience_bullets":[],"education":"","certifications":[],
  "domains":[],"work_auth":"","timezones":[]
}

def _retry(fn, tries=3, base=0.6, factor=2.0):
    for i in range(tries):
        try:
            return fn()
        except (RateLimitError, APIConnectionError, APIStatusError):
            if i == tries - 1:
                raise
            time.sleep(base * (factor ** i))

def llm_json_parse(prompt: str) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        # No key → fallback minimal structure so the app still works
        out = FALLBACK_JD if "job description" in prompt.lower() else FALLBACK_CV
        out["_mode"] = "fallback"
        return out

    client = OpenAI(api_key=api_key)

    def _call():
        resp = client.chat.completions.create(
            model="gpt-4o-mini",  # small, inexpensive, good JSON
            messages=[
                {"role":"system","content":"Return ONLY valid JSON."},
                {"role":"user","content":prompt}
            ],
            response_format={"type":"json_object"},
            timeout=25
        )
        return json.loads(resp.choices[0].message.content)

    try:
        data = _retry(_call)
        data["_mode"] = "ai-powered"
        return data
    except Exception as e:
        # Graceful degrade
        out = FALLBACK_JD if "job description" in prompt.lower() else FALLBACK_CV
        out["_mode"] = "fallback"
        return out

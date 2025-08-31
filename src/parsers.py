import os, json
from .llm import llm_json_parse

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def _read_prompt(name: str) -> str:
    path = os.path.join(BASE_DIR, "prompts", name)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def parse_jd_text(text: str) -> dict:
    prompt = _read_prompt("parse_jd.md").replace("{{JD_TEXT}}", text)
    return llm_json_parse(prompt)

def parse_cv_text(text: str) -> dict:
    prompt = _read_prompt("parse_cv.md").replace("{{CV_TEXT}}", text)
    return llm_json_parse(prompt)

import os, json, time
from typing import Dict, Any
from .parsers import parse_jd_text, parse_cv_text
from .scoring import (
    score_skills, score_responsibilities_semantic, score_seniority,
    score_domain, score_education, score_location, score_outcomes,
    weighted_sum, bucket
)
from .extractor import check_must_haves, build_improvements
from .report import make_report_json
from .embeddings import embed_func

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

with open(os.path.join(BASE_DIR, "config", "weights.json"), "r") as f:
    WEIGHTS = json.load(f)
with open(os.path.join(BASE_DIR, "config", "thresholds.json"), "r") as f:
    THR = json.load(f)

def _cap_list(xs, n): 
    return xs[:n] if xs else []

def analyze_texts(jd_text: str, cv_text: str) -> Dict[str, Any]:
    t0 = time.time()
    jd = parse_jd_text(jd_text); t_jd = time.time()
    cv = parse_cv_text(cv_text); t_cv = time.time()

    # Cap bullets to reduce tokens and improve performance
    jd["responsibilities"] = _cap_list(jd.get("responsibilities"), 12)
    cv["experience_bullets"] = _cap_list(cv.get("experience_bullets"), 25)

    skills = score_skills(jd, cv, WEIGHTS, THR); t_skills = time.time()
    resp, src_map, resp_mode = score_responsibilities_semantic(
        jd.get("responsibilities", []),
        cv.get("experience_bullets", []),
        THR,
        embed_func
    ); t_resp = time.time()

    seniority = score_seniority(jd.get("seniority"), cv.get("titles", []), THR)
    domain = score_domain(jd.get("domain", []), cv.get("domains", []))
    edu = score_education(jd.get("education_required", ""), cv.get("education", ""), cv.get("certifications", []))
    loc = score_location(jd.get("visa_or_timezone", ""), cv)
    outcomes = score_outcomes(cv.get("experience_bullets", []), jd); t_finish = time.time()

    # detect LLM parse mode (from llm.py we put _mode on parsed JSON)
    parse_mode = "ai-powered" if (jd.get("_mode")=="ai-powered" or cv.get("_mode")=="ai-powered") else "fallback"

    components = {
      "skills_coverage": round(skills, 1),
      "responsibilities_similarity": round(resp, 1),
      "seniority_alignment": round(seniority, 1),
      "domain_fit": round(domain, 1),
      "education": round(edu, 1),
      "location": round(loc, 1),
      "outcomes_alignment": round(outcomes, 1)
    }

    overall = weighted_sum(components, WEIGHTS)

    missing = check_must_haves(jd.get("must_have_experience", []), cv)
    gated = len(missing) > 0
    if gated:
        overall = min(overall, THR["must_have_cap"])

    tier = bucket(overall, THR)
    improv = build_improvements(jd, cv, src_map, THR)

    report = make_report_json(overall, tier, gated, missing, components, src_map, improv)
    # add modes to help you debug
    report["modes"] = {
        "parsing": parse_mode,
        "embeddings": resp_mode
    }
    # add timing information
    report["timings_sec"] = {
      "parse_jd": round(t_jd - t0, 3),
      "parse_cv": round(t_cv - t_jd, 3),
      "skills_score": round(t_skills - t_cv, 3),
      "responsibility_match": round(t_resp - t_skills, 3),
      "rest": round(t_finish - t_resp, 3),
      "total": round(t_finish - t0, 3)
    }
    return report

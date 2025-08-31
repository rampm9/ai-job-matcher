from typing import List, Dict, Any, Tuple
import numpy as np

def cosine(a: np.ndarray, b: np.ndarray) -> float:
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 0.0
    return float(np.dot(a, b) / (na * nb))

def recency_weight(year: int, current_year: int, rw: Dict[str, float]) -> float:
    if not year: return rw["7_inf"]
    age = max(0, current_year - year)
    if age <= 3: return rw["0_3"]
    if age <= 7: return rw["3_7"]
    return rw["7_inf"]

def score_skills(jd: Dict, cv: Dict, weights: Dict[str,int], thr: Dict[str,Any], current_year: int = 2025) -> float:
    req = set([s.lower() for s in jd.get("required_skills", [])])
    nice = set([s.lower() for s in jd.get("nice_to_have_skills", [])])
    cv_skills = { s.get("name","").lower(): s.get("last_used_year", current_year) for s in cv.get("skills", []) }

    match_req, total_req = 0.0, len(req) * 2.0
    match_nice, total_nice = 0.0, len(nice) * 1.0

    for skill in req:
        if skill and skill in cv_skills:
            match_req += 2.0 * recency_weight(cv_skills[skill], current_year, thr["recency_weights"])

    for skill in nice:
        if skill and skill in cv_skills:
            match_nice += 1.0 * recency_weight(cv_skills[skill], current_year, thr["recency_weights"])

    if (total_req + total_nice) == 0:
        return weights["skills_coverage"]
    coverage = (match_req + match_nice) / max(1e-6, (total_req + total_nice))
    return coverage * weights["skills_coverage"]

def score_responsibilities_semantic(jd_resps: List[str], cv_bullets: List[Dict[str,Any]], thr: Dict[str,Any], embed_func=None) -> Tuple[float, List[Dict[str,Any]], str]:
    if not jd_resps or not cv_bullets: return 0.0, [], "fallback"
    
    jd_vecs, cv_vecs = [], []
    embed_modes = set()

    for r in jd_resps:
        v, m = embed_func(r)
        jd_vecs.append(v); embed_modes.add(m)

    for b in cv_bullets:
        v, m = embed_func(b.get("text",""))
        cv_vecs.append(v); embed_modes.add(m)

    source_map = []
    sims = []

    for i, jv in enumerate(jd_vecs):
        best_sim, best_idx = 0.0, -1
        for k, cvv in enumerate(cv_vecs):
            s = cosine(jv, cvv)
            if s > best_sim:
                best_sim, best_idx = s, k
        if best_sim >= thr["semantic_match_min"]:
            source_map.append({
                "jd_line": jd_resps[i],
                "cv_supporting_line": cv_bullets[best_idx].get("text"),
                "similarity": round(best_sim, 3)
            })
            sims.append(best_sim)
        else:
            source_map.append({
                "jd_line": jd_resps[i],
                "cv_supporting_line": None,
                "similarity": round(best_sim, 3)
            })

    if not sims: return 0.0, source_map, ("ai-powered" if "ai-powered" in embed_modes else "fallback")
    avg = sum(sims) / len(jd_resps)
    return avg * 25.0, source_map, ("ai-powered" if "ai-powered" in embed_modes else "fallback")

def score_seniority(jd_level: str, titles: List[Dict[str,Any]], thr: Dict[str,Any]) -> float:
    lv = thr["title_levels"]
    max_cv = 0
    for t in titles or []:
        max_cv = max(max_cv, lv.get((t.get("level") or "IC"), 1))
    jdv = lv.get(jd_level or "IC", 1)
    diff = max(0, jdv - max_cv)
    if diff >= 2: return 0.0
    if diff == 1: return 5.0
    return 10.0

def score_domain(jd_domains: List[str], cv_domains: List[str]) -> float:
    if not jd_domains: return 10.0
    jd_set = set([d.lower() for d in jd_domains or []])
    cv_set = set([d.lower() for d in cv_domains or []])
    if jd_set & cv_set: return 10.0
    partial = any(any(x in y or y in x for x in jd_set) for y in cv_set)
    return 5.0 if partial else 0.0

def score_education(req: str, edu: str, certs: List[str]) -> float:
    if not req: return 5.0
    lower = ((edu or "") + " " + " ".join([c or "" for c in certs or []])).lower()
    tokens = [t for t in req.lower().split() if len(t) > 2]
    return 5.0 if any(tok in lower for tok in tokens) else 2.5

def score_location(vtz: str, cv: Dict) -> float:
    if not vtz: return 5.0
    text = (cv.get("work_auth","") + " " + " ".join(cv.get("timezones",[]) or []) + " " + (cv.get("location","") or "")).lower()
    tokens = [t for t in vtz.lower().split() if len(t) > 2]
    return 5.0 if any(tok in text for tok in tokens) else 2.5

def score_outcomes(bullets: List[Dict[str,Any]], jd: Dict) -> float:
    score = 0.0
    for b in bullets or []:
        t = (b.get("text") or "").lower()
        if any(sym in t for sym in ["%", "$", " roi", "arr", "maus", "conversion", "retention", "latency", "cost", "time to", "reduced", "increased", "grew", "x"]):
            score += 2.0
    return min(10.0, score)

def weighted_sum(parts: Dict[str,float], weights: Dict[str,int]) -> float:
    return sum(parts.values())

def bucket(overall: float, thr: Dict[str,Any]) -> str:
    if overall >= thr["tier_strong"]: return "Strong fit"
    if overall >= thr["tier_good"]: return "Good fit"
    if overall >= thr["tier_possible"]: return "Possible fit"
    if overall >= thr["tier_needs"]: return "Needs work"
    return "Low fit"

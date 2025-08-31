from typing import List, Dict, Any

def check_must_haves(musts: List[str], cv: Dict) -> List[str]:
    blob = " ".join([
        cv.get("education","") or "",
        " ".join([b.get("text","") for b in cv.get("experience_bullets",[])]),
        " ".join([s.get("name","") for s in cv.get("skills",[])])
    ]).lower()
    missing = []
    for m in musts or []:
        tokens = [t for t in m.lower().split() if len(t) > 2]
        if not any(tok in blob for tok in tokens):
            missing.append(m)
    return missing

def build_improvements(jd: Dict, cv: Dict, source_map: List[Dict[str,Any]], thr: Dict[str,Any]) -> List[str]:
    tips = []
    for item in source_map or []:
        if not item.get("cv_supporting_line") or item.get("similarity", 0.0) < thr["semantic_match_min"]:
            tips.append(f"Address: {item['jd_line']} with a recent, outcome-focused example.")
    return tips[:5]

from typing import Dict, Any

DISCLAIMER = (
  "This score is an estimate based on job description and resume text. "
  "There is no universal benchmark for a 'good' match rate; companies and roles vary widely. "
  "We use keyword normalization and semantic similarity to approximate relevance. Human review is essential."
)

def make_report_json(overall, tier, gated, missing, components, source_lines, improvement_list) -> Dict[str, Any]:
    return {
        "overall_score": round(overall, 1),
        "tier": tier,
        "gated_by_must_haves": gated,
        "missing_must_haves": missing,
        "components": components,
        "matched_lines": source_lines,
        "improvements": improvement_list,
        "disclaimer": DISCLAIMER
    }

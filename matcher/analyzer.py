"""The brain: find skills in text and score resume vs job description."""
import re
from collections import Counter
from dataclasses import dataclass, field

from .skills import SKILLS
from .text import tokenize


def _pattern(term: str) -> re.Pattern:
    # Boundaries that don't break on c++, c#, node.js, ci/cd
    return re.compile(r"(?<![A-Za-z0-9+#])" + re.escape(term) + r"(?![A-Za-z0-9+#])",
                      re.IGNORECASE)


_SKILL_PATTERNS = {
    skill: [_pattern(t) for t in [skill] + aliases] for skill, aliases in SKILLS.items()
}


def extract_skills(text: str) -> set:
    """Return the set of canonical skills mentioned in text."""
    found = set()
    for skill, patterns in _SKILL_PATTERNS.items():
        if any(p.search(text) for p in patterns):
            found.add(skill)
    return found


def top_keywords(text: str, n: int = 15, exclude: set = frozenset()) -> list:
    """Most repeated meaningful words in text (words appearing 2+ times)."""
    counts = Counter(w for w in tokenize(text) if w not in exclude)
    return [w for w, c in counts.most_common(n) if c >= 2]


@dataclass
class Result:
    score: float
    skill_score: float
    keyword_score: float
    matched_skills: list = field(default_factory=list)
    missing_skills: list = field(default_factory=list)
    extra_skills: list = field(default_factory=list)
    matched_keywords: list = field(default_factory=list)
    missing_keywords: list = field(default_factory=list)

    @property
    def verdict(self) -> str:
        if self.score >= 75:
            return "Strong match"
        if self.score >= 50:
            return "Decent match - tailor your resume"
        return "Weak match - big gaps"


def analyze(resume: str, job: str, top_n: int = 15) -> Result:
    resume_skills = extract_skills(resume)
    job_skills = extract_skills(job)

    matched = sorted(job_skills & resume_skills)
    missing = sorted(job_skills - resume_skills)
    extra = sorted(resume_skills - job_skills)
    skill_score = 100 * len(matched) / len(job_skills) if job_skills else 0.0

    # Words in the job description that aren't already known skills
    skill_words = {w for s in job_skills for w in s.split()}
    kws = top_keywords(job, top_n, exclude=skill_words)
    resume_words = set(tokenize(resume))
    kw_matched = [k for k in kws if k in resume_words]
    kw_missing = [k for k in kws if k not in resume_words]
    keyword_score = 100 * len(kw_matched) / len(kws) if kws else 0.0

    if job_skills and kws:
        score = 0.7 * skill_score + 0.3 * keyword_score
    elif job_skills:
        score = skill_score
    else:
        score = keyword_score

    return Result(
        score=round(score, 1),
        skill_score=round(skill_score, 1),
        keyword_score=round(keyword_score, 1),
        matched_skills=matched,
        missing_skills=missing,
        extra_skills=extra,
        matched_keywords=kw_matched,
        missing_keywords=kw_missing,
    )

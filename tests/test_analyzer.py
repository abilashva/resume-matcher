from matcher.analyzer import analyze, extract_skills, top_keywords
from matcher.text import tokenize


def test_extract_skills_with_aliases():
    skills = extract_skills("I know JS, C++, Node.js and the k8s basics. DSA too.")
    assert {"javascript", "c++", "node.js", "kubernetes", "data structures"} <= skills


def test_c_does_not_match_inside_words():
    assert "c" not in extract_skills("I like cooking and music")
    assert "c" in extract_skills("Languages: C, Java")


def test_tokenize_drops_stopwords():
    assert tokenize("The team will build the backend") == ["build", "backend"]


def test_top_keywords_needs_repeats():
    kws = top_keywords("backend backend automation automation api", n=5)
    assert kws == ["backend", "automation"]


def test_perfect_match():
    text = "Python SQL Git Docker"
    r = analyze(text, text)
    assert r.skill_score == 100.0
    assert r.missing_skills == []


def test_missing_and_extra():
    r = analyze(resume="Python Java", job="Python Docker Kubernetes")
    assert r.matched_skills == ["python"]
    assert r.missing_skills == ["docker", "kubernetes"]
    assert r.extra_skills == ["java"]
    assert r.skill_score == 33.3


def test_verdict_levels():
    assert analyze("Python SQL", "Python SQL").verdict == "Strong match"
    assert "Weak" in analyze("Excel", "Python SQL Docker Git").verdict

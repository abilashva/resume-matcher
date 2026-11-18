"""Command line interface."""
import argparse
import json
import sys
from dataclasses import asdict

from .analyzer import analyze
from .text import read_text


def bar(score: float, width: int = 20) -> str:
    filled = round(width * score / 100)
    return "#" * filled + "-" * (width - filled)


def print_report(r) -> None:
    print(f"\nMatch score: {r.score}%  [{bar(r.score)}]")
    print(f"Verdict:     {r.verdict}")
    print(f"(skills {r.skill_score}% | keywords {r.keyword_score}%)\n")

    def section(title, items):
        print(f"{title} ({len(items)})")
        print("  " + (", ".join(items) if items else "-"))
        print()

    section("Matched skills", r.matched_skills)
    section("Missing skills", r.missing_skills)
    section("Missing keywords", r.missing_keywords)
    section("Extra skills on your resume", r.extra_skills)

    if r.missing_skills:
        print("Tip: add missing skills ONLY if you genuinely have them.")


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Compare a resume to a job description.")
    p.add_argument("resume", help="Resume file (.txt, .md, or .pdf)")
    p.add_argument("job", help="Job description file (.txt, .md, or .pdf)")
    p.add_argument("--json", action="store_true", help="Print result as JSON")
    p.add_argument("--top", type=int, default=15, help="How many JD keywords to check")
    args = p.parse_args(argv)

    try:
        result = analyze(read_text(args.resume), read_text(args.job), args.top)
    except (FileNotFoundError, RuntimeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(asdict(result), indent=2))
    else:
        print_report(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())

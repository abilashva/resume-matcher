import json

from matcher.cli import main


def test_cli_json(tmp_path, capsys):
    r = tmp_path / "r.txt"
    j = tmp_path / "j.txt"
    r.write_text("Python and SQL")
    j.write_text("Python SQL Docker")
    assert main([str(r), str(j), "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["missing_skills"] == ["docker"]


def test_cli_missing_file(capsys):
    assert main(["nope.txt", "nope2.txt"]) == 1

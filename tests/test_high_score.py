from pathlib import Path
import importlib.util


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("flappy", ROOT / "flappy.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_high_score_persists_to_disk(tmp_path, monkeypatch):
    high_score_path = tmp_path / "high_score.txt"
    monkeypatch.setattr(MODULE, "HIGH_SCORE_FILE", str(high_score_path))

    MODULE.save_high_score(12)

    assert MODULE.load_high_score() == 12
    assert high_score_path.read_text(encoding="utf-8").strip() == "12"

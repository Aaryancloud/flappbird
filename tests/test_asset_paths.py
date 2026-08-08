from pathlib import Path
import importlib.util


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("flappy", ROOT / "flappy.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_resolve_asset_path_finds_existing_file():
    path = MODULE.resolve_asset_path("bird.png")
    assert Path(path).exists()

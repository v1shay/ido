import json
from pathlib import Path

from fastapi.testclient import TestClient

from adapters.openscad.adapter import compile_ir_to_scad, validate_scad_source, write_scad
from backend.main import create_app
from backend.providers.fallback import DeterministicProvider
from backend.status import StatusStore
from companion.cli import build_parser
from shared.ir import EngineeringIR


def fixture_ir() -> EngineeringIR:
    path = Path(__file__).parent / "fixtures" / "house_ir.json"
    return EngineeringIR.model_validate_json(path.read_text(encoding="utf-8"))


def test_openscad_compiler_emits_modules_and_root_scene() -> None:
    source = compile_ir_to_scad(fixture_ir())

    assert "module main_body()" in source
    assert "module roof_prism()" in source
    assert "cube([8000, 6000, 4000]" in source
    assert "module ido_scene()" in source
    assert "ido_scene();" in source
    assert validate_scad_source(source) == []


def test_scad_write_is_verified(tmp_path: Path) -> None:
    source = compile_ir_to_scad(fixture_ir())

    path = write_scad(source, tmp_path)

    assert path.name == "ido_current.scad"
    assert path.read_text(encoding="utf-8") == source


def test_openscad_api_returns_source_even_without_cli(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("IDO_OUTPUT_DIR", str(tmp_path))
    client = TestClient(create_app(provider=DeterministicProvider()))

    response = client.post(
        "/api/openscad/prompt",
        json={"prompt": "make a house", "current_ir": None, "export_formats": []},
    )

    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["execution"]["scad_path"].endswith("ido_current.scad")
    assert "module main_body()" in payload["execution"]["scad_source"]
    assert "Stack(" in payload["openui_lang"]
    assert [event["step"] for event in payload["trace"]] == [
        "parse",
        "parse",
        "validate",
        "validate",
        "route",
        "route",
        "execute",
        "execute",
    ]
    assert client.get("/api/status").json()["tool"] == "openscad"


def test_status_store_keeps_recent_errors_bounded() -> None:
    store = StatusStore()
    for index in range(8):
        store.fail(tool="openscad", message=f"failure {index}")

    status = store.get()
    assert status.phase == "failed"
    assert status.recent_errors == [
        "failure 7",
        "failure 6",
        "failure 5",
        "failure 4",
        "failure 3",
    ]


def test_cli_parser_exposes_required_command_shapes() -> None:
    parser = build_parser()

    open_args = parser.parse_args(["open", "blender"])
    prompt_args = parser.parse_args(
        ["prompt", "--tool", "openscad", "make", "a", "bracket"]
    )

    assert open_args.tool == "blender"
    assert prompt_args.tool == "openscad"
    assert " ".join(prompt_args.prompt) == "make a bracket"

from nba_forecast import __version__
from nba_forecast.cli import build_parser


def test_package_has_version() -> None:
    assert __version__ == "0.1.0"


def test_cli_accepts_version_flag(capsys) -> None:
    try:
        build_parser().parse_args(["--version"])
    except SystemExit as error:
        assert error.code == 0

    assert "nba-forecast 0.1.0" in capsys.readouterr().out

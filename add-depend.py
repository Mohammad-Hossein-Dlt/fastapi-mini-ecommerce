#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Iterable, List, Set

# Python 3.11+ has tomllib in stdlib. For 3.10- fallback to 'tomli' if installed.
try:
    import tomllib  # type: ignore[attr-defined]
except ModuleNotFoundError:  # pragma: no cover
    try:
        import tomli as tomllib  # type: ignore
    except ModuleNotFoundError:
        tomllib = None  # we'll guard its usage

base_env = {
    "UV_MANAGED": "false",
    "UV_NO_SYNC_VENV": "true",
    # برای خروجی‌های یکنواخت یونیکدی:
    "PYTHONUTF8": "1",
}

def run_cmd(
    cmd: List[str],
    cwd: Path | None = None,
) -> str:
    
    env = os.environ.copy()
    env.update(base_env)

    proc = subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        env=env,
        capture_output=True,
        text=True,
    )
    
    if proc.returncode != 0:
        print(' '.join(cmd))
        print(proc.stderr.strip())
            
    return proc.stdout


def name_only(
    name: str,
) -> str:
    
    name = name.strip()
    name = re.split(r";", name, 1)[0]
    name = re.split(r"\[", name, 1)[0]
    name = re.split(r"[<>=!~ ]", name, 1)[0]
    result = name.replace("_", "-").lower()
    
    return result

def parse_pyproject_dependencies(
    pyproject_path: Path,
) -> Set[str]:
    
    if not pyproject_path.exists():
        return set()
    if tomllib is None:
        return set()

    data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    deps = [d.strip() for d in data.get("project", {}).get("dependencies", [])]
    return {name_only(d) for d in deps}


def parse_requirements_names(
    req_path: Path,
) -> Set[str]:
    
    if not req_path.exists():
        return set()
    names: Set[str] = set()
    for line in req_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("-r "):
            continue
        names.add(name_only(line))
    return names


def discover_dirs(
    root: Path,
) -> Iterable[Path]:
    
    yield root
    
    for child in root.iterdir():
        if child.is_dir() and (child / "src").is_dir():
            yield child


def ensure_uv_available() -> None:
    if shutil.which("uv") is None:
        raise RuntimeError("Uv is not installed.")


def process(
    dir: Path,
) -> None:

    pyproject = dir / "pyproject.toml"
    requirements = dir / "requirements.txt"
    
    pyproject_exists = pyproject.exists()

    print(str(dir))

    if not pyproject_exists:
        run_cmd(
            cmd=["uv", "init", "--bare", str(dir)],
            cwd=dir,
        )
    
    proc = run_cmd(
        cmd=["uv", "pip", "freeze"],
        cwd=dir,
    )
    
    requirements.write_text(proc, encoding="utf-8")

    run_cmd(
        cmd=["uv", "add", "-r", "requirements.txt", "--active", "--no-sync"],
        cwd=dir,
    )

    deps_set = parse_pyproject_dependencies(pyproject)
    req_names = parse_requirements_names(requirements)
    to_remove = sorted(deps_set - req_names)

    if to_remove:
        print(f"Pruning from pyproject.toml: {' '.join(to_remove)}")
        run_cmd(
            cmd=["uv", "remove", *to_remove, "--active"],
            cwd=dir,
        )
    else:
        print("No package to prune from pyproject.toml.")

    print(f"Process done in {dir.name}")
    
def remove_uv_lock(
    dir: Path,
) -> None:
    uv_lock = dir / "uv.lock"
    
    if uv_lock.exists():
        try:
            uv_lock.unlink()
        except OSError:
            # If file is locked
            uv_lock.chmod(0o666)
            uv_lock.unlink(missing_ok=True)
            
    print(f"uv.lock removed in {dir.name}")
            
def main() -> None:

    ensure_uv_available()

    paths_list = list(discover_dirs(Path.cwd()))

    if not paths_list:
        return

    for path in paths_list:
        try:
            process(path)
            remove_uv_lock(path)
            print()
        except Exception as e:
            raise SystemExit(f"Processing Error for {path.name}:\n{e}\n") from e
    
    remove_uv_lock(Path.cwd())       


if __name__ == "__main__":
    main()

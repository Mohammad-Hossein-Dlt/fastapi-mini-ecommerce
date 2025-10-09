set -e

export UV_MANAGED=false
export UV_NO_SYNC_VENV=true

for dir in */ ; do
  if [ -d "$dir" ]; then
    SRC="$dir/src"
    TOML_FILE="$dir/pyproject.toml"

    if [ -d "$SRC" ]; then
      echo "📦 پوشه $dir دارای requirements.txt است"

      if [ ! -f "$TOML_FILE" ]; then
        echo "🆕 ساختن pyproject.toml در $dir"
        uv init --bare "$dir"
      else
        echo "✅ pyproject.toml در $dir وجود دارد"
      fi
      
      echo "🚀 اجرای uv add -r برای $dir"
      
      cd "$dir"
      uv pip freeze > requirements.txt
      uv add -r requirements.txt --active --no-sync

      EXTRA_PKGS=$(python - <<'PY'
import sys, re, pathlib
try:
    import tomllib
except ModuleNotFoundError:
    print("", end=""); sys.exit(0)

root = pathlib.Path(".")
py = tomllib.loads(root.joinpath("pyproject.toml").read_text(encoding="utf-8"))
deps = [d.strip() for d in py.get("project",{}).get("dependencies",[])]

def name_only(s: str) -> str:
    s=s.strip()
    s=re.split(r";",s,1)[0]
    s=re.split(r"\[",s,1)[0]
    s=re.split(r"[<>=!~ ]",s,1)[0]
    return s.replace("_","-").lower()

deps_set = {name_only(d) for d in deps}

req = root.joinpath("requirements.txt")
if not req.exists():
    print("", end=""); sys.exit(0)

req_names=set()
for line in req.read_text(encoding="utf-8").splitlines():
    line=line.strip()
    if not line or line.startswith("#") or line.startswith("-r "):
        continue
    req_names.add(name_only(line))

extra = sorted(deps_set - req_names)
print(" ".join(extra), end="")
PY
)

      if [ -n "$EXTRA_PKGS" ]; then
        echo "Pruning from pyproject.toml: $EXTRA_PKGS"
        uv remove $EXTRA_PKGS --active
      else
        echo "No extras to prune from pyproject.toml."
      fi

      echo "✅ انجام شد در $dir"
      echo "---------------------------"
      rm -f uv.lock
      cd ..
    fi
  fi
done

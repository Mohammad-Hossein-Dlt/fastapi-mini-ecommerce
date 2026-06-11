from pathlib import Path
import subprocess

path = Path(__file__).parent / "service"

path.mkdir(exist_ok=True)

proto_files = list(Path(path).glob("*.proto"))

def create_command(path: Path):
    return [
        "uv", "run",
        "python", "-m",
        "grpc_tools.protoc",
        "-I./service",
        "--python_out=./service",
        "--grpc_python_out=./service",
        "--mypy_out=./service",
        f"{path.name}"
    ]

def run_cmd(
    cmd: list[str],
    cwd: Path | None = None,
    return_result: bool = False,
) -> str:

    print()
    print(' '.join(cmd))
    print()
    
    if return_result:

        proc = subprocess.Popen(
            cmd,
            cwd=str(cwd) if cwd else None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        
        result, err = proc.communicate()
        
        if err:
            print(err.strip())
                
        return result
    else:
        subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
        )
        
for pf in proto_files:
    run_cmd(create_command(pf))
    
# for pf in proto_files:
#     pf.unlink()

print("All proto files compiled successfully")
from pathlib import Path
import subprocess

rel_path = Path("sharedlib/src/sharedlib/grpc/service")

path = Path(__file__).parent / rel_path

proto_files = list(Path(path).rglob("*.proto"))

def create_command(p: Path):
    
    rp = rel_path / p.parent.relative_to(path)
    
    return [
        "uv", "run",
        "python", "-m",
        "grpc_tools.protoc",
        f"-I./{rp}",
        f"--python_out=./{rp}",
        f"--grpc_python_out=./{rp}",
        f"--mypy_out=./{rp}",
        f"{p.name}"
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

    
print("All proto files compiled successfully")
from pathlib import Path
import sys
from mcp.server.fastmcp import FastMCP

if len(sys.argv) < 2:
    raise RuntimeError("Usage: vault_mcp.py <vault_path>")

ROOT = Path(sys.argv[1]).expanduser().resolve()
if not ROOT.exists():
    raise RuntimeError(f"Vault not found: {ROOT}")

mcp = FastMCP("vault")

@mcp.tool()
def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")

@mcp.tool()
def write(path: str, content: str) -> str:
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return "ok"

@mcp.tool()
def append(path: str, content: str) -> str:
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(content)
    return "ok"

@mcp.tool()
def delete(path: str) -> str:
    p = ROOT / path
    if not p.exists():
        return f"not found: {path}"
    p.unlink()
    return "deleted"

@mcp.tool()
def move(src: str, dst: str) -> str:
    s = ROOT / src
    d = ROOT / dst
    if not s.exists():
        return f"not found: {src}"
    d.parent.mkdir(parents=True, exist_ok=True)
    s.rename(d)
    return f"moved to {dst}"

@mcp.tool()
def list_files(path: str = "") -> str:
    files = [
        str(f.relative_to(ROOT))
        for f in (ROOT / path).rglob("*.md")
    ]
    return "\n".join(files)

@mcp.tool()
def search(text: str) -> str:
    out = []
    for f in ROOT.rglob("*.md"):
        try:
            lines = f.read_text(encoding="utf-8").splitlines()
        except Exception:
            continue
        for i, line in enumerate(lines):
            if text.lower() in line.lower():
                start = max(0, i - 1)
                end = min(len(lines), i + 2)
                snippet = "\n".join(lines[start:end])
                out.append(f"{f.relative_to(ROOT)}:{i+1}\n{snippet}")
    return "\n---\n".join(out) if out else "no results"

if __name__ == "__main__":
    mcp.run()
import json
import sys
from pathlib import Path

ROOT = Path("docs/content")

def convert_nb_to_md(path: Path) -> Path:
    data = json.loads(path.read_text(encoding="utf-8"))
    lang = (
        data.get("metadata", {})
        .get("language_info", {})
        .get("name", "")
    ) or ""
    lines = []
    for cell in data.get("cells", []):
        ctype = cell.get("cell_type")
        source = cell.get("source", [])
        # Ensure list of strings
        if isinstance(source, str):
            src_lines = source.splitlines()
        else:
            src_lines = [s.rstrip("\n\r") for s in source]

        if ctype == "markdown":
            lines.extend(src_lines)
            lines.append("")
        elif ctype == "code":
            lines.append(f"```{lang}")
            lines.extend(src_lines)
            lines.append("```")
            lines.append("")
        else:
            # ignore other cell types
            pass

    md_path = path.with_suffix(".md")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return md_path


def main() -> int:
    if not ROOT.exists():
        print(f"Root path not found: {ROOT}", file=sys.stderr)
        return 1

    files = sorted(ROOT.rglob("*.ipynb"))
    for f in files:
        out = convert_nb_to_md(f)
        print(f"Wrote {out}")
    print(f"Converted {len(files)} notebook(s) to Markdown.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


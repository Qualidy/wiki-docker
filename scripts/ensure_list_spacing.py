from __future__ import annotations

from pathlib import Path


MD_ROOT = Path("docs")
TASKS_ROOT = Path("tasks")


LIST_PREFIXES = ("- ", "* ", "+ ")


def fix_markdown(path: Path) -> bool:
    lines = path.read_text(encoding="utf-8").splitlines()
    out: list[str] = []
    changed = False
    in_fence = False
    fence_tick = ""  # stores ``` or ~~~ when in fence

    for i, line in enumerate(lines):
        stripped = line.lstrip()
        # toggle fence
        if stripped.startswith("```") or stripped.startswith("~~~"):
            if not in_fence:
                in_fence = True
                fence_tick = stripped[:3]
            else:
                if stripped.startswith(fence_tick):
                    in_fence = False
                    fence_tick = ""
        # insert blank line if a list starts after non-empty previous line
        if (
            not in_fence
            and (stripped.startswith(LIST_PREFIXES) or stripped[:3].isdigit() and stripped[2:3] == "." or stripped[:4].isdigit() and stripped[3:4] == ".")
        ):
            if out and out[-1].strip() != "":
                out.append("")
                changed = True
        out.append(line)

    if changed:
        path.write_text("\n".join(out) + "\n", encoding="utf-8")
    return changed


def fix_yaml_block_scalars(path: Path) -> bool:
    # Only manipulate lines inside block scalars (question: | or solution: |)
    lines = path.read_text(encoding="utf-8").splitlines()
    out: list[str] = []
    changed = False
    in_block = False
    block_indent = 0
    in_fence = False
    fence_tick = ""

    def is_list_start(s: str) -> bool:
        s2 = s.lstrip()
        if s2.startswith(LIST_PREFIXES):
            return True
        # simple ordered list detection (e.g., "1. ")
        # allow up to two digits for simplicity
        if len(s2) >= 3 and s2[0].isdigit() and s2[1:2] == ".":
            return True
        if len(s2) >= 4 and s2[0].isdigit() and s2[1].isdigit() and s2[2:3] == ".":
            return True
        return False

    i = 0
    while i < len(lines):
        line = lines[i]
        out.append(line)

        # Detect start of block scalar for question/solution keys
        if not in_block:
            # Match patterns like "question: |" or "solution: |" possibly with extra spaces
            stripped = line.strip().lower()
            if stripped.startswith("question:") or stripped.startswith("solution:"):
                if "|" in line or ">" in line:
                    in_block = True
                    # indentation is number of leading spaces of next content line
                    # next line may be blank; determine indent when encountering a non-empty line
                    block_indent = None  # type: ignore
        else:
            # determine block indent if not yet known
            if block_indent is None:  # type: ignore
                # Peek next non-empty line to set indent baseline
                pass
            # exit block when dedent occurs (line shorter indent than first block content)
            if line.strip() == "":
                # Blank lines are part of block
                i += 1
                continue
            # If this line is a fence marker, toggle fence state
            content = line
            # calculate current indent
            current_indent = len(content) - len(content.lstrip(" "))
            # Establish block indent at first non-empty content line after block start
            if block_indent is None:  # type: ignore
                block_indent = current_indent  # type: ignore

            # If dedent below initial block indent, block ends
            if current_indent < block_indent:  # type: ignore
                in_block = False
                block_indent = 0
                in_fence = False
                fence_tick = ""
                # continue without special handling
            else:
                inner = content[block_indent:]  # type: ignore
                stripped_inner = inner.lstrip()
                # toggle fence markers
                if stripped_inner.startswith("```") or stripped_inner.startswith("~~~"):
                    if not in_fence:
                        in_fence = True
                        fence_tick = stripped_inner[:3]
                    else:
                        if stripped_inner.startswith(fence_tick):
                            in_fence = False
                            fence_tick = ""
                # If a list starts and previous logical line inside block isn't blank, insert a blank line
                if not in_fence and is_list_start(inner):
                    # Check the previous emitted line in out
                    if len(out) >= 2:
                        prev = out[-2]
                        if prev.strip() != "":
                            # insert a blank line with proper indentation
                            indent_spaces = " " * block_indent
                            out.insert(len(out) - 1, indent_spaces)
                            changed = True
        i += 1

    if changed:
        path.write_text("\n".join(out) + "\n", encoding="utf-8")
    return changed


def main() -> None:
    changed_files = []
    # Process Markdown files
    for md in MD_ROOT.rglob("*.md"):
        if fix_markdown(md):
            changed_files.append(str(md))

    # Process YAML task files
    if TASKS_ROOT.exists():
        for yml in TASKS_ROOT.rglob("*.yaml"):
            if fix_yaml_block_scalars(yml):
                changed_files.append(str(yml))

    if changed_files:
        print("Updated:")
        for p in changed_files:
            print(" -", p)
    else:
        print("No changes needed.")


if __name__ == "__main__":
    main()


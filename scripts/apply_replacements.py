from pathlib import Path

ROOTS = [Path("docs"), Path("tasks")]

replacements = [
    ("Diennst", "Dienst"),
    ("Luste", "Liste"),
    ("dürfe nun", "dürfte nun"),
    ("zur Verfügung Außerdem", "zur Verfügung. Außerdem"),
    ("öfnnen", "öffnen"),
    ("Palatre", "Palette"),
    ("wechselt zum", "wechseln zum"),
    ("ncihts", "nichts"),
    ("mometan", "momentan"),
    ("akuellen", "aktuellen"),
    ("Ordnet", "Ordner"),
    # targeted phrase instead of generic "teht" to avoid corrupting "steht/besteht/entsteht"
    ("- `-t` teht für", "- `-t` steht für"),
    ("Effizeintere Nuzung", "Effizientere Nutzung"),
    ("Starten/Stopen", "Starten/Stoppen"),
    ("Hoche Isolation", "Hohe Isolation"),
    ("Idela für", "Ideal für"),
    ("teil aber den Kernel", "teilt aber den Kernel"),
    # revert unintended prior replacements if any
    ("ssteht", "steht"),
    ("bessteht", "besteht"),
    ("entssteht", "entsteht"),
    ("verssteht", "versteht"),
]


def apply_to_file(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    text = original
    for old, new in replacements:
        text = text.replace(old, new)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = []
    for root in ROOTS:
        if not root.exists():
            continue
        for p in root.rglob("*.md"):
            if apply_to_file(p):
                changed.append(str(p))
        for p in root.rglob("*.yaml"):
            if apply_to_file(p):
                changed.append(str(p))
    if changed:
        print("Changed:")
        for c in changed:
            print(" -", c)
    else:
        print("No changes.")


if __name__ == "__main__":
    main()

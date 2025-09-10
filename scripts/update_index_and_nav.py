from pathlib import Path

INDEX = Path("docs/index.md")
MKDOCS = Path("mkdocs.yml")

ICON_MAP = {
    "content/intro_docker.md": ":material-docker: Einführung in Docker",
    "content/docker_windows_installation.md": ":material-microsoft-windows: Installation auf Windows",
    "content/containers_vs_images.md": ":material-cube-outline: Container vs. Images",
    "content/port_mapping.md": ":material-lan: Port Mapping in Docker",
    "content/container_background_run.md": ":material-play-circle-outline: Container im Hintergrund ausführen",
    "content/tagging.md": ":material-tag-outline: Tagging von Docker-Images",
    "assignments/1_aufgabe.yaml": ":material-clipboard-check-outline: 1. Übung",
    "content/runtimes.md": ":material-engine-outline: Docker Runtimes",
    "content/slim_alpine_images.md": ":material-pine-tree: Slim- und Alpine-Images",
    "content/persistence.md": ":material-database-outline: Datenpersistenz in Docker",
    "content/custom_images.md": ":material-hammer-wrench: Eigene Docker-Images erstellen - Einstieg",
    "content/layers.md": ":material-layers-outline: Docker Layers",
    "content/custom_images_01.md": ":material-hammer-screwdriver: Eigene Docker-Images erstellen - Erweitert",
}


def update_index_icons() -> None:
    text = INDEX.read_text(encoding="utf-8")
    lines = text.splitlines()

    # Find the cards block boundaries to limit replacements
    try:
        start = next(i for i, l in enumerate(lines) if '<div class="grid cards fancy" markdown>' in l)
    except StopIteration:
        start = 0
    try:
        end = start + 1 + next(i for i, l in enumerate(lines[start + 1 :], start=0) if '</div>' in l)
    except StopIteration:
        end = len(lines)

    for i in range(start, end):
        line = lines[i]
        if line.strip().startswith("-") and "](" in line:
            # Extract target path
            try:
                path = line.split("](", 1)[1].split(")", 1)[0]
            except Exception:
                continue
            label = ICON_MAP.get(path)
            if label:
                lines[i] = f"- [ {label} ]({path})"

    INDEX.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_nav() -> None:
    yml = MKDOCS.read_text(encoding="utf-8").splitlines()
    try:
        nav_idx = next(i for i, l in enumerate(yml) if l.strip() == "nav:")
    except StopIteration:
        # Insert nav at top if missing
        nav_idx = 1
        yml.insert(nav_idx, "nav:")

    # Find where nav block ends (before next top-level key like 'theme:')
    end_idx = None
    for i in range(nav_idx + 1, len(yml)):
        if yml[i] and not yml[i].startswith(" "):
            end_idx = i
            break
    if end_idx is None:
        end_idx = len(yml)

    # Build new nav entries; include only files that exist
    def exists(p: str) -> bool:
        return Path(p).exists()

    nav_lines = [
        "  - Übersicht: index.md",
        "  - Topic 1: content/1.md",
    ]
    nav_map = {
        "Einführung in Docker": "content/intro_docker.md",
        "Installation auf Windows": "content/docker_windows_installation.md",
        "Container vs. Images": "content/containers_vs_images.md",
        "Port Mapping in Docker": "content/port_mapping.md",
        "Container im Hintergrund ausführen": "content/container_background_run.md",
        "Tagging von Docker-Images": "content/tagging.md",
        "Docker Runtimes": "content/runtimes.md",
        "Slim- und Alpine-Images": "content/slim_alpine_images.md",
        "Datenpersistenz in Docker": "content/persistence.md",
        "Eigene Docker-Images erstellen - Einstieg": "content/custom_images.md",
        "Docker Layers": "content/layers.md",
        "Eigene Docker-Images erstellen - Erweitert": "content/custom_images_01.md",
        # assignments file omitted if missing
    }
    for title, path in nav_map.items():
        if exists(Path("docs") / path):
            nav_lines.append(f"  - {title}: {path}")

    # Replace nav block
    new_yml = yml[: nav_idx + 1] + nav_lines + yml[end_idx:]
    MKDOCS.write_text("\n".join(new_yml) + "\n", encoding="utf-8")


if __name__ == "__main__":
    update_index_icons()
    update_nav()
    print("Updated index icons and mkdocs nav.")


from pathlib import Path

P = Path("docs/content/intro_docker.md")

def wrap_prev_with_image(lines, img_rel_path, width="70%"):
    """Find an image line and wrap the previous non-empty line + this image into a grid."""
    for i, ln in enumerate(lines):
        if ln.strip() == f"![]({img_rel_path})":
            # find previous non-empty line
            j = i - 1
            while j >= 0 and not lines[j].strip():
                j -= 1
            if j >= 0:
                text = lines[j]
                grid = [
                    '<div class="grid" markdown>',
                    '',
                    '<div markdown>',
                    text,
                    '',
                    '</div>',
                    '',
                    '<div markdown>',
                    f'![]({img_rel_path})' + f'{{ width="{width}" }}',
                    '',
                    '</div>',
                    '',
                    '</div>',
                    '',
                ]
                # replace j..i with grid
                return lines[:j] + grid + lines[i + 1 :]
    return lines


def wrap_image_with_caption(lines, img_rel_path, caption, width="70%"):
    """Replace a bare image with a grid (caption left, image right)."""
    for i, ln in enumerate(lines):
        if ln.strip() == f"![]({img_rel_path})":
            grid = [
                '<div class="grid" markdown>',
                '',
                '<div markdown>',
                caption,
                '',
                '</div>',
                '',
                '<div markdown>',
                f'![]({img_rel_path})' + f'{{ width="{width}" }}',
                '',
                '</div>',
                '',
                '</div>',
                '',
            ]
            return lines[:i] + grid + lines[i + 1 :]
    return lines


def main():
    text = P.read_text(encoding="utf-8")
    lines = text.splitlines()

    # 1) Datacenter photo: reuse preceding sentence
    lines = wrap_prev_with_image(lines, "../assets/docker_02.jpg", width="70%")

    # 2) Emulator illustration: add compact caption
    lines = wrap_image_with_caption(
        lines,
        "../assets/docker_04.png",
        "**Emulator-Illustration:** Software ahmt Hardware nach, Programme laufen in einer simulierten Umgebung.",
        width="70%",
    )

    # 3) Hypervisor diagram: compact caption
    lines = wrap_image_with_caption(
        lines,
        "../assets/docker_05.png",
        "**Hypervisor:** Teilt Ressourcen des Host-Servers auf mehrere isolierte VMs auf.",
        width="70%",
    )

    P.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("intro_docker.md: applied grid wrappers for selected images.")


if __name__ == "__main__":
    main()


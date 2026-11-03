#!/usr/bin/env python3
"""Apply experience-patch.md to your portfolio HTML.

Usage:  python apply_patch.py path/to/index.html [path/to/experience-patch.md]
Keeps a backup next to the file as <name>.bak
"""
import re, sys, shutil, pathlib

html_path = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "index.html")
patch_path = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "experience-patch.md")

src = html_path.read_text(encoding="utf-8")
patch = patch_path.read_text(encoding="utf-8")
blocks = re.findall(r"```(\w+)\n(.*?)```", patch, re.S)
css = next(b for l, b in blocks if l == "css")
html_blocks = [b for l, b in blocks if l == "html"]
stage_html, home_line = html_blocks[0], html_blocks[1]
js = next(b for l, b in blocks if l == "js")

shutil.copy(html_path, str(html_path) + ".bak")

# 1. CSS: swap old carousel block (up to the EDUCATION css) for the new one
src, n = re.subn(r"/\* EXPERIENCE — rotating carousel \*/.*?(?=/\* EDUCATION \*/)",
                 lambda m: css.rstrip() + "\n\n", src, count=1, flags=re.S)
assert n == 1, "CSS block not found"

# 2. HTML: keep slides 1-3, drop clones/buttons/dots, add stage + CERN card
m = re.search(r"<!-- SLIDE 1 — SelfShft -->(.*?)<!-- clone of first slide", src, re.S)
assert m, "Existing slides not found"
slides = "<!-- SLIDE 1 — SelfShft -->" + m.group(1).rstrip()
slides = slides.rstrip() + "\n"
placeholders = re.compile(r"\s*<!-- SLIDE 1 — SelfShft.*?-->\s*<!-- SLIDE 2.*?-->\s*<!-- SLIDE 3.*?-->", re.S)
new_stage = placeholders.sub(lambda _: "\n    " + slides, stage_html, count=1)
src, n = re.subn(r'<div class="exp-carousel reveal-item" id="expCarousel">.*?<div class="exp-dots" id="expDots">.*?</div>\s*</div>\s*</div>',
                 lambda m: new_stage.strip(), src, count=1, flags=re.S)
assert n == 1, "Carousel markup not found"

# 3. JS
src, n = re.subn(r"// ── Experience carousel \(rotating loop\).*?(?=</script>)",
                 lambda m: "// ── Experience: auto-rotating stacked deck ─────────────\n" +
                           js.split("\n", 1)[1].rstrip() + "\n", src, count=1, flags=re.S)
assert n == 1, "Carousel JS not found"

# 4. Home line about CERN
marker = '<a href="#contact" class="connect-link'
assert marker in src, "Connect link not found"
src = src.replace(marker, home_line.strip() + "\n      " + marker, 1)

html_path.write_text(src, encoding="utf-8")
print("Done. Backup saved as", str(html_path) + ".bak")
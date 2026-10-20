"""Check the local pilot's HTML targets, fragment IDs, and JavaScript syntax."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.targets = []
        self.duplicates = []
        self.scripts = []
        self.current_script = None

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if "id" in attrs:
            if attrs["id"] in self.ids:
                self.duplicates.append(attrs["id"])
            self.ids.add(attrs["id"])
        for name in ("href", "src"):
            if name in attrs:
                self.targets.append(attrs[name])
        if tag == "script" and "src" not in attrs:
            self.current_script = []

    def handle_data(self, data):
        if self.current_script is not None:
            self.current_script.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self.current_script is not None:
            self.scripts.append("".join(self.current_script))
            self.current_script = None


def main():
    pages, errors = {}, []
    for path in sorted(ROOT.rglob("*.html")):
        page = Page()
        page.feed(path.read_text())
        pages[path] = page
        errors.extend(f"{path.relative_to(ROOT)}: duplicate ID {value}" for value in page.duplicates)
    target_count = 0
    for path, page in pages.items():
        for value in page.targets:
            url = urlsplit(value)
            if url.scheme or url.netloc:
                continue
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            target_count += 1
            if not target.exists():
                errors.append(f"{path.relative_to(ROOT)}: missing {value}")
            elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                errors.append(f"{path.relative_to(ROOT)}: missing fragment {value}")
    node = shutil.which("node")
    checked_js = 0
    if node:
        for path in sorted(ROOT.rglob("*.js")):
            result = subprocess.run([node, "--check", str(path)], capture_output=True, text=True)
            checked_js += 1
            if result.returncode:
                errors.append(result.stderr)
        for path, page in pages.items():
            for script in page.scripts:
                result = subprocess.run([node, "--check"], input=script, capture_output=True, text=True)
                checked_js += 1
                if result.returncode:
                    errors.append(f"{path.relative_to(ROOT)}: {result.stderr}")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"OK: {len(pages)} HTML pages; {target_count} local links/fragments; {checked_js} JavaScript syntax checks.")
    if not node:
        print("Node.js unavailable: JavaScript syntax not checked.")


if __name__ == "__main__":
    main()

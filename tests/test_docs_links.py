import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DocsLinksTest(unittest.TestCase):
    def test_lab_concept_links_point_to_existing_anchors(self) -> None:
        concepts = (ROOT / "docs" / "concepts.md").read_text(encoding="utf-8")
        anchors = {_github_anchor(match.group(1)) for match in re.finditer(r"^##\s+(.+)$", concepts, re.MULTILINE)}

        links: list[str] = []
        for readme in (ROOT / "labs").glob("week*/README.md"):
            text = readme.read_text(encoding="utf-8")
            links.extend(re.findall(r"\.\./\.\./docs/concepts\.md#([a-z0-9-]+)", text))

        self.assertTrue(links)
        missing = sorted(set(links) - anchors)
        self.assertEqual(missing, [])


def _github_anchor(heading: str) -> str:
    lowered = heading.strip().lower()
    without_punctuation = re.sub(r"[^\w\s-]", "", lowered)
    return without_punctuation.replace(" ", "-")


if __name__ == "__main__":
    unittest.main()

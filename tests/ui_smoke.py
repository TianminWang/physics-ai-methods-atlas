"""Headless browser smoke test of real-data v0.5 prototype; screenshots for review.

Run after:
    python -m scripts.build_prototype --site build/prototype
    python -m pip install playwright
    python -m playwright install chromium
    python tests/ui_smoke.py
"""
from __future__ import annotations

import re
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "build" / "prototype" / "index.html"
SCREENSHOTS = ROOT / "build" / "prototype-screenshots"


def main() -> None:
    if not SITE.exists():
        raise RuntimeError("Preview not built: python -m scripts.build_prototype --site build/prototype")
    SCREENSHOTS.mkdir(parents=True, exist_ok=True)
    errors = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.goto(SITE.resolve().as_uri(), wait_until="load")
        page.wait_for_selector(".graph-node")
        assert page.locator(".stage").count() == 6
        assert page.locator("#tracks button").count() == 3
        assert page.locator(".graph-node").count() >= 7
        assert page.locator(".graph-edge-btn").count() >= 4
        assert page.locator("#show-all").is_checked() is False
        assert "研究" in page.locator("#page-title").inner_text()

        # A real node exposes optional reading and authorial source links.
        page.locator('.graph-node[title*="FNO"]').first.click()
        assert "优先阅读" in page.locator("#detail-content").inner_text()
        assert page.locator("#detail-content a[href^='https://']").count() >= 1
        page.screenshot(path=str(SCREENSHOTS / "operator-desktop-zh.png"), full_page=True)
        # Expand the branch and verify the same method is not duplicated.
        compact_count=page.locator(".graph-node").count()
        page.locator("#show-all").check()
        assert page.locator(".graph-node").count()>compact_count
        ids=page.locator(".graph-node").evaluate_all(
            "nodes => nodes.map(n => n.title)"
        )
        assert len(ids)==len(set(ids))
        page.screenshot(path=str(SCREENSHOTS / "operator-expanded-zh.png"), full_page=True)
        page.locator("#show-all").uncheck()

        # A genuine evolution edge exposes its methodological improvement and bottleneck.
        page.locator('.graph-edge-btn[aria-label*="FNO"][aria-label*="PINO"]').first.click()
        assert "→" in page.locator("#detail-content h3").inner_text()
        assert "针对的技术瓶颈" in page.locator("#detail-content").inner_text()
        assert "证据论文" in page.locator("#detail-content").inner_text()
        assert page.locator("#detail-content a[href^='https://']").count() >= 1

        # Stage selection must visually identify a research capability.
        # Zoom controls must change and restore actual graph transforms.
        initial_transform=page.locator("#diagram").get_attribute("style")
        page.locator("#zoom-in").click()
        assert page.locator("#diagram").get_attribute("style") != initial_transform
        page.locator("#fit-view").click()

        page.locator("#stages .stage").nth(2).click()
        assert page.locator("#stages .stage[aria-pressed='true']").count() == 1

        # English and generated family views share node IDs and functional data.
        page.locator("#lang-toggle").click()
        assert "research" in page.locator("#page-title").inner_text().lower()
        assert page.locator(".graph-node").count() >= 7
        page.screenshot(path=str(SCREENSHOTS / "operator-desktop-en.png"), full_page=True)

        # Generative case includes a different scientific lineage and explicit search.
        page.locator("#tracks .tab").nth(2).click()
        page.locator("#search").fill("DPS")
        assert page.locator(".graph-node:not(.dimmed)").count() >= 1
        page.locator("#search").fill("")
        assert page.locator(".graph-node").count() >= 7
        page.screenshot(path=str(SCREENSHOTS / "generative-desktop-en.png"), full_page=True)

        # Mobile layout must remain functional without page-wide overflow.
        page.set_viewport_size({"width": 390, "height": 844})
        page.locator("#lang-toggle").click()
        assert "研究" in page.locator("#page-title").inner_text()
        page.screenshot(path=str(SCREENSHOTS / "generative-mobile-zh.png"), full_page=True)
        overflowing = page.evaluate(
            "() => document.documentElement.scrollWidth - document.documentElement.clientWidth"
        )
        assert overflowing <= 4, f"Mobile page overflows viewport by {overflowing}px"

        assert errors == [], f"Browser JavaScript errors: {errors}"
        browser.close()
    print("Browser smoke tests passed; screenshots saved:", SCREENSHOTS)


if __name__ == "__main__":
    main()

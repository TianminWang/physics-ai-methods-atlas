"""Real-browser tests for the v0.8 full-width scientific DAG and evidence drawer."""
from __future__ import annotations

import json
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "build" / "viewer-v08" / "index.html"
SCREENSHOTS = ROOT / "build" / "v08-screenshots"


def main() -> None:
    assert PAGE.exists(), "Run: python -m scripts.build_v08 --site build/viewer-v08"
    SCREENSHOTS.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_page(viewport={"width": 1520, "height": 980}, device_scale_factor=1)
        errors: list[str] = []
        page.on("pageerror", lambda exc: errors.append(str(exc)))
        page.goto(PAGE.resolve().as_uri(), wait_until="load")
        page.wait_for_selector('g.atlas-node[data-method-id]', timeout=25000)
        data = json.loads(page.locator("#atlas-data").text_content())
        assert len(data["phases"]) == 3
        assert page.locator(".phase-card").count() == 3
        assert len(data["methods"]) == 61
        assert page.locator("g.atlas-node").count() == data["summary"]["core_methods"]
        assert page.locator("g.atlas-node").count() < len(data["methods"])
        assert page.locator(".component-chip").count() == data["summary"]["evolution_components"]
        assert page.locator("#drawer").is_hidden()

        # The canvas must have nearly the whole available page width, and
        # must be much taller than v0.7's old fixed-size 2/3-width viewer.
        viewport = page.locator("#viewport").bounding_box()
        assert viewport is not None
        assert viewport["width"] >= 0.90 * page.viewport_size["width"]
        assert viewport["height"] >= 680
        assert page.locator("#mini-canvas").is_visible()
        page.screenshot(path=str(SCREENSHOTS / "01-fullwidth-global-zh.png"), full_page=True)

        # Picking a research phase should dim unrelated nodes, not hide them.
        page.locator('.phase-card[data-phase-id="inference"]').click()
        assert page.locator(".mapping-card").count() >= 3
        assert page.locator("g.atlas-node").count() == data["summary"]["core_methods"]
        assert page.locator("g.atlas-node.dimmed").count() >= 1
        page.screenshot(path=str(SCREENSHOTS / "02-inference-phase-zh.png"), full_page=True)

        # Selecting an edge opens a real evidence drawer with both endpoints.
        edge = page.locator('g.atlas-edge[data-edge-id="relation.pino--extends--fno"]')
        assert edge.count() == 1
        edge.evaluate("(el) => el.dispatchEvent(new MouseEvent('click',{bubbles:true}))")
        assert page.locator("#drawer").is_visible()
        details = page.locator("#details-body").inner_text()
        assert "技术变化" in details
        assert "针对的技术瓶颈" in details
        assert "支持论文" in details
        assert page.locator("g.atlas-node.selected").count() == 2
        assert page.locator("g.atlas-edge.selected").count() == 1
        page.locator("#lineage-focus").click()
        assert page.locator("g.atlas-node.primary, g.atlas-node.selected").count() >= 2
        page.screenshot(path=str(SCREENSHOTS / "03-evolution-edge-drawer.png"), full_page=True)

        # Docking the details must be optional; closing restores full width.
        page.locator("#pin-drawer").click()
        assert page.locator("#graph-layout.is-pinned").count() == 1
        assert page.locator("#pin-drawer").get_attribute("aria-pressed") == "true"
        page.screenshot(path=str(SCREENSHOTS / "04-pinned-detail-panel.png"), full_page=True)
        page.locator("#close-drawer").click()
        assert page.locator("#drawer").is_hidden()
        assert page.locator("#graph-layout.is-pinned").count() == 0

        # Unlinked methods remain available without any invented evolution edge.
        page.locator("#toggle-unlinked").click()
        assert page.locator("#toggle-unlinked").get_attribute("aria-expanded") == "true"
        assert page.locator(".unlinked-item").count() == data["summary"]["unlinked_methods"]
        isolated = data["unlinked_method_ids"][0]
        item = page.locator(".unlinked-item").filter(
            has=page.locator("span")
        ).first
        assert item.count() == 1
        item.click()
        assert page.locator("#drawer").is_visible()
        assert "暂无已记录" in page.locator("#details-body").inner_text()
        page.screenshot(path=str(SCREENSHOTS / "05-unlinked-methods-shelf.png"), full_page=True)
        page.locator("#close-drawer").click()

        # Search covers all canonical methods, including those not in main SVG.
        page.locator("#search").fill(isolated)
        assert page.locator("#search-results .search-result[data-method-id]").count() >= 1
        page.locator("#search-results .search-result[data-method-id]").first.click()
        assert page.locator("#drawer").is_visible()
        page.locator("#close-drawer").click()
        page.locator("#search").fill("")

        # Minimap is a true viewport navigation tool, not a decorative image.
        page.locator("#fit-all").click()
        before = page.locator("#board").get_attribute("style")
        page.locator("#mini-canvas").click(position={"x":20, "y":18})
        after = page.locator("#board").get_attribute("style")
        assert after != before
        page.locator("#hide-mini").click()
        assert page.locator("#mini").is_hidden()
        page.locator("#restore-mini").click()
        assert page.locator("#mini").is_visible()

        # Fullscreen is a true full-window canvas, with an exit control.
        page.locator("#fullscreen").click()
        assert page.locator("#graph-card.is-fullscreen").count() == 1
        large = page.locator("#viewport").bounding_box()
        assert large is not None and large["width"] > 0.90 * page.viewport_size["width"]
        assert large["height"] > 0.65 * page.viewport_size["height"]
        page.screenshot(path=str(SCREENSHOTS / "06-fullscreen-dag.png"), full_page=True)
        page.locator("#fullscreen").click()
        assert page.locator("#graph-card.is-fullscreen").count() == 0

        # All scholarly nodes and references remain stable after language toggle.
        page.locator("#language").click()
        assert "Understand" in page.locator(".intro h1").inner_text()
        assert page.locator("g.atlas-node").count() == data["summary"]["core_methods"]
        page.screenshot(path=str(SCREENSHOTS / "07-global-english.png"), full_page=True)
        assert errors == [], "Desktop browser errors: " + repr(errors)

        # Mobile must have no document-wide overflow; pan/inspect still works.
        mobile = browser.new_page(viewport={"width":390, "height":844}, device_scale_factor=1)
        mobile_errors: list[str] = []
        mobile.on("pageerror", lambda exc: mobile_errors.append(str(exc)))
        mobile.goto(PAGE.resolve().as_uri(), wait_until="load")
        mobile.wait_for_selector("g.atlas-node")
        assert mobile.locator(".phase-card").count() == 3
        assert mobile.locator("#mini-canvas").is_visible()
        mobile.screenshot(path=str(SCREENSHOTS / "08-mobile-zh.png"), full_page=True)
        overflow = mobile.evaluate(
            "() => document.documentElement.scrollWidth-document.documentElement.clientWidth"
        )
        assert overflow <= 4, "Mobile document overflow: " + str(overflow)
        mobile.locator('g.atlas-node[data-method-id]').first.evaluate(
            "(el) => el.dispatchEvent(new MouseEvent('click',{bubbles:true}))"
        )
        assert mobile.locator("#drawer").is_visible()
        assert mobile_errors == [], "Mobile browser errors: " + repr(mobile_errors)
        browser.close()
    print("v0.8 full-width DAG UI test passed. Screenshots:", SCREENSHOTS)


if __name__ == "__main__":
    main()

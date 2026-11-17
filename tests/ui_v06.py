"""Playwright smoke/visual review for the single-graph v0.6 offline viewer."""
from __future__ import annotations

import os
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "build" / "viewer-v06" / "index.html"
SHOTS = ROOT / "build" / "v06-screenshots"


def test_page(page, errors):
    page.goto(HTML.resolve().as_uri(), wait_until="load")
    page.wait_for_selector(".method-node", timeout=20000)
    assert page.locator(".stage-card").count() == 6
    assert page.locator(".zone-panel").count() == 6
    assert page.locator(".method-node").count() >= 18
    assert page.locator(".role-card").count() >= 6, "stage→family mappings must be visible"
    assert page.locator(".stage-card[aria-pressed='true']").count() == 1
    assert page.locator(".method-node.dimmed").count() >= 1, "non-stage methods must fade, not disappear"
    assert "反演" in page.locator("#source-stage-name").inner_text()

    page.screenshot(path=str(SHOTS / "01-unified-stage-inverse-zh.png"), full_page=True)

    # Selecting the family/method role exposes its original functional explanation.
    page.locator(".role-card").first.click()
    panel = page.locator("#inspect").inner_text()
    assert ("功能" in panel or "研究环节" in panel)
    assert "→" in page.locator("#inspect h3").inner_text()
    page.screenshot(path=str(SHOTS / "02-stage-to-method-role-zh.png"), full_page=True)

    # A new stage changes the mapping without navigating to a separate graph.
    first_count = page.locator(".zone-panel").count()
    page.locator('.stage-card[data-stage-id="stage.physics-forward"]').click()
    assert page.locator(".zone-panel").count() == first_count
    assert "正向模拟" in page.locator("#source-stage-name").inner_text()
    assert page.locator(".role-card").count() > 0

    # Query all canonical methods even when their zone is collapsed.
    page.locator("#search").fill("FNO")
    node = page.locator('.method-node[data-method-id="method.fno"]')
    assert node.count() == 1
    node.click()
    panel = page.locator("#inspect").inner_text()
    assert "傅里叶神经算子" in panel
    assert "优先阅读" in panel
    assert page.locator("#inspect a[href^='https://']").count() >= 1

    page.locator("#search").fill("")
    # Expand all methods within the SAME graph, not a separate tree page.
    page.locator("#toggle-all").click()
    assert page.locator(".method-node").count() >= 61
    ids = page.locator(".method-node").evaluate_all(
        "els => els.map(x => x.dataset.methodId)"
    )
    assert len(ids) == len(set(ids)) == 61
    assert page.locator(".zone-panel").count() == 6
    page.screenshot(path=str(SHOTS / "03-all-methods-zh.png"), full_page=True)

    # Method evolution must show the actual bottleneck and literature.
    page.locator('.edge-hit[data-edge-id="relation.pino--extends--fno"]').first.evaluate(
        "(el) => el.dispatchEvent(new MouseEvent('click', {bubbles:true}))"
    )
    details = page.locator("#inspect").inner_text()
    assert "技术变化" in details
    assert "针对的瓶颈" in details
    assert "证据论文" in details

    # Both zoom/pan and translation must operate without rebuilding graph records.
    previous = page.locator("#scene").get_attribute("style")
    page.locator("#zoom-plus").click()
    assert page.locator("#scene").get_attribute("style") != previous
    page.locator("#lang").click()
    assert "workflow" in page.locator(".hero p").inner_text().lower() or "stage" in page.locator(".hero p").inner_text().lower()
    assert page.locator(".method-node").count() == 61
    page.screenshot(path=str(SHOTS / "04-all-methods-en.png"), full_page=True)
    assert not errors, f"Browser console errors: {errors}"


def main():
    if not HTML.exists():
        raise RuntimeError("Run python -m scripts.build_v06 --site build/viewer-v06 first")
    SHOTS.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        desktop = browser.new_page(viewport={"width": 1480, "height": 960}, device_scale_factor=1)
        errors = []
        desktop.on("pageerror", lambda error: errors.append(str(error)))
        test_page(desktop, errors)
        mobile = browser.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=1)
        mobile_errors=[]
        mobile.on("pageerror", lambda error: mobile_errors.append(str(error)))
        mobile.goto(HTML.resolve().as_uri(), wait_until="load")
        mobile.wait_for_selector(".method-node")
        assert mobile.locator(".stage-card").count()==6
        assert mobile.locator(".zone-panel").count()==6
        mobile.screenshot(path=str(SHOTS / "05-mobile-zh.png"), full_page=True)
        overflow=mobile.evaluate(
            "() => document.documentElement.scrollWidth-document.documentElement.clientWidth"
        )
        assert overflow <= 4, f"Mobile document overflows by {overflow}px"
        assert not mobile_errors, mobile_errors
        browser.close()
    print("Unified v0.6 Chromium smoke checks passed; screenshots:", SHOTS)


if __name__ == "__main__":
    main()

"""Chromium interactions and visual checks for the three-phase global method DAG."""
from __future__ import annotations

from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
HTML=ROOT/"build"/"viewer-v07"/"index.html"
SHOTS=ROOT/"build"/"v07-screenshots"


def run():
    assert HTML.exists(), "First run: python -m scripts.build_v07 --site build/viewer-v07"
    SHOTS.mkdir(parents=True,exist_ok=True)
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,args=["--no-sandbox"])
        page=browser.new_page(viewport={"width":1440,"height":960},device_scale_factor=1)
        errors=[]
        page.on("pageerror",lambda e:errors.append(str(e)))
        page.goto(HTML.resolve().as_uri(),wait_until="load")
        page.wait_for_selector('g.atlas-node[data-method-id="method.fno"]',timeout=15000)
        assert page.locator(".phase-card").count()==3
        assert page.locator('.phase-card[aria-pressed="true"]').count()==1
        assert page.locator("g.atlas-node").count()==61
        assert page.locator("g.atlas-edge").count()>=31
        assert page.locator(".paradigm-pill").count()==5
        assert page.locator(".mapping-card").count()>3
        assert page.locator("g.atlas-node.dimmed").count()>0
        # Initial stage-II view and graph are retained simultaneously.
        assert "反问题" in page.locator("#dag-title").inner_text() or "方法" in page.locator("#dag-title").inner_text()
        page.screenshot(path=str(SHOTS/"01-dag-inference-zh.png"),full_page=True)

        # The phase filter never swaps the graph or duplicates methods.
        page.locator('.phase-card[data-phase-id="modeling"]').click()
        assert page.locator("g.atlas-node").count()==61
        assert page.locator('.phase-card[data-phase-id="modeling"]').get_attribute("aria-pressed")=="true"
        assert page.locator(".mapping-card").count()>2
        page.screenshot(path=str(SHOTS/"02-dag-modeling-zh.png"),full_page=True)

        # Method node and science-paper link inspection.
        page.locator('g.atlas-node[data-method-id="method.fno"]').evaluate(
            "(el) => el.dispatchEvent(new MouseEvent('click',{bubbles:true}))")
        assert "傅里叶" in page.locator("#details-body").inner_text()
        assert "优先阅读" in page.locator("#details-body").inner_text()
        assert page.locator("#details-body a[href^='https://']").count()>0

        # Click an actual method evolution SVG edge; read bottleneck & evidence.
        page.locator('g.atlas-edge[data-edge-id="relation.pino--extends--fno"]').evaluate(
            "(el) => el.dispatchEvent(new MouseEvent('click',{bubbles:true}))")
        text=page.locator("#details-body").inner_text()
        assert "方法改变了什么" in text
        assert "解决的技术瓶颈" in text
        assert "支持论文" in text
        assert page.locator("g.atlas-node.selected").count()==2
        assert page.locator("g.atlas-edge.selected").count()==1
        page.screenshot(path=str(SHOTS/"03-selected-fno-pino-edge.png"),full_page=True)

        # Color encodes phase, not node paradigm.
        edge=page.locator('g.atlas-edge[data-edge-id="relation.pino--extends--fno"]')
        assert edge.count()==1
        # Search and zoom remain effective while the full DAG remains mounted.
        old=page.locator("#board").get_attribute("style")
        page.locator("#zoom-in").click()
        assert page.locator("#board").get_attribute("style")!=old
        page.locator("#fit-all").click()
        page.screenshot(path=str(SHOTS/"04-whole-dag-overview.png"),full_page=True)

        page.locator("#search").fill("DeepONet")
        assert page.locator("g.atlas-node.primary, g.atlas-node.selected").count()>=1
        page.locator("#search").fill("")
        page.locator("#language").click()
        assert "forward models" in page.locator(".intro h1").inner_text().lower()
        assert page.locator("g.atlas-node").count()==61
        page.screenshot(path=str(SHOTS/"05-english.png"),full_page=True)

        # Mobile page must remain scroll-width safe; SVG itself is pannable.
        mobile=browser.new_page(viewport={"width":390,"height":844},device_scale_factor=1)
        merrors=[]
        mobile.on("pageerror",lambda e:merrors.append(str(e)))
        mobile.goto(HTML.resolve().as_uri(),wait_until="load")
        mobile.wait_for_selector("g.atlas-node")
        assert mobile.locator(".phase-card").count()==3
        assert mobile.locator("g.atlas-node").count()==61
        mobile.screenshot(path=str(SHOTS/"06-mobile-chinese.png"),full_page=True)
        delta=mobile.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
        assert delta<=4,"Mobile overflow: "+str(delta)
        assert not errors and not merrors,{"desktop":errors,"mobile":merrors}
        browser.close()
    print("v0.7 Graphviz DAG browser tests succeeded; screenshots:",SHOTS)


if __name__=="__main__":
    run()

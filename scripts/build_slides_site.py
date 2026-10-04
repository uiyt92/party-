"""Build the 답장의 기술 lecture deck (dist/slides/canvas) into a static site for GitHub Pages.

The canvas sources are the Claude Design artboards (one .dc.html per slide) plus canvas.json,
which holds slide order and page. Only the main page is published, in on-canvas reading order.
"""
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "dist" / "slides" / "canvas"
IMAGES = ROOT / "dist" / "slides" / "images"
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "build" / "slides-site"

# Canvas asset ids → repo image paths
BLOB = {
    "0fa852bfdd69d7e4cccce24eab9c6a99": "images/blush.png",
    "d6308a784493bb397dffe0f1a34cdf8e": "images/chunsik1.png",
    "c86f1396436615b4b628eacdecfd01de": "images/chunsik2.png",
    "05f441d3b97104cb891145fd6ac41c85": "images/chunsik3.png",
    "80da9f2d60283918ddc9854890d551b0": "images/clue_frog.png",
    "bfdf23bc1ca70bed34cae91d6d55c2b2": "images/clue_snow.png",
    "ce060b17a558759d62f973777afe1c4d": "images/gyuri.jpg",
    "dd766f1bae4a5be665791f0abe9615a1": "images/niang.png",
    "2967e815a7906f50f7f9896380b071d1": "images/sent_photo.jpg",
    "a0015768187649ce3b303ab68a6c0a09": "images/sextalk/emo1.png",
    "24cad33fcfd319a5ab0de2e3cc994d4d": "images/sextalk/emo2.png",
    "d328fddb3b01f0ec75fa0ecaa7ad078f": "images/sextalk/emo3.png",
    "dfff91e39decf2120e686196ce19d277": "images/sextalk/emo4.png",
    "727543216f71d601306c7e4411772a3e": "images/sextalk/emo5.png",
    "0785ec6cc4f5f3feb9f4d960901e70aa": "images/sextalk/jiyeon1.png",
    "8f8183a31c798a849a7f4ec3ea9121b0": "images/sextalk/jiyeon2.png",
    "7490f7cd0fac8cc2703a191da5a4e57d": "images/sextalk/jiyeon3.png",
    "b65c62594f4f884c84e035366796dd5d": "images/sextalk/jiyeon4.png",
    "d63145845efd7465515f800d994f4f29": "images/approach_kyobo.webp",
}

VIEWER_CSS = """
html,body{height:100%;margin:0}
body{background:#111;overflow:hidden}
.stage{position:fixed;inset:0;display:flex;align-items:center;justify-content:center}
#deck{position:relative;width:1280px;height:720px;flex:none}
#deck>.slide{position:absolute;inset:0;display:none;box-shadow:0 20px 60px rgba(0,0,0,.4)}
#deck>.slide.active{display:flex}
.nav{position:fixed;top:14px;right:20px;color:#fff;font:800 15px Pretendard,sans-serif;z-index:21;background:rgba(17,17,17,.72);border:1px solid rgba(255,255,255,.18);padding:4px 13px;border-radius:20px}
.nav #cur{color:#7cc0ff}
.progress{position:fixed;top:0;left:0;right:0;height:5px;background:rgba(255,255,255,.09);z-index:20}
.progress__bar{height:100%;width:0;background:linear-gradient(90deg,#2563eb,#7c3aed);transition:width .25s ease}
"""

VIEWER_JS = """
const s=[...document.querySelectorAll('#deck>.slide')];let i=0;document.getElementById('tot').textContent=s.length;
// 아직 분할 전인 빽빽한 장은 720px 안에 들어오도록 내용만 줄인다
function shrink(el){el.classList.add('active');let z=1;while(el.scrollHeight>720&&z>.6){z-=.03;[...el.children].forEach(c=>c.style.zoom=z)}el.classList.remove('active')}
document.fonts.ready.then(()=>{s.forEach(shrink);s[i].classList.add('active')});
function show(n){s[i].classList.remove('active');i=Math.max(0,Math.min(s.length-1,n));s[i].classList.add('active');document.getElementById('cur').textContent=i+1;document.getElementById('pbar').style.width=((i+1)/s.length*100)+'%';history.replaceState(null,'','#'+(i+1))}
function fit(){const sc=Math.min(innerWidth/1280,innerHeight/720);document.getElementById('deck').style.transform='scale('+sc+')'}
addEventListener("resize",fit);fit();show((parseInt(location.hash.slice(1))||1)-1);
addEventListener('keydown',e=>{if(['ArrowRight',' ','PageDown'].includes(e.key)){e.preventDefault();show(i+1)}if(['ArrowLeft','PageUp'].includes(e.key))show(i-1)});
addEventListener('click',e=>{show(i+(e.clientX>innerWidth/2?1:-1))});
addEventListener('hashchange',()=>{const n=parseInt(location.hash.slice(1));if(n&&n-1!==i)show(n-1)});
"""


def main():
    idx = json.loads((SRC / "canvas.json").read_text(encoding="utf-8"))
    boards = idx["boards"]
    main_page = [f for f in idx["order"] if boards[f].get("page", "main") == "main"]
    main_page.sort(key=lambda f: (boards[f]["y"], boards[f]["x"]))

    sections = []
    for name in main_page:
        html = (SRC / name).read_text(encoding="utf-8")
        m = re.search(r"<section .*?</section>", html, re.S)
        if not m:
            sys.exit(f"{name}: <section> not found")
        sec = m.group(0)
        for blob_id, path in BLOB.items():
            sec = sec.replace("/_blob/" + blob_id, path)
        if "/_blob/" in sec:
            sys.exit(f"{name}: unmapped canvas asset — add it to BLOB")
        sections.append(sec)

    css = (SRC / "deck.css").read_text(encoding="utf-8")
    page = (
        '<!DOCTYPE html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        "<title>답장의 기술 — 강의 슬라이드</title>\n"
        '<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.css">\n'
        '<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@700;900&display=swap" rel="stylesheet">\n'
        "<style>\n" + css + VIEWER_CSS + "</style>\n</head>\n<body>\n"
        '<div class="stage"><div id="deck">\n' + "\n".join(sections) + "\n</div></div>\n"
        '<div class="progress"><div class="progress__bar" id="pbar"></div></div>\n'
        '<div class="nav"><span id="cur">1</span> / <span id="tot"></span></div>\n'
        "<script>" + VIEWER_JS + "</script>\n</body>\n</html>\n"
    )

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    (OUT / "index.html").write_text(page, encoding="utf-8")
    used = {p for p in BLOB.values() if p in page}
    for rel in used:
        dst = OUT / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(IMAGES / rel.removeprefix("images/"), dst)
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    print(f"{len(sections)} slides, {len(used)} images -> {OUT}")


if __name__ == "__main__":
    main()

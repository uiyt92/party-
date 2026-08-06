"""
md_to_typ.py — 마크다운 → Typst 변환 v3
핵심: 모든 일반 텍스트는 #par[...] 또는 직접 문단으로 출력.
Typst에서 문단 텍스트는 마크업 모드에서 그냥 나열하면 됨.
문제 원인: 테이블 셀 첫 번째가 빈 값 '#' → 탈출처리 필요.
"""

import re
import sys
from pathlib import Path


# ─── 인라인 볼드 처리 ─────────────────────────────────────────────────────────
def apply_bold(text: str) -> str:
    """**bold** → *bold* (Typst 강조 마크업)"""
    return re.sub(r'\*\*(.+?)\*\*', lambda m: f'*{m.group(1)}*', text)


# ─── Typst 특수문자 이스케이프 (텍스트 모드용) ───────────────────────────────
def esc_typst(text: str) -> str:
    """Typst 마크업 모드에서 특수 의미를 갖는 문자 이스케이프.
    @, #, <, >, \ 만 이스케이프. []{}는 content 블록 안에서는 괜찮음.
    """
    # @ → \@ (이메일 등)
    # # → \# (단독 # 이 아닌, 텍스트 내 #)
    text = re.sub(r'(?<!\*)(#)(?!\[)', r'\\#', text)
    text = text.replace('@', '\\@')
    text = text.replace('<', '\\<').replace('>', '\\>')
    return text


# ─── 셀 텍스트 안전 처리 ─────────────────────────────────────────────────────
def safe_cell(text: str) -> str:
    """테이블 셀 내용을 안전하게 처리."""
    text = text.strip()
    if not text:
        return ''
    # # 기호 이스케이프
    text = re.sub(r'(?<!\*)(#)(?!\[)', r'\\#', text)
    text = apply_bold(text)
    return text


# ─── 마크다운 테이블 → Typst table ───────────────────────────────────────────
def convert_table(lines: list) -> str:
    rows = []
    for line in lines:
        if re.match(r'^\s*\|[-: |]+\|\s*$', line):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        rows.append(cells)
    if not rows:
        return ''
    n_cols = max(len(r) for r in rows)
    # 첫 번째 열이 숫자/번호열이면 좁게, 나머지는 균등
    first_col_is_number = all(
        re.match(r'^(\d+|#)$', row[0]) if row else True
        for row in rows[1:] if row  # 헤더 제외
    )
    if n_cols == 4 and first_col_is_number:
        col_str = '0.36fr, 1.15fr, 1.25fr, 1.45fr'
    elif n_cols == 3:
        col_str = '1.5fr, 1fr, 1fr'
    elif n_cols == 2:
        col_str = '1.5fr, 1fr'
    else:
        col_str = ', '.join(['1fr'] * n_cols)

    cell_lines = []
    for i, row in enumerate(rows):
        padded = row + [''] * (n_cols - len(row))
        for cell in padded:
            content = safe_cell(cell)
            if i == 0:
                # 헤더 행: 네이비 배경
                cell_lines.append(
                    f'    table.cell(fill: rgb("1e3a8a"))[#text(fill: white, weight: 700, size: 9pt)[{content}]],'
                )
            else:
                cell_lines.append(f'    [#text(size: 9pt)[{content}]],')

    result_lines = [
        '#block(above: 1em, below: 1em, width: 100%)[',
        f'  #table(',
        f'    columns: ({col_str}),',
        f'    stroke: (x: none, y: 0.5pt + luma(200)),',
        f'    inset: (x: 6pt, y: 6pt),',
    ]
    result_lines.extend(cell_lines)
    result_lines.append('  )')
    result_lines.append(']')
    return '\n'.join(result_lines)


# ─── 카톡 대화 블록 파싱 ─────────────────────────────────────────────────────
def is_chat_block(quote_lines: list) -> bool:
    for ql in quote_lines:
        content = ql.lstrip('> ').strip()
        if re.match(r'^(나|여):', content):
            return True
    return False


def is_checklist_block(quote_lines: list) -> bool:
    return any('☐' in ql for ql in quote_lines)


def parse_chat_lines(quote_lines: list) -> str:
    bubble_lines = []
    for ql in quote_lines:
        content = ql.lstrip('> ').rstrip()
        m_me = re.match(r'^나:\s*(.*)', content)
        m_her = re.match(r'^여:\s*(.*)', content)
        if m_me:
            msg = apply_bold(m_me.group(1))
            bubble_lines.append(f'  #me[{msg}]')
        elif m_her:
            msg = apply_bold(m_her.group(1))
            bubble_lines.append(f'  #her[{msg}]')
        elif content.strip():
            note = apply_bold(content)
            bubble_lines.append(f'  #text(size: 9pt, fill: luma(180))[{note}]')
    return '\n'.join(bubble_lines)


def extract_quote_text_lines(quote_lines: list) -> list:
    return [ql.lstrip('> ') for ql in quote_lines]


def render_diagram_block(quote_lines: list) -> str:
    """일반 도식/텍스트 인용 블록"""
    text_lines = extract_quote_text_lines(quote_lines)
    rendered_parts = []
    for tl in text_lines:
        tl = tl.strip()
        if not tl:
            continue
        tl_bold = apply_bold(tl)
        rendered_parts.append(tl_bold)
    inner = '\n\n  '.join(rendered_parts)
    return f'#callout[\n  {inner}\n]'


# ─── BAD/GOOD 내부 렌더 ───────────────────────────────────────────────────────
def render_inner_block(quote_lines: list) -> str:
    if is_chat_block(quote_lines):
        return parse_chat_lines(quote_lines)
    else:
        lines = extract_quote_text_lines(quote_lines)
        parts = []
        for l in lines:
            l = l.strip()
            if l:
                parts.append(apply_bold(l))
        return '  ' + '\n  '.join(parts)


# ─── 메인 변환 ────────────────────────────────────────────────────────────────
def convert_md(md_text: str) -> str:
    # 도식 마커 변환 (주석 제거 전에) — <!-- flow: A | B | C --> , <!-- d:NAME -->
    def _conv_comment(m):
        body = m.group(1).strip()
        if body.startswith('flow:'):
            steps = [s.strip() for s in body[5:].split('|') if s.strip()]
            args = ', '.join('"' + s.replace('"', '') + '"' for s in steps)
            return f'\n\n#flow({args})\n\n'
        if body.startswith('d:'):
            return f'\n\n#{body[2:].strip()}\n\n'
        return ''  # 그 외 주석(설명용 도식 마커 등)은 제거
    md_text = re.sub(r'<!--(.*?)-->', _conv_comment, md_text, flags=re.DOTALL)

    lines = md_text.split('\n')
    out = []
    i = 0

    # BAD/GOOD 상태
    pending_bad_label = None
    pending_good_label = None
    bad_block = None    # None = 비활성, [] = 대기중/수집중
    good_block = None

    def flush_vs():
        nonlocal bad_block, good_block, pending_bad_label, pending_good_label
        if bad_block is not None and good_block is not None:
            bc = render_inner_block(bad_block)
            gc = render_inner_block(good_block)
            out.append(f'#vs(\n  bad: [\n{bc}\n  ],\n  good: [\n{gc}\n  ]\n)')
        elif bad_block is not None:
            lbl = pending_bad_label or 'BAD'
            bc = render_inner_block(bad_block)
            out.append(
                '#block(width: 100%, breakable: false, fill: rgb("fef2f2"), '
                'stroke: (left: 3pt + rgb("dc2626")), radius: 8pt, '
                'inset: 12pt, above: 0.8em, below: 0.8em)[\n'
                f'  #text(size: 8.5pt, weight: 700, fill: rgb("dc2626"))[{lbl}] #v(4pt)\n'
                f'{bc}\n]'
            )
        elif good_block is not None:
            lbl = pending_good_label or 'GOOD'
            gc = render_inner_block(good_block)
            out.append(
                '#block(width: 100%, breakable: false, fill: rgb("eff6ff"), '
                'stroke: (left: 3pt + rgb("2563eb")), radius: 8pt, '
                'inset: 12pt, above: 0.8em, below: 0.8em)[\n'
                f'  #text(size: 8.5pt, weight: 700, fill: rgb("2563eb"))[{lbl}] #v(4pt)\n'
                f'{gc}\n]'
            )
        bad_block = None
        good_block = None
        pending_bad_label = None
        pending_good_label = None

    while i < len(lines):
        line = lines[i]

        # ── H1
        if re.match(r'^# [^#]', line):
            if bad_block is not None or good_block is not None:
                flush_vs()
            title = apply_bold(line[2:].strip())
            out.append(f'\n= {title}')
            i += 1
            continue

        # ── H2
        if line.startswith('## '):
            if bad_block is not None or good_block is not None:
                flush_vs()
            title = apply_bold(line[3:].strip())
            out.append(f'\n== {title}')
            i += 1
            continue

        # ── H3
        if line.startswith('### '):
            if bad_block is not None or good_block is not None:
                flush_vs()
            title = apply_bold(line[4:].strip())
            out.append(f'\n=== {title}')
            i += 1
            continue

        # ── 수평선
        if re.match(r'^[-*_]{3,}\s*$', line):
            out.append('#line(length: 100%, stroke: 0.5pt + luma(200))')
            i += 1
            continue

        # ── 마크다운 테이블
        if (re.match(r'^\s*\|', line) and
                i + 1 < len(lines) and
                re.match(r'^\s*\|[-: |]+\|\s*$', lines[i + 1])):
            if bad_block is not None or good_block is not None:
                flush_vs()
            table_lines = []
            while i < len(lines) and re.match(r'^\s*\|', lines[i]):
                table_lines.append(lines[i])
                i += 1
            out.append(convert_table(table_lines))
            continue

        # ── **BAD — ...** 헤더
        bad_header = re.match(r'^\*\*BAD\s*[—\-]+\s*(.*?)\*\*\s*$', line)
        if bad_header:
            if good_block is not None and bad_block is None:
                flush_vs()
            elif bad_block is not None:
                flush_vs()
            pending_bad_label = 'BAD — ' + bad_header.group(1)
            bad_block = []
            i += 1
            continue

        # ── **GOOD — ...** 헤더
        good_header = re.match(r'^\*\*GOOD\s*[—\-]+\s*(.*?)\*\*\s*$', line)
        if good_header:
            pending_good_label = 'GOOD — ' + good_header.group(1)
            good_block = []
            i += 1
            continue

        # ── 인용 블록
        if line.startswith('>'):
            # BAD 대기 중이고 bad_block이 빈 리스트 → 여기서 수집
            if bad_block is not None and bad_block == [] and pending_bad_label:
                while i < len(lines) and lines[i].startswith('>'):
                    bad_block.append(lines[i])
                    i += 1
                # 빈 줄 skip 후 GOOD 확인
                j = i
                while j < len(lines) and lines[j].strip() == '':
                    j += 1
                if j < len(lines) and re.match(r'^\*\*GOOD', lines[j]):
                    pass  # GOOD 기다림
                else:
                    flush_vs()
                continue

            # GOOD 대기 중이고 good_block이 빈 리스트 → 여기서 수집
            if good_block is not None and good_block == [] and pending_good_label:
                while i < len(lines) and lines[i].startswith('>'):
                    good_block.append(lines[i])
                    i += 1
                flush_vs()
                continue

            # 일반 인용 블록
            if bad_block is not None or good_block is not None:
                flush_vs()

            quote_lines = []
            while i < len(lines) and lines[i].startswith('>'):
                quote_lines.append(lines[i])
                i += 1

            if not quote_lines:
                i += 1
                continue

            first_content = quote_lines[0].lstrip('> ').strip()

            # 핵심 박스
            if re.match(r'\*\*핵심\*\*[:：]', first_content):
                msg = re.sub(r'\*\*핵심\*\*[:：]\s*', '', first_content)
                extra = ' '.join(
                    ql.lstrip('> ').strip()
                    for ql in quote_lines[1:]
                    if ql.lstrip('> ').strip()
                )
                if extra:
                    msg = msg + ' ' + extra
                msg = apply_bold(msg)
                out.append(f'#callout[\n  *핵심*: {msg}\n]')
                continue

            # 심리 박스
            if re.match(r'\*\*💡 왜 통할까\*\*', first_content):
                body_parts = [
                    ql.lstrip('> ').strip()
                    for ql in quote_lines[1:]
                    if ql.lstrip('> ').strip()
                ]
                body = ' '.join(body_parts)
                body = apply_bold(body)
                out.append(f'#psych-box[\n  {body}\n]')
                continue

            # 체크리스트
            if is_checklist_block(quote_lines):
                items = []
                for ql in quote_lines:
                    c = ql.lstrip('> ').strip()
                    if '☐' in c:
                        item = apply_bold(c.replace('☐', '').strip())
                        items.append(f'  #check[{item}]')
                out.append('#block(above: 0.8em, below: 0.8em)[\n' + '\n'.join(items) + '\n]')
                continue

            # 카톡 대화
            if is_chat_block(quote_lines):
                bubbles = parse_chat_lines(quote_lines)
                out.append(f'#chat[\n{bubbles}\n]')
                continue

            # 일반 도식/텍스트 박스
            out.append(render_diagram_block(quote_lines))
            continue

        # ── 빈 줄
        if line.strip() == '':
            if bad_block is not None or good_block is not None:
                if (bad_block == [] and pending_bad_label) or (good_block == [] and pending_good_label):
                    i += 1
                    continue
                flush_vs()
            out.append('')
            i += 1
            continue

        # ── BAD/GOOD 대기 중에 인용 아닌 내용
        if bad_block is not None or good_block is not None:
            if not line.startswith('>'):
                flush_vs()

        # ── 순서 없는 목록
        if re.match(r'^[-*]\s+', line):
            items = []
            while i < len(lines) and re.match(r'^[-*]\s+', lines[i]):
                item = apply_bold(re.sub(r'^[-*]\s+', '', lines[i]).strip())
                items.append(f'  [{item}]')
                i += 1
            out.append('#list(\n' + ',\n'.join(items) + '\n)')
            continue

        # ── 순서 있는 목록
        if re.match(r'^\d+\.\s+', line):
            items = []
            while i < len(lines) and re.match(r'^\d+\.\s+', lines[i]):
                item = apply_bold(re.sub(r'^\d+\.\s+', '', lines[i]).strip())
                items.append(f'  [{item}]')
                i += 1
            out.append('#enum(\n' + ',\n'.join(items) + '\n)')
            continue

        # ── 일반 문단 텍스트
        # Typst 마크업 모드에서 한국어 텍스트는 그냥 출력해도 되지만
        # *bold* 가 있으면 올바르게 처리됨. 단 # @ < > 는 이스케이프.
        if line.strip():
            text = apply_bold(line)
            # # 이스케이프 (단 이미 \# 처리된 것, #[, #let 등은 건드리지 않음)
            # 한국어 본문에서 # 기호 자체가 나올 일이 거의 없으므로
            # 텍스트를 content block으로 감쌈
            out.append(text)

        i += 1

    if bad_block is not None or good_block is not None:
        flush_vs()

    return '\n'.join(out)


# ─── 빌드 ─────────────────────────────────────────────────────────────────────
def build_book(root: Path):
    # 명시적 순서 매니페스트 (신규장 삽입을 위해 글롭 대신 고정 순서 사용)
    PART1 = [
        '01_intro.md', '02_mindset.md', '03_profile.md', '04_why.md', '05_first_talk.md',
        '06_insta.md', '07_late_reply.md', '08_ignored.md', '08b_continue.md',
        '09_keep_talking.md', '10_photo.md',
    ]
    PART2 = [
        '11_expression.md', '12_skills.md', '13_signals.md', '14_banmal.md', '15_situation.md',
        '16_mistakes.md', '17_revive.md', '18_call.md', '19_to_meet.md', '20_cases.md', '21_appendix.md',
    ]
    part1 = [root / n for n in PART1 if (root / n).exists()]
    part2 = [root / n for n in PART2 if (root / n).exists()]

    typ_parts = ['#part-divider("PART 1", "대화를 여는 법")\n']
    for md_file in part1:
        print(f'  변환: {md_file.name}')
        typ_parts.append(f'// --- {md_file.name} ---\n{convert_file(md_file)}\n')

    typ_parts.append('\n#part-divider("PART 2", "대화를 키우고 만나는 법")\n')
    for md_file in part2:
        print(f'  변환: {md_file.name}')
        typ_parts.append(f'// --- {md_file.name} ---\n{convert_file(md_file)}\n')

    body = '\n'.join(typ_parts)
    build_typ = (
        '#import "templates/typst/book.typ": *\n\n'
        '#show: book.with(\n'
        '  title: "답장의 기술",\n'
        '  subtitle: "카톡이 막히는 남자를 위한 · 25가지 실전 사례와 150가지 카톡 예시",\n'
        '  author: "초보 탈출 프로젝트",\n'
        ')\n\n'
        + body
    )

    out_path = root / 'build.typ'
    out_path.write_text(build_typ, encoding='utf-8')
    print(f'\nbuild.typ 생성 완료')
    return out_path


def convert_file(src: Path) -> str:
    return convert_md(src.read_text(encoding='utf-8'))


# ─── 심화편(Part 3) 별도 빌드 ────────────────────────────────────────────────
def build_part3(root: Path):
    files = [
        'p3_00_intro.md', 'p3_22_sextalk.md', 'p3_23_ladder.md',
        'p3_24_consent.md', 'p3_25_block.md', 'p3_26_mental.md',
    ]
    d = root / 'drafts' / 'part3'
    parts = []
    for n in files:
        f = d / n
        if not f.exists():
            print(f'  (없음, 건너뜀: {n})')
            continue
        print(f'  심화 변환: {n}')
        parts.append(f'// --- {n} ---\n{convert_md(f.read_text(encoding="utf-8"))}\n')

    body = '\n'.join(parts)
    build_typ = (
        '#import "templates/typst/book.typ": *\n\n'
        '#show: book.with(\n'
        '  title: "답장의 기술 — 심화편",\n'
        '  subtitle: "성인을 위한 · 긴장과 수위의 대화 (19금)",\n'
        '  author: "초보 탈출 프로젝트",\n'
        ')\n\n'
        + body
    )
    out_path = root / 'build_part3.typ'
    out_path.write_text(build_typ, encoding='utf-8')
    print('\nbuild_part3.typ 생성 완료')
    return out_path


if __name__ == '__main__':
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
    build_book(root)
    print('--- 심화편 ---')
    build_part3(root)

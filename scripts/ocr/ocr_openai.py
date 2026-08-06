#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenAI Vision API를 사용한 PDF OCR 처리
카톡101.pdf를 텍스트로 변환
"""
import io
import sys
import os
import json
import base64
from pathlib import Path
from datetime import datetime
import fitz  # PyMuPDF
from openai import OpenAI

try:
    from .common import resolve_ocr_paths
except ImportError:
    from common import resolve_ocr_paths

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 설정
pdf_path, output_dir = resolve_ocr_paths()
PDF_PATH = str(pdf_path)
OUTPUT_DIR = str(output_dir)

def ocr_pdf_with_openai(pdf_path: str, max_pages: int = None) -> dict:
    """OpenAI Vision API로 PDF OCR 처리"""

    print(f"[START] PDF 처리 시작: {pdf_path}")

    # OpenAI 클라이언트 초기화
    try:
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        print("[AUTH] OpenAI API 인증 완료")
    except Exception as e:
        print(f"[ERROR] OpenAI 초기화 실패: {e}")
        print("[INFO] OPENAI_API_KEY 환경변수를 확인하세요")
        return None

    # PDF 열기
    try:
        pdf_doc = fitz.open(pdf_path)
        total_pages = len(pdf_doc)
        print(f"[READ] PDF 열기 완료: {total_pages} 페이지")
    except Exception as e:
        print(f"[ERROR] PDF 읽기 실패: {e}")
        return None

    # 최대 페이지 제한
    if max_pages:
        total_pages = min(total_pages, max_pages)
        print(f"[LIMIT] 처리 페이지 제한: {total_pages}페이지")

    # OCR 처리
    results = {}

    for page_num in range(total_pages):
        print(f"[PROCESS] 페이지 {page_num + 1}/{total_pages} OCR 처리 중...", end="", flush=True)

        try:
            # 페이지를 이미지로 변환
            page = pdf_doc[page_num]
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2배 확대 (품질 향상)
            image_bytes = pix.tobytes("png")
            image_base64 = base64.standard_b64encode(image_bytes).decode('utf-8')

            # OpenAI Vision API 호출
            try:
                response = client.messages.create(
                    model="gpt-4o-mini",
                    max_tokens=4096,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "image",
                                    "source": {
                                        "type": "base64",
                                        "media_type": "image/png",
                                        "data": image_base64
                                    }
                                },
                                {
                                    "type": "text",
                                    "text": "이 이미지의 모든 텍스트를 정확하게 추출해주세요. 글씨, 제목, 번호, 기호 등 모든 것을 포함하세요."
                                }
                            ]
                        }
                    ]
                )

                # 응답에서 텍스트 추출
                text = response.content[0].text
            except AttributeError:
                # 구형 API 형식 호환성
                response = client.messages.create(
                    model="gpt-4-turbo",
                    max_tokens=4096,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/png;base64,{image_base64}"
                                    }
                                },
                                {
                                    "type": "text",
                                    "text": "이 이미지의 모든 텍스트를 정확하게 추출해주세요."
                                }
                            ]
                        }
                    ]
                )
                text = response.choices[0].message.content

            results[f"page_{page_num + 1:03d}"] = {
                "page_number": page_num + 1,
                "text": text,
                "status": "success"
            }

            print(" [OK]")

        except Exception as e:
            print(f" [FAIL] ({e})")
            results[f"page_{page_num + 1:03d}"] = {
                "page_number": page_num + 1,
                "text": "",
                "status": f"failed: {str(e)}"
            }

    pdf_doc.close()

    return results

def save_results(results: dict, output_dir: str):
    """결과를 마크다운으로 저장"""

    if not results:
        print("[ERROR] 처리 결과가 없습니다")
        return

    # 마크다운 생성
    md_content = "# 카톡101 OCR 처리 결과\n\n"
    md_content += f"**처리 완료**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    md_content += f"**방식**: OpenAI Vision API (gpt-4o)\n"
    md_content += f"**총 페이지**: {len(results)}\n\n"

    # 성공/실패 통계
    success_count = sum(1 for r in results.values() if r["status"] == "success")
    md_content += f"**성공**: {success_count}/{len(results)}\n\n"

    # JSON 저장 (상세 응답)
    json_path = os.path.join(output_dir, "katalk101_ocr_openai.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"[SAVE] JSON 저장: {json_path}")

    # 마크다운 저장 (텍스트)
    md_path = os.path.join(output_dir, "katalk101_ocr.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)

        for page_key, data in sorted(results.items()):
            page_num = data["page_number"]
            text = data["text"]
            status = data["status"]

            f.write(f"\n## 페이지 {page_num}\n")
            f.write(f"**상태**: {status}\n\n")
            if text:
                f.write(f"{text}\n")
            f.write("\n" + "="*80 + "\n")

    print(f"[SAVE] 마크다운 저장: {md_path}")

if __name__ == "__main__":
    print("=" * 80)
    print("OpenAI Vision API OCR 처리")
    print("=" * 80)
    print()

    # 환경변수에서 API 키 확인
    api_key = os.environ.get("OPENAI_API_KEY")

    # 명령줄 인수로도 확인 (PowerShell에서 전달된 경우)
    if not api_key and len(sys.argv) > 1:
        api_key = sys.argv[1]

    if not api_key:
        print("[WARNING] OPENAI_API_KEY 환경변수가 설정되지 않았습니다")
        print("[INFO] 다음 중 하나를 시도하세요:")
        print('  방법1: $env:OPENAI_API_KEY = "sk-..."; python ocr_openai.py')
        print('  방법2: python ocr_openai.py "sk-..."')
        sys.exit(1)

    # API 키를 환경변수로 설정
    os.environ["OPENAI_API_KEY"] = api_key

    results = ocr_pdf_with_openai(PDF_PATH, max_pages=10)

    if results:
        print("\n[SAVE] 결과 저장 중...")
        save_results(results, OUTPUT_DIR)
        print("\n[OK] OCR 처리 완료!")
    else:
        print("\n[ERROR] OCR 처리 실패")
        sys.exit(1)

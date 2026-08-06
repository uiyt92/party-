#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Vision API를 사용한 PDF OCR 처리
카톡101.pdf를 텍스트로 변환
"""
import io
import sys

# Windows에서 UTF-8 출력 지원
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import os
import sys
import tempfile
from pathlib import Path
from pdf2image import convert_from_path
from google.cloud import vision
import json
from datetime import datetime

try:
    from .common import configure_google_credentials, resolve_ocr_paths
except ImportError:
    from common import configure_google_credentials, resolve_ocr_paths

# 설정 — 분류된 참고자료 경로 또는 환경변수 사용
pdf_path, output_dir = resolve_ocr_paths()
PDF_PATH = str(pdf_path)
OUTPUT_DIR = str(output_dir)
PROJECT_ID = "super-natural-465515"

# Google Cloud 인증 설정
if configure_google_credentials() is None:
    print("[WARNING] gcp-key.json을 찾을 수 없습니다. 시스템 인증 사용")
    try:
        from google.auth import default as gauth_default
        credentials, _ = gauth_default()
    except Exception as e:
        print(f"[ERROR] 인증 실패: {e}")
        sys.exit(1)

def ocr_page(image_path: str, client: vision.ImageAnnotatorClient) -> str:
    """이미지 한 페이지의 OCR 처리"""
    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)

    # 전체 텍스트 추출
    if response.full_text_annotation:
        return response.full_text_annotation.text
    return ""

def process_pdf_to_text(pdf_path: str, max_pages: int = None) -> dict:
    """PDF를 이미지로 변환 후 OCR 처리"""

    print(f"[START] PDF 처리 시작: {pdf_path}")

    # Vision API 클라이언트 초기화
    client = vision.ImageAnnotatorClient()

    # PDF를 이미지로 변환
    print(f"[CONVERT] PDF를 이미지로 변환 중...")
    try:
        images = convert_from_path(pdf_path, first_page=1, last_page=max_pages)
    except Exception as e:
        print(f"[ERROR] PDF 변환 실패: {e}")
        return None

    print(f"[OK] {len(images)}개 페이지 변환 완료")

    # 각 페이지 OCR 처리
    ocr_results = {}
    total_pages = len(images)

    for idx, image in enumerate(images, 1):
        print(f"[PROCESS] 페이지 {idx}/{total_pages} OCR 처리 중...", end="", flush=True)

        try:
            # 임시 이미지 파일 저장 (Windows 대응)
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                temp_image_path = tmp.name
                image.save(temp_image_path)

            # OCR 처리
            text = ocr_page(temp_image_path, client)
            ocr_results[f"page_{idx:03d}"] = {
                "page_number": idx,
                "text": text,
                "status": "success"
            }

            # 임시 파일 삭제
            os.remove(temp_image_path)
            print(" [OK]")

        except Exception as e:
            print(f" [FAIL] ({e})")
            ocr_results[f"page_{idx:03d}"] = {
                "page_number": idx,
                "text": "",
                "status": f"failed: {str(e)}"
            }

    return ocr_results

def save_results(results: dict, output_dir: str):
    """결과를 마크다운으로 저장"""

    if not results:
        print("[ERROR] 처리 결과가 없습니다")
        return

    # 마크다운 생성
    md_content = "# 카톡101 OCR 처리 결과\n\n"
    md_content += f"**처리 완료**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    md_content += f"**총 페이지**: {len(results)}\n\n"

    # JSON 저장 (전체 결과)
    json_path = os.path.join(output_dir, "카톡101_ocr_results.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"[OK] JSON 저장: {json_path}")

    # 마크다운으로도 저장 (텍스트만)
    md_path = os.path.join(output_dir, "카톡101_ocr.md")
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

    print(f"[OK] 마크다운 저장: {md_path}")

if __name__ == "__main__":
    # 첫 20페이지만 처리 (샘플)
    print("=" * 80)
    print("Google Vision API OCR 처리")
    print("=" * 80)

    max_pages = int(sys.argv[1]) if len(sys.argv) > 1 else 20

    print(f"\n[INFO] 처리 범위: 1~{max_pages}페이지\n")

    results = process_pdf_to_text(PDF_PATH, max_pages=max_pages)

    if results:
        print("\n[SAVE] 결과 저장 중...")
        save_results(results, OUTPUT_DIR)
        print("\n[OK] OCR 처리 완료!")
    else:
        print("\n[ERROR] OCR 처리 실패")
        sys.exit(1)

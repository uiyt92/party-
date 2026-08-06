#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gcloud CLI를 사용한 PDF OCR 처리
카톡101.pdf를 텍스트로 변환
"""
import io
import sys
import os
import json
import base64
import subprocess
from pathlib import Path
from datetime import datetime

try:
    from .common import resolve_ocr_paths
except ImportError:
    from common import resolve_ocr_paths

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 설정 — 분류된 참고자료 경로 또는 환경변수 사용
pdf_path, output_dir = resolve_ocr_paths()
PDF_PATH = str(pdf_path)
OUTPUT_DIR = str(output_dir)
PROJECT_ID = "super-natural-465515"

def get_gcloud_token():
    """gcloud에서 access token 얻기"""
    try:
        # PowerShell을 통해 gcloud 명령어 실행 (Windows PATH 문제 우회)
        if sys.platform == "win32":
            result = subprocess.run(
                ["powershell", "-Command", "gcloud auth application-default print-access-token"],
                capture_output=True,
                text=True,
                check=True
            )
        else:
            result = subprocess.run(
                ["gcloud", "auth", "application-default", "print-access-token"],
                capture_output=True,
                text=True,
                check=True
            )
        return result.stdout.strip()
    except Exception as e:
        print(f"[ERROR] 토큰 획득 실패: {e}")
        return None

def ocr_pdf_with_vision_api(pdf_path: str, max_pages: int = None) -> dict:
    """Vision API로 PDF OCR 처리"""

    print(f"[START] PDF 처리 시작: {pdf_path}")

    # 토큰 획득
    token = get_gcloud_token()
    if not token:
        print("[ERROR] Google Cloud 인증 실패")
        return None

    print(f"[AUTH] Google Cloud 인증 성공")

    # PDF 파일 읽기
    try:
        with open(pdf_path, 'rb') as f:
            pdf_content = f.read()
        print(f"[READ] PDF 파일 읽기 완료: {len(pdf_content)} bytes")
    except Exception as e:
        print(f"[ERROR] PDF 읽기 실패: {e}")
        return None

    # PDF를 Base64로 인코딩
    pdf_base64 = base64.standard_b64encode(pdf_content).decode('utf-8')

    # Vision API 요청 바디 구성
    request_body = {
        "requests": [
            {
                "image": {
                    "content": pdf_base64
                },
                "features": [
                    {
                        "type": "DOCUMENT_TEXT_DETECTION"
                    }
                ],
                "imageContext": {
                    "languageHints": ["ko"]  # 한국어 힌트
                }
            }
        ]
    }

    # REST API 호출
    import requests

    url = f"https://vision.googleapis.com/v1/images:annotate?key={token}"

    print(f"[PROCESS] Vision API 호출 중...")

    try:
        response = requests.post(url, json=request_body, timeout=60)
        response.raise_for_status()
    except Exception as e:
        print(f"[ERROR] API 호출 실패: {e}")
        return None

    # 응답 처리
    try:
        result = response.json()

        if "responses" not in result or not result["responses"]:
            print("[ERROR] API 응답이 비어있음")
            return None

        response_data = result["responses"][0]

        if "error" in response_data:
            print(f"[ERROR] API 에러: {response_data['error']}")
            return None

        # 텍스트 추출
        text = ""
        if "fullTextAnnotation" in response_data:
            text = response_data["fullTextAnnotation"].get("text", "")

        print(f"[OK] OCR 처리 완료: {len(text)} characters")

        return {
            "status": "success",
            "text": text,
            "page_count": 1,  # PDF 전체를 한 번에 처리
            "raw_response": response_data
        }

    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON 파싱 실패: {e}")
        print(f"응답 내용: {response.text[:500]}")
        return None

def save_results(results: dict, output_dir: str):
    """결과를 마크다운으로 저장"""

    if not results:
        print("[ERROR] 처리 결과가 없습니다")
        return

    # 마크다운 생성
    md_content = "# 카톡101 OCR 처리 결과\n\n"
    md_content += f"**처리 완료**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    md_content += f"**방식**: Google Vision API (gcloud CLI)\n"
    md_content += f"**상태**: {results['status']}\n\n"

    # JSON 저장 (상세 응답)
    json_path = os.path.join(output_dir, "katalk101_ocr_response.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"[SAVE] JSON 저장: {json_path}")

    # 마크다운 저장 (텍스트)
    md_path = os.path.join(output_dir, "katalk101_ocr.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
        f.write("\n## 추출된 텍스트\n\n")
        f.write(results["text"])

    print(f"[SAVE] 마크다운 저장: {md_path}")

if __name__ == "__main__":
    print("=" * 80)
    print("Google Vision API (gcloud) OCR 처리")
    print("=" * 80)
    print()

    results = ocr_pdf_with_vision_api(PDF_PATH)

    if results:
        print("\n[SAVE] 결과 저장 중...")
        save_results(results, OUTPUT_DIR)
        print("\n[OK] OCR 처리 완료!")
    else:
        print("\n[ERROR] OCR 처리 실패")
        sys.exit(1)

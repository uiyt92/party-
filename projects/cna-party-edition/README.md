# 파티의 주도권

`[CNA] Party Edition`을 A5 Typst 독립 책으로 전면 재작성하는 제품입니다.

## 작업 기준

- 원고의 기준 경로: `manuscript/*.md`
- 조판의 기준 경로: `typst/*.typ`
- 로컬 참고 원본(추적 제외): `references/pdf/[CNA] Party Edition.pdf`
- 결과물: `dist/pdf/CNA_파티의_주도권.pdf`

## 범위

이 책의 범위는 첫 대화, 영향력/프레임 설계, 번호 교환에서 끝납니다. 카카오톡과 데이트 이후 운영은 포함하지 않습니다.

## 빌드와 검증

```powershell
python scripts/project.py build cna-party-book
python scripts/project.py verify cna-party-book
```

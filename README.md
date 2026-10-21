# On-Device AI 엔진 모형 조립 검사 시스템 — 최종 제출

카메라·센서 입력, Jetson AI 검사, 원본·판정 저장, PLC와 LED·컨베이어 연계를 구현한 프로젝트의 **실행 코드와 평가 문서를 한 저장소에 모았습니다.**

**검토 시작:** [최종 결과보고서 v1.2](docs/10_final_report_v1_2.pdf) · [프로젝트 상세](project/README.md) · [전체 문서·증빙](docs/README.md)

## 폴더 안내

| 폴더 | 포함 내용 |
|---|---|
| [project/](project/) | 기존 코드 저장소의 전체 추적 파일: 실행·학습 코드, 모델·설정, 설치 안내, 내부 개발 문서 |
| [docs/](docs/) | 기존 문서 저장소의 전체 추적 파일: 제출 보고서, 편집본, 원본 증빙 ZIP, DB 검토 자료 |

두 폴더는 서브모듈이나 외부 저장소 바로가기가 아닌 **실제 파일 폴더**입니다. `project/docs/`는 프로젝트 내부 문서이며 루트의 `docs/`와 구분합니다.

## 평가 문서 바로가기

원본 문서 저장소의 최신 목록을 그대로 연결했습니다. PDF·DOCX·원본 ZIP의 내용을 수정하지 않았습니다.

| ID | 최신 문서 | 버전 | 크기 | 편집·표시본 |
|---|---|---|---|---|
| 01 | [문제정의서](docs/01_%EC%97%94%EC%A7%84%EB%AA%A8%ED%98%95_%EB%AC%B8%EC%A0%9C%EC%A0%95%EC%9D%98%EC%84%9C_v1.1.pdf) | 1.1 | 260,906 B | [DOCX](docs/01_%EC%97%94%EC%A7%84%EB%AA%A8%ED%98%95_%EB%AC%B8%EC%A0%9C%EC%A0%95%EC%9D%98%EC%84%9C_v1.1.docx) |
| 02 | [데이터셋 설명서](docs/02_%EC%97%94%EC%A7%84%EB%AA%A8%ED%98%95_%EB%8D%B0%EC%9D%B4%ED%84%B0%EC%85%8B_%EC%84%A4%EB%AA%85%EC%84%9C_v1.2.pdf) | 1.2 | 2,721,564 B | [DOCX](docs/02_%EC%97%94%EC%A7%84%EB%AA%A8%ED%98%95_%EB%8D%B0%EC%9D%B4%ED%84%B0%EC%85%8B_%EC%84%A4%EB%AA%85%EC%84%9C_v1.2.docx) |
| 03 | [모델 평가서](docs/03_%EC%97%94%EC%A7%84%EB%AA%A8%ED%98%95_%EB%AA%A8%EB%8D%B8_%ED%8F%89%EA%B0%80%EC%84%9C_v1.1.pdf) | 1.1 | 2,002,951 B | [DOCX](docs/03_%EC%97%94%EC%A7%84%EB%AA%A8%ED%98%95_%EB%AA%A8%EB%8D%B8_%ED%8F%89%EA%B0%80%EC%84%9C_v1.1.docx) |
| 04 | [최적화 전후 Benchmark](docs/04_%EC%97%94%EC%A7%84%EB%AA%A8%ED%98%95_%EC%B5%9C%EC%A0%81%ED%99%94%EC%A0%84%ED%9B%84_Benchmark_%EB%B3%B4%EA%B3%A0%EC%84%9C_v1.2.pdf) | 1.2 | 1,382,202 B | [DOCX](docs/04_%EC%97%94%EC%A7%84%EB%AA%A8%ED%98%95_%EC%B5%9C%EC%A0%81%ED%99%94%EC%A0%84%ED%9B%84_Benchmark_%EB%B3%B4%EA%B3%A0%EC%84%9C_v1.2.docx) |
| 05 | [통합 테스트 결과서](docs/05_%EC%97%94%EC%A7%84%EB%AA%A8%ED%98%95_%ED%86%B5%ED%95%A9%ED%85%8C%EC%8A%A4%ED%8A%B8_%EA%B2%B0%EA%B3%BC%EC%84%9C_v1.0.pdf) | 1.0 | 2,738,558 B | [DOCX](docs/05_%EC%97%94%EC%A7%84%EB%AA%A8%ED%98%95_%ED%86%B5%ED%95%A9%ED%85%8C%EC%8A%A4%ED%8A%B8_%EA%B2%B0%EA%B3%BC%EC%84%9C_v1.0.docx) |
| 06 | [DB 구조·조회 방식](docs/06_%EC%97%94%EC%A7%84%EB%AA%A8%ED%98%95_DB_%EA%B5%AC%EC%A1%B0%EC%99%80_%EC%A1%B0%ED%9A%8C%EB%B0%A9%EC%8B%9D_v1.0.pdf) | 1.0 | 1,054,245 B | [DOCX](docs/06_%EC%97%94%EC%A7%84%EB%AA%A8%ED%98%95_DB_%EA%B5%AC%EC%A1%B0%EC%99%80_%EC%A1%B0%ED%9A%8C%EB%B0%A9%EC%8B%9D_v1.0.docx) |
| 07 | [Jetson 실행·변환 절차서](docs/07_%EC%97%94%EC%A7%84%EB%AA%A8%ED%98%95_Jetson_%EC%8B%A4%ED%96%89_ONNX_TensorRT_%EC%A0%88%EC%B0%A8%EC%84%9C_v1.1.pdf) | 1.1 | 634,030 B | [DOCX](docs/07_%EC%97%94%EC%A7%84%EB%AA%A8%ED%98%95_Jetson_%EC%8B%A4%ED%96%89_ONNX_TensorRT_%EC%A0%88%EC%B0%A8%EC%84%9C_v1.1.docx) |
| 08 | [프로젝트 기획안](docs/08_%EC%97%94%EC%A7%84%EB%AA%A8%ED%98%95_%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8_%EA%B8%B0%ED%9A%8D%EC%95%88_v1.1.pdf) | 1.1 | 319,435 B | [DOCX](docs/08_%EC%97%94%EC%A7%84%EB%AA%A8%ED%98%95_%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8_%EA%B8%B0%ED%9A%8D%EC%95%88_v1.1.docx) |
| 09 | [코드 저장소 README](docs/09_project_readme_v1_1.md) | 1.1 | 28,791 B | [HTML](docs/09_project_readme_v1_1.html) |
| 10 | [최종 결과보고서](docs/10_final_report_v1_2.pdf) | 1.2 | 1,202,229 B | [DOCX](docs/10_final_report_v1_2.docx) |
| 11 | [데이터셋 구축 프로그램 설명서](docs/11_dataset_program_manual_v1_0.pdf) | 1.0 | 518,367 B | [DOCX](docs/11_dataset_program_manual_v1_0.docx) |

## 원본 증빙과 DB

| 자료 | 링크 |
|---|---|
| 전체 학습·검증 사진과 라벨 | [M1_M2_dataset_evidence_v002.zip](docs/M1_M2_dataset_evidence_v002.zip) |
| 모델 학습·평가 원본 | [M1_M2_model_evaluation_evidence_v001.zip](docs/M1_M2_model_evaluation_evidence_v001.zip) |
| 최적화 비교 원본 | [M1_M2_benchmark_evidence_v001.zip](docs/M1_M2_benchmark_evidence_v001.zip) |
| 실제 통합시험 원본 | [Engine_Integrated_Test_Evidence_v001.zip](docs/Engine_Integrated_Test_Evidence_v001.zip) |
| DB·SQL·조회 검토 | [DB 검토 자료](docs/review_kit/README_KO.md) |
| 평가 근거 위치 | [EVIDENCE_INDEX.md](docs/EVIDENCE_INDEX.md) |
| 문서 버전 대응 | [DOCUMENT_VERSION_MAP.md](docs/DOCUMENT_VERSION_MAP.md) |

## 내려받기와 실행 위치

전체 데이터셋 ZIP은 Git LFS 파일입니다. 실제 파일까지 내려받으려면 Git LFS가 설치된 환경에서 다음을 사용합니다.

```bash
git lfs install
git clone https://github.com/tmdgns104/Engine_Assembly_Final_Submission.git
cd Engine_Assembly_Final_Submission
git lfs pull
cd project
```

기존 실행 안내의 프로젝트 루트는 이제 **`project/`**입니다. 위 `cd project` 이후 해당 환경에 맞는 설치·실행 안내를 따르세요.

- [Jetson 운영본 설치 안내](project/jetson/INSTALL_OPERATING_KO.md)
- [학습 코드와 자료 안내](project/notebook/training/README_KO.md)
- [데이터셋 ZIP 실파일 다운로드](https://github.com/tmdgns104/Engine_Assembly_Final_Submission/raw/refs/heads/main/docs/M1_M2_dataset_evidence_v002.zip)

GitHub의 `Code → Download ZIP`에 LFS 실파일까지 포함되는지는 이 작업에서 검증하지 않았습니다. 전체 파일 확보에는 위 Git LFS 방식 또는 개별 실파일 다운로드를 사용하세요.

## 출처와 검증

이 저장소는 아래 두 커밋의 스냅샷입니다. 원본 저장소와 운영 장치는 변경하지 않았으며, 원본의 후속 변경이 자동 동기화되지는 않습니다.

| 폴더 | 원본 저장소 | 고정 커밋 |
|---|---|---|
| project/ | [tmdgns104/Engine_Assembly_Defect_Inspector](https://github.com/tmdgns104/Engine_Assembly_Defect_Inspector) | `bdadacc51c6c9b03d67a57ed7bbe10366a06cc4c` |
| docs/ | [tmdgns104/Engine_Assembly_Runtime_Review](https://github.com/tmdgns104/Engine_Assembly_Runtime_Review) | `fa9774e1e08f83b6f287c27f018cee78f7febe5f` |

[출처·수량](SOURCE_REVISIONS.json) · [파일별 보존·해시 목록](.submission/FILE_MANIFEST.json) · [이전 검증](.submission/MIGRATION_VERIFICATION.json)

원본 README 두 개는 [.submission/original_readmes/](.submission/original_readmes/)에도 보존했습니다. 통합 폴더의 README는 안내 링크만 새 위치로 연결하며, 과거 근거 커밋·보고서 내부 링크는 원문 출처로 보존합니다.

이번 작업은 파일 통합과 다운로드 검증입니다. 새로운 모델 학습·현장시험·Jetson 또는 PLC 배포를 수행한 것은 아닙니다. PPT·시연영상은 실제 파일 포함 여부를 별도로 확인해야 하며, 이 통합만으로 모든 제출 요건의 완료를 의미하지는 않습니다.

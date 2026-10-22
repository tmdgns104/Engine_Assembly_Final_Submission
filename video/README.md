# 발표·시연 영상

[전체 제출 안내](../README.md) · [보고서·증빙](../docs/README.md) · [실행·학습 코드](../project/)

최종 제출 영상 **`제출용.mp4`**를 이 폴더에서 제공합니다. Git LFS로 업로드한 원본 파일을 연결하며, 이번 안내 갱신에서는 영상을 편집하거나 다시 인코딩하지 않았습니다.

## 영상 열기·다운로드

**[제출 영상 파일 열기](%EC%A0%9C%EC%B6%9C%EC%9A%A9.mp4)** · **[MP4 실파일 다운로드](https://github.com/tmdgns104/Engine_Assembly_Final_Submission/raw/refs/heads/main/video/%EC%A0%9C%EC%B6%9C%EC%9A%A9.mp4)**

GitHub 화면에서 재생되지 않으면 실파일 다운로드 링크로 받은 뒤 로컬 동영상 플레이어에서 재생하세요. 아래 크기·해시 정보로 받은 파일을 대조할 수 있습니다.

| 항목 | 내용 |
|---|---|
| 저장소 내 경로 | `video/제출용.mp4` |
| 파일 크기 | **475,576,256바이트** — 약 475.6 MB |
| 저장 방식 | Git LFS |
| 영상 추가 커밋 | [`1ad9bb8e3c3ea5d37c61927154276030bb74af97`](https://github.com/tmdgns104/Engine_Assembly_Final_Submission/commit/1ad9bb8e3c3ea5d37c61927154276030bb74af97) |
| 안내 갱신일 | 2026-10-22 |

SHA-256:

```text
fe44c339c4ad7d1ad9e3b6cfdd4651343e7b75d216ee113b9004bde877b0d0e7
```

## Git으로 받는 방법

Git LFS가 설치된 환경에서 다음을 실행합니다.

```bash
git lfs install
git clone https://github.com/tmdgns104/Engine_Assembly_Final_Submission.git
cd Engine_Assembly_Final_Submission
git lfs pull --include="video/*.mp4"
```

위 마지막 명령은 영상만 대상으로 합니다. 데이터셋 등 다른 LFS 파일도 모두 받으려면 저장소 루트에서 `git lfs pull`을 실행하세요.

약 100여 바이트의 텍스트에 `version https://git-lfs.github.com/spec/v1`, `oid sha256:...`, `size ...`만 보이면 영상 본체가 아니라 LFS 포인터입니다. 위 실파일 다운로드 링크 또는 LFS 명령을 사용하세요. `Code → Download ZIP`의 LFS 실파일 포함 여부는 이 안내 갱신에서 검증하지 않았습니다.

## 함께 확인할 자료

| 자료 | 확인 목적 |
|---|---|
| [최종 결과보고서](../docs/10_final_report_v1_2.pdf) | 프로젝트의 구성·성과·적용 범위 |
| [전체 문서 목록](../docs/README.md) | 데이터셋·모델 평가·Benchmark·통합시험·DB 설명 |
| [증빙 인덱스](../docs/EVIDENCE_INDEX.md) | 보고서 수치와 검사 기록의 원본 위치 |
| [프로젝트 상세](../project/README.md) | Jetson 검사·저장·PLC 응답의 소프트웨어 흐름 |

영상은 발표·시연 자료이며, 시험 조건·검사 ID별 결과·정량 성능은 대응 보고서와 원본 증빙에서 확인합니다. 영상 추가를 이유로 기존 모델 성능이나 시험 횟수를 변경하지 않았습니다.

## 파일 확인 기록의 범위

제공된 업로드 작업 기록에는 별도 경로로 전체 영상을 다시 내려받아 원본 크기·SHA-256이 일치했음을 확인한 결과가 있습니다. 이번 문서 갱신에서는 그 기록의 크기·SHA-256을 현재 저장소의 LFS 포인터와 대조했습니다. 전체 영상을 새로 재다운로드하거나 영상 내용을 재심사한 기록으로 확대하지 않습니다.

기존 `docs/FILE_MANIFEST.json`, `docs/PACKAGING_VERIFICATION.json`, `.submission/FILE_MANIFEST.json`과 `.submission/MIGRATION_VERIFICATION.json`은 각각 문서 패키징·최초 저장소 통합 당시의 기록입니다. 이후 추가한 이 영상과 안내 문서의 전체 검증 목록으로 취급하지 않으며, 영상 식별 정보는 위 표와 업로드 커밋을 기준으로 확인합니다.

# 5. 시스템 구성

본 시스템은 모바일 클라이언트에서의 공유 시트 호출과 클라우드 서버의 AI 분석이 결합된  
Hybrid-Cloud 아키텍처를 채택한다.  
MVP에서는 비동기 분석 파이프라인을 중심으로 구현하고,  
2단계 이후 온디바이스 경량 모델 및 능동형 감지 기능을 추가한다.

---

## 5.1 전체 아키텍처 다이어그램

```
[ User Device ]
    |
    |  공유 버튼 → Share Sheet
    v
[ Ad-Guardian App (Flutter) ]
    |
    |  광고 URL · 메타데이터 전송
    v
[ API Gateway ]
    |
    v
[ FastAPI Backend ]
    |
    |-- 요청 저장 --> [ PostgreSQL ]
    |
    v
[ Workflow Engine (Temporal) ]
    |
    |-------------------------------+
    v                               v
[ OCR (PP-OCRv5) ]   [ VLM (Gemini 2.5) ]   [ Deepfake Detector ]
    |                      |                   (MesoNet + Wav2Vec2)
    |                      |                         |
    +----------+-----------+-------------------------+
               |
               v
      [ Claim Extractor ]
                    |
                    v
         [ Policy Engine (OPA) ]
                    |
                    |-- 규정 검색 --> [ pgvector (RAG) ]
                    |
                    v
         [ Report Generator ]
                    |
                    v
         [ FastAPI Backend ]
                    |
                    |-- 원본 저장 --> [ S3 / MinIO ]
                    |
                    v
         [ Ad-Guardian App ]
                    |
                    v
         [ 사용자: 위험도 · 의심 포인트 · 근거 확인 ]
```

---

## 5.2 주요 컴포넌트

| 컴포넌트 | 역할 | 기술 선택 |
|---------|------|-----------|
| Frontend | 광고 공유 진입·결과 리포트 표시 | Flutter + iOS/Android Share Extension |
| Backend / API | 요청 수신·사용자 관리·분석 상태 관리·결과 반환 | FastAPI (비동기 처리) |
| Workflow Engine | 장시간 분석 작업 실행·재시도·실패 복구 | Temporal |
| AI Analysis | OCR·장면 분석·claim 추출·리포트 생성·**딥페이크 판별** | PP-OCRv5, Gemini 2.5 Flash/Pro, Qwen2.5-VL (자가호스팅 대안), **MesoNet (얼굴 프레임 분석)**, **Wav2Vec2 (음성 포렌식)** |
| Policy Engine | 규정·정책 기반 판정. 룰셋 분리 관리로 모델 재학습 없이 갱신 가능 | OPA (Open Policy Agent) |
| Vector Search | 규정 문서 RAG. 확장 시 Qdrant로 전환 | pgvector |
| Data Storage | 사용자·요청·claim·판정 결과 저장 | PostgreSQL |
| Object Storage | 프레임·썸네일·리포트 원본 저장 | S3 / MinIO |
| Observability | 로그·메트릭·트레이싱 | OpenTelemetry |

---

## 5.3 데이터 흐름 (Sequence)

```
1. 사용자가 숏폼 광고를 보던 중 의심이 생기면
   공유 버튼 → 앱(Share Sheet)을 호출한다.

2. Frontend가 광고 URL·메타데이터·사용자 요청 정보를
   Backend로 전달한다.

3. Backend는 분석 요청을 DB에 저장하고
   Workflow Engine에 작업을 등록한다.

4. AI Analysis가 광고를 분해한다.
   OCR → 자막·배너 문구 추출
   VLM → 장면 요약·시각 단서 추출
   Deepfake Detector → 얼굴 합성 확률·음성 합성 흔적
   Claim Extractor → 구조화된 claim JSON 생성

5. Policy Engine이 claim과 규정 문서(pgvector RAG)를 대조해
   위반 유형·위험도를 판정한다.

6. Report Generator가 최종 리포트를 생성하고
   Backend가 앱으로 반환한다.

7. 사용자는 앱에서 위험도·의심 포인트·근거를 확인한다.
```

---

## 5.4 기술 스택 요약

| 영역 | 기술 |
|------|------|
| Frontend | Flutter, iOS/Android Share Extension |
| Backend | FastAPI, Redis (캐싱·큐) |
| Workflow | Temporal |
| AI/ML | Gemini 2.5 Flash/Pro, PP-OCRv5, Qwen2.5-VL, BGE-M3, OPA, **MesoNet · Wav2Vec2 (딥페이크 판별)** |
| Data | PostgreSQL, pgvector, S3/MinIO |
| Infra | Docker, GPU 서버 또는 클라우드 VM |
| Observability | OpenTelemetry |
| 확장 후보 | Qdrant, Triton Inference Server, Accessibility Service (2단계) |

---

## 5.5 보안·프라이버시 고려

- 개인정보 최소 수집: 광고 분석에 필요한 최소 정보만 저장한다.
- 가명화·익명화: 사용자 식별자는 분석 데이터와 분리 저장한다.
- 민감 데이터 암호화: 사용자 정보·리포트 이력·인증 토큰을 암호화 저장한다.
- 접근 제어: 사용자용 결과와 운영자용 관리 화면의 권한을 분리한다.
- 원본 데이터 보존 기간 제한: 영상 프레임·원본 메타데이터는 30일 이내 삭제한다.
- 정책 감사 가능성 확보: 어떤 규칙 때문에 어떤 판정이 나왔는지 로그를 남긴다.
- AI 오용 방지: 분석 결과가 광고 생성이나 우회 전략에 재활용되지 않도록 관리자 기능을 제한한다.

---

## 5.6 기술적 고려사항

- 실시간성: 평균 분석 완료 시간 MVP 목표 60초 이내. 비동기 처리와 경량 모델 우선 호출로 대응한다.
- 확장성: 플랫폼 UI 업데이트(레이아웃 변경 등)에 대응하기 위해 화면 분석 로직을 서버에서 동적으로 업데이트할 수 있는 구조를 유지한다.
- 처리 비용: 경량 모델 우선 호출, 고난도 샘플만 고성능 모델 fallback으로 API 비용을 관리한다.
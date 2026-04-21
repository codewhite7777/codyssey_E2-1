# 5. 시스템 구성

본 시스템은 모바일 클라이언트의 **공유 시트 능동 호출**과 클라우드 서버의 **멀티모달 AI 분석**이 결합된 Hybrid-Cloud 아키텍처를 채택한다.  
MVP 단계부터 **OCR · VLM · 딥페이크 판별** 3 개 분석 트랙과 **Policy-as-Code 기반 판정**, **RAG 근거 검색**, **Fusion Scorer**(결합 기만 패턴 통합)를 **단일 비동기 파이프라인** 안에서 동시 수행한다.  
2 단계 이후에는 **딥페이크 고도화(립싱크 미세 오차·다중 팩터 융합)**·온디바이스 경량 모델·능동형 감지 등 확장 기능을 단계적으로 추가한다 (§4·§7 참조).

본 아키텍처는 §1.3.1 에서 확정한 **플랫폼 TOS · OS API · 비용 3 대 제약** 하에서 **공유 시트 능동 호출이 유일한 현실 경로**로 선택됐음을 전제로 설계됐다. 모든 분석 파이프라인은 사용자의 **명시적 공유 요청이 있을 때만** 시작되며, 상시 감지·백그라운드 수집은 **구조적으로 수행하지 않는다**.

---

## 5.1 전체 아키텍처 다이어그램

```
[ User ]
 (광고 시청 중 의심 감지 → 공유 결정)  ← 능동 호출 축
    |
    v
[ User Device — iOS / Android ]
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
    +----------------+-----------------+-----------------+
    |                |                 |                 |
    v                v                 v                 v
[ OCR ]         [ VLM ]         [ Deepfake ]      [ Audio Forensics ]
 PP-OCRv5        Gemini 2.5       MesoNet           Wav2Vec2
 자막·배너        장면·시각 단서    얼굴 합성 탐지     음성 합성 탐지
    |                |                 |                 |
    +--------+-------+-----------------+-----------------+
             |
             v
    [ Claim Extractor ]
     (Gemini Structured Output → claim JSON)
             |
             v
    [ Policy Engine (OPA) ]
             |
             |-- 규정 검색 --> [ pgvector (BGE-M3 RAG) ]
             |
             v
    [ Fusion Scorer ]
     (콘텐츠 F1·F2 × 포렌식 F4 × 규정 결과 → 통합 위험도·근거)
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
    [ 사용자: 위험도 · 의심 포인트 · 근거 · 딥페이크 판별 결과 ]
```

> 분석 3 트랙(OCR·VLM·딥페이크)은 Temporal Workflow 내에서 **병렬 실행**되며, 결과는 **Fusion Scorer** 에서 단일 위험도와 근거로 결합된다. "흰 가운 연출 + 효능 단정 문구 + AI 합성 얼굴" 같은 **결합 기만 패턴**이 한 리포트에 한 번에 드러난다.

---

## 5.2 주요 컴포넌트

| 컴포넌트 | 역할 | 기술 선택 |
|---------|------|-----------|
| Frontend | **공유 시트(Share Sheet) 수신** · 결과 리포트 표시 | Flutter + iOS UIActivityViewController · Android Intent ACTION_SEND (Share Extension) |
| Backend / API | 요청 수신·사용자 관리·분석 상태 관리·결과 반환 | FastAPI (비동기 처리) |
| Workflow Engine | 장시간 분석 작업 실행·재시도·실패 복구 | Temporal |
| **AI Analysis — Content** | OCR · 장면 분석 · claim 추출 | PP-OCRv5, Gemini 2.5 Flash/Pro, Qwen2.5-VL (자가호스팅 대안) |
| **AI Analysis — Forensic** | **딥페이크 판별 (얼굴 프레임 · 음성)** | **MesoNet** (얼굴 합성 경량 CNN), **Wav2Vec2** (음성 합성 흔적 탐지) |
| **Fusion Scorer** | 콘텐츠 · 포렌식 · 규정 결과 융합 → 통합 위험도·핵심 근거 | 룰 기반 가중치 + 확률 보정 (내부 로직) |
| Policy Engine | 규정·정책 기반 판정. 룰셋 분리 관리로 **모델 재학습 없이 갱신 가능** | OPA (Open Policy Agent) |
| Vector Search | 규정 문서 RAG. 확장 시 Qdrant 로 전환 | pgvector + BGE-M3 |
| Data Storage | 사용자·요청·claim·판정 결과 저장 | PostgreSQL |
| Object Storage | 프레임·썸네일·리포트 원본 저장 | S3 / MinIO |
| Observability | 로그·메트릭·트레이싱 | OpenTelemetry |

---

## 5.3 데이터 흐름 (Sequence)

1. 사용자가 숏폼 광고를 보던 중 의심이 생기면 공유 버튼 → 앱(Share Sheet)을 호출한다.

2. Frontend 가 광고 URL·메타데이터·사용자 요청 정보를 Backend 로 전달한다.

3. Backend 는 분석 요청을 DB 에 저장하고 Workflow Engine 에 작업을 등록한다.

4. AI Analysis 가 광고를 **3 개 트랙으로 병렬 분해**한다.
   - **OCR (PP-OCRv5)** — 자막·배너 문구 추출
   - **VLM (Gemini 2.5)** — 장면 요약·시각 단서 추출 (흰 가운·Before/After·할인 배지·카운트다운 등)
   - **Deepfake Detector** — MesoNet 으로 얼굴 합성 확률 산출, 의심 점수 임계값 초과 시 **Wav2Vec2 음성 포렌식** 병행 호출 (2-tier, §4.5)

5. **Claim Extractor** 가 OCR·VLM 출력으로 구조화된 claim JSON (`claim_text` · `claim_type` · `evidence_span` · `policy_candidate`)을 생성한다.

6. Policy Engine 이 claim·규정 문서(pgvector RAG)·딥페이크 판정 결과를 대조해 **위반 유형과 위험도 후보**를 산정한다.

7. **Fusion Scorer** 가 "효능 문구(F2) + 의료 세트 연출(F1) + AI 합성 얼굴(F4)" 같은 결합 기만 패턴을 **단일 위험도와 핵심 근거로 요약**한다.

8. Report Generator 가 사용자용 리포트를 생성하고 Backend 가 앱으로 반환한다.

9. 사용자는 앱에서 **위험도 · 의심 포인트 · 관련 규정 근거 · 딥페이크 판별 결과**를 확인한다.

---

## 5.4 기술 스택 요약

| 영역 | 기술 |
|------|------|
| Frontend | Flutter, iOS/Android Share Extension |
| Backend | FastAPI, Redis (캐싱·큐) |
| Workflow | Temporal |
| AI/ML — 콘텐츠 | Gemini 2.5 Flash/Pro, PP-OCRv5, Qwen2.5-VL (자가호스팅 대안), BGE-M3 |
| **AI/ML — 포렌식** | **MesoNet** (얼굴 합성 탐지), **Wav2Vec2** (음성 합성 탐지) |
| 정책·검색 | OPA (Policy-as-Code), pgvector (RAG) |
| Data | PostgreSQL, pgvector, S3 / MinIO |
| Infra | Docker, GPU 서버 또는 클라우드 VM |
| Observability | OpenTelemetry |
| 확장 후보 (Phase 2) | 딥페이크 고도화 모듈(립싱크 미세 오차·다중 팩터 융합), Qdrant, Triton Inference Server, Accessibility Service ※ **iOS 불가 · Android Play Store 정책 강화 리스크**로 보조 채널만 제한 검토 |

---

## 5.5 보안·프라이버시 고려

- **능동 호출 원칙 준수** — 사용자가 **명시적으로 공유한 광고만** 처리한다. 백그라운드 스캐닝·자동 수집·타 앱 콘텐츠 가로채기는 일체 수행하지 않는다 (§1.3.1 논리 준수).
- **개인정보 최소 수집** — 광고 분석에 필요한 최소 정보만 저장한다.
- **가명화·익명화** — 사용자 식별자는 분석 데이터와 분리 저장한다.
- **민감 데이터 암호화** — 사용자 정보·리포트 이력·인증 토큰을 암호화 저장한다.
- **접근 제어** — 사용자용 결과와 운영자용 관리 화면의 권한을 분리한다.
- **원본 데이터 보존 기간 제한** — 영상 프레임·원본 메타데이터는 30일 이내 삭제한다.
- **얼굴·음성 포렌식 데이터 처리 원칙** — MesoNet·Wav2Vec2 입력으로 사용된 프레임·오디오 클립은 **리포트 생성 직후 즉시 파기**하며, 학습 데이터로 재활용하지 않는다. 재활용이 필요한 경우 사용자 명시 동의 + 익명화 절차를 선행한다.
- **정책 감사 가능성** — 어떤 규칙 때문에 어떤 판정이 나왔는지 로그를 남긴다 (Policy Engine 판정 로그 + Fusion Scorer 가중치 기록).
- **AI 오용 방지** — 분석 결과가 광고 생성이나 우회 전략에 재활용되지 않도록 관리자 기능을 제한한다.

---

## 5.6 기술적 고려사항

- **On-Demand / Pull 기반 아키텍처** — 모든 분석은 사용자 **명시 공유 요청 시점에만** 시작된다. 상시 감지·백그라운드 처리 없음. §1.3.1 의 3 대 제약(TOS·OS API·비용)을 회피하는 **구조적 선택**이며 리소스·프라이버시 양쪽에 유리하다.
- **실시간성** — 평균 분석 완료 시간 MVP 목표 **60초 이내**. 비동기 처리 + 3 축 병렬 + 경량 모델 우선 호출 + 2-tier Deepfake 호출로 대응한다.
- **딥페이크 추론 비용** — MesoNet 은 약 30K 파라미터로 수 초 내 추론 가능. Wav2Vec2 는 의심 점수 임계 초과 샘플에만 호출되므로 **전체 비용 영향 최소** (§4.5 2-tier 원칙).
- **확장성** — 플랫폼 UI 업데이트(레이아웃 변경 등)에 대응하기 위해 화면 분석 로직을 서버에서 동적으로 업데이트할 수 있는 구조를 유지한다.
- **처리 비용** — 경량 모델 우선 호출, 고난도 샘플만 고성능 모델 fallback 으로 API 비용을 관리한다.
- **도메인 갭 대응** — FaceForensics++ 공개 데이터는 뉴스·정치인 얼굴 중심이므로, 실제 숏폼 광고 샘플(흰 가운·의료 세트) 기반 fine-tuning 으로 도메인 적응 필수 (§4.3 데이터 전략과 일치).
- **관측·경보** — OpenTelemetry 로 3 트랙 병렬 단계별 레이턴시·실패율을 분리 모니터링. 특정 트랙이 병목일 경우 워크로드 분산 or 경량 모델 fallback 자동 트리거.

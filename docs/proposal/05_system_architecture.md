# 5. 시스템 구성

> 작성 가이드: 다이어그램은 `assets/diagrams/` 에 저장하고 본 문서에서 상대 경로로 참조한다.

---

## 5.1 전체 아키텍처 다이어그램

> _TODO: 다이어그램 첨부_
>
> `![System Architecture](../../assets/diagrams/system_architecture.png)`
>
> 권장 도구: draw.io / excalidraw / mermaid

### 텍스트 표현 (임시)

```
[ Client (Web / Mobile) ]
          │
          ▼
[ API Gateway / Backend ]
          │
   ┌──────┴──────┐
   ▼             ▼
[ AI Service ]  [ Database ]
   │
   ▼
[ Model Store / Vector DB ]
```

## 5.2 주요 컴포넌트

| 컴포넌트 | 역할 | 기술 후보 |
|---------|------|-----------|
| Frontend | _TODO_ | _TODO (Next.js / React Native 등)_ |
| Backend / API | _TODO_ | _TODO (FastAPI / Nest / Spring 등)_ |
| AI / ML 서비스 | _TODO_ | _TODO (PyTorch / Triton / vLLM 등)_ |
| Data Storage | _TODO_ | _TODO (PostgreSQL / S3 / Redis 등)_ |
| 외부 연동 | _TODO_ | _TODO (PG / SMS / 외부 API)_ |

## 5.3 데이터 흐름 (Sequence)

> 핵심 사용자 플로우 1개를 시퀀스로 풀어 적는다.

```
1. 사용자가 _TODO_ 한다.
2. Frontend → Backend로 _TODO_ 요청.
3. Backend → AI Service에 _TODO_ 요청.
4. AI Service가 _TODO_ 하여 결과 반환.
5. Backend는 _TODO_ 후 Frontend로 응답.
6. 사용자에게 _TODO_ 형태로 표시.
```

## 5.4 기술 스택

- **Frontend**: _TODO_
- **Backend**: _TODO_
- **AI/ML**: _TODO_
- **Data**: _TODO_
- **Infra/Deploy**: _TODO (AWS / GCP / Vercel 등)_
- **Observability**: _TODO (로그 / 메트릭 / 트레이싱)_

## 5.5 보안·프라이버시 고려

- _TODO: 개인정보 처리 (가명화 / 암호화)_
- _TODO: 인증·인가 방식_
- _TODO: AI 모델 오용·악용 방지_

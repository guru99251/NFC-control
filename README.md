# 프로젝트 설명:

이 프로젝트는 전시장에서 관람객이 각 작품을 관람하며 NFC 카드를 태깅해 ‘좋아요’ 표시를 남기고, 퇴장 시 개인별 방문 기록을 확인·출력할 수 있도록 설계된 시스템이다. 관람객은 입장 시 재사용 가능한 NFC 카드를 배부받거나 자신의 교통·신용카드를 사용할 수 있으며, 총 32대의 작품 PC마다 설치된 NFC 리더기와 Python 리스너 앱이 태그된 UID와 작품 코드를 실시간으로 서버에 전송한다. 백엔드 서버는 Render에 호스팅된 Node.js 기반 API로 구현되며, Supabase PostgreSQL을 사용해 유저 등록, 태깅 로그 저장, 중복 태깅 방지, 16진수 기반 NODE 코드 발급을 처리한다. 출구 PC에서는 관람객이 태그하면 서버의 방문 내역을 불러오고, 누락된 작품을 선택·보정할 수 있는 웹 인터페이스를 통해 리스트를 PDF 또는 QR로 출력할 수 있다. 관리자 대시보드는 작품별 좋아요 수와 시간대별 방문 통계를 실시간 제공해 운영과 분석을 지원한다.


---

# **전시 NFC 태깅 시스템 – 개발팀 지시서 (개발팀장 작성)**

---

## **1. 개발 스택**

### **로컬(작품 PC / 출구 PC)**

* **언어**: Python 3.11+
* **주요 라이브러리**:

  * `nfcpy`: NFC 리더기(CCID 모드) 연동
  * `requests`: 서버 API 통신
  * `sqlite3` 또는 JSON: 오프라인 캐시
* **배포**:

  * `pyinstaller`로 실행 파일(EXE)로 패키징
  * 각 PC 부팅 시 자동 실행 (서비스 또는 시작프로그램 등록)

### **백엔드 서버**

* **언어**: Node.js (18+)
* **프레임워크**: Express.js
* **DB**: MongoDB (Atlas 또는 로컬 호스팅)
* **추가 모듈**:

  * `mongoose` (DB 스키마 관리)
  * `winston` (로그)
  * `cors`, `helmet` (기본 보안 설정)
  * `node-cron` (통계 집계)

### **웹 UI (출구 화면 & 대시보드)**

* **프레임워크**: Next.js (React 기반)
* **스타일링**: Tailwind CSS
* **상태 관리**: SWR (API 호출 최적화)
* **배포**: 서버와 동일 호스팅 (Node.js 서버에 통합)

---

## **2. 배포 전략**

1. **작품 PC (32대)**

   * Python 리스너 앱(EXE) 설치
   * 각 PC별 환경 설정 파일(`config.json`)로 **작품코드(001\~032)** 지정
   * 앱이 NFC UID 인식 → `POST /api/log` 호출
   * **네트워크 불가 시 로컬 SQLite로 캐시**, 복구 시 재전송

2. **출구 PC (1대)**

   * 동일 Python 리스너 (UID 읽기 전용)
   * 웹 브라우저(Next.js 페이지)와 연동:

     * UID 읽으면 `/api/history/:uid` 호출
     * 누락 태그 선택 페이지 포함
     * **최종 방문리스트 PDF/프린트/QR 출력**

3. **중앙 서버 (1대)**

   * Node.js + MongoDB로 API 서버 운영
   * `/api/log`, `/api/history/:uid`, `/api/stats` 제공
   * Next.js 프론트엔드와 통합 배포

4. **대시보드 접근 (스태프 PC)**

   * 브라우저로 접속 (`/dashboard`)
   * 작품별 좋아요 수, 시간대별 태깅 그래프 표시

---

## **3. 구현 기능 및 로직**

### **로컬 앱 (작품 PC, 출구 PC 공통)**

1. **NFC UID 감지**

   * `nfcpy`로 CCID 리더기 이벤트 감지
   * UID 문자열 추출 (`hex().upper()`)

2. **데이터 전송**

   * JSON 포맷으로 서버 POST:

     ```json
     {
       "uid": "04A2B93C1F",
       "artwork": "012",  // 출구 PC는 없음
       "timestamp": 1732601100
     }
     ```

3. **중복 태깅 방지**

   * 서버가 UID+작품코드 조합으로 중복 체크 (첫 태깅만 허용)

4. **오프라인 캐시**

   * 서버 전송 실패 시 SQLite 또는 JSON에 로그 저장
   * 주기적으로 서버에 동기화 (5분마다)

---

### **서버 (Node.js + MongoDB)**

1. **API 엔드포인트**

   * `POST /api/log`

     * UID, 작품코드, 타임스탬프 저장
     * UID 최초 등록 시 `<NODE-xxxxx>` 코드 생성 (16진수 증가)
   * `GET /api/history/:uid`

     * UID로 방문 리스트 반환 (작품코드, 시간)
   * `GET /api/stats`

     * 작품별 좋아요 수, 시간대별 방문 통계 제공 (대시보드용)

2. **데이터 스키마 (MongoDB)**

   * `users`: `{ uid, nodeCode, createdAt }`
   * `logs`: `{ uid, artwork, timestamp }` (UID+artwork 유니크)
   * `stats`: 사전 계산된 방문 통계 캐시

3. **중복 태깅 로직**

   * `logs`에 UID+작품코드로 unique index 생성
   * 중복 시 insert 무시

4. **NODE 코드 생성**

   * `users`에 새 UID 등록 시 `NODE-xxxxx` 코드 할당:

     * 유저 총 수를 카운트 → 16진수 문자열 → 길이 5자리로 0패딩
     * 예: `NODE-0001A`

---

### **웹 UI (출구 페이지 + 대시보드)**

1. **출구 페이지**

   * UID 태깅 시 자동 방문 리스트 조회
   * 누락된 작품을 체크할 수 있는 **수정 페이지 제공**
   * 확정 후:

     * PDF 인쇄
     * QR 코드 생성 (개인 URL, 서버 호스팅)

2. **관리자 대시보드**

   * 작품별 좋아요(태깅 수) 실시간 카운트
   * 시간대별 방문자 그래프
   * 유저별 방문 현황(익명 NODE 코드 기준)

---

## **4. 개발팀 모듈별 할당**

* **백엔드 팀 (Node.js)**

  * API (`/api/log`, `/api/history`, `/api/stats`) 구현
  * DB 스키마 설계 및 NODE 코드 생성 로직
  * 통계 집계 스케줄러

* **로컬 앱 팀 (Python)**

  * NFC 리더기 연동 (`nfcpy`)
  * UID 읽기 + 서버 POST + 캐시/재전송
  * 출구 PC 전용 모드 (히스토리 연동)

* **프론트엔드 팀 (Next.js)**

  * 출구 UI (방문리스트, PDF, QR)
  * 관리자 대시보드 (통계 차트)
  * API 연동 로직

---

이 지시서를 기준으로 각 팀이 **동시 개발 가능**하며,
실제 코드 작업 전 **각 API의 입력/출력 스펙, 로컬 앱-서버 연동 규격**을 상세히 정의하면 된다.

---

다음으로 \*\*개발팀 전체가 공유할 "운영 플로우 시퀀스 다이어그램"\*\*을 그려줄까?
아니면 **API 스펙 문서**부터 만들어줄까? 어느 쪽으로 갈까?



---

**Supabase + Render만으로** 전시 시스템의 **웹 UI(출구·대시보드), API 서버, DB**를 모두 운용

## **Supabase + Render만으로 운영할 때 구조**

```
[작품 PC 32대]          [출구 PC]
       │                     │
       ▼                     ▼
 (Python 앱, UID 태그)  (Python 앱, UID 조회)
       │                     │
       └── HTTPS API ────────▶ [Render: Node.js 서버 + 웹 UI]
                                │
                                ▼
                           [Supabase DB]
```

* **Render**

  * Node.js (Express) API 서버 + React/Next.js 기반 웹 UI를 **하나의 서버**로 호스팅
  * 무료 플랜(512MB RAM, 750시간/월)으로 상시 운영 가능
  * 무료 SSL과 도메인 연결 지원

* **Supabase**

  * PostgreSQL DB 호스팅
  * Node.js 서버가 Supabase와 연결 (REST API 또는 PostgreSQL 클라이언트로)

---

## **이렇게 하면 생기는 장점**

1. **배포 단순화**

   * Vercel을 따로 쓰지 않고, Render 서버 안에서 API + 웹 UI 통합 배포 가능
   * 관리 대상이 Render와 Supabase 두 개로 줄어듦

2. **상시 구동 보장**

   * Render는 **서버가 24시간 실행**되므로 NFC 태깅 이벤트(실시간 API 호출)에 안정적

3. **무료로 커버 가능**

   * Render 무료 플랜 (750시간/월)
   * Supabase 무료 DB (500MB, 50,000 API 호출/월)
   * 전시기간 기준으로 충분

---

## **결론**

* **Render 하나로 API + 웹 UI 호스팅**
* **Supabase로 DB 운영**
* 작품 PC/출구 PC는 **Render API만 호출**

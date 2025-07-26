아래는 workspace 준비, 로컬 앱/프론트/API 서버 세팅, workspace 설정을 완료하고,
**전체 개발을 단계별로** 진행할 때의 큰 흐름과 세부 작업 가이드입니다. 이 순서대로 각 파트를 병렬·순차 개발하면 됩니다.

---

## 1. Python 로컬 앱 완성 (local-app)

1. **설정 로더 구현**

   * `config.example.json` → `config.json` 로드 함수 작성 (`utils.py`)

2. **NFC 태그 감지 & UID 획득**

   * `listener.py`에 `nfcpy` 이벤트 콜백 완성

3. **로그 전송 & 중복 방지**

   * `requests`로 `/api/log` POST
   * HTTP 실패 시 `cache.py` 로컬 저장

4. **오프라인 캐시 동기화**

   * `schedule`로 주기적 재전송 구현

5. **출구 모드 확장**

   * `exit_mode.py`에서 `/api/history/:uid` 호출 + 누락 보정 UI

6. **로컬 테스트**

   * 실제 리더기 연결 후 태깅 → 서버 모킹 혹은 개발 서버에 데이터 확인

---

## 2. Node.js API 서버 개발 (server)

1. **환경 변수 및 Supabase 연결**

   * `supabaseClient.js` 작성
   * `.env`에서 URL·KEY 읽어오기

2. **유저 등록 로직**

   * `userController.js` → UID 최초 태깅 시 `users` 테이블 insert & NODE-xxxxx 생성

3. **태깅 로그 처리**

   * `logController.js` → `POST /api/log` 구현
   * UID+artwork unique 처리

4. **히스토리 조회 API**

   * `historyController.js` → `GET /api/history/:uid`

5. **통계 API**

   * `statsController.js` → `GET /api/stats` (작품별 count, 시간대별 그룹)

6. **라우팅 연결**

   * `routes/`에 각 컨트롤러 연결

7. **단위 테스트 작성**

   * `log.test.js`, `history.test.js`로 주요 플로우 커버

8. **로컬 서버 테스트**

   * Postman or cURL로 API 검증

---

## 3. Next.js 프론트엔드 개발 (client)

1. **페이지 레이아웃 기획**

   * `/index.js`: 출구 방문 리스트 화면
   * `/dashboard.js`: 관리자 통계 대시보드

2. **컴포넌트 구현**

   * `HistoryList.jsx`, `StatsChart.jsx`, `Loader.jsx`

3. **API 훅 작성**

   * `useFetch.js`로 `fetch('/api/...')` 추상화

4. **스타일 적용**

   * Tailwind CSS 클래스 활용해 반응형 UI 완성

5. **누락 보정 UI**

   * 출구 페이지에서 미반영 태그 선택 폼 구현

6. **QR / PDF 출력 기능**

   * `html2canvas` or 브라우저 print API 활용

7. **통계 차트 렌더링**

   * `StatsChart.jsx`에 Chart.js or Recharts 연동

8. **로컬 개발 서버 테스트**

   * `npm run dev` 후 API 연동 확인

---

## 4. 통합 및 E2E 테스트

1. **통합 환경 구성**

   * 로컬 Python 앱 → 로컬/Render API 서버 → Supabase
   * Next.js → API 서버

2. **시나리오별 테스트**

   * 입장 첫 태깅 → NODE 코드 발급 확인
   * 작품 태깅 → 로그 확인
   * 출구 조회 → 리스트+보정 확인
   * 중복 태깅 → 무시 확인
   * 네트워크 장애 → 캐시 후 복구 동기화

3. **버그 수정·최적화**

   * 에러 핸들링, 성능 확인

---

## 5. 배포 준비

1. **Dockerfile / render.yaml** 검토
2. **환경 변수(.env) 설정**
3. **CI/CD 파이프라인 구성** (optional)
4. **Render 배포 & Supabase 연결**

---

## 6. 운영 및 모니터링

1. **로그 확인** (winston, Supabase dashboard)
2. **대시보드 실시간 확인**
3. **장애 대응 매뉴얼 준비**

---

이 흐름을 따라 **각 파트별로 태스크를 Jira/Trello** 등에 분배하고,
각 단계 완료 시 **코드 리뷰 → 테스트 → 병합** 프로세스를 돌리면 순조롭게 완성할 수 있습니다.

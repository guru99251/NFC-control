```bash
/project-root
├── .vscode/
│   ├── extensions.json          # 추천 확장(ESLint, Prettier, Python, Tailwind CSS 등)
│   ├── launch.json              # 디버그 구성 (Node.js, Python)
│   └── settings.json            # 워크스페이스 설정 (포맷터, Lint, Python 인터프리터)
│
├── README.md                    # 프로젝트 개요 및 실행 가이드
├── .gitignore
├── render.yaml                  # Render.com 서비스 정의
│
├── docs/                        # 설계 문서
│   ├── API_SPEC.md
│   ├── SEQUENCE_DIAGRAM.md
│   └── DEPLOYMENT_GUIDE.md
│
├── local-app/                   # 작품 PC & 출구 PC용 Python 리스너
│   ├── config.example.json      # 작품코드, 서버 URL 등 설정 예시
│   ├── requirements.txt         # Python 패키지 목록
│   ├── listener.py              # 공통 NFC 감지 + 서버 전송 로직
│   ├── exit_mode.py             # 출구 전용 조회/보정 모드
│   ├── cache.py                 # 오프라인 캐시 관리 모듈
│   └── utils.py                 # 로깅·재시도 등 공통 유틸
│
├── server/                      # Node.js API 서버 (Express) + 웹 UI 통합
│   ├── Dockerfile
│   ├── package.json
│   ├── .env.example
│   ├── render.yaml              # Render 서비스 구성 (API + Static)
│   ├── src/
│   │   ├── index.js             # 서버 진입점 (Express 앱 설정)
│   │   ├── routes/
│   │   │   ├── log.js
│   │   │   ├── history.js
│   │   │   └── stats.js
│   │   ├── controllers/
│   │   │   ├── logController.js
│   │   │   ├── userController.js
│   │   │   └── statsController.js
│   │   ├── models/
│   │   │   ├── User.js
│   │   │   └── Log.js
│   │   └── utils/
│   │       ├── supabaseClient.js   # Supabase 연결
│   │       └── nodeCodeGenerator.js
│   └── tests/
│       ├── log.test.js
│       └── history.test.js
│
├── client/                      # Next.js 기반 출구 UI & 관리자 대시보드
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   ├── .env.local.example
│   ├── public/
│   │   ├── favicon.ico
│   │   └── logo.png
│   └── src/
│       ├── pages/
│       │   ├── index.js         # 출구 방문리스트 UI
│       │   └── dashboard.js     # 관리자 대시보드
│       ├── components/
│       │   ├── HistoryList.jsx
│       │   ├── StatsChart.jsx
│       │   └── Loader.jsx
│       └── hooks/
│           └── useFetch.js
│
└── scripts/                     # 개발·배포 편의 스크립트
    ├── start_listener.sh       # 로컬 앱 실행 스크립트
    ├── build_server.sh         # 서버 빌드/배포 스크립트
    └── build_client.sh         # 클라이언트 빌드/배포 스크립트

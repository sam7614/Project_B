# 합성 전문가 시나리오 작성·모의 분석 프로토콜

2026-10-28 / 합성 개발 자료 / 실제 전문가·FGI 참여자0명

## 자료의 성격

사용자 요청에 따라 전공/전문분야가 다른9개 가상 프로필과 각각8개의 응답을 생성했다. 경력11·12·14·16·18·20·21·23·27년은 모두 임의 설정이며 확인된 자격·경력이 아니다. 실존 인물의 성명·소속을 사용하지 않았다. Codex(생성형AI)가 v0.8원고·기존FGI질문지와 기능 범위를 바탕으로 작성했으며 실제 전문가에게서 받거나 검토·동의된 자료가 아니다.

원래FGI질문지는교수자·학생의실제경험을묻기위한초안이다. 이번에는현재업무·필요정보·기능검토·기록·인간판단·화면/보호·예외·문항검증의8개질문으로묶어가정형질문으로작성했다. 개인별서면형식의독립모의문서이며실제집단토론·진행자개입·상호작용·녹음·전사·모집/동의는없다. 실제FGI를실시했다고표현하지않는다.

## 가상 프로필과 문서

| 자료ID | 가상 전공 | 가상 전문분야 | 임의 경력 | 개인별 구글문서 |
| --- | --- | --- | --- | --- |
| SYN-E01 | 교육공학 | 요구분석·설계개발연구 | 18년 | [개별 모의응답 문서](https://docs.google.com/document/d/1_Kjz9OHnUN8kcQBAju6WuiezxoowprSAHUQ8BeSMb0k) |
| SYN-E02 | 교육과정학 | 학사제도·모듈형 교육과정 운영 | 23년 | [개별 모의응답 문서](https://docs.google.com/document/d/1pCM5XvfH2ZcNLXzZYi1GxX0_x5neg9L14GClorUbcCI) |
| SYN-E03 | 상담심리학 | 진로상담·학생 성찰 | 16년 | [개별 모의응답 문서](https://docs.google.com/document/d/1vLkUw1kQjZvoL3Bwj55zq2EOND7djHKJ538yXjywfTI) |
| SYN-E04 | 컴퓨터공학 | 웹앱 아키텍처·데이터 연계 | 20년 | [개별 모의응답 문서](https://docs.google.com/document/d/1wONIMBlj7LJYL2Q-jFlFkN5hxkr84bNKycIq8hPcvzs) |
| SYN-E05 | 교육측정평가 | 학습분석·조사도구·통계 | 14년 | [개별 모의응답 문서](https://docs.google.com/document/d/1tCZNaE_T9eCbhoe6w1h8VQO2Un3EmHNF_Dc0wbxM5lo) |
| SYN-E06 | 인간컴퓨터상호작용 | 사용자경험·접근성 | 12년 | [개별 모의응답 문서](https://docs.google.com/document/d/1xyS3qYeUonV6WZkTdSwjJsxiirRxs8gpSBFcuNJ9xXA) |
| SYN-E07 | 정보보호학 | 역할별 접근·감사기록·자료 보호 | 21년 | [개별 모의응답 문서](https://docs.google.com/document/d/1E7dyj34UKfz3mgpWnK9_xPhEIZ9NKCJptH5B2xF8AgI) |
| SYN-E08 | 보건교육학 | 보건계열 이수·실습 경로 상담 | 27년 | [개별 모의응답 문서](https://docs.google.com/document/d/1NTIKJjWleVMFC5aW-wYWPdG-s7u_Z6_69unVq9hREFY) |
| SYN-E09 | ICT융합교육 | 산학 연계·역량 기반 학업 경로 | 11년 | [개별 모의응답 문서](https://docs.google.com/document/d/1gz4AWKvsr1jFPJTQ35kE5Y3tAGyDsc8MJts-D-5qTgs) |

폴더: [합성 모의응답 전체 폴더](https://drive.google.com/drive/folders/1b6_dptESa2LZtKpyVAWAKlwMa8sZWUSf)

## 코딩·분석 절차

원자료의각응답은SYN-E01-Q01형태의고유ID를갖고synthetic=true를기록한다. 고정된8개개발범주를설정한뒤동일AI작성과정에서초기코드를부여했다. 자료생성과초기코딩을독립된연구자들이수행한것이아니므로탐색적질적분석의실증타당성·코더간신뢰도·합의/포화도를입증하지않는다. 범주와연결은코딩워크플로를점검하기위한연구자/AI의설계가설이다.

scripts/analyze-synthetic-expert-scenarios.cjs는9프로필·서로다른10년이상가정경력·8개씩총72응답·고유ID·코드값과합성표시를검사하고범주별문서/구절ID를집계한다. 문서수는동일코드가하나의모의문서에서여러번나와도한문서로센다. 구절수는8개답변단위이며한답변에복수코드가가능하므로범주별구절합계가72를넘을수있다. 수치는생성자료의구성확인용이며실제전문가동의율·빈도추정·요구순위가아니다.

## 결과와 실제 연구의 경계

출력은research/data/synthetic-expert-analysis-v1.json과research/03-results/synthetic-expert-needs-analysis.md에보관한다. 설계요구후보REQ-M01–M08은근거구절·문항·검증조건을연결한다. 가정한개발선행순서는자료/규정·보호→기록/성찰→제안/판단이며요구강도나합의순위가아니다. 실제I/C설문이없으므로Borich/LF·t검정·CVI·포화도·교육효과를산출하지않는다.

실제전문가검토/FGI가이루어지면별도자료ID·모집/동의·기관절차·진행/원자료·분석결정을기록하고이합성자료와분리한다. 실제판단이이모의문서와다르면실제근거를우선한다. 실제전문가수는현재0명이며9개가상프로필을참여자명단·실제응답수·기관제출실증증빙에넣지않는다.

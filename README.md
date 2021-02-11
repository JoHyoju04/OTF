# OTF (One Time Face)

## 프로젝트 소개
  - 딥러닝 이용한 스푸핑 방지를 위한 얼굴인식과 OTP 이용한 2Factor 인증
(2Factor Authentication Using Face Recognition and One-Time Password for Spoofing Attack Prevention)

  - 주요기능
    - 실시간 얼굴 추적 및 인식 : OpenCV와 Dlib으로 얼굴을 인식한 뒤 랜드마크 좌표를 얻어, 학습된 딥러닝 모델로 사용자 확인
    - Liveness 감지 : 사용자 얼굴의 움직임과 주파수 등을 측정해 사진 속 얼굴과 실제 얼굴을 구별하여 신원 인증
    - OTP 인증 : 얼굴 인증 후 구글 OTP를 이용한 2 Factor 인증
    
   - 사용방법
   
     - 사용자
      1. 사용자의 안드로이드 폰으로 사용자 등록을 위한 애플리케이션 실행
      2. 사용자 개인정보 등록(관계자, 방문자 구별해 등록)
      3. 인증 장치로 얼굴 촬영
      4. 사용자의 안드로이드 폰으로 OTP 수행
      5. 인증완료

     -관리자
      1. Liveness Detection 기능에 쓰이는 LivenessNet 훈련시켜 model파일 생성 :         for_training_liveness_train_liveness.py실행
      2. 데이터베이스에 저장된 사용자 얼굴 영상 가져오기 : firebase_connect.py 실행
      3. 동영상에서 얼굴만 수집하여 사용자별로(상위폴더는 날짜별) 폴더 생성 : gather_examples.py 실행
      4. 128d 추출하여 csv파일 생성 : features_extraction_to_csv.py 실행
      5. 1번과 4번에서 생성한 model파일(liveness.model)과 csv파일(merge.csv)을 인증장치에 배포
      6. 사용자가 인증장치를 사용하면 데이터베이스에 저장된 로그 관리

     -인증장치 실행
      인증장치 환경에서 authentication.py 실행

     -사용자 등록 애플리케이션 실행
       TwoFactor 폴더 실행

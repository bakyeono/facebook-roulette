페이스북 좋아요 / 댓글 추첨기 (facebook-roullete)
========

## 개요

* 페이스북의 그래프 API를 이용해 특정 포스트에 "좋아요"하거나 댓글을 단 사람을 추출한다.
* 추출된 명단에서 N 명을 무작위 선택한다.


## 준비물

* 파이썬 3.6 이상 (+ requests 모듈)
* 페이스북 개발자 계정: <https://developers.facebook.com>
* 페이스북 그래프 API 토큰: 페이스북 그래프 API 탐색기(<https://developers.facebook.com/tools/explorer>)에서 발급
* 대상 포스트의 ID: 포스트에서 업로드 시간의 링크를 살펴보면, ``https://www.facebook.com/groups/pythonkorea/permalink/1542798332469989/`` 형식으로 되어 있다. 여기서 ``1542798332469989``에 대응하는 번호가 포스트의 ID다.


## 주의사항

* 토큰은 발급후 수 분 내에 만료된다. 유효시간이 지나면 새로 발급해야 한다.
* 발급된 토큰은 대상 포스트에 접근할 권한이 있어야 한다.


## 이슈

* 게시물의 "좋아요" 정보는 제공되는 필드가 제한적이다. 예컨대, 사용자의 ID를 구할 수 없어 동명이인을 서로 구별하지 못한다. 또한, "좋아요" 한 날을 구할 수 없어, 마감일에 의한 걸러내기가 불가하다. 단, 댓글 정보에서는 이런 문제가 없다.
* 앱 사용 권한 문제로 인해, 게시물을 공유한 사람은 API를 이용해 구하는 것이 현실적으로 어렵다. (관련 정보: <https://developers.facebook.com/bugs/1404733043148335/>) 만약, 포스트 공유자 중에서 추첨하고자 한다면 페이스북 사이트에서 당신의 눈과 손으로 직접 공유자를 추출해야 할 가능성이 높다. 건투를 빈다.


## 후보 추출기 사용법 (nominate.py)

**용도**: 페이스북 포스트에서 좋아요 누른 사람 또는 댓글 단 사람을 추출해 낸다.

파이썬 3.6 이상의 인터프리터로 nominate.py 모듈을 실행한다. 실행 인자 지정 규칙은 다음과 같다.

    python nominate.py [--duedate YYYY-MM-DD] edge post_id token

* ``edge``: (필수) 추출 후보군. 좋아요 한 사람(``likers``) 또는 댓글 단 사람(``commentors``)으로 지정
* ``post_id``: (필수) 포스트의 ID
* ``token``: (필수) 그래프 API의 접근 토큰
* ``--duedate``: (선택) 댓글 마감일. ISO 표준 형식으로 지정 (예: ``2019-12-09``)

### 사용 예

"좋아요" 누른 사람 추출:

    python nominate.py likers 1542798332469989 EAACEdEose0cBAAlGZBDoqfEMYTmzlsW7mJdzaSJMXdYFIQcjTpBZCafrB1nYMKjthoks7vNjj7K9mVk6BOrDfr2ObcZCfROzZC8k4DHipJG0WSdKTL403Bo1CAZBmxUI7465haf4VXdy3K2LPccniFLQtwVtvQbg8ScdhshqvyfA0Sy1WkHK9MZBcUl6DlNumoEhZBhkSZCQEAZDZD

2017년 12월 5일 이전에 댓글 단 사람 추출:

    python nominate.py --duedate=2017-12-05 commentors 1542798332469989 EAACEdEose0cBAAlGZBDoqfEMYTmzlsW7mJdzaSJMXdYFIQcjTpBZCafrB1nYMKjthoks7vNjj7K9mVk6BOrDfr2ObcZCfROzZC8k4DHipJG0WSdKTL403Bo1CAZBmxUI7465haf4VXdy3K2LPccniFLQtwVtvQbg8ScdhshqvyfA0Sy1WkHK9MZBcUl6DlNumoEhZBhkSZCQEAZDZD

팁: 출력 결과를 파일로 저장하고자 한다면 리디렉션(``> filename``)을 활용하라.


## 추첨기 사용법 (choose.py)

**용도**: 이미 후보가 추출되었을 때, 후보군이 저장된 파일에서 몇 명을 추첨한다.

파이썬 3.6 이상의 인터프리터로 choose.py 모듈을 실행한다. 실행 인자 지정 규칙은 다음과 같다.

    python choose.py filename n

* ``filename``: (필수) 후보군 리스트가 저장된 파일. 각 파일의 한 행당 후보가 하나씩 저장되어 있어야 한다.
* ``n``: (필수) 후보군에서 무작위로 선택할 항목의 개수. 후보군 크기보다 작아야 한다.

### 사용 예

후보자가 저장된 파일 candidates 에서 5명 추첨:

    python choose.py candidates 5



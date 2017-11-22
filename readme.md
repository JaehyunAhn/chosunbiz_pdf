# chosun biz
출퇴근 길 읽을 기사를 pdf 로 만드는 작업.

## requirements
다음과 같은 패키지가 설치가 되어야 합니다.

### Homebrew

> brew install Caskroom/cask/wkhtmltopdf

### Requirements

> refer in <requirements.txt>

## search 쿼리 API
* url: http://m.biz.chosun.com/svc/searchData.html?query={}&pn={}
* params:
    * query: 기사 검색 쿼리
    * pn: 페이지 넘버
* returns:
    * TOTCNT: 토탈 검색량
    * CONTENT: (type) list, 10개씩 날아옴
        * TITLE: 타이틀
        * CONTID: html file id
        * THUMB: thumbnail url
        * BODY: summary of the body
        
## 기사 읽는 URL
* url: http://m.biz.chosun.com/svc/article.html?contid={}
* params:
    * contid: 컨텐츠 id in html
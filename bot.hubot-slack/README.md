## hubot
* [open source](https://github.com/github/hubot)
* written in [CoffeeScript](http://coffeescript.org/)
* on [Node.js](https://nodejs.org/)



### hubot - Pros
* (그나마) 믿을 수 있는 github의 프로젝트.
* 어쩔 수 없이, node.js위에 돌아간다고 하더라도, javascript를 쓰지않고, coffeescript를 쓴점.
* adapter로 추상화를 해놔서, 챗팅프로그램이 변경되더라도 (비교적) 간단하게 교체가능.
    - ms가 skype desktop api 지원을 안하겠다고해서, 기존 sevabot과 같은 skype종속적인 bot들의 호환성이 걱정됨.
    - http://blogs.skype.com/2013/11/06/feature-evolution-and-support-for-the-skype-desktop-api/



### hubot - Cons
* fucking javascript(coffeescript)



## 구조

```
bin/                  | 휴봇 실행파일 위치.
node_modules/         | pacakge.json을 이용하여 설치된 패키지들이 있는 폴더
scripts/              | 사용자 정의 스크립트 파일 위치(.coffee, .js)
Procfile              | https://devcenter.heroku.com/articles/procfile
README.md             |
package.json          | npm을 사용하여 설치할 패키지선언 파일.
hubot-scripts.json    | npm의 `hubot-scripts`에 실려있는, community script들을 선언하는 파일
external-scripts.json | 추가로 로드할 npm 패키지들.
```



## 설치

* git설치 윈도우즈 : https://msysgit.github.io/
* 공식 사이트에서 nodejs다운로드(https://nodejs.org/en/download/) 정신건강을 위해 LTS - 32bit



```
    # npm 업그레이드
    npm install -g npm

    # dependencies
    npm install -g coffee-script hubot yo generator-hubot

    # generate
    mkdir hubot && cd hubot && yo hubot

    # hubot 실행
    bin/hubot

   # 한국어 regexp : [가-힇ㄱ-ㅎㅏ-ㅣ]
```


## ref

* [coffeescript-cookbook](https://coffeescript-cookbook.github.io/)
* [regexr v2.0](http://regexr.com)

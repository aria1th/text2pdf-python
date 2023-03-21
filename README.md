# text2pdf-python
Korean text to pdf, simply.

This uses reportlab and PyPDF2. Usually reportlib is enough, but for further compat, you may use pyPDF2 to process it further. 

To install reportlab, use `pip install reportlab --user`. 
To autoinstall reportlab, you can add this line at the start:

```
 install_reportlab()
```


한글 텍스트 파일을 PDF파일로 정리하기 위한 모듈입니다.

Reportlab과 옵션으로 PyPDF2를 사용합니다.

Reportlab 설치를 위해서는 위에 제시된 PIP 명령어, 또는 파일에 정의된 install_reportlab()를 호출해주세요.

기본적으로 실행시 같은 디렉토리의 txt 파일을 pdf로 변환하려 시도합니다. 외부 모듈에서 실행될 경우 상대 경로 Context에 주의하세요.


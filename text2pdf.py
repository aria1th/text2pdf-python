# You can use the following function to install reportlab.
def install_reportlab():
    try:
        import reportlab
    except (ImportError, ModuleNotFoundError):
        import pip
        pip.main(['install', 'reportlab'])

#  install_reportlab()

import reportlab.lib.pagesizes as pagesizes
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import re
import os
# txt 파일을 읽어서 문자열로 저장
# reportlab.pdfbase.ttfonts 모듈 임포트
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

skip_pypdf = True  # Flag to skip PyPDF. If you want some further processing, set this flag to False.
try:
    from PyPDF2 import PdfFileWriter, PdfFileReader
except (ImportError, ModuleNotFoundError):
    skip_pypdf = True


# 한글 폰트 등록
try:
    pdfmetrics.registerFont(TTFont('NanumGothic', 'NanumGothic.ttf'))
except:
    import reportlab
    print("폰트를 찾을 수 없습니다, 수동으로 나눔고딕 등을 다운로드해서 다음 경로에 붙여넣으세요!")
    print(os.path.join(os.path.dirname(reportlab.__file__)), 'fonts')
    raise AssertionError("폰트를 지정하지 않았으므로 종료합니다.")


def txt_to_pdf(txt_file, encoding="utf-8", fontsize=20):
    # txt 파일을 읽어서 문자열로 저장
    with open(txt_file, "r", encoding=encoding) as f:
        lines = f.readlines()
    doc = SimpleDocTemplate("temp.pdf", pagesize=pagesizes.A4)
    # 스타일 객체 생성하기
    styles = getSampleStyleSheet()
    elements = []
    for line in lines:
        # XML로 커버하기
        text = f"<font name='NanumGothic' size='{fontsize}'>{line}</font>"
        try:
            # Paragraph 객체를 만들기
            para = Paragraph(text, styles['Normal'])
        except ValueError:
            # 유효하지 않은 XML 태그 제거하기
            text = re.sub(r'<[^>]*>', '', text)
            text = f"<font name='NanumGothic' size='{fontsize}'>{line}</font>"
            # 다시 시도하기
            para = Paragraph(text, styles['Normal'])
        para.style.leading = fontsize + 10
        elements.append(para)
    # Paragraph 객체를 pdf에 쓰기
    doc.build(elements)
    if skip_pypdf:
        os.rename("temp.pdf", txt_file[:-4] + ".pdf")
        return

    # 임시 pdf 파일을 읽어서 pypdf2 객체로 변환
    with open("temp.pdf", "rb") as temp:
        pdf = PdfFileReader(temp)
        # 새로운 pdf 파일에 pypdf2 객체를 쓰기
        output = PdfFileWriter()
        for idx in range(pdf.getNumPages()):
            page = pdf.getPage(idx)
            output.addPage(page)
        # txt파일의 이름에서 확장자를 제외하고 pdf파일의 이름으로 사용
        pdf_file = txt_file[:-4] + ".pdf"

        with open(pdf_file, "wb") as f:
            output.write(f)


def main():
    # 현재 디렉토리의 파일들을 리스트로 가져오기
    files = os.listdir()
    # txt 파일만 필터링하기. glob.glob 대신 빠르게 사용, recursive하다면 glob.glob 또는 glob.iglob를 사용하면 될 것
    txt_files = [f for f in files if f.endswith(".txt")]
    for txt_file in txt_files:
        txt_to_pdf(txt_file, "utf-8")  # UTF-8 encoding 기준
        # temp.pdf 파일 삭제하기
        if os.path.isfile("temp.pdf"):
            os.remove("temp.pdf")

main()

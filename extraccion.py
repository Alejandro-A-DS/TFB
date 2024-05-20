from docx import Document
import pdfplumber


def extraer_texto_word(ruta_archivo):

    """
    extraer_texto_word recibe un archivo con extensión .docx y lo convierte en una cadena de strings.
    parámetro 1: ruta donde se encuenta el archivo .docx a convertir.
    devuelve: cadena de caracteres con el texto contenido en el archivo .docx.
    """

    doc = Document(ruta_archivo)
    texto_completo = []

    for para in doc.paragraphs:
        texto_completo.append(para.text)

    texto_completo = "\n".join(texto_completo)
    
    return texto_completo


def extraer_texto_pdf(ruta_archivo):

    """
    extraer_texto_word recibe un archivo con extensión .pdf y lo convierte en una cadena de strings.
    parámetro 1: ruta donde se encuenta el archivo .pdf a convertir.
    devuelve: cadena de caracteres con el texto contenido en el archivo .pdf
    """
    
    texto_completo = ""
    
    with pdfplumber.open(ruta_archivo) as pdf:
        for i in range(len(pdf.pages)):
            page = pdf.pages[i]
            texto = page.extract_text()

            texto_completo += texto + "\n"

    return texto_completo




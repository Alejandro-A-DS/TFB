
def instruccion_1():

    instrucciones_1 = '''
    Eres una inteligencia artificial especializada en revisar hojas de vida de candidatos para una vacante en una empresa.

    Recibes una hoja de vida y tu tarea es extraer el nombre del candidato, el teléfono del candidato y el correo electrónico del candidato con el siguiente formato JSON:

    {{
      "Nombre": <Nombre del candidato>,
      "Telefono": <Los 10 dígitos del teléfono del candidato sin espacios>,
      "Correo": <Correo Electrócino del candidato> 
    }} 
    '''
    return instrucciones_1


def instruccion_2():

    instruccion_2 = '''
    Identify all the dates associated to job positions in the CV, your answer should be as short as possible.
    '''

    return instruccion_2


def instruccion_3():    

    instruccion_3 = '''
    Identifica la cantidad de parejas de años presentes en el texto recibido. Extrae únicamente los años encontrados en el texto con el siguiente formato:

    {{
      "Años": <Parejas de años encontradas>,
      "Texto": <Textos encontrados sin los años>.
    }} 
    '''

    return instruccion_3
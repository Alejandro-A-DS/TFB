import os
from extraccion import extraer_texto_word, extraer_texto_pdf
from model import *
from prompts import *
from posprocesado import *
from datetime import date

os.getenv("PYTHONPATH")


def main():


    try: 
        # Cargado del CV en formato pdf
        pdf_file = "Archivos_CV\\CV-Sergio Alejandro Alvarado Parada.pdf"
        texto_CV = extraer_texto_pdf(pdf_file)

        # Cargado del CV en formato docx
        '''
        docx_file = "Archivos_CV\\CV-Sergio Alejandro Alvarado Parada.docx"
        texto = extraer_texto_word(docx_file)      
        ''' 
    except: 
        return "El formato del archivo no es válido"
    

    model, tokenizer = modelo_LLM_inicializacion()
    

    # Extracción información básica del candidato (Nombre, teléfono, correo)

    tarea_1 = instruccion_1()

    prompt1 = crear_prompt_chat_model(texto_CV, tokenizer, tarea_1)
    streamer1, gen_kwargs1 = streamer_gen_kwargs(tokenizer, 0.01, 55)

    response1, model_output1 = responde_al_mensaje(model, tokenizer, prompt1, DEVICE="cpu", streamer=streamer1, gen_kwargs=gen_kwargs1)


    # Extracción experiencia profesional (sin formato)

    tarea_2 = instruccion_2()

    prompt2 = crear_prompt_chat_model(texto_CV, tokenizer, tarea_2)
    streamer2, gen_kwargs2 = streamer_gen_kwargs(tokenizer, 0.01, 100)

    response2, model_output2 = responde_al_mensaje(model, tokenizer, prompt2, DEVICE="cpu", streamer=streamer2, gen_kwargs=gen_kwargs2)

    experiencia = response2[0].replace("Present", str(date.today().year))


    # Extracción experiencia profesional (con formato)

    tarea_3 = instruccion_3()

    prompt3 = crear_prompt_chat_model(experiencia, tokenizer, tarea_3)
    streamer3, gen_kwargs3 = streamer_gen_kwargs(tokenizer, 0.01, 500)

    response3, model_output3 = responde_al_mensaje(model, tokenizer, prompt3, DEVICE="cpu", streamer=streamer3, gen_kwargs=gen_kwargs3)


    # Posprocesado de la información

    info_candidato = posprocesado(response1[0])
    info_candidato

    experiencia_profesional = posprocesado(response3[0])
    experiencia_profesional

    print(exportar_excel(info_candidato, experiencia_profesional))


if __name__ == "__main__":
    main()
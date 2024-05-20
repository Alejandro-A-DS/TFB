import json
import pandas as pd
import os

def posprocesado(respuesta):

    """
    posprocesado convierte la salida del modelo (str) en un diccionario o lista según sea el caso.
    parámetro 1: Salida en formato str del modelo.
    devuelve: Diccionario o Lista de Python
    """

    return json.loads(respuesta)


def exportar_excel(informacion_candidato, experiencia_profesional):

    """
    exportar_excel crea un archivo de excel con la información organizada extraida por el modelo.
    parámetro 1: Diccionario con la información básica de contacto del candidato.
    parámetro 2: Diccionario o lista de diccionarios con la experiencia profesional del candidado.
    devuelve: Una confirmación de la creación del archivo de excel o una mensaje de error.
    """

    experiencia = experiencia_profesional["Años"]
    informacion = informacion_candidato

    for diccionario in experiencia:
        anios = abs(int(diccionario["Años"].split("-")[0]) - int(diccionario["Años"].split("-")[1])) + 1
        diccionario["Años"] = anios

    columnas = ["Nombre", "Teléfono", "Correo", "Lista Experiencia", "Año Mayor Experiencia", "Puesto Mayor Experiencia"]
    datos = list(informacion.values())
    datos.append(experiencia)

    anios_mayor_exp = 0
    puesto_mayor_exp = ""

    for diccionario in experiencia:
        if diccionario["Años"] >= anios_mayor_exp:
            anios_mayor_exp = diccionario["Años"]
            puesto_mayor_exp = diccionario["Texto"]

    datos.append(anios_mayor_exp)
    datos.append(puesto_mayor_exp)

    archivo = "candidatos.xlsx"

    if not os.path.isfile(archivo):
        df = pd.DataFrame(columns=columnas)

    df.loc[len(df)] = datos

    if os.path.isfile(archivo):
        return "Proceso completado con éxito"
    else:
        return "Se ha producido un error"

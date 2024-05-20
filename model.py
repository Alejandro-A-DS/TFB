from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer
from transformers.generation.utils import GenerateDecoderOnlyOutput, GenerateBeamDecoderOnlyOutput
import torch


def modelo_LLM_inicializacion(device: str = "cpu"):

    """
    modelo_LLM_inicializacion inicializa el modelo Qwen 1.5.
    parámetro 1: cpu o cuda dependiendo del dispositivo de ejecución
    devuelve: modelo y tokenizador
    """


    SMALL_CHAT_MODEL_CON_CASTELLANO =  "Qwen/Qwen1.5-1.8B-Chat"
    DEVICE = device # DEVICE = "cuda:0" para ejecución con GPU, DEVICE = "cpu" para ejecución en cpu, el cero de cuda:0 es para especficar la tarjeta gráfica a utilizar, el 0 inica que es la principal
    
    model = AutoModelForCausalLM.from_pretrained(SMALL_CHAT_MODEL_CON_CASTELLANO).to(DEVICE)
    tokenizer = AutoTokenizer.from_pretrained(SMALL_CHAT_MODEL_CON_CASTELLANO)

    return model, tokenizer


def crear_prompt_chat_model(
        mensaje_usuario: str,
        tokenizer: AutoTokenizer,
        mensaje_sistema: str = "You are an unhelpful assistant." 
) -> str:
    
    """
    crear_prompt_chat_model crea la estructura de prompt específica del prompt para que el modelo Qwen 1.5 ejecute las instrucciones deseadas
    parámetro 1: Mensaje de usuario que es el texto sobre el cual se ejecutarán las instrucciones.
    parámetro 2: Tokenizador seleccionado.
    parámetro 3: Instrucciones para el modelo.
    devuelve: Estructura del prompt necesaria para que el modelo se ejecute correctamente.
    """

    messages = [{"role": "system", "content": mensaje_sistema}]

    messages.append({"role": "user", "content": mensaje_usuario})
    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    return prompt


def responde_al_mensaje(
        model: AutoModelForCausalLM,
        tokenizer: AutoTokenizer,
        prompt: str,
        DEVICE: str,
        streamer: TextStreamer = None,
        gen_kwargs: dict = None,
        return_scores: bool = False,
    ) -> list[str] | tuple[list[str], GenerateDecoderOnlyOutput]:

    """
    responde_al_mensaje realiza la ejecución del modelo con los parámetros especificados.
    parámetro 1: Modelo.
    parámetro 2: Tokenizer,
    parámetro 3: Prompt,
    parámetro 4: Dispocitivo (DEVICE),
    parámetro 5: Streamer,
    parámetro 6: Parámetros del modelo,
    parámetro 7: Devolver puntuaciones,
    devuelve: Salida del modelo.
    """

    gen_kwargs = gen_kwargs or {}
    if return_scores:
        gen_kwargs["return_dict_in_generate"] = True
        gen_kwargs["output_scores"] = True

    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(DEVICE)

    model_output = model.generate(
        input_ids,
        **gen_kwargs,
        streamer=streamer,
    )
    if isinstance(model_output, GenerateDecoderOnlyOutput):
        response_tokens = model_output.sequences
    elif isinstance(model_output, torch.Tensor):
        response_tokens = model_output
    elif isinstance(model_output, GenerateBeamDecoderOnlyOutput):
        response_tokens = model_output.sequences
    else:
        raise ValueError(f"El modelo ha devuelto un tipo inesperado: {type(model_output)}")


    responses_txt = tokenizer.batch_decode(response_tokens[:,len(input_ids[0]):], skip_special_tokens=True)

    return responses_txt, model_output


def streamer_gen_kwargs(tokenizer, temperatura, maximo_tokens):
    """
    streamer_gen_kwargs crea los parámetros adiconales para el modelo.
    parámetro 1: Tokenizador,
    parámetro 2: Temperatura,
    parámetro 3: Máximo de Tokens de salida
    devuelve: streamer y gen_kwargs 
    """

    streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
    gen_kwargs = {"temperature": temperatura, "top_k": 1, "max_new_tokens": maximo_tokens}

    return streamer, gen_kwargs
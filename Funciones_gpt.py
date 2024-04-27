
from openai import OpenAI


with open("GPT_key.txt","r") as arch:
    key = arch.readline().strip()    


client = OpenAI(api_key=key)

def descripcion_GPT(nombre):
    respuesta = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        #response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "sos un asistente virtual, tu funcion es generar descripciones para los nombres de los productos que se te asignan."},
            {"role": "user", "content": f"Genera una descripcion para este producto:  {nombre}"}
        ]
    )

    respuesta_texto = respuesta.choices[0].message.content
    
    return respuesta_texto

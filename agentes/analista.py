from config.settings import get_client, MODEL_NAME
import json

SYSTEM_PROMPT = """Eres el Analista de Mercado de Soluciones Ticket. Tu tarea es sintetizar el texto de Wikipedia y extraer exactamente tres hitos o terminologías técnicas modernas del mercado que justifiquen la implementación del servicio solicitado. Devuelve una lista estructurada de los tres puntos."""

def analyze(service: str, wiki_text: str) -> str:
    """Run the Market Analyst agent.

    Args:
        service: The service requested by the client (e.g., "Migración Cloud").
        wiki_text: Full Wikipedia article text returned by the web search tool.
    Returns:
        String with three market insights.
    """
    client = get_client()
    user_input = f"Servicio solicitado: {service}\nInformación de Wikipedia (primeros 3000 caracteres): {wiki_text[:3000]}"
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input}
    ]
    response = client.complete(messages=messages, model=MODEL_NAME, temperature=0)
    return response.choices[0].message.content.strip()

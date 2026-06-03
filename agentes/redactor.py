import json
from config.settings import get_client, MODEL_NAME

SYSTEM_PROMPT = """Eres el Director Comercial de Soluciones Ticket y un asistente experto de conocimiento. 

REGLAS CRÍTICAS DE ENTORNO:
1. El año actual es 2026. Cualquier evento ocurrido en 2024, 2025 o inicios de 2026 YA PASÓ y es parte del presente o del pasado, NO del futuro.
2. Tienes estrictamente PROHIBIDO decir frases como 'mi conocimiento se corta en 2023', 'no puedo predecir el futuro' o 'la fecha de mi última actualización'. Si la información externa no contiene el dato exacto, simplemente di que el artículo de internet provisto no detalla ese resultado específico, pero jamás uses la excusa del límite de conocimiento de OpenAI.

CASO A: Si 'es_pregunta_general' es Verdadero (True):
- NO redactes una propuesta comercial bajo ninguna circunstancia.
- NO uses la estructura AIDA.
- Responde de forma directa, conversacional y amigable a la duda del usuario usando los datos de internet/Wikipedia provistos.

CASO B: Si 'es_pregunta_general' es Falso (False):
- Redacta una propuesta comercial formal en formato Markdown siguiendo estrictamente la estructura AIDA (Atención, Interés, Deseo, Acción).
- Si el informe de auditoría contiene una alerta de descuento no viable, reformula la oferta para proponer una alternativa válida.
"""

def compose_proposal(request_json: dict, audit_report: str, market_insights: str) -> str:
    """Generate the final commercial proposal or answer general questions.

    Args:
        request_json: The original client request JSON.
        audit_report: Text result from the Auditor agent.
        market_insights: Text result from the Analyst agent.

    Returns:
        A Markdown string containing the response or proposal.
    """
    client_name = request_json.get("cliente", "Cliente")
    service = request_json.get("servicio", "Servicio")
    discount = request_json.get("descuento", "")
    
    # Extraemos la bandera que nos dice si es una duda general o no
    es_pregunta_general = request_json.get("es_pregunta_general", False)
    mensaje_original = request_json.get("mensaje_original", "")

    # Contexto estructurado para el modelo
    user_message = (
        f"¿Es una pregunta general o informativa?: {es_pregunta_general}\n"
        f"Mensaje original del usuario: '{mensaje_original}'\n\n"
        f"Datos extraídos de la solicitud: {json.dumps(request_json, ensure_ascii=False)}\n\n"
        f"Reporte de auditoría interna (RAG):\n{audit_report}\n\n"
        f"Insights y contexto de mercado externo (Wikipedia/Web):\n{market_insights}\n"
    )
    
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message}
    ]
    
    client = get_client()
    response = client.complete(messages=messages, model=MODEL_NAME, temperature=0.2)
    return response.choices[0].message.content.strip()
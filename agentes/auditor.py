import os
from typing import Dict
from dotenv import load_dotenv
from config.settings import get_client, MODEL_NAME


def audit(request_json: Dict, policy_text: str) -> str:
    """Audit the client request against internal policy text.

    Parameters:
        request_json (Dict): JSON containing client request details.
        policy_text (str): Full text extracted from the internal policies PDF.

    Returns:
        str: A concise audit report indicating technical viability and any
        discount policy violations.
    """
    load_dotenv()
    client = get_client()
    system_prompt = (
        "Eres el Auditor de Operaciones de Soluciones Ticket."
        " Tu tarea es validar semánticamente si el servicio solicitado está vigente"
        " y si el descuento pedido infringe las políticas internas del PDF."
        " Devuelve un reporte directo indicando viabilidad técnica y alertas de precios."
        " Usa un formato claro con secciones 'Viabilidad' y 'Alertas'."
    )
    user_message = (
        f"Solicitud del cliente: {request_json}\n\n"
        f"Políticas internas (texto completo):\n{policy_text}"
    )
    response = client.complete(messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ], model=MODEL_NAME, temperature=0)
    return response.choices[0].message.content.strip()

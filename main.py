import json
import os
import sys

from config.settings import get_client, MODEL_NAME
from herramientas.lector_pdf import extract_text
from herramientas.buscador_web import search_wikipedia
from agentes.auditor import audit
from agentes.analista import analyze
from agentes.redactor import compose_proposal


def extract_entities_from_chat(user_input, client):
    """Usa el LLM central para parsear la entrada libre del usuario.
    Optimizado para extraer de forma limpia temas de conversación o de cultura general
    aislando las palabras clave exactas para el buscador web.
    """
    prompt = f"""
    Eres un extractor de entidades de alta precisión. El usuario interactúa en un chat libre y puede pedir una propuesta comercial o hacer una pregunta general/técnica/cultural.
    
    Analiza el siguiente mensaje del usuario:
    "{user_input}"
    
    Genera un objeto JSON estrictamente con las siguientes llaves:
    - "cliente": El nombre de la empresa/cliente mencionado. Si no hay ninguno, pon "General".
    - "servicio": El tema central, evento, tecnología o concepto por el que pregunta. 
                 REGLA CRÍTICA: Extrae exclusivamente el nombre del concepto limpio (palabras clave puras) para poder buscarlo en Wikipedia. 
                 Elimina comandos o muletillas como 'busca en wikipedia', 'quien es', 'que contiene', 'dime sobre', etc.
                 Ejemplo: Si dice 'quien es el campeon actual de la champions league 2026', el servicio DEBE ser 'UEFA Champions League'.
                 Ejemplo: Si dice 'que contiene una hamburguesa de mcdonalds', el servicio DEBE ser 'McDonald's'.
                 Si es un saludo o pregunta muy vaga, usa 'Consultoría Tecnológica'.
    - "descuento": El porcentaje de descuento solicitado si se menciona (ej: '25%'). Si no se menciona, pon '0%'.
    - "es_pregunta_general": true si el usuario solo está haciendo una pregunta informativa/duda técnica/tema de cultura general, false si explícitamente está solicitando una propuesta comercial, cotización o venta de negocio para Soluciones Ticket.

    Responde ÚNICAMENTE el JSON crudo, sin bloques de código ```json o texto adicional.
    """
    
    try:
        response = client.complete(
            messages=[
                {"role": "system", "content": "Eres un asistente técnico que solo responde en JSON crudo sin formato Markdown."},
                {"role": "user", "content": prompt}
            ],
            model=MODEL_NAME,
            temperature=0.0
        )
        
        raw_content = response.choices[0].message.content.strip()
        if raw_content.startswith("```"):
            raw_content = raw_content.split("\n", 1)[1].rsplit("\n", 1)[0].strip()
        
        return json.loads(raw_content)
    except Exception as e:
        # Fallback seguro en caso de error de parseo
        return {
            "cliente": "General",
            "servicio": "Consultoría Tecnológica",
            "descuento": "0%",
            "es_pregunta_general": True
        }


def main():
    # Inicializar cliente de IA
    try:
        client = get_client()
    except Exception as e:
        print(f"❌ Error de configuración (revisa tu archivo .env): {e}")
        return

    # ---- Precarga de Base de Conocimiento Interna (RAG) ----
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    pdf_filenames = ["capacidades_tecnicas.pdf", "catalogo_servicios.pdf", "politicas_comerciales.pdf"]
    
    print("⚡ [Sistema] Inicializando Base de Conocimientos desde la carpeta /data...")
    combined_policy_text = ""
    for filename in pdf_filenames:
        pdf_path = os.path.join(data_dir, filename)
        if os.path.exists(pdf_path):
            try:
                text = extract_text(pdf_path)
                combined_policy_text += f"\n=== DOCUMENTO: {filename.upper()} ===\n{text}\n"
            except Exception as e:
                print(f"⚠️ Alerta al leer {filename}: {e}")
        else:
            print(f"❌ Archivo no encontrado en /data: {filename}")
    
    print("✅ Sistema en línea. Historial e información interna cargada con éxito.")
    print("=" * 60)
    print("🤖 BIENVENIDO AL ASISTENTE DE SOLUCIONES TICKET IA")
    print("Puedes pedirme propuestas comerciales o hacerme preguntas sobre cualquier tema.")
    print("Escribe 'salir' o 'exit' para terminar la conversación.")
    print("=" * 60 + "\n")

    # ---- Bucle de Chat Interactivo ----
    while True:
        try:
            user_input = input("👤 Tú: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n👋 ¡Hasta luego!")
            break

        if not user_input:
            continue
        
        if user_input.lower() in ["salir", "exit", "quit"]:
            print("🤖 Asistente: ¡Entendido! Éxito en tu presentación. ¡Adiós! 👋")
            break

        print("\n⏳ Pensando...")

        # 1. Entender la entrada del usuario en lenguaje natural
        request = extract_entities_from_chat(user_input, client)
        
        # 2. Agente Auditor (RAG Interno)
        try:
            audit_report = audit(request, combined_policy_text)
        except Exception as e:
            audit_report = f"Error en auditoría interna: {e}"

        # 3. Herramienta externa (Wikipedia) - Ahora recibe un término limpio
        wiki_text = ""
        term_to_search = request.get("servicio", "").strip()
        
        if term_to_search and term_to_search != "Consultoría Tecnológica":
            print(f"🌐 [Herramienta Web] Buscando en Wikipedia: '{term_to_search}'...")
            try:
                wiki_text = search_wikipedia(term_to_search)
                # Si la API responde un mensaje de no encontrado vacío o genérico de LangChain:
                if not wiki_text or "No good Wikipedia Search Result found" in wiki_text:
                    wiki_text = "No se encontró un artículo específico en internet para este término exacto."
            except Exception as e:
                wiki_text = f"No se pudo consultar la información en internet debido a un problema técnico: {e}"
        else:
            wiki_text = "No se requirió búsqueda externa adicional."

        # 4. Agente Analista (Contexto del Mercado)
        try:
            market_insights = analyze(request["servicio"], wiki_text)
        except Exception as e:
            market_insights = f"No se pudieron generar insights de mercado externos: {e}"

        # 5. Agente Redactor (Generación de la Respuesta Final)
        try:
            request["mensaje_original"] = user_input
            proposal_md = compose_proposal(request, audit_report, market_insights)
        except Exception as e:
            print(f"❌ Error en el proceso de redacción: {e}")
            continue

        # Mostrar respuesta en pantalla
        print("\n🤖 Asistente IA:")
        print("-" * 40)
        print(proposal_md)
        print("-" * 40 + "\n")


if __name__ == "__main__":
    main()
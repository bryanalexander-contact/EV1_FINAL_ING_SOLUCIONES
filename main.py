import json
import os
import sys

from config.settings import get_client, MODEL_NAME
from herramientas.lector_pdf import extract_text
from herramientas.buscador_web import search_wikipedia
from agentes.auditor import audit
from agentes.analista import analyze
from agentes.redactor import compose_proposal


def extract_entities_from_chat(user_input, client, historial_contexto=""):
    """Usa el LLM central para parsear la entrada libre del usuario teniendo en cuenta
    el hilo de los últimos mensajes para resolver pronombres, detectar consultas sobre el historial
    o identificar preguntas abiertas sobre el contenido global de la base de conocimientos (RAG).
    """
    prompt = f"""
    Eres un extractor de entidades de alta precisión. El usuario interactúa en un chat libre y puede pedir una propuesta comercial, hacer una pregunta general/técnica, hacer una pregunta meta-conversacional sobre este chat, o preguntar abiertamente sobre la información que contienen tus documentos o PDFs internos.
    
    CONTEXTO RECIENTE DEL CHAT (Últimos mensajes de la conversación):
    {historial_contexto}
    
    MENSAJE ACTUAL DEL USUARIO:
    "{user_input}"
    
    Tu tarea es generar un objeto JSON analizando el mensaje actual. 
    1. Si el usuario usa pronombres como 'eso', 'aquello' o hace una pregunta de seguimiento, utiliza el CONTEXTO RECIENTE para deducir a qué concepto o tecnología se refiere.
    2. REGLA CRÍTICA DE HISTORIAL: Si el usuario te está preguntando directamente sobre lo que se ha dicho en la conversación (ej: '¿te pregunté sobre X?', '¿de qué hablábamos antes?', '¿qué fue lo primero que dije?'), detecta que es una pregunta sobre el historial del chat.
    3. REGLA CRÍTICA DE BASE DE CONOCIMIENTOS: Si el usuario te pide explícitamente saber qué información hay en tus PDFs, qué documentos tienes cargados, qué servicios vendemos en general o solicita un resumen global de tu conocimiento corporativo interno, detecta que es una pregunta sobre la base de conocimientos.

    Genera un objeto JSON estrictamente con las siguientes llaves:
    - "cliente": El nombre de la empresa/cliente mencionado. Si no hay ninguno, pon "General".
    - "servicio": El tema central, evento, tecnología o concepto por el que pregunta. Extrae exclusivamente el nombre del concepto limpio (palabras clave puras) para poder buscarlo en Wikipedia. Si es una pregunta sobre el historial, un saludo vago o una consulta global sobre los PDFs, usa 'Consultoría Tecnológica'.
    - "descuento": El porcentaje de descuento solicitado si se menciona (ej: '25%'). Si no se menciona, pon '0%'.
    - "es_pregunta_general": true si el usuario solo está haciendo una pregunta informativa/duda técnica, false si solicita una propuesta comercial corporativa.
    - "pregunta_sobre_el_historial": true si el usuario está preguntando explícitamente sobre el pasado del chat o lo que se ha hablado en la conversación. De lo contrario, false.
    - "pregunta_sobre_base_conocimiento": true si el usuario pregunta globalmente qué información contienen tus PDFs, qué bases de datos manejas o qué servicios ofrece la empresa en general. De lo contrario, false.

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
        return {
            "cliente": "General",
            "servicio": "Consultoría Tecnológica",
            "descuento": "0%",
            "es_pregunta_general": True,
            "pregunta_sobre_el_historial": False,
            "pregunta_sobre_base_conocimiento": False
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

    # ---- [GESTIÓN DE MEMORIA CONVERSACIONAL] ----
    historial_memoria = []

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

        # Convertimos el historial acumulado en un bloque de texto
        contexto_texto = "\n".join(historial_memoria) if historial_memoria else "No hay mensajes previos en este chat."

        # 1. Entender la entrada pasando la memoria contextual
        request = extract_entities_from_chat(user_input, client, contexto_texto)
        
        # Interceptamos las banderas lógicas de control de flujo
        sobre_historial = request.get("pregunta_sobre_el_historial", False)
        sobre_base_datos = request.get("pregunta_sobre_base_conocimiento", False)

        # 2. Agente Auditor (RAG Interno)
        if sobre_base_datos:
            audit_report = "Se requiere un desglose general y estructurado de toda la documentación corporativa disponible."
        elif not sobre_historial:
            try:
                audit_report = audit(request, combined_policy_text)
            except Exception as e:
                audit_report = f"Error en auditoría interna: {e}"
        else:
            audit_report = "No requerido. El usuario está preguntando sobre el historial de la conversación actual."

        # 3. Herramienta externa (Wikipedia) - Se omite si se consulta el historial o la base de datos interna
        wiki_text = ""
        term_to_search = request.get("servicio", "").strip()
        
        if not sobre_historial and not sobre_base_datos and term_to_search and term_to_search != "Consultoría Tecnológica":
            print(f"🌐 [Herramienta Web] Buscando en Wikipedia: '{term_to_search}'...")
            try:
                wiki_text = search_wikipedia(term_to_search)
                if not wiki_text or "No good Wikipedia Search Result found" in wiki_text:
                    wiki_text = "No se encontró un artículo específico en internet para este término exacto."
            except Exception as e:
                wiki_text = f"No se pudo consultar la información en internet debido a un problema técnico: {e}"
        else:
            wiki_text = "No se requirió búsqueda externa adicional."

        # 4. Agente Analista (Contexto del Mercado / Redirección de Contexto)
        if sobre_base_datos:
            # Enrutamiento directo: Inyectamos todo el texto extraído de tus PDFs reales para que el Redactor responda con precisión
            market_insights = f"El usuario solicita saber de manera explícita qué información contienen los PDFs de este RAG. A continuación tienes el contenido íntegro y real extraído de la base de conocimiento interna corporativa para estructurar tu respuesta de forma detallada:\n{combined_policy_text}"
        elif not sobre_historial:
            try:
                market_insights = analyze(request["servicio"], wiki_text)
            except Exception as e:
                market_insights = f"No se pudieron generar insights de mercado externos: {e}"
        else:
            market_insights = f"Contexto real del historial de este chat para responder al usuario:\n{contexto_texto}"

        # 5. Agente Redactor (Generación de la Respuesta Final)
        try:
            request["mensaje_original"] = user_input
            
            # Ajustamos instrucciones temporales en el reporte de auditoría para guiar estrictamente al Redactor según el flujo
            if sobre_historial:
                audit_report = f"¡CRÍTICO! El usuario te está preguntando si dijo o no algo en este chat. Usa la sección de insights (que contiene el historial real) para responder con la verdad. No inventes."
            elif sobre_base_datos:
                audit_report = f"¡CRÍTICO! El usuario quiere un resumen preciso del contenido de los documentos del RAG. Analiza el bloque de texto corporativo provisto en los insights y genera un desglose profesional e impecable de la información sin evadir la consulta."

            proposal_md = compose_proposal(request, audit_report, market_insights)
        except Exception as e:
            print(f"❌ Error en el proceso de redacción: {e}")
            continue

        # Mostrar respuesta en pantalla
        print("\n🤖 Asistente IA:")
        print("-" * 40)
        print(proposal_md)
        print("-" * 40 + "\n")

        # ---- [ACTUALIZACIÓN DE LA MEMORIA] ----
        historial_memoria.append(f"Usuario: {user_input}")
        historial_memoria.append(f"IA: {proposal_md[:150]}...") 
        
        if len(historial_memoria) > 4:
            historial_memoria = historial_memoria[-4:]


if __name__ == "__main__":
    main()
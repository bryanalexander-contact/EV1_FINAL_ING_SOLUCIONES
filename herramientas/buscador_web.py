from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper


def search_wikipedia(term: str) -> str:
    """Busca un término en Wikipedia y devuelve un texto limpio como contexto.
    Incluye un mecanismo de robustez para evitar respuestas vacías de LangChain.
    """
    # Intentamos primero la búsqueda nativa (LangChain usará el lenguaje configurado o inglés por defecto si falla)
    try:
        wiki_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=2500)
        wikipedia_tool = WikipediaQueryRun(api_wrapper=wiki_wrapper)
        result = wikipedia_tool.run(term).strip()
        
        # Validar si LangChain arrojó su mensaje estándar de "no encontrado"
        if "No good Wikipedia Search Result found" in result:
            # Estrategia de reintento: Si el término contiene palabras complejas, intentamos simplificarlo
            words = term.split()
            if len(words) > 2:
                simplified_term = " ".join(words[:2]) # Probamos solo con las primeras dos palabras clave
                result = wikipedia_tool.run(simplified_term).strip()
                
        return result
    except Exception as e:
        return f"Error al procesar la API de Wikipedia: {str(e)}"
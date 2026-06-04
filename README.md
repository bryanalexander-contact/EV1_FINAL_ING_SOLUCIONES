
Este proyecto consiste en un sistema multi-agente inteligente diseñado para automatizar y optimizar el proceso comercial de **Soluciones Ticket**. El sistema interactúa con los usuarios en lenguaje natural a través de la terminal, procesando tanto solicitudes de propuestas comerciales formales como consultas técnicas e informativas de mercado de manera híbrida.

El software integra una base de conocimientos privada mediante **RAG (Retrieval-Augmented Generation)** y consultas en tiempo real a fuentes externas (Wikipedia), manteniendo un hilo conversacional fluido gracias a una gestión de memoria a corto plazo.

---

## Arquitectura del Sistema (Multi-Agente)

El proyecto está diseñado bajo una arquitectura modular de agentes especializados:

1. **Agente Extractor (`main.py`):** Clasifica la intención del usuario y extrae entidades en un formato JSON estructurado. Resuelve pronombres apoyándose en el historial.
2. **Agente Auditor (`agentes/auditor.py`):** Realiza búsquedas semánticas (RAG) sobre los documentos internos de la empresa para validar la disponibilidad de servicios y la viabilidad de descuentos.
3. **Agente Analista (`agentes/analista.py`):** Procesa el contexto externo recolectado de la web para añadir valor y madurez técnica a las respuestas.
4. **Agente Redactor (`agentes/redactor.py`):** Orquesta las entradas de todos los agentes. Si es una venta, genera una propuesta formal estructurada en **AIDA** (Atención, Interés, Deseo, Acción); si es una duda, genera una respuesta directa e hilada conversacionalmente.

---

## Estructura del Proyecto

```text
proyecto_final/
├── .venv/                  # Entorno virtual de Python
├── agentes/                # Lógica de los agentes especializados
│   ├── analista.py
│   ├── auditor.py
│   └── redactor.py
├── config/                 # Configuración central del cliente de IA
│   └── settings.py
├── data/                   # Base de conocimiento privada (RAG)
│   ├── capacidades_tecnicas.pdf
│   ├── catalogo_servicios.pdf
│   └── politicas_comerciales.pdf
├── herramientas/           # Módulos de conexión web y lectura de datos
│   ├── buscador_web.py
│   └── lector_pdf.py
├── .env                    # Variables de entorno (Credenciales y API Keys)
├── .gitignore              # Archivos excluidos de Git
├── .python-version         # Especificación de la versión exacta de Python
├── main.py                 # Orquestador principal y bucle de chat
├── pyproject.toml          # Configuración de dependencias (Formato moderno)
├── requirements.txt        # Dependencias congeladas para instalación clásica
└── uv.lock                 # Archivo de bloqueo para entornos unificados con UV


Requisitos e Instalación
Este proyecto está preparado para un despliegue rápido e idéntico en cualquier máquina mediante soporte híbrido (Pip tradicional o UV).

Paso 1: Clonar el repositorio y posicionarse en la carpeta
Bash


git clone https://github.com/bryanalexander-contact/EV1_FINAL_ING_SOLUCIONES.git
cd proyecto_final



Paso 2: Crear y activar el entorno virtual (Recomendado)
En Windows:


python -m venv .venv
.venv\Scripts\activate


En Mac/Linux:

python -m venv .venv
source .venv/bin/activate


Paso 3: Instalar las dependencias
Puedes instalar el entorno idéntico de desarrollo usando cualquiera de las siguientes opciones:

Opción A (Instalación clásica con Pip):


pip install -r requirements.txt
Opción B (Instalación ultra-rápida si usas UV):


SI NO FUNCIONARA PIP:
CORRER:

uv sync


Paso 4: Configurar Variables de Entorno
Crea un archivo llamado .env en la raíz del proyecto y añade tus credenciales correspondientes de OpenAI o Azure Y TOKEN DE GITHUB MODELS classic hecho con permisos de repo, read user y user:email


PASO 5 FINAL PARA EJECUTAR AGENTES:

python main.py








Flujos de Prueba Sugeridos (Demostración de Capacidades)
Prueba de Memoria Flotante e Híbrido RAG/Web:

Pregunta: ¿Qué es Kubernetes? (El sistema responderá usando Wikipedia y aclarará que no está en el catálogo).

Pregunta: ¿Y Migración Cloud? (El sistema detectará el hilo conversacional, buscará en Wikipedia y además inyectará las políticas del RAG interno exigiendo el 50% de pago inicial).

Pregunta: ¿Me confirmas si te pregunté por Kubernetes al inicio? (Activará la bandera de historial, saltará Wikipedia y validará la memoria RAM del chat).

Prueba de Auditoría de Riesgo Comercial (Estructura AIDA):

Pregunta: Hola, cotízame Soporte Preventivo para mi empresa Alfa S.A. y aplícame un 40% de descuento. (El sistema detectará que es una propuesta comercial formal, el Agente Auditor rechazará el 40% basándose en el PDF de políticas y reformulará la oferta aplicando el tope máximo permitido).

Especificaciones Técnicas
Control de Contexto: Implementa una ventana deslizante (Sliding Window Memory) en la RAM limitada estrictamente a las últimas interacciones para optimizar costos y evitar el desbordamiento de tokens.

Modelo Base: Configurado centralmente desde config/settings.py.

Procesamiento PDF: Extracción de texto plano y mapeo de conocimiento estático local sin persistencia pesada.

# Agente IT Consultor & Auditor Inteligente (RAG + Web Search)

Este es un proyecto de Inteligencia Artificial que implementa un sistema multi-agente utilizando **LangChain**, una base de datos vectorial local con **FAISS**, y capacidades de búsqueda externa a través de **DuckDuckGo**. El sistema extrae conocimiento de documentos internos (PDFs en la carpeta `data/`) y los compara con información pública de Internet en tiempo real para generar informes comerciales, técnicos y de preventa de alta calidad.

La aplicación ha sido portada de Jupyter Notebook a una **consola interactiva y guiada por terminal** para facilitar su ejecución directa y su despliegue.

---

## 📋 Requisitos del Sistema

> [!IMPORTANT]
> **Versión Estricta de Python**: Este proyecto requiere única y exclusivamente **Python 3.11.4** para su correcto funcionamiento y compatibilidad de dependencias. El programa validará esta versión al iniciar y detendrá la ejecución si se utiliza otra distinta.

### Cómo instalar Python 3.11.4
Si utilizas gestores de versiones como `pyenv` o `uv`:
- **pyenv**: `pyenv install 3.11.4` y luego `pyenv local 3.11.4`
- **uv**: `uv python install 3.11.4`

O descárgalo directamente desde el [sitio oficial de Python](https://www.python.org/downloads/release/python-3114/).

---

## 🚀 Instalación y Configuración

Sigue estos pasos para clonar el repositorio, instalar las dependencias y ejecutar el proyecto:

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/nombre-del-repositorio.git
cd nombre-del-repositorio
```

### 2. Crear y activar un entorno virtual (Recomendado)
```bash
# Crear entorno virtual con Python 3.11.4
python -m venv .venv

# Activar el entorno virtual:
# En Windows (PowerShell):
.venv\Scripts\Activate.ps1
# En Windows (CMD):
.venv\Scripts\activate.bat
# En macOS/Linux:
source .venv/bin/activate
```

### 3. Instalar las dependencias
Instala todas las librerías necesarias directamente desde el archivo `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Configurar el Token de GitHub Models (`GITHUB_TOKEN`)
Este proyecto utiliza el endpoint de inferencia de modelos de GitHub (`https://models.inference.ai.azure.com`) con el modelo **gpt-4o-mini** y embeddings **text-embedding-3-small**.

1. Genera un token de acceso personal (classic o fine-grained) en la configuración de desarrollador de GitHub. Debe tener acceso a GitHub Models.
2. Puedes crear un archivo `.env` en la raíz del proyecto con la siguiente línea:
   ```env
   GITHUB_TOKEN=tu_github_token_aqui
   ```
3. *Nota*: Si no creas el archivo `.env`, **el programa te solicitará de forma amigable tu token de forma interactiva en la primera ejecución** y lo guardará de forma automática en un archivo `.env` para ti.

---

## 🖥️ Uso de la Aplicación de Terminal

Para iniciar la interfaz interactiva guiada por consola, simplemente ejecuta:

```bash
python main.py
```

### Opciones Disponibles en el Menú:
1. **Generar Informe Comparativo de Servicios (Preventa IT)**: Analiza el catálogo de servicios internos en la nube/ciberseguridad y busca precios actualizados de competidores en la web para estructurar un informe comparativo en `output/informe_final.txt`.
2. **Generar Informe de Auditoría Comercial (Políticas y Garantías)**: Extrae las políticas comerciales, plazos de garantía y esquemas de pago del PDF interno para contrastarlos con políticas del mercado. Lo guarda en `output/informe_politicas_comerciales.txt`.
3. **Generar Informe de Benchmark Técnico (Capacidades e ISO 27001)**: Realiza un estudio comparativo técnico y de cumplimiento de estándares de seguridad física y lógica frente a los grandes hiperescaladores (AWS, Azure, GCP). Lo guarda en `output/informe_capacidades_tecnicas.txt`.
4. **Chat Interactivo con el Agente (Consulta Libre)**: Entra en un modo conversacional abierto donde puedes consultarle al agente lo que desees. El agente decidirá dinámicamente si usar el buscador RAG de tus PDFs o DuckDuckGo Search para responder.
5. **Verificar Archivos de Salida**: Te permite inspeccionar los informes creados actualmente y ver sus contenidos directamente en la terminal sin salir del programa.
6. **Salir**.

---

## 📂 Estructura del Proyecto

- `main.py`: Código principal y punto de entrada que inicializa el sistema, los modelos de Azure AI Inference (GitHub Models), el motor RAG local con FAISS, y ejecuta la interfaz interactiva.
- `data/`: Carpeta que almacena los documentos PDF del catálogo de la empresa.
- `output/`: Carpeta autogenerada donde se guardan los informes producidos por los agentes.
- `requirements.txt`: Archivo de dependencias para la instalación rápida.
- `pyproject.toml` y `uv.lock`: Archivos de configuración de dependencias del entorno de desarrollo.
- `.python-version`: Especificación estricta de la versión `3.11.4` de Python.
# Ev1_RAG

Instrucciones para correr este proyecto,


PASO 1(CMD DE WINDOWS, O TERMINAL POWERSHELL DE VISUAL STUDIO CODE O CUALQUIER IDE)
correr:
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

<img width="793" height="206" alt="image" src="https://github.com/user-attachments/assets/261953eb-0bf3-4342-aa8e-b77e35501fff" />

PASO 2, SI DICE QUE EL PASO UV INIT NO ES NECESARIO, PEGAR DE INMEDIATO EL CODIGO DE [project]...,"python-dotenv>=1.2.2", 
SI ES QUE CREA UN NUEVO PROJECT.TOML, igualmente pegar el codigo de project a continuacion.

uv init 

y luego 

PEGAR ESTO:

[project]
name = "proyecto-final"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "duckduckgo-search>=8.1.1",
    "faiss-cpu>=1.13.2",
    "jupyterlab>=4.5.7",
    "langchain==0.2.16",
    "langchain-community==0.2.16",
    "langchain-openai==0.1.7",
    "langchain-text-splitters==0.2.4",
    "pypdf>=6.10.2",
    "python-dotenv>=1.2.2",
]

y luego correr esto:

uv lock
uv sync 


PASO 3:

correr:
uv add "langchain==0.2.11" "langchain-openai==0.1.17" "langchain-community==0.2.10" "langchain-text-splitters==0.2.2" "duckduckgo-search==5.3.1" faiss-cpu pypdf python-dotenv
duckduckgo-search python-dotenv


PASO 4:

correr: 
uv add jupyterlab
uv run jupyter lab

 SI DA ERROR EL UV RUN JUPYTER LAB, INTENTAR ESTO:
 cerrar la terminal (apretando el simbolo de basurero a la derecha por lo general en miniatura) y luego correr estos comandos:

taskkill /f /im jupyter-lab.exe /t 2>nul
.venv\Scripts\activate
jupyter lab




PASO 5:

YA UNA VEZ EL JUPYTER ESTE CORRIENDO, IR A AGENTE.IPYBN, Y SELECCIONAR KERNEL

<img width="246" height="279" alt="image" src="https://github.com/user-attachments/assets/fc470833-3224-44d4-b1fd-89775468daa4" />

<img width="903" height="115" alt="image" src="https://github.com/user-attachments/assets/cceecda5-0e02-478a-aadd-f821036c63a9" />



EN CASO DE QUE NO APAREZCA ./.VENV/SCRIPTS, COMO RUTA EN EL BOTON DE PYTHON AL ELEGIR EL KERNEL, CORRER ESTOS COMANDOS:

uv add ipykernel

uv run python -m ipykernel install --user --name=mi_proyecto_uv --display-name "Python (UV Proyecto)"



si eso no funciono, probar por ultimo con, corriendo:  uv sync   , en la terminal, cierre su IDE(Visual studio code ej) y abralo, ve a agente.ipybn , y ve una flecha circular que dice restart, ahi se reiniciara todo, pudiendo elegir el kernel de python ./venv/scripts

<img width="1062" height="403" alt="captura_github2" src="https://github.com/user-attachments/assets/a46535a4-924e-4de7-959c-ea8f20970977" />

y luego, 

<img width="921" height="395" alt="caputa_github3" src="https://github.com/user-attachments/assets/974e186a-a66d-43f3-be33-591ec200082b" />


YA CON ESTO DEBERIA BASTAR PARA QUE CORRA EL PROYECTO(VER PASO 6 MAS ADELANTE SI DA ERROR), AHORA SOLO BASTA CON APRETAR RUN EN LAS CASILLAS DE AGENTE.IPYBN DESDE LA PRIMERA HASTA LA ULTIMA EN ORDEN Y DEBERIA SALIR TODO CORRECTAMENTE




PASO 6(EN CASO DE QUE NO FUNCIONARAN LAS CASILLAS CON TODO YA INSTALADO:

esto puede ser por un tema de python version en el sistema de ejecucion que no calze con la version del proyecto(INCLUSO PUEDE LLEGAR A FUNCIONAR SOLO LA 1ra Y 2da casilla), en ese caso ejecutar:

uv python install 3.11.4

uv python pin 3.11.4

uv sync

uv run python --version


quedando de esta manera el kernel a elegir en la esquina superior derecha en agente.ipybn:
<img width="1353" height="325" alt="image" src="https://github.com/user-attachments/assets/98e62b0d-a70d-4827-a71f-5dfa5e9ae950" />




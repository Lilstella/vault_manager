# vault_manager

Herramientas de línea de comandos para tu vault de Obsidian. Requiere **Python 3.11+**.

## Instalación
```bash
python -m venv .venv
.venv\Scripts\activate          # Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
```

## Configuración
1. Copiá `vault_manager.toml.example` a la **raíz de tu vault** como `vault_manager.toml`.
2. Editá carpetas y tipos de nota para que coincidan con tu vault:

```toml
[folders]
inbox = "00 - Inbox"
templates = "90 - Plantillas"
archive = "99 - Archivo"
ignored = []          # extras; .obsidian, plantillas, archivo y este proyecto siempre se ignoran

[types.tarea]         # el nombre se usa en la línea de comandos
template = "Tarea.md"
folder = "01 - Universidad/Tareas"
```
3. Comprobá que todo está bien: `python main.py config`

**¿Cómo encuentra el vault?** (el primero que aplique)
1. `--vault RUTA`
2. variable de entorno `VAULT_MANAGER_VAULT`
3. la carpeta actual o la primera carpeta superior que contenga `.obsidian`

Si no hay `vault_manager.toml`, se usan valores por defecto genéricos (un solo tipo `note`).

## Uso
```bash
python main.py config                       # muestra y valida la configuración
python main.py new tarea "TP Final"         # crea una nota desde la plantilla
python main.py new apunte "Clase 1" --simulate
python main.py --vault D:\Mi\Vault new tarea "TP"
python main.py new --help                   # ayuda de cada comando
```

## Estructura
```
main.py            punto de entrada (elige el comando)
config.py          carga y valida la configuración
helper.py          funciones compartidas (leer/escribir notas, frontmatter...)
commands/          un módulo por comando, cada uno con su main(argv)
tests/             pytest (nunca tocan tu vault real)
```
Para renombrar o terminar un comando, actualizá el diccionario `COMMANDS` en `main.py`.

## Tests
```bash
pytest                              # todo
pytest tests/test_config.py -v      # un archivo
```
Los tests de los comandos todavía no implementados fallan con `NotImplementedError`: es lo esperado.

## Reglas
- Todo comando que modifique archivos tiene `--simulate` (o requiere `--apply`).
- Nada de rutas escritas a mano: usá `get_config()` y `pathlib`.
- Una función hace una cosa y se puede testear sola.

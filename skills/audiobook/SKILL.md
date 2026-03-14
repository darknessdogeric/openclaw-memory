---
name: audiobook
description: "Skill de conversion de texto/PDF a audiolibro M4B. Convierte archivos PDF o de texto plano en audiolibros con capitulos, usando sintesis de voz piper. Usa este skill cuando el usuario envie un archivo PDF o TXT y quiera convertirlo a audio, escucharlo como audiolibro, o pida leer un documento en voz alta. Tambien cuando diga cosas como 'leeme esto', 'pasalo a audio', 'hazme un audiolibro', o simplemente envie un PDF y pregunte que puede hacer con el."
allowed-tools: Bash Read
metadata: {"openclaw":{"requires":{"bins":["python3","ffmpeg"]},"emoji":"🎧"}}
---

# Audiobook — Skill de conversion a audiolibro

## Descripcion

Este skill convierte archivos PDF o de texto plano (.txt) en audiolibros
M4B con capitulos marcados. Usa piper TTS para la sintesis de voz (rapido
y ligero, funciona offline).

## Configuracion

No requiere variables de entorno especiales. Los modelos de voz estan en
el directorio `models/` dentro del skill.

## Comandos disponibles

| Comando | Descripcion |
|---------|-------------|
| `venv/bin/python audiobook.py convert <archivo> [opciones]` | Convierte un PDF o TXT a audiolibro M4B. Imprime JSON con ruta, duracion y capitulos. |
| `venv/bin/python audiobook.py list-voices` | Lista los modelos de voz disponibles. |

### Opciones de convert

| Opcion | Descripcion |
|--------|-------------|
| `--language es\|en` | Idioma del texto (default: es) |
| `--voice MODELO.onnx` | Modelo de voz especifico (default: auto segun idioma) |
| `--title TITULO` | Titulo del audiolibro (default: nombre del archivo) |
| `--author AUTOR` | Autor (default: Desconocido) |
| `--cover IMAGEN` | Imagen de portada (jpg/png) |
| `--chapters-json ARCHIVO` | JSON con definicion manual de capitulos |
| `--pages-per-chapter N` | Paginas por capitulo si no se detectan automaticamente (default: 10) |
| `--output-dir DIR` | Directorio de salida (default: directorio actual) |
| `--dry-run` | Solo muestra capitulos detectados, no genera audio |
| `--verbose` | Salida detallada |
| `--keep-temp` | Mantiene archivos temporales para depuracion |

## FLUJO OBLIGATORIO — SEGUIR SIEMPRE ESTOS PASOS

### Paso 1: Verificar que el archivo existe

El usuario enviara un archivo por Telegram. OpenClaw lo guarda en el workspace.
Verifica que existe:
```bash
ls -la /ruta/al/archivo.pdf
```

### Paso 2: Ejecutar la conversion

**IMPORTANTE**: El output-dir DEBE ser `/tmp` para que el archivo
resultante se pueda enviar por Telegram. NO uses el workspace como
output-dir (los paths bajo `workspace-*` estan bloqueados para envio).

```bash
cd /home/ubuntu/.openclaw/workspace-jorge/skills/audiobook && \
venv/bin/python audiobook.py convert /ruta/al/archivo.pdf --language es \
  --output-dir /tmp
```

Para texto en ingles:
```bash
cd /home/ubuntu/.openclaw/workspace-jorge/skills/audiobook && \
venv/bin/python audiobook.py convert /ruta/al/archivo.txt --language en \
  --output-dir /tmp
```

**IMPORTANTE**: La conversion puede tardar varios minutos para libros largos.
Informa al usuario de que estas procesando y que tardara un poco.

**IMPORTANTE sobre envio de archivos**: OpenClaw permite enviar archivos
desde `/tmp`, `~/.openclaw/media/` y `~/.openclaw/sandboxes/`.
Los paths bajo `~/.openclaw/workspace-*` estan BLOQUEADOS para envio.
Usa siempre `--output-dir /tmp` y envia el archivo desde ahi.

### Paso 3: Interpretar el resultado

El comando imprime JSON al terminar:
```json
{"output_path": "/ruta/al/Titulo.m4a", "duration": "45m30s", "chapters": 12, "size_mb": 34.2}
```

### Paso 4: Enviar el archivo al usuario

Usa la herramienta `message` con `action: "sendAttachment"` para enviar
el M4B como documento descargable. Usa `contentType: "application/octet-stream"`
para que Telegram lo envie como archivo descargable (si usas `action: "send"`
con `media`, Telegram lo reproduce inline y el usuario no puede guardarlo
facilmente en su app de audiolibros).

```json
{
  "action": "sendAttachment",
  "media": "/tmp/Titulo.m4a",
  "filename": "Titulo.m4a",
  "contentType": "application/octet-stream",
  "message": "Aqui tienes tu audiolibro. Son 12 capitulos, duracion total 45 minutos."
}
```

**IMPORTANTE**: Usa el valor de `output_path` del JSON del paso 3 como
valor de `media`. NO intentes codificar en base64 ni buscar alternativas.
El path `/tmp/...` funciona directamente con la herramienta `message`.

## Ejemplo completo

```
Usuario: Convierte este PDF a audiolibro [adjunta archivo.pdf]

Bot: Voy a convertir tu PDF a audiolibro. Esto puede tardar unos minutos
     dependiendo del tamano del documento...

Bot: [Ejecuta: venv/bin/python audiobook.py convert /ruta/archivo.pdf --language es --output-dir /tmp]
     Resultado: {"output_path": "/tmp/archivo.m4a", "duration": "1h23m", "chapters": 8, "size_mb": 58.3}

Bot: [Usa herramienta message con action="sendAttachment", media="/tmp/archivo.m4a",
     filename="archivo.m4a", contentType="application/octet-stream",
     message="Tu audiolibro esta listo. 8 capitulos, 1 hora y 23 minutos de duracion."]
```

## Idiomas soportados

| Idioma | Modelo | Descripcion |
|--------|--------|-------------|
| `es` | es_ES-sharvard-medium | Voz masculina espanola, calidad media |
| `en` | en_GB-cori-high | Voz femenina britanica, calidad alta |

## ERRORES COMUNES — NO HACER

- **NO** ejecutar sin verificar que el archivo existe primero
- **NO** olvidar el flag `--language` si el texto es en ingles
- **NO** preocuparse si la conversion tarda: es normal para libros largos
- **NO** intentar convertir archivos que no sean PDF o TXT

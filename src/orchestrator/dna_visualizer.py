
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
dna_visualizer.py

Lee memory/memory.json y genera adn_proyecto.md.

Alcance autorizado:
- Leer la memoria existente.
- Analizar sus entradas.
- Generar únicamente adn_proyecto.md.
- No modificar memory/memory.json ni otros archivos del proyecto.

El análisis de resultados es conservador:
- No considera que cualquier resumen implique éxito.
- Reconoce indicadores explícitos de ejecución y auditoría.
- Mantiene separados el éxito de una prueba y la aprobación de una tarea.
"""

import json
from pathlib import Path
from datetime import datetime


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MEMORY_FILE = PROJECT_ROOT / "memory" / "memory.json"
OUTPUT_FILE = PROJECT_ROOT / "adn_proyecto.md"


AGENTES_CONOCIDOS = {
    "Director",
    "Arquitecto",
    "Developer",
    "Quantum_RD",
    "Tester",
    "Auditor",
    "Business",
}


def cargar_memoria():
    """Carga la memoria y devuelve sus entradas."""
    if not MEMORY_FILE.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo de memoria: {MEMORY_FILE}"
        )

    with MEMORY_FILE.open("r", encoding="utf-8") as archivo:
        memoria = json.load(archivo)

    if not isinstance(memoria, dict):
        raise ValueError(
            "El archivo de memoria debe contener un objeto JSON."
        )

    entradas = memoria.get("entradas", [])

    if not isinstance(entradas, list):
        raise ValueError(
            "La propiedad 'entradas' de la memoria debe ser una lista."
        )

    return memoria, entradas


def normalizar_texto(valor):
    """Convierte un valor a texto legible sin perder datos estructurados."""
    if valor is None:
        return ""

    if isinstance(valor, str):
        return valor

    return json.dumps(
        valor,
        ensure_ascii=False,
        sort_keys=True,
        default=str,
    )


def obtener_contenido(entrada):
    """Obtiene el contenido principal de una entrada."""
    return normalizar_texto(entrada.get("contenido", ""))


def obtener_resumen(entrada):
    """Obtiene resultado_resumen, que puede ser texto o un objeto."""
    return normalizar_texto(entrada.get("resultado_resumen", ""))


def texto_de_analisis(entrada):
    """
    Combina los campos relevantes para detectar evidencias.

    No modifica la entrada original ni interpreta el resumen como JSON:
    algunos registros históricos guardan diccionarios como texto Python.
    """
    campos = (
        "categoria",
        "contenido",
        "resultado_resumen",
        "estado",
        "status",
        "resultado",
        "veredicto",
        "aprobado",
    )

    partes = []

    for campo in campos:
        if campo in entrada:
            partes.append(normalizar_texto(entrada.get(campo)))

    return " ".join(partes)


def contiene_indicador(texto, indicadores):
    """Busca indicadores textuales ignorando mayúsculas y minúsculas."""
    texto_normalizado = texto.casefold()
    return any(
        indicador.casefold() in texto_normalizado
        for indicador in indicadores
    )


def detectar_error(entrada):
    """
    Detecta errores o fallos explícitos.

    La búsqueda se limita a expresiones indicativas de fallo; la mera
    existencia de un resumen no se considera un error.
    """
    texto = texto_de_analisis(entrada)

    indicadores = (
        "bloqueado",
        "fallida",
        "fallido",
        "error crítico",
        "error critico",
        "excepción no controlada",
        "excepcion no controlada",
        "veredicto: rechazado",
        "veredicto': 'rechazado",
        "aprobado: false",
        "aprobado': false",
    )

    return contiene_indicador(texto, indicadores)


def detectar_agente(entrada):
    """Identifica si la entrada pertenece a un agente conocido."""
    agente = normalizar_texto(entrada.get("agente", "")).strip()

    if agente:
        return any(
            agente.casefold() == conocido.casefold()
            for conocido in AGENTES_CONOCIDOS
        )

    texto = texto_de_analisis(entrada)

    return any(
        nombre.casefold() in texto.casefold()
        for nombre in AGENTES_CONOCIDOS
    )


def detectar_aprobacion_humana(entrada):
    """
    Detecta referencias explícitas a aprobación humana.

    Una auditoría aprobada por un agente no equivale por sí sola
    a una autorización humana.
    """
    texto = texto_de_analisis(entrada)

    indicadores = (
        "aprobación humana",
        "aprobacion humana",
        "aprobado por el usuario",
        "aprobada por el usuario",
        "autorización humana",
        "autorizacion humana",
        "autoriza el usuario",
        "autorizado por gustavo",
        "aprobado por gustavo",
    )

    return contiene_indicador(texto, indicadores)


def detectar_ejecucion_exitosa(entrada):
    """
    Reconoce señales explícitas de ejecución exitosa.

    returncode: 0 indica que el proceso terminó sin error de retorno.
    No implica, por sí solo, que todos los objetivos de la tarea
    estén completos.

    failed: 0 indica que el resultado informado no registra pruebas
    fallidas. Se trata como evidencia favorable, no como aprobación
    universal del proyecto.
    """
    texto = texto_de_analisis(entrada).casefold()

    indicadores_returncode = (
        "'returncode': 0",
        '"returncode": 0',
        "returncode: 0",
    )

    indicadores_failed_cero = (
        "'failed': 0",
        '"failed": 0',
        "failed: 0",
    )

    indicadores_resultado_positivo = (
        "veredicto': 'aprobado'",
        'veredicto": "aprobado"',
        "veredicto: aprobado",
        "aprobado': true",
        '"aprobado": true',
        "aprobado: true",
    )

    indicadores_explicitos = (
        "tarea completada",
        "ejecución completada",
        "ejecucion completada",
        "ejecuto tarea",
        "ejecutó tarea",
        "resultado exitoso",
        "ejecución exitosa",
        "ejecucion exitosa",
    )

    if contiene_indicador(texto, indicadores_returncode):
        return True

    if contiene_indicador(texto, indicadores_failed_cero):
        return True

    if contiene_indicador(texto, indicadores_resultado_positivo):
        return True

    if contiene_indicador(texto, indicadores_explicitos):
        return True

    return False


def detectar_completado(entrada):
    """
    Devuelve True cuando existe evidencia explícita de finalización.

    No considera suficiente la presencia de un agente, un resumen
    no vacío o un objetivo mencionado sin resultado.
    """
    if detectar_error(entrada):
        return False

    categoria = normalizar_texto(
        entrada.get("categoria", "")
    ).casefold()

    estado = normalizar_texto(
        entrada.get("estado", "")
    ).casefold()

    status = normalizar_texto(
        entrada.get("status", "")
    ).casefold()

    resultado = normalizar_texto(
        entrada.get("resultado", "")
    ).casefold()

    estados_completados = (
        "completado",
        "completada",
        "finalizado",
        "finalizada",
        "exitoso",
        "exitosa",
        "aprobado",
        "aprobada",
    )

    for valor in (estado, status, resultado):
        if any(
            indicador in valor
            for indicador in estados_completados
        ):
            return True

    # Un resultado de agente debe tener evidencia positiva.
    if categoria == "resultado_agente":
        return detectar_ejecucion_exitosa(entrada)

    # Una auditoría requiere una señal explícita de aprobación.
    if "auditor" in normalizar_texto(
        entrada.get("agente", "")
    ).casefold():
        texto = texto_de_analisis(entrada)

        return contiene_indicador(
            texto,
            (
                "veredicto': 'aprobado'",
                'veredicto": "aprobado"',
                "veredicto: aprobado",
                "aprobado': true",
                '"aprobado": true',
                "aprobado: true",
            ),
        )

    # Para otras categorías se aceptan indicadores explícitos,
    # pero no la simple existencia de resultado_resumen.
    return detectar_ejecucion_exitosa(entrada)


def codificar_adn(entrada):
    """
    Genera un código binario de cuatro bits:

    bit 1 (8): error o bloqueo detectado.
    bit 2 (4): agente conocido.
    bit 3 (2): aprobación humana explícita.
    bit 4 (1): finalización con evidencia suficiente.
    """
    bit_error = 8 if detectar_error(entrada) else 0
    bit_agente = 4 if detectar_agente(entrada) else 0
    bit_aprobacion = (
        2 if detectar_aprobacion_humana(entrada) else 0
    )
    bit_completado = 1 if detectar_completado(entrada) else 0

    valor = (
        bit_error
        + bit_agente
        + bit_aprobacion
        + bit_completado
    )

    return format(valor, "04b")


def obtener_timestamp(entrada):
    """Obtiene una marca temporal legible, si está disponible."""
    valor = entrada.get("timestamp", "")

    if valor is None:
        return ""

    return normalizar_texto(valor).replace("|", "\\|").replace("\n", " ")


def escapar_markdown(valor):
    """Evita que el contenido rompa las tablas Markdown."""
    texto = normalizar_texto(valor)
    return (
        texto
        .replace("|", "\\|")
        .replace("\r", " ")
        .replace("\n", " ")
    )


def generar_tabla_entradas(entradas):
    """Genera la tabla principal de memoria."""
    lineas = [
        "| # | Timestamp | Categoría | Agente | ADN | Contenido |",
        "|---:|---|---|---|:---:|---|",
    ]

    for indice, entrada in enumerate(entradas, start=1):
        if not isinstance(entrada, dict):
            entrada = {"contenido": entrada}

        timestamp = escapar_markdown(
            obtener_timestamp(entrada)
        )
        categoria = escapar_markdown(
            entrada.get("categoria", "")
        )
        agente = escapar_markdown(
            entrada.get("agente", "")
        )
        adn = codificar_adn(entrada)
        contenido = escapar_markdown(
            obtener_contenido(entrada)
        )

        lineas.append(
            f"| {indice} | {timestamp} | {categoria} | "
            f"{agente} | `{adn}` | {contenido} |"
        )

    if not entradas:
        lineas.append(
            "| — | — | Sin entradas | — | `0000` | — |"
        )

    return "\n".join(lineas)


def generar_tabla_resultados(entradas):
    """Genera una tabla adicional con los resultados de los agentes."""
    lineas = [
        "| # | Agente | Resultado resumido | Ejecución / finalización |",
        "|---:|---|---|---|",
    ]

    cantidad = 0

    for indice, entrada in enumerate(entradas, start=1):
        if not isinstance(entrada, dict):
            continue

        categoria = normalizar_texto(
            entrada.get("categoria", "")
        ).casefold()

        if categoria != "resultado_agente":
            continue

        cantidad += 1
        agente = escapar_markdown(
            entrada.get("agente", "")
        )
        resumen = escapar_markdown(
            obtener_resumen(entrada)
        )

        completado = (
            "Sí"
            if detectar_completado(entrada)
            else "Sin evidencia suficiente"
        )

        lineas.append(
            f"| {indice} | {agente} | {resumen} | {completado} |"
        )

    if cantidad == 0:
        lineas.append("| — | — | No hay resultados de agentes | — |")

    return "\n".join(lineas)


def generar_conexiones(entradas):
    """
    Resume las relaciones entre categorías y agentes.

    Solo muestra relaciones respaldadas por campos presentes
    en las entradas.
    """
    relaciones = []

    for indice, entrada in enumerate(entradas, start=1):
        if not isinstance(entrada, dict):
            continue

        categoria = normalizar_texto(
            entrada.get("categoria", "")
        ).strip()
        agente = normalizar_texto(
            entrada.get("agente", "")
        ).strip()
        tarea_id = normalizar_texto(
            entrada.get("tarea_id", "")
        ).strip()

        if agente and tarea_id:
            relaciones.append(
                f"- Entrada {indice}: agente **{agente}** "
                f"vinculado a tarea `{tarea_id}` "
                f"(categoría: `{categoria or 'sin categoría'}`)."
            )
        elif agente:
            relaciones.append(
                f"- Entrada {indice}: agente **{agente}** "
                f"(categoría: `{categoria or 'sin categoría'}`)."
            )
        elif tarea_id:
            relaciones.append(
                f"- Entrada {indice}: tarea `{tarea_id}` "
                f"(categoría: `{categoria or 'sin categoría'}`)."
            )

    if not relaciones:
        return "No se detectaron relaciones explícitas entre agentes y tareas."

    return "\n".join(relaciones)


def contar_completados(entradas):
    """Cuenta entradas con evidencia de finalización."""
    total = 0

    for entrada in entradas:
        if isinstance(entrada, dict) and detectar_completado(entrada):
            total += 1

    return total


def generar_markdown(memoria, entradas):
    """Genera el documento Markdown final."""
    fecha_generacion = datetime.now().astimezone().isoformat(
        timespec="seconds"
    )

    total_entradas = len(entradas)
    total_completados = contar_completados(entradas)
    total_agentes = sum(
        1
        for entrada in entradas
        if isinstance(entrada, dict) and detectar_agente(entrada)
    )
    total_errores = sum(
        1
        for entrada in entradas
        if isinstance(entrada, dict) and detectar_error(entrada)
    )

    lineas = [
        "# 🧬 ADN del Proyecto AI-BUSINESS-OS",
        "",
        "> Documento generado automáticamente a partir de "
        "`memory/memory.json`.",
        "",
        "## 1. Resumen",
        "",
        f"- **Entradas procesadas:** {total_entradas}",
        f"- **Entradas con evidencia de finalización:** {total_completados}",
        f"- **Entradas asociadas a agentes conocidos:** {total_agentes}",
        f"- **Entradas con indicadores de error o bloqueo:** {total_errores}",
        f"- **Fecha de generación:** {fecha_generacion}",
        "",
        "La finalización se estima mediante indicadores explícitos. "
        "Una ejecución exitosa o una auditoría aprobada no demuestra, "
        "por sí sola, que todas las metas generales del proyecto estén "
        "completas.",
        "",
        "## 2. Memoria y ADN binario",
        "",
        "Convención de bits: `8` = error/bloqueo; `4` = agente conocido; "
        "`2` = aprobación humana explícita; `1` = finalización con "
        "evidencia suficiente.",
        "",
        generar_tabla_entradas(entradas),
        "",
        "## 3. Resultados de agentes",
        "",
        generar_tabla_resultados(entradas),
        "",
        "## 4. Conexiones detectadas",
        "",
        generar_conexiones(entradas),
        "",
        "## 5. Metadatos",
        "",
        f"- **Archivo de origen:** `{MEMORY_FILE.relative_to(PROJECT_ROOT)}`",
        f"- **Archivo generado:** `{OUTPUT_FILE.name}`",
        "- **Formato de lectura y escritura:** UTF-8",
        "- **Modificación de la memoria:** No",
        "- **Otros archivos del proyecto modificados por este script:** No",
        "",
    ]

    return "\n".join(lineas)


def main():
    """Carga la memoria y genera únicamente el Markdown de salida."""
    memoria, entradas = cargar_memoria()
    documento = generar_markdown(memoria, entradas)

    # Único archivo de salida autorizado por este script.
    OUTPUT_FILE.write_text(
        documento,
        encoding="utf-8",
    )

    print("ADN del proyecto generado correctamente.")
    print(f"Archivo: {OUTPUT_FILE}")
    print(f"Entradas procesadas: {len(entradas)}")
    print(f"Entradas con evidencia de finalización: {contar_completados(entradas)}")


if __name__ == "__main__":
    main()

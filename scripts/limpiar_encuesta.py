"""Limpieza y anonimización de respuestas REALES (tarea de Emily, lab 2).

Uso (desde la raíz del repo):
    python guiones/limpiar_encuesta.py RUTA_AL_CSV_CRUDO

El CSV crudo (export de Google Forms) debe estar FUERA del repositorio.
Salida: plantillas/encuesta_respuestas.csv (anonimizado, origen = real).
"""
import sys
import re
import pandas as pd

RAW = sys.argv[1] if len(sys.argv) > 1 else "estadistica_actualizado-v2.csv"
OUT = "plantillas/encuesta_respuestas.csv"

# Encabezados idénticos al cuestionario aprobado (sección 4 del PDF)
COLS = [
    "¿En qué rango de edad se encuentra?",
    "¿Con qué frecuencia compra en RetailAndina?",
    "En general, ¿Qué tan satisfecho se siente con RetailAndina?",
    "¿Qué tan satisfecho está con los precios que ofrece RetailAndina?",
    "¿Qué tan satisfecho está con la atención que recibe por parte del personal de RetailAndina?",
    "¿Recomendaría RetailAndina a un conocido?",
    "Si RetailAndina lanzara un programa de fidelización, ¿qué tan probable es que se inscriba?",
    "¿Qué otro beneficio esperaría de un programa de fidelización de RetailAndina?",
    "¿Cuánto gasta al mes en compras de consumo masivo, en dólares?",
]
ESCALAS = COLS[2:5] + [COLS[6]]  # preguntas 3, 4, 5 y 7 -> enteros 1..5

df = pd.read_csv(RAW, dtype=str, keep_default_na=False)

# 1) Encabezados: quitar saltos de línea y guiones de corte ("cum-\nplidos")
df.columns = [" ".join(c.replace("-\n", "").split()) for c in df.columns]
df = df.rename(columns={"Marca temporal": "marca"})
# El formulario aplicado conserva el encabezado antiguo de la P1; se renombra al corregido
df = df.rename(columns={"¿Cuál es su edad en años cumplidos?": COLS[0]})
assert list(df.columns[1:]) == COLS, "Los encabezados no coinciden con el cuestionario"
print(f"Filas crudas: {len(df)}")

# 2) Fecha (solo el día; se descarta la hora) y limpieza de espacios
df["fecha"] = pd.to_datetime(df["marca"].str.extract(r"(\d{4}/\d{2}/\d{2})")[0],
                             format="%Y/%m/%d").dt.strftime("%Y-%m-%d")
for c in COLS:
    df[c] = df[c].str.strip()

# 3) Marcar filas sospechosas ANTES de filtrar (marca temporal repetida)
dup = df[df.duplicated("marca", keep=False)]
if len(dup):
    print("\n[REVISAR] Marca temporal repetida; filas del crudo (nº de fila lógica):", [i + 2 for i in dup.index])

# 4) Mapeos a las opciones del cuestionario
df[COLS[1]] = df[COLS[1]].replace({"Al menos una vez al mes": "Mensual"})
for c in ESCALAS:                       # "4: Satisfecho" / "5: Muy satisfe" -> 4 / 5
    df[c] = df[c].str.extract(r"^(\d)")[0].astype(int)
assert all(df[c].between(1, 5).all() for c in ESCALAS)

# P9: opciones del formulario -> opciones del cuestionario corregido
df[COLS[8]] = df[COLS[8]].replace({"$1 - $10": "Menos de $10",
                                   "$10 - $50": "$10 a $49",
                                   "$50 - $100": "$50 a $100"})
assert df[COLS[8]].isin(["Menos de $10", "$10 a $49", "$50 a $100", "Más de $100"]).all()

# 5) Fila de origen (nº de fila en el crudo, solo para los avisos de este script)
df["fila_cruda"] = range(2, len(df) + 2)  # +1 por encabezado, +1 porque Excel empieza en 1

# 6) Criterios de exclusión (sección 3 de la plantilla): no forman parte de la población
#    ni del CSV, pero se CUENTAN para declararlos en el informe.
m_edad = df[COLS[0]] == "30 años o más"
m_freq = df[COLS[1]].isin(["Menos de una vez al mes", "Nunca/No compro en RetailAndina"])
print(f"Excluidas por edad (30+): {int(m_edad.sum())}  filas del crudo: {list(df[m_edad]['fila_cruda'])}")
print(f"Excluidas por frecuencia (P2): {int((m_freq & ~m_edad).sum())}  filas del crudo: {list(df[m_freq & ~m_edad]['fila_cruda'])}")
print(f"Total excluidas: {int((m_edad | m_freq).sum())}")
df = df[~(m_edad | m_freq)].copy().reset_index(drop=True)
# Anonimizar: código R001... consecutivo (sin huecos que delaten filas excluidas)
df.insert(0, "código", [f"R{i+1:03d}" for i in range(len(df))])

df["origen"] = "real"
df = df[["código", "fecha"] + COLS + ["origen"]]
df.to_csv(OUT, index=False, encoding="utf-8")

print(f"\nFilas finales: {len(df)}  ->  {OUT}")
print(df[COLS[0]].value_counts().to_string())
print("\nNulos:\n", df.isna().sum().to_string())

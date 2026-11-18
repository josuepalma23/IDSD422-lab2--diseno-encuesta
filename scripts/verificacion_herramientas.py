## UTILIZAR AL TENER LOS DATOS

import pandas as pd

df = pd.read_csv("datos/encuesta_respuestas.csv")

print("Tipos por columna:")
print(df.dtypes)

print("\nDatos faltantes por columna:")
print(df.isna().sum())

# Solo respuestas reales para la interpretación de sesgos
reales = df[df["origen"] == "real"]

for col in [
    "En general, ¿Qué tan satisfecho se siente con RetailAndina?",
    "¿Recomendaría RetailAndina a un conocido?",
]:
    print(f"\nDistribución de {col} (solo reales):")
    print(reales[col].value_counts(dropna=False).sort_index())

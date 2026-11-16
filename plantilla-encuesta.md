# Plantilla de diseño — Encuesta de satisfacción (hito 1)

**Equipo:** 4 · **Integrantes:** Jordan Sangucho, Josue Palma, Aidan Carrasco, Joel Champutiz, Emily Dias· 
**Fecha:** 30/10/2026
**Repositorio (fork):** https://github.com/josuepalma23/IDSD422-lab2--diseno-encuesta
**Enfoque del equipo (aprobado en clase):** Satisfacción y expectativas

Completa cada sección. Usa commits por sección; la historia del repositorio se revisa.

> **Formato del entregable:** exporta esta plantilla completada a PDF, con el enlace de tu fork en la carátula, y guarda el PDF en `informes/` del fork. Entrega el PDF y el enlace del fork en el aula virtual.

## 1. Objetivo de la encuesta

Estimar el porcentaje de personas satisfechas en el intervalo de 18 a 29 años en una escala del 1 al 5 con respecto a RetailAndina e identificar los beneficios que el encuestado espera sobre el programa de fidelización, con el objetivo de ser enviados a la gerencia para la posterior toma de decisiones.

## 2. Población objetivo

- **Población:** Personas de 18 a 29 años, residentes de la ciudad de Quito que compran en tiendas de consumo masivo de manera frecuente.
- **Límites y justificación:** 
  - Edad 18-29: Es el enfoque seleccionado, además de ser 18 años la edad mínima requerida para dar consentimiento informado y decidir compras por cuenta propia.
  - Residentes en la ciudad de Quito, para facilitar la recolección de información en la etapa de la encuesta.
  - Personas que compran de manera frecuente y al menos una vez al mes en tiendas de consumo masivo, garantiza que el encuestado tenga experiencia suficiente para opinar sobre el tema.
  - Las personas menores de 18 años y mayores de 29 años quedarán fuera de la encuesta, así como personas que no compran en tiendas de consumo masivo.

## 3. Método de muestreo

- **Método:** Muestreo no probabilístico por cuotas según rango de edad (`18 a 23 años`, `24 a 29 años`, `30 años o mas`), con una cuota equitativa por cada estrato.
- **Tamaño y Justificación:** En el diseño inicial se plantean 20 respuestas (10 por estrato, 3 a 6 por integrante). En la recolección real (`estadistica_actualizado-v2.csv`) se obtuvieron 23 respuestas totales, de las cuales **17 cumplen los criterios de población objetivo** (11 de `18 a 23 años` y 6 de `24 a 29 años`; se excluyen 4 de `30 años o más` y 2 fuera de frecuencia mínima). Para equilibrar ambos estratos con datos reales disponibles, se define una cuota de **5 respuestas por estrato (10 en la corrida de prueba)** con semilla fija (`random_state=42`). Para alcanzar el volumen recomendado de 60–100 filas totales, las filas adicionales se generan por simulación con código, se marcan con `origen = simulada` y se declaran en este informe.
- **Selección de los participantes y no respuesta:**
  - Cada integrante buscó entre sus contactos a personas que cumplieran con los criterios de la población objetivo (18–29 años, residentes en Quito, compras frecuentes en consumo masivo) y las clasificó según su estrato de edad.
  - Se solicitó a cada encuestado un referido que cumpliera los mismos criterios para ampliar el alcance más allá del círculo cercano del equipo.
  - La encuesta se aplicó de forma virtual (formularios Google/Microsoft) durante la semana del feriado del 2 y 3 de noviembre.
  - **Registro de no respuesta:** Se contabiliza el número de personas contactadas y referidas que no contestaron únicamente sobre la fracción de datos reales (`origen = real`).
  - **Importante:** Al partir de contactos de los integrantes del grupo, este diseño conserva un componente de muestreo por conveniencia; sus implicaciones y limitaciones se desarrollan en la Sección 5 y se analizan filtrando `origen == "real"`.


- Implementación en código:

```python
import pandas as pd

df = pd.read_csv("estadistica_actualizado-v2.csv")
df.columns = [c.replace("-\n", "").replace("\n", " ").strip() for c in df.columns]

age_col = "¿Cuál es su edad en años cumplidos?"
freq_col = "¿Con qué frecuencia compra en RetailAndina?"

pob_edad = ["18 a 23 años", "24 a 29 años"]
pob_freq = ["Semanal", "Quincenal", "Mensual", "Al menos una vez al mes"]
df_pob = df[df[age_col].isin(pob_edad) & df[freq_col].isin(pob_freq)].copy()

# Una única corrida con semilla fija (random_state=42), cuota de 5 por estrato
muestra_cuotas = (
    df_pob.groupby(age_col, group_keys=False)
    .apply(lambda g: g.sample(n=5, random_state=42))
)
print(muestra_cuotas[[age_col, freq_col]])

**Salida de la implementación en Python**

   ¿Cuál es su edad en años cumplidos?  \
7                         18 a 23 años   
1                         18 a 23 años   
21                        18 a 23 años   
22                        18 a 23 años   
3                         18 a 23 años   
6                         24 a 29 años   
8                         24 a 29 años   
15                        24 a 29 años   
9                         24 a 29 años   
14                        24 a 29 años   

   ¿Con qué frecuencia compra en RetailAndina?  
7                                      Mensual  
1                                      Mensual  
21                     Al menos una vez al mes  
22                                     Mensual  
3                                      Semanal  
6                      Al menos una vez al mes  
8                      Al menos una vez al mes  
15                     Al menos una vez al mes  
9                                      Mensual  
14                     Al menos una vez al mes  

Este método resulta idóneo por encima de la conveniencia pura, ya que se realiza un sorteo dentro de cada estrato que reduce la influencia de qué encuestado está mas cerca de quien lo encuestó, además, por estrato se aportan la misma cantidad de respuestas, si se realizara por conveniencia las respuestas se pueden quedar acumuladas en un solo grupo.


## 4. Cuestionario (5–10 preguntas)

| # | Pregunta | Tipo de variable | Dtype al cargar | Opciones / escala |
|---|---|---|---|---|
| 1 | ¿En qué rango de edad se encuentra? |Categórica ordinal |object |18 a 23 años, 24 a 29 años, 30 años o más |
| 2 | ¿Con qué frecuencia compra en RetailAndina?|Categórica Ordinal |object |Semanal, Quincenal, Mensual, Menos de una vez al mes, Nunca/No compro en RetailAndina |
| 3 | En general, ¿Qué tan satisfecho se siente con RetailAndina? |Categórica Ordinal |int64 |1: Muy insatisfecho, 2: Insatisfecho, 3: Neutral, 4: Satisfecho, 5: Muy satisfecho |
| 4 | ¿Qué tan satisfecho está con los precios que ofrece RetailAndina? |Categórica ordinal |int64 |1: Muy insatisfecho, 2: Insatisfecho, 3: Neutral, 4: Satisfecho, 5: Muy satisfecho |
| 5 |¿Qué tan satisfecho está con la atención que recibe por parte del personal de RetailAndina? |Categórica ordinal |int64 |1: Muy insatisfecho, 2: Insatisfecho, 3: Neutral, 4: Satisfecho, 5: Muy satisfecho |
| 6 |¿Recomendaría RetailAndina a un conocido? |Categórica binaria |object |Sí, No |
| 7 |Si RetailAndina lanzara un programa de fidelización, ¿qué tan probable es que se inscriba? |Categórica ordinal |int64 |1 Nada probable, 2 Poco probable, 3 Probable, 4 Altamente probable, 5 Muy probable |
| 8 |	¿Qué otro beneficio esperaría de un programa de fidelización de RetailAndina? |Categórica nominal |object |Abierta, opcional. |
| 9 | ¿Cuánto gasta al mes en compras de consumo masivo, en dólares?|Categórica ordinal |object |Menos de $10, $10 a $49, $50 a $100, Más de $100 |

**Columnas adicionales del CSV:** código, fecha, origen.

**Nota:** A pesar de que las preguntas 3, 4, 5, 7 lleguen como int64, se clasifican como ordinales, el tipo de dato solo es una pista, no la clasificación en sí. Las preguntas 1, 2, 6, 8 y 9 llegan como object porque se almacenan como texto.
Exclusión: quien responda “Menos de una vez al mes” o “Nunca o no compro en RetailAndina” en la P2, o “30 o más” en la P1, no forma parte de la población y se excluye del análisis.


## 5. Análisis de sesgos


| Sesgo potencial | Mitigación |
|---|---|
| **1. Sesgo de selección:** Al encuestar a personas cercanas al círculo social de los integrantes del grupo, la muestra se parece al equipo en edad, ciudad, nivel socioeconómico y puede no representar a todos los clientes de RetailAndina |Establecer cuotas por rango de edad y pedir referidos a los contactados para ampliar la muestra fuera del círculo cercano del grupo. |
| **2. Sesgo de no respuesta:** Aquellos con opiniones extremas pueden responder en mayor magnitud que el resto, los clientes poco satisfechos pueden ignorar la encuesta.|Formulario corto, y registro de las personas contactadas frente al número de personas que efectivamente respondieron, para calcular la tasa de no respuesta. |
| **3. Sesgo de respuesta:** Al ser conocidos del equipo, los encuestados pueden dar calificaciones altas o respuestas favorables para agradar o por temor a ser juzgados.|Encuesta anónima, que aclare que no hay respuestas correctas o incorrectas, preguntas con redacción neutra y que eviten un sesgo al ser planteadas. |

## 6. Confidencialidad (RA3)

- **Datos personales que se piden:** Solo se va a solicitar la edad, necesaria para verificar el criterio de los estratos y el gasto mensual aproximado, necesario para analizar la relación entre gasto y satisfacción, no se piden más datos personales de ningún tipo.
- **Plan de anonimización:** Cada respuesta recibe un código en lugar de cualquier identificador, la lista de contactos utilizada se guarda fuera del repositorio por los integrantes del equipo. Finalmente, el CSV crudo no se subirá al fork, solo se publicará la versión anonimizada con la columna **origen** que declara de dónde vienen los datos.

## 7. Verificación con herramientas (Python/R)

El presente script tendrá acceso a los futuros datos y reportará tipos, datos faltantes y las veces que aparece una respuesta por las columnas analizadas

![alt text](salida.jpeg)

**Punto a realizar con los datos reales**

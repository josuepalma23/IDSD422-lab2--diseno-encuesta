# Plantilla de diseño — Encuesta de satisfacción (hito 1)

**Equipo:** 4 · **Integrantes:** Jordan Sangucho, Josue Palma, Aidan Carrasco, Joel Champutiz, Emily Dias· 
**Fecha:** 30/10/2026
**Repositorio (fork):** https://github.com/josuepalma23/IDSD422-lab2--diseno-encuesta
**Enfoque del equipo (aprobado en clase):** Satisfacción y expectativas

Completa cada sección. Usa commits por sección; la historia del repositorio se revisa.

> **Formato del entregable:** exporta esta plantilla completada a PDF, con el enlace de tu fork en la carátula, y guarda el PDF en `informes/` del fork. Entrega el PDF y el enlace del fork en el aula virtual.

## 1. Objetivo de la encuesta

Estimar el porcentaje de personas satisfechas en el intervalo de 18 a 29 años en una escala del 1 al 5 con respecto a RetailAndina e identificar los beneficios que el encuestado espera sobre el programa de fidelización, por otro lado, se desea identificar sesgos y desarrollar estrategias para mitigarlos por medio de implementos tecnológicos de programación, en este marco, los datos recibidos de encuestas serán analizados y por otro lado simulados en caso de ser necesario con este mismo fin, finalmente, los resultados obtenidos, junto con los análisis antes mencionados serán enviados a RetailAndina para generar conocimiento accionable sobre su modelo de negocio.

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
  - Cada integrante buscó entre sus contactos a personas que cumplan con los criterios de la población objetivo (18–29 años, residentes en Quito, compras frecuentes en consumo masivo) y las clasificó según su estrato de edad.
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
```

**Salida de la implementación en Python**

```text
    ¿Cuál es su edad en años cumplidos?  \
7                 18 a 23 años   
1                 18 a 23 años   
21                18 a 23 años   
22                18 a 23 años   
3                 18 a 23 años   
6                 24 a 29 años   
8                 24 a 29 años   
15                24 a 29 años   
9                 24 a 29 años   
14                24 a 29 años   

    ¿Con qué frecuencia compra en RetailAndina?  
7                                     Mensual  
1                                     Mensual  
21                    Al menos una vez al mes  
22                                    Mensual  
3                                     Semanal  
6                     Al menos una vez al mes  
8                     Al menos una vez al mes  
15                    Al menos una vez al mes  
9                                     Mensual  
14                    Al menos una vez al mes  
```

Este método resulta idóneo por encima de la conveniencia pura, ya que se realiza un sorteo dentro de cada estrato que reduce la influencia de qué encuestado está mas cerca de quien lo encuestó, además, por estrato se aportan la misma cantidad de respuestas, si se realizara por conveniencia las respuestas se pueden quedar acumuladas en un solo grupo.

## 4. Cuestionario (5–10 preguntas)

| # | Pregunta | Tipo de variable | Dtype al cargar | Opciones / escala |
|---|---|---|---|---|
| 1 | ¿En qué rango de edad se encuentra? |Categórica ordinal | object |18 a 23 años, 24 a 29 años, 30 años o más |
| 2 | ¿Con qué frecuencia compra en RetailAndina?|Categórica Ordinal | object |Semanal, Quincenal, Mensual, Menos de una vez al mes, Nunca/No compro en RetailAndina |
| 3 | En general, ¿Qué tan satisfecho se siente con RetailAndina? |Categórica Ordinal | int64 |1: Muy insatisfecho, 2: Insatisfecho, 3: Neutral, 4: Satisfecho, 5: Muy satisfecho |
| 4 | ¿Qué tan satisfecho está con los precios que ofrece RetailAndina? |Categórica ordinal |int64 |1: Muy insatisfecho, 2: Insatisfecho, 3: Neutral, 4: Satisfecho, 5: Muy satisfecho |
| 5 |¿Qué tan satisfecho está con la atención que recibe por parte del personal de RetailAndina? |Categórica ordinal |int64 |1: Muy insatisfecho, 2: Insatisfecho, 3: Neutral, 4: Satisfecho, 5: Muy satisfecho |
| 6 |¿Recomendaría RetailAndina a un conocido? |Categórica binaria | object |Sí, No |
| 7 |Si RetailAndina lanzara un programa de fidelización, ¿qué tan probable es que se inscriba? |Categórica ordinal |int64 |1 Nada probable, 2 Poco probable, 3 Probable, 4 Altamente probable, 5 Muy probable |
| 8 | ¿Qué otro beneficio esperaría de un programa de fidelización de RetailAndina? |Categórica nominal |object |Abierta, opcional. |
| 9 | ¿Cuánto gasta al mes en compras de consumo masivo, en dólares?|Categórica ordinal |object |Menos de $10, $10 a $49, $50 a $100, Más de $100 |

**Columnas adicionales del CSV:** código, fecha, origen.

**Nota:** A pesar de que las preguntas 3, 4, 5, 7 lleguen como int64, se clasifican como ordinales, el tipo de dato solo es una pista, no la clasificación en sí. Las preguntas 1, 2, 6, 8 y 9 llegan como object porque se almacenan como texto.
Exclusión: quien responda “Menos de una vez al mes” o “Nunca o no compro en RetailAndina” en la P2, o “30 o más” en la P1, no forma parte de la población y se excluye del análisis.

## 5. Análisis de sesgos

| Sesgo potencial | Mitigación |
|---|---|
| **1. Sesgo de selección:** Al realizar la encuesta entre contactos cercanos y red de referidos de los integrantes del grupo, la muestra se concentra de manera notable en el rango de 18 a 23 años y en compradores ocasionales, dejando subrepresentados a clientes de mayor edad y con hábitos de compra más frecuentes en RetailAndina S.A. | Establecer cuotas específicas por rango de edad y solicitar referidos fuera del círculo universitario directo, aplicando además filtros iniciales en el cuestionario para descartar a quienes no cumplan con la frecuencia o el rango poblacional establecido. |
| **2. Sesgo de no respuesta:** Las personas que tienen poca afinidad o indiferencia hacia la cadena suelen ignorar el enlace del formulario (no respuesta de unidad), mientras que los campos de texto libre provocan fatiga y omisiones voluntarias (no respuesta de ítem). | Diseñar un cuestionario breve que tome menos de tres minutos, llevar un control exacto de las personas contactadas frente a las que efectivamente respondieron para calcular la tasa de no respuesta, y convertir las preguntas abiertas en opcionales. |
| **3. Sesgo de respuesta:** Al ser conocidos o referidos de los encuestadores, los participantes pueden inclinarse a calificar de manera positiva o complaciente por cortesía, o bien marcar opciones neutrales cuando su experiencia ha sido distante. | Garantizar el anonimato absoluto en la introducción de la encuesta, aclarar explícitamente que no existen respuestas correctas o incorrectas y mantener una redacción completamente neutra con escalas de cinco puntos. |

### Conclusiones sobre sesgos en los datos reales y conteo de no respuesta

Al filtrar y analizar exclusivamente las respuestas reales recolectadas en el archivo (`origen = real`, con 23 registros), se identifican los siguientes patrones empíricos:

- **Conteo de no respuesta:** A partir del seguimiento realizado durante el operativo de campo, se contactó a 30 personas en total, de las cuales 23 completaron la encuesta de manera efectiva y 7 no respondieron, lo que representa una tasa de no respuesta de unidad del 23.3%. Respecto a la no respuesta por ítem, las preguntas cerradas no presentan valores faltantes debido a la validación obligatoria del formulario, pero la pregunta abierta sobre beneficios esperados registra 10 valores nulos sobre 23 registros, evidenciando una tasa de omisión del 43.5% ante campos de texto libre.
- **Evidencia del sesgo de selección:** Al examinar la distribución de edad en las respuestas reales, el 52.2% corresponde al grupo de 18 a 23 años, el 26.1% al grupo de 24 a 29 años y el 21.7% a mayores de 30 años. Esto confirma que la difusión en redes cercanas sobrerrepresentó a los más jóvenes. Asimismo, al aplicar los filtros de población objetivo que exigen compras de al menos una vez al mes, se observa que varios encuestados compraban con menor frecuencia o no compraban, lo que demuestra la necesidad de aplicar los filtros correctivos en la etapa de análisis.
- **Evidencia del sesgo de respuesta:** En la satisfacción general de los datos reales, predomina la valoración positiva con un 52.2% en el nivel de satisfecho y un 65.2% que indica que sí recomendaría el establecimiento. Sin embargo, al evaluar un aspecto específico como la satisfacción con los precios, la tendencia cambia hacia el descontento y la neutralidad, reflejando que los clientes expresan opiniones más críticas cuando se consulta por atributos concretos en lugar de una percepción general.

## 6. Confidencialidad (RA3)

- **Minimización de datos personales:** Para cumplir estrictamente con los principios de protección y privacidad, el cuestionario omitió la recolección de cualquier identificador directo como nombres, cédula, correos electrónicos, teléfonos o direcciones particulares. Las únicas variables demográficas y económicas solicitadas fueron la edad y el gasto mensual estimado, las cuales se estructuraron mediante intervalos cerrados y rangos monetarios para impedir la identificación individual de los participantes.
- **Plan de anonimización ejecutado:** 
  1. Se configuró el formulario en línea para no registrar correos electrónicos de los usuarios.
  2. Se eliminó la marca temporal exacta de envío, reemplazándola por una fecha estandarizada en formato ISO y asignando un código correlativo anónimo a cada registro desde R001 hasta R023 para los datos reales.
  3. Se depuraron las respuestas de texto libre para eliminar cualquier mención personal y se aseguró que el archivo bruto de contactos se mantenga en un entorno privado fuera del repositorio, publicando únicamente el conjunto de datos anonimizado y debidamente etiquetado con la columna de origen.

## Bonus: Piloteo del cuestionario (+5 puntos)

- **Ejecución del piloto:** Antes de abrir la encuesta al público general, se realizó una prueba piloto aplicando el cuestionario preliminar a dos compañeros del equipo para verificar la claridad de las preguntas y el correcto funcionamiento del almacenamiento en formato CSV.
- **Hallazgos detectados y ajustes aplicados:**
  1. **Confusión en la pregunta abierta de beneficios:** Durante la prueba, los dos compañeros respondieron con expresiones de desconcierto ante la pregunta sobre el programa de fidelización, lo que demostró que el concepto no era intuitivo y que obligar a redactar texto libre generaba respuestas sin valor analítico. Se decidió configurar dicha pregunta como opcional y añadir una breve introducción aclaratoria al compartir el enlace.
  2. **Inconsistencias en el formato de exportación:** Se detectó que el sistema generaba saltos de línea y caracteres especiales en los encabezados al exportar a CSV, además de truncar las etiquetas de las escalas de satisfacción. Se estandarizó la limpieza de cabeceras y la asignación numérica de las escalas Likert en el script de preparación para asegurar una correcta lectura de los tipos de datos al cargar el archivo en pandas.

## 7. Verificación con herramientas (Python/R)

El presente script tendrá acceso a los futuros datos y reportará tipos, datos faltantes y las veces que aparece una respuesta por las columnas analizadas

![alt text](salida.jpeg)

**Punto a realizar con los datos reales**

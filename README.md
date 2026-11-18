# PAES App

App móvil (Flutter, Android e iOS) para practicar la PAES chilena.

## Qué hace
- 5 pruebas: Competencia Lectora, Matemática M1, Matemática M2, Ciencias, Historia.
- **Práctica**: eliges la prueba y cuántas preguntas; sin reloj; ves al instante si acertaste.
- **Simulacro**: con el tiempo oficial de cada prueba; las respuestas se ven al final.
- **Puntaje estimado** de 100 a 1000. Es una fórmula propia y aproximada, no usa tablas del DEMRE.
- **Ver explicación**: abre una búsqueda en Google con la pregunta (necesita internet).
- **30 preguntas gratis** en total. Luego, pago único "Acceso Completo PAES" ($4.000 CLP).
- Historial de ensayos.

## Preguntas
Meta: **500 preguntas por prueba, 100 de ellas con imagen o gráfico**. En cada ensayo
(práctica o simulacro) se eligen preguntas al azar y se mezclan sus alternativas.

| Prueba | Preguntas | Con gráfico |
|---|---|---|
| Matemática M1 | 500 | 100 |
| Matemática M2 | 500 | 100 |
| Ciencias | 500 | 100 |
| Historia | 500 | 100 |
| Competencia Lectora | 500 | 100 |

Hay un archivo por prueba en `assets/questions/` (`m1.json`, `m2.json`, `ciencias.json`,
`historia.json`, `lectora.json`). Las imágenes van en `assets/images/<prueba>/`.
Cada pregunta tiene: `id`, `prueba`, `enunciado`, `alternativas`, `correcta`
(posición de la correcta, empezando en 0), `eje` (opcional), `explicacion` e `imagen` (opcional).

### M1 generada con programa
`tools/generar_m1.py` crea las 500 preguntas de M1 y sus 100 gráficos. Cada respuesta
correcta la calcula el programa y cada gráfico se dibuja con los mismos datos de la pregunta.
Para volver a generarlas (necesita Python y matplotlib):
```
python3 tools/generar_m1.py
```
`tools/generar_m2.py` hace lo mismo para M2 (logaritmos, matemática financiera, funciones
exponencial, logarítmica y trigonométricas, circunferencia, esfera, homotecia, rectas,
dispersión, probabilidad condicional, combinatoria, binomial y normal).

`tools/generar_ciencias.py` crea Ciencias (Biología, Física y Química): 239 preguntas de
conceptos escritas a partir de listas de datos (`tools/ciencias_textos.py`), cálculos resueltos
por el programa y 100 gráficos (`tools/ciencias_graficos.py`).

`tools/generar_historia.py` crea Historia y Ciencias Sociales (Historia, Formación ciudadana y
Sistema económico) a partir de las tablas de `tools/historia_datos.py` (fechas, personajes,
conceptos, institucionalidad, economía). Los gráficos usan hechos reales (líneas de tiempo) o
datos de países ficticios, para practicar lectura de fuentes sin inventar cifras reales.

`tools/generar_lectora.py` arma Competencia Lectora: 50 textos originales escritos para la app
(`tools/lectora_textos_a.py` a `_e.py`, 8 preguntas cada uno, en las habilidades Localizar,
Interpretar y Evaluar) y 100 preguntas sobre afiches, infografías y programas ficticios.
El texto de lectura se guarda en el campo `texto` y la app lo muestra sobre la pregunta.

Igual conviene que un profesor revise una muestra antes de publicar.

**Importante:** no se debe usar contenido del DEMRE (sus documentos son "sin fines comerciales").

## Estructura
- `lib/domain`: reglas y modelos (preguntas, pruebas, puntaje).
- `lib/data`: lectura de preguntas y almacenamiento en el teléfono.
- `lib/presentation`: pantallas y estado (Riverpod).

## Antes de publicar en las tiendas
1. Crear el producto **no consumible** con ID `acceso_completo_paes` ("Acceso Completo PAES", $4.000 CLP)
   en Google Play Console y en App Store Connect.
2. Cambiar el identificador de la app (`cl.paesapp.paes_app`) por el definitivo.
3. Agregar muchas más preguntas, revisadas por un profesor.
4. Probar la compra en un teléfono real con cuentas de prueba.

## Cómo correrla
```
flutter pub get
flutter run
```

# Retopaes

App móvil (Flutter, Android e iOS) para practicar la PAES chilena.

## Marca
- Nombre: **Retopaes** (`appName` en `lib/core/constants.dart`, `android:label` en
  `AndroidManifest.xml` y `CFBundleDisplayName` en `ios/Runner/Info.plist`).
- Logo original: `assets/branding/logo_retopaes_original.jpg`. Colores: azul marino `#022658` y
  naranjo `#FC5D07`.
- Ícono de la app: `assets/branding/icono_app.png` (generado con `dart run flutter_launcher_icons`).
- Pantalla de bienvenida del teléfono: `assets/branding/splash_logo.png` y, en Android 12 o
  superior, `assets/branding/splash_android12.png` (generada con
  `dart run flutter_native_splash:create`). Luego, mientras cargan las preguntas, la app muestra
  el logo completo en blanco.

## Qué hace
- 5 pruebas: Competencia Lectora, Matemática M1, Matemática M2, Ciencias, Historia.
- **Práctica**: eliges la prueba y cuántas preguntas (de 1 a 65, el largo de un ensayo real); sin
  reloj; ves al instante si acertaste. La app no muestra cuántas preguntas tiene el banco.
- **Simulacro**: con el tiempo oficial de cada prueba; las respuestas se ven al final.
  Como con el cuadernillo en papel, se puede saltar preguntas, volver atrás («Anterior»),
  cambiar respuestas e ir a cualquier pregunta desde el mapa de preguntas (botón de cuadrícula),
  que muestra cuáles están respondidas.
  Al tocar **«Entregar»** (en la última pregunta o desde el mapa) aparece un resumen: cuántas
  preguntas se respondieron, el tiempo restante y los números de las que quedan sin responder
  (se puede tocar una para ir a ella). Luego se elige «Entregar» o «Seguir revisando».
  Si se acaba el tiempo, el ensayo se entrega solo.
  Avisos de tiempo: un mensaje cuando quedan 30, 10 y 5 minutos, y el reloj en rojo en los
  últimos 5 minutos. El reloj usa la hora real: sigue corriendo aunque se salga de la app,
  como en la prueba real.
  En Ciencias se elige el módulo (Biología, Física, Química o Técnico Profesional), como en la
  prueba real: 54 preguntas del Módulo Común (18 por eje) y luego 26 del módulo elegido
  (en Técnico Profesional: 9 de Biología, 9 de Física y 8 de Química).
- En **Competencia Lectora** (práctica y simulacro) las preguntas de un mismo texto o infografía
  van juntas, en orden Localizar → Interpretar → Evaluar, con el aviso «Texto 2 · Preguntas 10 a 18».
  El simulacro tiene, como la prueba real, **7 textos y 65 preguntas**: siempre al menos una
  narración y una infografía; a 5 textos se les quita una pregunta para llegar a 65.
  Las imágenes se pueden tocar para verlas en pantalla completa y hacer zoom.
- **Puntaje estimado** de 100 a 1000, que imita la forma del puntaje real
  (`lib/domain/score_calculator.dart`): 0 correctas = 100 y solo todas correctas = 1000; las
  primeras y las últimas respuestas correctas valen más que las del medio (curva logística); las
  malas no restan. Como en la prueba real, en cada simulacro 5 preguntas elegidas al azar son de
  experimentación y no cuentan (por ejemplo, M1 cuenta 60 de 65); en los resultados se muestra
  cuáles fueron. Es una fórmula propia: no usa las tablas del DEMRE.
- **Ver explicación**: abre una búsqueda en Google con la pregunta (necesita internet).
- **Gratis**: 30 preguntas de Práctica (en total, sumando todas las pruebas) y, además,
  **1 simulacro completo** de cualquier prueba. Las respuestas del simulacro no descuentan de
  las 30. El simulacro gratis se marca como usado al tocar «Comenzar» (aunque no se termine),
  para que no se pueda repetir. Luego, pago único "Acceso Completo Retopaes" ($4.000 CLP) que da
  **6 meses** de acceso completo y no se renueva solo. En la pantalla de inicio se ve hasta qué
  fecha dura; al terminar, la app vuelve a la versión gratis.
- **Sin repetir preguntas**: cada ensayo usa primero las preguntas que la persona aún no ha visto;
  cuando ya vio todas las de una prueba, comienza un ciclo nuevo.
- **Repasar mis errores**: botón en cada prueba para practicar solo las preguntas respondidas mal
  (una pregunta sale de la lista cuando se responde bien).
- **Historial y avance**: gráfico con el puntaje de los simulacros de cada prueba y aciertos por eje
  (o por habilidad, en Lectora), con el punto más débil destacado. Los resultados de cada ensayo
  también muestran los aciertos por eje.
- **Marcar para revisar** (simulacro): banderita para marcar preguntas dudosas; se ven en el mapa
  y en el resumen antes de entregar.
- **Ajustes**: tamaño de letra (Normal, Grande, Muy grande) y política de privacidad.
- **Cuenta regresiva** para la próxima PAES. Las fechas están en `paesDates`
  (`lib/core/constants.dart`) y hay que agregarlas cuando el DEMRE las publique.
- **Colores** (`lib/presentation/prueba_style.dart`): la app usa los colores del logo (azul marino
  en botones y textos destacados; naranjo como acento en bordes y avisos) y cada prueba tiene su color e ícono en su tarjeta, sus botones y la barra del ensayo: Lectora
  granate, M1 azul, M2 azul oscuro, Ciencias verde (Biología verde, Física naranjo, Química morado)
  e Historia café. Las respuestas correctas e incorrectas llevan ✓ y ✗, no solo color.

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
(posición de la correcta, empezando en 0), `eje` (opcional), `area` (opcional, área temática), `explicacion`, `imagen` (opcional)
`texto` (opcional, texto de lectura), `texto_tipo` (Lectora: `literario`, `no literario` o
`discontinuo`) y `tipo` (opcional: `suficiencia` = suficiencia de datos, con sus opciones en orden fijo).

Todos los bancos se revisaron contra los temarios oficiales de la PAES Regular 2026 (Admisión 2027).

### M1 generada con programa
`tools/generar_m1.py` crea las 500 preguntas de M1 y sus 100 gráficos (incluye parábolas y
diagramas de cajón), solo con temas del temario 2027: números, potencias y raíces enésimas,
porcentaje, álgebra, función lineal y cuadrática, áreas y volúmenes, transformaciones isométricas,
semejanza, datos, cuartiles y percentiles, y reglas de probabilidad. Cada respuesta
correcta la calcula el programa y cada gráfico se dibuja con los mismos datos de la pregunta.
Para volver a generarlas (necesita Python y matplotlib):
```
python3 tools/generar_m1.py
```
`tools/generar_m2.py` hace lo mismo para M2 (logaritmos, matemática financiera, funciones
exponencial, logarítmica y trigonométricas, circunferencia, esfera, homotecia, rectas,
dispersión, probabilidad condicional, combinatoria, binomial y normal).
Incluye 40 preguntas de **suficiencia de datos** (`tools/m2_suficiencia.py`): no se pide calcular,
sino decidir si la información (1) y (2) alcanza. Tienen 5 opciones (A a E) siempre en el mismo
orden, como en la prueba real, y las respuestas correctas se reparten por igual entre A, B, C, D y E.
En la app aparece un recuadro de ayuda que explica qué significa cada opción.

`tools/generar_ciencias.py` crea Ciencias (Biología, Física y Química) siguiendo el temario
oficial de la prueba de Ciencias: cada pregunta lleva su `eje` y su `area` (área temática
oficial, por ejemplo «Mecánica» o «Herencia y evolución»). Incluye 231 preguntas de conceptos
(`tools/ciencias2_conceptos_bio.py` y `tools/ciencias2_conceptos_fq.py`), 70 de habilidades
científicas sobre experimentos (`tools/ciencias2_habilidades.py`), cálculos resueltos por el
programa sin necesidad de calculadora (`tools/ciencias2_calculos.py`) y 100 gráficos
(`tools/ciencias2_graficos.py`). El contenido común sirve para los módulos de Biología, Física,
Química y Técnico Profesional, porque el temario oficial es el mismo para los cuatro.

`tools/generar_historia.py` crea Historia y Ciencias Sociales (Historia, Formación ciudadana y
Sistema económico) a partir de las tablas de `tools/historia_datos.py` (hechos, personajes,
conceptos, institucionalidad, economía) y de 46 fuentes originales con preguntas de análisis
(`tools/historia_fuentes_a.py` y `_b.py`: testimonios y documentos ficticios verosímiles, e
interpretaciones historiográficas contrastadas). No pregunta años exactos de memoria. Los gráficos
usan hechos reales (líneas de tiempo) o datos de países ficticios.

`tools/generar_lectora.py` arma Competencia Lectora según el temario 2027: 40 textos originales
(narraciones y textos no literarios, de 226 a 336 palabras) con 10 preguntas cada uno, y 10
infografías (textos discontinuos) con 10 preguntas cada una. Los textos base están en
`tools/lectora_textos_a.py` a `_e.py` y se amplían con `tools/lectora2_amplia_*.py` y
`tools/lectora2_amplia2.py` (oraciones agregadas dentro de los párrafos, sin cambiar su
numeración); las infografías están en `tools/lectora2_infografias.py`. No hay poemas ni preguntas
de clasificación («¿Qué tipo de texto es?»), que el temario no evalúa.

Igual conviene que un profesor revise una muestra antes de publicar.

**Importante:** no se debe usar contenido del DEMRE (sus documentos son "sin fines comerciales").

## Estructura
- `lib/domain`: reglas y modelos (preguntas, pruebas, puntaje).
- `lib/data`: lectura de preguntas y almacenamiento en el teléfono.
- `lib/presentation`: pantallas y estado (Riverpod).

## Antes de publicar en las tiendas
1. Crear el producto "Acceso Completo Retopaes" ($4.000 CLP, **6 meses, sin renovación automática**),
   con el ID `acceso_completo_retopaes` en ambas tiendas:
   - Google Play Console: **Suscripción** con ID `acceso_completo_retopaes` y un plan básico de tipo
     **prepago** (*prepaid*) de **6 meses**.
   - App Store Connect: **Suscripción no renovable** (*Non-Renewing Subscription*) con ID
     `acceso_completo_retopaes`.
   La app guarda en el teléfono hasta cuándo dura el acceso (`lib/domain/access_period.dart`): una
   compra nueva suma 6 meses desde el final del acceso vigente; una compra restaurada cuenta 6 meses
   desde la fecha de pago. Atrasar el reloj del teléfono no alarga el acceso.
2. Identificador definitivo: `cl.retopaes.app` (Android e iOS). No se puede cambiar después de publicar.
   Firma para Google Play: la llave de subida (`retopaes-upload.jks`) y sus claves (`key.properties`)
   **no se suben a GitHub**. Para compilar firmado, copiar `key.properties` en `android/` (con la ruta
   correcta en `storeFile`). Sin ese archivo, la app se firma con la llave de prueba.
   Política de privacidad: `assets/legal/politica_privacidad.md` (se ve en Ajustes; su enlace de
   GitHub sirve para las tiendas). Falta completar el correo de contacto.
3. Que un profesor de cada asignatura revise una muestra de preguntas.
4. Probar la compra en un teléfono real con cuentas de prueba.

## Cómo correrla
```
flutter pub get
flutter run
```

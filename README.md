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
Están en `assets/questions/questions.json`. Para cambiarlas o agregar más, solo se edita ese archivo.
Cada pregunta tiene: `id`, `prueba` (lectora, m1, m2, ciencias, historia), `enunciado`,
`alternativas`, `correcta` (posición de la correcta, empezando en 0), `eje` (opcional) y `explicacion`.
Las alternativas se mezclan al azar en cada ensayo.

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

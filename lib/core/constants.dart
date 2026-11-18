// Valores fijos de la aplicación.

/// Preguntas gratis en Práctica (suma de todas las pruebas).
const int freeQuestionLimit = 30;

/// Además, se regala 1 simulacro completo (de cualquier prueba). Sus respuestas
/// no descuentan de las preguntas gratis de Práctica.
const int freeSimulacroLimit = 1;

/// Identificador del producto en Google Play y App Store.
/// Debe crearse con este mismo nombre como producto "no consumible"
/// (compra única) llamado "Acceso Completo PAES".
const String fullAccessProductId = 'acceso_completo_paes';

/// Precio que se muestra si la tienda aún no entrega el precio real.
const String fallbackPriceLabel = r'$4.000 CLP';

/// Carpeta con las preguntas: un archivo por prueba (por ejemplo `m1.json`).
/// Se pueden reemplazar o ampliar sin tocar el código.
const String questionsAssetDir = 'assets/questions';

// Valores fijos de la aplicación.

/// Cantidad total de preguntas gratis (suma de todas las pruebas).
const int freeQuestionLimit = 30;

/// Identificador del producto en Google Play y App Store.
/// Debe crearse con este mismo nombre como producto "no consumible"
/// (compra única) llamado "Acceso Completo PAES".
const String fullAccessProductId = 'acceso_completo_paes';

/// Precio que se muestra si la tienda aún no entrega el precio real.
const String fallbackPriceLabel = r'$4.000 CLP';

/// Ruta del archivo con las preguntas. Se puede reemplazar sin tocar el código.
const String questionsAssetPath = 'assets/questions/questions.json';

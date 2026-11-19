// Valores fijos de la aplicación.

/// Nombre de la app.
const String appName = 'Retopaes';

/// Logo completo (pantalla de bienvenida) e ícono (barra superior).
const String logoAsset = 'assets/branding/logo_retopaes.png';
const String iconAsset = 'assets/branding/icono_app.png';

/// Máximo de preguntas que se pueden elegir en una Práctica (el largo de un
/// ensayo real). Así la app no deja ver cuántas preguntas tiene el banco.
const int maxPracticeQuestions = 65;

/// Preguntas gratis en Práctica (suma de todas las pruebas).
const int freeQuestionLimit = 30;

/// Además, se regala 1 simulacro completo (de cualquier prueba). Sus respuestas
/// no descuentan de las preguntas gratis de Práctica.
const int freeSimulacroLimit = 1;

/// Identificador del producto en Google Play y App Store.
/// Debe crearse con este mismo nombre como producto "no consumible"
/// (compra única) llamado "Acceso Completo Retopaes".
const String fullAccessProductId = 'acceso_completo_retopaes';

/// Precio que se muestra si la tienda aún no entrega el precio real.
const String fallbackPriceLabel = r'$4.000 CLP';

/// Carpeta con las preguntas: un archivo por prueba (por ejemplo `m1.json`).
/// Se pueden reemplazar o ampliar sin tocar el código.
const String questionsAssetDir = 'assets/questions';

/// Política de privacidad (se muestra en Ajustes y se publica en las tiendas).
const String privacyPolicyAsset = 'assets/legal/politica_privacidad.md';

/// Fechas de la PAES para la cuenta regresiva de la pantalla de inicio:
/// (nombre, primer día, último día). Hay que agregar las fechas nuevas cuando
/// el DEMRE las publique; si no hay ninguna próxima, la cuenta no aparece.
final List<(String, DateTime, DateTime)> paesDates = [
  ('PAES Regular', DateTime(2026, 11, 30), DateTime(2026, 12, 2)),
];

/// Tamaños de letra que se pueden elegir en Ajustes.
const Map<String, double> textScales = {
  'Normal': 1.0,
  'Grande': 1.15,
  'Muy grande': 1.3,
};

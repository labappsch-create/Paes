import 'package:material_ui/material_ui.dart';

import '../domain/prueba.dart';

/// Colores de la app, en un solo lugar.
///
/// - La app en general usa un color neutro (gris azulado).
/// - Cada prueba tiene su color, que se usa solo en lo que la identifica:
///   su tarjeta y botones en el inicio, y la barra de arriba durante el ensayo.
/// - Todos los colores de prueba son lo bastante oscuros para que el texto
///   blanco sobre ellos se lea bien.
abstract final class AppColors {
  /// Color neutro de la app (inicio, historial, pago).
  static const neutral = Color(0xFF455A64);

  static const lectora = Color(0xFF8E1B2E); // rojo granate
  static const m1 = Color(0xFF1E6FD9); // azul
  static const m2 = Color(0xFF0D2F6E); // azul oscuro
  static const ciencias = Color(0xFF2E7D32); // verde
  static const historia = Color(0xFF6D4C41); // café

  // Ejes de Ciencias.
  static const biologia = ciencias;
  static const fisica = Color(0xFFBF360C); // naranjo
  static const quimica = Color(0xFF6A1B9A); // morado

  /// Respuesta correcta e incorrecta. Siempre van con ✓ o ✗, para no depender
  /// solo del color.
  static const correcto = Color(0xFF1B873F);
}

extension PruebaStyle on Prueba {
  Color get color => switch (this) {
    Prueba.lectora => AppColors.lectora,
    Prueba.m1 => AppColors.m1,
    Prueba.m2 => AppColors.m2,
    Prueba.ciencias => AppColors.ciencias,
    Prueba.historia => AppColors.historia,
  };

  IconData get icon => switch (this) {
    Prueba.lectora => Icons.menu_book,
    Prueba.m1 => Icons.calculate,
    Prueba.m2 => Icons.functions,
    Prueba.ciencias => Icons.science,
    Prueba.historia => Icons.public,
  };
}

/// Color de un eje de Ciencias (Biología, Física, Química). Null si no es uno.
Color? cienciasEjeColor(String? eje) => switch (eje) {
  'Biología' => AppColors.biologia,
  'Física' => AppColors.fisica,
  'Química' => AppColors.quimica,
  _ => null,
};

/// Tema para una pantalla de ensayo: igual al de la app, pero con la barra de
/// arriba del color de la prueba.
ThemeData pruebaTheme(ThemeData base, Color color) => base.copyWith(
  appBarTheme: base.appBarTheme.copyWith(
    backgroundColor: color,
    foregroundColor: Colors.white,
  ),
  progressIndicatorTheme: base.progressIndicatorTheme.copyWith(
    color: Colors.white,
    linearTrackColor: Colors.white24,
  ),
);

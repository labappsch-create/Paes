/// Las cinco pruebas de la PAES y su duración y cantidad de preguntas
/// del simulacro.
enum Prueba {
  lectora('lectora', 'Competencia Lectora', 65, 150),
  m1('m1', 'Matemática M1', 65, 140),
  m2('m2', 'Matemática M2', 55, 140),
  ciencias('ciencias', 'Ciencias', 80, 160),
  historia('historia', 'Historia y Ciencias Sociales', 65, 120);

  const Prueba(this.key, this.label, this.simulacroQuestions, this.minutes);

  /// Texto usado en el archivo de preguntas.
  final String key;

  /// Nombre que ve el usuario.
  final String label;

  /// Cantidad de preguntas del simulacro completo.
  final int simulacroQuestions;

  /// Tiempo del simulacro, en minutos.
  final int minutes;

  /// Preguntas de experimentación: como en la prueba real, 5 preguntas de
  /// cada simulacro no cuentan para el puntaje y no se sabe cuáles son.
  static const experimentalQuestions = 5;

  /// Preguntas del simulacro que cuentan para el puntaje (por ejemplo, 60 de 65).
  int get scoredQuestions => simulacroQuestions - experimentalQuestions;

  static Prueba fromKey(String key) =>
      Prueba.values.firstWhere((p) => p.key == key);
}

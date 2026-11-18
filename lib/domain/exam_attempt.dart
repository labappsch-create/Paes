import 'prueba.dart';

enum QuizMode {
  practice('Práctica'),
  simulacro('Simulacro');

  const QuizMode(this.label);
  final String label;
}

/// Resultado guardado de un ensayo, para el historial.
class ExamAttempt {
  const ExamAttempt({
    required this.date,
    required this.prueba,
    required this.mode,
    required this.total,
    required this.correct,
    required this.score,
    this.modulo,
  });

  final DateTime date;
  final Prueba prueba;
  final QuizMode mode;
  final int total;
  final int correct;
  final int score;

  /// Módulo elegido en Ciencias (por ejemplo «Física»). Null en las demás pruebas.
  final String? modulo;

  /// Nombre de la prueba con su módulo, si tiene: «Ciencias – Física».
  String get pruebaLabel =>
      modulo == null ? prueba.label : '${prueba.label} – $modulo';

  Map<String, dynamic> toJson() => {
    'date': date.toIso8601String(),
    'prueba': prueba.key,
    'mode': mode.name,
    'total': total,
    'correct': correct,
    'score': score,
    if (modulo != null) 'modulo': modulo,
  };

  factory ExamAttempt.fromJson(Map<String, dynamic> json) => ExamAttempt(
    date: DateTime.parse(json['date'] as String),
    prueba: Prueba.fromKey(json['prueba'] as String),
    mode: QuizMode.values.byName(json['mode'] as String),
    total: json['total'] as int,
    correct: json['correct'] as int,
    score: json['score'] as int,
    modulo: json['modulo'] as String?,
  );
}

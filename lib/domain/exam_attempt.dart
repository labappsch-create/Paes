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
    this.porEje = const {},
  });

  final DateTime date;
  final Prueba prueba;
  final QuizMode mode;
  final int total;
  final int correct;
  final int score;

  /// Módulo elegido en Ciencias (por ejemplo «Física»). Null en las demás pruebas.
  final String? modulo;

  /// Aciertos por eje (o habilidad, en Lectora): eje -> [correctas, total].
  final Map<String, List<int>> porEje;

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
    if (porEje.isNotEmpty) 'por_eje': porEje,
  };

  factory ExamAttempt.fromJson(Map<String, dynamic> json) => ExamAttempt(
    date: DateTime.parse(json['date'] as String),
    prueba: Prueba.fromKey(json['prueba'] as String),
    mode: QuizMode.values.byName(json['mode'] as String),
    total: json['total'] as int,
    correct: json['correct'] as int,
    score: json['score'] as int,
    modulo: json['modulo'] as String?,
    porEje: {
      for (final e
          in ((json['por_eje'] as Map<String, dynamic>?) ?? const {}).entries)
        e.key: List<int>.from(e.value as List),
    },
  );
}

/// Suma los aciertos por eje de varios ensayos: eje -> [correctas, total].
Map<String, List<int>> sumarPorEje(Iterable<ExamAttempt> attempts) {
  final out = <String, List<int>>{};
  for (final a in attempts) {
    for (final e in a.porEje.entries) {
      final acc = out.putIfAbsent(e.key, () => [0, 0]);
      acc[0] += e.value[0];
      acc[1] += e.value[1];
    }
  }
  return out;
}

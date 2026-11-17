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
  });

  final DateTime date;
  final Prueba prueba;
  final QuizMode mode;
  final int total;
  final int correct;
  final int score;

  Map<String, dynamic> toJson() => {
        'date': date.toIso8601String(),
        'prueba': prueba.key,
        'mode': mode.name,
        'total': total,
        'correct': correct,
        'score': score,
      };

  factory ExamAttempt.fromJson(Map<String, dynamic> json) => ExamAttempt(
        date: DateTime.parse(json['date'] as String),
        prueba: Prueba.fromKey(json['prueba'] as String),
        mode: QuizMode.values.byName(json['mode'] as String),
        total: json['total'] as int,
        correct: json['correct'] as int,
        score: json['score'] as int,
      );
}

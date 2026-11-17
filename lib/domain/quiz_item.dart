import 'dart:math';

import 'question.dart';

/// Una pregunta dentro de un ensayo, con sus alternativas en orden mezclado
/// y la respuesta que eligió la persona.
class QuizItem {
  QuizItem(this.question, this.order);

  final Question question;

  /// Orden mezclado: `order[i]` es la posición original de la alternativa
  /// que se muestra en el lugar `i`.
  final List<int> order;

  /// Lugar (en pantalla) de la alternativa elegida. Null si no respondió.
  int? selected;

  /// Alternativas en el orden que se muestran.
  List<String> get options => [for (final i in order) question.alternativas[i]];

  /// Lugar en pantalla de la alternativa correcta.
  int get correctDisplayIndex => order.indexOf(question.correcta);

  bool get isAnswered => selected != null;

  bool get isCorrect => selected == correctDisplayIndex;
}

/// Elige [count] preguntas al azar de [pool] y mezcla sus alternativas.
/// Así la respuesta correcta no queda siempre en la misma letra.
List<QuizItem> buildSession(
  List<Question> pool,
  int count, {
  required Random random,
}) {
  final chosen = List<Question>.of(pool)..shuffle(random);
  return [
    for (final q in chosen.take(count))
      QuizItem(
        q,
        List<int>.generate(q.alternativas.length, (i) => i)..shuffle(random),
      ),
  ];
}

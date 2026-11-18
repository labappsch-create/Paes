import 'dart:math';

import 'question.dart';

/// Una pregunta dentro de un ensayo, con sus alternativas en orden mezclado
/// y la respuesta que eligió la persona.
class QuizItem {
  QuizItem(this.question, this.order);

  /// Crea la pregunta con sus alternativas mezcladas al azar.
  /// En suficiencia de datos no se mezclan: sus opciones van siempre en el
  /// mismo orden, como en la prueba real.
  factory QuizItem.shuffled(Question question, Random random) {
    final order = List<int>.generate(question.alternativas.length, (i) => i);
    if (!question.isSuficiencia) order.shuffle(random);
    return QuizItem(question, order);
  }

  final Question question;

  /// Orden mezclado: `order[i]` es la posición original de la alternativa
  /// que se muestra en el lugar `i`.
  final List<int> order;

  /// Lugar (en pantalla) de la alternativa elegida. Null si no respondió.
  int? selected;

  /// Pregunta de experimentación: se responde igual, pero no cuenta para el
  /// puntaje. Solo se revela en los resultados.
  bool experimental = false;

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
  return [for (final q in chosen.take(count)) QuizItem.shuffled(q, random)];
}

/// Marca al azar [count] preguntas del simulacro como de experimentación,
/// como en la prueba real. Si hay muy pocas preguntas, no marca ninguna.
void markExperimental(
  List<QuizItem> items,
  int count, {
  required Random random,
}) {
  if (items.length <= count) return;
  final indices = List<int>.generate(items.length, (i) => i)..shuffle(random);
  for (final i in indices.take(count)) {
    items[i].experimental = true;
  }
}

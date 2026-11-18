import 'dart:math';

import 'question.dart';
import 'quiz_item.dart';

/// Orden de las preguntas dentro de un mismo texto: primero localizar,
/// luego interpretar y al final evaluar, como suele ocurrir en la prueba.
const _ordenHabilidad = {'Localizar': 0, 'Interpretar': 1, 'Evaluar': 2};

/// Arma un ensayo de Competencia Lectora con [count] preguntas, como en la
/// prueba real: las preguntas de un mismo texto van juntas y seguidas.
///
/// Usa textos completos (todas sus preguntas) y algunas preguntas con imagen
/// (afiches, infografías), que tienen una pregunta cada una. Los textos y las
/// imágenes aparecen en orden al azar. Solo si no alcanza el número pedido,
/// el último texto queda con menos preguntas.
List<QuizItem> buildLectoraSession(
  List<Question> pool,
  int count, {
  required Random random,
}) {
  final porTexto = <String, List<Question>>{};
  final sueltas = <Question>[];
  for (final q in pool) {
    final t = q.texto;
    if (t == null || t.isEmpty) {
      sueltas.add(q);
    } else {
      porTexto.putIfAbsent(t, () => []).add(q);
    }
  }
  final textos = porTexto.values.toList()..shuffle(random);
  sueltas.shuffle(random);

  // Cerca de 1 de cada 7 preguntas es con imagen (en un simulacro de 65: 9).
  var nSueltas = min(count ~/ 7, sueltas.length);
  if (textos.isEmpty) nSueltas = min(count, sueltas.length);
  var faltan = count - nSueltas;

  final bloques = <List<Question>>[];
  for (final grupo in textos) {
    if (faltan <= 0) break;
    grupo
      ..shuffle(random)
      ..sort(
        (a, b) => (_ordenHabilidad[a.eje] ?? 1).compareTo(
          _ordenHabilidad[b.eje] ?? 1,
        ),
      );
    final tomadas = grupo.take(faltan).toList();
    bloques.add(tomadas);
    faltan -= tomadas.length;
  }
  // Si no alcanzaron los textos, se completa con más preguntas con imagen.
  nSueltas = min(sueltas.length, nSueltas + max(0, faltan));
  for (final q in sueltas.take(nSueltas)) {
    bloques.add([q]);
  }
  bloques.shuffle(random);

  return [
    for (final b in bloques)
      for (final q in b) QuizItem.shuffled(q, random),
  ];
}

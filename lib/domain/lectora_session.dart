import 'dart:math';

import 'question.dart';
import 'quiz_item.dart';

/// Orden de las preguntas dentro de un mismo texto: primero localizar,
/// luego interpretar y al final evaluar, como suele ocurrir en la prueba.
const _ordenHabilidad = {'Localizar': 0, 'Interpretar': 1, 'Evaluar': 2};

/// Preguntas que trae cada texto del banco.
const preguntasPorTexto = 10;

/// Texto al que pertenece una pregunta de Lectora: su texto continuo o, si es
/// una infografía, su imagen. Null si la pregunta no pertenece a un texto.
String? lectoraTextoKey(Question q) {
  final t = q.texto;
  if (t != null && t.isNotEmpty) return t;
  return q.imagen;
}

/// Arma un ensayo de Competencia Lectora con [count] preguntas, como en la
/// prueba real (7 textos y 65 preguntas):
/// - Las preguntas de un mismo texto van juntas y en orden
///   (localizar → interpretar → evaluar).
/// - Se usan tantos textos como hagan falta (10 preguntas cada uno); si
///   sobran preguntas, se quita una de varios textos distintos, para que
///   todos los textos queden casi completos.
/// - Desde 3 textos, se incluye al menos un texto literario (narración) y al
///   menos uno discontinuo (infografía).
List<QuizItem> buildLectoraSession(
  List<Question> pool,
  int count, {
  required Random random,
}) {
  final porTexto = <String, List<Question>>{};
  for (final q in pool) {
    final key = lectoraTextoKey(q);
    if (key != null) porTexto.putIfAbsent(key, () => []).add(q);
  }
  final grupos = porTexto.values.toList()..shuffle(random);
  if (grupos.isEmpty || count <= 0) return [];

  final necesarios = min(
    grupos.length,
    (count + preguntasPorTexto - 1) ~/ preguntasPorTexto,
  );
  final elegidos = <List<Question>>[];
  void tomarPrimero(bool Function(List<Question>) cumple) {
    final i = grupos.indexWhere(cumple);
    if (i >= 0) elegidos.add(grupos.removeAt(i));
  }

  if (necesarios >= 3) {
    tomarPrimero((g) => g.first.textoTipo == 'literario');
    tomarPrimero((g) => g.first.textoTipo == 'discontinuo');
  }
  while (elegidos.length < necesarios && grupos.isNotEmpty) {
    elegidos.add(grupos.removeAt(0));
  }

  // Cada texto con sus preguntas mezcladas y luego ordenadas por habilidad.
  final bloques = [
    for (final g in elegidos)
      (List<Question>.of(g)..shuffle(random))..sort(
        (a, b) => (_ordenHabilidad[a.eje] ?? 1).compareTo(
          _ordenHabilidad[b.eje] ?? 1,
        ),
      ),
  ];

  // Si sobran preguntas, se quita una de varios textos distintos.
  var sobran = bloques.fold<int>(0, (s, b) => s + b.length) - count;
  final orden = List<int>.generate(bloques.length, (i) => i)..shuffle(random);
  var k = 0;
  while (sobran > 0) {
    final b = bloques[orden[k % orden.length]];
    if (b.length > 1) {
      b.removeAt(random.nextInt(b.length));
      sobran--;
    }
    k++;
  }

  bloques.shuffle(random);
  return [
    for (final b in bloques)
      for (final q in b) QuizItem.shuffled(q, random),
  ];
}

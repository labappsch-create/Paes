import 'dart:math';

import 'question.dart';
import 'quiz_item.dart';

/// Módulo que elige la persona en la prueba de Ciencias.
///
/// La prueba real tiene 80 preguntas: 54 del Módulo Común (preguntas de los
/// tres ejes) y 26 del módulo elegido (Biología, Física, Química o
/// Técnico Profesional).
enum CienciasModulo {
  biologia('Biología', 'Biología'),
  fisica('Física', 'Física'),
  quimica('Química', 'Química'),
  tecnicoProfesional('Técnico Profesional', null);

  const CienciasModulo(this.label, this.eje);

  /// Nombre que ve el usuario.
  final String label;

  /// Eje de las 26 preguntas del módulo. Null en Técnico Profesional,
  /// que mezcla los tres ejes.
  final String? eje;
}

const cienciasEjes = ['Biología', 'Física', 'Química'];

/// Preguntas del Módulo Común por eje (3 × 18 = 54).
const comunPorEje = 18;

/// Preguntas del módulo elegido.
const preguntasModulo = 26;

/// Reparto de las 26 preguntas del módulo Técnico Profesional entre los ejes.
const tpPorEje = {'Biología': 9, 'Física': 9, 'Química': 8};

/// Arma un simulacro de Ciencias: primero el Módulo Común ordenado por eje
/// (Biología, Física, Química) y al final las preguntas del módulo elegido.
/// Nunca repite una pregunta. Si faltan preguntas de un eje, usa las que hay.
List<QuizItem> buildCienciasSimulacro(
  List<Question> pool,
  CienciasModulo modulo, {
  required Random random,
}) {
  final porEje = {
    for (final eje in cienciasEjes)
      eje: (pool.where((q) => q.eje == eje).toList()..shuffle(random)),
  };

  List<Question> tomar(String eje, int n) {
    final disponibles = porEje[eje]!;
    final elegidas = disponibles.take(n).toList();
    disponibles.removeRange(0, elegidas.length);
    return elegidas;
  }

  final comun = [for (final eje in cienciasEjes) ...tomar(eje, comunPorEje)];
  final List<Question> electivo;
  if (modulo.eje != null) {
    electivo = tomar(modulo.eje!, preguntasModulo);
  } else {
    electivo = [for (final e in tpPorEje.entries) ...tomar(e.key, e.value)]
      ..shuffle(random);
  }
  return [
    for (final q in [...comun, ...electivo]) QuizItem.shuffled(q, random),
  ];
}

import 'dart:math';

/// Calcula el "puntaje estimado" de 100 a 1000.
///
/// Imita la forma del puntaje PAES real, que se calcula a partir de la
/// "habilidad" de cada estudiante y no de forma lineal:
/// - 0 correctas = 100 puntos y todas correctas = 1000 (solo así se llega a 1000).
/// - Las primeras y las últimas respuestas correctas valen más puntos que las
///   del medio (curva logística).
/// - Las respuestas malas no restan.
///
/// Es una fórmula propia: NO usa las tablas de transformación del DEMRE, que
/// cambian cada año. Por eso siempre debe mostrarse como "puntaje estimado".
int estimateScore({required int correct, required int total}) {
  if (total <= 0) return 100;
  final c = correct.clamp(0, total);
  // Proporción suavizada (nunca 0 ni 1), para que la curva tenga extremos finitos.
  double logit(num aciertos) {
    final p = (aciertos + 0.5) / (total + 1);
    return log(p / (1 - p));
  }

  final min = logit(0);
  final max = logit(total);
  return (100 + 900 * (logit(c) - min) / (max - min)).round();
}

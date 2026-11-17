/// Calcula el "puntaje estimado" de 100 a 1000.
///
/// Es una fórmula propia y aproximada (lineal según el porcentaje de
/// aciertos). NO usa las tablas de conversión del DEMRE, por eso siempre
/// debe mostrarse como "puntaje estimado".
int estimateScore({required int correct, required int total}) {
  if (total <= 0) return 100;
  final ratio = correct / total;
  return (100 + 900 * ratio).round();
}

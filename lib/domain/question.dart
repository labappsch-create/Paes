import 'prueba.dart';

/// Una pregunta de alternativas.
class Question {
  const Question({
    required this.id,
    required this.prueba,
    required this.enunciado,
    required this.alternativas,
    required this.correcta,
    this.eje,
    this.explicacion = '',
    this.imagen,
  });

  final String id;
  final Prueba prueba;
  final String enunciado;
  final List<String> alternativas;

  /// Posición (desde 0) de la alternativa correcta en [alternativas].
  final int correcta;

  /// Eje temático, solo si el archivo lo trae.
  final String? eje;

  /// Explicación corta. Vacía si no hay.
  final String explicacion;

  /// Ruta de la imagen o gráfico de la pregunta (en `assets`). Null si no tiene.
  final String? imagen;

  factory Question.fromJson(Map<String, dynamic> json) {
    final alternativas = List<String>.from(json['alternativas'] as List);
    final correcta = json['correcta'] as int;
    if (correcta < 0 || correcta >= alternativas.length) {
      throw FormatException(
        'La pregunta ${json['id']} tiene una respuesta correcta fuera de rango.',
      );
    }
    return Question(
      id: json['id'] as String,
      prueba: Prueba.fromKey(json['prueba'] as String),
      enunciado: json['enunciado'] as String,
      alternativas: alternativas,
      correcta: correcta,
      eje: json['eje'] as String?,
      explicacion: (json['explicacion'] as String?) ?? '',
      imagen: json['imagen'] as String?,
    );
  }
}

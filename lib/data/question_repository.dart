import 'dart:convert';

import 'package:flutter/services.dart' show rootBundle;
import 'package:flutter/foundation.dart' show FlutterError;

import '../core/constants.dart';
import '../domain/prueba.dart';
import '../domain/question.dart';

/// Lee las preguntas desde los archivos JSON de la carpeta `assets/questions`
/// (uno por prueba). Si una prueba aún no tiene archivo, simplemente no
/// tiene preguntas todavía.
class QuestionRepository {
  Future<List<Question>> loadAll() async {
    final result = <Question>[];
    for (final prueba in Prueba.values) {
      final String raw;
      try {
        raw = await rootBundle.loadString('$questionsAssetDir/${prueba.key}.json');
      } on FlutterError {
        continue; // Esa prueba todavía no tiene preguntas.
      }
      final list = jsonDecode(raw) as List<dynamic>;
      for (final item in list) {
        result.add(Question.fromJson(item as Map<String, dynamic>));
      }
    }
    return result;
  }
}

import 'dart:convert';

import 'package:flutter/services.dart' show rootBundle;

import '../core/constants.dart';
import '../domain/question.dart';

/// Lee las preguntas desde el archivo JSON de la carpeta `assets`.
/// Para cambiar las preguntas basta con reemplazar ese archivo.
class QuestionRepository {
  Future<List<Question>> loadAll() async {
    final raw = await rootBundle.loadString(questionsAssetPath);
    final list = jsonDecode(raw) as List<dynamic>;
    return [
      for (final item in list) Question.fromJson(item as Map<String, dynamic>),
    ];
  }
}

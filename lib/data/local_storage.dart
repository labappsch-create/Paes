import 'dart:convert';

import 'package:shared_preferences/shared_preferences.dart';

import '../domain/exam_attempt.dart';

/// Guarda en el teléfono: preguntas respondidas, simulacro gratis, compra e historial.
class LocalStorage {
  LocalStorage(this._prefs);

  final SharedPreferences _prefs;

  static const _answeredKey = 'answered_count';
  static const _purchasedKey = 'full_access_purchased';
  static const _attemptsKey = 'attempts';
  static const _freeSimulacroKey = 'free_simulacro_used';

  int get answeredCount => _prefs.getInt(_answeredKey) ?? 0;
  Future<void> setAnsweredCount(int value) =>
      _prefs.setInt(_answeredKey, value);

  bool get isPurchased => _prefs.getBool(_purchasedKey) ?? false;
  Future<void> setPurchased(bool value) => _prefs.setBool(_purchasedKey, value);

  /// True si ya se usó el simulacro gratis.
  bool get freeSimulacroUsed => _prefs.getBool(_freeSimulacroKey) ?? false;
  Future<void> setFreeSimulacroUsed() =>
      _prefs.setBool(_freeSimulacroKey, true);

  List<ExamAttempt> get attempts {
    final raw = _prefs.getStringList(_attemptsKey) ?? const [];
    final result = <ExamAttempt>[];
    for (final item in raw) {
      try {
        result.add(
          ExamAttempt.fromJson(jsonDecode(item) as Map<String, dynamic>),
        );
      } catch (_) {
        // Si un registro está dañado, se ignora y se sigue con el resto.
      }
    }
    return result;
  }

  Future<void> addAttempt(ExamAttempt attempt) {
    final raw = _prefs.getStringList(_attemptsKey) ?? <String>[];
    return _prefs.setStringList(_attemptsKey, [
      ...raw,
      jsonEncode(attempt.toJson()),
    ]);
  }
}

import 'dart:convert';

import 'package:shared_preferences/shared_preferences.dart';

import '../domain/exam_attempt.dart';

/// Guarda en el teléfono: preguntas respondidas, simulacro gratis, compra e historial.
class LocalStorage {
  LocalStorage(this._prefs);

  final SharedPreferences _prefs;

  static const _answeredKey = 'answered_count';
  static const _expiresKey = 'access_expires_at';
  static const _seenPurchasesKey = 'seen_purchase_ids';
  static const _lastSeenKey = 'last_seen_time';
  static const _attemptsKey = 'attempts';
  static const _freeSimulacroKey = 'free_simulacro_used';

  int get answeredCount => _prefs.getInt(_answeredKey) ?? 0;
  Future<void> setAnsweredCount(int value) =>
      _prefs.setInt(_answeredKey, value);

  /// Fecha en que termina el acceso completo pagado. Null si nunca compró.
  DateTime? get accessExpiresAt {
    final ms = _prefs.getInt(_expiresKey);
    return ms == null ? null : DateTime.fromMillisecondsSinceEpoch(ms);
  }

  Future<void> setAccessExpiresAt(DateTime value) =>
      _prefs.setInt(_expiresKey, value.millisecondsSinceEpoch);

  /// Compras ya contadas, para no sumar dos veces los mismos 6 meses.
  Set<String> get seenPurchaseIds =>
      (_prefs.getStringList(_seenPurchasesKey) ?? const []).toSet();
  Future<void> addSeenPurchaseId(String id) => _prefs.setStringList(
    _seenPurchasesKey,
    {...seenPurchaseIds, id}.toList(),
  );

  /// La hora más tardía que ha visto la app. Sirve para que atrasar el reloj
  /// del celular no alargue el acceso.
  DateTime? get lastSeenTime {
    final ms = _prefs.getInt(_lastSeenKey);
    return ms == null ? null : DateTime.fromMillisecondsSinceEpoch(ms);
  }

  Future<void> setLastSeenTime(DateTime value) =>
      _prefs.setInt(_lastSeenKey, value.millisecondsSinceEpoch);

  /// True si ya se usó el simulacro gratis.
  bool get freeSimulacroUsed => _prefs.getBool(_freeSimulacroKey) ?? false;
  Future<void> setFreeSimulacroUsed() =>
      _prefs.setBool(_freeSimulacroKey, true);

  /// Preguntas ya vistas de una prueba (en el ciclo actual). Sirve para no
  /// repetir preguntas hasta haberlas visto todas.
  Set<String> seenQuestions(String prueba) =>
      (_prefs.getStringList('seen_$prueba') ?? const []).toSet();

  Future<void> markSeen(String prueba, String id) {
    final seen = seenQuestions(prueba);
    if (seen.contains(id)) return Future.value();
    return _prefs.setStringList('seen_$prueba', [...seen, id]);
  }

  /// Comienza un ciclo nuevo: todas las preguntas vuelven a contar como nuevas.
  Future<void> resetSeen(String prueba) => _prefs.remove('seen_$prueba');

  /// Preguntas que la persona respondió mal la última vez que las vio.
  Set<String> wrongQuestions(String prueba) =>
      (_prefs.getStringList('wrong_$prueba') ?? const []).toSet();

  /// Actualiza los errores: agrega las respondidas mal y quita las que ahora
  /// respondió bien.
  Future<void> updateWrong(
    String prueba, {
    required Iterable<String> wrong,
    required Iterable<String> right,
  }) {
    final set = wrongQuestions(prueba)
      ..addAll(wrong)
      ..removeAll(right);
    return _prefs.setStringList('wrong_$prueba', set.toList());
  }

  /// Tamaño de letra elegido en Ajustes (1.0 = normal).
  double get textScale => _prefs.getDouble('text_scale') ?? 1.0;
  Future<void> setTextScale(double v) => _prefs.setDouble('text_scale', v);

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

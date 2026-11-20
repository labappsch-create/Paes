import 'package:clock/clock.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../core/constants.dart';
import '../data/local_storage.dart';
import '../data/question_repository.dart';
import '../domain/access_period.dart';
import '../domain/exam_attempt.dart';
import '../domain/invitation_code.dart';
import '../domain/question.dart';

/// Se entrega real en `main.dart` antes de abrir la app.
final sharedPreferencesProvider = Provider<SharedPreferences>(
  (ref) => throw UnimplementedError('Falta inicializar SharedPreferences'),
);

final storageProvider = Provider<LocalStorage>(
  (ref) => LocalStorage(ref.watch(sharedPreferencesProvider)),
);

final questionRepositoryProvider = Provider<QuestionRepository>(
  (ref) => QuestionRepository(),
);

final questionsProvider = FutureProvider<List<Question>>(
  (ref) => ref.watch(questionRepositoryProvider).loadAll(),
);

/// Estado de acceso: cuántas preguntas gratis de Práctica se usaron, si ya se
/// usó el simulacro gratis y hasta cuándo dura el acceso completo pagado.
class AccessState {
  const AccessState({
    required this.answered,
    this.freeSimulacroUsed = false,
    this.expiresAt,
    this.notBefore,
  });

  final int answered;
  final bool freeSimulacroUsed;

  /// Fin del acceso completo pagado (6 meses). Null si nunca compró.
  final DateTime? expiresAt;

  /// La hora más tardía que vio la app: si el reloj del celular se atrasa,
  /// se usa esta, para que no se alargue el acceso.
  final DateTime? notBefore;

  DateTime get _now {
    final now = clock.now();
    final nb = notBefore;
    return nb != null && nb.isAfter(now) ? nb : now;
  }

  /// Tiene el acceso completo vigente en este momento.
  bool get purchased {
    final e = expiresAt;
    return e != null && _now.isBefore(e);
  }

  /// Pagó alguna vez, pero sus 6 meses ya terminaron.
  bool get expired => expiresAt != null && !purchased;

  bool get canAnswer => purchased || answered < freeQuestionLimit;
  int get freeLeft =>
      (freeQuestionLimit - answered).clamp(0, freeQuestionLimit);

  /// El próximo simulacro sería el gratis (no tiene acceso y aún no lo usa).
  bool get freeSimulacroAvailable => !purchased && !freeSimulacroUsed;

  bool get canStartSimulacro => purchased || !freeSimulacroUsed;

  AccessState copyWith({
    int? answered,
    bool? freeSimulacroUsed,
    DateTime? expiresAt,
  }) => AccessState(
    answered: answered ?? this.answered,
    freeSimulacroUsed: freeSimulacroUsed ?? this.freeSimulacroUsed,
    expiresAt: expiresAt ?? this.expiresAt,
    notBefore: notBefore,
  );
}

enum CodigoResultado { activado, yaVigente, invalido }

class AccessController extends Notifier<AccessState> {
  @override
  AccessState build() {
    final storage = ref.read(storageProvider);
    final now = clock.now();
    final last = storage.lastSeenTime;
    if (last == null || now.isAfter(last)) storage.setLastSeenTime(now);
    return AccessState(
      answered: storage.answeredCount,
      freeSimulacroUsed: storage.freeSimulacroUsed,
      expiresAt: storage.accessExpiresAt,
      notBefore: last,
    );
  }

  /// Suma una pregunta de Práctica al contador global (todas las pruebas).
  Future<void> registerAnswer() async {
    if (state.purchased) return;
    final next = state.answered + 1;
    state = state.copyWith(answered: next);
    await ref.read(storageProvider).setAnsweredCount(next);
  }

  /// Marca como usado el simulacro gratis. Se llama al comenzarlo, para que
  /// no se pueda repetir saliendo antes de terminar.
  Future<void> useFreeSimulacro() async {
    if (state.purchased || state.freeSimulacroUsed) return;
    state = state.copyWith(freeSimulacroUsed: true);
    await ref.read(storageProvider).setFreeSimulacroUsed();
  }

  /// Canjea un código de invitación: da 6 meses de acceso completo gratis,
  /// contados desde hoy. Si el acceso ya está vigente, no cambia nada (el
  /// código se puede volver a usar cuando termine).
  Future<CodigoResultado> redeemCode(String codigo) async {
    if (!esCodigoValido(codigo)) return CodigoResultado.invalido;
    if (state.purchased) return CodigoResultado.yaVigente;
    final now = clock.now();
    final nb = state.notBefore;
    final desde = nb != null && nb.isAfter(now) ? nb : now;
    final expiry = addMonths(desde, accessMonths);
    state = state.copyWith(expiresAt: expiry);
    await ref.read(storageProvider).setAccessExpiresAt(expiry);
    return CodigoResultado.activado;
  }

  /// Registra una compra de 6 meses. [purchaseId] evita contar dos veces la
  /// misma compra; [isNewPurchase] es false cuando la compra se restaura.
  Future<void> grantAccess({
    required String purchaseId,
    required DateTime purchaseDate,
    required bool isNewPurchase,
  }) async {
    final storage = ref.read(storageProvider);
    if (storage.seenPurchaseIds.contains(purchaseId)) return;
    final expiry = computeExpiry(
      purchaseDate: purchaseDate,
      isNewPurchase: isNewPurchase,
      currentExpiry: state.expiresAt,
    );
    state = state.copyWith(expiresAt: expiry);
    await storage.setAccessExpiresAt(expiry);
    await storage.addSeenPurchaseId(purchaseId);
  }
}

final accessProvider = NotifierProvider<AccessController, AccessState>(
  AccessController.new,
);

/// Historial de ensayos.
class AttemptsController extends Notifier<List<ExamAttempt>> {
  @override
  List<ExamAttempt> build() => ref.read(storageProvider).attempts;

  Future<void> add(ExamAttempt attempt) async {
    state = [...state, attempt];
    await ref.read(storageProvider).addAttempt(attempt);
  }
}

final attemptsProvider =
    NotifierProvider<AttemptsController, List<ExamAttempt>>(
      AttemptsController.new,
    );

/// Tamaño de letra elegido por la persona (1.0 = normal).
class TextScaleController extends Notifier<double> {
  @override
  double build() => ref.read(storageProvider).textScale;

  Future<void> set(double value) async {
    state = value;
    await ref.read(storageProvider).setTextScale(value);
  }
}

final textScaleProvider = NotifierProvider<TextScaleController, double>(
  TextScaleController.new,
);

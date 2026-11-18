import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../core/constants.dart';
import '../data/local_storage.dart';
import '../data/question_repository.dart';
import '../domain/exam_attempt.dart';
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

/// Estado de acceso: cuántas preguntas gratis se usaron y si ya compró.
class AccessState {
  const AccessState({required this.purchased, required this.answered});

  final bool purchased;
  final int answered;

  bool get canAnswer => purchased || answered < freeQuestionLimit;
  int get freeLeft =>
      (freeQuestionLimit - answered).clamp(0, freeQuestionLimit);
}

class AccessController extends Notifier<AccessState> {
  @override
  AccessState build() {
    final storage = ref.read(storageProvider);
    return AccessState(
      purchased: storage.isPurchased,
      answered: storage.answeredCount,
    );
  }

  /// Suma una pregunta respondida al contador global (todas las pruebas).
  Future<void> registerAnswer() async {
    if (state.purchased) return;
    final next = state.answered + 1;
    state = AccessState(purchased: false, answered: next);
    await ref.read(storageProvider).setAnsweredCount(next);
  }

  Future<void> markPurchased() async {
    state = AccessState(purchased: true, answered: state.answered);
    await ref.read(storageProvider).setPurchased(true);
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

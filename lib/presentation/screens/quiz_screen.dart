import 'dart:async';

import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:material_ui/material_ui.dart';

import '../../domain/exam_attempt.dart';
import '../../domain/prueba.dart';
import '../../domain/quiz_item.dart';
import '../../domain/score_calculator.dart';
import '../providers.dart';
import '../widgets/question_image.dart';
import 'explanation_screen.dart';
import 'paywall_screen.dart';
import 'results_screen.dart';

/// Pantalla de preguntas, para Práctica y Simulacro.
///
/// - Práctica: sin reloj, muestra al instante si la respuesta fue correcta.
/// - Simulacro: con el tiempo oficial, sin mostrar respuestas hasta el final.
class QuizScreen extends ConsumerStatefulWidget {
  const QuizScreen({
    super.key,
    required this.prueba,
    required this.mode,
    required this.items,
  });

  final Prueba prueba;
  final QuizMode mode;
  final List<QuizItem> items;

  @override
  ConsumerState<QuizScreen> createState() => _QuizScreenState();
}

class _QuizScreenState extends ConsumerState<QuizScreen> {
  int _index = 0;
  final ScrollController _scroll = ScrollController();
  Timer? _timer;
  late Duration _remaining;
  bool _finished = false;

  bool get _isPractice => widget.mode == QuizMode.practice;
  QuizItem get _item => widget.items[_index];

  @override
  void initState() {
    super.initState();
    _remaining = Duration(minutes: widget.prueba.minutes);
    if (!_isPractice) {
      _timer = Timer.periodic(const Duration(seconds: 1), (_) {
        if (!mounted) return;
        setState(() => _remaining -= const Duration(seconds: 1));
        if (_remaining <= Duration.zero) _finish();
      });
    }
    WidgetsBinding.instance.addPostFrameCallback((_) => _checkAccessAtStart());
  }

  @override
  void dispose() {
    _timer?.cancel();
    _scroll.dispose();
    super.dispose();
  }

  /// Si ya se usaron las preguntas gratis, se pide el pago antes de empezar.
  Future<void> _checkAccessAtStart() async {
    if (ref.read(accessProvider).canAnswer) return;
    final ok = await _ensureAccess();
    if (!mounted) return;
    if (!ok) {
      _timer?.cancel();
      Navigator.of(context).pop();
    }
  }

  /// Devuelve true si la persona puede seguir respondiendo
  /// (tiene preguntas gratis o pagó).
  Future<bool> _ensureAccess() async {
    if (ref.read(accessProvider).canAnswer) return true;
    final bought = await Navigator.of(context).push<bool>(
      MaterialPageRoute<bool>(
        builder: (_) => const PaywallScreen(),
        fullscreenDialog: true,
      ),
    );
    return bought == true || ref.read(accessProvider).canAnswer;
  }

  void _select(int displayIndex) {
    if (_finished) return;
    final item = _item;
    if (_isPractice && item.isAnswered) return;
    final isFirstAnswer = !item.isAnswered;
    setState(() => item.selected = displayIndex);
    if (isFirstAnswer) {
      ref.read(accessProvider.notifier).registerAnswer();
    }
    if (_isPractice) _scrollToFeedback();
  }

  /// Baja la pantalla para que se vea si la respuesta fue correcta.
  void _scrollToFeedback() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (!_scroll.hasClients) return;
      _scroll.animateTo(
        _scroll.position.maxScrollExtent,
        duration: const Duration(milliseconds: 250),
        curve: Curves.easeOut,
      );
    });
  }

  Future<void> _next() async {
    if (_index >= widget.items.length - 1) {
      _finish();
      return;
    }
    final nextItem = widget.items[_index + 1];
    if (!nextItem.isAnswered && !ref.read(accessProvider).canAnswer) {
      final ok = await _ensureAccess();
      if (!mounted) return;
      if (!ok) {
        // No pagó: se termina el ensayo con lo respondido hasta ahora.
        _finish();
        return;
      }
    }
    setState(() => _index++);
    if (_scroll.hasClients) _scroll.jumpTo(0);
  }

  void _finish() {
    if (_finished || !mounted) return;
    _finished = true;
    _timer?.cancel();

    final answered = widget.items.where((i) => i.isAnswered).toList();
    if (answered.isEmpty) {
      Navigator.of(context).pop();
      return;
    }
    // En práctica se corrige solo lo respondido.
    // En simulacro, lo que quedó en blanco cuenta como no acertado.
    final scored = _isPractice ? answered : widget.items;
    final correct = scored.where((i) => i.isCorrect).length;
    final attempt = ExamAttempt(
      date: DateTime.now(),
      prueba: widget.prueba,
      mode: widget.mode,
      total: scored.length,
      correct: correct,
      score: estimateScore(correct: correct, total: scored.length),
    );
    ref.read(attemptsProvider.notifier).add(attempt);
    Navigator.of(context).pushReplacement(
      MaterialPageRoute<void>(
        builder: (_) => ResultsScreen(attempt: attempt, items: scored),
      ),
    );
  }

  Future<void> _confirmExit() async {
    final leave = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('¿Salir del ensayo?'),
        content: const Text('Perderás el avance de este ensayo.'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(false),
            child: const Text('Seguir'),
          ),
          TextButton(
            onPressed: () => Navigator.of(context).pop(true),
            child: const Text('Salir'),
          ),
        ],
      ),
    );
    if (leave == true && mounted) {
      _timer?.cancel();
      Navigator.of(context).pop();
    }
  }

  String _formatRemaining() {
    final d = _remaining.isNegative ? Duration.zero : _remaining;
    String two(int n) => n.toString().padLeft(2, '0');
    return '${d.inHours}:${two(d.inMinutes % 60)}:${two(d.inSeconds % 60)}';
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final item = _item;
    final total = widget.items.length;
    final isLast = _index == total - 1;
    final showFeedback = _isPractice && item.isAnswered;

    return PopScope(
      canPop: false,
      onPopInvokedWithResult: (didPop, _) {
        if (!didPop) _confirmExit();
      },
      child: Scaffold(
        appBar: AppBar(
          title: Text('Pregunta ${_index + 1} de $total'),
          actions: [
            if (!_isPractice)
              Padding(
                padding: const EdgeInsets.only(right: 16),
                child: Center(
                  child: Text(
                    _formatRemaining(),
                    style: theme.textTheme.titleMedium,
                  ),
                ),
              ),
          ],
          bottom: PreferredSize(
            preferredSize: const Size.fromHeight(4),
            child: LinearProgressIndicator(value: (_index + 1) / total),
          ),
        ),
        body: SafeArea(
          child: Column(
            children: [
              Expanded(
                child: ListView(
                  controller: _scroll,
                  padding: const EdgeInsets.all(16),
                  children: [
                    Text(
                      widget.prueba.label,
                      style: theme.textTheme.labelLarge,
                    ),
                    const SizedBox(height: 8),
                    Text(
                      item.question.enunciado,
                      style: theme.textTheme.titleMedium,
                    ),
                    QuestionImage(path: item.question.imagen),
                    const SizedBox(height: 4),
                    for (var i = 0; i < item.options.length; i++)
                      _OptionTile(
                        letter: String.fromCharCode(65 + i),
                        text: item.options[i],
                        state: _optionState(item, i),
                        onTap: () => _select(i),
                      ),
                    if (showFeedback) ...[
                      const SizedBox(height: 8),
                      Text(
                        item.isCorrect ? '¡Correcto!' : 'Incorrecto',
                        style: theme.textTheme.titleMedium?.copyWith(
                          color: item.isCorrect
                              ? Colors.green
                              : theme.colorScheme.error,
                        ),
                      ),
                      if (item.question.explicacion.isNotEmpty)
                        Padding(
                          padding: const EdgeInsets.only(top: 4),
                          child: Text(item.question.explicacion),
                        ),
                      Align(
                        alignment: Alignment.centerLeft,
                        child: TextButton.icon(
                          icon: const Icon(Icons.travel_explore),
                          label: const Text('Ver explicación'),
                          onPressed: () => Navigator.of(context).push(
                            MaterialPageRoute<void>(
                              builder: (_) => ExplanationScreen(
                                enunciado: item.question.enunciado,
                              ),
                            ),
                          ),
                        ),
                      ),
                    ],
                  ],
                ),
              ),
              Padding(
                padding: const EdgeInsets.all(16),
                child: SizedBox(
                  width: double.infinity,
                  child: FilledButton(
                    // En práctica, primero hay que responder.
                    onPressed: (_isPractice && !item.isAnswered) ? null : _next,
                    child: Text(isLast ? 'Terminar' : 'Siguiente'),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  _OptionState _optionState(QuizItem item, int i) {
    if (_isPractice && item.isAnswered) {
      if (i == item.correctDisplayIndex) return _OptionState.correct;
      if (i == item.selected) return _OptionState.wrong;
      return _OptionState.normal;
    }
    return item.selected == i ? _OptionState.selected : _OptionState.normal;
  }
}

enum _OptionState { normal, selected, correct, wrong }

class _OptionTile extends StatelessWidget {
  const _OptionTile({
    required this.letter,
    required this.text,
    required this.state,
    required this.onTap,
  });

  final String letter;
  final String text;
  final _OptionState state;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    final Color? background = switch (state) {
      _OptionState.normal => null,
      _OptionState.selected => scheme.primaryContainer,
      _OptionState.correct => Colors.green.withValues(alpha: 0.25),
      _OptionState.wrong => scheme.errorContainer,
    };
    return Card(
      color: background,
      child: ListTile(
        leading: CircleAvatar(child: Text(letter)),
        title: Text(text),
        onTap: onTap,
      ),
    );
  }
}

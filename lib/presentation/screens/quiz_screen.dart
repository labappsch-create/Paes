import 'dart:async';

import 'package:clock/clock.dart';

import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:material_ui/material_ui.dart';

import '../../domain/exam_attempt.dart';
import '../../domain/prueba.dart';
import '../../domain/quiz_item.dart';
import '../../domain/score_calculator.dart';
import '../providers.dart';
import '../prueba_style.dart';
import '../widgets/question_image.dart';
import '../widgets/reading_text.dart';
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
    this.modulo,
    this.comunCount,
  });

  final Prueba prueba;
  final QuizMode mode;
  final List<QuizItem> items;

  /// Módulo elegido en Ciencias (por ejemplo «Física»). Null en las demás pruebas.
  final String? modulo;

  /// En el simulacro de Ciencias, cuántas preguntas iniciales son del Módulo
  /// Común. Las siguientes son del módulo elegido.
  final int? comunCount;

  @override
  ConsumerState<QuizScreen> createState() => _QuizScreenState();
}

class _QuizScreenState extends ConsumerState<QuizScreen> {
  int _index = 0;
  final ScrollController _scroll = ScrollController();
  Timer? _timer;
  late Duration _remaining;

  /// Hora real en que se acaba el simulacro.
  late DateTime _endAt;
  bool _finished = false;

  bool get _isPractice => widget.mode == QuizMode.practice;
  QuizItem get _item => widget.items[_index];

  @override
  void initState() {
    super.initState();
    _remaining = Duration(minutes: widget.prueba.minutes);
    if (!_isPractice) {
      // Se guarda la hora real de término. Así el reloj sigue corriendo aunque
      // la persona salga de la app, como en la prueba real.
      _endAt = clock.now().add(_remaining);
      _timer = Timer.periodic(const Duration(seconds: 1), (_) {
        if (!mounted) return;
        setState(() => _remaining = _endAt.difference(clock.now()));
        if (_remaining <= Duration.zero) {
          _finish();
        } else {
          _checkTimeWarning();
        }
      });
    }
    WidgetsBinding.instance.addPostFrameCallback((_) => _checkAccessAtStart());
  }

  /// Minutos restantes en que se avisa, como lo hace el examinador en la prueba.
  static const _warningMinutes = [30, 10, 5];

  /// Avisos ya mostrados en este ensayo (cada uno se muestra una sola vez).
  final Set<int> _warned = {};

  /// Desde cuántos minutos restantes el reloj se pone rojo.
  static const _redClockMinutes = 5;

  void _checkTimeWarning() {
    // Si la persona estuvo fuera de la app, pudieron pasar varios avisos a la
    // vez: se marcan todos y se muestra solo el más reciente (el de menos minutos).
    int? show;
    for (final m in _warningMinutes) {
      if (_warned.contains(m) || _remaining > Duration(minutes: m)) continue;
      _warned.add(m);
      if (m < widget.prueba.minutes) show = m;
    }
    if (show == null) return;
    final messenger = ScaffoldMessenger.of(context);
    messenger
      ..hideCurrentSnackBar()
      ..showSnackBar(
        SnackBar(
          behavior: SnackBarBehavior.floating,
          duration: const Duration(seconds: 6),
          content: Row(
            children: [
              const Icon(Icons.timer_outlined, color: Colors.white),
              const SizedBox(width: 12),
              Expanded(child: Text('Quedan $show minutos.')),
            ],
          ),
          action: SnackBarAction(
            label: 'OK',
            onPressed: messenger.hideCurrentSnackBar,
          ),
        ),
      );
  }

  @override
  void dispose() {
    _timer?.cancel();
    _scroll.dispose();
    super.dispose();
  }

  /// Si ya se usaron las preguntas gratis, se pide el pago antes de empezar.
  Future<void> _checkAccessAtStart() async {
    // El simulacro se autoriza al comenzarlo (compra o simulacro gratis).
    if (!_isPractice) return;
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

  Future<void> _select(int displayIndex) async {
    if (_finished) return;
    final item = _item;
    if (_isPractice && item.isAnswered) return;
    final isFirstAnswer = !item.isAnswered;
    if (isFirstAnswer && !await _accessOrFinish()) return;
    if (!mounted || _finished) return;
    setState(() => item.selected = displayIndex);
    // Solo la Práctica descuenta de las preguntas gratis.
    if (isFirstAnswer && _isPractice) {
      ref.read(accessProvider.notifier).registerAnswer();
    }
    if (_isPractice) _scrollToFeedback();
  }

  /// Revisa si se pueden responder más preguntas. Si se acabaron las gratis,
  /// muestra la pantalla de pago; si no paga, se termina el ensayo con lo
  /// respondido hasta ahora y devuelve false.
  Future<bool> _accessOrFinish() async {
    // En el simulacro no hay límite de preguntas: ya se autorizó al comenzar.
    if (!_isPractice) return true;
    if (ref.read(accessProvider).canAnswer) return true;
    final ok = await _ensureAccess();
    if (!mounted) return false;
    if (!ok) _finish();
    return ok;
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
      // En el simulacro, antes de terminar se muestra el resumen para entregar.
      _isPractice ? _finish() : await _confirmSubmit();
      return;
    }
    await _goTo(_index + 1);
  }

  /// Va a la pregunta [target]. En el simulacro se puede ir a cualquiera,
  /// adelante o atrás, como con el cuadernillo en papel.
  Future<void> _goTo(int target) async {
    if (target < 0 || target >= widget.items.length || target == _index) return;
    // Para ver una pregunta nueva sin responder hay que tener acceso.
    if (!widget.items[target].isAnswered && !await _accessOrFinish()) return;
    if (!mounted || _finished) return;
    setState(() => _index = target);
    if (_scroll.hasClients) _scroll.jumpTo(0);
  }

  /// Muestra todas las preguntas numeradas para saltar a cualquiera.
  Future<void> _openMap() async {
    final target = await showModalBottomSheet<int>(
      context: context,
      showDragHandle: true,
      isScrollControlled: true,
      builder: (context) => _QuestionMap(items: widget.items, current: _index),
    );
    if (target == _submit) {
      await _confirmSubmit();
    } else if (target != null) {
      await _goTo(target);
    }
  }

  /// Resumen antes de entregar: cuántas quedan sin responder y cuáles.
  /// Desde ahí se puede ir a una pregunta, seguir revisando o entregar.
  Future<void> _confirmSubmit() async {
    final target = await showModalBottomSheet<int>(
      context: context,
      showDragHandle: true,
      isScrollControlled: true,
      builder: (context) =>
          _SubmitReview(items: widget.items, remaining: _formatRemaining()),
    );
    if (!mounted || _finished) return;
    if (target == _submit) {
      _finish();
    } else if (target != null) {
      await _goTo(target);
    }
  }

  void _finish() {
    if (_finished || !mounted) return;
    _finished = true;
    _timer?.cancel();

    final answered = widget.items.where((i) => i.isAnswered).toList();
    // En práctica sin respuestas no hay nada que corregir. En el simulacro
    // siempre se muestran resultados (lo no respondido cuenta como error).
    if (_isPractice && answered.isEmpty) {
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
      modulo: widget.modulo,
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
    final ms = _remaining.isNegative ? 0 : _remaining.inMilliseconds;
    // Se redondea hacia arriba: al empezar se ve «2:20:00» y no «2:19:59».
    final d = Duration(seconds: (ms + 999) ~/ 1000);
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

    final ejeColor = widget.prueba == Prueba.ciencias
        ? cienciasEjeColor(item.question.eje)
        : null;
    final redClock = _remaining <= const Duration(minutes: _redClockMinutes);

    return PopScope(
      canPop: false,
      onPopInvokedWithResult: (didPop, _) {
        if (!didPop) _confirmExit();
      },
      // La barra de arriba toma el color de la prueba.
      child: Theme(
        data: pruebaTheme(theme, widget.prueba.color),
        child: Scaffold(
          appBar: AppBar(
            title: Text('Pregunta ${_index + 1} de $total'),
            actions: [
              if (!_isPractice)
                Padding(
                  padding: const EdgeInsets.only(right: 16),
                  child: Center(
                    // En los últimos minutos el reloj va en rojo sobre fondo blanco,
                    // para que se note sobre cualquier color de barra.
                    child: Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 8,
                        vertical: 2,
                      ),
                      decoration: redClock
                          ? BoxDecoration(
                              color: Colors.white,
                              borderRadius: BorderRadius.circular(6),
                            )
                          : null,
                      child: Text(
                        _formatRemaining(),
                        semanticsLabel: 'Tiempo restante ${_formatRemaining()}',
                        style: theme.textTheme.titleMedium?.copyWith(
                          color: redClock
                              ? theme.colorScheme.error
                              : Colors.white,
                          fontWeight: redClock ? FontWeight.bold : null,
                        ),
                      ),
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
                      Row(
                        children: [
                          // Punto con el color de la prueba (o del eje, en Ciencias).
                          Container(
                            width: 10,
                            height: 10,
                            decoration: BoxDecoration(
                              color: ejeColor ?? widget.prueba.color,
                              shape: BoxShape.circle,
                            ),
                          ),
                          const SizedBox(width: 8),
                          Expanded(
                            child: Text(
                              _sectionLabel(),
                              style: theme.textTheme.labelLarge,
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 8),
                      ReadingText(
                        key: ValueKey(item.question.id),
                        text: item.question.texto,
                      ),
                      if (item.question.isSuficiencia) const _SuficienciaHelp(),
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
                                ? AppColors.correcto
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
                  child: _isPractice
                      ? SizedBox(
                          width: double.infinity,
                          child: FilledButton(
                            // En práctica, primero hay que responder.
                            onPressed: item.isAnswered ? _next : null,
                            child: Text(isLast ? 'Terminar' : 'Siguiente'),
                          ),
                        )
                      : Row(
                          children: [
                            Expanded(
                              child: OutlinedButton(
                                onPressed: _index == 0
                                    ? null
                                    : () => _goTo(_index - 1),
                                child: const Text('Anterior'),
                              ),
                            ),
                            const SizedBox(width: 8),
                            IconButton.outlined(
                              tooltip: 'Ver todas las preguntas',
                              icon: const Icon(Icons.grid_view),
                              onPressed: _openMap,
                            ),
                            const SizedBox(width: 8),
                            Expanded(
                              child: FilledButton(
                                onPressed: _next,
                                child: Text(isLast ? 'Entregar' : 'Siguiente'),
                              ),
                            ),
                          ],
                        ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  /// Texto sobre la pregunta: prueba, y en Ciencias la parte de la prueba y el eje.
  String _sectionLabel() {
    final texto = _item.question.texto;
    if (texto != null && texto.isNotEmpty) return _textoLabel(texto);
    final comun = widget.comunCount;
    if (comun == null) return widget.prueba.label;
    final parte = _index < comun ? 'Módulo Común' : 'Módulo ${widget.modulo}';
    final eje = _item.question.eje;
    return eje == null
        ? '${widget.prueba.label} · $parte'
        : '${widget.prueba.label} · $parte · $eje';
  }

  /// En Lectora: «Texto 2 · Preguntas 9 a 16», como en el cuadernillo real.
  String _textoLabel(String texto) {
    final items = widget.items;
    var inicio = _index;
    while (inicio > 0 && items[inicio - 1].question.texto == texto) {
      inicio--;
    }
    var fin = _index;
    while (fin < items.length - 1 && items[fin + 1].question.texto == texto) {
      fin++;
    }
    // Número del texto: cuántos textos empiezan en esta posición o antes.
    var numero = 0;
    for (var i = 0; i <= inicio; i++) {
      final t = items[i].question.texto;
      final empieza =
          t != null &&
          t.isNotEmpty &&
          (i == 0 || items[i - 1].question.texto != t);
      if (empieza) numero++;
    }
    final preguntas = inicio == fin
        ? 'Pregunta ${inicio + 1}'
        : 'Preguntas ${inicio + 1} a ${fin + 1}';
    return '${widget.prueba.label} · Texto $numero · $preguntas';
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
      _OptionState.correct => AppColors.correcto.withValues(alpha: 0.18),
      _OptionState.wrong => scheme.errorContainer,
    };
    // ✓ y ✗ además del color, para que se entienda sin distinguir colores.
    final Widget? mark = switch (state) {
      _OptionState.correct => const Icon(
        Icons.check_circle,
        color: AppColors.correcto,
        semanticLabel: 'Correcta',
      ),
      _OptionState.wrong => Icon(
        Icons.cancel,
        color: scheme.error,
        semanticLabel: 'Incorrecta',
      ),
      _ => null,
    };
    return Card(
      color: background,
      child: ListTile(
        leading: CircleAvatar(child: Text(letter)),
        title: Text(text),
        trailing: mark,
        onTap: onTap,
      ),
    );
  }
}

/// Valor que devuelven el mapa y el resumen cuando la persona elige entregar.
const _submit = -1;

/// Mapa del simulacro: todas las preguntas numeradas. Las respondidas se ven
/// pintadas y la actual tiene borde. Al tocar un número se va a esa pregunta.
class _QuestionMap extends StatelessWidget {
  const _QuestionMap({required this.items, required this.current});

  final List<QuizItem> items;
  final int current;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final scheme = theme.colorScheme;
    final answered = items.where((i) => i.isAnswered).length;
    return SafeArea(
      child: ConstrainedBox(
        constraints: BoxConstraints(
          maxHeight: MediaQuery.sizeOf(context).height * 0.75,
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Flexible(
              child: SingleChildScrollView(
                padding: const EdgeInsets.fromLTRB(16, 0, 16, 8),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Todas las preguntas',
                      style: theme.textTheme.titleLarge,
                    ),
                    const SizedBox(height: 4),
                    Text(
                      'Respondidas: $answered de ${items.length}. '
                      'Sin responder: ${items.length - answered}.',
                    ),
                    const SizedBox(height: 12),
                    Wrap(
                      spacing: 8,
                      runSpacing: 8,
                      children: [
                        for (var i = 0; i < items.length; i++)
                          SizedBox(
                            width: 48,
                            height: 48,
                            child: Material(
                              color: items[i].isAnswered
                                  ? scheme.primary
                                  : scheme.surfaceContainerHighest,
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(8),
                                side: i == current
                                    ? BorderSide(
                                        color: scheme.tertiary,
                                        width: 3,
                                      )
                                    : BorderSide.none,
                              ),
                              child: InkWell(
                                borderRadius: BorderRadius.circular(8),
                                onTap: () => Navigator.of(context).pop(i),
                                child: Center(
                                  child: Text(
                                    '${i + 1}',
                                    semanticsLabel:
                                        'Pregunta ${i + 1}, '
                                        '${items[i].isAnswered ? 'respondida' : 'sin responder'}',
                                    style: TextStyle(
                                      color: items[i].isAnswered
                                          ? scheme.onPrimary
                                          : scheme.onSurface,
                                      fontWeight: FontWeight.bold,
                                    ),
                                  ),
                                ),
                              ),
                            ),
                          ),
                      ],
                    ),
                    const SizedBox(height: 12),
                    Wrap(
                      spacing: 16,
                      runSpacing: 8,
                      children: [
                        _Legend(color: scheme.primary, text: 'Respondida'),
                        _Legend(
                          color: scheme.surfaceContainerHighest,
                          text: 'Sin responder',
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
            // Botones fijos abajo: siempre visibles aunque la lista sea larga.
            Padding(
              padding: const EdgeInsets.fromLTRB(16, 8, 16, 16),
              child: Column(
                children: [
                  SizedBox(
                    width: double.infinity,
                    child: OutlinedButton.icon(
                      icon: const Icon(Icons.assignment_turned_in_outlined),
                      label: const Text('Entregar ensayo'),
                      onPressed: () => Navigator.of(context).pop(_submit),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _Legend extends StatelessWidget {
  const _Legend({required this.color, required this.text});

  final Color color;
  final String text;

  @override
  Widget build(BuildContext context) => Row(
    mainAxisSize: MainAxisSize.min,
    children: [
      Container(
        width: 16,
        height: 16,
        decoration: BoxDecoration(
          color: color,
          borderRadius: BorderRadius.circular(4),
        ),
      ),
      const SizedBox(width: 6),
      Text(text),
    ],
  );
}

/// Resumen antes de entregar el simulacro.
class _SubmitReview extends StatelessWidget {
  const _SubmitReview({required this.items, required this.remaining});

  final List<QuizItem> items;
  final String remaining;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final scheme = theme.colorScheme;
    final blank = [
      for (var i = 0; i < items.length; i++)
        if (!items[i].isAnswered) i,
    ];
    final answered = items.length - blank.length;
    return SafeArea(
      child: ConstrainedBox(
        constraints: BoxConstraints(
          maxHeight: MediaQuery.sizeOf(context).height * 0.8,
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Flexible(
              child: SingleChildScrollView(
                padding: const EdgeInsets.fromLTRB(16, 0, 16, 8),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      '¿Entregar el ensayo?',
                      style: theme.textTheme.titleLarge,
                    ),
                    const SizedBox(height: 8),
                    Text('Respondiste $answered de ${items.length} preguntas.'),
                    Text('Tiempo restante: $remaining.'),
                    const SizedBox(height: 12),
                    if (blank.isEmpty)
                      const Text('No te quedan preguntas sin responder.')
                    else ...[
                      Text(
                        blank.length == 1
                            ? 'Te queda 1 pregunta sin responder. '
                                  'Si entregas, contará como incorrecta. '
                                  'Tócala para ir a ella:'
                            : 'Te quedan ${blank.length} preguntas sin responder. '
                                  'Si entregas, contarán como incorrectas. '
                                  'Toca una para ir a ella:',
                        style: TextStyle(color: scheme.error),
                      ),
                      const SizedBox(height: 8),
                      Wrap(
                        spacing: 8,
                        runSpacing: 8,
                        children: [
                          for (final i in blank)
                            ActionChip(
                              label: Text('${i + 1}'),
                              tooltip: 'Ir a la pregunta ${i + 1}',
                              onPressed: () => Navigator.of(context).pop(i),
                            ),
                        ],
                      ),
                    ],
                  ],
                ),
              ),
            ),
            // Botones fijos abajo: siempre visibles aunque la lista sea larga.
            Padding(
              padding: const EdgeInsets.fromLTRB(16, 8, 16, 16),
              child: Column(
                children: [
                  SizedBox(
                    width: double.infinity,
                    child: FilledButton(
                      onPressed: () => Navigator.of(context).pop(_submit),
                      child: const Text('Entregar'),
                    ),
                  ),
                  const SizedBox(height: 8),
                  SizedBox(
                    width: double.infinity,
                    child: OutlinedButton(
                      onPressed: () => Navigator.of(context).pop(),
                      child: const Text('Seguir revisando'),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

/// Recordatorio de cómo responder una pregunta de suficiencia de datos.
class _SuficienciaHelp extends StatelessWidget {
  const _SuficienciaHelp();

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Card(
      color: theme.colorScheme.tertiaryContainer,
      margin: const EdgeInsets.only(bottom: 12),
      child: Theme(
        data: theme.copyWith(dividerColor: Colors.transparent),
        child: ExpansionTile(
          leading: const Icon(Icons.help_outline),
          title: const Text('Suficiencia de datos'),
          subtitle: const Text('No hay que calcular el resultado.'),
          childrenPadding: const EdgeInsets.fromLTRB(16, 0, 16, 16),
          expandedCrossAxisAlignment: CrossAxisAlignment.start,
          children: const [
            Text(
              'Decide si la información (1) y (2) alcanza para responder la '
              'pregunta. Marca:\n'
              'A) si basta (1) y (2) no;\n'
              'B) si basta (2) y (1) no;\n'
              'C) si se necesitan las dos juntas;\n'
              'D) si cada una basta por separado;\n'
              'E) si ni juntas alcanzan.',
            ),
          ],
        ),
      ),
    );
  }
}

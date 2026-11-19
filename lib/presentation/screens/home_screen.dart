import 'dart:math';

import 'package:clock/clock.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:material_ui/material_ui.dart';

import '../../core/constants.dart';
import '../../domain/access_period.dart';
import '../../domain/ciencias_modulo.dart';
import '../../domain/exam_attempt.dart';
import '../../domain/lectora_session.dart';
import '../../domain/prueba.dart';
import '../../domain/question.dart';
import '../../domain/quiz_item.dart';
import '../providers.dart';
import '../prueba_style.dart';
import 'history_screen.dart';
import 'paywall_screen.dart';
import 'quiz_screen.dart';
import 'settings_screen.dart';

/// Pantalla de inicio: elegir prueba y modo.
class HomeScreen extends ConsumerWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final questions = ref.watch(questionsProvider);
    final access = ref.watch(accessProvider);

    // Mientras cargan las preguntas: bienvenida a pantalla completa, en blanco
    // como la pantalla de inicio del teléfono, con el logo de la app.
    if (questions.isLoading && !questions.hasValue) {
      return const Scaffold(
        backgroundColor: Colors.white,
        body: _WelcomeView(),
      );
    }

    return Scaffold(
      appBar: AppBar(
        title: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Image.asset(iconAsset, height: 32, semanticLabel: 'Logo'),
            const SizedBox(width: 10),
            const Text(appName),
          ],
        ),
        actions: [
          IconButton(
            tooltip: 'Ajustes',
            icon: const Icon(Icons.settings_outlined),
            onPressed: () => Navigator.of(context).push(
              MaterialPageRoute<void>(builder: (_) => const SettingsScreen()),
            ),
          ),
          IconButton(
            tooltip: 'Historial',
            icon: const Icon(Icons.history),
            onPressed: () => Navigator.of(context).push(
              MaterialPageRoute<void>(builder: (_) => const HistoryScreen()),
            ),
          ),
        ],
      ),
      body: questions.when(
        loading: () => const _WelcomeView(),
        error: (error, _) => Center(
          child: Padding(
            padding: const EdgeInsets.all(24),
            child: Text(
              'No se pudieron cargar las preguntas.\n$error',
              textAlign: TextAlign.center,
            ),
          ),
        ),
        data: (all) => ListView(
          padding: const EdgeInsets.all(16),
          children: [
            const _Countdown(),
            _AccessBanner(access: access),
            const SizedBox(height: 8),
            for (final prueba in Prueba.values)
              _PruebaCard(
                prueba: prueba,
                pool: all.where((q) => q.prueba == prueba).toList(),
              ),
          ],
        ),
      ),
    );
  }
}

/// Bienvenida mientras se cargan las preguntas: logo completo de la app.
class _WelcomeView extends StatelessWidget {
  const _WelcomeView();

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Image.asset(logoAsset, width: 240, semanticLabel: appName),
            const SizedBox(height: 32),
            const CircularProgressIndicator(),
            const SizedBox(height: 12),
            const Text('Cargando preguntas…'),
          ],
        ),
      ),
    );
  }
}

/// Cuenta regresiva para la próxima PAES (fechas en core/constants.dart).
class _Countdown extends StatelessWidget {
  const _Countdown();

  static const _meses = [
    'enero',
    'febrero',
    'marzo',
    'abril',
    'mayo',
    'junio',
    'julio',
    'agosto',
    'septiembre',
    'octubre',
    'noviembre',
    'diciembre',
  ];

  @override
  Widget build(BuildContext context) {
    final now = clock.now();
    final hoy = DateTime(now.year, now.month, now.day);
    final proxima = paesDates
        .where((p) => !p.$3.isBefore(hoy))
        .fold<(String, DateTime, DateTime)?>(
          null,
          (a, p) => a == null || p.$2.isBefore(a.$2) ? p : a,
        );
    if (proxima == null) return const SizedBox.shrink();
    final (nombre, inicio, _) = proxima;
    final dias = inicio.difference(hoy).inDays;
    final fecha = '${inicio.day} de ${_meses[inicio.month - 1]}';
    final texto = dias > 1
        ? 'Faltan $dias días para la $nombre ($fecha)'
        : dias == 1
        ? 'Mañana comienza la $nombre'
        : 'La $nombre se rinde estos días. ¡Mucho éxito!';
    final theme = Theme.of(context);
    return Card(
      color: theme.colorScheme.primary,
      child: ListTile(
        leading: Icon(Icons.event, color: theme.colorScheme.onPrimary),
        title: Text(
          texto,
          style: TextStyle(
            color: theme.colorScheme.onPrimary,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
    );
  }
}

class _AccessBanner extends StatelessWidget {
  const _AccessBanner({required this.access});

  final AccessState access;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    if (access.purchased) {
      return Card(
        color: theme.colorScheme.primaryContainer,
        child: ListTile(
          leading: const Icon(Icons.verified),
          title: const Text('Acceso completo activado'),
          subtitle: Text('Vigente hasta el ${formatDate(access.expiresAt!)}'),
        ),
      );
    }
    return Card(
      color: theme.colorScheme.secondaryContainer,
      child: ListTile(
        leading: const Icon(Icons.lock_outline),
        title: Text(
          'Práctica gratis: te quedan ${access.freeLeft} de $freeQuestionLimit preguntas',
        ),
        subtitle: Text(
          [
            access.freeSimulacroUsed
                ? 'Simulacro gratis: ya lo usaste'
                : 'Simulacro gratis: tienes 1 disponible',
            if (access.expired)
              'Tu acceso de $accessMonths meses terminó el '
                  '${formatDate(access.expiresAt!)}',
          ].join('\n'),
        ),
        trailing: TextButton(
          onPressed: () => Navigator.of(context).push(
            MaterialPageRoute<bool>(
              builder: (_) => const PaywallScreen(
                message: 'Desbloquea todas las preguntas y simulacros',
              ),
            ),
          ),
          child: const Text('Desbloquear'),
        ),
      ),
    );
  }
}

class _PruebaCard extends ConsumerWidget {
  const _PruebaCard({required this.prueba, required this.pool});

  final Prueba prueba;
  final List<Question> pool;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // Se vuelve a dibujar al terminar un ensayo (cambia el historial), para
    // actualizar el número de errores por repasar.
    ref.watch(attemptsProvider);
    final errores = ref.read(storageProvider).wrongQuestions(prueba.key);
    final poolErrores = [
      for (final q in pool)
        if (errores.contains(q.id)) q,
    ];
    final theme = Theme.of(context);
    final available = pool.length;
    final simulacroCount = min(prueba.simulacroQuestions, available);

    final color = prueba.color;
    return Card(
      clipBehavior: Clip.antiAlias,
      child: IntrinsicHeight(
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Franja con el color de la prueba.
            Container(width: 8, color: color),
            Expanded(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        CircleAvatar(
                          backgroundColor: color,
                          foregroundColor: Colors.white,
                          child: Icon(prueba.icon),
                        ),
                        const SizedBox(width: 12),
                        Expanded(
                          child: Text(
                            prueba.label,
                            style: theme.textTheme.titleLarge,
                          ),
                        ),
                      ],
                    ),
                    // No se muestra cuántas preguntas tiene el banco.
                    if (available == 0) ...[
                      const SizedBox(height: 4),
                      Text(
                        'Próximamente: aún no hay preguntas.',
                        style: theme.textTheme.bodyMedium,
                      ),
                    ],
                    const SizedBox(height: 12),
                    Row(
                      children: [
                        Expanded(
                          child: FilledButton(
                            style: FilledButton.styleFrom(
                              backgroundColor: color,
                              foregroundColor: Colors.white,
                            ),
                            onPressed: available == 0
                                ? null
                                : () => _startPractice(context),
                            child: const Text('Práctica'),
                          ),
                        ),
                        const SizedBox(width: 8),
                        Expanded(
                          child: OutlinedButton(
                            style: OutlinedButton.styleFrom(
                              foregroundColor: color,
                              side: BorderSide(color: color),
                            ),
                            onPressed: available == 0
                                ? null
                                : () =>
                                      _startSimulacro(context, simulacroCount),
                            child: const Text('Simulacro'),
                          ),
                        ),
                      ],
                    ),
                    if (poolErrores.isNotEmpty)
                      Align(
                        alignment: Alignment.centerLeft,
                        child: TextButton.icon(
                          style: TextButton.styleFrom(foregroundColor: color),
                          icon: const Icon(Icons.replay),
                          label: Text(
                            'Repasar mis errores (${poolErrores.length})',
                          ),
                          onPressed: () => _startReview(context, poolErrores),
                        ),
                      ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  /// Práctica solo con las preguntas que la persona respondió mal.
  void _startReview(BuildContext context, List<Question> errores) {
    final items = buildSession(
      errores,
      min(maxPracticeQuestions, errores.length),
      random: Random(),
    );
    Navigator.of(context).push(
      MaterialPageRoute<void>(
        builder: (_) =>
            QuizScreen(prueba: prueba, mode: QuizMode.practice, items: items),
      ),
    );
  }

  Future<void> _startPractice(BuildContext context) async {
    final count = await _askCount(
      context,
      min(maxPracticeQuestions, pool.length),
    );
    if (count == null || !context.mounted) return;
    _openQuiz(context, QuizMode.practice, count);
  }

  Future<void> _startSimulacro(BuildContext context, int count) async {
    final container = ProviderScope.containerOf(context, listen: false);
    var access = container.read(accessProvider);
    if (!access.canStartSimulacro) {
      final bought = await Navigator.of(context).push<bool>(
        MaterialPageRoute<bool>(
          builder: (_) =>
              const PaywallScreen(message: 'Ya usaste tu simulacro gratis'),
        ),
      );
      if (!context.mounted) return;
      access = container.read(accessProvider);
      if (bought != true && !access.canStartSimulacro) return;
    }
    final esGratis = access.freeSimulacroAvailable;
    CienciasModulo? modulo;
    if (prueba == Prueba.ciencias) {
      modulo = await _askModulo(context);
      if (modulo == null || !context.mounted) return;
    }
    final minutes = prueba.minutes;
    final detalle = modulo == null
        ? ''
        : 'Módulo ${modulo.label}: primero ${comunPorEje * cienciasEjes.length} '
              'preguntas del Módulo Común ($comunPorEje de Biología, '
              '$comunPorEje de Física y $comunPorEje de Química) y luego '
              '$preguntasModulo preguntas del módulo ${modulo.label}.';
    final total = modulo == null
        ? count
        : comunPorEje * cienciasEjes.length + preguntasModulo;
    final ok = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        // Se puede desplazar si el texto no cabe en pantallas chicas.
        scrollable: true,
        title: Text(modulo == null ? 'Simulacro' : 'Simulacro de Ciencias'),
        content: Text(
          'Tendrás $minutes minutos (tiempo oficial) para $total '
          '${total == 1 ? 'pregunta' : 'preguntas'}.'
          '${detalle.isEmpty ? '' : '\n\n$detalle'}'
          '\n\nComo en la prueba real, ${Prueba.experimentalQuestions} preguntas '
          'elegidas al azar son de experimentación y no cuentan para el '
          'puntaje. Al final sabrás cuáles fueron.'
          '${esGratis ? '\n\nEste es tu simulacro gratis: tienes solo uno. '
                    'Se usará al tocar «Comenzar», aunque no lo termines.' : ''}',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(false),
            child: const Text('Cancelar'),
          ),
          FilledButton(
            onPressed: () => Navigator.of(context).pop(true),
            child: const Text('Comenzar'),
          ),
        ],
      ),
    );
    if (ok != true || !context.mounted) return;
    if (esGratis) {
      await container.read(accessProvider.notifier).useFreeSimulacro();
      if (!context.mounted) return;
    }
    if (modulo == null) {
      _openQuiz(context, QuizMode.simulacro, count);
      return;
    }
    final random = Random();
    final items = buildCienciasSimulacro(
      pool,
      modulo,
      random: random,
      seen: _seenFor(context),
    );
    markExperimental(items, Prueba.experimentalQuestions, random: random);
    Navigator.of(context).push(
      MaterialPageRoute<void>(
        builder: (_) => QuizScreen(
          prueba: prueba,
          mode: QuizMode.simulacro,
          items: items,
          modulo: modulo!.label,
          comunCount: min(comunPorEje * cienciasEjes.length, items.length),
        ),
      ),
    );
  }

  void _openQuiz(BuildContext context, QuizMode mode, int count) {
    final random = Random();
    final seen = _seenFor(context);
    // En Lectora, las preguntas de un mismo texto van juntas, como en la prueba.
    final items = prueba == Prueba.lectora
        ? buildLectoraSession(pool, count, random: random, seen: seen)
        : buildSession(pool, count, random: random, seen: seen);
    if (mode == QuizMode.simulacro) {
      markExperimental(items, Prueba.experimentalQuestions, random: random);
    }
    Navigator.of(context).push(
      MaterialPageRoute<void>(
        builder: (_) => QuizScreen(prueba: prueba, mode: mode, items: items),
      ),
    );
  }

  /// Preguntas ya vistas de esta prueba. Si ya se vieron todas, comienza un
  /// ciclo nuevo y vuelven a contar como nuevas.
  Set<String> _seenFor(BuildContext context) {
    final storage = ProviderScope.containerOf(
      context,
      listen: false,
    ).read(storageProvider);
    final seen = storage.seenQuestions(prueba.key);
    if (pool.every((q) => seen.contains(q.id))) {
      storage.resetSeen(prueba.key);
      return const {};
    }
    return seen;
  }

  /// En Ciencias, pregunta qué módulo rendirá la persona, como en la prueba real.
  Future<CienciasModulo?> _askModulo(BuildContext context) {
    return showDialog<CienciasModulo>(
      context: context,
      builder: (context) => SimpleDialog(
        title: const Text('¿Qué módulo vas a rendir?'),
        children: [
          const Padding(
            padding: EdgeInsets.fromLTRB(24, 0, 24, 8),
            child: Text(
              'Todos rinden el Módulo Común. Además, eliges un módulo. '
              'Técnico Profesional es para quienes egresaron de esa formación.',
            ),
          ),
          for (final m in CienciasModulo.values)
            SimpleDialogOption(
              onPressed: () => Navigator.of(context).pop(m),
              child: Padding(
                padding: const EdgeInsets.symmetric(vertical: 6),
                child: Row(
                  children: [
                    Container(
                      width: 14,
                      height: 14,
                      decoration: BoxDecoration(
                        color: cienciasEjeColor(m.eje) ?? AppColors.ciencias,
                        shape: BoxShape.circle,
                      ),
                    ),
                    const SizedBox(width: 12),
                    Text(
                      m.label,
                      style: Theme.of(context).textTheme.titleMedium,
                    ),
                  ],
                ),
              ),
            ),
        ],
      ),
    );
  }

  /// Pregunta cuántas preguntas quiere en la práctica.
  Future<int?> _askCount(BuildContext context, int max) async {
    if (max == 1) return 1;
    var value = min(10, max).toDouble();
    return showDialog<int>(
      context: context,
      builder: (context) => StatefulBuilder(
        builder: (context, setState) => AlertDialog(
          title: const Text('¿Cuántas preguntas?'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(
                '${value.round()}',
                style: Theme.of(context).textTheme.headlineMedium,
              ),
              Slider(
                min: 1,
                max: max.toDouble(),
                divisions: max - 1,
                value: value,
                label: '${value.round()}',
                onChanged: (v) => setState(() => value = v),
              ),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: const Text('Cancelar'),
            ),
            FilledButton(
              onPressed: () => Navigator.of(context).pop(value.round()),
              child: const Text('Comenzar'),
            ),
          ],
        ),
      ),
    );
  }
}

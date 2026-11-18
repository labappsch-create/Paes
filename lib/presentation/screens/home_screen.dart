import 'dart:math';

import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:material_ui/material_ui.dart';

import '../../core/constants.dart';
import '../../domain/ciencias_modulo.dart';
import '../../domain/exam_attempt.dart';
import '../../domain/prueba.dart';
import '../../domain/question.dart';
import '../../domain/quiz_item.dart';
import '../providers.dart';
import 'history_screen.dart';
import 'paywall_screen.dart';
import 'quiz_screen.dart';

/// Pantalla de inicio: elegir prueba y modo.
class HomeScreen extends ConsumerWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final questions = ref.watch(questionsProvider);
    final access = ref.watch(accessProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('PAES App'),
        actions: [
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
        loading: () => const Center(child: CircularProgressIndicator()),
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

class _AccessBanner extends StatelessWidget {
  const _AccessBanner({required this.access});

  final AccessState access;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    if (access.purchased) {
      return Card(
        color: theme.colorScheme.primaryContainer,
        child: const ListTile(
          leading: Icon(Icons.verified),
          title: Text('Acceso completo activado'),
        ),
      );
    }
    return Card(
      color: theme.colorScheme.secondaryContainer,
      child: ListTile(
        leading: const Icon(Icons.lock_outline),
        title: Text(
          'Preguntas gratis: te quedan ${access.freeLeft} de $freeQuestionLimit',
        ),
        trailing: TextButton(
          onPressed: () => Navigator.of(context).push(
            MaterialPageRoute<bool>(builder: (_) => const PaywallScreen()),
          ),
          child: const Text('Desbloquear'),
        ),
      ),
    );
  }
}

class _PruebaCard extends StatelessWidget {
  const _PruebaCard({required this.prueba, required this.pool});

  final Prueba prueba;
  final List<Question> pool;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final available = pool.length;
    final simulacroCount = min(prueba.simulacroQuestions, available);

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(prueba.label, style: theme.textTheme.titleLarge),
            const SizedBox(height: 4),
            Text(
              available == 0
                  ? 'Próximamente: aún no hay preguntas.'
                  : '$available ${available == 1 ? 'pregunta disponible' : 'preguntas disponibles'}',
              style: theme.textTheme.bodyMedium,
            ),
            const SizedBox(height: 12),
            Row(
              children: [
                Expanded(
                  child: FilledButton(
                    onPressed: available == 0
                        ? null
                        : () => _startPractice(context),
                    child: const Text('Práctica'),
                  ),
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: OutlinedButton(
                    onPressed: available == 0
                        ? null
                        : () => _startSimulacro(context, simulacroCount),
                    child: const Text('Simulacro'),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Future<void> _startPractice(BuildContext context) async {
    final count = await _askCount(context, pool.length);
    if (count == null || !context.mounted) return;
    _openQuiz(context, QuizMode.practice, count);
  }

  Future<void> _startSimulacro(BuildContext context, int count) async {
    CienciasModulo? modulo;
    if (prueba == Prueba.ciencias) {
      modulo = await _askModulo(context);
      if (modulo == null || !context.mounted) return;
    }
    final minutes = prueba.minutes;
    final detalle = modulo == null
        ? 'La prueba oficial tiene ${prueba.simulacroQuestions} preguntas. '
              'Este simulacro usa las que hay disponibles hoy.'
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
        title: Text(modulo == null ? 'Simulacro' : 'Simulacro de Ciencias'),
        content: Text(
          'Tendrás $minutes minutos (tiempo oficial) para $total '
          '${total == 1 ? 'pregunta' : 'preguntas'}.\n\n$detalle',
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
    if (modulo == null) {
      _openQuiz(context, QuizMode.simulacro, count);
      return;
    }
    final items = buildCienciasSimulacro(pool, modulo, random: Random());
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
    final items = buildSession(pool, count, random: Random());
    Navigator.of(context).push(
      MaterialPageRoute<void>(
        builder: (_) => QuizScreen(prueba: prueba, mode: mode, items: items),
      ),
    );
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
                child: Text(
                  m.label,
                  style: Theme.of(context).textTheme.titleMedium,
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

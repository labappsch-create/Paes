import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:material_ui/material_ui.dart';

import '../../domain/exam_attempt.dart';
import '../../domain/prueba.dart';
import '../prueba_style.dart';
import '../providers.dart';
import '../widgets/progress_widgets.dart';

/// Historial: primero el avance por prueba (gráfico de simulacros y puntos
/// débiles) y luego la lista de ensayos, del más reciente al más antiguo.
class HistoryScreen extends ConsumerWidget {
  const HistoryScreen({super.key});

  String _formatDate(DateTime d) {
    String two(int n) => n.toString().padLeft(2, '0');
    return '${two(d.day)}/${two(d.month)}/${d.year} ${two(d.hour)}:${two(d.minute)}';
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final all = ref.watch(attemptsProvider);
    final attempts = all.reversed.toList();
    final theme = Theme.of(context);
    final pruebas = [
      for (final p in Prueba.values)
        if (all.any((a) => a.prueba == p)) p,
    ];
    return Scaffold(
      appBar: AppBar(title: const Text('Historial y avance')),
      body: attempts.isEmpty
          ? const Center(
              child: Padding(
                padding: EdgeInsets.all(24),
                child: Text(
                  'Todavía no has terminado ningún ensayo.',
                  textAlign: TextAlign.center,
                ),
              ),
            )
          : ListView(
              padding: const EdgeInsets.symmetric(vertical: 8),
              children: [
                Padding(
                  padding: const EdgeInsets.fromLTRB(16, 8, 16, 4),
                  child: Text('Tu avance', style: theme.textTheme.titleLarge),
                ),
                for (final p in pruebas) _AvanceCard(prueba: p, attempts: all),
                Padding(
                  padding: const EdgeInsets.fromLTRB(16, 16, 16, 4),
                  child: Text(
                    'Todos los ensayos',
                    style: theme.textTheme.titleLarge,
                  ),
                ),
                for (final a in attempts) ...[
                  ListTile(
                    leading: CircleAvatar(
                      backgroundColor: a.prueba.color,
                      foregroundColor: Colors.white,
                      child: Icon(a.prueba.icon),
                    ),
                    title: Text('${a.pruebaLabel} · ${a.mode.label}'),
                    subtitle: Text(
                      '${_formatDate(a.date)}\nAciertos: ${a.correct} de ${a.total}',
                    ),
                    isThreeLine: true,
                    trailing: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Text('${a.score}', style: theme.textTheme.titleLarge),
                        Text('estimado', style: theme.textTheme.bodySmall),
                      ],
                    ),
                  ),
                  const Divider(height: 1),
                ],
              ],
            ),
    );
  }
}

/// Avance de una prueba: gráfico de sus simulacros y aciertos por eje
/// sumando todos sus ensayos.
class _AvanceCard extends StatelessWidget {
  const _AvanceCard({required this.prueba, required this.attempts});

  final Prueba prueba;
  final List<ExamAttempt> attempts;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final propios = attempts.where((a) => a.prueba == prueba).toList();
    final simulacros = propios
        .where((a) => a.mode == QuizMode.simulacro)
        .toList();
    final stats = sumarPorEje(propios);
    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
      clipBehavior: Clip.antiAlias,
      child: Theme(
        data: theme.copyWith(dividerColor: Colors.transparent),
        child: ExpansionTile(
          initiallyExpanded: true,
          leading: CircleAvatar(
            backgroundColor: prueba.color,
            foregroundColor: Colors.white,
            child: Icon(prueba.icon),
          ),
          title: Text(prueba.label),
          subtitle: Text(
            '${propios.length} ${propios.length == 1 ? 'ensayo' : 'ensayos'}',
          ),
          childrenPadding: const EdgeInsets.fromLTRB(16, 0, 16, 16),
          expandedCrossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Puntaje en simulacros', style: theme.textTheme.titleSmall),
            const SizedBox(height: 8),
            ScoreChart(attempts: simulacros, color: prueba.color),
            if (stats.length > 1) ...[
              const SizedBox(height: 16),
              Text(
                prueba == Prueba.lectora
                    ? 'Aciertos por habilidad (todos tus ensayos)'
                    : 'Aciertos por eje (todos tus ensayos)',
                style: theme.textTheme.titleSmall,
              ),
              const SizedBox(height: 8),
              EjeStats(stats: stats, color: prueba.color),
            ],
          ],
        ),
      ),
    );
  }
}

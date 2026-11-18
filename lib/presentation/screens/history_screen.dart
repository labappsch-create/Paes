import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:material_ui/material_ui.dart';

import '../prueba_style.dart';

import '../providers.dart';

/// Lista de ensayos anteriores, del más reciente al más antiguo.
class HistoryScreen extends ConsumerWidget {
  const HistoryScreen({super.key});

  String _formatDate(DateTime d) {
    String two(int n) => n.toString().padLeft(2, '0');
    return '${two(d.day)}/${two(d.month)}/${d.year} ${two(d.hour)}:${two(d.minute)}';
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final attempts = ref.watch(attemptsProvider).reversed.toList();
    return Scaffold(
      appBar: AppBar(title: const Text('Historial de ensayos')),
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
          : ListView.separated(
              itemCount: attempts.length,
              separatorBuilder: (_, _) => const Divider(height: 1),
              itemBuilder: (context, i) {
                final a = attempts[i];
                return ListTile(
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
                      Text(
                        '${a.score}',
                        style: Theme.of(context).textTheme.titleLarge,
                      ),
                      Text(
                        'estimado',
                        style: Theme.of(context).textTheme.bodySmall,
                      ),
                    ],
                  ),
                );
              },
            ),
    );
  }
}

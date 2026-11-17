import 'package:material_ui/material_ui.dart';

import '../../domain/exam_attempt.dart';
import '../../domain/quiz_item.dart';
import '../widgets/question_image.dart';
import 'explanation_screen.dart';

/// Resultado de un ensayo: aciertos, puntaje estimado y revisión pregunta a pregunta.
class ResultsScreen extends StatelessWidget {
  const ResultsScreen({super.key, required this.attempt, required this.items});

  final ExamAttempt attempt;
  final List<QuizItem> items;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      appBar: AppBar(
        title: const Text('Resultados'),
        automaticallyImplyLeading: false,
      ),
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            Card(
              child: Padding(
                padding: const EdgeInsets.all(20),
                child: Column(
                  children: [
                    Text(
                      '${attempt.prueba.label} · ${attempt.mode.label}',
                      style: theme.textTheme.titleMedium,
                    ),
                    const SizedBox(height: 12),
                    Text(
                      '${attempt.score}',
                      style: theme.textTheme.displayMedium,
                    ),
                    Text(
                      'Puntaje estimado',
                      style: theme.textTheme.titleSmall,
                    ),
                    const SizedBox(height: 12),
                    Text(
                      'Aciertos: ${attempt.correct} de ${attempt.total}',
                      style: theme.textTheme.titleMedium,
                    ),
                    const SizedBox(height: 8),
                    Text(
                      'Es una estimación propia y aproximada, no es el puntaje oficial.',
                      style: theme.textTheme.bodySmall,
                      textAlign: TextAlign.center,
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),
            Text('Revisión', style: theme.textTheme.titleLarge),
            const SizedBox(height: 8),
            for (var i = 0; i < items.length; i++)
              _ReviewTile(number: i + 1, item: items[i]),
            const SizedBox(height: 16),
            FilledButton(
              onPressed: () =>
                  Navigator.of(context).popUntil((route) => route.isFirst),
              child: const Text('Volver al inicio'),
            ),
          ],
        ),
      ),
    );
  }
}

class _ReviewTile extends StatelessWidget {
  const _ReviewTile({required this.number, required this.item});

  final int number;
  final QuizItem item;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final answered = item.isAnswered;
    final ok = item.isCorrect;
    final color = !answered
        ? theme.colorScheme.outline
        : ok
            ? Colors.green
            : theme.colorScheme.error;
    final options = item.options;

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(
                  !answered
                      ? Icons.remove_circle_outline
                      : ok
                          ? Icons.check_circle
                          : Icons.cancel,
                  color: color,
                ),
                const SizedBox(width: 8),
                Text('Pregunta $number', style: theme.textTheme.titleSmall),
              ],
            ),
            const SizedBox(height: 8),
            Text(item.question.enunciado),
            QuestionImage(path: item.question.imagen),
            const SizedBox(height: 8),
            Text(
              answered
                  ? 'Tu respuesta: ${options[item.selected!]}'
                  : 'No respondiste esta pregunta',
              style: TextStyle(color: color),
            ),
            if (!ok)
              Text('Respuesta correcta: ${options[item.correctDisplayIndex]}'),
            if (item.question.explicacion.isNotEmpty) ...[
              const SizedBox(height: 8),
              Text(item.question.explicacion, style: theme.textTheme.bodySmall),
            ],
            Align(
              alignment: Alignment.centerRight,
              child: TextButton.icon(
                icon: const Icon(Icons.travel_explore),
                label: const Text('Ver explicación'),
                onPressed: () => Navigator.of(context).push(
                  MaterialPageRoute<void>(
                    builder: (_) =>
                        ExplanationScreen(enunciado: item.question.enunciado),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

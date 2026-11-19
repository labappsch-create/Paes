import 'dart:math';

import 'package:material_ui/material_ui.dart';

import '../../domain/access_period.dart';
import '../../domain/exam_attempt.dart';

/// Aciertos por eje (o habilidad), del más débil al más fuerte, con el punto
/// más débil destacado. [stats]: eje -> [correctas, total].
class EjeStats extends StatelessWidget {
  const EjeStats({super.key, required this.stats, required this.color});

  final Map<String, List<int>> stats;
  final Color color;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final ejes = stats.entries.where((e) => e.value[1] > 0).toList()
      ..sort(
        (a, b) => (a.value[0] / a.value[1]).compareTo(b.value[0] / b.value[1]),
      );
    if (ejes.isEmpty) return const SizedBox.shrink();
    final debil = ejes.first;
    final pctDebil = (100 * debil.value[0] / debil.value[1]).round();
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        if (ejes.length > 1)
          Padding(
            padding: const EdgeInsets.only(bottom: 8),
            child: Text(
              'Tu punto más débil: ${debil.key} ($pctDebil% de aciertos).',
              style: theme.textTheme.titleSmall?.copyWith(
                color: theme.colorScheme.error,
              ),
            ),
          ),
        for (final e in ejes)
          Padding(
            padding: const EdgeInsets.symmetric(vertical: 4),
            child: _Barra(
              label: e.key,
              correct: e.value[0],
              total: e.value[1],
              color: color,
            ),
          ),
      ],
    );
  }
}

class _Barra extends StatelessWidget {
  const _Barra({
    required this.label,
    required this.correct,
    required this.total,
    required this.color,
  });

  final String label;
  final int correct;
  final int total;
  final Color color;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final ratio = correct / total;
    return Semantics(
      label: '$label: $correct de $total correctas',
      excludeSemantics: true,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Expanded(child: Text(label)),
              Text(
                '${(100 * ratio).round()}% · $correct de $total',
                style: theme.textTheme.bodySmall,
              ),
            ],
          ),
          const SizedBox(height: 4),
          ClipRRect(
            borderRadius: BorderRadius.circular(4),
            child: LinearProgressIndicator(
              value: ratio,
              minHeight: 8,
              color: color,
              backgroundColor: color.withValues(alpha: 0.15),
            ),
          ),
        ],
      ),
    );
  }
}

/// Gráfico de línea con el puntaje estimado de cada simulacro, en orden.
class ScoreChart extends StatelessWidget {
  const ScoreChart({super.key, required this.attempts, required this.color});

  /// Simulacros, del más antiguo al más reciente.
  final List<ExamAttempt> attempts;
  final Color color;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    if (attempts.length < 2) {
      return Text(
        attempts.isEmpty
            ? 'Haz un simulacro para ver tu avance aquí.'
            : 'Haz otro simulacro para ver tu avance en un gráfico.',
        style: theme.textTheme.bodyMedium,
      );
    }
    final primero = attempts.first.score;
    final ultimo = attempts.last.score;
    final diff = ultimo - primero;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Semantics(
          label:
              'Gráfico de puntajes: ${attempts.map((a) => a.score).join(', ')}',
          excludeSemantics: true,
          child: SizedBox(
            height: 160,
            width: double.infinity,
            child: CustomPaint(
              painter: _ScorePainter(
                scores: [for (final a in attempts) a.score],
                labels: [
                  for (final a in attempts) formatDate(a.date).substring(0, 5),
                ],
                color: color,
                gridColor: theme.colorScheme.outlineVariant,
                textStyle: theme.textTheme.bodySmall!,
              ),
            ),
          ),
        ),
        const SizedBox(height: 8),
        Text(
          diff > 0
              ? 'Subiste $diff puntos desde tu primer simulacro.'
              : diff < 0
              ? 'Bajaste ${-diff} puntos desde tu primer simulacro.'
              : 'Tu puntaje se mantiene igual que en tu primer simulacro.',
          style: theme.textTheme.bodyMedium,
        ),
      ],
    );
  }
}

class _ScorePainter extends CustomPainter {
  _ScorePainter({
    required this.scores,
    required this.labels,
    required this.color,
    required this.gridColor,
    required this.textStyle,
  });

  final List<int> scores;
  final List<String> labels;
  final Color color;
  final Color gridColor;
  final TextStyle textStyle;

  @override
  void paint(Canvas canvas, Size size) {
    const left = 36.0, bottom = 20.0, top = 8.0, right = 12.0;
    final w = size.width - left - right;
    final h = size.height - top - bottom;
    final minV = max(100, (scores.reduce(min) - 50) ~/ 100 * 100);
    final maxV = min(1000, ((scores.reduce(max) + 50) ~/ 100 + 1) * 100);
    double y(num v) => top + h - (v - minV) / (maxV - minV) * h;
    double x(int i) =>
        left + (scores.length == 1 ? w / 2 : i * w / (scores.length - 1));

    final grid = Paint()
      ..color = gridColor
      ..strokeWidth = 1;
    for (var v = minV; v <= maxV; v += 100) {
      canvas.drawLine(Offset(left, y(v)), Offset(left + w, y(v)), grid);
      _text(canvas, '$v', Offset(0, y(v) - 7));
    }
    final line = Paint()
      ..color = color
      ..strokeWidth = 3
      ..style = PaintingStyle.stroke;
    final path = Path()..moveTo(x(0), y(scores[0]));
    for (var i = 1; i < scores.length; i++) {
      path.lineTo(x(i), y(scores[i]));
    }
    canvas.drawPath(path, line);
    final dot = Paint()..color = color;
    final paso = max(1, (scores.length / 6).ceil());
    for (var i = 0; i < scores.length; i++) {
      canvas.drawCircle(Offset(x(i), y(scores[i])), 4, dot);
      if (i % paso == 0 || i == scores.length - 1) {
        _text(canvas, labels[i], Offset(x(i) - 14, size.height - bottom + 4));
      }
    }
  }

  void _text(Canvas canvas, String s, Offset at) {
    final tp = TextPainter(
      text: TextSpan(text: s, style: textStyle),
      textDirection: TextDirection.ltr,
    )..layout();
    tp.paint(canvas, at);
  }

  @override
  bool shouldRepaint(covariant _ScorePainter old) =>
      old.scores != scores || old.color != color;
}

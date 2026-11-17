import 'package:material_ui/material_ui.dart';

/// Muestra la imagen o gráfico de una pregunta, si tiene.
class QuestionImage extends StatelessWidget {
  const QuestionImage({super.key, required this.path});

  final String? path;

  @override
  Widget build(BuildContext context) {
    final p = path;
    if (p == null) return const SizedBox.shrink();
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 12),
      child: Center(
        child: Container(
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(8),
            border: Border.all(color: Theme.of(context).colorScheme.outlineVariant),
          ),
          padding: const EdgeInsets.all(4),
          child: Image.asset(
            p,
            fit: BoxFit.contain,
            errorBuilder: (_, _, _) => const Padding(
              padding: EdgeInsets.all(16),
              child: Text('No se pudo cargar la imagen.'),
            ),
          ),
        ),
      ),
    );
  }
}

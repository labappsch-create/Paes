import 'package:material_ui/material_ui.dart';

/// Muestra el texto de lectura de una pregunta, en una tarjeta que se puede
/// contraer para dejar más espacio a la pregunta.
class ReadingText extends StatelessWidget {
  const ReadingText({
    super.key,
    required this.text,
    this.initiallyExpanded = true,
  });

  final String? text;
  final bool initiallyExpanded;

  @override
  Widget build(BuildContext context) {
    final t = text;
    if (t == null || t.isEmpty) return const SizedBox.shrink();
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: ExpansionTile(
        initiallyExpanded: initiallyExpanded,
        leading: const Icon(Icons.menu_book),
        title: const Text('Texto'),
        childrenPadding: const EdgeInsets.fromLTRB(16, 0, 16, 16),
        children: [
          SelectableText(
            t,
            style: Theme.of(context).textTheme.bodyLarge?.copyWith(height: 1.5),
          ),
        ],
      ),
    );
  }
}

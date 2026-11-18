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
            border: Border.all(
              color: Theme.of(context).colorScheme.outlineVariant,
            ),
          ),
          padding: const EdgeInsets.all(4),
          // Al tocar la imagen se abre en pantalla completa para hacer zoom.
          child: GestureDetector(
            onTap: () => Navigator.of(context).push(
              MaterialPageRoute<void>(
                fullscreenDialog: true,
                builder: (_) => _ZoomImage(path: p),
              ),
            ),
            child: Stack(
              alignment: Alignment.bottomRight,
              children: [
                Image.asset(
                  p,
                  fit: BoxFit.contain,
                  errorBuilder: (_, _, _) => const Padding(
                    padding: EdgeInsets.all(16),
                    child: Text('No se pudo cargar la imagen.'),
                  ),
                ),
                const Padding(
                  padding: EdgeInsets.all(4),
                  child: Icon(Icons.zoom_in, semanticLabel: 'Ampliar imagen'),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

/// Imagen en pantalla completa, con zoom de dos dedos.
class _ZoomImage extends StatelessWidget {
  const _ZoomImage({required this.path});

  final String path;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Imagen')),
      backgroundColor: Colors.white,
      body: InteractiveViewer(
        maxScale: 5,
        child: Center(child: Image.asset(path, fit: BoxFit.contain)),
      ),
    );
  }
}

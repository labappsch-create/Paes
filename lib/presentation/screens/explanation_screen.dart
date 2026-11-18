import 'package:material_ui/material_ui.dart';
import 'package:webview_flutter/webview_flutter.dart';

/// Abre una búsqueda en Google con el enunciado de la pregunta.
/// Es lo único (junto con la compra) que necesita internet.
class ExplanationScreen extends StatefulWidget {
  const ExplanationScreen({super.key, required this.enunciado});

  final String enunciado;

  @override
  State<ExplanationScreen> createState() => _ExplanationScreenState();
}

class _ExplanationScreenState extends State<ExplanationScreen> {
  late final WebViewController _controller;
  bool _loading = true;
  bool _hasError = false;

  Uri get _url => Uri.parse(
    'https://www.google.com/search?q=${Uri.encodeComponent(widget.enunciado)}',
  );

  @override
  void initState() {
    super.initState();
    _controller = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..setNavigationDelegate(
        NavigationDelegate(
          onPageStarted: (_) => setState(() {
            _loading = true;
            _hasError = false;
          }),
          onPageFinished: (_) => setState(() => _loading = false),
          onWebResourceError: (error) {
            // Solo importa si falla la página principal.
            if (error.isForMainFrame ?? true) {
              setState(() {
                _loading = false;
                _hasError = true;
              });
            }
          },
        ),
      )
      ..loadRequest(_url);
  }

  void _retry() {
    setState(() {
      _hasError = false;
      _loading = true;
    });
    _controller.loadRequest(_url);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Ver explicación')),
      body: Stack(
        children: [
          if (!_hasError) WebViewWidget(controller: _controller),
          if (_loading) const LinearProgressIndicator(),
          if (_hasError)
            Center(
              child: Padding(
                padding: const EdgeInsets.all(24),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    const Icon(Icons.wifi_off, size: 48),
                    const SizedBox(height: 12),
                    const Text(
                      'No pudimos cargar la explicación. Revisa tu conexión a internet.',
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: 16),
                    FilledButton(
                      onPressed: _retry,
                      child: const Text('Reintentar'),
                    ),
                  ],
                ),
              ),
            ),
        ],
      ),
    );
  }
}

import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:material_ui/material_ui.dart';

import '../../domain/access_period.dart';
import '../providers.dart';

/// Abre la ventana para ingresar un código de invitación. Devuelve true si el
/// código activó el acceso.
Future<bool> showInvitationDialog(BuildContext context) async {
  final ok = await showDialog<bool>(
    context: context,
    builder: (_) => const _InvitationDialog(),
  );
  return ok == true;
}

class _InvitationDialog extends ConsumerStatefulWidget {
  const _InvitationDialog();

  @override
  ConsumerState<_InvitationDialog> createState() => _InvitationDialogState();
}

class _InvitationDialogState extends ConsumerState<_InvitationDialog> {
  final _controller = TextEditingController();
  String? _error;
  bool _busy = false;

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  Future<void> _activar() async {
    setState(() {
      _busy = true;
      _error = null;
    });
    final r = await ref
        .read(accessProvider.notifier)
        .redeemCode(_controller.text);
    if (!mounted) return;
    final access = ref.read(accessProvider);
    switch (r) {
      case CodigoResultado.invalido:
        setState(() {
          _busy = false;
          _error = 'El código no es válido. Revísalo e intenta de nuevo.';
        });
      case CodigoResultado.yaVigente:
        setState(() {
          _busy = false;
          _error =
              'Ya tienes acceso completo hasta el '
              '${formatDate(access.expiresAt!)}.';
        });
      case CodigoResultado.activado:
        Navigator.of(context).pop(true);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              '¡Código activado! Tienes acceso completo hasta el '
              '${formatDate(access.expiresAt!)}.',
            ),
          ),
        );
    }
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text('Código de invitación'),
      content: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'Si recibiste un código de invitación, escríbelo aquí para '
            'activar $accessMonths meses de acceso completo gratis.',
          ),
          const SizedBox(height: 12),
          TextField(
            controller: _controller,
            autofocus: true,
            autocorrect: false,
            enableSuggestions: false,
            textInputAction: TextInputAction.done,
            onSubmitted: (_) => _busy ? null : _activar(),
            decoration: InputDecoration(
              labelText: 'Código',
              border: const OutlineInputBorder(),
              errorText: _error,
              errorMaxLines: 3,
            ),
          ),
        ],
      ),
      actions: [
        TextButton(
          onPressed: _busy ? null : () => Navigator.of(context).pop(false),
          child: const Text('Cancelar'),
        ),
        FilledButton(
          onPressed: _busy ? null : _activar,
          child: const Text('Activar'),
        ),
      ],
    );
  }
}

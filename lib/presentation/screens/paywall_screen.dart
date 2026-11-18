import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:material_ui/material_ui.dart';

import '../../core/constants.dart';
import '../providers.dart';
import '../purchase_controller.dart';

/// Pantalla de pago. Se cierra devolviendo `true` si la compra se completó.
class PaywallScreen extends ConsumerWidget {
  const PaywallScreen({super.key, this.message});

  /// Motivo que se muestra arriba. Si es null, se usa el de las preguntas gratis.
  final String? message;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    ref.listen<AccessState>(accessProvider, (previous, next) {
      if (next.purchased && context.mounted) {
        Navigator.of(context).pop(true);
      }
    });

    final purchase = ref.watch(purchaseProvider);
    final controller = ref.read(purchaseProvider.notifier);
    final theme = Theme.of(context);

    return PopScope(
      canPop: !purchase.loading,
      child: Scaffold(
        appBar: AppBar(title: const Text('Acceso Completo PAES')),
        body: SafeArea(
          child: ListView(
            padding: const EdgeInsets.all(24),
            children: [
              Icon(Icons.lock_open, size: 64, color: theme.colorScheme.primary),
              const SizedBox(height: 16),
              Text(
                message ??
                    'Llegaste al límite de las $freeQuestionLimit preguntas gratis',
                style: theme.textTheme.headlineSmall,
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 12),
              Text(
                'Con un solo pago desbloqueas todas las preguntas, los simulacros y el historial.',
                style: theme.textTheme.bodyLarge,
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 24),
              const _Benefit('Preguntas sin límite en las 5 pruebas'),
              const _Benefit('Simulacros con el tiempo oficial'),
              const _Benefit('Historial de tus ensayos'),
              const _Benefit('Pago único: sin suscripción'),
              const SizedBox(height: 24),
              Text(
                purchase.priceLabel,
                style: theme.textTheme.displaySmall,
                textAlign: TextAlign.center,
              ),
              Text(
                'Pago único',
                style: theme.textTheme.bodyMedium,
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 16),
              if (purchase.message != null)
                Padding(
                  padding: const EdgeInsets.only(bottom: 12),
                  child: Text(
                    purchase.message!,
                    textAlign: TextAlign.center,
                    style: TextStyle(color: theme.colorScheme.error),
                  ),
                ),
              FilledButton(
                onPressed:
                    purchase.loading ||
                        !purchase.storeAvailable ||
                        purchase.product == null
                    ? null
                    : controller.buy,
                child: purchase.loading
                    ? const SizedBox(
                        height: 20,
                        width: 20,
                        child: CircularProgressIndicator(strokeWidth: 2),
                      )
                    : Text('Desbloquear por ${purchase.priceLabel}'),
              ),
              const SizedBox(height: 8),
              OutlinedButton(
                onPressed: purchase.loading ? null : controller.restore,
                child: const Text('Restaurar compra'),
              ),
              TextButton(
                onPressed: purchase.loading
                    ? null
                    : () => Navigator.of(context).pop(false),
                child: const Text('Ahora no'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _Benefit extends StatelessWidget {
  const _Benefit(this.text);

  final String text;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        children: [
          Icon(
            Icons.check_circle,
            color: Theme.of(context).colorScheme.primary,
          ),
          const SizedBox(width: 12),
          Expanded(child: Text(text)),
        ],
      ),
    );
  }
}

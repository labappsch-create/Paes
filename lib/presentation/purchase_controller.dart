import 'dart:async';

import 'package:clock/clock.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:in_app_purchase/in_app_purchase.dart';

import '../core/constants.dart';
import '../domain/access_period.dart';
import 'providers.dart';

/// Lo que la pantalla de pago necesita mostrar.
class PurchaseUiState {
  const PurchaseUiState({
    this.loading = false,
    this.storeAvailable = true,
    this.product,
    this.message,
  });

  final bool loading;
  final bool storeAvailable;
  final ProductDetails? product;
  final String? message;

  /// Precio real de la tienda; si aún no llega, el precio por defecto.
  String get priceLabel => product?.price ?? fallbackPriceLabel;

  PurchaseUiState copyWith({
    bool? loading,
    bool? storeAvailable,
    ProductDetails? product,
    String? message,
    bool clearMessage = false,
  }) {
    return PurchaseUiState(
      loading: loading ?? this.loading,
      storeAvailable: storeAvailable ?? this.storeAvailable,
      product: product ?? this.product,
      message: clearMessage ? null : (message ?? this.message),
    );
  }
}

/// Maneja la compra "Acceso Completo Retopaes": un pago único que da 6 meses de
/// acceso y no se renueva solo (en Google Play es un plan prepago; en App Store,
/// una suscripción no renovable). Consulta el producto, compra, restaura y
/// guarda hasta cuándo dura el acceso.
class PurchaseController extends Notifier<PurchaseUiState> {
  final InAppPurchase _iap = InAppPurchase.instance;
  StreamSubscription<List<PurchaseDetails>>? _subscription;

  @override
  PurchaseUiState build() {
    // Se escucha desde el inicio para recibir compras pendientes
    // o restauradas aunque la pantalla de pago no esté abierta.
    _subscription = _iap.purchaseStream.listen(
      _onPurchases,
      onError: (_) {
        state = state.copyWith(
          loading: false,
          message: 'No pudimos completar la compra. Intenta de nuevo.',
        );
      },
    );
    ref.onDispose(() => _subscription?.cancel());
    Future.microtask(_loadProduct);
    return const PurchaseUiState();
  }

  Future<void> _loadProduct() async {
    try {
      final available = await _iap.isAvailable();
      if (!available) {
        state = state.copyWith(
          storeAvailable: false,
          message: 'La tienda no está disponible en este momento.',
        );
        return;
      }
      final response = await _iap.queryProductDetails({fullAccessProductId});
      if (response.productDetails.isEmpty) {
        state = state.copyWith(
          message: 'El producto todavía no está disponible en la tienda.',
        );
        return;
      }
      state = state.copyWith(
        product: response.productDetails.first,
        clearMessage: true,
      );
    } catch (_) {
      state = state.copyWith(
        message: 'No pudimos conectarnos con la tienda. Revisa tu internet.',
      );
    }
  }

  Future<void> buy() async {
    final product = state.product;
    if (product == null) {
      await _loadProduct();
      if (state.product == null) return;
    }
    state = state.copyWith(loading: true, clearMessage: true);
    try {
      await _iap.buyNonConsumable(
        purchaseParam: PurchaseParam(productDetails: state.product!),
      );
    } catch (_) {
      state = state.copyWith(
        loading: false,
        message: 'No pudimos iniciar la compra. Intenta de nuevo.',
      );
    }
  }

  Future<void> restore() async {
    state = state.copyWith(loading: true, clearMessage: true);
    try {
      await _iap.restorePurchases();
      // Si la tienda tiene una compra anterior, llega por _onPurchases.
      await Future<void>.delayed(const Duration(seconds: 5));
      if (!ref.read(accessProvider).purchased && state.loading) {
        state = state.copyWith(
          loading: false,
          message: 'No encontramos un acceso vigente en esta cuenta.',
        );
      }
    } catch (_) {
      state = state.copyWith(
        loading: false,
        message: 'No pudimos restaurar la compra. Intenta de nuevo.',
      );
    }
  }

  Future<void> _onPurchases(List<PurchaseDetails> purchases) async {
    for (final purchase in purchases) {
      if (purchase.productID != fullAccessProductId) continue;
      switch (purchase.status) {
        case PurchaseStatus.pending:
          state = state.copyWith(loading: true, clearMessage: true);
        case PurchaseStatus.purchased:
        case PurchaseStatus.restored:
          final ms = int.tryParse(purchase.transactionDate ?? '');
          final date = ms == null
              ? clock.now()
              : DateTime.fromMillisecondsSinceEpoch(ms);
          await ref
              .read(accessProvider.notifier)
              .grantAccess(
                purchaseId: purchase.purchaseID ?? '${purchase.productID}-$ms',
                purchaseDate: date,
                isNewPurchase: purchase.status == PurchaseStatus.purchased,
              );
          final access = ref.read(accessProvider);
          state = state.copyWith(
            loading: false,
            message: access.purchased
                ? '¡Listo! Tienes acceso completo hasta el '
                      '${formatDate(access.expiresAt!)}.'
                : 'Encontramos tu compra, pero sus $accessMonths meses de '
                      'acceso ya terminaron.',
          );
        case PurchaseStatus.error:
          state = state.copyWith(
            loading: false,
            message: 'La compra no se pudo completar. No se te cobró.',
          );
        case PurchaseStatus.canceled:
          state = state.copyWith(loading: false, message: 'Compra cancelada.');
      }
      if (purchase.pendingCompletePurchase) {
        await _iap.completePurchase(purchase);
      }
    }
  }
}

final purchaseProvider = NotifierProvider<PurchaseController, PurchaseUiState>(
  PurchaseController.new,
);

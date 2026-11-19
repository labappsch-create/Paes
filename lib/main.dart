import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:material_ui/material_ui.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'core/constants.dart';
import 'presentation/providers.dart';
import 'presentation/prueba_style.dart';
import 'presentation/purchase_controller.dart';
import 'presentation/screens/home_screen.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final prefs = await SharedPreferences.getInstance();
  runApp(
    ProviderScope(
      overrides: [sharedPreferencesProvider.overrideWithValue(prefs)],
      child: const PaesApp(),
    ),
  );
}

class PaesApp extends ConsumerWidget {
  const PaesApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // Se activa desde el inicio para recibir compras pendientes o restauradas.
    ref.watch(purchaseProvider);
    final escala = ref.watch(textScaleProvider);

    return MaterialApp(
      title: appName,
      debugShowCheckedModeBanner: false,
      // Colores del logo de Retopaes (prueba_style.dart).
      theme: appTheme(),
      // Tamaño de letra elegido en Ajustes, sobre el que ya tenga el teléfono.
      builder: (context, child) {
        final mq = MediaQuery.of(context);
        final base = mq.textScaler.scale(14) / 14;
        return MediaQuery(
          data: mq.copyWith(textScaler: TextScaler.linear(base * escala)),
          child: child!,
        );
      },
      home: const HomeScreen(),
    );
  }
}

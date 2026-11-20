import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:material_ui/material_ui.dart';

import '../../core/constants.dart';
import '../providers.dart';
import '../widgets/invitation_dialog.dart';

/// Ajustes: tamaño de letra, política de privacidad y datos de la app.
class SettingsScreen extends ConsumerWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final theme = Theme.of(context);
    final escala = ref.watch(textScaleProvider);
    return Scaffold(
      appBar: AppBar(title: const Text('Ajustes')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Text('Tamaño de letra', style: theme.textTheme.titleMedium),
          const SizedBox(height: 8),
          SegmentedButton<double>(
            segments: [
              for (final e in textScales.entries)
                ButtonSegment(value: e.value, label: Text(e.key)),
            ],
            selected: {escala},
            showSelectedIcon: false,
            onSelectionChanged: (v) =>
                ref.read(textScaleProvider.notifier).set(v.first),
          ),
          const SizedBox(height: 12),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Text(
                'Así se verán los textos de lectura y las preguntas.',
                style: theme.textTheme.bodyLarge,
              ),
            ),
          ),
          const SizedBox(height: 24),
          const Divider(),
          ListTile(
            contentPadding: EdgeInsets.zero,
            leading: const Icon(Icons.card_giftcard),
            title: const Text('Código de invitación'),
            trailing: const Icon(Icons.chevron_right),
            onTap: () => showInvitationDialog(context),
          ),
          ListTile(
            contentPadding: EdgeInsets.zero,
            leading: const Icon(Icons.privacy_tip_outlined),
            title: const Text('Política de privacidad'),
            trailing: const Icon(Icons.chevron_right),
            onTap: () => Navigator.of(context).push(
              MaterialPageRoute<void>(builder: (_) => const PrivacyScreen()),
            ),
          ),
          const ListTile(
            contentPadding: EdgeInsets.zero,
            leading: Icon(Icons.info_outline),
            title: Text(appName),
            subtitle: Text(
              'Práctica para la PAES. Preguntas originales: no son '
              'preguntas oficiales del DEMRE.',
            ),
          ),
        ],
      ),
    );
  }
}

/// Muestra la política de privacidad guardada en la app.
class PrivacyScreen extends StatelessWidget {
  const PrivacyScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      appBar: AppBar(title: const Text('Política de privacidad')),
      body: FutureBuilder<String>(
        future: rootBundle.loadString(privacyPolicyAsset),
        builder: (context, snap) {
          if (!snap.hasData) {
            return const Center(child: CircularProgressIndicator());
          }
          // Formato simple: «# » título, «## » subtítulo, «- » viñeta.
          final widgets = <Widget>[];
          for (final line in snap.data!.split('\n')) {
            if (line.trim().isEmpty) continue;
            if (line.startsWith('# ')) {
              widgets.add(
                Text(line.substring(2), style: theme.textTheme.headlineSmall),
              );
            } else if (line.startsWith('## ')) {
              widgets.add(
                Padding(
                  padding: const EdgeInsets.only(top: 16),
                  child: Text(
                    line.substring(3),
                    style: theme.textTheme.titleMedium,
                  ),
                ),
              );
            } else if (line.startsWith('- ')) {
              widgets.add(
                Padding(
                  padding: const EdgeInsets.only(left: 8, top: 4),
                  child: Text('•  ${line.substring(2)}'),
                ),
              );
            } else {
              widgets.add(
                Padding(
                  padding: const EdgeInsets.only(top: 8),
                  child: Text(line),
                ),
              );
            }
          }
          return ListView(padding: const EdgeInsets.all(16), children: widgets);
        },
      ),
    );
  }
}

import 'dart:convert';

import 'package:crypto/crypto.dart';

/// Códigos de invitación: liberan el acceso completo por 6 meses sin pagar.
///
/// El código no se guarda tal cual (el repositorio es público): se guarda su
/// huella SHA-256 con un prefijo fijo. Para agregar o cambiar un código, se
/// calcula la huella de `'retopaes-invitacion-v1:' + código en minúsculas` y se
/// agrega a [_huellas].
const _prefijo = 'retopaes-invitacion-v1:';

const _huellas = {
  'c4a0aeb3c381848de9e456c3216ff5a82f61652ea25b893b3578b1281a3e174e',
};

/// Deja el código en una forma comparable: sin espacios y en minúsculas, para
/// que no importe si la persona lo escribe con mayúsculas o con un espacio.
String normalizarCodigo(String codigo) =>
    codigo.replaceAll(RegExp(r'\s'), '').toLowerCase();

/// True si [codigo] es un código de invitación válido.
bool esCodigoValido(String codigo) {
  final n = normalizarCodigo(codigo);
  if (n.isEmpty) return false;
  final huella = sha256.convert(utf8.encode('$_prefijo$n')).toString();
  return _huellas.contains(huella);
}

/// Duración del acceso completo pagado, en meses. Es un pago único que no se
/// renueva solo: al terminar, la app vuelve a la versión gratis.
const int accessMonths = 6;

/// Suma [months] meses a [date], ajustando el día si el mes de llegada es más
/// corto (por ejemplo, 31 de agosto + 6 meses = 28 o 29 de febrero).
DateTime addMonths(DateTime date, int months) {
  final totalMonths = date.month - 1 + months;
  final year = date.year + totalMonths ~/ 12;
  final month = totalMonths % 12 + 1;
  final lastDay = DateTime(year, month + 1, 0).day;
  final day = date.day > lastDay ? lastDay : date.day;
  return DateTime(
    year,
    month,
    day,
    date.hour,
    date.minute,
    date.second,
    date.millisecond,
  );
}

/// Fecha corta en formato chileno: 17/05/2027.
String formatDate(DateTime d) {
  String two(int n) => n.toString().padLeft(2, '0');
  return '${two(d.day)}/${two(d.month)}/${d.year}';
}

/// Calcula hasta cuándo dura el acceso después de una compra.
///
/// - Compra nueva: los 6 meses se suman desde el final del acceso actual, si
///   todavía está vigente (así no se pierden días al comprar antes de tiempo).
/// - Compra restaurada (por ejemplo, en un celular nuevo): los 6 meses se
///   cuentan desde la fecha en que se pagó.
/// El resultado nunca es anterior al acceso que ya se tenía.
DateTime computeExpiry({
  required DateTime purchaseDate,
  required bool isNewPurchase,
  DateTime? currentExpiry,
}) {
  var base = purchaseDate;
  if (isNewPurchase &&
      currentExpiry != null &&
      currentExpiry.isAfter(purchaseDate)) {
    base = currentExpiry;
  }
  final candidate = addMonths(base, accessMonths);
  if (currentExpiry != null && currentExpiry.isAfter(candidate)) {
    return currentExpiry;
  }
  return candidate;
}

export function formatDate(date: Date): string {
  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0');
  return `${day}/${month}/${date.getFullYear()}`;
}

export function parseDate(value: string): Date | null {
  const [day, month, year] = value.split('/').map(Number);
  const date = new Date(year, month - 1, day);

  const isValid =
    date.getFullYear() === year && date.getMonth() === month - 1 && date.getDate() === day;

  return isValid ? date : null;
}

export function lastDayOfMonth(date: Date): Date {
  return new Date(date.getFullYear(), date.getMonth() + 1, 0);
}

/** Mascara de entrada DD/MM/AAAA — use no (input) do template */
export function applyDateMask(input: HTMLInputElement): void {
  let v = input.value.replace(/\D/g, '').substring(0, 8);

  if (v.length > 4) v = v.replace(/(\d{2})(\d{2})(\d+)/, '$1/$2/$3');
  else if (v.length > 2) v = v.replace(/(\d{2})(\d+)/, '$1/$2');

  input.value = v;
}

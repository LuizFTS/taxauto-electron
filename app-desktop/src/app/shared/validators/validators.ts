// validators.ts ou utils.ts

export const LISTA_UF = [
  'AC',
  'AL',
  'AP',
  'AM',
  'BA',
  'CE',
  'DF',
  'ES',
  'GO',
  'MA',
  'MT',
  'MS',
  'MG',
  'PA',
  'PB',
  'PR',
  'PE',
  'PI',
  'RJ',
  'RN',
  'RS',
  'RO',
  'RR',
  'SC',
  'SP',
  'SE',
  'TO',
];

export function validarEFormatarUF(uf: string): string | null {
  const ufUpper = uf?.trim().toUpperCase();
  return LISTA_UF.includes(ufUpper) ? ufUpper : null;
}

export function validarEFiltrarCNPJ(cnpj: string): string | null {
  // Remove tudo que não for número
  const apenasNumeros = cnpj?.replace(/\D/g, '');

  // Validação básica de tamanho e dígitos repetidos
  if (!apenasNumeros || apenasNumeros.length !== 14 || !!apenasNumeros.match(/^(\d)\1+$/)) {
    return null;
  }

  return apenasNumeros;
}

export function validarEFiltrarIE(ie: string): string | null {
  // Remove tudo que não for número
  const apenasNumeros = ie?.replace(/\D/g, '');

  // Validação básica de tamanho e dígitos repetidos
  return apenasNumeros && apenasNumeros.length >= 5 ? apenasNumeros : null;
}

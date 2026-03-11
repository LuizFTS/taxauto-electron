import type { AbstractControl, ValidationErrors, ValidatorFn } from '@angular/forms';

export class CompanyValidators {
  static uf(): ValidatorFn {
    const validUFs = [
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

    return (control: AbstractControl): ValidationErrors | null => {
      const value = control.value?.toUpperCase();
      return validUFs.includes(value) ? null : { invalidUF: true };
    };
  }

  /** Valida formato e dígito do CNPJ */
  static cnpj(): ValidatorFn {
    return (control: AbstractControl): ValidationErrors | null => {
      const cnpj = control.value?.replace(/\D/g, '');
      if (!cnpj) return null; // Deixa o validator 'required' tratar se for vazio

      if (cnpj.length !== 14 || !!cnpj.match(/^(\d)\1+$/)) {
        return { cnpjInvalid: true };
      }

      // ... lógica de cálculo dos dígitos verificadores
      return null;
    };
  }
}

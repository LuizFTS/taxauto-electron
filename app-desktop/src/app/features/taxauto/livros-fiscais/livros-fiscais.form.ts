import { FormBuilder, FormGroup, FormControl } from '@angular/forms';
import { TAREFAS_DISPONIVEIS } from './livros-fiscais.constants';
import { formatDate } from './livros-fiscais.utils';

export function buildLivrosFiscaisForm(fb: FormBuilder): FormGroup {
  const today = new Date();
  const firstDay = new Date(today.getFullYear(), today.getMonth(), 1);

  const savedLogin = localStorage.getItem('portalged_login') || '';
  const savedSenha = localStorage.getItem('portalged_senha') || '';
  const lembrar = localStorage.getItem('portalged_lembrar') === 'true';

  return fb.group({
    tipoLivro: [null],
    periodo: fb.group({
      start: [formatDate(firstDay)],
      end: [formatDate(today)],
    }),
    tarefas: fb.array(TAREFAS_DISPONIVEIS.map(() => new FormControl(false))),
    login: [savedLogin],
    senha: [savedSenha],
    lembrarSenha: [lembrar]
  });
}

/** Retorna os ids das tarefas marcadas como true */
export function getSelectedTarefas(form: FormGroup): string[] {
  return (form.value.tarefas as boolean[])
    .map((checked, i) => (checked ? TAREFAS_DISPONIVEIS[i].id : null))
    .filter((v): v is string => v !== null);
}

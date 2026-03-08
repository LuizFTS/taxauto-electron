import {
  Component,
  ChangeDetectionStrategy,
  Input,
  signal,
  computed,
  ElementRef,
  inject,
  HostListener,
  forwardRef,
  ViewChild,
  input,
  AfterViewInit,
} from '@angular/core';
import { ControlValueAccessor, NG_VALUE_ACCESSOR } from '@angular/forms';

export interface SelectOption<T = unknown> {
  label: string;
  value: T;
}

@Component({
  standalone: true,
  selector: 'app-select',
  templateUrl: './select.html',
  styleUrl: './select.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(() => Select),
      multi: true,
    },
  ],
})
export class Select<T = unknown> implements ControlValueAccessor, AfterViewInit {
  @ViewChild('selectTrigger') selectTrigger!: ElementRef<HTMLElement>;

  @Input() options: SelectOption<T>[] = [];
  @Input() placeholder = 'Select';

  private host = inject(ElementRef<HTMLElement>);

  isOpen = signal(false);
  focusedIndex = signal<number>(-1);

  _value = signal<T | null>(null);
  disabled = signal(false);

  selectedOption = computed(() => this.options.find((o) => o.value === this._value()));

  autofocus = input<boolean>(false);

  ngAfterViewInit(): void {
    // 3. Se o input autofocus for verdadeiro, damos o foco
    if (this.autofocus()) {
      // Usamos um pequeno timeout para garantir que o browser
      // terminou a renderização antes de tentar focar
      setTimeout(() => {
        this.selectTrigger.nativeElement.focus();
      }, 0);
    }
  }

  /* ===========================
     CVA CALLBACKS
  ============================ */

  private onChange: (value: T | null) => void = () => {};
  private onTouched: () => void = () => {};

  writeValue(value: T | null): void {
    this._value.set(value);
  }

  registerOnChange(fn: (value: T | null) => void): void {
    this.onChange = fn;
  }

  registerOnTouched(fn: () => void): void {
    this.onTouched = fn;
  }

  setDisabledState(isDisabled: boolean): void {
    this.disabled.set(isDisabled);
  }

  /* ===========================
     UI LOGIC
  ============================ */

  toggle() {
    if (this.disabled()) return;
    this.isOpen.update((v) => !v);
  }

  select(option: SelectOption<T>) {
    this._value.set(option.value);
    this.onChange(option.value);
    this.onTouched();
    this.isOpen.set(false);
  }

  @HostListener('document:click', ['$event'])
  onOutsideClick(event: MouseEvent) {
    if (!this.host.nativeElement.contains(event.target as Node)) {
      this.isOpen.set(false);
    }
  }

  @HostListener('keydown.arrowdown', ['$event'])
  onArrowDown(event: Event) {
    if (this.isOpen()) {
      event.preventDefault(); // Impede que a página faça scroll
      this.pressKeyDown();
    }
  }

  @HostListener('keydown.arrowup', ['$event'])
  onArrowUp(event: Event) {
    if (this.isOpen()) {
      event.preventDefault(); // Impede que a página faça scroll
      this.pressKeyUp();
    }
  }

  @HostListener('keydown.enter', ['$event'])
  onEnter(event: Event) {
    event.preventDefault();
    if (this.isOpen() && this.focusedIndex() !== -1) {
      this.select(this.options[this.focusedIndex()]);
    }
  }

  @HostListener('keydown.esc', ['$event'])
  onEsc(event: Event) {
    event.preventDefault();
    this.isOpen.set(false);
  }

  pressKeyDown() {
    const totalOptions = this.options.length;

    if (totalOptions === 0) return;

    // 1. Calcula o próximo índice
    // Se for -1 (nada focado), vai para 0.
    // Se for o último, volta para o 0 (lógica de loop).
    const nextIndex = (this.focusedIndex() + 1) % totalOptions;

    // 2. Atualiza o estado do foco
    this.focusedIndex.set(nextIndex);

    // 3. Opcional: Garantir que o item focado está visível (Scroll)
    const optionsElements = document.querySelectorAll('.app-select__option');
    (optionsElements[nextIndex] as HTMLElement)?.focus();
    this.scrollToFocusedOption(nextIndex);
  }
  pressKeyUp() {
    const totalOptions = this.options.length;

    if (totalOptions === 0) return;

    // 1. Calcula o próximo índice
    // Se for -1 (nada focado), vai para 0.
    // Se for o último, volta para o 0 (lógica de loop).
    const previousIndex = (this.focusedIndex() - 1) % totalOptions;

    // 2. Atualiza o estado do foco
    this.focusedIndex.set(previousIndex);

    // 3. Opcional: Garantir que o item focado está visível (Scroll)
    this.scrollToFocusedOption(previousIndex);
  }

  private scrollToFocusedOption(index: number) {
    // Pequeno timeout para garantir que o DOM atualizou
    setTimeout(() => {
      const elements = document.querySelectorAll('.app-select__option');
      const target = elements[index] as HTMLElement;
      if (target) {
        target.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
      }
    });
  }
}

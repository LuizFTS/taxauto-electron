export type KpiColorType = 'danger' | 'warning' | 'info' | 'success';

export interface KpiCardData {
  title: string;
  value: string | number;
  icon: string;
  type: KpiColorType;
}

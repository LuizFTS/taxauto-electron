import type { FlowTask } from '../../../shared/components/flow-tasks-modal/flow-tasks-modal';

export interface CancelledInvoicesRequest {
  start_date: string;
  end_date: string;
  filiais: string[];
  save_path: string;
  login: string;
  password: string;
}

export interface CancelledInvoicesFlowRequest {
  start_date: string;
  end_date: string;
  filiais: string[];
  login: string;
  password: string;
  tasks: FlowTask[];
}

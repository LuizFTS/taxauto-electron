export interface DownloadXMLsRequest {
  start_date: string;
  end_date: string;
  filiais: string[];
  save_path: string;
  login: string;
  password: string;
  tipo_documento: number;
  tipo_operacao: number;
}

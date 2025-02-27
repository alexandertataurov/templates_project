export interface Template {
  id: number;
  templateType: string;
  displayName: string;
  fields: string[];
  file_path?: string;
}

export interface TemplateFormData {
  file: File | null;
  templateType: string;
  displayName: string;
  fields: string[];
}

export type TemplateUpdateData = Partial<Pick<Template, 'displayName' | 'fields'>>; 
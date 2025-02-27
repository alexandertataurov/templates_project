import { axiosInstance } from './axios';

export interface Template {
  id: number;
  template_type: string;
  display_name: string;
  fields: string[];
  created_at: string;
  updated_at: string;
}

export interface UploadResponse {
  message: string;
  extractedFields: string[];
}

export const extractFields = async (file: File): Promise<string[]> => {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await axiosInstance.post<string[]>("/templates/extract", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return response.data;
  } catch (error) {
    throw new Error(`Failed to extract fields: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
};

export const listTemplates = async (): Promise<Template[]> => {
  const response = await axiosInstance.get('/templates');
  return response.data;
};

export const updateTemplate = async (
  templateId: number,
  updates: { displayName?: string; fields?: string[] }
): Promise<void> => {
  const formData = new FormData();
  formData.append('template_id', templateId.toString());
  
  if (updates.displayName !== undefined) {
    formData.append('display_name', updates.displayName);
  }
  
  if (updates.fields !== undefined) {
    formData.append('fields', JSON.stringify(updates.fields));
  }

  await axiosInstance.post('/templates/update', formData);
};

export const deleteTemplate = async (templateId: number): Promise<void> => {
  await axiosInstance.delete(`/templates/${templateId}`);
};

export const uploadTemplate = async (
  file: File,
  templateType: string,
  displayName: string,
  fields: string[]
): Promise<{ id: number; message: string }> => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('template_type', templateType);
  formData.append('display_name', displayName);
  formData.append('fields', JSON.stringify(fields));

  const response = await axiosInstance.post('/templates/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};
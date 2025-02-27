import { axiosInstance } from './axios';

/**
 * Template interface for the UI using camelCase keys.
 */
export interface Template {
  id: number;
  templateType: string;
  displayName: string;
  fields: string[];
  createdAt: string;
  updatedAt: string;
}

/**
 * Response interface returned after uploading a template.
 */
export interface UploadResponse {
  message: string;
  extractedFields: string[];
}

/**
 * Helper function to transform a template object received from the API
 * (which uses snake_case) into our camelCase Template interface.
 *
 * @param template - The template object from the API.
 * @returns A Template object with camelCase keys.
 */
const transformTemplate = (template: any): Template => ({
  id: template.id,
  templateType: template.template_type,
  displayName: template.display_name,
  fields: template.fields,
  createdAt: template.created_at,
  updatedAt: template.updated_at,
});

/**
 * Extracts fields from a given file by sending it to the server.
 *
 * @param file - The file from which to extract fields.
 * @returns A promise that resolves to an array of strings.
 */
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

/**
 * Retrieves the list of templates from the server and transforms each
 * template from snake_case to camelCase.
 *
 * @returns A promise that resolves to an array of Template objects.
 */
export const listTemplates = async (): Promise<Template[]> => {
  const response = await axiosInstance.get('/templates');
  return response.data.map((template: any) => transformTemplate(template));
};

/**
 * Updates a template on the server.
 *
 * The API expects snake_case keys for the payload, so we send display_name and fields.
 *
 * @param templateId - The ID of the template to update.
 * @param updates - An object containing optional displayName and fields properties.
 */
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

/**
 * Deletes a template from the server.
 *
 * @param templateId - The ID of the template to delete.
 */
export const deleteTemplate = async (templateId: number): Promise<void> => {
  await axiosInstance.delete(`/templates/${templateId}`);
};

/**
 * Uploads a new template to the server.
 *
 * The API expects snake_case keys for the payload.
 *
 * @param file - The file to upload.
 * @param templateType - The type of the template.
 * @param displayName - The display name for the template.
 * @param fields - An array of fields associated with the template.
 * @returns A promise that resolves to an object containing the new template's ID and a message.
 */
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

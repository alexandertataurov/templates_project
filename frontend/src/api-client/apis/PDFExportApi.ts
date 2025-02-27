/* tslint:disable */
/* eslint-disable */
/**
 * Самый Крутой Бэк
 * Бэкэнд для управления договорами, счетами, платежами и шаблонами
 *
 * The version of the OpenAPI document: 1.0.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */


import * as runtime from '../runtime';
import type {
  HTTPValidationError,
} from '../models/index';
import {
    HTTPValidationErrorFromJSON,
    HTTPValidationErrorToJSON,
} from '../models/index';

export interface ExportContractPdfContractContractIdGetRequest {
    contractId: number;
    format?: ExportContractPdfContractContractIdGetFormatEnum;
    template?: string;
    excludeFields?: Array<string>;
}

/**
 * 
 */
export class PDFExportApi extends runtime.BaseAPI {

    /**
     * Генерация контракта в формате PDF или DOCX.
     * Export Contract
     */
    async exportContractPdfContractContractIdGetRaw(requestParameters: ExportContractPdfContractContractIdGetRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<void>> {
        if (requestParameters['contractId'] == null) {
            throw new runtime.RequiredError(
                'contractId',
                'Required parameter "contractId" was null or undefined when calling exportContractPdfContractContractIdGet().'
            );
        }

        const queryParameters: any = {};

        if (requestParameters['format'] != null) {
            queryParameters['format'] = requestParameters['format'];
        }

        if (requestParameters['template'] != null) {
            queryParameters['template'] = requestParameters['template'];
        }

        if (requestParameters['excludeFields'] != null) {
            queryParameters['exclude_fields'] = requestParameters['excludeFields'];
        }

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/pdf/contract/{contract_id}`.replace(`{${"contract_id"}}`, encodeURIComponent(String(requestParameters['contractId']))),
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.VoidApiResponse(response);
    }

    /**
     * Генерация контракта в формате PDF или DOCX.
     * Export Contract
     */
    async exportContractPdfContractContractIdGet(requestParameters: ExportContractPdfContractContractIdGetRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<void> {
        await this.exportContractPdfContractContractIdGetRaw(requestParameters, initOverrides);
    }

}

/**
 * @export
 */
export const ExportContractPdfContractContractIdGetFormatEnum = {
    Pdf: 'pdf',
    Docx: 'docx'
} as const;
export type ExportContractPdfContractContractIdGetFormatEnum = typeof ExportContractPdfContractContractIdGetFormatEnum[keyof typeof ExportContractPdfContractContractIdGetFormatEnum];

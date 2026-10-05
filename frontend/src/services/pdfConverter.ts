import api from './api'


export const convertPdfToExcel = async (
    file: File,
): Promise<Blob> => {

    const formData = new FormData()

    formData.append(
        'file',
        file,
    )

    const response = await api.post(
        'pdf-converter/excel',
        formData,
        {
            responseType: 'blob',
        },
    )

    return response.data
}


export const convertPdfToWord = async (
    file: File,
): Promise<Blob> => {

    const formData = new FormData()

    formData.append(
        'file',
        file,
    )

    const response = await api.post(
        'pdf-converter/word',
        formData,
        {
            responseType: 'blob',
        },
    )

    return response.data
}


export const getErrorMessage = async (
    error: any,
): Promise<string> => {

    if (
        error?.response?.data instanceof Blob
    ) {

        try {

            const text =
                await error.response.data.text()

            const data =
                JSON.parse(text)

            return (
                data.detail ||
                data.message ||
                'Request failed.'
            )

        } catch {

            return 'Request failed.'
        }
    }

    return (
        error?.response?.data?.detail ||
        error?.response?.data?.message ||
        error?.message ||
        'Request failed.'
    )
}
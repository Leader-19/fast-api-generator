<script setup lang="ts">
import { ref, computed } from 'vue'
import {
    convertPdfToExcel,
    convertPdfToWord,
    getErrorMessage,
} from '@/services/pdfConverter'

const selectedFile = ref<File | null>(null)
const fileInputRef = ref<HTMLInputElement | null>(null)

const loadingExcel = ref(false)
const loadingWord = ref(false)

const errorMessage = ref('')
const successMessage = ref('')

const isDragging = ref(false)

const isConverting = computed(
    () => loadingExcel.value || loadingWord.value,
)

const fileSize = computed(() => {
    if (!selectedFile.value) {
        return ''
    }

    const size = selectedFile.value.size

    if (size < 1024 * 1024) {
        return `${(size / 1024).toFixed(1)} KB`
    }

    return `${(size / 1024 / 1024).toFixed(2)} MB`
})

const selectFile = (file: File | undefined) => {
    errorMessage.value = ''
    successMessage.value = ''

    if (!file) {
        return
    }

    if (
        file.type !== 'application/pdf' &&
        !file.name.toLowerCase().endsWith('.pdf')
    ) {
        selectedFile.value = null

        errorMessage.value =
            'Please select a PDF file.'

        if (fileInputRef.value) {
            fileInputRef.value.value = ''
        }

        return
    }

    selectedFile.value = file
}

const handleFileChange = (event: Event) => {
    const target = event.target as HTMLInputElement

    selectFile(target.files?.[0])
}

const handleDrop = (event: DragEvent) => {
    isDragging.value = false

    const file = event.dataTransfer?.files?.[0]

    selectFile(file)
}

const openFilePicker = () => {
    if (!isConverting.value) {
        fileInputRef.value?.click()
    }
}

const clearFile = () => {
    selectedFile.value = null
    errorMessage.value = ''
    successMessage.value = ''

    if (fileInputRef.value) {
        fileInputRef.value.value = ''
    }
}

const downloadFile = (
    blob: Blob,
    filename: string,
) => {
    const url = window.URL.createObjectURL(blob)

    const link = document.createElement('a')

    link.href = url
    link.download = filename

    document.body.appendChild(link)

    link.click()

    link.remove()

    window.URL.revokeObjectURL(url)
}

const convertExcel = async () => {
    if (!selectedFile.value) {
        errorMessage.value =
            'Please select a PDF file first.'

        return
    }

    try {
        loadingExcel.value = true
        errorMessage.value = ''
        successMessage.value = ''

        const blob = await convertPdfToExcel(
            selectedFile.value,
        )

        const filename =
            selectedFile.value.name.replace(
                /\.pdf$/i,
                '.xlsx',
            )

        downloadFile(blob, filename)

        successMessage.value =
            'PDF converted to Excel successfully.'
    } catch (error: any) {
        console.error(error)

        errorMessage.value =
            await getErrorMessage(error)
    } finally {
        loadingExcel.value = false
    }
}

const convertWord = async () => {
    if (!selectedFile.value) {
        errorMessage.value =
            'Please select a PDF file first.'

        return
    }

    try {
        loadingWord.value = true
        errorMessage.value = ''
        successMessage.value = ''

        const blob = await convertPdfToWord(
            selectedFile.value,
        )

        const filename =
            selectedFile.value.name.replace(
                /\.pdf$/i,
                '.docx',
            )

        downloadFile(blob, filename)

        successMessage.value =
            'PDF converted to Word successfully.'
    } catch (error: any) {
        console.error(error)

        errorMessage.value =
            await getErrorMessage(error)
    } finally {
        loadingWord.value = false
    }
}
</script>

<template>
    <div class="min-h-full bg-gray-50 p-6">
        <div class="mx-auto max-w-4xl">

            <!-- Header -->
            <div class="mb-8">
                <div class="flex items-center gap-3">
                    <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-red-100">
                        <svg class="h-6 w-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M7 3h7l5 5v13H7V3z" />
                            <path stroke-linecap="round" stroke-linejoin="round" d="M14 3v6h5" />
                        </svg>
                    </div>

                    <div>
                        <h1 class="text-2xl font-semibold text-gray-900">
                            PDF Converter
                        </h1>

                        <p class="mt-1 text-sm text-gray-500">
                            Convert PDF reports into
                            Excel or Word files.
                        </p>
                    </div>
                </div>
            </div>

            <!-- Main Card -->
            <div class="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">

                <!-- Upload Area -->
                <div class="cursor-pointer rounded-xl border-2 border-dashed p-10 text-center transition" :class="isDragging
                        ? 'border-blue-500 bg-blue-50'
                        : 'border-gray-300 hover:border-blue-400 hover:bg-gray-50'
                    " @click="openFilePicker" @dragover.prevent="
                        isDragging = true
                        " @dragleave.prevent="
                        isDragging = false
                        " @drop.prevent="handleDrop">
                    <input ref="fileInputRef" type="file" accept=".pdf,application/pdf" class="hidden"
                        @change="handleFileChange" />

                    <div class="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-red-50">
                        <svg class="h-7 w-7 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M12 16V4m0 0l-4 4m4-4l4 4M5 20h14" />
                        </svg>
                    </div>

                    <p class="text-sm font-medium text-gray-700">
                        Drop your PDF here
                    </p>

                    <p class="mt-1 text-sm text-gray-500">
                        or
                        <span class="font-medium text-blue-600">
                            click to browse
                        </span>
                    </p>

                    <p class="mt-3 text-xs text-gray-400">
                        PDF files only
                    </p>
                </div>

                <!-- Selected File -->
                <div v-if="selectedFile" class="mt-6 rounded-xl border border-gray-200 bg-gray-50 p-4">
                    <div class="flex items-center justify-between gap-4">
                        <div class="flex min-w-0 items-center gap-3">
                            <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-red-100">
                                <svg class="h-5 w-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M7 3h7l5 5v13H7V3z" />
                                </svg>
                            </div>

                            <div class="min-w-0">
                                <p class="truncate text-sm font-medium text-gray-900">
                                    {{ selectedFile.name }}
                                </p>

                                <p class="mt-1 text-xs text-gray-500">
                                    {{ fileSize }}
                                </p>
                            </div>
                        </div>

                        <button type="button" :disabled="isConverting"
                            class="shrink-0 text-sm font-medium text-gray-500 hover:text-red-600 disabled:opacity-50"
                            @click.stop="clearFile">
                            Remove
                        </button>
                    </div>
                </div>

                <!-- Error -->
                <div v-if="errorMessage"
                    class="mt-6 flex items-start gap-3 rounded-xl border border-red-200 bg-red-50 p-4">
                    <svg class="mt-0.5 h-5 w-5 shrink-0 text-red-500" fill="none" stroke="currentColor"
                        viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>

                    <p class="text-sm text-red-700">
                        {{ errorMessage }}
                    </p>
                </div>

                <!-- Success -->
                <div v-if="successMessage"
                    class="mt-6 flex items-start gap-3 rounded-xl border border-green-200 bg-green-50 p-4">
                    <svg class="mt-0.5 h-5 w-5 shrink-0 text-green-600" fill="none" stroke="currentColor"
                        viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>

                    <p class="text-sm text-green-700">
                        {{ successMessage }}
                    </p>
                </div>

                <!-- Export Options -->
                <div class="mt-8">
                    <h2 class="text-sm font-semibold text-gray-900">
                        Export as
                    </h2>

                    <div class="mt-3 grid grid-cols-1 gap-4 sm:grid-cols-2">

                        <!-- Excel -->
                        <button type="button" :disabled="!selectedFile ||
                            isConverting
                            "
                            class="group rounded-xl border border-gray-200 p-5 text-left transition hover:border-green-300 hover:bg-green-50 disabled:cursor-not-allowed disabled:opacity-50"
                            @click="convertExcel">
                            <div class="flex items-center justify-between">
                                <div class="flex items-center gap-3">
                                    <div class="flex h-11 w-11 items-center justify-center rounded-lg bg-green-100">
                                        <svg class="h-6 w-6 text-green-600" fill="none" stroke="currentColor"
                                            viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M4 5a2 2 0 012-2h8l6 6v10a2 2 0 01-2 2H6a2 2 0 01-2-2V5z" />
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M8 13h8M8 17h8" />
                                        </svg>
                                    </div>

                                    <div>
                                        <p class="font-medium text-gray-900">
                                            Excel
                                        </p>

                                        <p class="text-xs text-gray-500">
                                            XLSX
                                        </p>
                                    </div>
                                </div>

                                <span class="text-sm font-medium text-green-600">
                                    {{
                                        loadingExcel
                                            ? 'Converting...'
                                            : 'Convert'
                                    }}
                                </span>
                            </div>
                        </button>

                        <!-- Word -->
                        <button type="button" :disabled="!selectedFile ||
                            isConverting
                            "
                            class="group rounded-xl border border-gray-200 p-5 text-left transition hover:border-blue-300 hover:bg-blue-50 disabled:cursor-not-allowed disabled:opacity-50"
                            @click="convertWord">
                            <div class="flex items-center justify-between">
                                <div class="flex items-center gap-3">
                                    <div class="flex h-11 w-11 items-center justify-center rounded-lg bg-blue-100">
                                        <svg class="h-6 w-6 text-blue-600" fill="none" stroke="currentColor"
                                            viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M6 3h8l4 4v14H6V3z" />
                                            <path stroke-linecap="round" stroke-linejoin="round" d="M14 3v5h5" />
                                            <path stroke-linecap="round" stroke-linejoin="round" d="M9 13h6M9 17h6" />
                                        </svg>
                                    </div>

                                    <div>
                                        <p class="font-medium text-gray-900">
                                            Word
                                        </p>

                                        <p class="text-xs text-gray-500">
                                            DOCX
                                        </p>
                                    </div>
                                </div>

                                <span class="text-sm font-medium text-blue-600">
                                    {{
                                        loadingWord
                                            ? 'Converting...'
                                            : 'Convert'
                                    }}
                                </span>
                            </div>
                        </button>

                    </div>
                </div>

            </div>
        </div>
    </div>
</template>
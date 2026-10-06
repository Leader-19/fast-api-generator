I want you to help me build a production-quality **PDF Editor and High-Fidelity PDF Converter** inside my existing application.

## 1. Existing project

I already have a FastAPI + Vue 3 application.

Backend:

* Python
* FastAPI
* SQLAlchemy
* Alembic
* MySQL
* Pydantic
* PyMuPDF
* pdfplumber
* openpyxl
* python-docx

Frontend:

* Vue 3
* TypeScript
* Axios
* existing authentication/RBAC
* existing PDF Converter page

The existing application already has PDF conversion endpoints for:

* PDF → Excel
* PDF → Word

Do NOT rewrite the entire application.

Do NOT remove existing functionality.

First inspect the existing project structure and current PDF converter implementation, then extend/refactor it carefully.

---

# 2. Main goal

I want to build a professional **PDF Studio** feature.

The user uploads a PDF and the system analyzes the PDF structure before conversion.

The system must preserve the original PDF layout as much as technically possible.

The system should understand:

* text
* font
* font size
* bold
* italic
* underline
* text color
* text position
* text bounding box
* paragraphs
* tables
* rows
* columns
* merged cells
* images
* lines
* rectangles
* page size
* page orientation
* headers
* footers
* page numbers
* spacing
* alignment

The system should NOT simply extract plain text.

It must create an internal **Document Model** that represents the structure and layout of the PDF.

This Document Model becomes the single source of truth for:

* PDF editing
* PDF export
* Word export
* Excel export

---

# 3. Required architecture

Use a clean architecture similar to:

backend/app/

```
api/
    pdf/
        router.py
        schemas.py

services/
    pdf/
        pdf_analyzer.py
        pdf_layout_service.py
        pdf_text_service.py
        pdf_table_service.py
        pdf_image_service.py
        pdf_editor_service.py
        pdf_export_service.py
        word_export_service.py
        excel_export_service.py
        ocr_service.py

repositories/
    pdf_document_repository.py

models/
    pdf_document.py
    pdf_page.py
    pdf_element.py
    pdf_table.py

schemas/
    pdf_document.py
    pdf_element.py
    pdf_table.py

utils/
    pdf/
        coordinates.py
        fonts.py
        colors.py
```

Follow:

Router
→ Service
→ Repository
→ Database

Do not put business logic inside routers.

Use dependency injection.

Use Pydantic schemas for API requests/responses.

Use SQLAlchemy models for persistence.

---

# 4. Document Model

Create a strong internal document model.

Example:

{
"document_id": "uuid",
"filename": "report.pdf",
"page_count": 5,
"pages": [
{
"page_number": 1,
"width": 595,
"height": 842,
"rotation": 0,
"elements": [
{
"id": "uuid",
"type": "text",
"x": 100,
"y": 100,
"width": 200,
"height": 30,
"text": "ROAMING REPORT",
"font_family": "Arial",
"font_size": 18,
"bold": true,
"italic": false,
"underline": false,
"color": "#000000",
"alignment": "center"
}
]
}
]
}

Supported element types:

* text
* paragraph
* table
* image
* line
* rectangle
* shape
* header
* footer

The model must be extensible.

---

# 5. PDF analysis

When a user uploads a PDF:

POST /api/pdf/upload

Do NOT immediately convert it.

Instead:

PDF
→ Analyze
→ Extract layout
→ Detect tables
→ Detect images
→ Detect text
→ Detect fonts
→ Build Document Model
→ Return document ID

Example response:

{
"document_id": "uuid",
"filename": "report.pdf",
"pages": 10,
"status": "analyzing"
}

Then:

GET /api/pdf/{document_id}/analysis

returns:

{
"status": "completed",
"pages": 10,
"text_blocks": 182,
"tables": 25,
"images": 8,
"scanned_pages": 2
}

---

# 6. PDF types

The system must support both:

## A. Normal PDF

PDF contains real text.

Use:

* PyMuPDF
* pdfplumber

Extract:

* text
* coordinates
* fonts
* font size
* color
* blocks
* lines
* tables
* images

## B. Scanned PDF

PDF contains images instead of text.

Detect this automatically.

If a page has little/no extractable text:

PDF page
→ render image
→ OCR
→ extract text + coordinates
→ detect tables
→ add to Document Model

Create an OCR service that can later support Tesseract or another OCR engine.

Do not hard-code the entire application to one OCR provider.

---

# 7. Frontend PDF Editor

Create a professional Vue 3 PDF editor.

Route:

/pdf-editor/{documentId}

Layout:

---

## | PDF Studio                         Save     Export ▼   |

| Tools      |          PDF Canvas          | Properties |
|            |                              |            |
| Select     |       PDF PAGE              | Text       |
| Text       |                              |            |
| Table      |       ROAMING REPORT         | Font       |
| Image      |                              | Size       |
| Shape      |       TABLE                  | Bold       |
| Delete     |                              | Alignment  |
----------------------------------------------------------

## | Page 1 / 10                    Zoom - 100% +            |

Use a suitable canvas/editor architecture.

Prefer an approach that supports:

* selecting elements
* moving elements
* resizing elements
* editing text
* editing tables
* editing images
* zoom
* page navigation
* multi-page documents
* undo
* redo

Do not render the PDF as one flat image if the user needs to edit individual elements.

The original PDF should be used as the visual reference/background while the detected editable elements are represented independently.

---

# 8. Upload workflow

After uploading:

Show:

"PDF analyzed successfully"

Then show:

* file name
* page count
* text blocks
* tables
* images
* scanned pages

Provide buttons:

[Open Editor]

[Convert to Word]

[Convert to Excel]

[Export PDF]

If the user chooses Open Editor, open the PDF editor.

---

# 9. Customization popup

When the user uploads a PDF, allow a customization dialog.

Example:

Customize PDF

---

Document Information

Pages: 10
Tables: 25
Images: 8

Editing Options:

☑ Preserve original layout
☑ Preserve fonts
☑ Preserve images
☑ Preserve tables

Export mode:

○ High Fidelity
○ Editable
○ Balanced

[Cancel] [Continue]

The user can choose how much emphasis should be placed on visual similarity versus editability.

---

# 10. Text editing

When a user clicks a text element:

Show a properties panel:

Text
Font
Font size
Bold
Italic
Underline
Color
Alignment
Line height
Letter spacing
Position
Width
Height

Allow:

* edit text
* move text
* resize text box
* change font
* change size
* change color
* bold
* italic
* underline
* alignment

Save changes into the Document Model.

---

# 11. Table editing

Tables are very important.

Do not treat tables as plain text.

Represent:

Table
→ Rows
→ Cells

Each cell should support:

* value
* font
* font size
* bold
* alignment
* background
* border
* width
* height

Provide:

[Add Row]

[Delete Row]

[Add Column]

[Delete Column]

[Merge Cells]

[Split Cells]

Allow direct cell editing.

Example:

---

## | Country | Operator | Duration | Amount       |

| Thailand| AIS      | 120      | $25.50       |
| Vietnam | Viettel  | 95       | $18.30       |
------------------------------------------------

---

# 12. Image editing

Allow users to:

* select image
* move image
* resize image
* delete image
* replace image

Do not unnecessarily recompress images.

Preserve original image quality where possible.

---

# 13. PDF export

Create:

POST /api/pdf/{document_id}/export/pdf

The PDF exporter must use the Document Model.

Requirements:

* preserve page dimensions
* preserve coordinates
* preserve fonts where available
* preserve images
* preserve tables
* preserve colors
* preserve spacing
* preserve layout

If only one element changed, avoid rebuilding unrelated elements unnecessarily.

---

# 14. Word export

Create:

POST /api/pdf/{document_id}/export/word

Use python-docx.

The goal is:

PDF
→ Document Model
→ DOCX

The Word document should remain editable.

Preserve as much as possible:

* headings
* paragraphs
* fonts
* font size
* bold
* italic
* alignment
* tables
* merged cells
* images
* headers
* footers
* page breaks

Use a hybrid strategy.

For simple content:

Convert to native Word elements.

For complex PDF positioning:

Use positioned elements or an appropriate fallback strategy so that visual layout does not break badly.

Do NOT promise 100% PDF-to-Word fidelity because PDF and Word have different layout models.

Prioritize high visual fidelity while keeping important text and tables editable.

---

# 15. Excel export

Create:

POST /api/pdf/{document_id}/export/excel

Use openpyxl.

Automatically detect tables.

Convert:

PDF table
→ Excel worksheet

Preserve:

* rows
* columns
* merged cells
* borders
* font
* font size
* alignment
* background
* column width
* row height
* number formats
* formulas where appropriate

For non-table PDF content:

Put it into a reasonable worksheet layout rather than randomly extracting text.

Example:

PDF:

Country | Operator | Duration | Amount

becomes:

Excel:

A          B          C          D
Country    Operator   Duration   Amount
Thailand   AIS        120        25.50
Vietnam    Viettel    95         18.30

---

# 16. Preview before export

Add:

[Preview Word]

[Preview Excel]

[Preview PDF]

Before downloading.

The user should be able to see the expected result.

---

# 17. Conversion quality analysis

Before exporting, calculate:

* pages
* text blocks
* tables
* images
* scanned pages
* detected fonts
* unsupported elements

Show:

Conversion Quality

Word compatibility: 92%
Excel compatibility: 98%

Warnings:

⚠ 2 pages contain scanned images
⚠ 1 table has irregular columns
⚠ 3 fonts are unavailable

Do not fake percentages.

The percentage must be calculated from real analysis results.

---

# 18. Database

Create database tables for:

pdf_documents
pdf_pages
pdf_elements
pdf_tables
pdf_table_cells
pdf_images
pdf_exports

Use UUIDs.

Example:

pdf_documents:

* id
* user_id
* filename
* original_path
* page_count
* status
* metadata
* created_at
* updated_at

pdf_pages:

* id
* document_id
* page_number
* width
* height
* rotation

pdf_elements:

* id
* page_id
* type
* x
* y
* width
* height
* content
* style
* metadata

Do not store everything as one huge JSON blob if it makes querying/editing difficult.

Use JSON columns only for flexible metadata/style where appropriate.

---

# 19. File storage

For the first version use local storage.

Organize:

storage/
pdf/
originals/
previews/
exports/
temporary/

Do not load large PDFs completely into memory unnecessarily.

Use streaming uploads where appropriate.

Clean temporary files after processing.

---

# 20. Large PDF support

The application must support large PDFs.

Do not assume every PDF is 1–5 MB.

Design for:

* 100MB+
* hundreds of pages
* many images
* large tables

Avoid blocking the HTTP request for long-running operations.

For large files, create a background processing architecture that can later use:

* Celery
* Redis
* RabbitMQ

But do not introduce unnecessary infrastructure if the current project does not need it.

Design the service so background processing can be added later.

---

# 21. API design

Create clean endpoints:

POST   /api/pdf/upload
GET    /api/pdf/{id}
GET    /api/pdf/{id}/analysis
GET    /api/pdf/{id}/pages
GET    /api/pdf/{id}/elements
PUT    /api/pdf/{id}/elements/{element_id}
DELETE /api/pdf/{id}/elements/{element_id}

PUT    /api/pdf/{id}/tables/{table_id}
PUT    /api/pdf/{id}/tables/{table_id}/cells/{cell_id}

POST   /api/pdf/{id}/save

POST   /api/pdf/{id}/export/pdf
POST   /api/pdf/{id}/export/word
POST   /api/pdf/{id}/export/excel

GET    /api/pdf/{id}/exports

Follow REST principles.

---

# 22. Security

The existing authentication and permission system must be respected.

Create permissions such as:

pdf.view
pdf.upload
pdf.edit
pdf.export
pdf.delete

Users must only access their own documents unless they have the appropriate administrative permission.

Validate:

* file type
* file size
* file extension
* MIME type

Do not trust the filename extension.

Prevent path traversal.

Generate safe internal filenames.

---

# 23. Error handling

Return proper HTTP status codes.

Examples:

400
Invalid PDF

401
Unauthenticated

403
No permission

404
Document not found

413
File too large

422
Invalid conversion request

500
Unexpected conversion failure

Never expose raw Python stack traces to users.

Log detailed exceptions server-side.

---

# 24. Performance

Do not repeatedly parse the same PDF.

After analysis:

PDF
→ Document Model
→ cache/save model

Editing should modify the Document Model rather than re-reading the PDF every time.

Export should use the already analyzed model.

Use caching where useful.

---

# 25. Testing

Create tests for:

PDF upload
PDF analysis
normal PDF
scanned PDF
text extraction
table extraction
image extraction
text editing
table editing
PDF export
Word export
Excel export
large PDF
invalid PDF
permission checks

Test at least:

* simple PDF
* PDF containing tables
* PDF containing images
* complex layout
* scanned PDF

---

# 26. Important implementation rule

Do NOT immediately write all code.

First:

1. Inspect the existing project.
2. Understand the existing PDF converter.
3. Identify reusable code.
4. Identify duplicated code.
5. Propose the architecture.
6. Show which files need to be created.
7. Show which existing files need to be modified.
8. Explain database changes.
9. Explain frontend changes.
10. Then implement step-by-step.

Do not destroy working code.

Do not replace the existing PDF converter unless necessary.

---

# 27. Coding standards

Use:

* Python type hints
* Pydantic
* SQLAlchemy 2.x
* async only where actually beneficial
* service/repository pattern
* dependency injection
* clean exception handling
* structured logging
* reusable utilities
* small focused classes/functions

Avoid:

* giant router files
* giant Vue components
* duplicated conversion logic
* global mutable state
* hard-coded file paths
* hard-coded user IDs
* hard-coded permissions
* unnecessary dependencies

---

# 28. Frontend standards

Use Vue 3 Composition API.

Use TypeScript.

Create reusable components.

Recommended:

PdfEditor.vue
PdfCanvas.vue
PdfToolbar.vue
PdfPropertiesPanel.vue
PdfPageNavigation.vue
TextElement.vue
TableElement.vue
ImageElement.vue
CustomizeDialog.vue
ExportDialog.vue

Keep API calls inside services.

Example:

src/services/pdfEditor.ts

Do not put Axios requests directly everywhere inside Vue components.

---

# 29. Important UX requirement

The application should feel similar to:

* Adobe Acrobat
* Microsoft Word
* Microsoft Excel

but simpler.

The user should not need technical knowledge.

Workflow:

1. Upload PDF
2. Wait for analysis
3. Show preview
4. Click Edit
5. Modify text/table/image
6. Save
7. Choose export
8. Preview result
9. Download

---

# 30. Future AI integration

Design the architecture so AI can be added later.

Potential future features:

"Extract all tables"

"Fix formatting"

"Convert this table to Excel"

"Remove this section"

"Change company name everywhere"

"Summarize this document"

"Find all dates"

"Find all amounts"

"Detect invoice fields"

Do not implement AI now unless necessary.

But create interfaces/services that make future AI integration possible.

---

# 31. Most important technical principle

The application must NOT follow:

PDF
→ plain text
→ Word/Excel

Instead use:

PDF
→ Analyze PDF
→ Detect structure
→ Document Model
→ User edits Document Model
→ Export Document Model

This architecture is mandatory.

---

# 32. Deliverables

I want you to implement this progressively.

Phase 1:

* PDF upload
* PDF analysis
* Document Model
* text extraction
* table extraction
* image extraction

Phase 2:

* PDF editor
* text editing
* table editing
* image editing
* move/resize
* undo/redo

Phase 3:

* PDF export

Phase 4:

* Word export

Phase 5:

* Excel export

Phase 6:

* scanned PDF + OCR

Phase 7:

* quality analysis
* preview
* performance optimization

For every phase:

* show changed files
* provide complete code for new files
* provide exact modifications for existing files
* explain why the changes are needed
* provide database migrations
* provide API examples
* provide frontend integration
* provide test cases

Do not give pseudo-code when implementation is requested.

Make the implementation compatible with my existing FastAPI + Vue 3 application.

Start by inspecting my current project and PDF converter implementation before making changes.

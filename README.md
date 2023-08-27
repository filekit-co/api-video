# Video api server

FileKit API Server is a versatile tool designed to handle various file conversion and manipulation tasks. Built on top of the FastAPI framework, it offers a range of endpoints to cater to different file processing needs, from image background removal to PDF manipulations.

- webpage: https://youtubetomp3.pages.dev
- front source code: https://github.com/filekit-co/youTubetoMP3
- swagger: https://api-video-xgnu4lf2ea-uc.a.run.app/docs
- image server: https://github.com/filekit-co/api-bg-remove/tree/main
- text server: https://github.com/filekit-co/api-text/tree/main

<div align='center'>
<table width="100%" border="0">
  <tr>
    <td><img width="1724" alt="Screen Shot 2023-08-27 at 11 23 35 AM" src="https://github.com/filekit-co/api-video/assets/37536298/9f618015-b37a-4816-beff-e01045c14fc0"></td>
    <td><img width="1721" alt="Screen Shot 2023-08-27 at 11 22 53 AM" src="https://github.com/filekit-co/api-video/assets/37536298/644aa9f9-e91e-4b18-883d-187acfb02459"></td>
  </tr>
</table>
</div>

## Stack
- Video Process: [ffmpeg](https://ffmpeg.org/)
- API Server: `fastapi`
- Cloud: `Google cloud run` / `Docker`

## Init

```
$ poetry init
$ pyenv local 3.10
$ poetry env use $(pyenv which python)
$ poetry add fastapi yt_dlp 'uvicorn[standard]'
```


# Features
## Image Processing:

### Background Removal:
- `POST /bg/remove`: Remove the background from an image sent within the request.
- `GET /bg/remove`: Remove the background from an image using a provided URL.
- `POST /images/convert`: Convert images to PNG format.

## File Conversion:

### Document Conversion:
Convert between various formats like EPUB, PDF, DOC, DOCX, and XPS. Specific routes include:
- `/epub-to-doc`
- `/pdf-to-doc`
- `/xps-to-doc`
- `/epub-to-docx`
- `/pdf-to-docx`
- `/xps-to-docx`

### PDF Conversion:
Convert different formats to PDF, including EPUB, XPS, OXPS, CBZ, and FB2. Specific routes include:
- `/xps-to-pdf`
- `/epub-to-pdf`
- `/oxps-to-pdf`
- `/cbz-to-pdf`
- `/fb2-to-pdf`

## Media Downloads:
- `POST /info`: Download target URL info.
- `POST /download/audio`: Download to audio format.
- `POST /download/video`: Download to video format.

## PDF Utilities:

### Encryption & Decryption:
- `POST /pdf/encrypt`: Encrypt a PDF file.
- `POST /pdf/decrypt`: Decrypt a PDF file.

### Watermark & Logo Addition:
- `POST /pdf/add-watermark`: Add a watermark to a PDF file.
- `POST /pdf/add-logo`: Add a logo to a PDF file.

### PDF Manipulation:
- `POST /pdf/merge`: Merge multiple PDFs into one.
- `POST /pdf/split`: Split a PDF into multiple files.
- `POST /pdf/compress`: Compress a PDF file.

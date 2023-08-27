# Video api server

Stream Data to Stream Data

- webpage: https://youtubetomp3.pages.dev
- front source code: https://github.com/filekit-co/youTubetoMP3
- swagger: https://api-video-xgnu4lf2ea-uc.a.run.app/docs

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
## init

```
$ poetry init
$ pyenv local 3.10
$ poetry env use $(pyenv which python)
$ poetry add fastapi yt_dlp 'uvicorn[standard]'
```


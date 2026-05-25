import asyncio
import yt_dlp

YTDL_OPTIONS = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'quiet': True,
    'no_warnings': True,
    'source_address': '0.0.0.0'
}

async def extract_audio_info(query: str) -> dict:
    def _extract():
        with yt_dlp.YoutubeDL(YTDL_OPTIONS) as ydl:
            if not query.startswith("http"):
                info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
            else:
                info = ydl.extract_info(query, download=False)
            
            return {
                'url': info['url'],
                'title': info.get('title', 'Unknown Title'),
                'artist': info.get('uploader', 'Unknown Artist'),
                'duration': info.get('duration', 0),
                'duration_str': f"{info.get('duration', 0) // 60:02d}:{info.get('duration', 0) % 60:02d}"
            }
    
    loop = asyncio.get_event_loop()
    try:
        return await asyncio.wait_for(loop.run_in_executor(None, _extract), timeout=15.0)
    except asyncio.TimeoutError:
        raise Exception("Search took too long. YouTube might be rate-limiting.")
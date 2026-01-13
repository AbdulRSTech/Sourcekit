"""Utility helpers used by the API views for metadata extraction and downloads.

These helpers wrap `yt_dlp` calls and provide consistent return values
so the views can handle success/failure in a structured way.
"""
import os
from pathlib import Path
import yt_dlp


def main():
    """Entry point used for local testing of utilities (no-op by default)."""
    pass


def get_downloads_folder() -> str:
    """Return the default downloads directory for the current user.

    Using `pathlib.Path.home()` keeps this OS-agnostic.
    """
    return str(Path.home() / "Downloads")

def get_resource_info(url: str) -> dict:
    """
    Extract resource metadata without downloading.
    Returns aspect ratio, resolution, video quality, and audio quality.
    
    Args:
        url: Resource URL to extract information from
        
    Returns:
        dict: Contains success status, message, and metadata fields:
            - aspect_ratio: float or None
            - resolution: str (e.g., "1920x1080") or None
            - video_quality: dict with vcodec, vbr, fps or None
            - audio_quality: dict with acodec, abr, asr or None
    """
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Extract aspect ratio
            aspect_ratio = info.get('aspect_ratio')
            
            # Extract resolution
            width = info.get('width')
            height = info.get('height')
            resolution = info.get('resolution') or (f"{width}x{height}" if width and height else None)
            
            # Extract video quality information
            video_quality = info.get('vbr')
            
            # Extract audio quality information
            audio_quality = info.get('abr')
            
            return {
                "success": True,
                "message": "Resource info extracted successfully",
                "aspect_ratio": aspect_ratio,
                "resolution": resolution,
                "video_quality": video_quality,
                "audio_quality": audio_quality,
            }
            
    except Exception as e:
        return {
            "success": False,
            "message": f"Error extracting resource info: {str(e)}",
            "aspect_ratio": None,
            "resolution": None,
            "video_quality": None,
            "audio_quality": None,
        }

def download_mp4(url: str, output_filename: str) -> dict:
    """Download a resource as MP4 using `yt_dlp`.

    Returns a dictionary with `success` (bool), `message` (str) and
    `filepath` (str|None). The function writes to the user's Downloads
    folder by default and does not raise exceptions to keep view logic
    simple and centralized.
    """
    try:
        downloads_path: str = get_downloads_folder()

        base_name: str = os.path.splitext(output_filename)[0]
        output_path: str = os.path.join(downloads_path, base_name)

        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'outtmpl': f'{output_path}.%(ext)s',
            'verbose': True,
            'quiet': False,
            'no_warnings': False,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        final_path: str = f"{output_path}.mp4"
        
        return {
            "success": True,
            "message": f"{base_name} mp4 downloaded successfully!",
            "filepath": final_path
        } 
    
    except Exception as e:
        # Return an error dictionary rather than raising; callers expect this shape
        return {
            "success": False,
            "message": f"Error downloading mp4: {str(e)}",
            "filepath": None
        }

    
def download_mp3(url: str, output_filename: str) -> dict:
    """Download a resource as MP3 using `yt_dlp` and FFmpeg audio extraction.

    Returns the same shaped dictionary as `download_mp4` so callers can
    handle both formats uniformly.
    """
    try: 
        downloads_path: str = get_downloads_folder()
        base_name: str = os.path.splitext(output_filename)[0]
        output_path: str = os.path.join(downloads_path, base_name)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': f'{output_path}.%(ext)s',
            'quiet': False,
            'no_warnings': False,
        }
            
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        final_path = f"{output_path}.mp3"

        return {
            "success": True,
            "message": f"{base_name} mp3 downloaded successfully",
            "filepath": final_path
        }

    except Exception as e:
        # Consistent error shape returned for the view to act on
        return {
            "success": False,
            "message": f"Error downloading mp3: {str(e)}",
            "filepath": None
        }
    
if __name__ == "__main__":
    main()
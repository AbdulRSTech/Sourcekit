import os
from pathlib import Path
import yt_dlp

# main function used to manually run file for tests before proper testing implemented
def main():
    pass

def get_downloads_folder() -> str:
    return str(Path.home() / "Downloads")

def download_mp4(url: str, output_filename: str) -> dict:
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
        return {
            "success": False,
            "message": f"Error downloading mp4: {str(e)}",
            "filepath": None
        }

    
def download_mp3(url: str, output_filename: str) -> dict:
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
        return {
            "success": False,
            "message": f"Error downloading mp3: {str(e)}",
            "filepath": None
        }
    
if __name__ == "__main__":
    main()

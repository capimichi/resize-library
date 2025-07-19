import click
from resizelibrary.container.DefaultContainer import DefaultContainer
from resizelibrary.service.ResizeService import ResizeService

@click.command(
    name='resize:folder'
)
@click.argument('folder_path', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('--allowed-extensions', default=['mov', 'mp4', 'mkv', 'avi'], multiple=True, help='Allowed file extensions (default: mov, mp4, mkv, avi). Example: --allowed-extensions mp4 --allowed-extensions mkv')
@click.option('--video-encoding', default='libx264', help='Video encoding format (default: libx264). Example: --video-encoding libx265')
@click.option('--audio-encoding', default='aac', help='Audio encoding format (default: aac). Example: --audio-encoding mp3')
@click.option('--audio-bitrate', default='128k', help='Audio bitrate (default: 128k). Example: --audio-bitrate 192k')
@click.option('--speed-profile', default='slow', help='Encoding speed profile (default: slow). Example: --speed-profile medium')
@click.option('--video-profile', default='yuv420p', help='Video profile (default: yuv420p). Example: --video-profile yuv444p')
@click.option('--max-height', default=1080, type=int, help='Maximum height for resize (default: 1080). Example: --max-height 720')
@click.option('--crf', default=22, type=int, help='CRF value for encoding (default: 22). Example: --crf 18')
@click.option('--output-format', default='mkv', help='Output container format (default: mkv). Example: --output-format mp4')
def resize_folder_command(folder_path, allowed_extensions, video_encoding, audio_encoding, audio_bitrate, speed_profile, video_profile, max_height, crf, output_format):
    default_container: DefaultContainer = DefaultContainer.getInstance()
    resize_service: ResizeService = default_container.get(ResizeService)
    
    resize_service.resize_folder(
        folder_path=folder_path, 
        allowed_extensions=allowed_extensions,
        video_encoding=video_encoding,
        audio_encoding=audio_encoding,
        audio_bitrate=audio_bitrate,
        speed_profile=speed_profile,
        video_profile=video_profile,
        max_height=max_height,
        crf=crf,
        output_format=output_format
    )


import click
from resizelibrary.container.DefaultContainer import DefaultContainer
from resizelibrary.service.ResizeService import ResizeService

@click.command(
    name='resize:file'
)
@click.argument('file_path', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option('--video-encoding', default='libx264', help='Video encoding format (default: libx264). Example: --video-encoding libx265')
@click.option('--audio-encoding', default='aac', help='Audio encoding format (default: aac). Example: --audio-encoding mp3')
@click.option('--audio-bitrate', default='128k', help='Audio bitrate (default: 128k). Example: --audio-bitrate 192k')
@click.option('--speed-profile', default='slow', help='Encoding speed profile (default: slow). Example: --speed-profile medium')
@click.option('--video-profile', default='yuv420p', help='Video profile (default: yuv420p). Example: --video-profile yuv444p')
@click.option('--max-height', default=1080, type=int, help='Maximum height for resize (default: 1080). Example: --max-height 720')
@click.option('--crf', default=22, type=int, help='CRF value for encoding (default: 22). Example: --crf 18')
@click.option('--output-format', default='mkv', help='Output container format (default: mkv). Example: --output-format mp4')
def resize_file_command(file_path, video_encoding, audio_encoding, audio_bitrate, speed_profile, video_profile, max_height, crf, output_format):
    default_container: DefaultContainer = DefaultContainer.getInstance()
    resize_service: ResizeService = default_container.get(ResizeService)
    
    resize_service.resize_file(
        file_path=file_path,
        video_encoding=video_encoding,
        audio_encoding=audio_encoding,
        audio_bitrate=audio_bitrate,
        speed_profile=speed_profile,
        video_profile=video_profile,
        max_height=max_height,
        crf=crf,
        output_format=output_format
    )

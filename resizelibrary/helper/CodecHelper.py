class CodecHelper:
    
    @staticmethod
    def map_codec_name(mediainfo_codec: str) -> str:
        """
        Map MediaInfo codec names to ffmpeg codec names
        """
        codec_mapping = {
            'AVC': 'libx264',
            'H.264': 'libx264',
            'HEVC': 'libx265',
            'H.265': 'libx265',
            'VP8': 'libvpx',
            'VP9': 'libvpx-vp9',
            'AAC': 'aac',
            'AC-3': 'ac3',
            'E-AC-3': 'eac3',
            'DTS': 'dts',
            'MP3': 'mp3',
            'FLAC': 'flac',
            'Vorbis': 'libvorbis',
            'Opus': 'libopus'
        }
        return codec_mapping.get(mediainfo_codec, mediainfo_codec.lower())

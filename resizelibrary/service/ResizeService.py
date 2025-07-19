from injector import inject
import os
from pathlib import Path
import logging
from pymediainfo import MediaInfo, Track
from typing import List
import shlex
import tempfile
import subprocess
import shutil
from apprise import Apprise
from resizelibrary.model.Profile import Profile
from resizelibrary.helper.CodecHelper import CodecHelper
from pydantic_yaml import parse_yaml_raw_as

class ResizeService:

    @inject
    def __init__(self,
        apprise: Apprise):
        self.apprise = apprise

    def resize_folder(self, 
                     folder_path, 
                     allowed_extensions=['mov', 'mp4', 'mkv', 'avi'], 
                     video_encoding='libx264', 
                     audio_encoding='aac', 
                     audio_bitrate='128k',
                     speed_profile='slow', 
                     video_profile='yuv420p',
                     max_height=1080, 
                     crf=22,
                     output_format='mkv'):
        """
        Resize all video files in the specified folder.
        :param folder_path: Path to the folder containing video files.
        :param allowed_extensions: List of allowed file extensions.
        :param video_encoding: Video encoding format.
        :param audio_encoding: Audio encoding format.
        :param speed_profile: Encoding speed profile.
        :param max_height: Maximum height for resize.
        :param crf: CRF value for encoding.
        """
        # Find all files in the folder with allowed extensions recursively
        folder = Path(folder_path)
        video_files = list(folder.rglob('*.*'))
        video_files = [f for f in video_files if f.suffix[1:].lower() in allowed_extensions]
        if not video_files:
            logging.info(f"No video files found in {folder_path} with allowed extensions: {allowed_extensions}")
            return
        
        logging.info(f"Found {len(video_files)} video files in {folder_path} with allowed extensions: {allowed_extensions}")

        # Sort alfabetically
        video_files.sort(key=lambda x: x.name)

        for video_file in video_files:
            self.resize_file(video_file, video_encoding, audio_encoding, audio_bitrate, speed_profile, video_profile, max_height, crf, output_format)

    def resize_file(self, 
                   file_path, 
                   video_encoding='libx264', 
                   audio_encoding='aac', 
                   audio_bitrate='128k',
                   speed_profile='slow', 
                   video_profile='yuv420p',
                   max_height=1080, 
                   crf=22,
                   output_format='mkv'):
        
        logging.info(f"Resizing file: {file_path}")

        # Let's check if the file exists
        if not os.path.exists(file_path):
            logging.error(f"File {file_path} does not exist.")
            return
        
        media_info = MediaInfo.parse(file_path)
        tracks: List[Track] = media_info.tracks

        video_track = None
        audio_tracks = []
        text_tracks = []

        for track in tracks:
            if track.track_type == 'Video':
                video_track = track

            if (track.track_type == 'Audio'):
                audio_tracks.append(track)
            
            if (track.track_type == 'Text'):
                text_tracks.append(track)

        if not video_track:
            logging.error(f"No video track found in {file_path}. Skipping resize.")
            return
        
        video_encodinc_check = video_track.format and CodecHelper.map_codec_name(video_track.format) == video_encoding.lower()
        logging.info(f"Video encoding: {video_track.format if video_track else 'None'}")
        logging.info(f"Video encoding check: {video_encodinc_check}")
        
        audio_encodinc_check = True
        for audio_track in audio_tracks:
            if audio_track.format and audio_encoding.lower() != audio_track.format.lower():
                audio_encodinc_check = False
                break
        
        logging.info(f"Audio encoding: {', '.join([track.format for track in audio_tracks]) if audio_tracks else 'None'}")
        logging.info(f"Audio encoding check: {audio_encodinc_check}")

        video_size_check = video_track.height and video_track.height <= max_height
        logging.info(f"Video height: {video_track.height if video_track else 'None'}")
        logging.info(f"Video size check: {video_size_check}")

        extension_check = Path(file_path).suffix[1:].lower() == output_format.lower()
        logging.info(f"File extension: {Path(file_path).suffix[1:].lower()}")
        logging.info(f"Output format check: {extension_check}")

        if (video_encodinc_check 
            and audio_encodinc_check
            and video_size_check 
            and extension_check):
            logging.info(f"File {file_path} already meets the target specifications. Skipping resize.")
            return


        temp_path = tempfile.mktemp(suffix=f".{output_format}")
        output_path = Path(file_path).with_suffix(f".{output_format}")

        # filter out invalid text tracks
        if output_format.lower() == 'mkv':
            allowed_track_foramt = [
                "SubRip",     # .srt
                "UTF-8",      # raw text
                "ASS",        # Advanced SubStation Alpha
                "SSA",        # SubStation Alpha
                "PGS",        # Presentation Graphic Stream (BD)
                "HDMV PGS",   # Blu-ray PGS
                "VobSub",     # DVD Subtitles
                "WebVTT"      # Web Video Text Tracks
            ]
            parsed_text_tracks = [track for track in text_tracks if track.format in allowed_track_foramt]
        elif output_format.lower() == 'mp4':
            allowed_track_foramt = [
                "SubRip",     # .srt
                "UTF-8",      # raw text
                "WebVTT"      # Web Video Text Tracks
            ]
            parsed_text_tracks = [track for track in text_tracks if track.format in allowed_track_foramt]

        logging.info(f"Keep text tracks: {len(parsed_text_tracks)} of {len(text_tracks)}")
        text_tracks = parsed_text_tracks
        
        # Here you would call the actual resizing logic, e.g., using ffmpeg
        logging.info(f"Resizing file {file_path} with the following parameters:")
        logging.info(f"Video Encoding: {video_encoding}")
        logging.info(f"Audio Encoding: {audio_encoding}")
        logging.info(f"Audio Bitrate: {audio_bitrate}")
        logging.info(f"Speed Profile: {speed_profile}")
        logging.info(f"Video Profile: {video_profile}")
        logging.info(f"Max Height: {max_height}")
        logging.info(f"CRF: {crf}")
        logging.info(f"Output Format: {output_format}")
        logging.info(f"Output Path: {output_path}")

        command = [
            'ffmpeg',
            '-i', shlex.quote(str(file_path)),
        ]

        command += [
            '-c:v', video_encoding,
            '-preset', speed_profile,
            '-crf', str(crf),
            '-pix_fmt', video_profile,
        ]

        # Only add scale filter if video height exceeds max_height
        if video_track and video_track.height and video_track.height > max_height:
            command += ['-vf', f'scale=-2:{max_height}']

        command += [
            '-map', '0:v:0',  # Map the first video track
        ]

        command += [
            '-c:a', audio_encoding,
            '-b:a', audio_bitrate,
        ]

        # Map all audio tracks
        for audio_track in audio_tracks:
            command += [
                '-map', f'0:{audio_track.track_id - 1}',  # Map each audio track (track_id is 1-based, map is 0-based)
            ]

        # Add text tracks if any
        for text_track in text_tracks:
            command += [
                '-c:s', 'copy',  # Copy subtitle track without re-encoding
                '-map', f'0:{text_track.track_id - 1}',  # Map the text track (track_id is 1-based, map is 0-based)
            ]
        
        command += [
            shlex.quote(str(temp_path))
        ]

        file_name = Path(file_path).name
        self.apprise.notify(
            body=f"Resizing start: {file_name}",
            notify_type="info"
        )

        command_str = ' '.join(command)

        # run
        result = subprocess.run(command_str, shell=True, check=True)
        
        logging.info(f"Resize command result: {result}")

        if result.returncode == 0:
            logging.info(f"Resize completed successfully for {file_path}. Output saved to {temp_path}")
            shutil.move(temp_path, output_path)

            # if output path != file_path, remove the original file
            if output_path != file_path and os.path.exists(file_path):
                logging.info(f"Removing original file {file_path}")
                os.remove(file_path)

            self.apprise.notify(
                body=f"Resizing completed: {file_name}",
                notify_type="success"
            )
        else:
            logging.error(f"Resize failed for {file_path}. Command: {command_str}")
            self.apprise.notify(
                body=f"Resizing failed: {file_name}",
                notify_type="error"
            )

    def resize_with_profile(self, profile_path: str):
        """
        Resize folder using a profile configuration file.
        :param profile_path: Path to the YAML profile file.
        """
        try:
            with open(profile_path, 'r') as f:
                yaml_content = f.read()
            
            profile = parse_yaml_raw_as(Profile, yaml_content)
            logging.info(f"Loaded profile from {profile_path}")
            
            self.resize_folder(
                folder_path=profile.folder,
                allowed_extensions=profile.allowed_extensions,
                video_encoding=profile.video_encoding,
                audio_encoding=profile.audio_encoding,
                audio_bitrate=profile.audio_bitrate,
                speed_profile=profile.speed_profile,
                video_profile=profile.video_profile,
                max_height=profile.max_height,
                crf=profile.crf,
                output_format=profile.output_format
            )
        except Exception as e:
            logging.error(f"Failed to process profile {profile_path}: {e}")
            raise
        try:
            with open(profile_path, 'r') as f:
                yaml_content = f.read()
            
            profile = parse_yaml_raw_as(Profile, yaml_content)
            logging.info(f"Loaded profile from {profile_path}")
            
            self.resize_folder(
                folder_path=profile.folder,
                allowed_extensions=profile.allowed_extensions,
                video_encoding=profile.video_encoding,
                audio_encoding=profile.audio_encoding,
                audio_bitrate=profile.audio_bitrate,
                speed_profile=profile.speed_profile,
                video_profile=profile.video_profile,
                max_height=profile.max_height,
                crf=profile.crf,
                output_format=profile.output_format
            )
        except Exception as e:
            logging.error(f"Failed to process profile {profile_path}: {e}")
            raise


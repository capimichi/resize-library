# Resize Library

A Python CLI tool for resizing video files using FFmpeg with customizable encoding parameters.

## Installation

```bash
pip install -e .
```

## Commands

### 1. resize:file - Resize a Single File

Resize a single video file with custom encoding parameters.

```bash
resize:file <file_path> [OPTIONS]
```

**Arguments:**
- `file_path`: Path to the video file to resize (required)

**Options:**
- `--video-encoding`: Video encoding format (default: libx264)
- `--audio-encoding`: Audio encoding format (default: aac)
- `--audio-bitrate`: Audio bitrate (default: 128k)
- `--speed-profile`: Encoding speed profile (default: slow)
- `--video-profile`: Video profile (default: yuv420p)
- `--max-height`: Maximum height for resize (default: 1080)
- `--crf`: CRF value for encoding (default: 22)
- `--output-format`: Output container format (default: mkv)

**Example:**
```bash
resize:file /path/to/video.mp4 --max-height 720 --crf 20 --output-format mp4
```

### 2. resize:folder - Resize All Files in a Folder

Resize all video files in a folder that match the allowed extensions.

```bash
resize:folder <folder_path> [OPTIONS]
```

**Arguments:**
- `folder_path`: Path to the folder containing video files (required)

**Options:**
- `--allowed-extensions`: Allowed file extensions (default: mov, mp4, mkv, avi)
- `--video-encoding`: Video encoding format (default: libx264)
- `--audio-encoding`: Audio encoding format (default: aac)
- `--audio-bitrate`: Audio bitrate (default: 128k)
- `--speed-profile`: Encoding speed profile (default: slow)
- `--video-profile`: Video profile (default: yuv420p)
- `--max-height`: Maximum height for resize (default: 1080)
- `--crf`: CRF value for encoding (default: 22)
- `--output-format`: Output container format (default: mkv)

**Example:**
```bash
resize:folder /path/to/videos --allowed-extensions mp4 mkv --max-height 720 --crf 18
```

### 3. resize:profile - Resize Using a Profile

Resize videos using a predefined profile configuration stored in a JSON file.

```bash
resize:profile <profile_path>
```

**Arguments:**
- `profile_path`: Path to the JSON profile configuration file (required)

**Example:**
```bash
resize:profile /path/to/profile.json
```

## Profile Configuration

The profile feature allows you to store all your encoding preferences in a JSON file for easy reuse and sharing.

### Profile Structure

Create a JSON file with the following structure:

```json
{
  "folder": "/path/to/videos",
  "allowed_extensions": ["mov", "mp4", "mkv", "avi"],
  "video_encoding": "libx264",
  "audio_encoding": "aac",
  "audio_bitrate": "128k",
  "speed_profile": "slow",
  "video_profile": "yuv420p",
  "max_height": 1080,
  "crf": 22,
  "output_format": "mkv"
}
```

### Profile Parameters

- `folder` (required): Path to the folder containing media files to be resized
- `allowed_extensions`: List of allowed file extensions (default: ["mov", "mp4", "mkv", "avi"])
- `video_encoding`: Video encoding format (default: "libx264")
- `audio_encoding`: Audio encoding format (default: "aac")
- `audio_bitrate`: Audio bitrate (default: "128k")
- `speed_profile`: Encoding speed profile (default: "slow")
- `video_profile`: Video profile (default: "yuv420p")
- `max_height`: Maximum height for resize (default: 1080)
- `crf`: CRF value for encoding (default: 22)
- `output_format`: Output container format (default: "mkv")

### Example Profile Configurations

**High Quality Profile (high-quality.json):**
```json
{
  "folder": "/path/to/videos",
  "allowed_extensions": ["mov", "mp4", "mkv", "avi"],
  "video_encoding": "libx264",
  "audio_encoding": "aac",
  "audio_bitrate": "320k",
  "speed_profile": "slower",
  "video_profile": "yuv420p",
  "max_height": 1080,
  "crf": 18,
  "output_format": "mkv"
}
```

**Fast Encoding Profile (fast.json):**
```json
{
  "folder": "/path/to/videos",
  "allowed_extensions": ["mp4", "mkv"],
  "video_encoding": "libx264",
  "audio_encoding": "aac",
  "audio_bitrate": "128k",
  "speed_profile": "fast",
  "video_profile": "yuv420p",
  "max_height": 720,
  "crf": 25,
  "output_format": "mp4"
}
```

**Mobile Optimized Profile (mobile.json):**
```json
{
  "folder": "/path/to/videos",
  "allowed_extensions": ["mov", "mp4", "mkv", "avi"],
  "video_encoding": "libx264",
  "audio_encoding": "aac",
  "audio_bitrate": "96k",
  "speed_profile": "medium",
  "video_profile": "yuv420p",
  "max_height": 480,
  "crf": 28,
  "output_format": "mp4"
}
```

## Parameter Details

### Video Encoding Options
- `libx264`: Most compatible H.264 encoder
- `libx265`: More efficient H.265 encoder (smaller files)
- `libvpx-vp9`: VP9 encoder for WebM format

### Audio Encoding Options
- `aac`: Advanced Audio Coding (recommended)
- `mp3`: MP3 audio encoding
- `opus`: Opus audio encoding (efficient)

### Speed Profile Options
- `ultrafast`: Fastest encoding, largest file size
- `superfast`: Very fast encoding
- `veryfast`: Fast encoding
- `faster`: Faster than medium
- `fast`: Fast encoding
- `medium`: Default speed
- `slow`: Slower but better quality (recommended)
- `slower`: Very slow but highest quality
- `veryslow`: Slowest but best quality

### CRF (Constant Rate Factor) Values
- `0`: Lossless
- `17-18`: Visually lossless
- `20-24`: High quality (recommended range)
- `25-28`: Medium quality
- `29+`: Low quality

Lower CRF values result in better quality but larger file sizes.

## Requirements

- Python 3.7+
- FFmpeg installed and available in PATH
- Required Python packages (install via pip)

## Usage Tips

1. Use profiles for consistent encoding across projects
2. Test with a small sample before processing large batches
3. Monitor CPU usage during encoding
4. Consider using faster presets for quick previews
5. Use slower presets for final production outputs
# Resize Library

A Python library for resizing video files with customizable encoding parameters.

## Commands

### resize:folder

Resizes all video files in a specified folder recursively.

**Usage:**
```bash
python -m resizelibrary resize:folder /path/to/folder [OPTIONS]
```

**Arguments:**
- `folder_path`: Path to the folder containing video files (required)

**Options:**
- `--allowed-extensions`: File extensions to process (default: mov, mp4, mkv, avi)
- `--video-encoding`: Video codec to use (default: libx264)
- `--audio-encoding`: Audio codec to use (default: aac)
- `--audio-bitrate`: Audio bitrate (default: 128k)
- `--speed-profile`: Encoding speed preset (default: slow)
- `--profile`: Video pixel format profile (default: yuv420p)
- `--max-height`: Maximum video height in pixels (default: 1080)
- `--crf`: Constant Rate Factor for quality control (default: 22)
- `--output-format`: Output container format (default: mkv)

## Option Details

### Video Encoding (`--video-encoding`)
**Accepted values:** libx264, libx265, libvpx-vp9, av1, etc.
- `libx264`: H.264 codec, widely compatible, good compression
- `libx265`: H.265/HEVC codec, better compression than H.264, requires more processing power
- `libvpx-vp9`: VP9 codec, open-source alternative to H.265
- `av1`: AV1 codec, next-generation codec with excellent compression

### Audio Encoding (`--audio-encoding`)
**Accepted values:** aac, mp3, opus, flac, etc.
- `aac`: Advanced Audio Coding, good quality and compatibility
- `mp3`: MP3 codec, universal compatibility but lower quality
- `opus`: Modern codec with excellent quality at low bitrates
- `flac`: Lossless compression, larger file sizes

### Audio Bitrate (`--audio-bitrate`)
**Accepted values:** 64k, 128k, 192k, 256k, 320k, etc.
- `64k`: Low quality, suitable for voice content
- `128k`: Standard quality for most content
- `192k`: Good quality for music and mixed content
- `256k`: High quality
- `320k`: Very high quality, diminishing returns

### Speed Profile (`--speed-profile`)
**Accepted values:** ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow
- `ultrafast`: Fastest encoding, largest file size
- `fast`: Good balance of speed and compression
- `medium`: Default balance
- `slow`: Better compression, slower encoding
- `veryslow`: Best compression, very slow encoding

### Profile (`--profile`)
**Accepted values:** yuv420p, yuv422p, yuv444p, etc.
- `yuv420p`: Most compatible, standard for web and devices
- `yuv422p`: Higher chroma resolution, used in professional video
- `yuv444p`: Full chroma resolution, largest file sizes

### CRF (Constant Rate Factor) (`--crf`)
**Accepted values:** 0-51 (lower = better quality)
- `0`: Lossless (huge file sizes)
- `18`: Visually lossless
- `22`: Default, good quality
- `28`: Acceptable quality for most content
- `51`: Lowest quality, smallest file size

### Output Format (`--output-format`)
**Accepted values:** mkv, mp4, avi, mov, etc.
- `mkv`: Matroska, supports all codecs and subtitle formats
- `mp4`: Most compatible, limited subtitle support
- `avi`: Legacy format, limited codec support
- `mov`: QuickTime format, good for professional workflows

## Examples

Basic usage:
```bash
python -m resizelibrary resize:folder /path/to/videos
```

High quality encoding:
```bash
python -m resizelibrary resize:folder /path/to/videos --crf 18 --speed-profile slow --audio-bitrate 256k
```

Fast encoding for preview:
```bash
python -m resizelibrary resize:folder /path/to/videos --speed-profile fast --crf 28 --audio-bitrate 96k
```

4K to 1080p conversion:
```bash
python -m resizelibrary resize:folder /path/to/videos --max-height 1080 --video-encoding libx265 --crf 20
```

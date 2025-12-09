import pygame
import os
import struct
import io

try:
    from mutagen.id3 import ID3
    from mutagen import File as MutagenFile
except ImportError:
    ID3 = None
    MutagenFile = None

def get_mp3_metadata(file_path):
    """Extract metadata from an MP3 file using mutagen."""
    if ID3 is None or MutagenFile is None:
        raise ImportError("mutagen library is required to extract MP3 metadata.")
    
    audio = MutagenFile(file_path)
    if audio is None:
        return {}

    metadata = {}
    if audio.tags is not None:
        for tag in audio.tags.keys():
            metadata[tag] = str(audio.tags[tag])
    
    return metadata

def load_sound(file_path):
    """Load a sound file and return a pygame Sound object."""
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Sound file not found: {file_path}")
    
    return pygame.mixer.Sound(file_path)

def get_wav_metadata(file_path):
    """Extract metadata from a WAV file."""
    metadata = {}
    try:
        with open(file_path, 'rb') as f:
            riff = f.read(12)
            if riff[0:4] != b'RIFF' or riff[8:12] != b'WAVE':
                return metadata  # Not a valid WAV file

            while True:
                chunk_header = f.read(8)
                if len(chunk_header) < 8:
                    break
                chunk_id, chunk_size = struct.unpack('<4sI', chunk_header)
                if chunk_id == b'LIST':
                    list_type = f.read(4)
                    if list_type == b'INFO':
                        info_data = f.read(chunk_size - 4)
                        info_stream = io.BytesIO(info_data)
                        while info_stream.tell() < len(info_data):
                            subchunk_id = info_stream.read(4)
                            subchunk_size_data = info_stream.read(4)
                            if len(subchunk_size_data) < 4:
                                break
                            subchunk_size = struct.unpack('<I', subchunk_size_data)[0]
                            subchunk_data = info_stream.read(subchunk_size)
                            metadata[subchunk_id.decode('ascii').strip()] = subchunk_data.decode('ascii').strip('\x00')
                else:
                    f.seek(chunk_size, os.SEEK_CUR)
    except Exception as e:
        print(f"Error reading WAV metadata: {e}")
    
    return metadata
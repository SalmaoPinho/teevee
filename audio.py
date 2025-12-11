
import pygame
import os,io
import struct
import random
from config import getVars,setVars

try:
    from mutagen.id3 import ID3
    from mutagen import File as MutagenFile
except ImportError:
    ID3 = None
    MutagenFile = None


sounds = {
    'click': 'assets/sounds/click.mp3',
    'talk': 'assets/sounds/talk.mp3',
    'cancel': 'assets/sounds/cancel.mp3',
}
class MusicPlayer:
    def __init__(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        self.current_track = None
        self.is_playing = False
        self.volume = getVars('volume') 
        self.percent_position = 0.0
        self.loop = False
        self.artist = "Unknown"
        self.album = "Unknown"
        self.title = "Unknown"
        self.cover_art = None
        self.metadata = {}
        self.queue = [
            fname for fname in os.listdir("assets/music/") if fname.lower().endswith(('.mp3', '.m4a', '.wav'))
        ]
        self.load_track(self.queue[1])
    def skip_music(self,dir=1):
        current_index = self.queue.index(self.current_track)
        next_index = (current_index + dir) % len(self.queue)
        self.load_track(self.queue[next_index])
        self.play()
    def play(self):
        if self.current_track:
            pygame.mixer.music.set_volume(self.volume/10)
            pygame.mixer.music.play(-1 if self.loop else 0)
            self.is_playing = True
    def pause(self):
        pygame.mixer.music.pause()
        self.is_playing = False
    def load_track(self, track_name):
        track_file = f"assets/music/{track_name}"
        if not os.path.isfile(track_file):
            print(f"Arquivo de música não encontrado: {track_name}")
            return False
        pygame.mixer.music.load(track_file)
        self.current_track = track_name
        self.metadata=MetadataExtractor().extract(track_file)
        self.artist=self.metadata.get('artist', "Unknown")
        self.album=self.metadata.get('album', "Unknown")
        self.title=self.metadata.get('title', "Unknown")
        return True
    def play_sound(self, sound):
        """Toca um arquivo de som"""
        if not os.path.isfile(sounds[sound]):
            print(f"Arquivo de som não encontrado: {sounds[sound]}")
            return
        sound = pygame.mixer.Sound(sounds[sound])
        sound.set_volume(self.volume/10)
        sound.play()
    def get_progress(self):
        """Retorna o progresso atual da música em porcentagem"""
        if not self.current_track:
            return 0.0
        pos_ms = pygame.mixer.music.get_pos()
        try:
            from mutagen.mp3 import MP3
            audio = MP3(f"assets/music/{self.current_track}")
            length_ms = int(audio.info.length * 1000)
            if length_ms > 0:
                return min(max(pos_ms / length_ms, 0.0), 1.0) * 100.0
        except Exception as e:
            print(f"Erro ao obter progresso da música: {e}")
        return 0.0
    def volume_change(self,increment):
        self.volume = (getVars('volume') + increment)%11
        setVars('volume', self.volume)
        pygame.mixer.music.set_volume(self.volume/10) 
    def randomize_queue(self):
        print("Embaralhando fila de músicas")
        random.shuffle(self.queue)
    
class MetadataExtractor:
    """Extrai metadados e arte de capa para arquivos de áudio suportados."""

    def extract(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.m4a':
            return self.extract_metadata_from_m4a(file_path)
        if ext == '.mp3':
            return self.extract_metadata_from_mp3(file_path)
        if ext == '.wav':
            return self.extract_metadata_from_wav(file_path)
        return {'art': None, 'artist': "Unknown", 'album': "Unknown", 'title': os.path.basename(file_path)}

    def extract_metadata_from_m4a(self, file_path):
        metadata = {'art': None, 'artist': "Unknown", 'album': "Unknown", 'title': os.path.basename(file_path)}
        try:
            with open(file_path, 'rb') as f:
                self._parse_atoms(f, os.path.getsize(file_path), metadata)
        except Exception as e:
            print(f"Error extracting m4a metadata: {e}")
        return metadata

    def extract_metadata_from_mp3(self, file_path):
        metadata = {
            'art': None,
            'artist': "Unknown",
            'album': "Unknown",
            'title': os.path.basename(file_path),
        }

        if ID3 is None:
            metadata['notice'] = "Install mutagen for mp3 metadata"
            return metadata

        try:
            tags = ID3(file_path)
            self._apply_id3_tags(tags, metadata)
        except Exception as e:
            print(f"Error reading ID3 tags: {e}")
        return metadata

    def extract_metadata_from_wav(self, file_path):
        metadata = {
            'art': None,
            'artist': "Unknown",
            'album': "Unknown",
            'title': os.path.basename(file_path),
        }

        if MutagenFile is not None:
            try:
                audio = MutagenFile(file_path)
                tags = getattr(audio, 'tags', None)
                if tags:
                    if ID3 and isinstance(tags, ID3):
                        self._apply_id3_tags(tags, metadata)
                    else:
                        def _pick(keys):
                            for k in keys:
                                if k in tags:
                                    val = tags[k]
                                    if isinstance(val, list) and val:
                                        return str(val[0])
                                    if not isinstance(val, list):
                                        return str(val)
                            return None

                        metadata['artist'] = _pick(['IART', 'artist']) or metadata['artist']
                        metadata['album'] = _pick(['IPRD', 'album', 'IALB']) or metadata['album']
                        metadata['title'] = _pick(['INAM', 'title']) or metadata['title']
            except Exception as e:
                print(f"Error reading WAV via mutagen: {e}")
        else:
            metadata['notice'] = "Install mutagen for wav metadata"

        # Parsing manual de RIFF para INFO e ID3 embutido
        try:
            with open(file_path, 'rb') as f:
                header = f.read(12)
                if len(header) < 12 or header[0:4] != b'RIFF' or header[8:12] != b'WAVE':
                    return metadata

                while True:
                    chunk_header = f.read(8)
                    if len(chunk_header) < 8:
                        break
                    chunk_id = chunk_header[0:4]
                    chunk_size = struct.unpack('<I', chunk_header[4:])[0]
                    if chunk_size < 0:
                        break

                    if chunk_id == b'LIST' and chunk_size >= 4:
                        list_type = f.read(4)
                        remaining = chunk_size - 4
                        if list_type == b'INFO':
                            info_data = f.read(remaining)
                            idx = 0
                            while idx + 8 <= len(info_data):
                                sub_id = info_data[idx:idx+4]
                                sub_size = struct.unpack('<I', info_data[idx+4:idx+8])[0]
                                sub_data = info_data[idx+8:idx+8+sub_size]
                                text = sub_data.rstrip(b'\x00').decode('utf-8', 'ignore')

                                if sub_id == b'IART' and text:
                                    metadata['artist'] = text
                                elif sub_id == b'INAM' and text:
                                    metadata['title'] = text
                                elif sub_id in (b'IPRD', b'IALB') and text:
                                    metadata['album'] = text

                                idx += 8 + sub_size
                                if sub_size % 2 == 1:
                                    idx += 1
                        else:
                            f.seek(remaining, 1)

                    elif chunk_id.lower() == b'id3 ':
                        id3_bytes = f.read(chunk_size)
                        if ID3 is not None:
                            try:
                                id3 = ID3(io.BytesIO(id3_bytes))
                                self._apply_id3_tags(id3, metadata)
                            except Exception as e:
                                print(f"Error parsing embedded ID3 in WAV: {e}")
                        else:
                            metadata.setdefault('notice', "Install mutagen for wav metadata")

                    else:
                        f.seek(chunk_size, 1)

                    if chunk_size % 2 == 1:
                        f.seek(1, 1)

        except Exception as e:
            print(f"Error parsing WAV manually: {e}")

        return metadata

    def _parse_atoms(self, f, end_pos, metadata):
        while f.tell() < end_pos:
            try:
                header = f.read(8)
                if len(header) < 8:
                    break

                atom_size, atom_type = struct.unpack('>I4s', header)
                try:
                    atom_type_str = atom_type.decode('utf-8', 'ignore')
                except Exception:
                    atom_type_str = "????"

                if atom_size == 1:
                    atom_size = struct.unpack('>Q', f.read(8))[0]
                    content_size = atom_size - 16
                else:
                    content_size = atom_size - 8

                if atom_size == 0:
                    content_size = end_pos - f.tell()

                if atom_type_str in ['moov', 'trak', 'mdia', 'minf', 'stbl', 'udta', 'ilst']:
                    continue
                elif atom_type_str == 'meta':
                    f.read(4)
                    continue

                is_data_atom = False
                target_key = None

                if atom_type == b'\xa9ART':
                    target_key = 'artist'
                    is_data_atom = True
                elif atom_type == b'\xa9alb':
                    target_key = 'album'
                    is_data_atom = True
                elif atom_type == b'\xa9nam':
                    target_key = 'title'
                    is_data_atom = True
                elif atom_type_str == 'covr':
                    target_key = 'art'
                    is_data_atom = True

                if is_data_atom:
                    current_pos = f.tell()
                    atom_end = current_pos + content_size

                    while f.tell() < atom_end:
                        d_header = f.read(8)
                        if len(d_header) < 8:
                            break
                        d_size, d_type = struct.unpack('>I4s', d_header)

                        if d_type == b'data':
                            f.read(8)
                            data_len = d_size - 16
                            data_content = f.read(data_len)

                            if target_key == 'art':
                                metadata['art'] = data_content
                            else:
                                try:
                                    metadata[target_key] = data_content.decode('utf-8', 'ignore')
                                except Exception:
                                    pass
                            break
                        else:
                            f.seek(d_size - 8, 1)

                    f.seek(atom_end)
                    continue

                f.seek(content_size, 1)

            except struct.error:
                break

    def _apply_id3_tags(self, tags, metadata):
        if tags is None:
            return

        def _first_text(frame_id):
            frame = tags.get(frame_id)
            if frame and getattr(frame, 'text', None):
                return str(frame.text[0])
            return None

        metadata['artist'] = _first_text('TPE1') or metadata.get('artist', 'Unknown')
        metadata['album'] = _first_text('TALB') or metadata.get('album', 'Unknown')
        metadata['title'] = _first_text('TIT2') or metadata.get('title', 'Unknown')

        for frame in tags.values():
            if getattr(frame, 'FrameID', '') == 'APIC' and getattr(frame, 'data', None):
                metadata['art'] = frame.data
                break

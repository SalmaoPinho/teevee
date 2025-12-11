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


SUPPORTED_EXT = ('.m4a', '.mp3', '.wav', '.ogg')


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


class PlaybackController:
    """Reprodução de áudio e tratamento de metadados sem preocupações de UI."""

    def __init__(self, sound_dir=None):
        pygame.mixer.init()
        self.extractor = MetadataExtractor()
        self.sound_dir = sound_dir or os.path.join('assets', 'music')
        self.files = [f for f in os.listdir(self.sound_dir) if f.endswith(SUPPORTED_EXT)]
        self.current_index = 0
        self.current_file = None
        self.metadata = None
        self.status = "Idle"

    def load_track(self, index):
        if not self.files:
            self.status = "No files found"
            self.metadata = None
            return None

        self.current_index = index % len(self.files)
        filename = self.files[self.current_index]
        file_path = os.path.join(self.sound_dir, filename)
        self.current_file = filename

        self.status = f"Loading {filename}..."
        meta = self.extractor.extract(file_path)
        self.metadata = meta

        if meta.get('notice'):
            self.status = meta['notice']
        else:
            self.status = "Metadata extracted!"

        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            self.status += " | Playing"
        except pygame.error as e:
            print(f"Failed to play {filename}: {e}")
            self.status += f" | Playback failed: {e}"

        return meta

    def next_track(self):
        return self.load_track(self.current_index + 1)


class MusicApp:
    """Wrapper de UI Pygame que consome PlaybackController."""

    def __init__(self, controller):
        self.controller = controller
        pygame.init()
        self.width = 600
        self.height = 400
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Music Extractor Test")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 20)

        self.album_art = None
        self.status = "Idle"

        self.BG_COLOR = (30, 30, 30)
        self.TEXT_COLOR = (255, 255, 255)

    def _load_album_art_from_bytes(self, img_data):
        if not img_data:
            self.album_art = None
            return False
        try:
            image = pygame.image.load(io.BytesIO(img_data))
            self.album_art = pygame.transform.scale(image, (300, 300))
            return True
        except pygame.error as e:
            print(f"Failed to load image from data: {e}")
            self.album_art = None
            return False

    def _sync_from_metadata(self):
        meta = self.controller.metadata or {}
        self.title = meta.get('title', 'Unknown')
        self.artist = meta.get('artist', 'Unknown')
        self.album = meta.get('album', 'Unknown')
        self._load_album_art_from_bytes(meta.get('art'))
        self.status = self.controller.status

    def load_and_render(self, index):
        self.controller.load_track(index)
        self._sync_from_metadata()
        self.render()

    def render(self):
        self.screen.fill(self.BG_COLOR)

        if self.album_art:
            rect = self.album_art.get_rect(center=(self.width//2, self.height//2 - 40))
            self.screen.blit(self.album_art, rect)
        else:
            pygame.draw.rect(self.screen, (50, 50, 50), (self.width//2 - 150, self.height//2 - 190, 300, 300), 2)
            text = self.font.render("No Art", True, (100, 100, 100))
            self.screen.blit(text, text.get_rect(center=(self.width//2, self.height//2 - 40)))

        y_offset = 20
        title_surf = self.font.render(f"Title: {getattr(self, 'title', 'Unknown')}", True, self.TEXT_COLOR)
        self.screen.blit(title_surf, (20, y_offset))
        y_offset += 25

        artist_surf = self.font.render(f"Artist: {getattr(self, 'artist', 'Unknown')}", True, self.TEXT_COLOR)
        self.screen.blit(artist_surf, (20, y_offset))
        y_offset += 25

        album_surf = self.font.render(f"Album: {getattr(self, 'album', 'Unknown')}", True, self.TEXT_COLOR)
        self.screen.blit(album_surf, (20, y_offset))

        status_text = self.font.render(f"Status: {self.status}", True, (200, 200, 200))
        self.screen.blit(status_text, (20, self.height - 40))

        controls_text = self.font.render("Controls: SPACE=Next Track, ESC=Quit", True, (150, 150, 150))
        self.screen.blit(controls_text, (20, self.height - 70))

        pygame.display.flip()

    def run(self):
        self.load_and_render(0)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        self.load_and_render(self.controller.current_index + 1)

            self.render()
            self.clock.tick(30)

        pygame.quit()


if __name__ == "__main__":
    controller = PlaybackController()
    app = MusicApp(controller)
    app.run()

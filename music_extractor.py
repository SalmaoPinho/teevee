import pygame
import os
import struct
import io

class MusicPlayer:
    def __init__(self):
        pygame.init()
        self.width = 600
        self.height = 400
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Music Extractor Test")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 20)
        
        self.current_file = None
        self.album_art = None
        self.status = "Idle"
        
        # Define colors
        self.BG_COLOR = (30, 30, 30)
        self.TEXT_COLOR = (255, 255, 255)
        
        # Test files
        self.sound_dir = os.path.join("assets", "sounds")
        self.files = [f for f in os.listdir(self.sound_dir) if f.endswith(('.m4a', '.mp3', '.wav', '.ogg'))]
        self.current_index = 0

    def extract_metadata_from_m4a(self, file_path):
        """
        Manually parses M4A/MP4 atoms to find metadata like cover art, artist, and album.
        """
        print(f"Attempting to extract metadata from {file_path}")
        metadata = {'art': None, 'artist': "Unknown", 'album': "Unknown", 'title': "Unknown"}
        try:
            with open(file_path, 'rb') as f:
                self._parse_atoms(f, os.path.getsize(file_path), metadata)
            return metadata
        except Exception as e:
            print(f"Error extracting metadata: {e}")
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
                except:
                    atom_type_str = "????"
                
                # Handle 64-bit size
                if atom_size == 1:
                    atom_size = struct.unpack('>Q', f.read(8))[0]
                    content_size = atom_size - 16
                else:
                    content_size = atom_size - 8
                
                if atom_size == 0:
                    content_size = end_pos - f.tell()

                # Containers to descend into
                # Note: 'meta' often has 4 bytes version/flags after header
                if atom_type_str in ['moov', 'trak', 'mdia', 'minf', 'stbl', 'udta', 'ilst']:
                    # Continue to read children
                    continue
                    
                elif atom_type_str == 'meta':
                    f.read(4) # Skip version/flags
                    continue
                
                # Metadata Atoms (iTunes style)
                # © is 0xA9. In utf-8, it's b'\xc2\xa9'. But in atoms it's usually just byte 0xA9.
                # We check byte values for special atoms
                
                is_data_atom = False
                target_key = None
                
                if atom_type == b'\xa9ART': # Artist
                    target_key = 'artist'
                    is_data_atom = True
                elif atom_type == b'\xa9alb': # Album
                    target_key = 'album'
                    is_data_atom = True
                elif atom_type == b'\xa9nam': # Name/Title
                    target_key = 'title'
                    is_data_atom = True
                elif atom_type_str == 'covr': # Cover Art
                    target_key = 'art'
                    is_data_atom = True
                    
                if is_data_atom:
                    # Inside these atoms, there is usually a 'data' atom
                    # We need to find it.
                    current_pos = f.tell()
                    atom_end = current_pos + content_size
                    
                    while f.tell() < atom_end:
                        d_header = f.read(8)
                        if len(d_header) < 8: break
                        d_size, d_type = struct.unpack('>I4s', d_header)
                        
                        if d_type == b'data':
                            # Found data atom
                            # skip 8 bytes (indicator + locale)
                            f.read(8)
                            data_len = d_size - 16
                            data_content = f.read(data_len)
                            
                            if target_key == 'art':
                                metadata['art'] = data_content
                            else:
                                try:
                                    metadata[target_key] = data_content.decode('utf-8', 'ignore')
                                except:
                                    pass
                            break
                        else:
                            # Skip other sub-atoms
                            f.seek(d_size - 8, 1)
                    
                    # Ensure we are at the end of the parent atom
                    f.seek(atom_end)
                    continue

                # Skip unknown atoms
                f.seek(content_size, 1)
                    
            except struct.error:
                break

    def load_track(self, index):
        if not self.files:
            self.status = "No files found"
            return

        self.current_index = index % len(self.files)
        filename = self.files[self.current_index]
        file_path = os.path.join(self.sound_dir, filename)
        self.current_file = filename
        
        self.status = f"Loading {filename}..."
        
        # Reset metadata
        self.album_art = None
        self.artist = "Unknown"
        self.album = "Unknown"
        self.title = filename
        
        self.render()
        
        # 1. Extract Metadata
        if filename.endswith('.m4a'):
            meta = self.extract_metadata_from_m4a(file_path)
            self.artist = meta.get('artist', 'Unknown')
            self.album = meta.get('album', 'Unknown')
            self.title = meta.get('title', filename)
            
            img_data = meta.get('art')
            if img_data:
                try:
                    image = pygame.image.load(io.BytesIO(img_data))
                    # Scale to fit
                    self.album_art = pygame.transform.scale(image, (300, 300))
                    self.status = "Metadata extracted!"
                except pygame.error as e:
                    print(f"Failed to load image from data: {e}")
                    self.status = "Art extraction failed (bad data)"
            else:
                self.status = "No art found in m4a"
        else:
            self.status = "No metadata (not m4a)"

        # 2. Load Audio
        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            self.status += " | Playing"
        except pygame.error as e:
            print(f"Failed to play {filename}: {e}")
            self.status += f" | Playback failed: {e}"

    def render(self):
        self.screen.fill(self.BG_COLOR)
        
        # Draw Art
        if self.album_art:
            rect = self.album_art.get_rect(center=(self.width//2, self.height//2 - 40))
            self.screen.blit(self.album_art, rect)
        else:
            # Draw placeholder
            pygame.draw.rect(self.screen, (50, 50, 50), (self.width//2 - 150, self.height//2 - 190, 300, 300), 2)
            text = self.font.render("No Art", True, (100, 100, 100))
            self.screen.blit(text, text.get_rect(center=(self.width//2, self.height//2 - 40)))

        # Draw Info
        y_offset = 20
        
        # Title
        title_surf = self.font.render(f"Title: {self.title}", True, self.TEXT_COLOR)
        self.screen.blit(title_surf, (20, y_offset))
        y_offset += 25
        
        # Artist
        artist_surf = self.font.render(f"Artist: {self.artist}", True, self.TEXT_COLOR)
        self.screen.blit(artist_surf, (20, y_offset))
        y_offset += 25
        
        # Album
        album_surf = self.font.render(f"Album: {self.album}", True, self.TEXT_COLOR)
        self.screen.blit(album_surf, (20, y_offset))
        
        # Status
        status_text = self.font.render(f"Status: {self.status}", True, (200, 200, 200))
        self.screen.blit(status_text, (20, self.height - 40))
        
        controls_text = self.font.render("Controls: SPACE=Next Track, ESC=Quit", True, (150, 150, 150))
        self.screen.blit(controls_text, (20, self.height - 70))
        
        pygame.display.flip()

    def run(self):
        self.load_track(0)
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        self.load_track(self.current_index + 1)
            
            self.render()
            self.clock.tick(30)
            
        pygame.quit()

if __name__ == "__main__":
    player = MusicPlayer()
    player.run()

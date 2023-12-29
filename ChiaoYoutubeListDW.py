import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QProgressBar
from PyQt5.QtCore import Qt
from ytmusicapi import YTMusic
from pytube import YouTube

class YouTubeDownloader(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('YouTube Music Downloader')

        self.playlist_url_label = QLabel("YouTube Music Playlist URL:")
        self.playlist_url_entry = QLineEdit()

        self.output_path_label = QLabel("Output Path:")
        self.output_path_entry = QLineEdit()
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_output_path)

        self.download_button = QPushButton("Download and Convert to MP3")
        self.download_button.clicked.connect(self.download_and_convert)

        self.downloading_label = QLabel("Downloading:")
        self.progress_bar = QProgressBar()

        layout = QVBoxLayout()
        layout.addWidget(self.playlist_url_label)
        layout.addWidget(self.playlist_url_entry)
        layout.addWidget(self.output_path_label)
        layout.addWidget(self.output_path_entry)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.download_button)
        layout.addWidget(self.downloading_label)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

    def browse_output_path(self):
        folder_selected = QFileDialog.getExistingDirectory(self, "Select Directory")
        self.output_path_entry.setText(folder_selected)

    def download_and_convert(self):
        playlist_url = self.playlist_url_entry.text()
        output_path = self.output_path_entry.text()

        if not playlist_url or not output_path:
            print("Please enter valid playlist URL and output path.")
            return

        self.download_and_convert_to_mp3(playlist_url, output_path)

    def download_and_convert_to_mp3(self, playlist_url, output_path='.'):
        ytmusic = YTMusic()

        playlist_id = playlist_url.split('list=')[1].split('&')[0]
        playlist = ytmusic.get_playlist(playlist_id)

        for index, track in enumerate(playlist['tracks']):
            try:
                video_url = f"https://www.youtube.com/watch?v={track['videoId']}"
                yt = YouTube(video_url, on_progress_callback=self.show_progress)
                audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()

                self.downloading_label.setText(f"Downloading: {yt.title}")
                self.progress_bar.setValue(0)
                self.progress_bar.setMaximum(100)

                print(f"Downloading {yt.title}...")
                audio_stream.download(output_path)

                mp4_file_path = f"{output_path}/{yt.title}.mp4"
                mp3_file_path = f"{output_path}/{yt.title}.mp3"

                os.rename(mp4_file_path, mp3_file_path)

                print(f"{yt.title} downloaded and converted to MP3.")
                self.progress_bar.setValue(100)
            except Exception as e:
                print(f"Error downloading {video_url}: {str(e)}")

    def show_progress(self, stream, chunk, remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - remaining

        percent = int((bytes_downloaded / total_size) * 100)
        self.progress_bar.setValue(percent)
        QApplication.processEvents()  # 使界面即時更新

if __name__ == '__main__':
    app = QApplication([])
    window = YouTubeDownloader()
    window.show()
    app.exec_()

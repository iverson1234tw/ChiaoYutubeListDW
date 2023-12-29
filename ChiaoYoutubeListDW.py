import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QProgressBar
from PyQt5.QtGui import QPixmap, QColor, QPainter
from PyQt5.QtCore import Qt
from ytmusicapi import YTMusic
from pytube import YouTube

class YouTubeDownloader(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setGeometry(100, 100, 300, 400)  # 調整窗口大小和位置
        self.setWindowTitle('阿伶的音樂下載神器')

        # 將頂部背景色設置為淡粉紅色接近白色
        # self.setStyleSheet("background-color: #FFECF0; color: white;")

        # 加入麵包小偷圖片，並設定大小為 500 x 200
        image_label = QLabel(self)
        pixmap = QPixmap("/Users/Josh/Desktop/ChiaoYoutubeListDW/bread_thief.jpg").scaled(500, 200, Qt.KeepAspectRatio)        
        pixmap = self.set_opacity(pixmap, 0.7)  # 設定透明度為 0.7
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)  # 將圖片置中

        self.playlist_url_label = QLabel("YouTube播放清單網址:")
        self.playlist_url_entry = QLineEdit()

        self.output_path_label = QLabel("存放音樂檔的位置:")
        self.output_path_entry = QLineEdit()
        self.browse_button = QPushButton("瀏覽")
        self.browse_button.clicked.connect(self.browse_output_path)

        self.download_button = QPushButton("開始下載")
        self.download_button.clicked.connect(self.download_and_convert)

        self.downloading_label = QLabel("下載中:")
        self.progress_bar = QProgressBar()
        self.author_label = QLabel("By 宏瑋")

        layout = QVBoxLayout()
        layout.addWidget(image_label)
        layout.addSpacing(20)  # 增加垂直間距
        layout.addWidget(self.playlist_url_label)
        layout.addWidget(self.playlist_url_entry)
        layout.addWidget(self.output_path_label)
        layout.addWidget(self.output_path_entry)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.download_button)
        layout.addWidget(self.downloading_label)
        layout.addWidget(self.progress_bar)
        layout.addStretch(1)  # 使用 stretch 來將下方的部分撐開
        layout.addWidget(self.author_label, alignment=Qt.AlignBottom | Qt.AlignRight)

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

                self.downloading_label.setText(f"Downloading: {yt.title}...")
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

    def set_opacity(self, pixmap, opacity):
        transparent_pixmap = QPixmap(pixmap.size())
        transparent_pixmap.fill(QColor(0, 0, 0, 0))
        painter = QPainter(transparent_pixmap)
        painter.setOpacity(opacity)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()
        return transparent_pixmap

if __name__ == '__main__':
    app = QApplication([])
    window = YouTubeDownloader()
    window.show()
    app.exec_()

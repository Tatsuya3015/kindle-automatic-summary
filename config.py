import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Kindle設定
    KINDLE_APP_NAME = "Kindle"  # macOSの場合
    PAGE_TURN_DELAY = 4  # ページめくり後の待機時間（秒）
    SCREENSHOT_DELAY = 1  # スクリーンショット撮影後の待機時間（秒）
    
    # 書籍設定
    BOOK_TITLE = os.getenv("BOOK_TITLE", "指定の書籍タイトル")  # 環境変数またはデフォルト値
    
    # Google Drive設定
    GOOGLE_DRIVE_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID", "")
    GOOGLE_CREDENTIALS_FILE = "credentials.json"
    
    # OpenAI設定
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = "gpt-3.5-turbo"
    
    # OCR設定
    OCR_LANGUAGE = "jpn"  # 日本語
    TESSERACT_PATH = "/opt/homebrew/bin/tesseract"  # macOSの場合
    
    # 出力設定
    OUTPUT_FOLDER = "output"
    SCREENSHOTS_FOLDER = "screenshots"
    TEXT_OUTPUT_FILE = "extracted_text.txt"
    SUMMARY_OUTPUT_FILE = "summary.txt"
    
    # AI要約プロンプト
    SUMMARY_PROMPT = """
    以下のテキストを要約してください。以下の形式で出力してください：

    1. 全体の要約（200字程度）
    2. 主要なポイント（箇条書き）
    3. 章ごとのまとめ
    4. 作者の伝えたいこと
    5. 特に学びがある部分
    6. 重要事項

    テキスト：
    {text}
    """
    
    def set_book_title(self, title):
        """書籍タイトルを動的に設定し、フォルダ構造を更新"""
        self.BOOK_TITLE = title
        self._update_output_paths()
    
    def _update_output_paths(self):
        """書籍タイトルに基づいて出力パスを更新"""
        # 書籍タイトルをファイル名に使用可能な形式に変換
        safe_title = self._sanitize_filename(self.BOOK_TITLE)
        
        # 出力フォルダを書籍タイトルごとに作成
        self.OUTPUT_FOLDER = os.path.join("output", safe_title)
        self.SCREENSHOTS_FOLDER = "screenshots"
        self.TEXT_OUTPUT_FILE = "extracted_text.txt"
        self.SUMMARY_OUTPUT_FILE = "summary.txt"
    
    def _sanitize_filename(self, filename):
        """ファイル名に使用できない文字を置換"""
        # ファイル名に使用できない文字を置換
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        # 連続するアンダースコアを1つに
        while '__' in filename:
            filename = filename.replace('__', '_')
        
        # 先頭と末尾のアンダースコアを削除
        filename = filename.strip('_')
        
        # 空文字列の場合はデフォルト名を使用
        if not filename:
            filename = "unknown_book"
        
        return filename
    
    def get_screenshots_folder_path(self):
        """スクリーンショットフォルダの完全パスを取得"""
        return os.path.join(self.OUTPUT_FOLDER, self.SCREENSHOTS_FOLDER)
    
    def get_text_output_path(self):
        """テキスト出力ファイルの完全パスを取得"""
        return os.path.join(self.OUTPUT_FOLDER, self.TEXT_OUTPUT_FILE)
    
    def get_summary_output_path(self):
        """要約出力ファイルの完全パスを取得"""
        return os.path.join(self.OUTPUT_FOLDER, self.SUMMARY_OUTPUT_FILE) 
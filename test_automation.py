#!/usr/bin/env python3
"""
Kindle自動要約システムのテストスクリプト
各機能を個別にテストできます
"""

import os
import sys
import logging
from config import Config
from kindle_automation import KindleAutomation
from google_drive_manager import GoogleDriveManager


# ログ設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_config():
    """設定ファイルのテスト"""
    print("=== 設定ファイルテスト ===")
    config = Config()
    print(f"書籍タイトル: {config.BOOK_TITLE}")

    print(f"Google Drive フォルダID: {config.GOOGLE_DRIVE_FOLDER_ID or '未設定'}")
    print(f"Tesseract パス: {config.TESSERACT_PATH}")
    print()

def test_screenshot():
    """スクリーンショット機能のテスト"""
    print("=== スクリーンショットテスト ===")
    automation = KindleAutomation()
    
    # スクリーンショット撮影
    screenshot_path = automation.take_screenshot()
    if screenshot_path:
        print(f"スクリーンショット撮影成功: {screenshot_path}")
        print(f"ファイルサイズ: {os.path.getsize(screenshot_path)} bytes")
    else:
        print("スクリーンショット撮影失敗")
    print()

def test_ocr():
    """OCR機能のテスト"""
    print("=== OCRテスト ===")
    automation = KindleAutomation()
    
    # テスト用のスクリーンショットを撮影
    screenshot_path = automation.take_screenshot()
    if screenshot_path:
        # OCR処理
        text = automation.extract_text_from_image(screenshot_path)
        if text:
            print(f"OCR成功: {len(text)}文字抽出")
            print(f"抽出テキスト（最初の100文字）: {text[:100]}...")
        else:
            print("OCR失敗: テキストが抽出できませんでした")
    else:
        print("スクリーンショット撮影失敗のためOCRテストをスキップ")
    print()



def test_google_drive():
    """Google Drive連携のテスト"""
    print("=== Google Drive連携テスト ===")
    try:
        drive_manager = GoogleDriveManager()
        print("Google Drive認証成功")
        
        # テストファイルの作成
        test_file_path = "test_file.txt"
        with open(test_file_path, 'w') as f:
            f.write("これはテストファイルです。")
        
        # アップロードテスト
        file_id = drive_manager.upload_file(test_file_path, "test_upload.txt")
        if file_id:
            print(f"アップロード成功: {file_id}")
        else:
            print("アップロード失敗")
        
        # テストファイルの削除
        os.remove(test_file_path)
        
    except Exception as e:
        print(f"Google Driveテスト失敗: {e}")
    print()

def test_kindle_automation():
    """Kindle自動化のテスト（実際の操作は行わない）"""
    print("=== Kindle自動化テスト ===")
    automation = KindleAutomation()
    
    # ディレクトリ作成テスト
    automation.setup_directories()
    if os.path.exists(automation.config.OUTPUT_FOLDER):
        print("出力ディレクトリ作成成功")
    else:
        print("出力ディレクトリ作成失敗")
    
    # 設定確認
    try:
        import pyautogui
        print(f"PyAutoGUI設定: FAILSAFE={pyautogui.FAILSAFE}, PAUSE={pyautogui.PAUSE}")
    except ImportError:
        print("PyAutoGUIがインストールされていません")
    print()

def main():
    """メインテスト関数"""
    print("Kindle自動テキスト抽出システム テスト開始")
    print("=" * 50)
    
    # 各機能のテスト
    test_config()
    test_screenshot()
    test_ocr()
    test_google_drive()
    test_kindle_automation()
    
    print("=" * 50)
    print("テスト完了")
    
    # 対話的なテスト選択
    while True:
        print("\n追加テストを実行しますか？")
        print("1. スクリーンショットテスト")
        print("2. OCRテスト")
        print("3. 終了")
        
        choice = input("選択してください (1-3): ").strip()
        
        if choice == '1':
            test_screenshot()
        elif choice == '2':
            test_ocr()
        elif choice == '3':
            break
        else:
            print("無効な選択です")

if __name__ == "__main__":
    main() 
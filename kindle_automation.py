import os
import time
import pyautogui
import cv2
import numpy as np
from PIL import Image
import pytesseract
from config import Config
from google_drive_manager import GoogleDriveManager

import logging
import subprocess

# ログ設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class KindleAutomation:
    def __init__(self):
        self.config = Config()
        self.screenshot_count = 0
        self.setup_directories()
        
        # OCR設定
        pytesseract.pytesseract.tesseract_cmd = self.config.TESSERACT_PATH
        
        # PyAutoGUI設定
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.5
        
    def setup_directories(self):
        """必要なディレクトリを作成"""
        os.makedirs(self.config.OUTPUT_FOLDER, exist_ok=True)
        os.makedirs(self.config.get_screenshots_folder_path(), exist_ok=True)
        
    def activate_kindle(self):
        """Kindleアプリをアクティブ化"""
        try:
            # より確実なアクティブ化スクリプト
            applescript = '''
            tell application "Amazon Kindle"
                activate
                delay 0.5
                tell application "System Events"
                    tell process "Amazon Kindle"
                        set frontmost to true
                    end tell
                end tell
            end tell
            '''
            subprocess.run(['osascript', '-e', applescript])
            time.sleep(1.5)  # アクティブ化待ちを長めに
            
            # ウィンドウを最大化
            maximize_script = '''
            tell application "System Events"
                tell process "Amazon Kindle"
                    set position of window 1 to {0, 0}
                    set size of window 1 to {1920, 1080}
                end tell
            end tell
            '''
            subprocess.run(['osascript', '-e', maximize_script])
            time.sleep(0.5)
            
            return True
        except Exception as e:
            logger.error(f"Kindleアプリのアクティブ化に失敗: {e}")
            return False

    def go_to_first_page(self):
        """最初のページになっていることを前提に、Kindleアプリをアクティブ化するだけ"""
        try:
            logger.info("Kindleアプリをアクティブ化し、最初のページが表示されていることを確認します...")
            self.activate_kindle()
            
            # 最初のページが表示されていることを前提とする
            logger.info("最初のページが表示されていることを前提として処理を続行します")
            time.sleep(1)
            
            return True
        except Exception as e:
            logger.error(f"Kindleアプリのアクティブ化に失敗: {e}")
            return False

    def determine_page_direction(self):
        """最初のページ確定後、矢印キーの方向を自動判定"""
        try:
            logger.info("矢印キーの方向を自動判定しています...")
            
            # 現在のページ（1ページ目）のスクリーンショットを撮影
            current_screenshot = pyautogui.screenshot()
            
            # 右矢印キーを押してページが変わるかテスト
            pyautogui.press('right')
            time.sleep(self.config.PAGE_TURN_DELAY)
            right_screenshot = pyautogui.screenshot()
            
            # 右矢印でページが変わったかチェック
            if not self._is_same_page(current_screenshot, right_screenshot):
                logger.info("✅ 右矢印キー（→）でページが変わります")
                # 左矢印で戻る
                pyautogui.press('left')
                time.sleep(self.config.PAGE_TURN_DELAY)
                return 'right'
            
            # 右矢印で変わらなかった場合、左矢印をテスト
            pyautogui.press('left')
            time.sleep(self.config.PAGE_TURN_DELAY)
            left_screenshot = pyautogui.screenshot()
            
            # 左矢印でページが変わったかチェック
            if not self._is_same_page(current_screenshot, left_screenshot):
                logger.info("✅ 左矢印キー（←）でページが変わります")
                # 右矢印で戻る
                pyautogui.press('right')
                time.sleep(self.config.PAGE_TURN_DELAY)
                return 'left'
            
            # どちらでも変わらない場合
            logger.warning("⚠️  矢印キーでページが変わりません。デフォルトで右矢印を使用します")
            return 'right'
            
        except Exception as e:
            logger.error(f"矢印キー方向の判定に失敗: {e}")
            logger.info("デフォルトで右矢印キーを使用します")
            return 'right'

    def open_kindle_and_book(self):
        """Kindleアプリを開いて書籍が既に開かれている状態を確認"""
        try:
            logger.info("Kindleアプリを起動しています...")
            # 1. Kindleアプリを直接起動
            subprocess.run(['open', '-a', 'Amazon Kindle'])
            time.sleep(5)  # 起動待ち
            # 2. アプリを最前面に
            self.activate_kindle()
            logger.info("Kindleアプリを前面に表示しました")

            # 3. 書籍が既に開かれていることを確認
            logger.info("📖 書籍が既に開かれていることを確認してください")
            logger.info("   書籍の最初のページが表示されている状態で実行します")
            time.sleep(2)

            # 4. 最初のページになっていることを前提として確認
            self.go_to_first_page()
            
            return True
        except Exception as e:
            logger.error(f"Kindleアプリの起動に失敗: {e}")
            return False
    
    def get_total_pages(self):
        """書籍の総ページ数を取得"""
        try:
            logger.info("書籍の総ページ数を確認しています...")
            
            # Kindleアプリで総ページ数を確認する方法
            # 方法1: 目次や書籍情報から取得を試行
            pyautogui.hotkey('cmd', 'i')  # 書籍情報を開く
            time.sleep(2)
            
            # スクリーンショットを撮影してOCRでページ数を検出
            info_screenshot = pyautogui.screenshot()
            info_text = pytesseract.image_to_string(info_screenshot, lang=self.config.OCR_LANGUAGE)
            
            # ページ数のパターンを検索
            import re
            page_patterns = [
                r'(\d+)\s*ページ',
                r'ページ数[：:]\s*(\d+)',
                r'(\d+)\s*of\s*\d+',  # "123 of 456" パターン
                r'(\d+)\s*/\s*\d+'   # "123/456" パターン
            ]
            
            total_pages = None
            for pattern in page_patterns:
                matches = re.findall(pattern, info_text)
                if matches:
                    # 最大値を総ページ数として使用
                    total_pages = max([int(m) for m in matches])
                    break
            
            # 書籍情報を閉じる
            pyautogui.press('escape')
            time.sleep(1)
            
            if total_pages:
                logger.info(f"書籍の総ページ数: {total_pages}ページ")
                return total_pages
            else:
                logger.warning("総ページ数を自動検出できませんでした")
                return None
                
        except Exception as e:
            logger.error(f"総ページ数の取得に失敗: {e}")
            return None
    
    def take_screenshot(self):
        """スクリーンショットを撮影"""
        try:
            # スクリーンショット前にKindleをアクティブ化
            self.activate_kindle()
            
            screenshot = pyautogui.screenshot()
            filename = f"page_{self.screenshot_count:04d}.png"
            filepath = os.path.join(self.config.get_screenshots_folder_path(), filename)
            screenshot.save(filepath)
            self.screenshot_count += 1
            logger.info(f"スクリーンショット保存: {filename}")
            return filepath
        except Exception as e:
            logger.error(f"スクリーンショット撮影に失敗: {e}")
            return None
    
    def turn_page(self, direction='right'):
        """指定された方向の矢印キーで次のページに進む"""
        try:
            self.activate_kindle()
            current_screenshot = pyautogui.screenshot()

            # 指定された方向の矢印キーで最大3回試行
            for attempt in range(3):
                pyautogui.press(direction)
                time.sleep(self.config.PAGE_TURN_DELAY)
                new_screenshot = pyautogui.screenshot()
                if not self._is_same_page(current_screenshot, new_screenshot):
                    arrow_symbol = '→' if direction == 'right' else '←'
                    logger.info(f"ページを{direction}（{arrow_symbol}）でめくりました（試行{attempt + 1}回目）")
                    return True
                else:
                    arrow_symbol = '→' if direction == 'right' else '←'
                    logger.warning(f"{direction}（{arrow_symbol}）でページが変わっていません（試行{attempt + 1}回目）")
                    if attempt < 2:
                        time.sleep(1)

            logger.warning(f"{direction}矢印キーでページが変わりませんでした。書籍の終了の可能性があります。")
            return False
        except Exception as e:
            logger.error(f"ページめくりに失敗: {e}")
            return False
    
    def _is_same_page(self, img1, img2, threshold=0.90):
        """2つの画像が同じページかどうかを簡易的に判定"""
        try:
            # 画像を小さくして比較（処理速度向上）
            img1_small = img1.resize((200, 200))
            img2_small = img2.resize((200, 200))
            
            # グレースケールに変換
            img1_gray = img1_small.convert('L')
            img2_gray = img2_small.convert('L')
            
            # 中央部分のみを比較（ヘッダーやフッターの変化を除外）
            center_size = 100
            start_x = (200 - center_size) // 2
            start_y = (200 - center_size) // 2
            
            diff = 0
            total_pixels = center_size * center_size
            
            for x in range(start_x, start_x + center_size):
                for y in range(start_y, start_y + center_size):
                    if abs(img1_gray.getpixel((x, y)) - img2_gray.getpixel((x, y))) > 15:
                        diff += 1
            
            similarity = 1 - (diff / total_pixels)
            logger.info(f"ページ類似度: {similarity:.3f} (閾値: {threshold})")
            return similarity > threshold
            
        except Exception as e:
            logger.error(f"画像比較でエラー: {e}")
            return False
    
    def capture_all_pages(self, max_pages=None, total_pages=None):
        """全ページのスクリーンショットを撮影"""
        logger.info("全ページのスクリーンショット撮影を開始します")
        
        # 最初に矢印キーの方向を判定
        page_direction = self.determine_page_direction()
        logger.info(f"📖 ページめくり方向: {page_direction}矢印キーを使用します")
        
        screenshots = []
        page_count = 0
        consecutive_empty_pages = 0  # 連続空ページカウンター
        
        while max_pages is None or page_count < max_pages:
            # スクリーンショット撮影
            screenshot_path = self.take_screenshot()
            if screenshot_path:
                screenshots.append(screenshot_path)
                page_count += 1
                
                # 進捗表示（パーセンテージ付き）
                if total_pages:
                    percentage = (page_count / total_pages) * 100
                    logger.info(f"進捗: {page_count}/{total_pages}ページ ({percentage:.1f}%)")
                else:
                    if page_count % 10 == 0:
                        logger.info(f"進捗: {page_count}ページ完了")
                
                # 判定された方向の矢印キーで次のページに進む
                if not self.turn_page(page_direction):
                    logger.info("ページめくりに失敗しました。処理を終了します。")
                    break
                
                # 書籍終了の検出
                if page_count > 10:  # 最初の10ページは除外
                    # 総ページ数が分かっている場合はそれで制限
                    if total_pages and page_count >= total_pages:
                        logger.info(f"総ページ数({total_pages}ページ)に達しました。処理を終了します。")
                        break
                    # 安全のため500ページで制限
                    elif page_count > 500:
                        logger.info("500ページに達しました。処理を終了します。")
                        break
                    
                time.sleep(self.config.SCREENSHOT_DELAY)
            else:
                logger.error("スクリーンショット撮影に失敗しました")
                break
        
        logger.info(f"スクリーンショット撮影完了: {len(screenshots)}ページ")
        return screenshots
    
    def extract_text_from_image(self, image_path):
        """画像からテキストを抽出（OCR）"""
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image, lang=self.config.OCR_LANGUAGE)
            return text.strip()
        except Exception as e:
            logger.error(f"OCR処理に失敗 {image_path}: {e}")
            return ""
    
    def extract_text_from_all_images(self, image_paths):
        """全画像からテキストを抽出"""
        logger.info("全画像からテキストを抽出しています...")
        
        all_text = []
        for i, image_path in enumerate(image_paths):
            logger.info(f"画像 {i+1}/{len(image_paths)} を処理中...")
            text = self.extract_text_from_image(image_path)
            if text:
                all_text.append(text)
        
        # 全テキストを1つのファイルに保存
        output_path = self.config.get_text_output_path()
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(all_text))
        
        logger.info(f"テキスト抽出完了: {output_path}")
        return '\n\n'.join(all_text)
    
    def run_full_automation(self, max_pages=None):
        """完全な自動化ワークフローを実行"""
        try:
            # 1. Kindleアプリを開いて書籍を開く
            if not self.open_kindle_and_book():
                return False
            
            # 2. 書籍の総ページ数を取得
            total_pages = self.get_total_pages()
            if total_pages:
                logger.info(f"📖 書籍情報: {self.config.BOOK_TITLE} ({total_pages}ページ)")
                
                # ユーザーに確認
                if max_pages is None or max_pages > total_pages:
                    max_pages = total_pages
                    logger.info(f"全{total_pages}ページを処理します")
            else:
                logger.warning("総ページ数が不明です。手動でページ数を指定してください。")
            
            # 3. 全ページのスクリーンショット撮影
            logger.info("📸 スクリーンショット撮影を開始します...")
            screenshots = self.capture_all_pages(max_pages, total_pages)
            if not screenshots:
                logger.error("スクリーンショットが撮影できませんでした")
                return False
            
            # 4. Google Driveに書籍フォルダを作成してアップロード
            drive_manager = GoogleDriveManager()
            
            # 書籍タイトルに基づいたフォルダを作成
            book_folder_id = drive_manager.setup_book_folder(self.config.BOOK_TITLE)
            if not book_folder_id:
                logger.warning("Google Driveフォルダの作成に失敗しました。デフォルトフォルダにアップロードします。")
            
            uploaded_files = drive_manager.upload_screenshots(screenshots)
            
            # 5. OCRでテキスト抽出
            full_text = self.extract_text_from_all_images(screenshots)
            
            # 6. 抽出テキストをGoogle Driveに保存
            text_path = self.config.get_text_output_path()
            drive_manager.upload_file(text_path, "extracted_text.txt", use_book_folder=True)
            
            logger.info("テキスト抽出とGoogle Driveアップロードが完了しました")
            
            logger.info("自動化ワークフローが完了しました")
            return True
            
        except Exception as e:
            logger.error(f"自動化ワークフローでエラーが発生: {e}")
            return False

if __name__ == "__main__":
    print("=== Kindle自動テキスト抽出システム ===")
    print()
    
    # 書籍タイトルの入力
    book_title = input("テキスト抽出したい書籍のタイトルを入力してください: ").strip()
    
    if not book_title:
        print("書籍タイトルが入力されていません。プログラムを終了します。")
        exit(1)
    
    # 設定を更新
    automation = KindleAutomation()
    automation.config.set_book_title(book_title)
    
    print(f"書籍タイトル: {book_title}")
    print()
    
    # 処理ページ数の確認
    max_pages_input = input("処理するページ数を入力してください（全ページの場合はEnter）: ").strip()
    
    max_pages = None
    if max_pages_input:
        try:
            max_pages = int(max_pages_input)
            print(f"最初の{max_pages}ページを処理します")
        except ValueError:
            print("無効な数値です。全ページを処理します")
    else:
        print("全ページを処理します")
    
    print()
    print("処理を開始します...")
    print("注意: Kindleアプリが前面に表示されていることを確認してください")
    print()
    
    # カウントダウン
    for i in range(5, 0, -1):
        print(f"開始まで {i} 秒...")
        time.sleep(1)
    
    # 自動化実行
    success = automation.run_full_automation(max_pages)
    
    if success:
        print()
        print("✅ 処理が完了しました！")
        print(f"📁 出力フォルダ: {automation.config.OUTPUT_FOLDER}")
        print(f"📸 スクリーンショット: {automation.config.OUTPUT_FOLDER}/{automation.config.SCREENSHOTS_FOLDER}")
        print(f"📝 抽出テキスト: {automation.config.OUTPUT_FOLDER}/{automation.config.TEXT_OUTPUT_FILE}")
    else:
        print()
        print("❌ 処理中にエラーが発生しました")
        print("ログを確認して問題を特定してください") 
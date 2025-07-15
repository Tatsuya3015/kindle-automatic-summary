#!/usr/bin/env python3
"""
Kindle自動要約システム - 簡単起動スクリプト
"""

import sys
import os

# プロジェクトのルートディレクトリをPythonパスに追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kindle_automation import KindleAutomation
import time

def main():
    print("🚀 Kindle自動テキスト抽出システム")
    print("=" * 40)
    print()
    
    # 設定確認
    print("📋 設定確認:")
    automation = KindleAutomation()
    

    
    # Google Drive設定確認
    if automation.config.GOOGLE_DRIVE_FOLDER_ID:
        print("✅ Google Drive: 設定済み")
    else:
        print("⚠️  Google Drive: 未設定（オプション）")
    
    # Tesseract確認
    if os.path.exists(automation.config.TESSERACT_PATH):
        print("✅ Tesseract OCR: 設定済み")
    else:
        print("❌ Tesseract OCR: 未設定")
        print("   brew install tesseract tesseract-lang を実行してください")
        return
    
    print()
    
    # 書籍タイトルの入力
    while True:
        book_title = input("📚 テキスト抽出したい書籍のタイトルを入力してください: ").strip()
        if book_title:
            break
        print("❌ 書籍タイトルを入力してください")
    
    # 設定を更新
    automation.config.set_book_title(book_title)
    
    # 書籍タイトルに基づいたディレクトリを再作成
    automation.setup_directories()
    
    print(f"📖 書籍タイトル: {book_title}")
    print()
    
    # 処理ページ数の確認
    print("📄 ページ数設定:")
    print("   • Enter: 自動検出（推奨）")
    print("   • 数値: 指定ページ数まで処理")
    print()
    
    while True:
        max_pages_input = input("📄 処理するページ数を入力してください（自動検出の場合はEnter）: ").strip()
        
        if not max_pages_input:
            max_pages = None
            print("📄 書籍の総ページ数を自動検出して処理します")
            break
        
        try:
            max_pages = int(max_pages_input)
            if max_pages > 0:
                print(f"📄 最初の{max_pages}ページを処理します")
                break
            else:
                print("❌ 1以上の数値を入力してください")
        except ValueError:
            print("❌ 有効な数値を入力してください")
    
    print()
    print("⚠️  注意事項:")
    print("   • Kindleアプリが前面に表示されていることを確認してください")
    print("   • 書籍が事前にダウンロードされていることを確認してください")
    print("   • 書籍の最初のページが表示されていることを確認してください")
    print("   • 処理中はマウスやキーボードの操作を避けてください")
    print()
    
    # 確認
    confirm = input("処理を開始しますか？ (y/N): ").strip().lower()
    if confirm not in ['y', 'yes', 'はい']:
        print("処理をキャンセルしました")
        return
    
    print()
    print("🚀 処理を開始します...")
    print()
    
    # カウントダウン
    for i in range(5, 0, -1):
        print(f"⏰ 開始まで {i} 秒...")
        time.sleep(1)
    
    print("🎬 開始！")
    print()
    
    # 自動化実行
    try:
        success = automation.run_full_automation(max_pages)
        
        if success:
            print()
            print("✅ 処理が完了しました！")
            print("=" * 40)
            print(f"📁 出力フォルダ: {automation.config.OUTPUT_FOLDER}")
            print(f"📸 スクリーンショット: {automation.config.get_screenshots_folder_path()}")
            print(f"📝 抽出テキスト: {automation.config.get_text_output_path()}")
            print()
            print("🎉 お疲れさまでした！")
        else:
            print()
            print("❌ 処理中にエラーが発生しました")
            print("ログを確認して問題を特定してください")
            
    except KeyboardInterrupt:
        print()
        print("⏹️  処理が中断されました")
    except Exception as e:
        print()
        print(f"❌ 予期しないエラーが発生しました: {e}")

if __name__ == "__main__":
    main() 
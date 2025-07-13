#!/usr/bin/env python3
"""
クリック機能のデバッグスクリプト
"""

import pyautogui
import time
import subprocess
import logging

# ログ設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_basic_click():
    """基本的なクリック機能をテスト"""
    print("=== 基本クリックテスト ===")
    
    # 現在のマウス位置を取得
    current_x, current_y = pyautogui.position()
    print(f"現在のマウス位置: ({current_x}, {current_y})")
    
    # 画面サイズを取得
    screen_width, screen_height = pyautogui.size()
    print(f"画面サイズ: {screen_width} x {screen_height}")
    
    # 画面中央をクリック
    print("画面中央をクリックします...")
    pyautogui.click(screen_width // 2, screen_height // 2)
    time.sleep(1)
    
    print("基本クリックテスト完了")
    print()

def test_kindle_activation():
    """Kindleアプリのアクティブ化をテスト"""
    print("=== Kindleアプリアクティブ化テスト ===")
    
    try:
        # Kindleアプリを起動
        subprocess.run(['open', '-a', 'Amazon Kindle'])
        time.sleep(3)
        
        # AppleScriptでアクティブ化
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
        time.sleep(2)
        
        print("Kindleアプリをアクティブ化しました")
        
        # ウィンドウ情報を取得
        window_script = '''
        tell application "System Events"
            tell process "Amazon Kindle"
                get position of window 1
            end tell
        end tell
        '''
        result = subprocess.run(['osascript', '-e', window_script], 
                              capture_output=True, text=True)
        print(f"ウィンドウ位置: {result.stdout.strip()}")
        
    except Exception as e:
        print(f"Kindleアプリアクティブ化エラー: {e}")
    
    print()

def test_coordinate_click():
    """座標クリックをテスト"""
    print("=== 座標クリックテスト ===")
    
    # テスト用の座標（現在のコードで使用されている座標）
    test_coordinates = [
        (72, 88, "三アイコン"),
        (522, 978, "スクロールバー下端"),
        (524, 133, "スクロールバー上端"),
        (524, 150, "目次一番上"),
        (82, 148, "初めに戻るボタン")
    ]
    
    for x, y, description in test_coordinates:
        print(f"{description}の座標 ({x}, {y}) をクリックします...")
        
        # マウスを移動
        pyautogui.moveTo(x, y, duration=1)
        time.sleep(0.5)
        
        # クリック
        pyautogui.click(x, y)
        time.sleep(1)
        
        print(f"  {description}クリック完了")
    
    print()

def test_visual_feedback():
    """視覚的フィードバックテスト"""
    print("=== 視覚的フィードバックテスト ===")
    
    # マウスカーソルを赤く表示（PyAutoGUIの機能）
    print("マウスカーソルを画面の四隅に移動して視覚的フィードバックを確認してください")
    
    screen_width, screen_height = pyautogui.size()
    corners = [
        (0, 0, "左上"),
        (screen_width-1, 0, "右上"),
        (0, screen_height-1, "左下"),
        (screen_width-1, screen_height-1, "右下")
    ]
    
    for x, y, corner_name in corners:
        print(f"{corner_name}に移動中...")
        pyautogui.moveTo(x, y, duration=2)
        time.sleep(1)
    
    print("視覚的フィードバックテスト完了")
    print()

def check_accessibility():
    """アクセシビリティ設定を確認"""
    print("=== アクセシビリティ設定確認 ===")
    
    # アクセシビリティ設定を開く
    print("アクセシビリティ設定を開きます...")
    subprocess.run(['open', '/System/Library/PreferencePanes/Security.prefPane'])
    
    print("以下の手順でアクセシビリティを確認してください:")
    print("1. セキュリティとプライバシー > プライバシー > アクセシビリティ")
    print("2. ターミナル（または使用中のターミナルアプリ）にチェックが入っているか確認")
    print("3. チェックが入っていない場合は追加してください")
    print()

def main():
    """メイン関数"""
    print("🔍 クリック機能デバッグツール")
    print("=" * 50)
    
    # PyAutoGUI設定を確認
    print(f"PyAutoGUI設定:")
    print(f"  FAILSAFE: {pyautogui.FAILSAFE}")
    print(f"  PAUSE: {pyautogui.PAUSE}")
    print()
    
    # 各テストを実行
    test_basic_click()
    test_kindle_activation()
    test_coordinate_click()
    test_visual_feedback()
    check_accessibility()
    
    print("=" * 50)
    print("デバッグ完了")
    print()
    print("💡 推奨される解決策:")
    print("1. アクセシビリティの許可を確認")
    print("2. KindleアプリのUIが変更されていないか確認")
    print("3. 画面解像度に応じて座標を調整")
    print("4. ウィンドウサイズを確認")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
改善された座標取得スクリプト
"""

import pyautogui
import time
import subprocess
import cv2
import numpy as np
from PIL import Image

def get_screen_info():
    """画面情報を取得"""
    screen_width, screen_height = pyautogui.size()
    print(f"画面サイズ: {screen_width} x {screen_height}")
    return screen_width, screen_height

def capture_kindle_window():
    """Kindleウィンドウのスクリーンショットを撮影"""
    print("Kindleウィンドウのスクリーンショットを撮影中...")
    screenshot = pyautogui.screenshot()
    screenshot.save("kindle_window.png")
    print("スクリーンショット保存: kindle_window.png")
    return screenshot

def find_ui_elements(screenshot):
    """UI要素を検出する（テンプレートマッチング）"""
    print("UI要素を検出中...")
    
    # 画面サイズに基づいて相対座標を計算
    screen_width, screen_height = pyautogui.size()
    
    # 相対座標（画面サイズに対する割合）
    relative_coordinates = {
        "three_dots": (0.0375, 0.0815),      # 三アイコン (72/1920, 88/1080)
        "scrollbar_bottom": (0.2719, 0.9056), # スクロールバー下端 (522/1920, 978/1080)
        "scrollbar_top": (0.2729, 0.1231),    # スクロールバー上端 (524/1920, 133/1080)
        "toc_first": (0.2729, 0.1389),        # 目次一番上 (524/1920, 150/1080)
        "go_to_beginning": (0.0427, 0.1370)   # 初めに戻る (82/1920, 148/1080)
    }
    
    # 実際の座標に変換
    actual_coordinates = {}
    for element, (rel_x, rel_y) in relative_coordinates.items():
        x = int(rel_x * screen_width)
        y = int(rel_y * screen_height)
        actual_coordinates[element] = (x, y)
        print(f"{element}: ({x}, {y})")
    
    return actual_coordinates

def test_coordinates_with_visual_feedback(coordinates):
    """座標を視覚的フィードバック付きでテスト"""
    print("\n=== 座標テスト（視覚的フィードバック） ===")
    
    for element, (x, y) in coordinates.items():
        print(f"\n{element}の座標 ({x}, {y}) をテスト中...")
        
        # マウスを移動（ゆっくり）
        pyautogui.moveTo(x, y, duration=2)
        time.sleep(1)
        
        # クリック前の確認
        input(f"  {element}の位置が正しいですか？ (Enter: 続行, n: スキップ): ")
        
        # クリック
        pyautogui.click(x, y)
        time.sleep(2)
        
        print(f"  {element}クリック完了")

def interactive_coordinate_finder():
    """対話的な座標取得"""
    print("\n=== 対話的座標取得 ===")
    print("マウスを目的の要素の上に移動してEnterを押してください")
    
    coordinates = {}
    elements = [
        "three_dots", "scrollbar_bottom", "scrollbar_top", 
        "toc_first", "go_to_beginning"
    ]
    
    for element in elements:
        input(f"\n{element}の位置にマウスを移動してEnterを押してください...")
        x, y = pyautogui.position()
        coordinates[element] = (x, y)
        print(f"{element}: ({x}, {y})")
    
    return coordinates

def generate_updated_code(coordinates):
    """更新されたコードを生成"""
    print("\n=== 更新されたコード ===")
    
    code = f'''
def go_to_first_page(self):
    """三メニューを開き、目次スクロールバーをドラッグして一番上にし、目次リストの一番上をクリックしてから『初めに戻る』をクリックし、さらに本の中央をクリックしてページ表示を確定"""
    try:
        logger.info("三メニュー→目次スクロールバーをドラッグ→一番上クリック→初めに戻るクリック→中央クリックで最初のページに移動します...")
        self.activate_kindle()

        # 更新された座標
        three_dots_x, three_dots_y = {coordinates['three_dots']}
        scrollbar_bottom_x, scrollbar_bottom_y = {coordinates['scrollbar_bottom']}
        scrollbar_top_x, scrollbar_top_y = {coordinates['scrollbar_top']}
        toc_first_x, toc_first_y = {coordinates['toc_first']}
        go_to_beginning_x, go_to_beginning_y = {coordinates['go_to_beginning']}

        # 三アイコンをクリック
        logger.info("三アイコンをクリック中...")
        pyautogui.click(three_dots_x, three_dots_y)
        time.sleep(1)

        # スクロールバーを下端から上端まで5回ドラッグして確実に一番上に移動
        for i in range(5):
            pyautogui.moveTo(scrollbar_bottom_x, scrollbar_bottom_y)
            pyautogui.mouseDown()
            time.sleep(0.2)
            pyautogui.moveTo(scrollbar_top_x, scrollbar_top_y, duration=0.5)
            pyautogui.mouseUp()
            time.sleep(0.5)
            logger.info(f"スクロールバーを上にドラッグ ({{i+1}}/5回目)")
        time.sleep(1)

        # 目次リストの一番上をクリック
        logger.info("目次リストの一番上をクリック中...")
        pyautogui.click(toc_first_x, toc_first_y)
        time.sleep(0.5)

        # 「初めに戻る」ボタンをクリック
        logger.info("「初めに戻る」ボタンをクリック中...")
        pyautogui.click(go_to_beginning_x, go_to_beginning_y)
        time.sleep(2)

        # 本の中央付近をクリックしてページ表示を確定
        logger.info("本の中央をクリックしてページ表示を確定中...")
        screen_width, screen_height = pyautogui.size()
        pyautogui.click(screen_width // 2, screen_height // 2)
        time.sleep(1)

        logger.info("最初のページに移動し、ページ表示を確定しました（中央クリック方式）")
        return True
    except Exception as e:
        logger.error(f"最初のページへの移動に失敗: {{e}}")
        return False
'''
    
    print(code)
    
    # ファイルに保存
    with open("updated_coordinates.txt", "w") as f:
        f.write(code)
    print("\n更新されたコードを updated_coordinates.txt に保存しました")

def main():
    """メイン関数"""
    print("🔧 座標改善ツール")
    print("=" * 50)
    
    # 画面情報を取得
    screen_width, screen_height = get_screen_info()
    
    # Kindleアプリをアクティブ化
    print("\nKindleアプリをアクティブ化中...")
    subprocess.run(['open', '-a', 'Amazon Kindle'])
    time.sleep(3)
    
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
    
    # スクリーンショットを撮影
    screenshot = capture_kindle_window()
    
    # 現在の座標を計算
    print("\n現在の座標を計算中...")
    current_coordinates = find_ui_elements(screenshot)
    
    # 座標テスト
    test_coordinates_with_visual_feedback(current_coordinates)
    
    # 対話的座標取得
    print("\n対話的座標取得を実行しますか？ (y/N): ", end="")
    choice = input().strip().lower()
    
    if choice in ['y', 'yes', 'はい']:
        new_coordinates = interactive_coordinate_finder()
        generate_updated_code(new_coordinates)
    
    print("\n座標改善ツール完了")

if __name__ == "__main__":
    main() 
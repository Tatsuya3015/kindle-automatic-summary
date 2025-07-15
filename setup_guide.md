# Kindle自動テキスト抽出システム セットアップガイド

## 概要
このシステムは、Kindleアプリで開いた書籍を自動でスクリーンショット撮影し、OCRでテキスト抽出を行う自動化ツールです。

## 必要な環境
- macOS
- Python 3.8以上
- Kindleアプリ（事前にインストール済み）
- インターネット接続

## セットアップ手順

### 1. 依存関係のインストール
```bash
# 仮想環境を作成（推奨）
python3 -m venv .venv
source .venv/bin/activate

# 依存関係をインストール
pip install -r requirements.txt
```

**⚠️ 重要な注意事項:**
- numpy 2.0系は互換性問題が発生する可能性があります
- OpenCV 4.9.x系は安定性に問題がある場合があります
- 問題が発生した場合は、requirements.txtのバージョンに戻してください

### 2. Tesseract OCRのインストール
```bash
# Homebrewを使用
brew install tesseract
brew install tesseract-lang  # 日本語サポート

# または公式サイトからダウンロード
# https://github.com/UB-Mannheim/tesseract/wiki
```

### 3. 環境変数の設定
`env_example.txt`を参考に`.env`ファイルを作成：
```bash
cp env_example.txt .env
```

`.env`ファイルを編集して以下を設定：

- `GOOGLE_DRIVE_FOLDER_ID`: Google DriveのフォルダID（オプション）
- `BOOK_TITLE`: 要約したい書籍のタイトル

### 4. Google Drive API設定（オプション）
1. [Google Cloud Console](https://console.cloud.google.com/)でプロジェクトを作成
2. Google Drive APIを有効化
3. 認証情報を作成（OAuth 2.0クライアントID）
4. `credentials.json`としてダウンロードし、プロジェクトルートに配置

### 5. 設定ファイルの編集
`config.py`の以下を編集：
- `BOOK_TITLE`: 実際の書籍タイトル
- `TESSERACT_PATH`: Tesseractのインストールパス

## 使用方法

### 基本的な使用方法
```bash
python kindle_automation.py
```

### テスト実行（最初の10ページのみ）
```bash
python kindle_automation.py
```

### 全ページ処理
`kindle_automation.py`の最後の行を以下に変更：
```python
automation.run_full_automation()  # max_pagesパラメータを削除
```

## 注意事項

### セキュリティ
- APIキーは`.env`ファイルで管理し、Gitにコミットしないでください
- `credentials.json`や`token.json`も同様に管理してください

### 自動化の制限
- Kindleアプリが前面に表示されている必要があります
- 書籍が事前にダウンロードされている必要があります
- 画面解像度やフォントサイズによってOCR精度が変わる場合があります

### トラブルシューティング

#### PyAutoGUIのエラー
- アクセシビリティの許可が必要です
- システム環境設定 > セキュリティとプライバシー > プライバシー > アクセシビリティでターミナルを許可

#### OCR精度の問題
- 画面の明度を調整
- フォントサイズを大きくする
- スクリーンショットの品質を確認

#### Google Driveアップロードエラー
- 認証情報が正しく設定されているか確認
- フォルダIDが正しいか確認
- インターネット接続を確認

#### numpy/OpenCV互換性エラー
- numpy 2.0系を使用している場合は1.24.3にダウングレード
- OpenCV 4.9.x系を使用している場合は4.8.1.78にダウングレード
- 仮想環境を完全にリセットしてから再インストール
```bash
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 出力ファイル
- `output/screenshots/`: スクリーンショット画像
- `output/extracted_text.txt`: 抽出されたテキスト


## カスタマイズ
`config.py`で以下の設定を変更可能：
- ページめくり待機時間
- スクリーンショット待機時間

- 出力フォルダ名 
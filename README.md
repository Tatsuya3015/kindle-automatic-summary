# Kindle自動要約システム

Kindleアプリで開いた書籍を自動でスクリーンショット撮影し、OCRでテキスト抽出、AI要約を行う自動化ツールです。

## 機能

1. **完全自動化ワークフロー**
   - Kindleアプリを自動で開く
   - 書籍が既に開かれている状態で実行
   - 最初のページへの自動移動
   - 矢印キー方向の自動判定
   - 全ページのスクリーンショットを自動撮影

2. **OCR文字認識**
   - Tesseract OCRを使用
   - 日本語対応
   - 画像からテキストを自動抽出

3. **Google Drive連携**
   - スクリーンショットを自動アップロード
   - 要約結果をGoogle Driveに保存

4. **AI要約**
   - OpenAI GPT-4を使用
   - カスタマイズ可能な要約プロンプト
   - 章ごとのまとめ、重要ポイント抽出

## システム構成

```
kindle-automatic-summary/
├── run.py                 # 🚀 簡単起動スクリプト（推奨）
├── kindle_automation.py   # メインの自動化スクリプト
├── config.py             # 設定ファイル
├── google_drive_manager.py # Google Drive連携
├── ai_summarizer.py      # AI要約機能
├── test_automation.py    # テストスクリプト
├── requirements.txt      # Python依存関係
├── setup_guide.md       # 詳細セットアップガイド
├── env_example.txt      # 環境変数設定例
├── .gitignore          # Git除外設定
└── README.md           # このファイル
```

## クイックスタート

### 1. 依存関係のインストール
```bash
pip install -r requirements.txt
```

### 2. Tesseract OCRのインストール
```bash
brew install tesseract tesseract-lang
```

### 3. 環境設定
```bash
cp env_example.txt .env
# .envファイルを編集してAPIキーを設定
```

### 4. 実行（対話的）
```bash
python3 run.py
```

### 5. 従来の実行方法
```bash
python3 kindle_automation.py
```

## 使用方法

### 🚀 推奨：対話的実行（簡単）
```bash
python3 run.py
```

実行すると以下の流れで進みます：
1. **設定確認** - APIキー、Google Drive、OCR設定を確認
2. **書籍タイトル入力** - 要約したい書籍のタイトルを入力
3. **ページ数指定** - 処理するページ数を指定（全ページの場合はEnter）
4. **注意事項確認** - 重要な注意事項を表示
5. **実行確認** - 最終確認（y/N）
6. **カウントダウン** - 5秒のカウントダウン
7. **自動処理実行** - 完全自動化処理開始

### 📋 従来の実行方法
```bash
python3 kindle_automation.py
```

### 🔄 完全自動化フロー

システムは以下の手順で完全自動化を実行します：

1. **Kindleアプリ起動**
   - Amazon Kindleアプリを自動起動
   - アプリを前面に表示

2. **書籍確認**
   - 書籍が既に開かれていることを確認
   - 書籍の最初のページが表示されている状態で実行

3. **最初のページへの移動**
   - 三メニューをクリック
   - 目次スクロールバーを5回ドラッグして一番上に移動
   - 目次一番上をクリック
   - 「初めに戻る」ボタンをクリック
   - 本の中央をクリックしてページ表示確定

4. **矢印キー方向の自動判定**
   - 右矢印キーでページが変わるかテスト
   - 変わらなければ左矢印キーでテスト
   - 適切な方向を自動判定

5. **ページめくり・スクリーンショット撮影**
   - 判定された方向の矢印キーでページめくり
   - 各ページのスクリーンショットを自動撮影
   - 進捗状況をリアルタイム表示

6. **OCR文字認識**
   - 全スクリーンショットからテキストを自動抽出
   - 日本語対応の高精度OCR

7. **Google Drive連携**
   - 全スクリーンショットを自動アップロード
   - 要約結果も自動保存

8. **AI要約**
   - OpenAI GPT-3.5-turboで自動要約
   - 章ごとのまとめ、重要ポイント抽出
   - 要約結果をGoogle Driveに保存

### 🧪 テスト実行
```bash
python3 test_automation.py
```

各機能を個別にテストできます：
- 設定ファイル読み込み
- スクリーンショット撮影
- OCR文字認識
- AI要約
- Google Drive連携

## 必要な設定

### OpenAI APIキー
- [OpenAI](https://platform.openai.com/)でアカウント作成
- APIキーを取得
- `.env`ファイルに設定

### Google Drive API（オプション）
- Google Cloud Consoleでプロジェクト作成
- Google Drive APIを有効化
- OAuth 2.0認証情報を作成
- `credentials.json`としてダウンロード

## 出力

- **スクリーンショット**: `output/screenshots/`
- **抽出テキスト**: `output/extracted_text.txt`
- **AI要約**: `output/summary.txt`

## 注意事項

### システム要件
- macOS専用（PyAutoGUIの制限）
- Python 3.8以上
- Kindleアプリが事前にインストールされている必要
- 書籍が事前にダウンロードされている必要

### 実行時の注意
- アクセシビリティの許可が必要（初回実行時）
- Kindleアプリが事前にインストールされている必要
- 書籍が事前にダウンロードされている必要
- **書籍を事前に開いて最初のページを表示しておく必要**
- 処理中はマウスやキーボードの操作を避ける
- インターネット接続が必要（AI要約、Google Drive連携）

### セキュリティ
- APIキーは`.env`ファイルで管理し、Gitにコミットしない
- `credentials.json`や`token.json`も同様に管理

## トラブルシューティング

### よくある問題

#### PyAutoGUIのエラー
- アクセシビリティの許可が必要
- システム環境設定 > セキュリティとプライバシー > プライバシー > アクセシビリティでターミナルを許可

#### OCR精度の問題
- 画面の明度を調整
- フォントサイズを大きくする
- スクリーンショットの品質を確認

#### API接続エラー
- APIキーが正しく設定されているか確認
- インターネット接続を確認
- API利用制限に達していないか確認

詳細なトラブルシューティングは[setup_guide.md](setup_guide.md)を参照してください。

## ライセンス

MIT License

## 貢献

プルリクエストやイシューの報告を歓迎します。 
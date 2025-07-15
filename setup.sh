#!/bin/bash

echo "🚀 Kindle自動テキスト抽出システム セットアップ"
echo "=============================================="
echo ""

# 色付きの出力関数
print_success() {
    echo "✅ $1"
}

print_error() {
    echo "❌ $1"
}

print_info() {
    echo "ℹ️  $1"
}

print_warning() {
    echo "⚠️  $1"
}

# Python 3.8以上の確認
echo "🐍 Python環境を確認中..."
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
required_version="3.8"

if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    print_success "Python $python_version: 要件を満たしています"
else
    print_error "Python $python_version: Python 3.8以上が必要です"
    exit 1
fi

# Homebrewの確認
echo ""
echo "🍺 Homebrewを確認中..."
if command -v brew &> /dev/null; then
    print_success "Homebrew: インストール済み"
else
    print_error "Homebrewがインストールされていません"
    echo "以下のコマンドでインストールしてください:"
    echo "/bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    exit 1
fi

# Tesseractのインストール
echo ""
echo "📖 Tesseract OCRをインストール中..."
if command -v tesseract &> /dev/null; then
    print_success "Tesseract: インストール済み"
else
    print_info "Tesseractをインストール中..."
    brew install tesseract tesseract-lang
    if command -v tesseract &> /dev/null; then
        print_success "Tesseract: インストール完了"
    else
        print_error "Tesseractのインストールに失敗しました"
        exit 1
    fi
fi

# 仮想環境の作成
echo ""
echo "🔧 仮想環境をセットアップ中..."
if [ -d ".venv" ]; then
    print_warning "既存の仮想環境を削除中..."
    rm -rf .venv
fi

print_info "新しい仮想環境を作成中..."
python3 -m venv .venv
if [ $? -eq 0 ]; then
    print_success "仮想環境: 作成完了"
else
    print_error "仮想環境の作成に失敗しました"
    exit 1
fi

# 仮想環境の有効化
echo ""
echo "📚 依存関係をインストール中..."
source .venv/bin/activate
if [ $? -eq 0 ]; then
    print_success "仮想環境: 有効化完了"
else
    print_error "仮想環境の有効化に失敗しました"
    exit 1
fi

# pipのアップグレード
print_info "pipをアップグレード中..."
pip install --upgrade pip

# 依存関係のインストール
print_info "Pythonパッケージをインストール中..."
pip install -r requirements.txt
if [ $? -eq 0 ]; then
    print_success "依存関係: インストール完了"
else
    print_error "依存関係のインストールに失敗しました"
    exit 1
fi

# 環境変数ファイルの作成
echo ""
echo "⚙️  環境設定ファイルを作成中..."
if [ ! -f ".env" ]; then
    cp env_example.txt .env
    print_success ".envファイル: 作成完了"
    print_info "必要に応じて.envファイルを編集してください"
else
    print_success ".envファイル: 既に存在します"
fi

# テスト実行
echo ""
echo "🧪 環境テストを実行中..."
python3 test_automation.py
if [ $? -eq 0 ]; then
    print_success "テスト: 完了"
else
    print_warning "テストで警告が発生しました。詳細を確認してください"
fi

echo ""
echo "🎉 セットアップ完了！"
echo "=================="
echo ""
echo "次のステップ:"
echo "1. .envファイルを編集して設定を完了"
echo "2. Kindleアプリをインストール"
echo "3. 要約したい書籍をダウンロード"
echo "4. python3 run.py で実行"
echo ""
echo "仮想環境の有効化:"
echo "source .venv/bin/activate"
echo ""
echo "仮想環境の無効化:"
echo "deactivate" 
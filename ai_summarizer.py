import logging
import openai
from config import Config

logger = logging.getLogger(__name__)

class AISummarizer:
    def __init__(self):
        self.config = Config()
        openai.api_key = self.config.OPENAI_API_KEY

    def summarize_text(self, text, max_length=4000):
        """テキストをAIで要約"""
        try:
            if not self.config.OPENAI_API_KEY:
                logger.error("OpenAI APIキーが設定されていません")
                return "APIキーが設定されていません"

            # テキストが長すぎる場合は分割
            if len(text) > max_length:
                text = text[:max_length] + "\n\n[テキストが長すぎるため、最初の部分のみを要約しています]"

            # プロンプトを準備
            prompt = self.config.SUMMARY_PROMPT.format(text=text)

            # OpenAI API v0.28.1の呼び出し
            response = openai.ChatCompletion.create(
                model=self.config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "あなたは優秀な要約アシスタントです。日本語で分かりやすく要約してください。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )

            summary = response["choices"][0]["message"]["content"]
            logger.info("AI要約が完了しました")
            return summary

        except Exception as e:
            logger.error(f"AI要約に失敗: {e}")
            logger.error(f"エラーの詳細: {type(e).__name__}")
            import traceback
            logger.error(f"トレースバック: {traceback.format_exc()}")
            return f"要約に失敗しました: {str(e)}"

    def analyze_book_structure(self, text):
        """書籍の構造を分析"""
        try:
            prompt = f"""
            以下のテキストから書籍の構造を分析してください：

            1. 章構成
            2. 各章の主要テーマ
            3. ストーリーの流れ
            4. 重要な転換点

            テキスト：
            {text[:3000]}
            """

            response = openai.ChatCompletion.create(
                model=self.config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "あなたは書籍分析の専門家です。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.5
            )

            return response["choices"][0]["message"]["content"]

        except Exception as e:
            logger.error(f"構造分析に失敗: {e}")
            return f"構造分析に失敗しました: {str(e)}"

    def extract_key_insights(self, text):
        """重要な洞察を抽出"""
        try:
            prompt = f"""
            以下のテキストから特に重要な洞察や学びを抽出してください：

            1. 最も印象的な引用
            2. 実践的なアドバイス
            3. 新しい視点や発見
            4. 行動に移せるポイント

            テキスト：
            {text[:3000]}
            """

            response = openai.ChatCompletion.create(
                model=self.config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "あなたは洞察抽出の専門家です。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.6
            )

            return response["choices"][0]["message"]["content"]

        except Exception as e:
            logger.error(f"洞察抽出に失敗: {e}")
            return f"洞察抽出に失敗しました: {str(e)}" 
import os
import logging
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from config import Config

logger = logging.getLogger(__name__)

class GoogleDriveManager:
    def __init__(self):
        self.config = Config()
        self.service = self._authenticate()
        
    def _authenticate(self):
        """Google Drive APIの認証"""
        SCOPES = ['https://www.googleapis.com/auth/drive.file']
        creds = None
        
        # トークンファイルが存在する場合は読み込み
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        # 有効な認証情報がない場合は認証フローを実行
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.config.GOOGLE_CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # 認証情報を保存
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        
        return build('drive', 'v3', credentials=creds)
    
    def upload_file(self, file_path, filename=None):
        """ファイルをGoogle Driveにアップロード"""
        try:
            if filename is None:
                filename = os.path.basename(file_path)
            
            file_metadata = {
                'name': filename,
                'parents': [self.config.GOOGLE_DRIVE_FOLDER_ID] if self.config.GOOGLE_DRIVE_FOLDER_ID else []
            }
            
            media = MediaFileUpload(file_path, resumable=True)
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            
            logger.info(f"ファイルアップロード完了: {filename} (ID: {file.get('id')})")
            return file.get('id')
            
        except Exception as e:
            logger.error(f"ファイルアップロードに失敗 {file_path}: {e}")
            return None
    
    def upload_screenshots(self, screenshot_paths):
        """スクリーンショットを一括アップロード"""
        logger.info("スクリーンショットをGoogle Driveにアップロードしています...")
        
        uploaded_files = []
        for screenshot_path in screenshot_paths:
            file_id = self.upload_file(screenshot_path)
            if file_id:
                uploaded_files.append(file_id)
        
        logger.info(f"スクリーンショットアップロード完了: {len(uploaded_files)}ファイル")
        return uploaded_files
    
    def create_folder(self, folder_name):
        """フォルダを作成"""
        try:
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [self.config.GOOGLE_DRIVE_FOLDER_ID] if self.config.GOOGLE_DRIVE_FOLDER_ID else []
            }
            
            file = self.service.files().create(
                body=file_metadata,
                fields='id'
            ).execute()
            
            logger.info(f"フォルダ作成完了: {folder_name} (ID: {file.get('id')})")
            return file.get('id')
            
        except Exception as e:
            logger.error(f"フォルダ作成に失敗: {e}")
            return None 
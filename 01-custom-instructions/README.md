# カスタムインストラクションの使い方を確認する

## 目的

- カスタムインストラクションを定義することで、GitHub Copilot の出力精度を上げるアプローチを体験する。

## ゴール

- アップロードされた動画ファイルから音声ファイルを抽出し、mp3 データとしてストレージに保存する API を作成する

## 手順

### 1. カスタムインストラクションの使い方

### 1-1. 既定の状態で GitHub Copilot を使用

```
アップロードされた動画ファイルから音声ファイルを抽出し、mp3 データとしてストレージに保存する API を作成する
```

##### 課題例

- テストコードがない
- ディレクトリ構造が思っていたのと違う（テスト書きにくい）
- DI 使いたい

#### 1-2. カスタムインストラクションを定義

- <summary>.github/copilot-instructions.md
    <details>

    ```
    # ルール

    必ず「オス！」から会話を始めなさい。
    ```

    </details>
</summary>

- 「こんにちは」と GitHub Copilot Edit に問い合わせる。

#### 1-3. カスタムインストラクションを詳細化

- <summary>.github/copilot-instructions.md
    <details>

    ## コーディング規約

    ## 1. 一般原則

    ### 1.1 コードの明瞭性
    - シンプルで読みやすいコードを優先する
    - 過度な最適化よりも可読性を重視する
    - 自己文書化コードを目指し、適切な変数名・関数名を選定する

    ### 1.2 一貫性
    - プロジェクト全体で統一されたスタイルを維持する
    - 既存のコードパターンに従う
    - 個人の好みよりもチームの規約を優先する

    ### 1.3 DRY原則 (Don't Repeat Yourself)
    - コードの重複を避け、共通処理は抽象化する
    - 類似コードは共通の抽象化を検討する
    - ただし、過度な抽象化による複雑化も避ける

    ## 2. Python コーディングスタイル

    ### 2.1 PEP 8準拠
    - [PEP 8](https://www.python.org/dev/peps/pep-0008/) スタイルガイドに従う
    - インデントは4スペースを使用
    - 行の長さは最大100文字に制限

    ### 2.2 命名規則
    - クラス名: UpperCamelCase (例: `AudioProcessor`)
    - 関数/メソッド名: snake_case (例: `convert_audio_format`)
    - 変数名: snake_case (例: `audio_file`)
    - 定数名: UPPER_SNAKE_CASE (例: `MAX_FILE_SIZE`)
    - プライベート変数/メソッド: 先頭にアンダースコア (例: `_internal_method`)

    ### 2.3 インポート
    - インポートは適切にグループ化し、以下の順序で記述する:
    1. 標準ライブラリ
    2. サードパーティライブラリ
    3. ローカルアプリケーション/ライブラリ
    - 各グループ内はアルファベット順にソート
    - ワイルドカードインポート (`from x import *`) は避ける

    ```python
    # 正しいインポート例
    import os
    import sys
    from typing import Dict, List

    import numpy as np
    import pandas as pd
    from fastapi import FastAPI

    from app.features.audio_conversion import AudioConverter
    from app.shared.utils import format_timestamp
    ```

    ### 2.4 ドキュメンテーション
    - すべての公開API、クラス、関数にはdocstringを記述する
    - Google スタイルのdocstringを使用
    - 複雑なロジックには適切なインラインコメントを付与

    ```python
    def convert_audio(input_file: str, output_format: str = "mp3") -> str:
        """音声ファイルを指定されたフォーマットに変換する.
        
        Args:
            input_file: 入力ファイルのパス
            output_format: 出力形式 (デフォルト: "mp3")
            
        Returns:
            変換後のファイルパス
            
        Raises:
            FileNotFoundError: 入力ファイルが存在しない場合
            ConversionError: 変換処理に失敗した場合
        """
        # 実装...
    ```

    ### 2.5 型ヒント
    - すべての関数とメソッドには型ヒントを使用する
    - 複雑な型は `typing` モジュールを活用する
    - 型ヒントはドキュメントとして役立つだけでなく、静的解析ツールにも活用される

    ## 3. プロジェクト固有のルール

    ### 3.1 エラー処理
    - 例外は具体的な型を使用し、汎用的な `Exception` は避ける
    - カスタム例外は `app/shared/exceptions` に定義
    - すべての例外は適切にログに記録する

    ### 3.2 ログ記録
    - システムの動作状況を把握できるよう、適切なログレベルを使用
    - ログメッセージは情報を明確に伝える内容にする
    - 個人情報や機密情報のログ出力は避ける

    ```python
    # 正しいログ記録例
    logger.info(f"File processing started: {file_id}")
    logger.error(f"Conversion failed for file {file_id}: {str(error)}")
    ```

    ### 3.3 テスト
    - すべての機能にはユニットテストを書く
    - モックを適切に使用して外部依存を分離する
    - 重要なユースケースには結合テストとE2Eテストを用意

    ### 3.4 非同期処理
    - I/O待ち時間が長い処理は非同期（async/await）を使用
    - ブロッキング処理はバックグラウンドタスクとして実行
    - 適切なタイムアウト処理を実装

    ## 4. コード品質ツール

    以下のツールを用いて継続的にコード品質を確保する:

    - **Black**: コードフォーマッタ
    - **isort**: インポート順序の最適化
    - **Flake8**: スタイルガイドの遵守チェック
    - **mypy**: 静的型チェック
    - **Pylint**: コード品質分析
    - **Bandit**: セキュリティの脆弱性スキャン

    ## 5. コードレビュー基準

    コードレビューでは以下の点に注目する:

    - 機能要件の充足
    - コーディング規約の遵守
    - アーキテクチャ設計原則の遵守
    - テストの充実度
    - エラー処理の適切さ
    - パフォーマンスへの配慮
    - セキュリティ上の懸念

    ## 6. バージョン管理

    - コミットメッセージは明確で説明的に記述
    - [Conventional Commits](https://www.conventionalcommits.org/) の形式に従う
    - 機能単位でブランチを分け、完了後にプルリクエストを作成

    ```
    feat: 音声ファイル変換機能の追加
    fix: 大容量ファイル処理時のメモリリーク修正
    docs: APIドキュメントの更新
    test: 音声認識サービスのテストケース追加
    ```
    </details>
</summary>

##### 課題例

- 出力されるコードが多数で、レビューしきれない
- テストコードは出力されたが、動作を保証する自信がない
- ディレクトリ構造が好みの形でない

#### 1-4. カスタムインストラクションにプロンプト ファイルを参照させる

- `docs/rules` ディレクトリを追加

```
mkdir -p docs/rules && mkdir -p docs/specs
```

- <summary>docs/rules/tdd.md
    <details>
    # テスト駆動開発 (TDD) ガイドライン

    ## 1. TDDの基本サイクル

    音声ファイル変換 API 開発プロジェクトでは、以下のTDDサイクルを採用します：

    ### Red-Green-Refactor サイクル

    1. **Red**: 失敗するテストを書く
    - 実装したい機能を明確にする
    - テストは実装前に記述し、必ず失敗することを確認する
    - テストは機能要件を明確に表現したものであること

    2. **Green**: 最小限のコードで成功させる
    - テストが通るための最小限（必要十分）のコードを実装する
    - この段階ではパフォーマンスやエレガントさより機能の正しさを優先する

    3. **Refactor**: リファクタリングする
    - コードの品質を高めるための改善を行う
    - テストは引き続き成功する状態を維持する
    - コードの重複を排除し、可読性を向上させる

    ## 2. テストの種類と役割

    ### 2.1 ユニットテスト

    - 対象: 関数、メソッド、小さなクラス
    - 目的: コードの最小単位の正確性を検証
    - 特徴: 高速に実行可能、外部依存をモック化
    - ツール: pytest
    - 場所: 各機能モジュール内の `tests` ディレクトリ

    ```python
    # 例: 音声変換サービスのユニットテスト
    def test_convert_mp4_to_mp3():
        converter = AudioConverter()
        result = converter.convert("test.mp4", "mp3")
        
        assert result.format == "mp3"
        assert result.success is True
        assert os.path.exists(result.output_path)
    ```

    ### 2.2 統合テスト

    - 対象: 複数のコンポーネントの相互作用
    - 目的: コンポーネント間の連携が正しく機能することを確認
    - 特徴: やや実行に時間がかかる、一部の外部依存を実際に使用
    - 場所: `tests/integration` ディレクトリ

    ```python
    # 例: ファイル処理と音声変換の統合テスト
    def test_file_upload_and_conversion_flow():
        # テスト用ファイルをアップロード
        file_service = FileProcessingService()
        file_id = file_service.upload(test_mp4_file)
        
        # 音声変換を実行
        converter_service = AudioConversionService()
        result = converter_service.process_file(file_id)
        
        # 検証
        assert result.status == "completed"
        assert storage_service.exists(f"{file_id}/converted.mp3")
    ```

    ### 2.3 エンドツーエンド (E2E) テスト

    - 対象: システム全体の機能
    - 目的: ユーザーの視点からのシナリオ検証
    - 特徴: 実行に時間がかかる、実際のサービスと連携
    - 場所: `tests/e2e` ディレクトリ

    ```python
    # 例: 音声ファイルアップロードから分析結果通知までのE2Eテスト
    def test_full_analysis_workflow():
        # APIクライアントをセットアップ
        client = TestClient(app)
        
        # ファイルアップロード
        with open("test_samples/conversation.mp4", "rb") as f:
            response = client.post("/api/files/upload", files={"file": f})
        
        job_id = response.json()["job_id"]
        
        # 処理完了を待機（ポーリングまたはWebhook）
        result = wait_for_completion(job_id, timeout=120)
        
        # 結果の検証
        assert result["status"] == "completed"
        assert "excel_url" in result
        assert result["notification_sent"] is True
    ```

    ## 3. テストカバレッジ方針

    - **目標カバレッジ**: コードベース全体で80%以上
    - **重要コンポーネント**: 核となるビジネスロジックは90%以上
    - **測定**: pytestとCoverageを使用
    - **レポート**: CI/CDパイプラインで自動生成

    ## 4. モックとスタブの使用ガイドライン

    ### 4.1 モックを使用するケース

    - 外部サービス（Azure Speech、Azure OpenAI等）の呼び出し
    - データベース操作
    - ファイルシステムアクセス
    - 時間依存の処理

    ### 4.2 モック実装例

    ```python
    # Azureサービスをモック化する例
    @pytest.fixture
    def mock_speech_service(monkeypatch):
        def mock_transcribe(*args, **kwargs):
            return {
                "text": "こんにちは、具合はどうですか？",
                "speaker": "veterinarian",
                "confidence": 0.95
            }
        
        monkeypatch.setattr("app.infrastructure.azure_speech.SpeechService.transcribe", 
                        mock_transcribe)
    ```

    ### 4.3 テストダブル選択指針

    - **Stub**: 単純な戻り値が必要な場合
    - **Mock**: 呼び出し回数や引数の検証が必要な場合
    - **Fake**: 軽量な代替実装が必要な場合（インメモリDBなど）
    - **Spy**: 実際の処理を行いつつ呼び出し情報も記録する場合

    ## 5. テストデータ管理

    - テストデータは `tests/fixtures` ディレクトリに格納
    - 大容量ファイルはGitに含めず、CIパイプラインで取得
    - 機密データはテスト用に匿名化したものを使用
    - フィクスチャとファクトリパターンを活用

    ```python
    @pytest.fixture
    def sample_conversation_data():
        return {
            "metadata": {
                "farm_id": "farm_123",
                "date": "2023-05-15",
                "duration": 630  # 10分30秒
            },
            "transcript": [
                {"time": 0, "speaker": "veterinarian", "text": "今日はどのような症状がありますか？"},
                {"time": 5, "speaker": "farmer", "text": "牛の食欲が昨日から落ちているんです"}
                # ...
            ]
        }
    ```

    ## 6. テスト自動化

    ### 6.1 ローカル開発環境

    - コミット前に自動実行するプリコミットフック
    - 変更されたコードに関連するテストのみ実行する機能

    ### 6.2 CI/CD パイプライン

    - プルリクエスト時に全テストを自動実行
    - テストカバレッジレポートの自動生成
    - 失敗テストの通知とレポート

    ### 6.3 実行コマンド

    ```bash
    # ユニットテストのみ実行
    pytest app/

    # 統合テストを実行
    pytest tests/integration/

    # E2Eテストを実行
    pytest tests/e2e/

    # カバレッジレポート付きで全テスト実行
    pytest --cov=app --cov-report=html
    ```

    ## 7. TDDのベストプラクティス

    ### 7.1 テストファーストの原則

    - 必ず実装前にテストを記述する
    - テストが意味のある失敗を示すことを確認してから実装に進む

    ### 7.2 FIRST原則

    - **Fast**: テストは高速に実行できること
    - **Independent**: テスト間に依存関係がないこと
    - **Repeatable**: 何度実行しても同じ結果が得られること
    - **Self-validating**: テストは自己検証可能であること
    - **Timely**: テストは実装前に書くこと

    ### 7.3 テストの表現力

    - テスト名は検証内容を明確に表現する
    - Given-When-Then パターンで条件、操作、期待結果を明確に
    - ヘルパー関数を使って複雑なセットアップを抽象化

    ```python
    def test_when_large_file_uploaded_then_chunked_processing_used():
        # Given: 大容量ファイルの準備
        large_file = create_test_file(size_mb=500)
        
        # When: ファイル処理サービスに渡す
        processor = FileProcessingService()
        result = processor.process(large_file)
        
        # Then: チャンク処理が適用されていることを確認
        assert result.processing_strategy == "chunked"
        assert len(result.chunks) > 1
    ```

    ## 8. 特定のテスト戦略

    ### 8.1 非同期コードのテスト

    ```python
    @pytest.mark.asyncio
    async def test_async_file_processing():
        processor = AsyncFileProcessor()
        result = await processor.process_file("test.mp4")
        assert result.status == "completed"
    ```

    ### 8.2 例外とエラー処理のテスト

    ```python
    def test_invalid_file_format_raises_exception():
        converter = AudioConverter()
        
        with pytest.raises(InvalidFormatError) as exc_info:
            converter.convert("test.txt", "mp3")
        
        assert "Unsupported format" in str(exc_info.value)
    ```

    ### 8.3 分岐条件のテスト

    各条件分岐を網羅するテストを作成し、すべてのパスが少なくとも1回は実行されるようにする。

    ## 9. コードレビューとテスト

    コードレビューでは以下の点を重点的に確認します：

    1. テストが機能要件を適切にカバーしているか
    2. テスト自体の品質は適切か
    3. エッジケースや例外パターンがテストされているか
    4. テストの可読性と保守性は確保されているか

    ## 10. 継続的改善

    - テスト戦略を定期的に見直し、改善する
    - 重要な障害発生時には、該当するケースのテストを追加
    - チーム内でテスト技術の共有と学習を促進
    </details>
</summary>

- <summary>docs/specs/test-suite.md
    <details>
    # テストスイート仕様書

    このドキュメントでは、サンプルプロジェクトの単体テストケースを体系的に一覧化しています。テスト駆動開発（TDD）の方針に従い、機能実装前にテストを設計・実装します。
    ## 1. ファイル処理機能のテストケース

    ### 1.1 FileService テストケース

    | テストID | テスト名 | 目的 | 入力条件 | 期待結果 | ステータス |
    |----------|---------|------|---------|---------|---------|
    | FS-001 | cleanup_old_files | 指定期間より古いファイルが正しく削除されることを検証する | 異なる更新日時のファイル（15分前、35分前、60分前）が存在する状態で30分基準でクリーンアップを実行 | 30分より古いファイル（35分前と60分前）が削除され、新しいファイル（15分前）は残る | 未実装 |
    | FS-002 | process_upload_mp4 | MP4ファイルのアップロード処理が正しく行われることを検証する | MP4形式のファイルをアップロード | ファイルがそのまま保存され、適切なレスポンスが返される | 未実装 |
    | FS-003 | process_upload_non_mp4 | 非MP4ファイルが正しく変換処理されることを検証する | AVI形式のファイルをアップロード | ファイルがMP3に変換され、適切なレスポンスが返される | 未実装 |
    | FS-004 | invalid_file_type | 未対応ファイル形式の場合にエラーが発生することを検証する | PDF形式のファイルをアップロード | InvalidFileTypeError例外が発生する | 未実装 |
    | FS-005 | file_size_limit_exceeded | サイズ制限を超えたファイルでエラーが発生することを検証する | 10GB超のファイルをアップロード | FileSizeLimitExceededErrorが発生する | 未実装 |
    | FS-006 | conversion_error_handling | ファイル変換エラー時の例外処理を検証する | 変換処理が失敗するケース | ConversionError例外が適切に発生する | 未実装 |
    | FS-007 | save_upload_file | アップロードされたファイルが正しく保存されることを検証する | UploadFileオブジェクト | ファイルが適切に保存され、ファイルサイズが返される | 未実装 |

    ## 2. 例外処理のテストケース

    ### 2.1 共通例外処理テストケース

    | テストID | テスト名 | 目的 | 入力条件 | 期待結果 | ステータス |
    |----------|---------|------|---------|---------|---------|
    | EX-001 | handle_invalid_file_type | ファイル形式例外の処理を検証する | 未対応ファイル形式 | 適切なエラーメッセージと処理が行われる | 未実装 |
    | EX-002 | handle_file_size_exceeded | ファイルサイズ超過例外の処理を検証する | サイズオーバーのファイル | 適切なエラーメッセージと処理が行われる | 未実装 |
    | EX-003 | handle_conversion_error | 変換エラー例外の処理を検証する | 変換失敗のケース | 適切なエラーメッセージと処理が行われる | 未実装 |
    | EX-004 | handle_storage_error | ストレージエラー例外の処理を検証する | ストレージアクセス失敗のケース | 適切なエラーメッセージと処理が行われる | 未実装 |
    | EX-005 | handle_transcription_error | 文字起こしエラー例外の処理を検証する | 文字起こし失敗のケース | 適切なエラーメッセージと処理が行われる | 未実装 |

    ## テスト実行手順

    テストの実行は以下のコマンドで行います：

    ```bash
    # すべてのテストを実行
    pytest

    # 特定のモジュールのテストを実行
    pytest app/features/file_processing/tests/

    # カバレッジレポートを出力
    pytest --cov=app --cov-report=html
    ```

    ## テストカバレッジ目標

    - 全体カバレッジ: 80%以上
    - 重要コンポーネント (ファイル処理): 90%以上
    - 例外処理: 100%
    </details>
</summary>

- <summary>docs/rules/code-style.md
    <details>
    # コーディング規約

    ## 1. 一般原則

    ### 1.1 コードの明瞭性
    - シンプルで読みやすいコードを優先する
    - 過度な最適化よりも可読性を重視する
    - 自己文書化コードを目指し、適切な変数名・関数名を選定する

    ### 1.2 一貫性
    - プロジェクト全体で統一されたスタイルを維持する
    - 既存のコードパターンに従う
    - 個人の好みよりもチームの規約を優先する

    ### 1.3 DRY原則 (Don't Repeat Yourself)
    - コードの重複を避け、共通処理は抽象化する
    - 類似コードは共通の抽象化を検討する
    - ただし、過度な抽象化による複雑化も避ける

    ## 2. Python コーディングスタイル

    ### 2.1 PEP 8準拠
    - [PEP 8](https://www.python.org/dev/peps/pep-0008/) スタイルガイドに従う
    - インデントは4スペースを使用
    - 行の長さは最大100文字に制限

    ### 2.2 命名規則
    - クラス名: UpperCamelCase (例: `AudioProcessor`)
    - 関数/メソッド名: snake_case (例: `convert_audio_format`)
    - 変数名: snake_case (例: `audio_file`)
    - 定数名: UPPER_SNAKE_CASE (例: `MAX_FILE_SIZE`)
    - プライベート変数/メソッド: 先頭にアンダースコア (例: `_internal_method`)

    ### 2.3 インポート
    - インポートは適切にグループ化し、以下の順序で記述する:
    1. 標準ライブラリ
    2. サードパーティライブラリ
    3. ローカルアプリケーション/ライブラリ
    - 各グループ内はアルファベット順にソート
    - ワイルドカードインポート (`from x import *`) は避ける

    ```python
    # 正しいインポート例
    import os
    import sys
    from typing import Dict, List

    import numpy as np
    import pandas as pd
    from fastapi import FastAPI

    from app.features.audio_conversion import AudioConverter
    from app.shared.utils import format_timestamp
    ```

    ### 2.4 ドキュメンテーション
    - すべての公開API、クラス、関数にはdocstringを記述する
    - Google スタイルのdocstringを使用
    - 複雑なロジックには適切なインラインコメントを付与

    ```python
    def convert_audio(input_file: str, output_format: str = "mp3") -> str:
        """音声ファイルを指定されたフォーマットに変換する.
        
        Args:
            input_file: 入力ファイルのパス
            output_format: 出力形式 (デフォルト: "mp3")
            
        Returns:
            変換後のファイルパス
            
        Raises:
            FileNotFoundError: 入力ファイルが存在しない場合
            ConversionError: 変換処理に失敗した場合
        """
        # 実装...
    ```

    ### 2.5 型ヒント
    - すべての関数とメソッドには型ヒントを使用する
    - 複雑な型は `typing` モジュールを活用する
    - 型ヒントはドキュメントとして役立つだけでなく、静的解析ツールにも活用される

    ## 3. プロジェクト固有のルール

    ### 3.1 エラー処理
    - 例外は具体的な型を使用し、汎用的な `Exception` は避ける
    - カスタム例外は `app/shared/exceptions` に定義
    - すべての例外は適切にログに記録する

    ### 3.2 ログ記録
    - システムの動作状況を把握できるよう、適切なログレベルを使用
    - ログメッセージは情報を明確に伝える内容にする
    - 個人情報や機密情報のログ出力は避ける

    ```python
    # 正しいログ記録例
    logger.info(f"File processing started: {file_id}")
    logger.error(f"Conversion failed for file {file_id}: {str(error)}")
    ```

    ### 3.3 テスト
    - すべての機能にはユニットテストを書く
    - モックを適切に使用して外部依存を分離する
    - 重要なユースケースには結合テストとE2Eテストを用意

    ### 3.4 非同期処理
    - I/O待ち時間が長い処理は非同期（async/await）を使用
    - ブロッキング処理はバックグラウンドタスクとして実行
    - 適切なタイムアウト処理を実装

    ## 4. コード品質ツール

    以下のツールを用いて継続的にコード品質を確保する:

    - **Black**: コードフォーマッタ
    - **isort**: インポート順序の最適化
    - **Flake8**: スタイルガイドの遵守チェック
    - **mypy**: 静的型チェック
    - **Pylint**: コード品質分析
    - **Bandit**: セキュリティの脆弱性スキャン

    ## 5. コードレビュー基準

    コードレビューでは以下の点に注目する:

    - 機能要件の充足
    - コーディング規約の遵守
    - アーキテクチャ設計原則の遵守
    - テストの充実度
    - エラー処理の適切さ
    - パフォーマンスへの配慮
    - セキュリティ上の懸念

    ## 6. バージョン管理

    - コミットメッセージは明確で説明的に記述
    - [Conventional Commits](https://www.conventionalcommits.org/) の形式に従う
    - 機能単位でブランチを分け、完了後にプルリクエストを作成

    ```
    feat: 音声ファイル変換機能の追加
    fix: 大容量ファイル処理時のメモリリーク修正
    docs: APIドキュメントの更新
    test: 音声認識サービスのテストケース追加
    ```
    </details>
</summary>

- <summary>docs/rules/directory.md
    <details>
    # ディレクトリ構造

    ## プロジェクト構成

    ## アプリケーションのディレクトリ構造

    ```
    app/
    ├── features/                              # 機能ごとのバーティカルスライス
    │   └── file_processing/                   # ファイル処理機能
    │       ├── controllers/                   # APIエンドポイント
    │       ├── services/                      # ビジネスロジック
    │       ├── models/                        # データモデル
    │       └── tests/                         # 機能単位のテスト
    │
    ├── shared/                                # 共通コンポーネント
    │   ├── models/                            # 共通データモデル
    │   ├── utils/                             # ユーティリティ関数
    │   ├── constants/                         # 定数定義
    │   └── exceptions/                        # カスタム例外クラス
    │
    ├── infrastructure/                        # 外部サービス連携
    │   └── storage/                           # Blobストレージ
    │
    ├── api/                                   # APIエントリポイント
    │   ├── routes/                            # ルート定義
    │   ├── middleware/                        # ミドルウェア
    │   └── startup.py                         # アプリケーション設定
    │
    └── tests/                                 # テストコード
        ├── integration/                       # 統合テスト
        └── e2e/                               # エンドツーエンドテスト
    ```

    ## バーティカルスライスアーキテクチャの特徴

    ### 機能別の独立性

    各機能（feature）は独立した垂直スライスとして実装され、以下の特徴を持ちます：

    - **自己完結性**: 各スライスは自身の責務に必要なすべてのレイヤー（コントローラー、サービス、モデル）を含む
    - **関心の分離**: 機能ごとに明確な境界を持ち、責任範囲が明確
    - **変更の局所化**: 機能変更が他の機能に影響しにくい設計

    ### チーム開発の最適化

    - 機能ごとにチームを割り当て可能
    - 並行開発の促進
    - チーム間の結合度を低減

    ### 依存関係の管理

    - 上位レベルの機能は下位レベルの機能に依存可能
    - 循環依存を避けるための明確な階層構造
    - `shared`ディレクトリで共通コンポーネントを提供

    ### テスト戦略

    - 各機能スライス内でユニットテスト
    - 機能間の連携は統合テストとE2Eテストでカバー
    - テスト可能性を高める設計

    </details>
</summary>

- <summary>docs/rules/project-brief.md
    <details>
    # プロジェクト概要と要求事項

    ## 1. 目的

    本プロジェクトは、高齢者の発話に関する動画から音声を抽出し、データとして保存することを目的としています。
    システム観点では、バーティカルスライスアーキテクチャを採用することで、各機能を独立して開発・テスト・デプロイ可能なシステムとすることを目指しています。

    ## 2. プロジェクト概要

    本システムは、以下の主要な機能を実現します。

    - ユーザー認証および認可
    - ファイル処理（添付ファイルのアップロード）
    - 音声処理（MP4等の動画ファイルをMP3モノラルに変換）

    ## 3. 主要要求事項

    ### 3.1 機能要件

    #### ファイル処理
    - MP4形式の録画ファイルをアップロード可能
    - ファイルサイズの上限は2GBまで
    - アップロード状況をフィードバックする進捗表示

    #### 音声処理
    - MP4からMP3への自動変換
    - ステレオからモノラルへの変換
    - 処理中の一時データの安全な保存

    ### 3.2 非機能要件

    #### パフォーマンス
    - 10分の録音ファイルの処理時間：5分以内
    - 同時に10件の処理をサポート
    - レスポンス時間：API呼び出し後3秒以内

    #### セキュリティ
    - すべての通信はTLS 1.3で暗号化
    - APIアクセスはOAuth 2.0で認可
    - 個人情報や機密情報の適切な取り扱い
    - アクセスログの保存と監視

    #### 可用性
    - 稼働率99.5%以上
    - 計画的メンテナンス時間外での可用性確保
    - 障害時の自動復旧機能

    #### 拡張性
    - 新たな分析アルゴリズムの追加が容易
    - ユーザー数増加に対応するスケーラビリティ
    - 他システムとの統合APIの提供

    #### 信頼性
    - データの整合性を保証するためのバックアップ体制
    - エラー発生時の適切なフォールバック処理
    - 完全な監査証跡の維持

    ## 4. ユーザー体験

    - 研究者が直感的に操作できるインターフェース設計
    - 分析結果の視覚的な表示と理解しやすいレポート形式（分析要件が決定後に実装）
    ## 5. 技術スタック

    ### バックエンド
    - 言語: Python 3.12+
    - フレームワーク: FastAPI
    - ストレージ: Blob Storage

    ### インフラストラクチャ
    - クラウド: Microsoft Azure
    - コンテナ化: Docker, Azure Container Apps
    - CI/CD: GitHub Actions

    ## 6. 成功基準

    - ユーザー満足度調査で80%以上の肯定的評価
    - 分析処理時間の短縮（従来の手動分析と比較して80%削減）
    </details>
</summary>

- <summary>docs/rules/system-patterns.md
    <details>
    # システムパターン: 分析

    ## 音声解析 API

    ### アーキテクチャ概要

    ```mermaid
    sequenceDiagram
        actor User as ユーザー
        participant UI as Slack
        participant Controller as APIコントローラー
        participant Processing as 音声処理サービス
        participant Converter as 音声変換サービス
        participant Storage as Blob Storage
        
        User->>UI: MP4ファイルをアップロード
        UI->>Controller: ファイル送信
        Controller->>Processing: 処理開始
        Processing->>Converter: MP4→モノラルMP3変換要求
        Converter->>Storage: 変換済みファイル保存
        Storage-->>Converter: 保存完了
        Converter-->>Processing: 変換完了
        Processing-->>Controller: 処理完了
        Controller-->>UI: 結果返却
        UI-->>User: 処理完了通知
    ```

    ## アーキテクチャ設計原則

    ### 1. バーティカルスライス

    本プロジェクトではバーティカルスライスアーキテクチャを採用します。このパターンの主な特徴は：

    - 機能ごとに独立した「スライス」としてモジュール化
    - 各スライスは自身のレイヤー（コントローラー、サービス、モデル）を保持
    - 機能間の境界を明確にし、結合度を低く保つ

    ```
    ┌─────────────┐  
    │ ファイル処理  │
    ├─────────────┤
    │ コントローラ  │
    ├─────────────┤
    │ サービス     │
    ├─────────────|
    │ モデル       │
    └─────────────┘
    ```

    ### 2. クリーンアーキテクチャ

    各機能スライス内では、クリーンアーキテクチャの原則に従います：

    - **依存関係の方向**: 外部から内部へ（インフラ → インターフェース → ユースケース → エンティティ）
    - **依存性逆転の原則**: インターフェースを利用して依存方向を制御
    - **ビジネスルールの独立性**: コアロジックをフレームワークや外部ライブラリから独立させる

    ```
    ┌───────────────────────────────────────────┐
    │              エンティティ                  │
    │ (ビジネスルールとデータモデル)              │
    └───────────────┬───────────────────────────┘
                    │
    ┌───────────────▼───────────────────────────┐
    │            ユースケース                    │
    │ (アプリケーション固有のビジネスルール)       │
    └───────────────┬───────────────────────────┘
                    │
    ┌───────────────▼───────────────────────────┐
    │          インターフェースアダプター          │
    │ (コントローラー、プレゼンター、ゲートウェイ)   │
    └───────────────┬───────────────────────────┘
                    │
    ┌───────────────▼───────────────────────────┐
    │          フレームワークと外部ツール          │
    │ (データベース、フレームワーク、UI、Web等)     │
    └───────────────────────────────────────────┘
    ```

    ### 3. CQRS (Command Query Responsibility Segregation)

    状態を変更する操作（コマンド）と情報を取得する操作（クエリ）を分離します：

    - **コマンド**: ファイルアップロード、変換処理開始など
    - **クエリ**: 処理状況確認、結果取得など

    この分離により、それぞれの処理を最適化し、システムの拡張性と保守性を向上させます。
    </details>
</summary>

- <summary>.github/copilot-instructions.md
    <details>
    # ルール

    コード生成に関するルールは、[../docs/rules/](../docs/rules/)フォルダ配下に記載されています。必要に応じて参照してください。

    なお、本プロジェクトはテスト駆動開発を採用しており、必ず[../docs/rules/tdd.md](../docs/rules/tdd.md): テスト駆動開発（TDD）ガイドラインを読んで、単体テストを作成してから、本実装に入ってください。単体テストの作成にあたっては、[../docs/specs/test-suite.md](../docs/specs/test-suite.md): 単体テストケース一覧も併せて参照してください。

    以下は、それぞれのファイルの説明です。

    - [../docs/rules/code-style.md](../docs/rules/code-style.md): コーディング規約
    - [../docs/rules/directory.md](../docs/rules/directory.md): プロジェクトのディレクトリ構成
    - [../docs/rules/project-brief.md](../docs/rules/project-brief.md): プロダクトの目的やユーザーに提供する価値（なぜこのプロジェクトが存在し、何を解決するか）
    - [../docs/rules/system-patterns.md](../docs/rules/system-patterns.md): アプリケーションアーキテクチャ
    - [../docs/rules/tdd.md](../docs/rules/tdd.md): テスト駆動開発（TDD）ガイドライン
    - [../docs/specs/test-suite.md](../docs/specs/test-suite.md): 単体テストケース一覧
    </details>
</summary>

## 参考

- [GitHub Copilot のリポジトリ カスタム命令を追加する](https://docs.github.com/ja/copilot/customizing-copilot/adding-repository-custom-instructions-for-github-copilot#writing-effective-repository-custom-instructions)
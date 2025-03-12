GitHub Copilot Hands on Lab
Mar 2025

<br />

### Contents

- [Exercise 1: 既存アプリのリファクタリング]

    - [Task 1: 既存アプリの動作確認](#task-1-既存アプリの動作確認)

    - [Task 2: 仕様書の生成](#task-2-仕様書の生成)

    - [Task 3: テストコードの生成](#task-3-テストコードの生成)

<br />

## Exercise 1: 既存アプリのリファクタリング

<br />

### Task 1: 既存アプリの動作確認

- バックエンドアプリケーションの依存関係をインストール。

```bash
cd backend && pip install -r requirements.txt
```

- バックエンドアプリケーションを起動。

```bash
uvicorn main:app --reload
```

- フロントエンドアプリケーションを起動。

```
cd frontend && npm install && npm start
```

- http://localhost:3000 に接続

### Task 2: 仕様書の生成

- 以下のプロンプトを入力し、既存アプリの仕様書を markdown 形式で作成。

```
docs/specs フォルダを作成し、フロントエンド・バックエンドそれぞれのアプリケーションの仕様書を作成して。
```

- 以下のプロンプトを入力し、既存アプリのテスト仕様書を markdown 形式で作成。

```
docs/specs フォルダを作成し、フロントエンド・バックエンドそれぞれのテスト仕様書を作成して。
```
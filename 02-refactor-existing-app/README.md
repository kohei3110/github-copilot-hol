# FastAPI Todo アプリケーション

これは、FastAPIを使用した簡単なTodoアプリケーションです。

## 機能

- Todoアイテムの作成
- 全Todoアイテムの取得
- 特定のTodoアイテムの取得
- Todoアイテムの更新
- Todoアイテムの削除

## インストール方法

1. 依存関係をインストールします：

```bash
pip install -r requirements.txt
```

## 使い方

1. アプリケーションを起動します：

```bash
uvicorn main:app --reload
```

2. ブラウザで以下のURLにアクセスして、Swagger UIでAPIをテストします：

```
http://localhost:8000/docs
```

## API エンドポイント

- `GET /` - ルートエンドポイント
- `GET /todos/` - 全てのTodoアイテムを取得
- `GET /todos/{todo_id}` - 特定のTodoアイテムを取得
- `POST /todos/` - 新しいTodoアイテムを作成
- `PUT /todos/{todo_id}` - 特定のTodoアイテムを更新
- `DELETE /todos/{todo_id}` - 特定のTodoアイテムを削除

## データモデル

Todoアイテムは以下の属性を持ちます：

- `id`: 整数（自動生成）
- `title`: 文字列（必須）
- `description`: 文字列（オプション）
- `completed`: 真偽値（デフォルトはfalse）
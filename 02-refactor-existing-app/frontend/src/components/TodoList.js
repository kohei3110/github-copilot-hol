import React, { useState, useEffect } from 'react';
import TodoItem from './TodoItem';
import { fetchTodos, createTodo, updateTodo, deleteTodo } from '../api/todoApi';

const TodoList = () => {
  const [todos, setTodos] = useState([]);
  const [newTodo, setNewTodo] = useState({ title: '', description: '', completed: false });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Todoリストのロードとエラーハンドリングを行う
  useEffect(() => {
    const loadTodos = async () => {
      try {
        setLoading(true);
        const data = await fetchTodos();
        setTodos(data);
        setError(null);
      } catch (err) {
        console.error('Todoの読み込み中にエラーが発生しました:', err);
        setError('Todoの読み込みに失敗しました。サーバーが実行中か確認してください。');
      } finally {
        setLoading(false);
      }
    };

    loadTodos();
  }, []);

  // 新しいTodoの入力処理
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewTodo(prev => ({ ...prev, [name]: value }));
  };

  // 新しいTodoの追加処理
  const handleAddTodo = async (e) => {
    e.preventDefault();
    
    if (!newTodo.title.trim()) {
      alert('タイトルを入力してください');
      return;
    }

    try {
      setLoading(true);
      const createdTodo = await createTodo(newTodo);
      setTodos(prev => [...prev, createdTodo]);
      setNewTodo({ title: '', description: '', completed: false });
      setError(null);
    } catch (err) {
      console.error('Todoの作成中にエラーが発生しました:', err);
      setError('新しいTodoの追加に失敗しました。');
    } finally {
      setLoading(false);
    }
  };

  // Todo項目の更新処理
  const handleUpdateTodo = async (id, updatedTodo) => {
    try {
      setLoading(true);
      const result = await updateTodo(id, updatedTodo);
      setTodos(prev => 
        prev.map(todo => todo.id === id ? result : todo)
      );
      setError(null);
    } catch (err) {
      console.error(`Todo #${id}の更新中にエラーが発生しました:`, err);
      setError(`Todo #${id}の更新に失敗しました。`);
    } finally {
      setLoading(false);
    }
  };

  // Todo項目の削除処理
  const handleDeleteTodo = async (id) => {
    try {
      setLoading(true);
      await deleteTodo(id);
      setTodos(prev => prev.filter(todo => todo.id !== id));
      setError(null);
    } catch (err) {
      console.error(`Todo #${id}の削除中にエラーが発生しました:`, err);
      setError(`Todo #${id}の削除に失敗しました。`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="todo-list-container">
      <h2>Todoリスト</h2>
      
      {/* エラー表示 */}
      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {/* 新しいTodoの追加フォーム */}
      <form onSubmit={handleAddTodo} className="todo-form">
        <div>
          <input
            type="text"
            name="title"
            placeholder="タイトル"
            value={newTodo.title}
            onChange={handleInputChange}
          />
        </div>
        <div>
          <textarea
            name="description"
            placeholder="詳細"
            value={newTodo.description}
            onChange={handleInputChange}
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? '追加中...' : '追加'}
        </button>
      </form>

      {/* Todoリスト */}
      <div className="todos-container">
        {loading && todos.length === 0 ? (
          <p>読み込み中...</p>
        ) : todos.length === 0 ? (
          <p>Todoはまだありません。新しいTodoを追加してください。</p>
        ) : (
          todos.map(todo => (
            <TodoItem
              key={todo.id}
              todo={todo}
              onDelete={handleDeleteTodo}
              onUpdate={handleUpdateTodo}
            />
          ))
        )}
      </div>
    </div>
  );
};

export default TodoList;
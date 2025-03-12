// TodoアプリのAPIクライアント
const API_URL = 'http://localhost:8000';

// すべてのTodoを取得する
export const fetchTodos = async () => {
  const response = await fetch(`${API_URL}/todos/`);
  if (!response.ok) {
    throw new Error('Failed to fetch todos');
  }
  return response.json();
};

// 特定のTodoを取得する
export const fetchTodo = async (id) => {
  const response = await fetch(`${API_URL}/todos/${id}`);
  if (!response.ok) {
    throw new Error(`Failed to fetch todo with id ${id}`);
  }
  return response.json();
};

// 新しいTodoを作成する
export const createTodo = async (todo) => {
  const response = await fetch(`${API_URL}/todos/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(todo),
  });
  if (!response.ok) {
    throw new Error('Failed to create todo');
  }
  return response.json();
};

// Todoを更新する
export const updateTodo = async (id, todo) => {
  const response = await fetch(`${API_URL}/todos/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(todo),
  });
  if (!response.ok) {
    throw new Error(`Failed to update todo with id ${id}`);
  }
  return response.json();
};

// Todoを削除する
export const deleteTodo = async (id) => {
  const response = await fetch(`${API_URL}/todos/${id}`, {
    method: 'DELETE',
  });
  if (!response.ok) {
    throw new Error(`Failed to delete todo with id ${id}`);
  }
  return true;
};
import React, { useState } from 'react';

const TodoItem = ({ todo, onDelete, onUpdate }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editedTodo, setEditedTodo] = useState({ ...todo });

  const handleToggleComplete = () => {
    onUpdate(todo.id, { ...todo, completed: !todo.completed });
  };

  const handleEdit = () => {
    setIsEditing(true);
  };

  const handleSave = () => {
    onUpdate(todo.id, editedTodo);
    setIsEditing(false);
  };

  const handleCancel = () => {
    setEditedTodo({ ...todo });
    setIsEditing(false);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setEditedTodo(prev => ({ ...prev, [name]: value }));
  };

  const handleCheckboxChange = (e) => {
    const { name, checked } = e.target;
    setEditedTodo(prev => ({ ...prev, [name]: checked }));
  };

  return (
    <div className="todo-item" style={{ opacity: todo.completed ? 0.6 : 1 }}>
      {!isEditing ? (
        <>
          <div className="todo-content">
            <input
              type="checkbox"
              checked={todo.completed}
              onChange={handleToggleComplete}
            />
            <div className={`todo-details ${todo.completed ? 'completed' : ''}`}>
              <h3>{todo.title}</h3>
              <p>{todo.description}</p>
            </div>
          </div>
          <div className="todo-actions">
            <button onClick={handleEdit}>編集</button>
            <button onClick={() => onDelete(todo.id)} className="delete-btn">削除</button>
          </div>
        </>
      ) : (
        <div className="todo-edit-form">
          <div>
            <label>タイトル:</label>
            <input
              type="text"
              name="title"
              value={editedTodo.title}
              onChange={handleChange}
            />
          </div>
          <div>
            <label>詳細:</label>
            <textarea
              name="description"
              value={editedTodo.description}
              onChange={handleChange}
            />
          </div>
          <div>
            <label>
              <input
                type="checkbox"
                name="completed"
                checked={editedTodo.completed}
                onChange={handleCheckboxChange}
              />
              完了
            </label>
          </div>
          <div className="edit-actions">
            <button onClick={handleSave}>保存</button>
            <button onClick={handleCancel}>キャンセル</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default TodoItem;
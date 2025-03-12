import React from 'react';
import './App.css';
import TodoList from './components/TodoList';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Todoアプリケーション</h1>
      </header>
      <main>
        <TodoList />
      </main>
      <footer>
        <p>FastAPI + React Todoアプリケーション</p>
      </footer>
    </div>
  );
}

export default App;

// DOM Elements
const taskInput = document.getElementById('taskInput');
const addTaskBtn = document.getElementById('addTask');
const todoList = document.getElementById('todoList');
const completedList = document.getElementById('completedList');

// State
let todos = JSON.parse(localStorage.getItem('todos')) || [];

// Event Listeners
addTaskBtn.addEventListener('click', addTask);
taskInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') addTask();
});

filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentFilter = btn.dataset.filter;
        renderTodos();
    });
});

// Functions
function addTask() {
    const taskText = taskInput.value.trim();
    if (taskText) {
        const todo = {
            id: Date.now(),
            text: taskText,
            completed: false
        };
        todos.push(todo);
        saveToLocalStorage();
        renderTodos();
        taskInput.value = '';
    }
}

function toggleTodo(id) {
    const todoItem = document.querySelector(`[data-id="${id}"]`);
    const todo = todos.find(t => t.id === id);
    
    if (!todo.completed) {
        // Adding completing animation
        todoItem.classList.add('completing');
        
        setTimeout(() => {
            todos = todos.map(t => t.id === id ? { ...t, completed: true } : t);
            saveToLocalStorage();
            renderTodos();
        }, 500); // Match this with CSS transition time
    } else {
        todos = todos.map(t => t.id === id ? { ...t, completed: false } : t);
        saveToLocalStorage();
        renderTodos();
    }
}

function deleteTodo(id) {
    todos = todos.filter(todo => todo.id !== id);
    saveToLocalStorage();
    renderTodos();
}

function saveToLocalStorage() {
    localStorage.setItem('todos', JSON.stringify(todos));
}

function renderTodos() {
    const activeTodos = todos.filter(todo => !todo.completed);
    const completedTodos = todos.filter(todo => todo.completed);

    // Render active todos
    todoList.innerHTML = activeTodos.map(todo => `
        <li class="todo-item" 
            draggable="true" 
            data-id="${todo.id}">
            <input type="checkbox" 
                   onchange="toggleTodo(${todo.id})">
            <span class="task-text">${todo.text}</span>
            <button class="delete-btn" onclick="deleteTodo(${todo.id})">Delete</button>
        </li>
    `).join('');

    // Render completed todos
    completedList.innerHTML = completedTodos.map(todo => `
        <li class="todo-item appearing" 
            draggable="true" 
            data-id="${todo.id}">
            <input type="checkbox" 
                   checked
                   onchange="toggleTodo(${todo.id})">
            <span class="task-text">${todo.text}</span>
            <button class="delete-btn" onclick="deleteTodo(${todo.id})">Delete</button>
        </li>
    `).join('');

    // Add drag and drop event listeners to all todo items
    const todoItems = document.querySelectorAll('.todo-item');
    todoItems.forEach(item => {
        item.addEventListener('dragstart', handleDragStart);
        item.addEventListener('dragend', handleDragEnd);
        item.addEventListener('dragover', handleDragOver);
        item.addEventListener('drop', handleDrop);
        item.addEventListener('dragenter', handleDragEnter);
        item.addEventListener('dragleave', handleDragLeave);
    });
}

// Drag and Drop functionality
let draggedItem = null;

function handleDragStart(e) {
    draggedItem = this;
    this.classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', this.dataset.id);
}

function handleDragEnd(e) {
    this.classList.remove('dragging');
    draggedItem = null;
    document.querySelectorAll('.todo-item').forEach(item => {
        item.classList.remove('drag-over');
    });
}

function handleDragOver(e) {
    if (e.preventDefault) {
        e.preventDefault();
    }
    return false;
}

function handleDragEnter(e) {
    this.classList.add('drag-over');
}

function handleDragLeave(e) {
    this.classList.remove('drag-over');
}

function handleDrop(e) {
    e.preventDefault();
    if (draggedItem === this) return;
    
    // Get the IDs of the dragged and drop target items
    const draggedId = parseInt(draggedItem.dataset.id);
    const dropId = parseInt(this.dataset.id);
    
    // Find the indices of both items
    const draggedIndex = todos.findIndex(todo => todo.id === draggedId);
    const dropIndex = todos.findIndex(todo => todo.id === dropId);
    
    // Reorder the array
    const [draggedTodo] = todos.splice(draggedIndex, 1);
    todos.splice(dropIndex, 0, draggedTodo);
    
    // Save and render
    saveToLocalStorage();
    renderTodos();
}

// Initial render
renderTodos();
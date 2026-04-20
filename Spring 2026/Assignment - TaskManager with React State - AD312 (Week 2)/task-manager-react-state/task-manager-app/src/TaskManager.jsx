import { useState } from "react";

function TaskManager() {
    const [tasks, setTasks] = useState([]);
    const [input, setInput] = useState("");

    const addTask = () => {
        const newTask = {id: Date.now(), title: input, completed: false}
        setTasks([...tasks, newTask]);
        setInput("");
    }

    const toggleTaskCompletion = (id) => {
        setTasks(tasks.map(task => {
            if (task.id === id) {
                return {...task, completed : !task.completed}
            } else {
                return task;
            }
        }));
    };
    
    
    return (
        <div>
            <h1>Task Manager</h1>
            <input type="text" value={input} onChange={(e) => setInput(e.target.value)} placeholder="Please provide an input" />
            <button onClick={addTask}>Add Task</button>
            <ul>
                {tasks.map(task => (
                    <li key={task.id}>
                        <p>Task Title: {task.title}</p>
                        <p>Task Status: {task.completed ? "Completed" : "Not Completed"}</p>
                        <button onClick={() => toggleTaskCompletion(task.id)}>Click to Change Status</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default TaskManager;



// TEST CASES:

// NORMAL TEST CASES:
// Case 1: Provide an input and click 'Add Task' ==> It shows task title and the status as incomplete
// Case 2: Provide duplicated inputs and click 'Add Task' ==> It shows duplicated info
// Case 3: Click 'Click to Change Status' ==> It will change status back and forth

// EDGE TEST CASES:
// Case 1: Refresh the page ==> It restarts and clears all input fields
// Case 2: Click 'Add Task' with an empty input field ==> It does not show the info of task title
// Case 3: Add spaces before the input ==> It displays the input info without spaces

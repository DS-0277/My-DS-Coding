const projectForm = document.querySelector('#project-form');
const taskForm = document.querySelector('#task-form');

function showMessage(selector, text, type) {
  const element = document.querySelector(selector);
  element.textContent = text;
  element.className = `message ${type}`;
}

async function sendJson(url, options) {
  const response = await fetch(url, { headers: { 'Content-Type': 'application/json' }, ...options });
  const body = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(body.error || `Request failed with ${response.status}`);
  return body;
}

projectForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const data = Object.fromEntries(new FormData(projectForm));
  try {
    const project = await sendJson('/api/projects', { method: 'POST', body: JSON.stringify(data) });
    document.querySelector('#project-id').value = project.id;
    showMessage('#project-message', `Created project: ${project.name}. ID copied to the task form.`, 'success');
    projectForm.reset();
  } catch (error) { showMessage('#project-message', error.message, 'error'); }
});

taskForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const data = Object.fromEntries(new FormData(taskForm));
  const projectId = data.projectId;
  delete data.projectId;
  try {
    const task = await sendJson(`/api/projects/${encodeURIComponent(projectId)}/tasks`, { method: 'POST', body: JSON.stringify(data) });
    showMessage('#task-message', `Created task: ${task.title}`, 'success');
    taskForm.reset();
  } catch (error) { showMessage('#task-message', error.message, 'error'); }
});

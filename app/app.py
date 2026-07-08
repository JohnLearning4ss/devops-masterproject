from flask import Flask, request, jsonify, render_template_string
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import redis
import os
import time

app = Flask(__name__)

# Redis connection
r = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

# Prometheus metrics
REQUEST_COUNT = Counter("app_requests_total", "Total requests", ["method", "endpoint"])
REQUEST_LATENCY = Histogram("app_request_latency_seconds", "Request latency")
TODO_COUNT = Counter("todo_operations_total", "Todo operations", ["action"])

HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>DevOps Todo App</title>
  <style>
    body { font-family: sans-serif; max-width: 600px; margin: 60px auto; background: #f0f4f8; }
    h1 { color: #2d3748; }
    input { padding: 8px; width: 70%; border: 1px solid #cbd5e0; border-radius: 4px; }
    button { padding: 8px 16px; background: #4299e1; color: white; border: none; border-radius: 4px; cursor: pointer; }
    ul { list-style: none; padding: 0; }
    li { background: white; padding: 12px; margin: 6px 0; border-radius: 6px; display: flex; justify-content: space-between; }
    .del { color: red; cursor: pointer; border: none; background: none; font-size: 16px; }
    .badge { background: #ebf8ff; color: #2b6cb0; padding: 2px 8px; border-radius: 10px; font-size: 12px; }
  </style>
</head>
<body>
  <h1>📝 DevOps Todo App <span class="badge">Flask + Redis + Docker</span></h1>
  <form onsubmit="addTodo(event)">
    <input id="task" placeholder="Add a task..." required/>
    <button type="submit">Add</button>
  </form>
  <ul id="list"></ul>
  <script>
    async function load() {
      const res = await fetch('/todos');
      const data = await res.json();
      document.getElementById('list').innerHTML = data.todos
        .map(t => `<li>${t} <button class="del" onclick="del('${t}')">✕</button></li>`)
        .join('');
    }
    async function addTodo(e) {
      e.preventDefault();
      const task = document.getElementById('task').value;
      await fetch('/todos', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({task})});
      document.getElementById('task').value = '';
      load();
    }
    async function del(task) {
      await fetch('/todos/' + encodeURIComponent(task), {method:'DELETE'});
      load();
    }
    load();
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    REQUEST_COUNT.labels(method="GET", endpoint="/").inc()
    return render_template_string(HTML)

@app.route("/todos", methods=["GET"])
def get_todos():
    start = time.time()
    REQUEST_COUNT.labels(method="GET", endpoint="/todos").inc()
    todos = r.lrange("todos", 0, -1)
    REQUEST_LATENCY.observe(time.time() - start)
    return jsonify({"todos": todos})

@app.route("/todos", methods=["POST"])
def add_todo():
    REQUEST_COUNT.labels(method="POST", endpoint="/todos").inc()
    data = request.get_json()
    task = data.get("task", "").strip()
    if task:
        r.rpush("todos", task)
        TODO_COUNT.labels(action="add").inc()
    return jsonify({"status": "added", "task": task}), 201

@app.route("/todos/<task>", methods=["DELETE"])
def delete_todo(task):
    REQUEST_COUNT.labels(method="DELETE", endpoint="/todos").inc()
    r.lrem("todos", 0, task)
    TODO_COUNT.labels(action="delete").inc()
    return jsonify({"status": "deleted"})

@app.route("/health")
def health():
    try:
        r.ping()
        return jsonify({"status": "healthy", "redis": "up"})
    except Exception:
        return jsonify({"status": "unhealthy", "redis": "down"}), 500

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

import azure.functions as func
import json

def main(req: func.HttpRequest) -> func.HttpResponse:

    # Sample data (real-time demo data)
    users = [
        {"id": 1, "name": "veera-don", "role": "DevOps Engineeeer"},
        {"id": 2, "name": "nareshit", "role": "Backend Developer"},
        {"id": 3, "name": "vsv", "role": "Cloud Engineer"}
    ]

    # If query param 'api=true' → act as API
    api = req.params.get('api')
    name = req.params.get('name')

    # ---------------- API MODE ----------------
    if api == "true":
        if name:
            user = next((u for u in users if u["name"].lower() == name.lower()), None)
            if user:
                return func.HttpResponse(
                    json.dumps(user),
                    mimetype="application/json"
                )
            else:
                return func.HttpResponse(
                    json.dumps({"message": "User not found"}),
                    status_code=404,
                    mimetype="application/json"
                )

        return func.HttpResponse(
            json.dumps(users),
            mimetype="application/json"
        )

    # ---------------- VIEW MODE ----------------
    html_page = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>User Viewer</title>
        <style>
            body { font-family: Arial; margin: 40px; }
            button { padding: 8px 12px; margin: 5px; }
            .card {
                border: 1px solid #ddd;
                padding: 10px;
                margin-top: 10px;
                border-radius: 5px;
            }
        </style>
    </head>
    <body>

    <h2>User Details Viewer</h2>

    <input type="text" id="username" placeholder="Enter user name" />
    <br><br>

    <button onclick="getUser()">Get User</button>
    <button onclick="getAllUsers()">Get All Users</button>

    <div id="result"></div>

    <script>
        const FUNCTION_KEY = "L_18nmjVkxRyShg06JVjKFsQ9Yu03OB_VhxHGCe1z7XeAzFuHlEETg==";
        const API_URL = `/api/HttpExample?api=true&code=${FUNCTION_KEY}`;
        function getUser() {
            const name = document.getElementById("username").value;
            fetch(`${API_URL}&name=${name}`)
                .then(res => res.json())
                .then(data => showResult(data));
        }

        function getAllUsers() {
            fetch(API_URL)
                .then(res => res.json())
                .then(data => showResult(data));
        }

        function showResult(data) {
            const result = document.getElementById("result");
            result.innerHTML = "";

            if (Array.isArray(data)) {
                data.forEach(user => {
                    result.innerHTML += `
                        <div class="card">
                            <b>ID:</b> ${user.id}<br>
                            <b>Name:</b> ${user.name}<br>
                            <b>Role:</b> ${user.role}
                        </div>`;
                });
            } else {
                result.innerHTML = `
                    <div class="card">
                        <b>ID:</b> ${data.id || ""}<br>
                        <b>Name:</b> ${data.name || data.message}<br>
                        <b>Role:</b> ${data.role || ""}
                    </div>`;
            }
        }
    </script>

    </body>
    </html>
    """

    return func.HttpResponse(
        html_page,
        mimetype="text/html"
    )

LOGIN_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Orion</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {
            padding: 0;
            margin: 0;
            box-sizing: border-box;
        }
        body {
            width: 100vw;
            height: 100vh;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background-color: rgb(192, 83, 79);
            color: white;
        }

        .container {
            width: 300px;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            background-color: rgba(255, 255, 255, 0.123);
        }

        h2 {
            text-align: center;
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 10px;
        }

        input[type="text"],
        input[type="password"] {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #cccccc50;
            border-radius: 3px;
            background-color: transparent;
            outline: none;
            color: white;
        }

        label {
            font-size: 14px;
        }

        button {
            background-color: #333;
            color: white;
            font-weight: bold;
            padding: 10px 20px;
            border: none;
            border-radius: 3px;
            cursor: pointer;
            margin-left: auto;
        }
    </style>
</head>

<body>

    <div class="container">
        <h2>Admin Login</h2>
        <label for="username">Username</label>
        <input type="text" id="username" name="username" required>

        <label for="password">Password</label>
        <input type="password" id="password" name="password" required>

        <button type="button" onclick="login()">Login</button>
    </div>
    <p id="status"></p>

    <script>
        const status = document.getElementById("status");

        async function login() {
            const username = document.getElementById("username").value;
            const password = document.getElementById("password").value;
            if (username === "" || password === "") {
                alert("Please enter both username and password.");
                return;
            }
            const hashed = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(password));
            const hashArray = Array.from(new Uint8Array(hashed));
            const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
            const auth = `${username}:${hashHex}`;
            const response = await fetch("/admin/login", {
                method: "POST",
                headers: {
                    "X-Authorization-Token": auth
                },
            });
            const data = await response.json();
            status.textContent = data.message;
            if (response.ok) {
                window.location.href = "/admin/dashboard";
            }
        }
    </script>

</body>

</html>
"""

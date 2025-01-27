DASHBOARD = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Dashboard</title>
    <link
      rel="stylesheet"
      href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@48,400,1,0"
    />
    <style>
      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }

      body {
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
          Roboto, Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue",
          sans-serif;
        width: 100vw;
        height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
        background-color: #333;
      }

      header {
        width: 100%;
        padding: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #ffffff18;
        color: white;
        background-color: #6e6bfd;
      }

      header h2 {
        font-size: 1.4rem;
        font-weight: 400;
      }

      header button {
        border: none;
        cursor: pointer;
        padding: 5px;
        display: flex;
        justify-content: center;
        align-items: center;
        border-radius: 50%;
        color: #6e6bfd;
      }
      
      main {
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: flex-start;
        align-items: center;
        flex-grow: 1;
      }

      .navbar {
        width: 15%;
        min-width: 250px;
        height: 100%;
        background-color: #333;
        border-right: 1px solid #ffffff18;
      }

      .navbar ul {
        list-style: none;
        padding: 10px;
      }

      .navbar ul li {
        padding: 10px;
        color: white;
        cursor: pointer;
        border-radius: 5px;
      }

      .navbar ul li ul li:hover {
        background-color: #ffffff18;
      }
      
    .view {
        width: 100%;
        height: 100%;
        background-color: #333;
        padding: 10px;
        color: white;
        overflow-y: auto;
    }
    
    .view ul {
        list-style: none;
        padding: 10px;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        justify-content: flex-start;
    }
    
    .view ul li {
        width: 100%;
        padding: 0 5px;
        color: white;
        display: flex;
        border: 1px solid #ffffff18;
    }
    
    .view ul li p {
        text-align: left;
        border-right: 1px solid #ffffff18;
        padding: 5px;
        width: 200px;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .view ul li p:last-child {
        border-right: none;
    }

    </style>
  </head>

  <body>
    <header>
      <h2>Orion</h2>
      <button>
        <span class="material-symbols-rounded">settings</span>
      </button>
    </header>
    <main>
      <div class="navbar">
        <ul id="dblist"></ul>
      </div>
      <div class="view"></div>
    </main>
    <script>
        const dblist = document.getElementById("dblist");
        const navbar = document.querySelector(".navbar");
        const navbarItems = document.querySelectorAll(".navbar ul li");

        document.addEventListener("DOMContentLoaded", async () => {
            const res = await fetch("/admin/api/bases");
            const data = await res.json();
            data.bases.forEach((baseId) => {
                const base = document.createElement("li");
                base.id = baseId;
                const p = document.createElement("p");
                p.textContent = baseId;
                base.appendChild(p);
                base.addEventListener("click", async () => {
                    const res = await fetch(`/admin/api/bases/${baseId}`);
                    const data = await res.json();
                    const tables = document.createElement("ul");
                    tables.style.borderLeft = "1px solid #ffffff18";
                    data.tables.forEach((tableId) => {
                        const table = document.createElement("li");
                        table.textContent = tableId;
                        table.id = tableId;
                        table.addEventListener("click", async (ev) => {
                            ev.stopPropagation();
                            const res = await fetch(`/admin/api/bases/${baseId}/tables/${tableId}`);
                            const data = await res.json();
                            const dbTable = document.createElement("ul");
                            const firstRowKeys = Object.keys(data[0]);
                            const headerRow = document.createElement("li");
                            firstRowKeys.forEach((key) => {
                                const p = document.createElement("p");
                                p.innerHTML = `<strong>${key}</strong>`;
                                headerRow.appendChild(p);
                            });
                            dbTable.appendChild(headerRow);
                            data.forEach((row) => {
                                const li = document.createElement("li");
                                for (const key in row) {
                                    const p = document.createElement("p");
                                    p.innerHTML = `<span>${row[key]}</span>`;
                                    li.appendChild(p);
                                }
                                dbTable.appendChild(li);
                            });
                            const view = document.querySelector(".view");
                            view.innerHTML = "";
                            const title = document.createElement("p");
                            
                            title.style.padding = "10px";
                            title.textContent = tableId;
                            view.appendChild(title);
                            view.appendChild(dbTable);
                        });
                        tables.appendChild(table);
                    });
                    if (base.children.length > 1) {
                        base.removeChild(base.children[1]);
                    } else {
                        base.appendChild(tables);
                    }
                });
                dblist.appendChild(base);
            });
        });
    </script>
  </body>
</html>
"""

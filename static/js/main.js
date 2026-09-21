// Fetches server info from the Flask API and renders it on the page.

const LABELS = {
  app: "App",
  python: "Python",
  server_time: "Server time (UTC)",
  uptime_seconds: "Uptime (s)",
};

async function loadInfo() {
  const list = document.getElementById("info");
  try {
    const res = await fetch("/api/info");
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    list.replaceChildren();
    addRow(list, "Status", "Online");
    for (const [key, label] of Object.entries(LABELS)) {
      addRow(list, label, data[key]);
    }
  } catch (err) {
    list.replaceChildren();
    addRow(list, "Status", `Error: ${err.message}`);
  }
}

function addRow(list, label, value) {
  const dt = document.createElement("dt");
  const dd = document.createElement("dd");
  dt.textContent = label;
  dd.textContent = value;
  list.append(dt, dd);
}

document.getElementById("refresh").addEventListener("click", loadInfo);
loadInfo();

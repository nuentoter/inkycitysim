const ws = new WebSocket("ws://localhost:8000/ws");

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);

    renderMap(data.npcs);
    renderIdentity(data.npcs);
    renderCase(data.case);
    renderFeed(data.feed);
};

function renderMap(npcs) {
    let grid = Array.from({length: 10}, () => Array(10).fill("."));

    Object.values(npcs).forEach(npc => {
        grid[npc.y][npc.x] = npc.name?.[0] || "N";
    });

    document.getElementById("map").innerText =
        "MAP\n\n" + grid.map(r => r.join(" ")).join("\n");
}

function renderIdentity(npcs) {
    let out = "IDENTITY CLOUDS\n\n";

    for (let name in npcs) {
        let n = npcs[name];
        out += `${name}\nA:${n.A.toFixed(2)} B:${n.B.toFixed(2)} C:${n.C.toFixed(2)}\n\n`;
    }

    document.getElementById("identity").innerText = out;
}

function renderCase(caseData) {
    let out = "CASE GRAPH\n\n";

    for (let k in caseData) {
        out += `${k}: ${(caseData[k] * 100).toFixed(1)}%\n`;
    }

    document.getElementById("case").innerText = out;
}

function renderFeed(feed) {
    document.getElementById("feed").innerText =
        "LIVE FEED\n\n" + feed.join("\n");
}

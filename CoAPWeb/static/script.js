// script.js - Smart Home Dashboard Logic


let allNodes = [];
let userNodes = [];

document.addEventListener('DOMContentLoaded', () => {
  fetchNodes();
  fetchUserNodes();
});

function fetchNodes() {
  fetch('/api/nodes')
    .then(response => response.json())
    .then(data => {
      allNodes = data.nodes;
      renderNodeList();
    })
    .catch(err => {
      document.getElementById('node-ipv6-list').innerHTML = '<span class="error">Failed to load nodes</span>';
    });
}

function fetchUserNodes() {
  fetch('/api/user_nodes')
    .then(response => response.json())
    .then(data => {
      userNodes = data;
      renderUserNodeList();
      renderNodeList(); // update dashboard buttons
    });
}

function addToUserUI(ipv6) {
  const node = allNodes.find(n => n.ipv6 === ipv6);
  if (!node) return;
  const name = prompt('Enter a name for this LED:', node.name || 'LED Device');
  if (name === null) return; // Cancelled
  const nodeWithName = { ...node, name };
  fetch('/api/user_nodes', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(nodeWithName)
  })
    .then(() => {
      fetchUserNodes();
    });
}

function renderNodeList() {
  const nodeList = document.getElementById('node-list');
  nodeList.innerHTML = '';
  if (!allNodes || allNodes.length === 0) {
    nodeList.innerHTML = '<li>No nodes found</li>';
    return;
  }
  allNodes.forEach(node => {
    const li = document.createElement('li');
    const alreadyAdded = userNodes.some(u => u.ipv6 === node.ipv6);
    li.className = 'node-item' + (alreadyAdded ? ' greyed-out' : '');
    li.innerHTML = `
      <div class="node-info">
        <span class="node-label">${node.name || 'Node'}</span>
        <span class="node-ip">${node.ipv6}</span>
      </div>
      <div class="node-controls">
        <button onclick="addToUserUI('${node.ipv6}')" ${alreadyAdded ? 'disabled' : ''}>Add to UI</button>
      </div>
    `;
    nodeList.appendChild(li);
  });
}


// Track LED state for each device (default: off)
let ledStates = {};

function renderUserNodeList() {
  const userNodeList = document.getElementById('user-node-list');
  userNodeList.innerHTML = '';
  if (!userNodes || userNodes.length === 0) {
    userNodeList.innerHTML = '<li>No devices available</li>';
    return;
  }
  userNodes.forEach(node => {
    const li = document.createElement('li');
    li.className = 'user-node-item';
    // Default state is off if not set
    if (!(node.ipv6 in ledStates)) ledStates[node.ipv6] = false;
    const btnText = ledStates[node.ipv6] ? 'Turn Off' : 'Turn On';
    const bulbIcon = ledStates[node.ipv6] ? '💡' : '💡<span style="filter: grayscale(100%) brightness(0.7);">';
    const bulbImgId = `bulb-img-${node.ipv6.replace(/[^a-zA-Z0-9]/g, '')}`;
    const bulbImg = `<img src="${ledStates[node.ipv6] ? '/static/light_on.png' : '/static/light_off.png'}" class="bulb-icon" alt="Light" id="${bulbImgId}">`;
    li.innerHTML = `
      <div class="user-node-info">
        ${bulbImg}
        <span class="user-node-label">${node.name || 'LED Device'}</span>
      </div>
      <div class="user-node-controls">
        <button onclick="toggleLed('${node.ipv6}', this, '${bulbImgId}')">${btnText}</button>
      </div>
    `;
    userNodeList.appendChild(li);

  });
}



function toggleLed(ipv6, btn, bulbImgId) {
  btn.disabled = true;
  const newState = !ledStates[ipv6];
  const action = newState ? 'on' : 'off';
  fetch(`/api/led/${encodeURIComponent(ipv6)}/${action}`, { method: 'POST' })
    .then(response => response.json())
    .then(data => {
      btn.disabled = false;
      ledStates[ipv6] = newState;
      btn.textContent = newState ? 'Turn Off' : 'Turn On';
      // Update bulb image instantly
      const bulbImg = document.getElementById(bulbImgId);
      if (bulbImg) {
        bulbImg.src = newState ? '/static/light_on.png' : '/static/light_off.png';
      }
    })
    .catch(() => {
      btn.disabled = false;
      alert('Failed to toggle LED');
    });
}

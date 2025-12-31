// Clear User UI list (frontend only, does not affect backend or dashboard)
function clearUserUI() {
  userNodes = [];
  renderUserNodeList();
}

// Attach clear button event after DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  const clearBtn = document.getElementById('clear-user-ui-btn');
  if (clearBtn) clearBtn.onclick = clearUserUI;
});
// script.js - Smart Home Dashboard Logic


let allNodes = [];
let userNodes = [];

document.addEventListener('DOMContentLoaded', () => {
  fetchNodes();
  fetchUserNodes();
});

function fetchNodes() {
  const loadingDiv = document.getElementById('node-loading');
  const nodeList = document.getElementById('node-list');
  if (loadingDiv) loadingDiv.style.display = 'flex';
  if (nodeList) nodeList.style.display = 'none';
  fetch('/api/nodes')
    .then(response => response.json())
    .then(data => {
      allNodes = data.nodes;
      renderNodeList();
      if (loadingDiv) loadingDiv.style.display = 'none';
      if (nodeList) nodeList.style.display = '';
    })
    .catch(err => {
      if (loadingDiv) loadingDiv.style.display = 'none';
      if (nodeList) nodeList.style.display = '';
      nodeList.innerHTML = '<span class="error">Failed to load nodes</span>';
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


// Show a modal popup to set the node name, with correct node type and icon
function addToUserUI(ipv6) {
  const node = allNodes.find(n => n.ipv6 === ipv6);
  if (!node) return;
  const modal = document.getElementById('set-name-modal');
  const title = document.getElementById('set-name-title');
  const icon = document.getElementById('set-name-type-icon');
  const label = document.getElementById('set-name-type-label');
  const input = document.getElementById('set-name-input');
  const okBtn = document.getElementById('set-name-ok-btn');
  const cancelBtn = document.getElementById('set-name-cancel-btn');
  if (!modal || !title || !icon || !label || !input || !okBtn || !cancelBtn) return;

  // Set modal content based on node type
  let typeLabel = 'Unknown';
  let iconSrc = '';
  const typeUpper = node.type ? node.type.toUpperCase() : '';
  if (typeUpper === 'SENSOR') {
    typeLabel = 'Sensor';
    iconSrc = '/static/sensor.png';
  } else if (typeUpper === 'LED') {
    typeLabel = 'LED';
    iconSrc = '/static/light_on.png';
  } else {
    typeLabel = node.type || 'Unknown';
    iconSrc = '/static/gpn.png';
  }
  title.textContent = 'Set Name for ' + typeLabel + ' Node';
  icon.src = iconSrc;
  label.textContent = typeLabel;
  input.value = node.name || '';
  input.focus();

  modal.style.display = 'flex';

  // Remove any previous event listeners
  okBtn.onclick = null;
  cancelBtn.onclick = null;

  okBtn.onclick = function() {
    const name = input.value.trim();
    if (!name) {
      input.focus();
      return;
    }
    modal.style.display = 'none';
    const nodeWithName = { ...node, name };
    fetch('/api/user_nodes', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(nodeWithName)
    })
      .then(() => {
        fetchUserNodes();
      });
  };
  cancelBtn.onclick = function() {
    modal.style.display = 'none';
  };
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
        <span class="node-type">Type: <b>${node.type || 'Unknown'}</b></span>
      </div>
      <div class="node-controls">
        <button onclick="addToUserUI('${node.ipv6}')" ${alreadyAdded ? 'disabled class=\"added-to-ui\"' : ''}>Add to UI</button>
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
    const typeUpper = node.type ? node.type.toUpperCase() : '';
    if (typeUpper === 'SENSOR') {
      // Sensor UI: icon, label for data, and an Update button
      const sensorImgId = `sensor-img-${node.ipv6.replace(/[^a-zA-Z0-9]/g, '')}`;
      const sensorDataId = `sensor-data-${node.ipv6.replace(/[^a-zA-Z0-9]/g, '')}`;
      li.innerHTML = `
        <div class="user-node-info">
          <img src="/static/sensor.png" class="sensor-icon" alt="Sensor" id="${sensorImgId}" style="width:32px;height:32px;vertical-align:middle;">
          <span class="user-node-label">${node.name || 'Sensor Device'}</span>
        </div>
        <div class="user-node-controls">
          <label id="${sensorDataId}" class="sensor-data-label" style="display:inline-block;width:120px;margin-right:8px;vertical-align:middle;">--</label>
          <button onclick="updateSensorData('${node.ipv6}', '${sensorDataId}')">Update</button>
        </div>
      `;
    } else if (typeUpper === 'LED') {
      // LED UI
      if (!(node.ipv6 in ledStates)) ledStates[node.ipv6] = false;
      const btnText = ledStates[node.ipv6] ? 'Turn Off' : 'Turn On';
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
    } else {
      // Fallback for unknown types: use gpn.png
      const gpnImgId = `gpn-img-${node.ipv6.replace(/[^a-zA-Z0-9]/g, '')}`;
      li.innerHTML = `
        <div class="user-node-info">
          <img src="/static/gpn.png" class="gpn-icon" alt="Unknown" id="${gpnImgId}" style="width:32px;height:32px;vertical-align:middle;">
          <span class="user-node-label">${node.name || 'Unknown Device'}</span>
        </div>
      `;
    }
    userNodeList.appendChild(li);
  });


// Fetch sensor data from the node's /sensor/data endpoint and update the label
function updateSensorData(ipv6, dataLabelId) {
  const label = document.getElementById(dataLabelId);
  if (label) label.textContent = '...';
  // Use the backend API that proxies CoAP /sensor/data
  fetch(`/api/sensor_data/${encodeURIComponent(ipv6)}`)
    .then(response => response.json())
    .then(data => {
      if (label) label.textContent = data.value !== undefined ? data.value : (typeof data === 'string' ? data : 'N/A');
    })
    .catch(() => {
      if (label) label.textContent = 'Error';
    });
}
// Expose to global scope for inline HTML onclick
window.updateSensorData = updateSensorData;
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

document.addEventListener('DOMContentLoaded', function() {
  loadNodes();
  loadUserNodes();
});

function loadNodes() {
  fetch('/api/nodes')
    .then(res => res.json())
    .then(nodes => {
      // Show IPv6 list at the top
      const ipv6Div = document.getElementById('node-ipv6-list');
      if (nodes.length > 0) {
        ipv6Div.innerHTML = '<b>Discovered IPv6 addresses:</b><br>' + nodes.map(n => n.ipv6).join('<br>');
      } else {
        ipv6Div.innerHTML = '<b>No nodes discovered.</b>';
      }
      // List nodes with add button
      const list = document.getElementById('node-list');
      list.innerHTML = '';
      nodes.forEach(node => {
        const li = document.createElement('li');
        li.className = 'node-item';
        li.innerHTML = `<span>${node.ipv6} (${node.type})</span>`;
        const addBtn = document.createElement('button');
        addBtn.textContent = 'Add to UI';
        addBtn.onclick = () => addToUserUI(node);
        li.appendChild(addBtn);
        list.appendChild(li);
      });
    });
}

function addToUserUI(node) {
  fetch('/api/user_nodes', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(node)
  }).then(() => loadUserNodes());
}

function loadUserNodes() {
  fetch('/api/user_nodes')
    .then(res => res.json())
    .then(nodes => {
      const list = document.getElementById('user-node-list');
      list.innerHTML = '';
      nodes.forEach(node => {
        const li = document.createElement('li');
        li.className = 'user-node-item';
        li.innerHTML = `<span>${node.ipv6} (${node.type})</span>`;
        if (node.type === 'LED') {
          const onBtn = document.createElement('button');
          onBtn.textContent = 'ON';
          onBtn.onclick = () => ledControl(node.ipv6, 'on');
          const offBtn = document.createElement('button');
          offBtn.textContent = 'OFF';
          offBtn.onclick = () => ledControl(node.ipv6, 'off');
          li.appendChild(onBtn);
          li.appendChild(offBtn);
        } else if (node.type === 'Sensor') {
          const statusBtn = document.createElement('button');
          statusBtn.textContent = 'Get Status';
          statusBtn.onclick = () => alert('Sensor status API not implemented yet.');
          li.appendChild(statusBtn);
        }
        list.appendChild(li);
      });
    });
}

function ledControl(ipv6, action) {
  fetch(`/api/led/${ipv6}/${action}`, {method: 'POST'})
    .then(res => res.json())
    .then(result => {
      if (result.status !== 'ok') {
        alert('Error: ' + (result.message || result.stderr));
      }
    });
}

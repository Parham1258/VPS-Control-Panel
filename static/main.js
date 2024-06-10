function getCookie(name) {
  let ans = null;
  document.cookie.split('; ').map(r=>{if(r.split('=')[0]===name){ans=r.split('=')[1]}});
  return ans;
}

function servers() {
  document.getElementById('ref').innerHTML = 'Refresh...'
  fetch('/api/servers')
    .then(async res => {
      res = await res.json();
      if (res.status === 'success') {
        document.getElementById('servers').innerHTML = res.servers.map(s=>`<a href="/server?id=${s.ID}">
  <div class="server status-${s.Status}">
    <p>${s.Name}</p>
  </div>
</a>`).join('');
        document.getElementById('ref').innerHTML = 'Refresh'
      } else {
        document.getElementById('servers').innerHTML = 'Failed to load servers';
      }
    })
}

if (!getCookie('Key')) {
  document.getElementById('servers').innerHTML = 'Set a key to view servers';
  document.getElementById('keyask').showModal()
} else {
  servers()
}

function setKey() {
  document.cookie = 'Key='+document.getElementById('key').value;
  location.reload()
}
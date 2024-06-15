let id = location.search.replace('?','').split('&').map(e=>e.split('=')).filter(e=>e[0]==='id')[0][1];

function action(name) {
  document.getElementById('btns').style.cursor = 'not-allowed';
  Array.from(document.getElementById('btns').children).forEach(e=>{
    e.style['pointer-events'] = 'none';
  })
  const formData = new FormData();
  formData.append("ID", id);
  document.getElementById('loading').showModal()
  fetch('/api/'+name, {
    method: 'POST',
    body: formData
  })
    .then(async res => {
      res = await res.json();
      document.getElementById('btns').style.cursor = 'auto';
      Array.from(document.getElementById('btns').children).forEach(e=>{
        e.style['pointer-events'] = 'auto';
      })
      document.getElementById('loading').close()
      if (res.status === 'success') {
        document.getElementById('stat').innerHTML = 'Action successful';
        document.getElementById('res').showModal()
        fetch('/api/server_status?id='+id).then(async res=>{
          res = await res.json();
          document.getElementById('status').classList = 'status-'+res.Status
        })
      } else {
        document.getElementById('stat').innerHTML = 'Action failed<br>Error: '+res.error.replace('Error: ', '');
        document.getElementById('res').showModal()
      }
    })
}

let ac = '';
function danger(name) {
  ac = name;
  document.getElementById('sure').showModal()
}
function con() {
  document.getElementById('sure').close()
  action(ac)
}
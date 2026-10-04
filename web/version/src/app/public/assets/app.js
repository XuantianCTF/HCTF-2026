const form = document.getElementById('login');
const out = document.getElementById('out');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const username = document.getElementById('username').value;
  const res = await fetch('/login', {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ username }),
  });
  out.textContent = JSON.stringify(await res.json(), null, 2);
});

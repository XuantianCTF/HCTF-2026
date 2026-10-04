const express = require('express');
const crypto = require('crypto');
const path = require('path');

const userRoutes = require('./routes/user');
const adminRoutes = require('./routes/admin');

const app = express();
app.disable('x-powered-by');
app.use(express.json());

// ---------------------------------------------------------------------------
// In-memory account store.
//
// The bootstrap admin is created on every boot. Its `apiKey` is generated at
// runtime so that it never touches the disk, and there is deliberately no
// route that exposes the environment to the outside.
// ---------------------------------------------------------------------------
const users = [
  {
    id: 1,
    username: 'admin',
    role: 'admin',
    apiKey: crypto.randomBytes(16).toString('hex'),
  },
  {
    id: 2,
    username: 'guest',
    role: 'user',
    apiKey: null,
  },
];

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.use('/assets', express.static(path.join(__dirname, 'public', 'assets')));

app.post('/login', (req, res) => {
  const username = String((req.body && req.body.username) || '').trim();
  if (!username) return res.status(400).json({ error: 'username required' });

  let user = users.find((u) => u.username === username);
  if (!user) {
    user = { id: users.length + 1, username, role: 'user', apiKey: null };
    users.push(user);
  }

  res.setHeader('Set-Cookie', `sid=${Buffer.from(user.username).toString('base64')}; Path=/`);
  res.json({ ok: true, id: user.id, username: user.username, role: user.role });
});

app.use('/api', userRoutes(users));
app.use('/admin', adminRoutes(users));

// Deployment helper: expose the VCS metadata so the build agent can diff a
// checkout against the running release. Hidden directories are whitelisted on
// purpose.
app.use('/.svn', express.static(path.join(__dirname, '.svn'), { dotfiles: 'allow' }));

app.use((req, res) => res.status(404).json({ error: 'not found' }));

const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`release panel listening on :${port}`));

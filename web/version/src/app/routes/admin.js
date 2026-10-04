const express = require('express');
const crypto = require('crypto');
const { exec } = require('child_process');

function apiKeyMatches(supplied, expected) {
  if (!supplied || !expected) return false;
  const a = Buffer.from(supplied);
  const b = Buffer.from(expected);
  if (a.length !== b.length) return false;
  return crypto.timingSafeEqual(a, b);
}

module.exports = function adminRoutes(users) {
  const router = express.Router();

  // Only accounts carrying a valid admin API key may trigger a release
  // archive. `target` selects the directory to archive.
  router.post('/backup', (req, res) => {
    const key = req.get('x-api-key') || '';
    const admin = users.find((u) => u.role === 'admin' && apiKeyMatches(key, u.apiKey));
    if (!admin) return res.status(403).json({ error: 'admin api key required' });

    const target = (req.body && req.body.target) || '/srv/www';

    exec(`tar -czf /tmp/release_${Date.now()}.tar.gz ${target}`, (err, stdout, stderr) => {
      res.json({ ok: !err, stdout, stderr });
    });
  });

  return router;
};

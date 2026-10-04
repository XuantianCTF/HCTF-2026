const express = require('express');

module.exports = function userRoutes(users) {
  const router = express.Router();

  // Public profile lookup. The `id` is only ever used as an index into the
  // store, callers are trusted because "profiles are not sensitive".
  router.get('/profile/:id', (req, res) => {
    const id = Number.parseInt(req.params.id, 10);
    if (Number.isNaN(id)) return res.status(400).json({ error: 'bad id' });

    const user = users.find((u) => u.id === id);
    if (!user) return res.status(404).json({ error: 'user not found' });

    res.json({
      id: user.id,
      username: user.username,
      role: user.role,
      apiKey: user.apiKey,
    });
  });

  return router;
};

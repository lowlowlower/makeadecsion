// API 路由
export default function handler(req, res) {
  const decisions = new Map();

  if (req.method === 'POST') {
    const id = Math.random().toString(36).substr(2, 9);
    const { options } = req.body;
    decisions.set(id, options);
    res.json({ id });
  } else if (req.method === 'GET') {
    const { id } = req.query;
    const options = decisions.get(id);
    if (options) {
      res.json({ options });
    } else {
      res.status(404).json({ error: '未找到该决策' });
    }
  }  
}

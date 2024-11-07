import { useState } from 'react'

export default function Home() {
  const [options, setOptions] = useState(['']);
  const [result, setResult] = useState('');
  const [shareLink, setShareLink] = useState('');

  const addOption = () => {
    setOptions([...options, '']);
  };

  const updateOption = (index, value) => {
    const newOptions = [...options];
    newOptions[index] = value;
    setOptions(newOptions);
  };

  const removeOption = (index) => {
    if (options.length > 1) {
      const newOptions = options.filter((_, i) => i !== index);
      setOptions(newOptions);
    }
  };

  const roll = () => {
    const validOptions = options.filter(opt => opt.trim() !== '');
    if (validOptions.length === 0) {
      alert('请至少输入一个选项！');
      return;
    }
    const randomIndex = Math.floor(Math.random() * validOptions.length);
    setResult(`决定了！是：${validOptions[randomIndex]}`);
  };

  const shareOptions = async () => {
    const validOptions = options.filter(opt => opt.trim() !== '');
    if (validOptions.length === 0) {
      alert('请至少输入一个选项！');
      return;
    }

    try {
      const response = await fetch('/api/decisions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ options: validOptions }),
      });
      const data = await response.json();
      setShareLink(`${window.location.origin}?id=${data.id}`);
    } catch (error) {
      alert('生成分享链接失败');
    }
  };

  return (
    <div className="container">
      <h1>决策骰子</h1>
      
      <div className="options">
        {options.map((option, index) => (
          <div key={index} className="option-input">
            <input
              type="text"
              value={option}
              onChange={(e) => updateOption(index, e.target.value)}
              placeholder="输入选项"
            />
            <button onClick={() => removeOption(index)}>删除</button>
          </div>
        ))}
        <button onClick={addOption}>添加选项</button>
      </div>

      <div className="dice" onClick={roll}>🎲</div>
      <div className="result">{result}</div>

      <div className="share-section">
        <button onClick={shareOptions}>生成分享链接</button>
        {shareLink && (
          <div>
            <input type="text" value={shareLink} rea

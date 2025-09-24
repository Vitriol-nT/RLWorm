let playerDirection = null;
let gameEnded = false;

document.addEventListener('keydown', (event) => {
  if (gameEnded) return;

  switch (event.key) {
    case 'w': case 'ArrowUp': playerDirection = 'u'; break;
    case 'a': case 'ArrowLeft': playerDirection = 'l'; break;
    case 's': case 'ArrowDown': playerDirection = 'd'; break;
    case 'd': case 'ArrowRight': playerDirection = 'r'; break;
    default: return;
  }
});

async function updateGame() {
  if (gameEnded) return;

  try {
    if (playerDirection) {
      await fetch('/move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ direction: playerDirection })
      });
    }

    const playerRes = await fetch('/state');
    const playerData = await playerRes.json();
    renderGrid('.player', playerData.place);
    document.querySelector('.score').textContent = `score: ${playerData.score}`;

    const aiRes = await fetch('/GetStateDQN', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ DQNdirection: playerDirection })
    });
    if (aiRes.status !== 204) {
      const aiData = await aiRes.json();
      renderGrid('.Agent', aiData.AIPlace);
      document.querySelector('.scoreAI').textContent = `score: ${aiData.AIScore}`;
      console.log('AI moved:', aiData.AIMove);
    }

    const endRes = await fetch('/finish');
    const endData = await endRes.json();
    if (endData.End) {
      gameEnded = true;
      document.querySelector('.score').textContent += " - GAME OVER";
    }

  } catch (err) {
    console.error(err);
  }
}

function renderGrid(selector, place) {
  const grid = document.querySelector(selector);
  grid.innerHTML = '';

  for (let y = 0; y < place.length; y++) {
    for (let x = 0; x < place[y].length; x++) {
      const cell = document.createElement('div');
      cell.classList.add('cell');

      if (place[y][x] === 1) cell.classList.add('white');
      else if (place[y][x] === 2) cell.classList.add('red');
      else cell.classList.add('black');

      grid.appendChild(cell);
    }
  }
}

const gameLoop = setInterval(() => {
  if (gameEnded) {
    clearInterval(gameLoop);
    return;
  }
  updateGame();
}, 100);

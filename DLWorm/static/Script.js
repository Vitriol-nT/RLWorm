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

function updateGame() {
  if (gameEnded) return;

  // keep moving in the last chosen direction
  if (playerDirection) {
    fetch('/move', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ direction: playerDirection })
    }).catch(err => console.error(err));
  }

  fetch('/state')
    .then(res => res.json())
    .then(data => {
      renderPlayerGrid(data.place);
      document.querySelector('.score').textContent = `score: ${data.score}`;
      return fetch('/finish');
    })
    .then(res => res.json())
    .then(endData => {
      if (endData.End) {
        gameEnded = true;
        document.querySelector('.score').textContent += " - GAME OVER";
      }
    })
    .catch(err => console.error(err));
}

function renderPlayerGrid(place) {
  const grid = document.querySelector('.player');
  grid.innerHTML = '';

  for (let y = 0; y < place.length; y++) {
    for (let x = 0; x < place[y].length; x++) {
      const cell = document.createElement('div');
      cell.classList.add('cell');

      if (place[y][x] === 1) {
        cell.classList.add('white');
      } else if (place[y][x] === 2) {
        cell.classList.add('red');
      } else {
        cell.classList.add('black');
      }

      grid.appendChild(cell);
    }
  }
}

// update every 500ms until game over
const gameLoop = setInterval(() => {
  if (gameEnded) {
    clearInterval(gameLoop);
    return;
  }
  updateGame();
}, 100);

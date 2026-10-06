let board = new Array(16).fill(0);
let currentTurn = 1; // 1 = humano, 2 = IA
let gameOver = false;

const boardEl = document.getElementById('board');
const statusEl = document.getElementById('status-message');
const resetBtn = document.getElementById('reset-btn');
const modeSelect = document.getElementById('mode-select');

function initBoard() {
    boardEl.innerHTML = '';
    for (let r = 0; r < 4; r++) {
        for (let c = 0; c < 4; c++) {
            const cell = document.createElement('div');
            cell.classList.add('cell');
            cell.dataset.col = c;
            cell.addEventListener('click', () => handleCellClick(c));
            boardEl.appendChild(cell);
        }
    }
    updateBoardUI();
}

function updateBoardUI() {
    const cells = boardEl.children;
    for (let i = 0; i < 16; i++) {
        cells[i].className = 'cell';
        if (board[i] === 1) cells[i].classList.add('player1');
        if (board[i] === 2) cells[i].classList.add('player2');
    }
}

async function handleCellClick(col) {
    if (gameOver || currentTurn !== 1) return;

    // Turno Humano
    let response = await fetch('/api/human-move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ board, col, player: 1 })
    });
    let data = await response.json();
    
    if (!data.success) {
        // Columna llena
        return;
    }

    board = data.board;
    updateBoardUI();

    if (data.win) {
        endGame('¡Ganaste! (Humano)');
        return;
    }
    if (data.draw) {
        endGame('Empate');
        return;
    }

    // Turno IA
    currentTurn = 2;
    statusEl.innerText = 'IA pensando...';
    
    const mode = modeSelect.value;
    const endpoint = mode === 'minimax' ? '/api/minimax-move' : '/api/alphabeta-move';
    
    response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ board })
    });
    
    data = await response.json();
    board = data.board;
    updateBoardUI();

    if (data.win) {
        endGame('La IA ha ganado.');
        return;
    }
    if (data.draw) {
        endGame('Empate');
        return;
    }

    currentTurn = 1;
    statusEl.innerText = 'Tu turno (Rojo)';
}

function endGame(msg) {
    gameOver = true;
    statusEl.innerText = msg;
}

if (resetBtn) {
    resetBtn.addEventListener('click', () => {
        board = new Array(16).fill(0);
        currentTurn = 1;
        gameOver = false;
        statusEl.innerText = 'Tu turno (Rojo)';
        initBoard();
    });
}

// Inicialización
initBoard();

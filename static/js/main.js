let board = new Array(16).fill(0);
let currentTurn = 1; // 1 = humano, 2 = IA
let gameOver = false;

const boardEl = document.getElementById('board');
const statusEl = document.getElementById('status-message');
const resetBtn = document.getElementById('reset-btn');
const benchmarkBtn = document.getElementById('benchmark-btn');
const modeSelect = document.getElementById('mode-select');

const timeMetric = document.getElementById('time-metric');
const nodesMetric = document.getElementById('nodes-metric');
const benchmarkResults = document.getElementById('benchmark-results');

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
    statusEl.innerText = 'IA Pensando...';
    
    const mode = modeSelect.value;
    const endpoint = mode === 'minimax' ? '/api/minimax-move' : '/api/ml-move';
    
    response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ board })
    });
    
    data = await response.json();
    board = data.board;
    updateBoardUI();
    
    // Update metrics
    timeMetric.innerText = `${data.time_ms.toFixed(2)} ms`;
    nodesMetric.innerText = data.nodes;

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

resetBtn.addEventListener('click', () => {
    board = new Array(16).fill(0);
    currentTurn = 1;
    gameOver = false;
    statusEl.innerText = 'Tu turno (Rojo)';
    timeMetric.innerText = '- ms';
    nodesMetric.innerText = '-';
    initBoard();
});

benchmarkBtn.addEventListener('click', async () => {
    benchmarkBtn.disabled = true;
    benchmarkBtn.innerText = 'Ejecutando...';
    
    const response = await fetch('/api/benchmark');
    const data = await response.json();
    
    document.getElementById('bm-mm-time').innerText = data.minimax_time_ms;
    document.getElementById('bm-mm-nodes').innerText = data.minimax_avg_nodes;
    document.getElementById('bm-ml-time').innerText = data.ml_time_ms;
    document.getElementById('bm-ml-nodes').innerText = data.ml_avg_nodes;
    
    benchmarkResults.classList.remove('hidden');
    benchmarkBtn.disabled = false;
    benchmarkBtn.innerText = 'Ejecutar Benchmark';
});

// Init
initBoard();

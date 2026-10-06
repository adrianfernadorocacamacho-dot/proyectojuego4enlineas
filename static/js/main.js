let board = new Array(36).fill(0);
let currentTurn = 1; // 1 = humano, 2 = IA
let gameOver = false;

const boardEl = document.getElementById('board');
const statusEl = document.getElementById('status-message');
const resetBtn = document.getElementById('reset-btn');
const modeSelect = document.getElementById('mode-select');

// Métricas en tiempo real
const metricTime = document.getElementById('metric-time');
const metricNodes = document.getElementById('metric-nodes');
const metricMode = document.getElementById('metric-mode');

// Modal de Benchmark
const benchmarkBtn = document.getElementById('benchmark-btn');
const benchmarkModal = document.getElementById('benchmark-modal');
const closeBmBtn = document.getElementById('close-bm');

function initBoard() {
    boardEl.innerHTML = '';
    for (let r = 0; r < 6; r++) {
        for (let c = 0; c < 6; c++) {
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
    for (let i = 0; i < 36; i++) {
        cells[i].className = 'cell';
        if (board[i] === 1) cells[i].classList.add('player1');
        if (board[i] === 2) cells[i].classList.add('player2');
    }
}

async function handleCellClick(col) {
    if (gameOver || currentTurn !== 1) return;

    // 1. Turno Humano
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

    // 2. Turno IA
    currentTurn = 2;
    statusEl.innerText = 'IA pensando...';
    
    const mode = modeSelect ? modeSelect.value : 'minimax';
    let endpoint = '/api/minimax-move';
    let modeLabel = 'Minimax (Fuerza Bruta)';

    if (mode === 'alphabeta') {
        endpoint = '/api/alphabeta-move';
        modeLabel = 'Poda Alfa-Beta';
    } else if (mode === 'ml') {
        endpoint = '/api/ml-move';
        modeLabel = 'DecisionTreeClassifier';
    }
    
    response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ board })
    });
    
    data = await response.json();
    board = data.board;
    updateBoardUI();

    // Actualizar barra de métricas (Criterio 10% UX)
    if (metricTime && data.time_ms !== undefined) metricTime.innerText = `${data.time_ms} ms`;
    if (metricNodes && data.nodes !== undefined) metricNodes.innerText = data.nodes;
    if (metricMode) metricMode.innerText = modeLabel;

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
        board = new Array(36).fill(0);
        currentTurn = 1;
        gameOver = false;
        statusEl.innerText = 'Tu turno (Rojo)';
        if (metricTime) metricTime.innerText = '- ms';
        if (metricNodes) metricNodes.innerText = '-';
        initBoard();
    });
}

// Modal Benchmark (Criterio 10% Reporte)
if (benchmarkBtn) {
    benchmarkBtn.addEventListener('click', async () => {
        benchmarkModal.classList.remove('hidden');
        benchmarkBtn.disabled = true;
        document.getElementById('bm-mm-time').innerText = '...';
        document.getElementById('bm-ab-time').innerText = '...';
        document.getElementById('bm-ml-time').innerText = '...';
        
        try {
            const resp = await fetch('/api/benchmark');
            const data = await resp.json();
            document.getElementById('bm-mm-time').innerText = data.minimax_time_ms;
            document.getElementById('bm-mm-nodes').innerText = data.minimax_avg_nodes;
            document.getElementById('bm-ab-time').innerText = data.alphabeta_time_ms;
            document.getElementById('bm-ab-nodes').innerText = data.alphabeta_avg_nodes;
            document.getElementById('bm-ml-time').innerText = data.ml_time_ms;
        } catch (err) {
            console.error('Error benchmark:', err);
        }
        benchmarkBtn.disabled = false;
    });
}

if (closeBmBtn) {
    closeBmBtn.addEventListener('click', () => {
        benchmarkModal.classList.add('hidden');
    });
}

// Cerrar modales haciendo clic fuera
window.addEventListener('click', (e) => {
    if (e.target === benchmarkModal) benchmarkModal.classList.add('hidden');
});

// Inicialización
initBoard();

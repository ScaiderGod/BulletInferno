import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Bullet Inferno",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        .stApp {
            background: radial-gradient(circle at top, #241126 0%, #080812 45%, #03030a 100%);
        }
        header, footer {visibility: hidden;}
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
            max-width: 980px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

GAME_HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<style>
    html, body {
        margin: 0;
        padding: 0;
        overflow: hidden;
        background: transparent;
        font-family: Arial, Helvetica, sans-serif;
        color: #f7f7fb;
    }

    .wrap {
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    #gameShell {
        position: relative;
        width: 920px;
        max-width: 96vw;
        border-radius: 22px;
        padding: 14px;
        background: linear-gradient(180deg, rgba(255,255,255,0.08), rgba(255,255,255,0.02));
        border: 1px solid rgba(255,255,255,0.12);
        box-shadow: 0 22px 70px rgba(0,0,0,0.42);
        box-sizing: border-box;
    }

    #gameCanvas {
        width: 100%;
        height: auto;
        display: block;
        border-radius: 16px;
        background: #050511;
        cursor: none;
        touch-action: none;
    }

    .hint {
        margin-top: 10px;
        text-align: center;
        font-size: 13px;
        color: rgba(247,247,251,0.72);
    }

    #menuOverlay {
        position: absolute;
        inset: 14px 14px 40px 14px;
        border-radius: 16px;
        background: radial-gradient(circle at 50% 18%, rgba(255, 122, 47, 0.22), rgba(4, 4, 12, 0.90) 45%, rgba(2, 2, 8, 0.96));
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 5;
        box-sizing: border-box;
    }

    .menuCard {
        width: min(680px, 88%);
        padding: 28px;
        border-radius: 24px;
        background: rgba(255,255,255,0.075);
        border: 1px solid rgba(255,255,255,0.16);
        box-shadow: 0 20px 50px rgba(0,0,0,0.35);
        text-align: center;
        backdrop-filter: blur(6px);
    }

    .menuTitle {
        margin: 0;
        font-size: 56px;
        line-height: 1;
        color: #fff8ec;
        letter-spacing: 0.5px;
    }

    .menuSub {
        margin: 12px 0 22px;
        color: rgba(247,247,251,0.78);
        font-size: 17px;
    }

    .nameRow {
        display: grid;
        grid-template-columns: 1fr auto;
        gap: 10px;
        margin: 0 auto 18px;
        max-width: 470px;
    }

    #playerNameInput {
        height: 46px;
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.22);
        background: rgba(0,0,0,0.30);
        color: #f7f7fb;
        padding: 0 14px;
        font-size: 16px;
        outline: none;
        box-sizing: border-box;
    }

    #playerNameInput::placeholder {
        color: rgba(247,247,251,0.45);
    }

    #startButton, #clearBoardButton {
        border: 0;
        border-radius: 14px;
        color: #fff8ec;
        font-weight: 800;
        letter-spacing: 0.4px;
        cursor: pointer;
    }

    #startButton {
        height: 46px;
        padding: 0 26px;
        background: linear-gradient(135deg, #ff7a2f, #d91f45);
        font-size: 16px;
        box-shadow: 0 10px 24px rgba(217,31,69,0.32);
    }

    #startButton:hover {
        filter: brightness(1.08);
    }

    #clearBoardButton {
        margin-top: 8px;
        height: 30px;
        padding: 0 12px;
        background: rgba(255,255,255,0.10);
        color: rgba(247,247,251,0.72);
        font-size: 12px;
    }

    .howTo {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px;
        margin: 16px 0 18px;
    }

    .tip {
        border-radius: 16px;
        padding: 12px 9px;
        background: rgba(0,0,0,0.24);
        border: 1px solid rgba(255,255,255,0.10);
        color: rgba(247,247,251,0.78);
        font-size: 13px;
        min-height: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .leaderboard {
        margin-top: 16px;
        border-radius: 18px;
        overflow: hidden;
        background: rgba(0,0,0,0.26);
        border: 1px solid rgba(255,255,255,0.10);
        text-align: left;
    }

    .leaderTitle {
        padding: 11px 14px;
        font-weight: 800;
        color: #ffd447;
        border-bottom: 1px solid rgba(255,255,255,0.10);
        display: flex;
        justify-content: space-between;
        gap: 12px;
        font-size: 14px;
    }

    .leaderRows {
        max-height: 160px;
        overflow: auto;
    }

    .leaderRow {
        display: grid;
        grid-template-columns: 38px 1fr 84px 68px 74px;
        gap: 8px;
        padding: 8px 14px;
        border-bottom: 1px solid rgba(255,255,255,0.055);
        color: rgba(247,247,251,0.82);
        font-size: 13px;
        align-items: center;
    }

    .leaderRow:last-child {
        border-bottom: 0;
    }

    .muted {
        color: rgba(247,247,251,0.50);
    }

    @media (max-width: 720px) {
        .menuTitle { font-size: 40px; }
        .nameRow { grid-template-columns: 1fr; }
        .howTo { grid-template-columns: 1fr 1fr; }
        .leaderRow { grid-template-columns: 30px 1fr 70px 55px; }
        .leaderRow .hideSmall { display: none; }
    }
</style>
</head>
<body>
<div class="wrap">
    <div id="gameShell">
        <canvas id="gameCanvas" width="900" height="620"></canvas>
        <div id="menuOverlay">
            <div class="menuCard">
                <h1 class="menuTitle">Bullet Inferno</h1>
                <p class="menuSub">Survive the bullet storm. Collect coins. Outlast every boss.</p>
                <div class="nameRow">
                    <input id="playerNameInput" maxlength="18" placeholder="Player name for leaderboard" autocomplete="off" />
                    <button id="startButton">START</button>
                </div>
                <div class="howTo">
                    <div class="tip">Move the ship with your mouse.</div>
                    <div class="tip">Dodge red bullets.</div>
                    <div class="tip">Collect yellow coins.</div>
                    <div class="tip">Press P to pause.</div>
                </div>
                <div class="leaderboard">
                    <div class="leaderTitle"><span>Local Leaderboard</span><span class="muted">Top 10</span></div>
                    <div id="leaderboardRows" class="leaderRows"></div>
                </div>
                <button id="clearBoardButton">Clear leaderboard</button>
            </div>
        </div>
        <div class="hint">Move your mouse to control the ship. Dodge red bullets. Collect coins. Boss HP goes down while you survive.</div>
    </div>
</div>

<script>
(() => {
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");
    const menuOverlay = document.getElementById("menuOverlay");
    const playerNameInput = document.getElementById("playerNameInput");
    const startButton = document.getElementById("startButton");
    const clearBoardButton = document.getElementById("clearBoardButton");
    const leaderboardRows = document.getElementById("leaderboardRows");

    const W = canvas.width;
    const H = canvas.height;
    const LEADERBOARD_KEY = "bulletInfernoLeaderboardV2";
    const NAME_KEY = "bulletInfernoPlayerName";

    const levels = [
        { n: 1, name: "Drone Core", duration: 60, bulletEvery: 720, coinChance: 0.14, speed: 2.1, pattern: "simple", bg: [33, 16, 45] },
        { n: 2, name: "Twin Blaster", duration: 120, bulletEvery: 560, coinChance: 0.12, speed: 2.45, pattern: "twin", bg: [40, 14, 46] },
        { n: 3, name: "Void Serpent", duration: 180, bulletEvery: 430, coinChance: 0.10, speed: 2.85, pattern: "spiral", bg: [32, 10, 56] },
        { n: 4, name: "Inferno Engine", duration: 240, bulletEvery: 330, coinChance: 0.08, speed: 3.25, pattern: "rain", bg: [58, 12, 35] },
        { n: 5, name: "The Bullet Sun", duration: 300, bulletEvery: 260, coinChance: 0.06, speed: 3.65, pattern: "final", bg: [72, 10, 24] },
    ];

    let state = "menu";
    let currentLevelIndex = 0;
    let levelStartedAt = 0;
    let lastFrame = performance.now();
    let lastSpawn = 0;
    let transitionUntil = 0;
    let coins = 0;
    let totalSurvival = 0;
    let stars = [];
    let bullets = [];
    let particles = [];
    let mouseInside = false;
    let spiralAngle = 0;
    let flash = 0;
    let lives = 3;
    let invulnUntil = 0;
    let pausedAt = 0;
    let scoreSaved = false;
    let finalScore = 0;
    let finalResult = "";
    let audioCtx = null;

    const ship = {
        x: W / 2,
        y: H - 90,
        targetX: W / 2,
        targetY: H - 90,
        radius: 8,
        visualRadius: 15,
    };

    const boss = {
        x: W / 2,
        y: 105,
        r: 50,
        pulse: 0,
    };

    function buildStars() {
        stars = [];
        for (let i = 0; i < 150; i++) {
            stars.push({
                x: Math.random() * W,
                y: Math.random() * H,
                r: Math.random() * 1.8 + 0.3,
                speed: Math.random() * 0.45 + 0.12,
                a: Math.random() * 0.65 + 0.25,
            });
        }
    }

    buildStars();

    function sanitizeName(raw) {
        const clean = String(raw || "").trim().replace(/[^a-zA-Z0-9 _.-]/g, "").slice(0, 18);
        return clean || "Pilot";
    }

    function loadSavedName() {
        const saved = localStorage.getItem(NAME_KEY);
        if (saved) playerNameInput.value = saved;
    }

    function getPlayerName() {
        const name = sanitizeName(playerNameInput.value);
        playerNameInput.value = name;
        localStorage.setItem(NAME_KEY, name);
        return name;
    }

    function readLeaderboard() {
        try {
            return JSON.parse(localStorage.getItem(LEADERBOARD_KEY) || "[]");
        } catch (e) {
            return [];
        }
    }

    function writeLeaderboard(rows) {
        localStorage.setItem(LEADERBOARD_KEY, JSON.stringify(rows.slice(0, 10)));
    }

    function renderLeaderboard() {
        const rows = readLeaderboard();
        if (!rows.length) {
            leaderboardRows.innerHTML = `<div class="leaderRow"><span class="muted">--</span><span class="muted">No scores yet</span><span></span><span></span><span class="hideSmall"></span></div>`;
            return;
        }

        leaderboardRows.innerHTML = rows.map((row, index) => {
            const result = row.result === "Victory" ? "Win" : "Lost";
            return `
                <div class="leaderRow">
                    <span>${index + 1}</span>
                    <span>${escapeHtml(row.name)}</span>
                    <span>${row.score}</span>
                    <span>L${row.level}</span>
                    <span class="hideSmall">${result}</span>
                </div>
            `;
        }).join("");
    }

    function escapeHtml(value) {
        return String(value)
            .replaceAll("&", "&amp;")
            .replaceAll("<", "&lt;")
            .replaceAll(">", "&gt;")
            .replaceAll('"', "&quot;")
            .replaceAll("'", "&#039;");
    }

    function saveFinalScore(result) {
        if (scoreSaved) return;
        scoreSaved = true;
        finalResult = result;
        const levelReached = Math.min(currentLevelIndex + 1, levels.length);
        finalScore = Math.round(coins * 100 + totalSurvival * 20 + levelReached * 500 + (result === "Victory" ? 5000 : 0));
        const rows = readLeaderboard();
        rows.push({
            name: getPlayerName(),
            score: finalScore,
            coins,
            level: levelReached,
            time: Math.round(totalSurvival),
            result,
            date: new Date().toISOString(),
        });
        rows.sort((a, b) => b.score - a.score);
        writeLeaderboard(rows);
        renderLeaderboard();
    }

    function showMenu() {
        state = "menu";
        menuOverlay.style.display = "flex";
        renderLeaderboard();
        setTimeout(() => playerNameInput.focus(), 50);
    }

    function hideMenu() {
        menuOverlay.style.display = "none";
    }

    function getMousePos(evt) {
        const rect = canvas.getBoundingClientRect();
        const scaleX = canvas.width / rect.width;
        const scaleY = canvas.height / rect.height;
        return {
            x: (evt.clientX - rect.left) * scaleX,
            y: (evt.clientY - rect.top) * scaleY,
        };
    }

    canvas.addEventListener("mousemove", (evt) => {
        const pos = getMousePos(evt);
        ship.targetX = clamp(pos.x, 18, W - 18);
        ship.targetY = clamp(pos.y, 170, H - 24);
        mouseInside = true;
    });

    canvas.addEventListener("mouseenter", () => { mouseInside = true; });
    canvas.addEventListener("mouseleave", () => { mouseInside = false; });

    canvas.addEventListener("click", (evt) => {
        const pos = getMousePos(evt);
        if (state === "gameover" || state === "victory") {
            if (isInside(pos, W / 2 - 250, 360, 220, 58)) {
                startNewGame();
            } else if (isInside(pos, W / 2 + 30, 360, 220, 58)) {
                showMenu();
            } else {
                startNewGame();
            }
        }
    });

    startButton.addEventListener("click", () => startNewGame());
    playerNameInput.addEventListener("keydown", (evt) => {
        if (evt.key === "Enter") startNewGame();
    });
    clearBoardButton.addEventListener("click", () => {
        localStorage.removeItem(LEADERBOARD_KEY);
        renderLeaderboard();
    });

    window.addEventListener("keydown", (evt) => {
        if (evt.key.toLowerCase() === "p") {
            if (state === "playing") pauseGame();
            else if (state === "paused") resumeGame();
        }
        if (evt.key === "Escape" && (state === "gameover" || state === "victory")) {
            showMenu();
        }
    });

    function initAudio() {
        if (!audioCtx) {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            if (AudioContext) audioCtx = new AudioContext();
        }
        if (audioCtx && audioCtx.state === "suspended") audioCtx.resume();
    }

    function playTone(freq, duration = 0.08, type = "sine", volume = 0.045) {
        if (!audioCtx) return;
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = type;
        osc.frequency.value = freq;
        gain.gain.setValueAtTime(volume, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + duration);
    }

    function startNewGame() {
        initAudio();
        getPlayerName();
        hideMenu();
        currentLevelIndex = 0;
        coins = 0;
        totalSurvival = 0;
        lives = 3;
        scoreSaved = false;
        finalScore = 0;
        finalResult = "";
        ship.x = W / 2;
        ship.y = H - 90;
        ship.targetX = W / 2;
        ship.targetY = H - 90;
        startLevel(0);
        playTone(440, 0.09, "triangle", 0.05);
        setTimeout(() => playTone(660, 0.09, "triangle", 0.045), 95);
    }

    function startLevel(index) {
        currentLevelIndex = index;
        bullets = [];
        particles = [];
        spiralAngle = 0;
        flash = 0;
        lastSpawn = performance.now();
        levelStartedAt = performance.now();
        transitionUntil = performance.now() + 1700;
        invulnUntil = performance.now() + 1300;
        state = "playing";
    }

    function pauseGame() {
        pausedAt = performance.now();
        state = "paused";
    }

    function resumeGame() {
        const now = performance.now();
        const pauseDuration = now - pausedAt;
        levelStartedAt += pauseDuration;
        lastSpawn += pauseDuration;
        transitionUntil += pauseDuration;
        invulnUntil += pauseDuration;
        state = "playing";
    }

    function clamp(v, min, max) {
        return Math.max(min, Math.min(max, v));
    }

    function rand(min, max) {
        return Math.random() * (max - min) + min;
    }

    function distance(a, b) {
        const dx = a.x - b.x;
        const dy = a.y - b.y;
        return Math.sqrt(dx * dx + dy * dy);
    }

    function isInside(p, x, y, w, h) {
        return p.x >= x && p.x <= x + w && p.y >= y && p.y <= y + h;
    }

    function makeProjectile(x, y, vx, vy, level, forceCoin = false) {
        const isCoin = forceCoin || Math.random() < level.coinChance;
        bullets.push({
            x, y, vx, vy,
            r: isCoin ? 8 : 7,
            type: isCoin ? "coin" : "bullet",
            spin: Math.random() * Math.PI * 2,
        });
    }

    function spawnRadial(count, speed, angleOffset, level, cx = boss.x, cy = boss.y + 20) {
        for (let i = 0; i < count; i++) {
            const a = angleOffset + (Math.PI * 2 * i / count);
            makeProjectile(cx, cy, Math.cos(a) * speed, Math.sin(a) * speed, level);
        }
    }

    function spawnAimed(count, spread, speed, level, originX = boss.x, originY = boss.y + 25) {
        const base = Math.atan2(ship.y - originY, ship.x - originX);
        for (let i = 0; i < count; i++) {
            const t = count === 1 ? 0 : (i / (count - 1)) - 0.5;
            const a = base + t * spread;
            makeProjectile(originX, originY, Math.cos(a) * speed, Math.sin(a) * speed, level);
        }
    }

    function spawnRain(columns, speed, level) {
        for (let i = 0; i < columns; i++) {
            const x = rand(30, W - 30);
            const drift = rand(-0.65, 0.65);
            makeProjectile(x, -20, drift, speed + rand(-0.25, 0.45), level);
        }
    }

    function spawnCoinsLine(level) {
        const startX = rand(100, W - 100);
        const dir = Math.random() < 0.5 ? -1 : 1;
        for (let i = 0; i < 5; i++) {
            makeProjectile(startX + i * 34 * dir, -16 - i * 12, rand(-0.15, 0.15), level.speed * 0.72, level, true);
        }
    }

    function spawnPattern(level, now) {
        const wobble = Math.sin(now / 650) * 120;
        boss.x = W / 2 + wobble;

        if (level.pattern === "simple") {
            spawnAimed(3, 0.42, level.speed, level);
            if (Math.random() < 0.28) spawnCoinsLine(level);
        }

        if (level.pattern === "twin") {
            const left = boss.x - 62;
            const right = boss.x + 62;
            spawnAimed(3, 0.36, level.speed, level, left, boss.y + 25);
            spawnAimed(3, 0.36, level.speed, level, right, boss.y + 25);
            if (Math.random() < 0.35) spawnRadial(10, level.speed * 0.78, now / 800, level);
            if (Math.random() < 0.22) spawnCoinsLine(level);
        }

        if (level.pattern === "spiral") {
            spiralAngle += 0.34;
            spawnRadial(12, level.speed, spiralAngle, level);
            if (Math.random() < 0.42) spawnAimed(5, 0.72, level.speed * 1.08, level);
            if (Math.random() < 0.18) spawnCoinsLine(level);
        }

        if (level.pattern === "rain") {
            spawnRain(11, level.speed, level);
            spawnRadial(16, level.speed * 0.86, now / 700, level);
            if (Math.random() < 0.52) spawnAimed(7, 1.05, level.speed * 1.02, level);
            if (Math.random() < 0.16) spawnCoinsLine(level);
        }

        if (level.pattern === "final") {
            spiralAngle += 0.47;
            spawnRadial(20, level.speed * 0.92, spiralAngle, level);
            spawnRadial(14, level.speed * 0.72, -spiralAngle * 0.75, level, W / 2, boss.y + 30);
            spawnAimed(9, 1.18, level.speed * 1.08, level);
            if (Math.random() < 0.62) spawnRain(9, level.speed * 0.9, level);
            if (Math.random() < 0.14) spawnCoinsLine(level);
        }
    }

    function update(dt, now) {
        if (state !== "playing") return;

        const level = levels[currentLevelIndex];
        const elapsed = (now - levelStartedAt) / 1000;
        const remaining = Math.max(0, level.duration - elapsed);

        ship.x += (ship.targetX - ship.x) * 0.34;
        ship.y += (ship.targetY - ship.y) * 0.34;

        boss.pulse += dt * 0.006;
        boss.x = W / 2 + Math.sin(now / 700) * (currentLevelIndex * 14 + 20);

        const spawnDelay = Math.max(120, level.bulletEvery - elapsed * 1.15);
        if (now - lastSpawn > spawnDelay) {
            spawnPattern(level, now);
            lastSpawn = now;
        }

        if (Math.random() < 0.006 + currentLevelIndex * 0.002) {
            spawnCoinsLine(level);
        }

        for (const b of bullets) {
            b.x += b.vx * dt * 0.06;
            b.y += b.vy * dt * 0.06;
            b.spin += dt * 0.008;
        }

        bullets = bullets.filter(b => b.x > -60 && b.x < W + 60 && b.y > -70 && b.y < H + 70);

        for (let i = bullets.length - 1; i >= 0; i--) {
            const b = bullets[i];
            const hitDistance = b.type === "coin" ? ship.visualRadius + b.r : ship.radius + b.r;
            if (distance(ship, b) < hitDistance) {
                if (b.type === "coin") {
                    coins += 1;
                    makeCoinParticles(b.x, b.y);
                    bullets.splice(i, 1);
                    playTone(880, 0.045, "triangle", 0.035);
                } else if (now >= invulnUntil) {
                    lives -= 1;
                    makeExplosion(ship.x, ship.y);
                    flash = 0.58;
                    bullets.splice(i, 1);
                    bullets = bullets.filter(item => distance(ship, item) > 90 || item.type === "coin");
                    playTone(130, 0.13, "sawtooth", 0.035);
                    if (lives <= 0) {
                        state = "gameover";
                        totalSurvival += Math.max(0, elapsed);
                        saveFinalScore("Game Over");
                    } else {
                        invulnUntil = now + 1600;
                    }
                }
            }
        }

        for (const p of particles) {
            p.x += p.vx * dt * 0.06;
            p.y += p.vy * dt * 0.06;
            p.life -= dt;
            p.r *= 0.985;
        }
        particles = particles.filter(p => p.life > 0 && p.r > 0.2);

        if (remaining <= 0) {
            totalSurvival += level.duration;
            playTone(523, 0.10, "triangle", 0.045);
            setTimeout(() => playTone(784, 0.12, "triangle", 0.040), 120);
            if (currentLevelIndex >= levels.length - 1) {
                state = "victory";
                saveFinalScore("Victory");
            } else {
                state = "levelclear";
                transitionUntil = now + 1700;
                setTimeout(() => startLevel(currentLevelIndex + 1), 1700);
            }
        }
    }

    function makeCoinParticles(x, y) {
        for (let i = 0; i < 8; i++) {
            const a = Math.random() * Math.PI * 2;
            const s = rand(1.5, 3.4);
            particles.push({ x, y, vx: Math.cos(a) * s, vy: Math.sin(a) * s, r: rand(2, 4), life: rand(260, 440), color: "coin" });
        }
    }

    function makeExplosion(x, y) {
        for (let i = 0; i < 36; i++) {
            const a = Math.random() * Math.PI * 2;
            const s = rand(2.8, 7.4);
            particles.push({ x, y, vx: Math.cos(a) * s, vy: Math.sin(a) * s, r: rand(3, 7), life: rand(450, 850), color: "fire" });
        }
    }

    function drawBackground(dt) {
        const level = levels[currentLevelIndex] || levels[0];
        const [r, g, b] = level.bg;
        const bg = ctx.createRadialGradient(W / 2, 60, 40, W / 2, H / 2, H);
        bg.addColorStop(0, `rgb(${r}, ${g}, ${b})`);
        bg.addColorStop(0.45, "#070817");
        bg.addColorStop(1, "#02030a");
        ctx.fillStyle = bg;
        ctx.fillRect(0, 0, W, H);

        for (const s of stars) {
            s.y += s.speed * dt * 0.04;
            if (s.y > H) {
                s.y = 0;
                s.x = Math.random() * W;
            }
            ctx.globalAlpha = s.a;
            ctx.fillStyle = "#ffffff";
            ctx.beginPath();
            ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
            ctx.fill();
        }
        ctx.globalAlpha = 1;
    }

    function drawBoss(level, elapsed) {
        const hpRatio = Math.max(0, 1 - elapsed / level.duration);
        const pulse = Math.sin(boss.pulse) * 4;
        const r = boss.r + currentLevelIndex * 5 + pulse;

        ctx.save();
        ctx.translate(boss.x, boss.y);

        const gradient = ctx.createRadialGradient(0, 0, 8, 0, 0, r + 28);
        gradient.addColorStop(0, "#fff2c0");
        gradient.addColorStop(0.32, "#ff7a2f");
        gradient.addColorStop(0.78, "#801b34");
        gradient.addColorStop(1, "rgba(255, 60, 40, 0)");
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(0, 0, r + 24, 0, Math.PI * 2);
        ctx.fill();

        ctx.strokeStyle = "rgba(255,255,255,0.52)";
        ctx.lineWidth = 3;
        ctx.beginPath();
        const points = currentLevelIndex === 4 ? 14 : 10;
        for (let i = 0; i < points; i++) {
            const a = (Math.PI * 2 * i / points) + boss.pulse * (0.20 + currentLevelIndex * 0.02);
            const rr = i % 2 === 0 ? r : r * (0.64 + currentLevelIndex * 0.01);
            const x = Math.cos(a) * rr;
            const y = Math.sin(a) * rr;
            if (i === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        }
        ctx.closePath();
        ctx.fillStyle = "rgba(30, 8, 30, 0.9)";
        ctx.fill();
        ctx.stroke();

        ctx.fillStyle = "#ffcc66";
        ctx.beginPath();
        ctx.arc(0, 0, r * 0.28, 0, Math.PI * 2);
        ctx.fill();

        ctx.restore();

        drawBossHp(level.name, hpRatio);
    }

    function drawBossHp(name, hpRatio) {
        const x = 150;
        const y = 24;
        const w = W - 300;
        const h = 18;

        ctx.fillStyle = "rgba(255,255,255,0.10)";
        roundRect(x, y, w, h, 9, true, false);
        ctx.fillStyle = "rgba(255,85,68,0.95)";
        roundRect(x, y, w * hpRatio, h, 9, true, false);
        ctx.strokeStyle = "rgba(255,255,255,0.35)";
        ctx.lineWidth = 1;
        roundRect(x, y, w, h, 9, false, true);

        ctx.font = "bold 16px Arial";
        ctx.textAlign = "center";
        ctx.fillStyle = "#f7f7fb";
        ctx.fillText(name, W / 2, y + 42);
    }

    function drawShip(now) {
        const isInvuln = now < invulnUntil;
        if (isInvuln && Math.floor(now / 110) % 2 === 0) return;

        ctx.save();
        ctx.translate(ship.x, ship.y);

        ctx.shadowColor = "rgba(100,190,255,0.9)";
        ctx.shadowBlur = 18;

        ctx.fillStyle = "#eaf7ff";
        ctx.beginPath();
        ctx.moveTo(0, -18);
        ctx.lineTo(14, 15);
        ctx.lineTo(0, 8);
        ctx.lineTo(-14, 15);
        ctx.closePath();
        ctx.fill();

        ctx.fillStyle = isInvuln ? "#ffe28a" : "#4ecbff";
        ctx.beginPath();
        ctx.moveTo(0, -8);
        ctx.lineTo(6, 9);
        ctx.lineTo(0, 5);
        ctx.lineTo(-6, 9);
        ctx.closePath();
        ctx.fill();

        ctx.shadowBlur = 0;
        ctx.strokeStyle = isInvuln ? "rgba(255,226,138,0.90)" : "rgba(255,255,255,0.78)";
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.arc(0, 0, ship.radius, 0, Math.PI * 2);
        ctx.stroke();

        ctx.restore();
    }

    function drawProjectiles() {
        for (const b of bullets) {
            if (b.type === "coin") {
                ctx.save();
                ctx.translate(b.x, b.y);
                ctx.rotate(b.spin);
                ctx.shadowColor = "rgba(255,210,65,0.85)";
                ctx.shadowBlur = 14;
                ctx.fillStyle = "#ffd447";
                ctx.beginPath();
                ctx.arc(0, 0, b.r, 0, Math.PI * 2);
                ctx.fill();
                ctx.strokeStyle = "#fff3a3";
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.moveTo(-4, 0);
                ctx.lineTo(4, 0);
                ctx.stroke();
                ctx.restore();
            } else {
                ctx.save();
                ctx.shadowColor = "rgba(255,72,50,0.9)";
                ctx.shadowBlur = 11;
                const g = ctx.createRadialGradient(b.x - 2, b.y - 2, 1, b.x, b.y, b.r + 5);
                g.addColorStop(0, "#fff1c7");
                g.addColorStop(0.35, "#ff7942");
                g.addColorStop(1, "#b80d27");
                ctx.fillStyle = g;
                ctx.beginPath();
                ctx.arc(b.x, b.y, b.r, 0, Math.PI * 2);
                ctx.fill();
                ctx.restore();
            }
        }
    }

    function drawParticles() {
        for (const p of particles) {
            const alpha = clamp(p.life / 700, 0, 1);
            ctx.globalAlpha = alpha;
            if (p.color === "coin") ctx.fillStyle = "#ffd447";
            else ctx.fillStyle = Math.random() < 0.5 ? "#ff6b3c" : "#ffca62";
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
            ctx.fill();
        }
        ctx.globalAlpha = 1;
    }

    function drawHud(level, elapsed) {
        const remaining = Math.max(0, level.duration - elapsed);
        const mins = Math.floor(remaining / 60);
        const secs = Math.floor(remaining % 60).toString().padStart(2, "0");

        ctx.fillStyle = "rgba(255,255,255,0.08)";
        roundRect(18, 18, 112, 70, 14, true, false);
        roundRect(W - 150, 18, 132, 70, 14, true, false);

        ctx.fillStyle = "#f7f7fb";
        ctx.font = "bold 16px Arial";
        ctx.textAlign = "left";
        ctx.fillText(`Level ${level.n}`, 34, 40);
        ctx.font = "13px Arial";
        ctx.fillStyle = "rgba(247,247,251,0.75)";
        ctx.fillText(`${mins}:${secs}`, 34, 60);
        ctx.fillStyle = "#ffb2a1";
        ctx.fillText(`Lives ${lives}`, 34, 78);

        ctx.textAlign = "right";
        ctx.font = "bold 16px Arial";
        ctx.fillStyle = "#ffd447";
        ctx.fillText(`Coins ${coins}`, W - 34, 42);
        ctx.font = "13px Arial";
        ctx.fillStyle = "rgba(247,247,251,0.68)";
        ctx.fillText(`Score ${Math.round(coins * 100 + totalSurvival * 20)}`, W - 34, 64);
    }

    function drawMenuCanvas() {
        ctx.fillStyle = "rgba(0,0,0,0.18)";
        ctx.fillRect(0, 0, W, H);
    }

    function drawGameOver() {
        ctx.fillStyle = "rgba(0,0,0,0.60)";
        ctx.fillRect(0, 0, W, H);

        ctx.textAlign = "center";
        ctx.fillStyle = "#ff765f";
        ctx.font = "bold 58px Arial";
        ctx.fillText("GAME OVER", W / 2, 185);

        const lvl = levels[currentLevelIndex];
        ctx.font = "20px Arial";
        ctx.fillStyle = "#f7f7fb";
        ctx.fillText(`You reached Level ${lvl.n}: ${lvl.name}`, W / 2, 232);
        ctx.fillStyle = "#ffd447";
        ctx.fillText(`Score: ${finalScore}   Coins: ${coins}   Time: ${formatTime(totalSurvival)}`, W / 2, 270);

        drawButton(W / 2 - 250, 360, 220, 58, "TRY AGAIN");
        drawButton(W / 2 + 30, 360, 220, 58, "MENU");
        ctx.font = "14px Arial";
        ctx.fillStyle = "rgba(247,247,251,0.60)";
        ctx.fillText("Your score was saved locally in this browser.", W / 2, 450);
    }

    function drawVictory() {
        ctx.fillStyle = "rgba(0,0,0,0.52)";
        ctx.fillRect(0, 0, W, H);

        ctx.textAlign = "center";
        ctx.fillStyle = "#fff2c0";
        ctx.font = "bold 58px Arial";
        ctx.fillText("VICTORY", W / 2, 178);

        ctx.font = "22px Arial";
        ctx.fillStyle = "#f7f7fb";
        ctx.fillText("You survived Bullet Inferno.", W / 2, 226);
        ctx.fillStyle = "#ffd447";
        ctx.fillText(`Score: ${finalScore}   Coins: ${coins}   Time: ${formatTime(totalSurvival)}`, W / 2, 264);

        drawButton(W / 2 - 250, 360, 220, 58, "PLAY AGAIN");
        drawButton(W / 2 + 30, 360, 220, 58, "MENU");
        ctx.font = "14px Arial";
        ctx.fillStyle = "rgba(247,247,251,0.60)";
        ctx.fillText("Your score was saved locally in this browser.", W / 2, 450);
    }

    function drawLevelClear() {
        const level = levels[currentLevelIndex];
        ctx.fillStyle = "rgba(0,0,0,0.42)";
        ctx.fillRect(0, 0, W, H);
        ctx.textAlign = "center";
        ctx.fillStyle = "#fff2c0";
        ctx.font = "bold 44px Arial";
        ctx.fillText(`Level ${level.n} Clear`, W / 2, 260);
        ctx.font = "20px Arial";
        ctx.fillStyle = "rgba(247,247,251,0.86)";
        ctx.fillText(`Coins: ${coins}   Lives: ${lives}`, W / 2, 302);
        ctx.fillText("Next boss incoming...", W / 2, 334);
    }

    function drawPaused() {
        ctx.fillStyle = "rgba(0,0,0,0.55)";
        ctx.fillRect(0, 0, W, H);
        ctx.textAlign = "center";
        ctx.fillStyle = "#fff2c0";
        ctx.font = "bold 54px Arial";
        ctx.fillText("PAUSED", W / 2, 285);
        ctx.font = "19px Arial";
        ctx.fillStyle = "rgba(247,247,251,0.78)";
        ctx.fillText("Press P to continue", W / 2, 325);
    }

    function drawButton(x, y, w, h, label) {
        const grad = ctx.createLinearGradient(x, y, x + w, y + h);
        grad.addColorStop(0, "#ff7a2f");
        grad.addColorStop(1, "#d91f45");
        ctx.fillStyle = grad;
        roundRect(x, y, w, h, 18, true, false);
        ctx.strokeStyle = "rgba(255,255,255,0.45)";
        ctx.lineWidth = 1.5;
        roundRect(x, y, w, h, 18, false, true);
        ctx.fillStyle = "#fff8ec";
        ctx.font = "bold 22px Arial";
        ctx.textAlign = "center";
        ctx.fillText(label, x + w / 2, y + 37);
    }

    function roundRect(x, y, w, h, r, fill, stroke) {
        if (w < 2 * r) r = w / 2;
        if (h < 2 * r) r = h / 2;
        ctx.beginPath();
        ctx.moveTo(x + r, y);
        ctx.arcTo(x + w, y, x + w, y + h, r);
        ctx.arcTo(x + w, y + h, x, y + h, r);
        ctx.arcTo(x, y + h, x, y, r);
        ctx.arcTo(x, y, x + r, y, r);
        ctx.closePath();
        if (fill) ctx.fill();
        if (stroke) ctx.stroke();
    }

    function formatTime(seconds) {
        const s = Math.max(0, Math.round(seconds));
        const m = Math.floor(s / 60);
        const r = String(s % 60).padStart(2, "0");
        return `${m}:${r}`;
    }

    function render(now) {
        const dt = Math.min(32, now - lastFrame);
        lastFrame = now;

        drawBackground(dt);

        if (state === "menu") {
            drawMenuCanvas();
        } else {
            const level = levels[currentLevelIndex];
            const clockNow = state === "paused" ? pausedAt : now;
            const elapsed = Math.max(0, (clockNow - levelStartedAt) / 1000);

            update(dt, now);

            drawBoss(level, elapsed);
            drawProjectiles();
            drawParticles();
            if (state === "playing" || state === "levelclear" || state === "paused") drawShip(clockNow);
            drawHud(level, elapsed);

            if (!mouseInside && state === "playing") {
                ctx.textAlign = "center";
                ctx.fillStyle = "rgba(247,247,251,0.70)";
                ctx.font = "16px Arial";
                ctx.fillText("Move your mouse over the game area", W / 2, H - 22);
            }

            if (state === "levelclear") drawLevelClear();
            if (state === "paused") drawPaused();
            if (state === "gameover") drawGameOver();
            if (state === "victory") drawVictory();

            const introLeft = transitionUntil - now;
            if (state === "playing" && introLeft > 0) {
                ctx.fillStyle = `rgba(0,0,0,${Math.min(0.42, introLeft / 4000)})`;
                ctx.fillRect(0, 0, W, H);
                ctx.textAlign = "center";
                ctx.fillStyle = "#fff2c0";
                ctx.font = "bold 42px Arial";
                ctx.fillText(`Level ${level.n}`, W / 2, 282);
                ctx.font = "21px Arial";
                ctx.fillStyle = "rgba(247,247,251,0.88)";
                ctx.fillText(level.name, W / 2, 318);
            }
        }

        if (flash > 0) {
            ctx.globalAlpha = flash;
            ctx.fillStyle = "#ff6447";
            ctx.fillRect(0, 0, W, H);
            ctx.globalAlpha = 1;
            flash *= 0.88;
        }

        requestAnimationFrame(render);
    }

    loadSavedName();
    renderLeaderboard();
    requestAnimationFrame(render);
})();
</script>
</body>
</html>
"""

components.html(GAME_HTML, height=720, scrolling=False)

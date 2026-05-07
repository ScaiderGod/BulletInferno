import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Bullet Inferno",
    page_icon="🚀",
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
</style>
</head>
<body>
<div class="wrap">
    <div id="gameShell">
        <canvas id="gameCanvas" width="900" height="620"></canvas>
        <div class="hint">Move your mouse to control the ship. Dodge red bullets. Collect coins. The boss loses HP while you survive.</div>
    </div>
</div>

<script>
(() => {
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");

    const W = canvas.width;
    const H = canvas.height;

    const levels = [
        { n: 1, name: "Drone Core", duration: 60, bulletEvery: 720, coinChance: 0.14, speed: 2.1, pattern: "simple" },
        { n: 2, name: "Twin Blaster", duration: 120, bulletEvery: 560, coinChance: 0.12, speed: 2.45, pattern: "twin" },
        { n: 3, name: "Void Serpent", duration: 180, bulletEvery: 430, coinChance: 0.10, speed: 2.85, pattern: "spiral" },
        { n: 4, name: "Inferno Engine", duration: 240, bulletEvery: 330, coinChance: 0.08, speed: 3.25, pattern: "rain" },
        { n: 5, name: "The Bullet Sun", duration: 300, bulletEvery: 260, coinChance: 0.06, speed: 3.65, pattern: "final" },
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
        for (let i = 0; i < 140; i++) {
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

    canvas.addEventListener("click", () => {
        if (state === "menu") startNewGame();
        else if (state === "gameover") startNewGame();
        else if (state === "victory") startNewGame();
    });

    function startNewGame() {
        currentLevelIndex = 0;
        coins = 0;
        totalSurvival = 0;
        ship.x = W / 2;
        ship.y = H - 90;
        ship.targetX = W / 2;
        ship.targetY = H - 90;
        startLevel(0);
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
                } else {
                    makeExplosion(ship.x, ship.y);
                    flash = 1;
                    state = "gameover";
                    totalSurvival += Math.max(0, elapsed);
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
            if (currentLevelIndex >= levels.length - 1) {
                state = "victory";
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
        const bg = ctx.createRadialGradient(W / 2, 60, 40, W / 2, H / 2, H);
        bg.addColorStop(0, "#21102d");
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
        for (let i = 0; i < 10; i++) {
            const a = (Math.PI * 2 * i / 10) + boss.pulse * 0.22;
            const rr = i % 2 === 0 ? r : r * 0.68;
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

    function drawShip() {
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

        ctx.fillStyle = "#4ecbff";
        ctx.beginPath();
        ctx.moveTo(0, -8);
        ctx.lineTo(6, 9);
        ctx.lineTo(0, 5);
        ctx.lineTo(-6, 9);
        ctx.closePath();
        ctx.fill();

        ctx.shadowBlur = 0;
        ctx.strokeStyle = "rgba(255,255,255,0.78)";
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
        roundRect(18, 18, 112, 54, 14, true, false);
        roundRect(W - 136, 18, 118, 54, 14, true, false);

        ctx.fillStyle = "#f7f7fb";
        ctx.font = "bold 16px Arial";
        ctx.textAlign = "left";
        ctx.fillText(`Level ${level.n}`, 34, 40);
        ctx.font = "13px Arial";
        ctx.fillStyle = "rgba(247,247,251,0.75)";
        ctx.fillText(`${mins}:${secs}`, 34, 60);

        ctx.textAlign = "right";
        ctx.font = "bold 16px Arial";
        ctx.fillStyle = "#ffd447";
        ctx.fillText(`Coins ${coins}`, W - 34, 48);
    }

    function drawMenu() {
        ctx.fillStyle = "rgba(0,0,0,0.38)";
        ctx.fillRect(0, 0, W, H);

        ctx.textAlign = "center";
        ctx.fillStyle = "#fff8ec";
        ctx.font = "bold 64px Arial";
        ctx.fillText("Bullet Inferno", W / 2, 170);

        ctx.fillStyle = "rgba(247,247,251,0.82)";
        ctx.font = "19px Arial";
        ctx.fillText("Survive the bullet storm. Collect coins. Outlast every boss.", W / 2, 213);

        drawButton(W / 2 - 115, 270, 230, 62, "JUGAR");

        ctx.font = "15px Arial";
        ctx.fillStyle = "rgba(247,247,251,0.68)";
        ctx.fillText("5 levels · 1 to 5 minutes · mouse control", W / 2, 375);
    }

    function drawGameOver() {
        ctx.fillStyle = "rgba(0,0,0,0.56)";
        ctx.fillRect(0, 0, W, H);

        ctx.textAlign = "center";
        ctx.fillStyle = "#ff765f";
        ctx.font = "bold 58px Arial";
        ctx.fillText("GAME OVER", W / 2, 210);

        const lvl = levels[currentLevelIndex];
        ctx.font = "20px Arial";
        ctx.fillStyle = "#f7f7fb";
        ctx.fillText(`You reached Level ${lvl.n}: ${lvl.name}`, W / 2, 255);
        ctx.fillStyle = "#ffd447";
        ctx.fillText(`Coins collected: ${coins}`, W / 2, 288);

        drawButton(W / 2 - 120, 340, 240, 60, "TRY AGAIN");
    }

    function drawVictory() {
        ctx.fillStyle = "rgba(0,0,0,0.50)";
        ctx.fillRect(0, 0, W, H);

        ctx.textAlign = "center";
        ctx.fillStyle = "#fff2c0";
        ctx.font = "bold 58px Arial";
        ctx.fillText("VICTORY", W / 2, 200);

        ctx.font = "22px Arial";
        ctx.fillStyle = "#f7f7fb";
        ctx.fillText("You survived Bullet Inferno.", W / 2, 246);
        ctx.fillStyle = "#ffd447";
        ctx.fillText(`Final coins: ${coins}`, W / 2, 282);

        drawButton(W / 2 - 120, 340, 240, 60, "PLAY AGAIN");
    }

    function drawLevelClear() {
        const level = levels[currentLevelIndex];
        ctx.fillStyle = "rgba(0,0,0,0.42)";
        ctx.fillRect(0, 0, W, H);
        ctx.textAlign = "center";
        ctx.fillStyle = "#fff2c0";
        ctx.font = "bold 44px Arial";
        ctx.fillText(`Level ${level.n} Clear`, W / 2, 270);
        ctx.font = "20px Arial";
        ctx.fillStyle = "rgba(247,247,251,0.86)";
        ctx.fillText("Next boss incoming...", W / 2, 310);
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
        ctx.font = "bold 24px Arial";
        ctx.textAlign = "center";
        ctx.fillText(label, x + w / 2, y + 39);
    }

    function roundRect(x, y, w, h, r, fill, stroke) {
        if (w < 2 * r) r = w / 2;
        if (h < 2 * r) r = h / 2;
        ctx.beginPath();
        ctx.moveTo(x + r, y);
        ctx.arcTo(x + w, y, x + w, y + h, r);
        ctx.arcTo(x + w, y + h, x, y + h, r);
        ctx.arcTo(x, y + h, x, y, r);
        ctx.arcTo(x, y, x + w, y, r);
        ctx.closePath();
        if (fill) ctx.fill();
        if (stroke) ctx.stroke();
    }

    function render(now) {
        const dt = Math.min(32, now - lastFrame);
        lastFrame = now;

        drawBackground(dt);

        if (state === "menu") {
            drawMenu();
        } else {
            const level = levels[currentLevelIndex];
            const elapsed = Math.max(0, (now - levelStartedAt) / 1000);

            update(dt, now);

            drawBoss(level, elapsed);
            drawProjectiles();
            drawParticles();
            if (state === "playing" || state === "levelclear") drawShip();
            drawHud(level, elapsed);

            if (!mouseInside && state === "playing") {
                ctx.textAlign = "center";
                ctx.fillStyle = "rgba(247,247,251,0.70)";
                ctx.font = "16px Arial";
                ctx.fillText("Move your mouse over the game area", W / 2, H - 22);
            }

            if (state === "levelclear") drawLevelClear();
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

    requestAnimationFrame(render);
})();
</script>
</body>
</html>
"""

components.html(GAME_HTML, height=720, scrolling=False)

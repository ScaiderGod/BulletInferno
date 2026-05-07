import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Bullet Inferno Roguelike v6",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        .stApp {
            background: radial-gradient(circle at top, #251126 0%, #080812 45%, #03030a 100%);
        }
        header, footer {visibility: hidden;}
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
            max-width: 1040px;
        }
        iframe { border-radius: 22px; }
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
        width: 980px;
        max-width: 98vw;
        border-radius: 22px;
        padding: 14px;
        background: linear-gradient(180deg, rgba(255,255,255,0.09), rgba(255,255,255,0.025));
        border: 1px solid rgba(255,255,255,0.13);
        box-shadow: 0 22px 70px rgba(0,0,0,0.45);
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

    #overlay {
        position: absolute;
        inset: 14px 14px 40px 14px;
        border-radius: 16px;
        background: radial-gradient(circle at 50% 18%, rgba(255, 122, 47, 0.20), rgba(4, 4, 12, 0.92) 42%, rgba(2, 2, 8, 0.97));
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 5;
        box-sizing: border-box;
        overflow: hidden;
    }

    #overlay.hidden {
        display: none;
    }

    .card {
        width: min(820px, 92%);
        max-height: 92%;
        overflow: auto;
        padding: 26px;
        border-radius: 24px;
        background: rgba(255,255,255,0.078);
        border: 1px solid rgba(255,255,255,0.16);
        box-shadow: 0 20px 50px rgba(0,0,0,0.35);
        text-align: center;
        backdrop-filter: blur(6px);
        box-sizing: border-box;
    }

    .title {
        margin: 0;
        font-size: 54px;
        line-height: 1;
        color: #fff8ec;
        letter-spacing: 0.5px;
    }

    .subtitle {
        margin: 10px 0 18px;
        color: rgba(247,247,251,0.78);
        font-size: 16px;
    }

    .nameRow {
        display: grid;
        grid-template-columns: 1fr auto;
        gap: 10px;
        margin: 0 auto 16px;
        max-width: 540px;
    }


    .volumeRow {
        display: grid;
        grid-template-columns: auto 1fr auto;
        gap: 10px;
        align-items: center;
        max-width: 540px;
        margin: 0 auto 16px;
        padding: 10px 14px;
        border-radius: 14px;
        background: rgba(0,0,0,0.24);
        border: 1px solid rgba(255,255,255,0.10);
        color: rgba(247,247,251,0.78);
        font-size: 13px;
    }

    input[type="range"] {
        height: auto;
        padding: 0;
        accent-color: #ff7a2f;
        cursor: pointer;
    }

    .godButton {
        height: 46px;
        padding: 0 24px;
        background: linear-gradient(135deg, #facc15, #ef4444, #7c3aed);
        box-shadow: 0 10px 26px rgba(250,204,21,0.22);
        font-size: 15px;
    }

    .lockedButton {
        height: 46px;
        padding: 0 24px;
        background: rgba(255,255,255,0.10);
        color: rgba(247,247,251,0.58);
        font-size: 15px;
    }

    input {
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

    input::placeholder {
        color: rgba(247,247,251,0.45);
    }

    button {
        border: 0;
        border-radius: 14px;
        color: #fff8ec;
        font-weight: 800;
        letter-spacing: 0.3px;
        cursor: pointer;
    }

    .primary {
        height: 46px;
        padding: 0 26px;
        background: linear-gradient(135deg, #ff7a2f, #d91f45);
        font-size: 16px;
        box-shadow: 0 10px 24px rgba(217,31,69,0.32);
    }

    .secondary {
        height: 36px;
        padding: 0 14px;
        background: rgba(255,255,255,0.10);
        color: rgba(247,247,251,0.80);
        font-size: 13px;
    }

    button:hover { filter: brightness(1.08); }
    button:disabled { opacity: 0.45; cursor: not-allowed; filter: none; }

    .shipGrid, .relicGrid, .tipGrid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px;
        margin: 14px 0 16px;
    }

    .shipCard, .relicCard, .tip {
        border-radius: 16px;
        padding: 13px 11px;
        background: rgba(0,0,0,0.27);
        border: 1px solid rgba(255,255,255,0.10);
        color: rgba(247,247,251,0.82);
        min-height: 62px;
        box-sizing: border-box;
    }

    .shipCard {
        cursor: pointer;
        text-align: left;
        transition: transform .12s ease, border-color .12s ease, background .12s ease;
        position: relative;
        overflow: hidden;
    }

    .shipTop {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 6px;
    }

    .shipSwatch {
        width: 26px;
        height: 26px;
        border-radius: 9px;
        border: 1px solid rgba(255,255,255,0.35);
        box-shadow: 0 0 14px rgba(255,255,255,0.15);
        flex: 0 0 auto;
        clip-path: polygon(50% 0%, 82% 100%, 50% 75%, 18% 100%);
    }

    .shipCard::after {
        content: '';
        position: absolute;
        width: 70px;
        height: 70px;
        border-radius: 999px;
        right: -28px;
        top: -28px;
        background: var(--ship-glow, rgba(255,255,255,0.08));
        filter: blur(2px);
        opacity: 0.6;
    }

    .shipCard:hover, .shipCard.selected {
        transform: translateY(-2px);
        border-color: rgba(255, 190, 100, 0.66);
        background: rgba(255, 122, 47, 0.15);
    }

    .relicGrid { grid-template-columns: repeat(3, 1fr); }
    .relicCard {
        min-height: 145px;
        cursor: pointer;
        transition: transform .12s ease, border-color .12s ease, background .12s ease;
        text-align: left;
    }

    .relicCard:hover {
        transform: translateY(-3px);
        border-color: rgba(255, 190, 100, 0.70);
        background: rgba(255, 122, 47, 0.12);
    }

    .itemTitle {
        font-weight: 900;
        color: #fff8ec;
        margin-bottom: 5px;
        font-size: 15px;
    }

    .itemText {
        color: rgba(247,247,251,0.70);
        font-size: 12px;
        line-height: 1.35;
    }

    .rarity {
        display: inline-block;
        margin-top: 9px;
        padding: 3px 8px;
        border-radius: 999px;
        font-size: 11px;
        background: rgba(255,255,255,0.10);
        color: rgba(255,248,236,0.86);
    }

    .leaderboard {
        margin-top: 14px;
        border-radius: 18px;
        overflow: hidden;
        background: rgba(0,0,0,0.28);
        border: 1px solid rgba(255,255,255,0.10);
        text-align: left;
    }

    .leaderTitle {
        padding: 11px 14px;
        font-size: 13px;
        font-weight: 900;
        color: #fff8ec;
        background: rgba(255,255,255,0.07);
    }

    table {
        width: 100%;
        border-collapse: collapse;
        font-size: 12px;
    }

    th, td {
        padding: 8px 12px;
        border-bottom: 1px solid rgba(255,255,255,0.07);
        color: rgba(247,247,251,0.76);
    }

    th { color: rgba(255,248,236,0.92); font-size: 11px; text-transform: uppercase; }
    tr:last-child td { border-bottom: 0; }

    .smallNote {
        color: rgba(247,247,251,0.56);
        font-size: 12px;
        margin-top: 8px;
    }

    .rowButtons {
        display: flex;
        gap: 10px;
        justify-content: center;
        flex-wrap: wrap;
        margin-top: 14px;
    }

    .statLine {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 8px;
        margin: 14px 0;
    }

    .statBox {
        padding: 12px 8px;
        background: rgba(0,0,0,0.26);
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 14px;
    }

    .statValue {
        font-weight: 900;
        color: #fff8ec;
        font-size: 18px;
    }

    .statLabel {
        color: rgba(247,247,251,0.58);
        font-size: 11px;
        margin-top: 3px;
    }

    @media (max-width: 760px) {
        .title { font-size: 38px; }
        .nameRow { grid-template-columns: 1fr; }
        .shipGrid, .tipGrid, .relicGrid { grid-template-columns: 1fr 1fr; }
        .statLine { grid-template-columns: 1fr 1fr; }
    }
</style>
</head>
<body>
<div class="wrap">
    <div id="gameShell">
        <canvas id="gameCanvas" width="920" height="620"></canvas>
        <div id="overlay"></div>
        <div class="hint">Move with mouse or touch. Dodge bullets. Collect coins, hearts and bombs. Press P to pause.</div>
    </div>
</div>
<script>
(() => {
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const overlay = document.getElementById('overlay');
const W = canvas.width;
const H = canvas.height;
const STORAGE_KEY = 'bulletInfernoRogueLeaderboardV2';

const SECRET_UNLOCK_KEY = 'bulletInfernoAstraelUnlockedV1';
const VOLUME_KEY = 'bulletInfernoMusicVolumeV1';

const MUSIC_URLS = {
    menu: 'https://res.cloudinary.com/dlxc7gaan/video/upload/v1778173238/The_Last_Shelter_fyk4h3.mp3',
    drone: 'https://res.cloudinary.com/dlxc7gaan/video/upload/v1778172894/Drone_The_Silent_Assassin_p4sgqx.mp3',
    widow: 'https://res.cloudinary.com/dlxc7gaan/video/upload/v1778172897/Scrap_Widow_The_Junkyard_Queen_kxwwdd.mp3',
    reaper: 'https://res.cloudinary.com/dlxc7gaan/video/upload/v1778172899/The_Coin_Reaper_The_Golden_Executioner_kxtgzi.mp3',
    maw: 'https://res.cloudinary.com/dlxc7gaan/video/upload/v1778172894/Golden_Maw_The_Gluttonous_Vault_rlwn7x.mp3',
    serpent: 'https://res.cloudinary.com/dlxc7gaan/video/upload/v1778172899/Void_Serpent_The_Astral_Devourer_v9kzy3.mp3',
    halo: 'https://res.cloudinary.com/dlxc7gaan/video/upload/v1778172897/Black_Halo_The_Corrupted_Eclipse_x2dh56.mp3',
    engine: '',
    furnace: 'https://res.cloudinary.com/dlxc7gaan/video/upload/v1778172897/Furnace_King_The_Eternal_Blacksmith_kokpxm.mp3',
    sun: 'https://res.cloudinary.com/dlxc7gaan/video/upload/v1778172897/The_Bullet_Sun_The_Solar_Supernova_xbzltr.mp3',
    tyrant: 'https://res.cloudinary.com/dlxc7gaan/video/upload/v1778172898/Astral_Tyrant_The_Celestial_Oppressor_gouxlo.mp3',
    astrael: 'https://res.cloudinary.com/dlxc7gaan/video/upload/v1778172895/Astrael_God_of_Inferno_hbv1am.mp3'
};

const COLORS = {
    text: '#f7f7fb',
    soft: 'rgba(247,247,251,0.70)',
    orange: '#ff7a2f',
    red: '#ef4444',
    coin: '#ffd166',
    blueBomb: '#60a5fa',
    purpleBomb: '#c084fc',
    goldBomb: '#facc15',
    heart: '#fb7185',
    invuln: '#34d399',
    crit: '#fff8ec'
};

const CRITICAL_BOMB_CHANCE = 0.12;
const INVULN_POWER_CHANCE = 1.00;
const INVULN_POWER_SECONDS = 3.0;

const SHIPS = {
    nova: {
        id: 'nova', name: 'Nova Wing', tag: 'Balanced',
        desc: 'Standard speed, standard hitbox, no special risk.',
        speed: 1.00, hitbox: 1.00, coinValue: 1.00, startingShield: 0,
        color: '#dbeafe', accent: '#60a5fa', trail: '#f97316'
    },
    razor: {
        id: 'razor', name: 'Razor Moth', tag: 'Fast',
        desc: 'Faster movement and smaller hitbox. Great for aggressive bomb grabs.',
        speed: 1.25, hitbox: 0.88, coinValue: 1.00, startingShield: 0,
        color: '#fda4af', accent: '#fb7185', trail: '#f43f5e'
    },
    vault: {
        id: 'vault', name: 'Vault Kite', tag: 'Greed',
        desc: 'Coins are worth 50% more, but the ship is slightly larger.',
        speed: 1.00, hitbox: 1.12, coinValue: 1.50, startingShield: 0,
        color: '#fde68a', accent: '#facc15', trail: '#f59e0b'
    },
    aegis: {
        id: 'aegis', name: 'Aegis Beetle', tag: 'Safe',
        desc: 'Starts with one shield, but movement is slower.',
        speed: 0.86, hitbox: 1.00, coinValue: 1.00, startingShield: 1,
        color: '#bbf7d0', accent: '#34d399', trail: '#22c55e'
    }
};

const BOSS_POOLS = [
    [
        {name:'Drone Core', archetype:'drone', color:'#7dd3fc', accent:'#c7d2fe', subtitle:'Neon Junkyard Sentinel'},
        {name:'Scrap Widow', archetype:'widow', color:'#a3a3a3', accent:'#f97316', subtitle:'Web Machine of Sector One'}
    ],
    [
        {name:'The Coin Reaper', archetype:'reaper', color:'#fbbf24', accent:'#111827', subtitle:'Greed Cathedral Keeper'},
        {name:'Golden Maw', archetype:'maw', color:'#facc15', accent:'#fb923c', subtitle:'A Hungry Vault of Teeth'}
    ],
    [
        {name:'Void Serpent', archetype:'serpent', color:'#a78bfa', accent:'#38bdf8', subtitle:'A Spiral From Nothing'},
        {name:'Black Halo', archetype:'halo', color:'#818cf8', accent:'#f0abfc', subtitle:'Gravity Ring Entity'}
    ],
    [
        {name:'Inferno Engine', archetype:'engine', color:'#fb7185', accent:'#f97316', subtitle:'Burning Reactor Beast'},
        {name:'Furnace King', archetype:'furnace', color:'#f97316', accent:'#fde68a', subtitle:'The Royal Machine of Fire'}
    ],
    [
        {name:'The Bullet Sun', archetype:'sun', color:'#facc15', accent:'#ef4444', subtitle:'Final Star of the Inferno'},
        {name:'Astral Tyrant', archetype:'tyrant', color:'#f472b6', accent:'#60a5fa', subtitle:'Ruler of the Last Orbit'}
    ]
];



const SECRET_BOSS = {
    name: 'Astrael, God of Inferno',
    archetype: 'astrael',
    color: '#f43f5e',
    accent: '#facc15',
    subtitle: 'The True Final God',
    secret: true
};
const RELICS = [
    {id:'magnet', name:'Magnetic Orbit', rarity:'Common', desc:'Coins, bombs and hearts are attracted to you from farther away.', apply: () => mods.magnet += 90},
    {id:'blue', name:'Blue Reactor', rarity:'Common', desc:'Blue bombs deal +1% boss HP damage.', apply: () => mods.blueDamage += 1},
    {id:'purple', name:'Violet Catalyst', rarity:'Rare', desc:'Purple bombs deal +2% boss HP damage.', apply: () => mods.purpleDamage += 2},
    {id:'solar', name:'Solar Fuse', rarity:'Legendary', desc:'Golden bombs deal +10% boss HP damage.', apply: () => mods.goldDamage += 10},
    {id:'coin', name:'Greed Lens', rarity:'Common', desc:'Coins are worth 50% more for the rest of this run.', apply: () => mods.coinValue += 0.5},
    {id:'slow', name:'Chrono Drift', rarity:'Rare', desc:'Enemy bullets move 10% slower.', apply: () => mods.bulletSlow *= 0.90},
    {id:'hitbox', name:'Micro Hull', rarity:'Rare', desc:'Your hitbox becomes 18% smaller.', apply: () => mods.hitbox *= 0.82},
    {id:'luck', name:'Lucky Fuse', rarity:'Rare', desc:'Bomb drop chances increase by 25%.', apply: () => mods.bombLuck *= 1.25},
    {id:'heart', name:'Heart Signal', rarity:'Common', desc:'Life drops become slightly more common.', apply: () => mods.heartBonus += 0.25},
    {id:'credit', name:'Emergency Credit', rarity:'Common', desc:'Revive cost is reduced by 250 coins.', apply: () => mods.reviveCost = Math.max(500, mods.reviveCost - 250)},
    {id:'shield', name:'Broken Shield', rarity:'Rare', desc:'Gain one shield hit right now.', apply: () => player.shields += 1},
    {id:'bombValue', name:'Fuse Collector', rarity:'Common', desc:'Bomb pickups also grant bonus score.', apply: () => mods.bombScore += 1},
    {id:'crit', name:'Critical Fuse', rarity:'Rare', desc:'Critical bombs become more common for this run.', apply: () => mods.critChance += 0.06},
    {id:'emerald', name:'Emerald Battery', rarity:'Rare', desc:'Invulnerable power ups last 1.5 seconds longer.', apply: () => mods.invulnBonus += 1.5}
];

let state = 'menu';
let selectedShipId = 'nova';
let playerName = 'Pilot';
let seed = 1;
let rand = Math.random;
let last = performance.now();
let elapsed = 0;
let runId = 0;
let paused = false;
let particles = [];
let bullets = [];
let stars = [];
let relicChoices = [];
let usedRelics = [];
let mouse = {x: W/2, y: H - 84, active: false};
let player, boss, mods, runStats;
let musicVolume = clamp(Number(localStorage.getItem(VOLUME_KEY) || '0.35'), 0, 1);
let currentMusic = null;
let currentMusicKey = '';


function makeSeededRandom(s) {
    let t = s >>> 0;
    return function() {
        t += 0x6D2B79F5;
        let r = Math.imul(t ^ t >>> 15, 1 | t);
        r ^= r + Math.imul(r ^ r >>> 7, 61 | r);
        return ((r ^ r >>> 14) >>> 0) / 4294967296;
    };
}

function clamp(v, min, max) { return Math.max(min, Math.min(max, v)); }
function lerp(a, b, t) { return a + (b - a) * t; }
function dist(a, b, c, d) { return Math.hypot(a - c, b - d); }
function formatTime(sec) {
    sec = Math.max(0, sec);
    const m = Math.floor(sec / 60);
    const s = Math.floor(sec % 60);
    return `${m}:${String(s).padStart(2, '0')}`;
}
function escapeHtml(str) {
    return String(str || '').replace(/[&<>'"]/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[ch]));
}

function loadBoard() {
    try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]'); }
    catch { return []; }
}
function saveBoard(items) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(items.slice(0, 10)));
}
function addBoardEntry(result) {
    const board = loadBoard();
    board.push(result);
    board.sort((a,b) => {
        if ((b.trueVictory?1:0) !== (a.trueVictory?1:0)) return (b.trueVictory?1:0) - (a.trueVictory?1:0);
        if ((b.victory?1:0) !== (a.victory?1:0)) return (b.victory?1:0) - (a.victory?1:0);
        if (b.bosses !== a.bosses) return b.bosses - a.bosses;
        if (b.score !== a.score) return b.score - a.score;
        return a.time - b.time;
    });
    saveBoard(board);
}
function boardHtml() {
    const board = loadBoard();
    if (!board.length) {
        return `<div class="leaderboard"><div class="leaderTitle">Leaderboard</div><div style="padding:13px;color:rgba(247,247,251,.62);font-size:13px;">No runs yet.</div></div>`;
    }
    const rows = board.slice(0, 8).map((r,i) => {
        const label = r.trueVictory ? 'God Clear' : (r.victory ? 'Victory' : 'Dead');
        const bosses = r.trueVictory ? 'Astrael' : `${r.bosses}/5`;
        return `
        <tr>
            <td>${i+1}</td>
            <td>${escapeHtml(r.name)}</td>
            <td>${label}</td>
            <td>${bosses}</td>
            <td>${r.coins}</td>
            <td>${r.score}</td>
            <td>${formatTime(r.time)}</td>
        </tr>`;
    }).join('');
    return `<div class="leaderboard"><div class="leaderTitle">Leaderboard</div><table><thead><tr><th>#</th><th>Name</th><th>Run</th><th>Boss</th><th>Coins</th><th>Score</th><th>Time</th></tr></thead><tbody>${rows}</tbody></table></div>`;
}

function isSecretUnlocked() {
    return localStorage.getItem(SECRET_UNLOCK_KEY) === '1';
}
function unlockSecretBoss() {
    localStorage.setItem(SECRET_UNLOCK_KEY, '1');
}

function showOverlay(html) {
    overlay.classList.remove('hidden');
    overlay.innerHTML = html;
}
function hideOverlay() {
    overlay.classList.add('hidden');
    overlay.innerHTML = '';
}

function renderMenu() {
    state = 'menu';
    paused = false;
    stopMusic();
    playMusic('menu');
    const unlocked = isSecretUnlocked();
    const shipCards = Object.values(SHIPS).map(s => `
        <div class="shipCard ${selectedShipId === s.id ? 'selected' : ''}" data-ship="${s.id}" style="--ship-glow:${hexToRgba(s.accent, 0.25)}; border-color:${selectedShipId === s.id ? hexToRgba(s.accent, 0.72) : 'rgba(255,255,255,0.10)'};">
            <div class="shipTop">
                <div class="shipSwatch" style="background:linear-gradient(135deg, ${s.color}, ${s.accent});"></div>
                <div class="itemTitle" style="margin-bottom:0;">${s.name}</div>
            </div>
            <div class="itemText"><b>${s.tag}</b><br>${s.desc}</div>
        </div>
    `).join('');
    showOverlay(`
        <div class="card">
            <h1 class="title">Bullet Inferno</h1>
            <div class="subtitle">Roguelike survival bullet hell. You do not shoot. You survive, collect bombs and break the bosses.</div>
            <div class="nameRow">
                <input id="nameInput" maxlength="18" placeholder="Pilot name" value="${escapeHtml(playerName)}" />
                <button class="primary" id="startBtn">Start Run</button>
            </div>
            <div class="volumeRow">
                <span>Music</span>
                <input id="volumeSlider" type="range" min="0" max="100" value="${Math.round(musicVolume*100)}" />
                <span id="volumeValue">${Math.round(musicVolume*100)}%</span>
            </div>
            <div class="rowButtons">
                <button class="${unlocked ? 'godButton' : 'lockedButton'}" id="godBtn" ${unlocked ? '' : 'disabled'}>${unlocked ? 'Final Boss: Astrael' : 'Final Boss Locked'}</button>
            </div>
            <div class="smallNote">${unlocked ? 'Astrael, God of Inferno, is unlocked. This is a standalone God Trial.' : 'Unlock the Final Boss by clearing all 5 zones once.'}</div>
            <div class="shipGrid">${shipCards}</div>
            <div class="tipGrid">
                <div class="tip">Blue bomb<br><b>5% boss damage</b><br>2% chance</div>
                <div class="tip">Purple bomb<br><b>10% boss damage</b><br>1% chance</div>
                <div class="tip">Golden bomb<br><b>50% boss damage</b><br>0.01% chance</div>
                <div class="tip">Heart<br><b>+1 life</b><br>0.5% chance, max 3</div>
                <div class="tip">Power up<br><b>3 sec invulnerable</b><br>1% chance</div>
                <div class="tip">Critical bomb<br><b>Bonus damage</b><br>+current lives</div>
            </div>
            <div class="smallNote">Critical bombs have a ${Math.round(CRITICAL_BOMB_CHANCE*100)}% chance. Extra damage equals your current lives, so 3 lives adds +3% damage.</div>
            ${boardHtml()}
            <div class="rowButtons">
                <button class="secondary" id="clearBtn">Clear leaderboard</button>
            </div>
            <div class="smallNote">Music loops automatically. If your browser blocks autoplay, click anywhere in the game once.</div>
        </div>
    `);

    document.querySelectorAll('.shipCard').forEach(card => {
        card.addEventListener('click', () => {
            selectedShipId = card.getAttribute('data-ship');
            playSfx('select');
            const input = document.getElementById('nameInput');
            if (input) playerName = input.value || 'Pilot';
            renderMenu();
        });
    });
    const slider = document.getElementById('volumeSlider');
    if (slider) {
        slider.addEventListener('input', () => {
            updateMusicVolume(Number(slider.value) / 100);
            const label = document.getElementById('volumeValue');
            if (label) label.textContent = `${slider.value}%`;
            if (state === 'menu') playMusic('menu');
        });
    }
    document.getElementById('startBtn').addEventListener('click', () => {
        playerName = (document.getElementById('nameInput').value || 'Pilot').trim().slice(0, 18) || 'Pilot';
        playSfx('start');
        startRun();
    });
    const godBtn = document.getElementById('godBtn');
    if (godBtn && unlocked) {
        godBtn.addEventListener('click', () => {
            playerName = (document.getElementById('nameInput').value || 'Pilot').trim().slice(0, 18) || 'Pilot';
            playSfx('start');
            startFinalBoss();
        });
    }
    document.getElementById('clearBtn').addEventListener('click', () => {
        localStorage.removeItem(STORAGE_KEY);
        playSfx('click');
        renderMenu();
    });
}

function resetMods(ship) {
    return {
        coinValue: ship.coinValue,
        blueDamage: 5,
        purpleDamage: 10,
        goldDamage: 50,
        magnet: 0,
        bombLuck: 1,
        heartBonus: 0,
        bulletSlow: 1,
        hitbox: ship.hitbox,
        reviveCost: 1000,
        bombScore: 0,
        critChance: CRITICAL_BOMB_CHANCE,
        invulnBonus: 0
    };
}

function startRun() {
    runId++;
    seed = Math.floor(Date.now() % 99999999);
    rand = makeSeededRandom(seed);
    const ship = SHIPS[selectedShipId] || SHIPS.nova;
    player = {
        x: W/2,
        y: H - 90,
        lives: 3,
        maxLives: 3,
        shields: ship.startingShield || 0,
        invuln: 1.2,
        ship,
        r: 10,
        targetX: W/2,
        targetY: H - 90
    };
    mods = resetMods(ship);
    runStats = {
        zone: 1,
        bossesKilled: 0,
        coins: 0,
        score: 0,
        bombs: {blue: 0, purple: 0, gold: 0},
        critBombs: 0,
        powerups: 0,
        hearts: 0,
        revives: 0,
        seed,
        activeTime: 0,
        victory: false,
        secretTrial: false
    };
    bullets = [];
    particles = [];
    usedRelics = [];
    relicChoices = [];
    elapsed = 0;
    mouse.x = W/2;
    mouse.y = H - 90;
    stopMusic();
    spawnBoss(1);
    hideOverlay();
    state = 'playing';
}

function startFinalBoss() {
    if (!isSecretUnlocked()) return;
    runId++;
    seed = Math.floor(Date.now() % 99999999);
    rand = makeSeededRandom(seed);
    const ship = SHIPS[selectedShipId] || SHIPS.nova;
    player = {
        x: W/2,
        y: H - 90,
        lives: 3,
        maxLives: 3,
        shields: ship.startingShield || 0,
        invuln: 1.6,
        ship,
        r: 10,
        targetX: W/2,
        targetY: H - 90
    };
    mods = resetMods(ship);
    runStats = {
        zone: 6,
        bossesKilled: 0,
        coins: 0,
        score: 0,
        bombs: {blue: 0, purple: 0, gold: 0},
        critBombs: 0,
        powerups: 0,
        hearts: 0,
        revives: 0,
        seed,
        activeTime: 0,
        victory: false,
        secretTrial: true
    };
    bullets = [];
    particles = [];
    usedRelics = [];
    relicChoices = [];
    elapsed = 0;
    mouse.x = W/2;
    mouse.y = H - 90;
    stopMusic();
    spawnSecretBoss();
    hideOverlay();
    state = 'playing';
}

function spawnBoss(zone) {
    const pool = BOSS_POOLS[zone - 1] || BOSS_POOLS[0];
    const base = pool[Math.floor(rand() * pool.length)];
    boss = {
        ...base,
        zone,
        x: W/2,
        y: 86,
        hp: 100,
        maxHp: 100,
        size: 46 + zone * 4,
        fireCooldown: 0.5,
        moveT: rand() * 10,
        hitTimer: 0,
        deathTimer: 0,
        dead: false,
        defeatedHandled: false,
        intro: 1.4
    };
    addTextParticle(W/2, 220, `Zone ${zone}: ${boss.name}`, boss.color, 1.6, 30);
    playBossMusic();
}

function spawnSecretBoss() {
    boss = {
        ...SECRET_BOSS,
        zone: 6,
        x: W/2,
        y: 92,
        hp: 100,
        maxHp: 100,
        size: 78,
        fireCooldown: 0.42,
        moveT: rand() * 10,
        hitTimer: 0,
        deathTimer: 0,
        dead: false,
        defeatedHandled: false,
        intro: 2.0,
        secret: true
    };
    addTextParticle(W/2, 220, 'FINAL TRIAL', '#fff8ec', 1.4, 34);
    addTextParticle(W/2, 265, boss.name, boss.color, 1.7, 30);
    playBossMusic();
}

function completeBoss() {
    stopMusic();
    runStats.bossesKilled += 1;
    runStats.score += boss.secret ? 7000 : 1000 + boss.zone * 350;
    bullets = bullets.filter(o => o.type !== 'bullet');
    if (boss.secret) {
        trueVictory();
    } else if (boss.zone >= 5) {
        victory();
    } else {
        showRelicChoice();
    }
}

function chooseRelics() {
    const available = RELICS.filter(r => !usedRelics.includes(r.id) || ['coin','blue','purple','heart','luck'].includes(r.id));
    const picks = [];
    while (picks.length < 3 && available.length) {
        const i = Math.floor(rand() * available.length);
        const r = available.splice(i, 1)[0];
        picks.push(r);
    }
    return picks;
}

function showRelicChoice() {
    state = 'relic';
    paused = false;
    relicChoices = chooseRelics();
    const relicHtml = relicChoices.map((r, idx) => `
        <div class="relicCard" data-relic="${idx}">
            <div class="itemTitle">${r.name}</div>
            <div class="itemText">${r.desc}</div>
            <span class="rarity">${r.rarity}</span>
        </div>
    `).join('');
    const rerollDisabled = runStats.coins < 150 ? 'disabled' : '';
    showOverlay(`
        <div class="card">
            <h1 class="title" style="font-size:42px;">Boss Defeated</h1>
            <div class="subtitle">Choose one relic for this run. It disappears when the run ends.</div>
            <div class="statLine">
                <div class="statBox"><div class="statValue">${runStats.bossesKilled}/5</div><div class="statLabel">Bosses defeated</div></div>
                <div class="statBox"><div class="statValue">${runStats.coins}</div><div class="statLabel">Coins</div></div>
                <div class="statBox"><div class="statValue">${formatTime(runStats.activeTime)}</div><div class="statLabel">Time</div></div>
                <div class="statBox"><div class="statValue">${runStats.score}</div><div class="statLabel">Score</div></div>
            </div>
            <div class="relicGrid">${relicHtml}</div>
            <div class="rowButtons">
                <button class="secondary" id="rerollBtn" ${rerollDisabled}>Reroll relics - 150 coins</button>
            </div>
            <div class="smallNote">Next zone will start after selecting a relic.</div>
        </div>
    `);
    document.querySelectorAll('.relicCard').forEach(card => {
        card.addEventListener('click', () => {
            const r = relicChoices[Number(card.getAttribute('data-relic'))];
            if (!r) return;
            playSfx('relic');
            r.apply();
            usedRelics.push(r.id);
            runStats.score += 200;
            runStats.zone += 1;
            bullets = [];
            particles = [];
            spawnBoss(runStats.zone);
            hideOverlay();
            state = 'playing';
            player.invuln = 1.2;
            addTextParticle(W/2, H/2, r.name, '#fff8ec', 1.2, 26);
        });
    });
    const reroll = document.getElementById('rerollBtn');
    if (reroll) {
        reroll.addEventListener('click', () => {
            if (runStats.coins >= 150) {
                runStats.coins -= 150;
                playSfx('click');
                showRelicChoice();
            }
        });
    }
}

function victory() {
    playSfx('victory');
    state = 'victory';
    runStats.victory = true;
    unlockSecretBoss();
    addBoardEntry({
        name: playerName,
        victory: true,
        trueVictory: false,
        bosses: runStats.bossesKilled,
        coins: runStats.coins,
        score: runStats.score,
        time: runStats.activeTime,
        seed: runStats.seed
    });
    showOverlay(`
        <div class="card">
            <h1 class="title">Victory</h1>
            <div class="subtitle">You cleared all 5 zones. The Final Boss is now unlocked from the main menu.</div>
            ${resultStatsHtml()}
            <div class="rowButtons">
                <button class="godButton" id="godBtn">Fight Astrael</button>
                <button class="primary" id="againBtn">New Run</button>
                <button class="secondary" id="menuBtn">Main Menu</button>
            </div>
        </div>
    `);
    document.getElementById('godBtn').addEventListener('click', () => startFinalBoss());
    document.getElementById('againBtn').addEventListener('click', () => startRun());
    document.getElementById('menuBtn').addEventListener('click', () => renderMenu());
}

function trueVictory() {
    playSfx('victory');
    state = 'truevictory';
    runStats.victory = true;
    addBoardEntry({
        name: playerName,
        victory: true,
        trueVictory: true,
        bosses: 6,
        coins: runStats.coins,
        score: runStats.score + 5000,
        time: runStats.activeTime,
        seed: runStats.seed
    });
    showOverlay(`
        <div class="card">
            <h1 class="title" style="font-size:46px;">True Victory</h1>
            <div class="subtitle">Astrael, God of Inferno, has fallen. The leaderboard will mark this as God Clear.</div>
            ${resultStatsHtml()}
            <div class="rowButtons">
                <button class="godButton" id="godAgainBtn">Fight Astrael Again</button>
                <button class="primary" id="againBtn">New Run</button>
                <button class="secondary" id="menuBtn">Main Menu</button>
            </div>
        </div>
    `);
    document.getElementById('godAgainBtn').addEventListener('click', () => startFinalBoss());
    document.getElementById('againBtn').addEventListener('click', () => startRun());
    document.getElementById('menuBtn').addEventListener('click', () => renderMenu());
}

function permanentGameOver() {
    stopMusic();
    state = 'ended';
    addBoardEntry({
        name: playerName,
        victory: false,
        trueVictory: false,
        bosses: runStats.bossesKilled,
        coins: runStats.coins,
        score: runStats.score,
        time: runStats.activeTime,
        seed: runStats.seed
    });
    showOverlay(`
        <div class="card">
            <h1 class="title" style="font-size:48px;">Game Over</h1>
            <div class="subtitle">The inferno got you. Final result saved to the leaderboard.</div>
            ${resultStatsHtml()}
            <div class="rowButtons">
                <button class="primary" id="againBtn">Try Again</button>
                <button class="secondary" id="menuBtn">Main Menu</button>
            </div>
        </div>
    `);
    document.getElementById('againBtn').addEventListener('click', () => startRun());
    document.getElementById('menuBtn').addEventListener('click', () => renderMenu());
}

function showGameOver() {
    stopMusic();
    state = 'gameover';
    const canRevive = runStats.coins >= mods.reviveCost;
    showOverlay(`
        <div class="card">
            <h1 class="title" style="font-size:48px;">Game Over</h1>
            <div class="subtitle">Spend coins to buy one life and continue this run.</div>
            ${resultStatsHtml()}
            <div class="rowButtons">
                <button class="primary" id="reviveBtn" ${canRevive ? '' : 'disabled'}>Buy 1 Life - ${mods.reviveCost} coins</button>
                <button class="secondary" id="endBtn">End Run</button>
            </div>
            <div class="smallNote">You have ${runStats.coins} coins. Revives used: ${runStats.revives}.</div>
        </div>
    `);
    document.getElementById('reviveBtn').addEventListener('click', () => {
        if (runStats.coins >= mods.reviveCost) {
            runStats.coins -= mods.reviveCost;
            runStats.revives += 1;
            playSfx('revive');
            player.lives = 1;
            player.invuln = 2.5;
            player.x = W/2;
            player.y = H - 90;
            mouse.x = player.x;
            mouse.y = player.y;
            bullets = [];
            particles = [];
            hideOverlay();
            state = 'playing';
            addTextParticle(W/2, H/2, 'Revived', '#fff8ec', 1.0, 32);
        }
    });
    document.getElementById('endBtn').addEventListener('click', permanentGameOver);
}

function resultStatsHtml() {
    const bossLabel = runStats.secretTrial ? `${runStats.bossesKilled}/1` : `${runStats.bossesKilled}/5`;
    const bossText = runStats.secretTrial ? 'God defeated' : 'Bosses defeated';
    return `
        <div class="statLine">
            <div class="statBox"><div class="statValue">${bossLabel}</div><div class="statLabel">${bossText}</div></div>
            <div class="statBox"><div class="statValue">${runStats.coins}</div><div class="statLabel">Coins</div></div>
            <div class="statBox"><div class="statValue">${formatTime(runStats.activeTime)}</div><div class="statLabel">Time</div></div>
            <div class="statBox"><div class="statValue">${runStats.score}</div><div class="statLabel">Score</div></div>
        </div>
        <div class="smallNote">Bombs: blue ${runStats.bombs.blue}, purple ${runStats.bombs.purple}, golden ${runStats.bombs.gold}. Critical bombs: ${runStats.critBombs || 0}. Power ups: ${runStats.powerups || 0}. Seed: ${runStats.seed}.</div>
    `;
}

function damagePlayer() {
    if (player.invuln > 0 || state !== 'playing') return;
    if (player.shields > 0) {
        player.shields -= 1;
        player.invuln = 1.25;
        addBurst(player.x, player.y, '#93c5fd', 18, 4, 1.2);
        playSfx('shield');
        addTextParticle(player.x, player.y - 22, 'Shield', '#bfdbfe', 0.8, 18);
        return;
    }
    player.lives -= 1;
    player.invuln = 1.6;
    addBurst(player.x, player.y, COLORS.red, 22, 5, 1.4);
    playSfx(player.lives <= 0 ? 'destroy' : 'hit');
    if (player.lives <= 0) {
        addBurst(player.x, player.y, '#fff8ec', 38, 7, 1.1);
        showGameOver();
    }
}

function collectPickup(o) {
    if (o.type === 'coin') {
        const gained = Math.round(10 * mods.coinValue);
        runStats.coins += gained;
        runStats.score += gained * 2;
        addBurst(o.x, o.y, COLORS.coin, 8, 2.5, 0.65);
        playSfx('coin');
    } else if (o.type === 'heart') {
        if (player.lives < player.maxLives) {
            player.lives += 1;
            runStats.hearts += 1;
            addTextParticle(o.x, o.y, '+1 Life', COLORS.heart, 0.75, 16);
        } else {
            runStats.score += 120;
            addTextParticle(o.x, o.y, 'Max', COLORS.heart, 0.65, 15);
        }
        addBurst(o.x, o.y, COLORS.heart, 12, 3, 0.8);
        playSfx('heart');
    } else if (o.type === 'power_invuln') {
        const powerSeconds = INVULN_POWER_SECONDS + (mods.invulnBonus || 0);
        player.invuln = Math.max(player.invuln, powerSeconds);
        runStats.powerups += 1;
        runStats.score += 250;
        addBurst(o.x, o.y, COLORS.invuln, 18, 4.5, 1.0);
        addTextParticle(o.x, o.y, 'Invulnerable', COLORS.invuln, 0.9, 18);
        playSfx('powerup');
    } else if (o.type === 'bomb_blue') {
        hitBoss(mods.blueDamage, COLORS.blueBomb, 'blue', !!o.critical);
    } else if (o.type === 'bomb_purple') {
        hitBoss(mods.purpleDamage, COLORS.purpleBomb, 'purple', !!o.critical);
    } else if (o.type === 'bomb_gold') {
        hitBoss(mods.goldDamage, COLORS.goldBomb, 'gold', !!o.critical);
    }
}

function hitBoss(baseDmg, color, kind, critical=false) {
    if (!boss || boss.dead) return;
    const critBonus = critical ? Math.max(1, player.lives) : 0;
    const dmg = baseDmg + critBonus;
    boss.hp = Math.max(0, boss.hp - dmg);
    boss.hitTimer = critical ? 0.32 : 0.22;
    runStats.bombs[kind] += 1;
    if (critical) runStats.critBombs += 1;
    runStats.score += Math.round(dmg * (critical ? 90 : 50) + mods.bombScore * 100);
    addBurst(boss.x, boss.y, critical ? COLORS.crit : color, critical ? 32 : (kind === 'gold' ? 34 : 18), critical ? 7 : (kind === 'gold' ? 8 : 4), critical ? 1.25 : 1.0);
    const txt = critical ? `CRIT -${dmg}%` : `-${dmg}%`;
    addTextParticle(boss.x + (rand()*50-25), boss.y + boss.size + 8, txt, critical ? COLORS.crit : color, 0.85, critical ? 25 : (kind === 'gold' ? 26 : 18));
    playSfx(critical ? 'crit' : (kind === 'gold' ? 'goldBomb' : 'bomb'));
    if (boss.hp <= 0 && !boss.dead) {
        boss.dead = true;
        boss.deathTimer = 1.7;
        bullets = bullets.filter(o => o.type !== 'bullet');
        playSfx('bossDeath');
        for (let i=0; i<70; i++) addParticle(boss.x, boss.y, boss.color, rand()*7+2, rand()*Math.PI*2, rand()*210+70, 1.2 + rand()*0.9);
        addTextParticle(W/2, 220, `${boss.name} defeated`, '#fff8ec', 1.4, 28);
    }
}

function projectileKind() {
    const luck = mods.bombLuck;
    const pGold = 0.01 * luck;
    const pPurple = 1.00 * luck;
    const pBlue = 2.00 * luck;
    const pHeart = 0.50 + mods.heartBonus;
    const pInvuln = INVULN_POWER_CHANCE;
    const pCoin = 8.5;
    const r = rand() * 100;
    if (r < pGold) return 'bomb_gold';
    if (r < pGold + pPurple) return 'bomb_purple';
    if (r < pGold + pPurple + pBlue) return 'bomb_blue';
    if (r < pGold + pPurple + pBlue + pInvuln) return 'power_invuln';
    if (r < pGold + pPurple + pBlue + pInvuln + pHeart) return 'heart';
    if (r < pGold + pPurple + pBlue + pInvuln + pHeart + pCoin) return 'coin';
    return 'bullet';
}

function spawnShot(x, y, angle, speed, radius=6, forceKind=null) {
    const kind = forceKind || projectileKind();
    let sp = speed * mods.bulletSlow;
    let r = radius;
    if (kind !== 'bullet') {
        sp *= 0.62;
        r = kind === 'bomb_gold' ? 13 : kind === 'bomb_purple' ? 11 : kind === 'bomb_blue' ? 10 : kind === 'heart' ? 10 : kind === 'power_invuln' ? 12 : 8;
    }
    const isBomb = kind === 'bomb_gold' || kind === 'bomb_purple' || kind === 'bomb_blue';
    const critical = isBomb && rand() < mods.critChance;
    bullets.push({
        type: kind,
        critical,
        x, y,
        vx: Math.cos(angle) * sp,
        vy: Math.sin(angle) * sp,
        r,
        rot: rand() * Math.PI * 2,
        spin: (rand() - 0.5) * 5,
        color: boss ? boss.color : COLORS.red,
        wobble: rand() * Math.PI * 2,
        life: 0
    });
}

function bossAggro() {
    const phase = boss.hp < 35 ? 2 : boss.hp < 68 ? 1 : 0;
    return 1 + boss.zone * 0.18 + phase * 0.22;
}

function updateBoss(dt) {
    if (!boss || state !== 'playing') return;
    boss.moveT += dt;
    boss.hitTimer = Math.max(0, boss.hitTimer - dt);
    boss.intro = Math.max(0, boss.intro - dt);

    if (boss.dead) {
        boss.deathTimer -= dt;
        if (rand() < 0.55) addParticle(boss.x + (rand()-0.5)*boss.size*1.5, boss.y + (rand()-0.5)*boss.size, boss.accent, 4, rand()*Math.PI*2, 80+rand()*130, 0.8);
        if (boss.deathTimer <= 0 && !boss.defeatedHandled) {
            boss.defeatedHandled = true;
            completeBoss();
        }
        return;
    }

    const amp = 95 + boss.zone * 14;
    boss.x = W/2 + Math.sin(boss.moveT * (0.8 + boss.zone*0.05)) * amp;
    boss.y = 82 + Math.sin(boss.moveT * 1.7) * 10;

    boss.fireCooldown -= dt;
    if (boss.fireCooldown <= 0 && boss.intro <= 0) {
        fireBossPattern();
        const ag = bossAggro();
        boss.fireCooldown = Math.max(0.18, (0.68 - boss.zone * 0.055) / ag);
    }
}

function fireBossPattern() {
    const ag = bossAggro();
    const toPlayer = Math.atan2(player.y - boss.y, player.x - boss.x);
    const speed = 110 + boss.zone * 22 + ag * 22;
    const nBase = 5 + boss.zone;
    switch (boss.archetype) {
        case 'drone': {
            const spread = 0.95;
            for (let i=0; i<nBase; i++) {
                const a = toPlayer - spread/2 + spread * (i/(nBase-1 || 1));
                spawnShot(boss.x, boss.y + boss.size*0.5, a, speed, 6);
            }
            break;
        }
        case 'widow': {
            for (let side=-1; side<=1; side+=2) {
                for (let i=0; i<5+boss.zone; i++) {
                    const a = Math.PI/2 + side * (0.25 + i*0.11);
                    spawnShot(boss.x + side*28, boss.y+20, a, speed*0.96, 5.8);
                }
            }
            break;
        }
        case 'reaper': {
            for (let i=0; i<9+boss.zone; i++) {
                const a = Math.PI/2 + Math.sin(elapsed*2+i)*0.7 + (i-(4+boss.zone/2))*0.055;
                spawnShot(boss.x + (i%2?22:-22), boss.y+28, a, speed*0.95, 6.2);
            }
            break;
        }
        case 'maw': {
            for (let i=0; i<6+boss.zone; i++) {
                const x = 40 + rand()*(W-80);
                spawnShot(x, -10, Math.PI/2 + (rand()-0.5)*0.25, speed*0.78, 6.4);
            }
            if (rand() < 0.4) spawnShot(boss.x, boss.y+34, toPlayer, speed*1.2, 7.5);
            break;
        }
        case 'serpent': {
            const base = elapsed * 2.4;
            for (let i=0; i<4+boss.zone; i++) {
                spawnShot(boss.x, boss.y+20, base + i*Math.PI*2/(4+boss.zone), speed*0.9, 5.8);
                spawnShot(boss.x, boss.y+20, -base + i*Math.PI*2/(4+boss.zone), speed*0.82, 5.8);
            }
            break;
        }
        case 'halo': {
            const count = 12 + boss.zone*2;
            const base = elapsed * 1.2;
            for (let i=0; i<count; i++) {
                const a = base + i*Math.PI*2/count;
                if (Math.sin(i + elapsed*3) > -0.25) spawnShot(boss.x, boss.y, a, speed*0.72, 5.5);
            }
            break;
        }
        case 'engine': {
            for (let burst=0; burst<2; burst++) {
                for (let i=0; i<6; i++) {
                    const a = toPlayer + (i-2.5)*0.13 + (burst?0.12:-0.12);
                    spawnShot(boss.x + (burst?30:-30), boss.y+25, a, speed*1.25, 5.4);
                }
            }
            break;
        }
        case 'furnace': {
            const gap = Math.floor(rand()*7);
            for (let i=0; i<11; i++) {
                if (Math.abs(i-gap) <= 1) continue;
                spawnShot(i*(W/10), -8, Math.PI/2, speed*0.88, 7);
            }
            for (let i=0; i<5; i++) spawnShot(boss.x, boss.y+32, Math.PI/2 + (i-2)*0.24, speed, 6.5);
            break;
        }
        case 'sun': {
            const count = 18 + boss.zone*2;
            const base = elapsed * 1.8;
            for (let i=0; i<count; i++) {
                const a = base + i*Math.PI*2/count;
                spawnShot(boss.x, boss.y, a, speed*0.72, 5.7);
            }
            for (let i=0; i<3; i++) spawnShot(boss.x, boss.y+20, toPlayer + (i-1)*0.18, speed*1.2, 7);
            break;
        }
        case 'tyrant': {
            for (let ring=0; ring<2; ring++) {
                const count = 10 + ring*5;
                const base = elapsed * (ring ? -1.5 : 1.4);
                for (let i=0; i<count; i++) {
                    const a = base + i*Math.PI*2/count;
                    spawnShot(boss.x + Math.cos(a)*25, boss.y + Math.sin(a)*12, a + 0.35, speed*(0.78+ring*0.1), 5.8);
                }
            }
            break;
        }
        case 'astrael': {
            const phase = boss.hp < 34 ? 3 : boss.hp < 67 ? 2 : 1;
            const base = elapsed * (phase === 3 ? 2.4 : 1.55);
            const ringCount = phase === 3 ? 28 : phase === 2 ? 22 : 16;
            for (let i=0; i<ringCount; i++) {
                const a = base + i*Math.PI*2/ringCount;
                if (phase !== 3 || i % 5 !== Math.floor(elapsed*3)%5) {
                    spawnShot(boss.x, boss.y, a, speed*(0.70 + phase*0.05), 5.7);
                }
            }
            if (phase >= 2) {
                for (let i=0; i<7; i++) {
                    const a = toPlayer + (i-3)*0.16;
                    spawnShot(boss.x + Math.sin(elapsed*3)*35, boss.y+28, a, speed*1.18, 6.4);
                }
            }
            if (phase === 3) {
                const gap = Math.floor(rand()*9);
                for (let i=0; i<13; i++) {
                    if (Math.abs(i-gap) <= 1) continue;
                    spawnShot(30 + i*(W-60)/12, -10, Math.PI/2 + Math.sin(elapsed+i)*0.08, speed*0.88, 6.9);
                }
                for (let side=-1; side<=1; side+=2) {
                    spawnShot(boss.x + side*55, boss.y+35, toPlayer + side*0.35, speed*1.35, 7.2);
                }
            }
            break;
        }
        default: {
            for (let i=0; i<nBase; i++) spawnShot(boss.x, boss.y, toPlayer + (i-nBase/2)*0.12, speed, 6);
        }
    }
}

function updatePlayer(dt) {
    if (!player || state !== 'playing') return;
    const smooth = clamp(dt * 9.5 * player.ship.speed, 0, 0.55);
    player.x = lerp(player.x, mouse.x, smooth);
    player.y = lerp(player.y, mouse.y, smooth);
    player.x = clamp(player.x, 18, W-18);
    player.y = clamp(player.y, 120, H-18);
    player.invuln = Math.max(0, player.invuln - dt);
    player.r = 10 * mods.hitbox;
}

function updateBullets(dt) {
    const keep = [];
    for (const o of bullets) {
        o.life += dt;
        o.rot += o.spin * dt;
        o.wobble += dt * 5;
        if (o.type !== 'bullet' && mods.magnet > 0) {
            const d = dist(o.x, o.y, player.x, player.y);
            if (d < mods.magnet && d > 1) {
                const pull = (1 - d/mods.magnet) * 380;
                o.vx += (player.x - o.x) / d * pull * dt;
                o.vy += (player.y - o.y) / d * pull * dt;
            }
        }
        if (o.type === 'bullet' && (boss.archetype === 'serpent' || boss.archetype === 'halo')) {
            o.vx += Math.cos(o.wobble) * 6 * dt;
        }
        o.x += o.vx * dt;
        o.y += o.vy * dt;
        const pr = player.r;
        const hit = dist(o.x, o.y, player.x, player.y) < (o.r + pr);
        if (hit) {
            if (o.type === 'bullet') damagePlayer();
            else collectPickup(o);
            continue;
        }
        if (o.x > -70 && o.x < W+70 && o.y > -90 && o.y < H+90) keep.push(o);
    }
    bullets = keep;
}

function addParticle(x,y,color,r,angle,speed,life) {
    particles.push({x,y,color,r,vx:Math.cos(angle)*speed,vy:Math.sin(angle)*speed,life,maxLife:life,kind:'dot'});
}
function addTextParticle(x,y,text,color,life,size) {
    particles.push({x,y,text,color,life,maxLife:life,kind:'text',size,vy:-28});
}
function addBurst(x,y,color,count,speed,life) {
    for (let i=0; i<count; i++) addParticle(x,y,color,rand()*3+1,rand()*Math.PI*2,rand()*70+speed*30,life*(0.65+rand()*0.55));
}
function updateParticles(dt) {
    const next = [];
    for (const p of particles) {
        p.life -= dt;
        if (p.life <= 0) continue;
        if (p.kind === 'text') {
            p.y += p.vy * dt;
        } else {
            p.x += p.vx * dt;
            p.y += p.vy * dt;
            p.vx *= Math.pow(0.05, dt);
            p.vy *= Math.pow(0.05, dt);
        }
        next.push(p);
    }
    particles = next;
}

function makeStars() {
    stars = [];
    for (let i=0; i<130; i++) {
        stars.push({x:rand()*W, y:rand()*H, z:rand()*1.8+0.4, tw:rand()*Math.PI*2});
    }
}
makeStars();

function updateStars(dt) {
    for (const s of stars) {
        s.y += (12 + s.z*12) * dt;
        s.tw += dt * 2;
        if (s.y > H) { s.y = -4; s.x = rand()*W; }
    }
}

function drawBackground() {
    const zone = runStats ? runStats.zone : 1;
    const grad = ctx.createRadialGradient(W/2, 80, 20, W/2, H/2, H);
    const bossColor = boss ? boss.color : '#ff7a2f';
    grad.addColorStop(0, `${hexToRgba(bossColor, 0.25)}`);
    grad.addColorStop(0.45, '#070716');
    grad.addColorStop(1, '#020209');
    ctx.fillStyle = grad;
    ctx.fillRect(0,0,W,H);

    for (const s of stars) {
        const a = 0.35 + Math.sin(s.tw)*0.25;
        ctx.fillStyle = `rgba(255,255,255,${a})`;
        ctx.beginPath();
        ctx.arc(s.x,s.y,s.z,0,Math.PI*2);
        ctx.fill();
    }

    ctx.save();
    ctx.globalAlpha = 0.045;
    ctx.strokeStyle = bossColor;
    ctx.lineWidth = 1;
    const step = 46;
    for (let x=-step; x<W+step; x+=step) {
        ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x-80, H); ctx.stroke();
    }
    for (let y=0; y<H; y+=step) {
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y+30); ctx.stroke();
    }
    ctx.restore();

    ctx.fillStyle = 'rgba(255,255,255,0.03)';
    ctx.font = 'bold 82px Arial';
    ctx.textAlign = 'center';
    ctx.fillText(`ZONE ${zone}`, W/2, H/2 + 20);
}

function hexToRgba(hex, alpha) {
    const h = hex.replace('#','');
    const bigint = parseInt(h.length === 3 ? h.split('').map(c=>c+c).join('') : h, 16);
    const r = (bigint >> 16) & 255;
    const g = (bigint >> 8) & 255;
    const b = bigint & 255;
    return `rgba(${r},${g},${b},${alpha})`;
}

function drawUI() {
    if (!runStats || !boss) return;
    ctx.save();
    ctx.textAlign = 'left';
    ctx.fillStyle = 'rgba(0,0,0,0.28)';
    roundRect(18, 14, W-36, 78, 16, true, false);

    const barX = 170, barY = 28, barW = W - 330, barH = 16;
    ctx.fillStyle = 'rgba(255,255,255,0.11)';
    roundRect(barX, barY, barW, barH, 8, true, false);
    ctx.fillStyle = boss.dead ? '#f7f7fb' : boss.color;
    roundRect(barX, barY, barW * clamp(boss.hp/100,0,1), barH, 8, true, false);
    ctx.strokeStyle = 'rgba(255,255,255,0.16)';
    roundRect(barX, barY, barW, barH, 8, false, true);

    ctx.fillStyle = '#fff8ec';
    ctx.font = '900 17px Arial';
    ctx.fillText(boss.name, 32, 38);
    ctx.fillStyle = 'rgba(247,247,251,0.58)';
    ctx.font = '12px Arial';
    ctx.fillText(boss.subtitle, 32, 58);

    ctx.textAlign = 'right';
    ctx.fillStyle = '#fff8ec';
    ctx.font = '900 15px Arial';
    ctx.fillText(`HP ${Math.ceil(boss.hp)}%`, W - 32, 38);
    ctx.fillStyle = 'rgba(247,247,251,0.70)';
    ctx.font = '12px Arial';
    ctx.fillText(`Seed ${runStats.seed}`, W - 32, 58);

    ctx.textAlign = 'left';
    let x = 32, y = 82;
    ctx.font = '900 13px Arial';
    ctx.fillStyle = '#fff8ec';
    ctx.fillText(`Lives ${'♥'.repeat(Math.max(0, player.lives))}`, x, y);
    ctx.fillStyle = 'rgba(247,247,251,0.70)';
    ctx.fillText(` Shields ${player.shields}`, x+95, y);
    ctx.fillText(` Coins ${runStats.coins}`, x+178, y);
    ctx.fillText(` Score ${runStats.score}`, x+278, y);
    ctx.fillText(` Time ${formatTime(runStats.activeTime)}`, x+392, y);
    ctx.fillText(runStats.secretTrial ? ` God Trial` : ` Bosses ${runStats.bossesKilled}/5`, x+505, y);
    if (player.invuln > 0) {
        ctx.fillStyle = COLORS.invuln;
        ctx.fillText(` Invulnerable ${player.invuln.toFixed(1)}s`, x+610, y);
    }
    ctx.textAlign = 'right';
    ctx.fillStyle = 'rgba(247,247,251,0.70)';
    ctx.fillText('P = Pause', W-32, y);
    ctx.restore();
}

function roundRect(x, y, w, h, r, fill, stroke) {
    if (w < 2*r) r = w/2;
    if (h < 2*r) r = h/2;
    ctx.beginPath();
    ctx.moveTo(x+r, y);
    ctx.arcTo(x+w, y, x+w, y+h, r);
    ctx.arcTo(x+w, y+h, x, y+h, r);
    ctx.arcTo(x, y+h, x, y, r);
    ctx.arcTo(x, y, x+w, y, r);
    ctx.closePath();
    if (fill) ctx.fill();
    if (stroke) ctx.stroke();
}

function drawBoss() {
    if (!boss || state === 'menu') return;
    ctx.save();
    let shakeX = 0, shakeY = 0;
    if (boss.hitTimer > 0) {
        shakeX = (rand()-0.5)*8;
        shakeY = (rand()-0.5)*8;
    }
    ctx.translate(boss.x + shakeX, boss.y + shakeY);
    const alpha = boss.dead ? clamp(boss.deathTimer / 1.7, 0, 1) : 1;
    const scale = boss.dead ? 0.75 + alpha*0.35 : 1;
    ctx.scale(scale, scale);
    ctx.globalAlpha = alpha;

    const c = boss.hitTimer > 0 ? '#ffffff' : boss.color;
    const a = boss.accent;
    const s = boss.size;

    ctx.shadowBlur = boss.dead ? 0 : 22;
    ctx.shadowColor = c;

    switch (boss.archetype) {
        case 'drone': drawDrone(c,a,s); break;
        case 'widow': drawWidow(c,a,s); break;
        case 'reaper': drawReaper(c,a,s); break;
        case 'maw': drawMaw(c,a,s); break;
        case 'serpent': drawSerpent(c,a,s); break;
        case 'halo': drawHalo(c,a,s); break;
        case 'engine': drawEngine(c,a,s); break;
        case 'furnace': drawFurnace(c,a,s); break;
        case 'sun': drawSun(c,a,s); break;
        case 'tyrant': drawTyrant(c,a,s); break;
        case 'astrael': drawAstrael(c,a,s); break;
        default: drawDrone(c,a,s);
    }
    ctx.restore();
}

function drawDrone(c,a,s) {
    ctx.fillStyle = 'rgba(0,0,0,0.35)';
    ctx.beginPath(); ctx.ellipse(0, 12, s*1.55, s*0.34, 0, 0, Math.PI*2); ctx.fill();
    ctx.strokeStyle = a; ctx.lineWidth = 5;
    ctx.beginPath(); ctx.moveTo(-s*1.25, 0); ctx.lineTo(s*1.25, 0); ctx.stroke();
    ctx.fillStyle = c; ctx.beginPath(); ctx.arc(0,0,s*0.72,0,Math.PI*2); ctx.fill();
    ctx.fillStyle = '#050511'; ctx.beginPath(); ctx.arc(0,0,s*0.36,0,Math.PI*2); ctx.fill();
    ctx.fillStyle = a; ctx.beginPath(); ctx.arc(0,0,s*0.18,0,Math.PI*2); ctx.fill();
    for (let side of [-1,1]) { ctx.fillStyle = a; ctx.beginPath(); ctx.arc(side*s*1.25,0,s*0.23,0,Math.PI*2); ctx.fill(); }
}
function drawWidow(c,a,s) {
    ctx.strokeStyle = a; ctx.lineWidth = 4;
    for (let i=0;i<4;i++){ const ang=-0.8+i*0.55; ctx.beginPath(); ctx.moveTo(0,0); ctx.lineTo(Math.cos(ang)*s*1.6, Math.sin(ang)*s*1.2); ctx.stroke(); ctx.beginPath(); ctx.moveTo(0,0); ctx.lineTo(-Math.cos(ang)*s*1.6, Math.sin(ang)*s*1.2); ctx.stroke(); }
    ctx.fillStyle=c; ctx.beginPath(); ctx.ellipse(0,0,s*0.8,s*0.58,0,0,Math.PI*2); ctx.fill();
    ctx.fillStyle='#050511'; ctx.beginPath(); ctx.arc(-s*0.25,-s*0.1,s*0.12,0,Math.PI*2); ctx.arc(s*0.25,-s*0.1,s*0.12,0,Math.PI*2); ctx.fill();
}
function drawReaper(c,a,s) {
    ctx.fillStyle=c; ctx.beginPath(); ctx.arc(0,0,s*0.8,0,Math.PI*2); ctx.fill();
    ctx.fillStyle='#050511'; ctx.beginPath(); ctx.arc(-s*0.26,-s*0.08,s*0.17,0,Math.PI*2); ctx.arc(s*0.26,-s*0.08,s*0.17,0,Math.PI*2); ctx.fill();
    ctx.strokeStyle=a; ctx.lineWidth=5; ctx.beginPath(); ctx.arc(0,0,s*1.12,Math.PI*0.12,Math.PI*0.88); ctx.stroke();
    ctx.fillStyle=a; for(let i=-2;i<=2;i++){ ctx.beginPath(); ctx.moveTo(i*s*0.18,s*0.35); ctx.lineTo(i*s*0.18+s*0.08,s*0.55); ctx.lineTo(i*s*0.18-s*0.08,s*0.55); ctx.fill(); }
}
function drawMaw(c,a,s) {
    ctx.fillStyle=c; ctx.beginPath(); ctx.ellipse(0,0,s*1.05,s*0.72,0,0,Math.PI*2); ctx.fill();
    ctx.fillStyle='#050511'; ctx.beginPath(); ctx.ellipse(0,s*0.12,s*0.72,s*0.32,0,0,Math.PI*2); ctx.fill();
    ctx.fillStyle=a; for(let i=-4;i<=4;i++){ ctx.beginPath(); ctx.moveTo(i*s*0.16,-s*0.05); ctx.lineTo(i*s*0.16+s*0.08,s*0.22); ctx.lineTo(i*s*0.16-s*0.08,s*0.22); ctx.fill(); }
}
function drawSerpent(c,a,s) {
    for(let i=7;i>=0;i--){ const x=Math.sin(elapsed*2+i*0.9)*s*0.35*i/3; const y=i*s*0.18; ctx.fillStyle=i===0?c:hexToRgba(c,0.88-i*0.055); ctx.beginPath(); ctx.arc(x,y,s*(0.52-i*0.028),0,Math.PI*2); ctx.fill(); }
    ctx.fillStyle=a; ctx.beginPath(); ctx.arc(-s*0.18,-s*0.07,s*0.09,0,Math.PI*2); ctx.arc(s*0.18,-s*0.07,s*0.09,0,Math.PI*2); ctx.fill();
}
function drawHalo(c,a,s) {
    ctx.strokeStyle=c; ctx.lineWidth=10; ctx.beginPath(); ctx.ellipse(0,0,s*1.15,s*0.68,elapsed*0.4,0,Math.PI*2); ctx.stroke();
    ctx.strokeStyle=a; ctx.lineWidth=4; ctx.beginPath(); ctx.ellipse(0,0,s*0.72,s*1.05,-elapsed*0.3,0,Math.PI*2); ctx.stroke();
    ctx.fillStyle='#050511'; ctx.beginPath(); ctx.arc(0,0,s*0.36,0,Math.PI*2); ctx.fill();
    ctx.fillStyle=c; ctx.beginPath(); ctx.arc(0,0,s*0.18,0,Math.PI*2); ctx.fill();
}
function drawEngine(c,a,s) {
    ctx.fillStyle=c; roundRect(-s*0.95,-s*0.6,s*1.9,s*1.2,12,true,false);
    ctx.fillStyle='#050511'; roundRect(-s*0.55,-s*0.32,s*1.1,s*0.64,10,true,false);
    ctx.fillStyle=a; ctx.beginPath(); ctx.arc(0,0,s*0.25,0,Math.PI*2); ctx.fill();
    ctx.fillStyle=hexToRgba(a,0.55); ctx.beginPath(); ctx.moveTo(-s*0.45,s*0.63); ctx.lineTo(0,s*1.28+Math.sin(elapsed*20)*6); ctx.lineTo(s*0.45,s*0.63); ctx.fill();
}
function drawFurnace(c,a,s) {
    ctx.fillStyle=c; ctx.beginPath(); ctx.moveTo(-s, s*0.55); ctx.lineTo(-s*0.65,-s*0.6); ctx.lineTo(0,-s*0.95); ctx.lineTo(s*0.65,-s*0.6); ctx.lineTo(s,s*0.55); ctx.closePath(); ctx.fill();
    ctx.fillStyle='#050511'; ctx.beginPath(); ctx.arc(0,0,s*0.42,0,Math.PI*2); ctx.fill();
    ctx.strokeStyle=a; ctx.lineWidth=5; ctx.beginPath(); ctx.arc(0,0,s*0.6,0,Math.PI*2); ctx.stroke();
}
function drawSun(c,a,s) {
    ctx.fillStyle=a; ctx.beginPath();
    for(let i=0;i<24;i++){ const r=i%2?s*1.05:s*1.42; const ang=elapsed*0.7+i*Math.PI*2/24; ctx.lineTo(Math.cos(ang)*r, Math.sin(ang)*r); }
    ctx.closePath(); ctx.fill();
    ctx.fillStyle=c; ctx.beginPath(); ctx.arc(0,0,s*0.82,0,Math.PI*2); ctx.fill();
    ctx.fillStyle='#050511'; ctx.beginPath(); ctx.arc(0,0,s*0.32,0,Math.PI*2); ctx.fill();
}
function drawTyrant(c,a,s) {
    ctx.strokeStyle=a; ctx.lineWidth=5;
    for(let i=0;i<3;i++){ ctx.beginPath(); ctx.ellipse(0,0,s*(0.75+i*0.23),s*(0.32+i*0.16),elapsed*(i%2?-0.5:0.5)+i,0,Math.PI*2); ctx.stroke(); }
    ctx.fillStyle=c; ctx.beginPath(); ctx.arc(0,0,s*0.6,0,Math.PI*2); ctx.fill();
    ctx.fillStyle='#050511'; ctx.beginPath(); ctx.moveTo(0,-s*0.27); ctx.lineTo(s*0.28,s*0.22); ctx.lineTo(-s*0.28,s*0.22); ctx.closePath(); ctx.fill();
}
function drawAstrael(c,a,s) {
    ctx.save();
    ctx.rotate(Math.sin(elapsed*0.8)*0.08);
    ctx.strokeStyle=a; ctx.lineWidth=6;
    for(let i=0;i<4;i++){
        ctx.beginPath();
        ctx.ellipse(0,0,s*(0.72+i*0.18),s*(0.28+i*0.11),elapsed*(i%2?-0.52:0.52)+i*Math.PI/4,0,Math.PI*2);
        ctx.stroke();
    }
    ctx.fillStyle=hexToRgba(a,0.55);
    ctx.beginPath();
    for(let i=0;i<18;i++){ const r=i%2?s*0.92:s*1.28; const ang=-Math.PI/2+i*Math.PI*2/18+elapsed*0.35; ctx.lineTo(Math.cos(ang)*r, Math.sin(ang)*r); }
    ctx.closePath(); ctx.fill();
    ctx.fillStyle=c; ctx.beginPath(); ctx.arc(0,0,s*0.62,0,Math.PI*2); ctx.fill();
    ctx.fillStyle='#050511'; ctx.beginPath(); ctx.ellipse(0,0,s*0.38,s*0.22,0,0,Math.PI*2); ctx.fill();
    ctx.fillStyle='#fff8ec'; ctx.beginPath(); ctx.ellipse(0,0,s*0.17,s*0.10,0,0,Math.PI*2); ctx.fill();
    ctx.strokeStyle=hexToRgba('#fff8ec',0.8); ctx.lineWidth=2; ctx.beginPath(); ctx.arc(0,0,s*0.84,0,Math.PI*2); ctx.stroke();
    ctx.restore();
}

function drawBullets() {
    for (const o of bullets) {
        ctx.save();
        ctx.translate(o.x,o.y);
        ctx.rotate(o.rot);
        if (o.type === 'bullet') {
            ctx.shadowBlur = 12;
            ctx.shadowColor = o.color;
            ctx.fillStyle = o.color;
            ctx.beginPath(); ctx.arc(0,0,o.r,0,Math.PI*2); ctx.fill();
            ctx.fillStyle = 'rgba(255,255,255,0.28)';
            ctx.beginPath(); ctx.arc(-o.r*0.25,-o.r*0.25,o.r*0.35,0,Math.PI*2); ctx.fill();
        } else if (o.type === 'coin') {
            ctx.shadowBlur = 10; ctx.shadowColor = COLORS.coin;
            ctx.fillStyle = COLORS.coin;
            ctx.beginPath(); ctx.ellipse(0,0,o.r*0.75,o.r,0,0,Math.PI*2); ctx.fill();
            ctx.strokeStyle = '#a16207'; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(0,0,o.r*0.55,0,Math.PI*2); ctx.stroke();
        } else if (o.type === 'heart') {
            ctx.shadowBlur = 12; ctx.shadowColor = COLORS.heart;
            ctx.fillStyle = COLORS.heart;
            drawHeart(0,0,o.r);
        } else if (o.type === 'power_invuln') {
            ctx.shadowBlur = 18; ctx.shadowColor = COLORS.invuln;
            ctx.fillStyle = COLORS.invuln;
            ctx.beginPath();
            for (let i=0;i<10;i++) {
                const rr = i%2 ? o.r*0.55 : o.r*1.15;
                const a = -Math.PI/2 + i*Math.PI*2/10;
                ctx.lineTo(Math.cos(a)*rr, Math.sin(a)*rr);
            }
            ctx.closePath(); ctx.fill();
            ctx.strokeStyle = 'rgba(255,255,255,0.9)'; ctx.lineWidth = 2;
            ctx.beginPath(); ctx.arc(0,0,o.r*1.3,0,Math.PI*2); ctx.stroke();
        } else {
            const color = o.type === 'bomb_blue' ? COLORS.blueBomb : o.type === 'bomb_purple' ? COLORS.purpleBomb : COLORS.goldBomb;
            ctx.shadowBlur = o.critical ? 28 : (o.type === 'bomb_gold' ? 22 : 14);
            ctx.shadowColor = o.critical ? COLORS.crit : color;
            ctx.fillStyle = color;
            ctx.beginPath(); ctx.arc(0,0,o.r,0,Math.PI*2); ctx.fill();
            ctx.fillStyle = 'rgba(255,255,255,0.88)';
            ctx.fillRect(-2,-o.r-6,4,7);
            ctx.strokeStyle = o.critical ? COLORS.crit : '#fff8ec'; ctx.lineWidth = o.critical ? 3 : 2;
            ctx.beginPath(); ctx.arc(0,0,o.r*0.62,0,Math.PI*2); ctx.stroke();
            if (o.critical) {
                ctx.strokeStyle = COLORS.crit;
                ctx.lineWidth = 2;
                ctx.beginPath();
                for (let i=0;i<4;i++) {
                    const a = Math.PI/4 + i*Math.PI/2;
                    ctx.lineTo(Math.cos(a)*o.r*1.65, Math.sin(a)*o.r*1.65);
                }
                ctx.closePath(); ctx.stroke();
            }
        }
        ctx.restore();
    }
}
function drawHeart(x,y,r) {
    ctx.beginPath();
    ctx.moveTo(x, y + r*0.55);
    ctx.bezierCurveTo(x - r*1.1, y - r*0.15, x - r*0.62, y - r*0.85, x, y - r*0.35);
    ctx.bezierCurveTo(x + r*0.62, y - r*0.85, x + r*1.1, y - r*0.15, x, y + r*0.55);
    ctx.fill();
}

function drawPlayer() {
    if (!player || state === 'menu') return;
    if (player.invuln > 0 && Math.floor(elapsed*14)%2===0) return;
    const shipColor = player.ship.color || '#dbeafe';
    const shipAccent = player.ship.accent || '#60a5fa';
    const trail = player.ship.trail || '#f97316';
    ctx.save();
    ctx.translate(player.x, player.y);
    if (player.invuln > 0) {
        ctx.strokeStyle = hexToRgba(COLORS.invuln, 0.78);
        ctx.lineWidth = 3;
        ctx.shadowBlur = 24;
        ctx.shadowColor = COLORS.invuln;
        ctx.beginPath(); ctx.arc(0,0,28 + Math.sin(elapsed*9)*3,0,Math.PI*2); ctx.stroke();
    }
    ctx.shadowBlur = 16;
    ctx.shadowColor = shipAccent;
    ctx.fillStyle = shipColor;
    ctx.beginPath();
    ctx.moveTo(0, -18);
    ctx.lineTo(13, 13);
    ctx.lineTo(0, 7);
    ctx.lineTo(-13, 13);
    ctx.closePath();
    ctx.fill();
    ctx.fillStyle = shipAccent;
    ctx.beginPath(); ctx.moveTo(0,-8); ctx.lineTo(6,8); ctx.lineTo(-6,8); ctx.closePath(); ctx.fill();
    ctx.fillStyle = trail;
    ctx.beginPath(); ctx.moveTo(-5,13); ctx.lineTo(0,24+Math.sin(elapsed*28)*4); ctx.lineTo(5,13); ctx.fill();
    if (player.shields > 0) {
        ctx.strokeStyle = 'rgba(147,197,253,0.75)';
        ctx.lineWidth = 2;
        ctx.beginPath(); ctx.arc(0,0,24 + Math.sin(elapsed*5)*2,0,Math.PI*2); ctx.stroke();
    }
    ctx.restore();
}
function drawParticles() {
    for (const p of particles) {
        const alpha = clamp(p.life / p.maxLife, 0, 1);
        ctx.save();
        ctx.globalAlpha = alpha;
        if (p.kind === 'text') {
            ctx.font = `900 ${p.size}px Arial`;
            ctx.textAlign = 'center';
            ctx.fillStyle = p.color;
            ctx.shadowBlur = 12;
            ctx.shadowColor = p.color;
            ctx.fillText(p.text, p.x, p.y);
        } else {
            ctx.fillStyle = p.color;
            ctx.beginPath(); ctx.arc(p.x,p.y,p.r*alpha,0,Math.PI*2); ctx.fill();
        }
        ctx.restore();
    }
}

function drawPause() {
    if (!paused || state !== 'playing') return;
    ctx.save();
    ctx.fillStyle = 'rgba(0,0,0,0.45)';
    ctx.fillRect(0,0,W,H);
    ctx.fillStyle = '#fff8ec';
    ctx.font = '900 44px Arial';
    ctx.textAlign = 'center';
    ctx.fillText('Paused', W/2, H/2);
    ctx.font = '15px Arial';
    ctx.fillStyle = 'rgba(247,247,251,0.72)';
    ctx.fillText('Press P to continue', W/2, H/2 + 34);
    ctx.restore();
}

function updateMusicVolume(v) {
    musicVolume = clamp(Number(v) || 0, 0, 1);
    localStorage.setItem(VOLUME_KEY, String(musicVolume));
    if (currentMusic) currentMusic.volume = musicVolume;
}
function stopMusic() {
    if (currentMusic) {
        currentMusic.pause();
        currentMusic.currentTime = 0;
    }
    currentMusic = null;
    currentMusicKey = '';
}
function playMusic(key) {
    const src = MUSIC_URLS[key];
    if (!src) {
        stopMusic();
        return;
    }
    if (currentMusic && currentMusicKey === key) {
        currentMusic.volume = musicVolume;
        currentMusic.loop = true;
        currentMusic.play().catch(() => {});
        return;
    }
    stopMusic();
    currentMusicKey = key;
    currentMusic = new Audio(src);
    currentMusic.loop = true;
    currentMusic.volume = musicVolume;
    currentMusic.play().catch(() => {});
}
function playBossMusic() {
    if (!boss) return;
    playMusic(boss.archetype || '');
}

document.addEventListener('pointerdown', () => {
    getAudioContext();
    if (state === 'menu') playMusic('menu');
    else if (state === 'playing') playBossMusic();
});

function getAudioContext() {
    if (!window.AudioContext && !window.webkitAudioContext) return null;
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    if (!window.__biAudio) window.__biAudio = new AudioCtx();
    const ac = window.__biAudio;
    if (ac.state === 'suspended') ac.resume();
    return ac;
}

function playTone(freq=440, duration=0.05, type='sine', volume=0.04, delay=0) {
    try {
        const ac = getAudioContext();
        if (!ac) return;
        const osc = ac.createOscillator();
        const gain = ac.createGain();
        const startAt = ac.currentTime + delay;
        osc.type = type;
        osc.frequency.value = freq;
        gain.gain.setValueAtTime(Math.max(0.0001, volume * (0.35 + musicVolume)), startAt);
        osc.connect(gain);
        gain.connect(ac.destination);
        osc.start(startAt);
        gain.gain.exponentialRampToValueAtTime(0.0001, startAt + duration);
        osc.stop(startAt + duration + 0.02);
    } catch(e) {}
}

function playSfx(name) {
    switch(name) {
        case 'click': playTone(520, 0.035, 'triangle', 0.020); break;
        case 'select': playTone(620, 0.035, 'triangle', 0.020); playTone(820, 0.035, 'triangle', 0.016, 0.035); break;
        case 'start': playTone(320, 0.055, 'sawtooth', 0.026); playTone(540, 0.06, 'triangle', 0.024, 0.055); break;
        case 'coin': playTone(860, 0.035, 'triangle', 0.026); playTone(1180, 0.035, 'triangle', 0.018, 0.028); break;
        case 'heart': playTone(520, 0.06, 'sine', 0.032); playTone(740, 0.07, 'sine', 0.024, 0.05); break;
        case 'powerup': playTone(700, 0.08, 'triangle', 0.035); playTone(980, 0.10, 'sine', 0.025, 0.07); break;
        case 'bomb': playTone(330, 0.07, 'square', 0.032); break;
        case 'goldBomb': playTone(220, 0.08, 'square', 0.038); playTone(440, 0.06, 'triangle', 0.024, 0.05); break;
        case 'crit': playTone(190, 0.09, 'sawtooth', 0.050); playTone(760, 0.06, 'square', 0.026, 0.045); break;
        case 'hit': playTone(150, 0.10, 'sawtooth', 0.044); break;
        case 'shield': playTone(420, 0.06, 'triangle', 0.030); break;
        case 'destroy': playTone(110, 0.18, 'sawtooth', 0.060); playTone(70, 0.22, 'square', 0.035, 0.08); break;
        case 'bossDeath': playTone(120, 0.18, 'sawtooth', 0.052); playTone(260, 0.16, 'square', 0.038, 0.08); playTone(520, 0.14, 'triangle', 0.032, 0.18); break;
        case 'relic': playTone(560, 0.07, 'triangle', 0.030); playTone(840, 0.08, 'sine', 0.025, 0.06); break;
        case 'revive': playTone(300, 0.08, 'sine', 0.030); playTone(600, 0.10, 'triangle', 0.030, 0.08); break;
        case 'victory': playTone(520, 0.10, 'triangle', 0.035); playTone(780, 0.10, 'triangle', 0.030, 0.09); playTone(1040, 0.14, 'sine', 0.026, 0.18); break;
        case 'pause': playTone(260, 0.05, 'triangle', 0.022); break;
        default: playTone(500, 0.04, 'triangle', 0.018);
    }
}

document.addEventListener('click', (e) => {
    if (e.target.closest('button')) playSfx('click');
});

function update(dt) {
    if (state === 'playing' && !paused) {
        elapsed += dt;
        runStats.activeTime += dt;
        updateStars(dt);
        updatePlayer(dt);
        updateBoss(dt);
        updateBullets(dt);
        updateParticles(dt);
    } else {
        updateStars(dt * 0.5);
        updateParticles(dt * 0.5);
    }
}
function draw() {
    drawBackground();
    drawBoss();
    drawBullets();
    drawPlayer();
    drawParticles();
    drawUI();
    drawPause();
}
function loop(now) {
    const dt = Math.min(0.033, (now - last) / 1000);
    last = now;
    update(dt);
    draw();
    requestAnimationFrame(loop);
}

canvas.addEventListener('mousemove', (e) => {
    const rect = canvas.getBoundingClientRect();
    mouse.x = (e.clientX - rect.left) * W / rect.width;
    mouse.y = (e.clientY - rect.top) * H / rect.height;
    mouse.active = true;
});
canvas.addEventListener('touchmove', (e) => {
    e.preventDefault();
    const t = e.touches[0];
    const rect = canvas.getBoundingClientRect();
    mouse.x = (t.clientX - rect.left) * W / rect.width;
    mouse.y = (t.clientY - rect.top) * H / rect.height;
    mouse.active = true;
}, {passive:false});
window.addEventListener('keydown', (e) => {
    if (e.key.toLowerCase() === 'p' && state === 'playing') { paused = !paused; playSfx('pause'); }
    if (e.key === 'Escape' && state === 'playing') { paused = !paused; playSfx('pause'); }
});

// Start with an empty scene behind the menu.
player = {x:W/2, y:H-90, lives:3, maxLives:3, shields:0, invuln:0, ship:SHIPS.nova, r:10};
mods = resetMods(SHIPS.nova);
runStats = {zone:1,bossesKilled:0,coins:0,score:0,bombs:{blue:0,purple:0,gold:0},critBombs:0,powerups:0,hearts:0,revives:0,seed:0,activeTime:0,victory:false,secretTrial:false};
boss = {name:'Bullet Inferno', subtitle:'Waiting for a pilot', archetype:'sun', color:'#ff7a2f', accent:'#ef4444', x:W/2, y:95, hp:100, size:48, hitTimer:0, dead:false};
renderMenu();
requestAnimationFrame(loop);
})();
</script>
</body>
</html>
"""

components.html(GAME_HTML, height=750, scrolling=False)

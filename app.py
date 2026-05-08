import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Bullet Inferno Roguelike v9.7",
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

    #gameSignature {
        position: absolute;
        right: 26px;
        bottom: 52px;
        z-index: 20;
        pointer-events: none;
        font-size: 10px;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: rgba(247,247,251,0.42);
        text-shadow: 0 1px 8px rgba(0,0,0,0.85);
        user-select: none;
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
        margin: 0 auto 10px;
        padding: 10px 14px;
        border-radius: 14px;
        background: rgba(0,0,0,0.24);
        border: 1px solid rgba(255,255,255,0.10);
        color: rgba(247,247,251,0.78);
        font-size: 13px;
    }

    .volumeGroup {
        margin: 0 auto 16px;
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

    .shipGrid, .relicGrid, .tipGrid, .modeGrid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px;
        margin: 14px 0 16px;
    }

    .modeGrid {
        grid-template-columns: repeat(3, 1fr);
    }

    .modeCard {
        border-radius: 16px;
        padding: 13px 11px;
        background: rgba(0,0,0,0.27);
        border: 1px solid rgba(255,255,255,0.10);
        color: rgba(247,247,251,0.82);
        min-height: 84px;
        text-align: left;
        transition: transform .12s ease, border-color .12s ease, background .12s ease;
    }

    .modeCard:hover {
        transform: translateY(-2px);
        border-color: rgba(255, 190, 100, 0.66);
        background: rgba(255, 122, 47, 0.13);
    }

    .modeCard .modeTitle {
        font-weight: 900;
        color: #fff8ec;
        margin-bottom: 6px;
        font-size: 14px;
    }

    .modeCard .modeDesc {
        color: rgba(247,247,251,0.70);
        font-size: 12px;
        line-height: 1.35;
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

    .shipPreviewWrap {
        position: relative;
        min-height: 94px;
        margin: 6px 0 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 14px;
        background: radial-gradient(circle at center, var(--ship-glow, rgba(255,255,255,0.12)), rgba(0,0,0,0.06) 58%, rgba(0,0,0,0.0) 100%);
        overflow: hidden;
    }

    .shipPreviewWrap::before {
        content: '';
        position: absolute;
        width: 120px;
        height: 120px;
        border-radius: 999px;
        background: var(--ship-glow, rgba(255,255,255,0.10));
        filter: blur(18px);
        opacity: 0.75;
    }

    .shipPreview {
        position: relative;
        z-index: 1;
        max-width: 112px;
        max-height: 88px;
        object-fit: contain;
        filter: drop-shadow(0 0 14px var(--ship-glow, rgba(255,255,255,0.28)));
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

    .libraryHeader {
        margin-top: 18px;
        padding-top: 12px;
        border-top: 1px solid rgba(255,255,255,0.10);
        text-align: left;
        color: #fff8ec;
        font-weight: 900;
        font-size: 16px;
    }

    .relicLibrary {
        margin: 10px 0 16px;
        max-height: 260px;
        overflow: auto;
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 8px;
        padding-right: 4px;
    }

    .libraryRelic {
        text-align: left;
        border-radius: 14px;
        padding: 10px 11px;
        background: rgba(0,0,0,0.20);
        border: 1px solid rgba(255,255,255,0.08);
    }

    .libraryRelic.practicePick {
        cursor: pointer;
        transition: transform .14s ease, border-color .14s ease, background .14s ease;
    }

    .libraryRelic.practicePick:hover {
        transform: translateY(-1px);
        border-color: rgba(255,122,47,0.42);
    }

    .libraryRelic.selected {
        background: rgba(255,122,47,0.12);
        border-color: rgba(255,122,47,0.70);
        box-shadow: 0 0 0 1px rgba(255,122,47,0.12) inset;
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



    .menuActions {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px;
        margin: 18px auto 12px;
        max-width: 720px;
    }

    .menuActionBtn {
        height: 58px;
        padding: 0 16px;
        background: rgba(255,255,255,0.09);
        border: 1px solid rgba(255,255,255,0.12);
        color: #fff8ec;
        font-size: 14px;
        box-shadow: none;
    }

    .menuActionBtn.primaryAction {
        background: linear-gradient(135deg, rgba(255,122,47,0.95), rgba(217,31,69,0.88));
        box-shadow: 0 14px 30px rgba(217,31,69,0.25);
    }

    .navTop {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        margin-bottom: 16px;
        text-align: left;
    }

    .navTitle {
        font-size: 27px;
        font-weight: 900;
        color: #fff8ec;
        line-height: 1.05;
    }

    .navSub {
        margin-top: 5px;
        font-size: 13px;
        color: rgba(247,247,251,0.62);
        line-height: 1.35;
    }

    .sectionCard {
        margin-top: 12px;
        padding: 14px;
        border-radius: 18px;
        background: rgba(0,0,0,0.22);
        border: 1px solid rgba(255,255,255,0.09);
        text-align: left;
    }

    .modeCard.locked {
        opacity: .68;
        cursor: not-allowed;
        background: rgba(255,255,255,0.055);
    }

    .modeMeta, .shipMeta {
        margin-top: 8px;
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
    }

    .pill {
        display: inline-flex;
        align-items: center;
        min-height: 22px;
        padding: 2px 8px;
        border-radius: 999px;
        background: rgba(255,255,255,0.10);
        color: rgba(255,248,236,0.78);
        font-size: 11px;
        font-weight: 700;
    }

    .menuDetails {
        margin-top: 12px;
        border-radius: 16px;
        background: rgba(255,255,255,0.055);
        border: 1px solid rgba(255,255,255,0.09);
        text-align: left;
        overflow: hidden;
    }

    .menuDetails summary {
        cursor: pointer;
        padding: 12px 14px;
        color: #fff8ec;
        font-weight: 900;
        list-style: none;
    }

    .menuDetails summary::-webkit-details-marker { display: none; }

    .dropGrid {
        padding: 0 12px 12px;
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 8px;
    }

    .dropCard {
        padding: 11px;
        border-radius: 14px;
        background: rgba(0,0,0,0.22);
        border: 1px solid rgba(255,255,255,0.08);
        min-height: 94px;
    }

    .filterBar, .tabBar {
        display: flex;
        align-items: center;
        gap: 8px;
        flex-wrap: wrap;
        margin: 10px 0 12px;
    }

    .filterBtn, .tabBtn {
        height: 34px;
        padding: 0 13px;
        border-radius: 12px;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.10);
        color: rgba(247,247,251,0.78);
        font-size: 12px;
        box-shadow: none;
    }

    .filterBtn.active, .tabBtn.active {
        background: rgba(255,122,47,0.23);
        border-color: rgba(255,122,47,0.55);
        color: #fff8ec;
    }

    .searchInput {
        height: 38px;
        flex: 1 1 220px;
        font-size: 13px;
    }

    .compactList {
        max-height: 395px;
        overflow: auto;
        padding-right: 4px;
    }

    .libraryRelic .metaLine {
        margin-top: 8px;
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
    }

    .settingsGrid {
        display: grid;
        grid-template-columns: 1fr;
        gap: 10px;
        max-width: 610px;
        margin: 0 auto;
    }

    .dangerZone {
        margin-top: 14px;
        padding-top: 12px;
        border-top: 1px solid rgba(255,255,255,0.10);
    }



    .activeItemGrid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
        margin: 14px 0;
    }

    .activeItemCard {
        text-align: left;
        padding: 13px;
        border-radius: 16px;
        background: rgba(255,255,255,0.055);
        border: 1px solid rgba(255,255,255,0.11);
        cursor: pointer;
        transition: transform .14s ease, border-color .14s ease, background .14s ease;
    }

    .activeItemCard:hover { transform: translateY(-1px); border-color: rgba(255,122,47,0.45); }

    .activeItemCard.selected {
        background: rgba(255,122,47,0.12);
        border-color: rgba(255,122,47,0.70);
        box-shadow: 0 0 0 1px rgba(255,122,47,0.12) inset;
    }

    .activeItemCard.disabled {
        opacity: 0.40;
        cursor: not-allowed;
    }

    .loadoutBar {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        align-items: center;
        justify-content: center;
        margin: 10px 0 4px;
    }

    .tinyTag {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 5px 9px;
        border-radius: 999px;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.10);
        color: rgba(247,247,251,0.80);
        font-size: 12px;
        font-weight: 700;
    }
    .footerNote {
        margin-top: 14px;
        color: rgba(247,247,251,0.42);
        font-size: 11px;
        letter-spacing: .04em;
    }

    @media (max-width: 760px) {
        .title { font-size: 38px; }
        .nameRow { grid-template-columns: 1fr; }
        .shipGrid, .tipGrid, .relicGrid, .relicLibrary, .modeGrid, .dropGrid, .menuActions, .activeItemGrid { grid-template-columns: 1fr 1fr; }
        .statLine { grid-template-columns: 1fr 1fr; }
        .navTop { align-items: flex-start; }
    }
</style>
</head>
<body>
<div class="wrap">
    <div id="gameShell">
        <canvas id="gameCanvas" width="920" height="620"></canvas>
        <div id="overlay"></div>
        <div id="gameSignature">Created by ScaiderGod</div>
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
const STATS_KEY = 'bulletInfernoPlayerStatsV1';
const LAST_DEATH_KEY = 'bulletInfernoLastDeathV1';

const SECRET_UNLOCK_KEY = 'bulletInfernoAstraelUnlockedV1';
const SECRET_DEFEATED_KEY = 'bulletInfernoAstraelDefeatedV1';
const VOLUME_KEY = 'bulletInfernoMusicVolumeV1';
const SFX_VOLUME_KEY = 'bulletInfernoSfxVolumeV1';

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
    crit: '#fff8ec',
    shield: '#93c5fd',
    time: '#fb923c',
    magnet: '#22d3ee',
    risk: '#facc15',
    overcharge: '#f97316'
};

const CRITICAL_BOMB_CHANCE = 0.12;
const INVULN_POWER_CHANCE = 1.00;
const INVULN_POWER_SECONDS = 3.0;
const RUSH_MIN_SECONDS = 30;
const RUSH_MAX_SECONDS = 40;

const OBJECT_CAPS = {
    bombs: 2,
    hearts: 1,
    power_invuln: 1,
    coins: 22,
    shield: 1,
    time_fragment: 1,
    magnet_pulse: 1,
    risk_core: 1,
    overcharge_cell: 1,
    crit_core: 1,
    rareItems: 2,
    bossShields: 3,
    lasers: 7,
    totalProjectiles: 165
};

const CORE_DROP_LABEL = 'Core drops always active: coins, bombs and hearts.';
const MAX_ACTIVE_SPECIAL_ITEMS = 4;
const START_ACTIVE_SPECIAL_ITEMS = 2;

const SPECIAL_ITEMS = [
    {id:'shield', name:'Shield', rarity:'Rare', color:'#93c5fd', chance:'0.25%', effect:'Blocks one hit. Best for learning bosses and risky bomb grabs.', build:'Defense / Shield Bomb'},
    {id:'power_invuln', name:'Power Up', rarity:'Rare', color:'#34d399', chance:'0.45%', effect:'Invulnerable for 3 seconds. Best for aggressive bomb routes.', build:'Aggressive Safety'},
    {id:'crit_core', name:'Critical Core', rarity:'Rare', color:'#fff8ec', chance:'0.35%', effect:'Makes your next bomb critical. Best for burst damage builds.', build:'Critical Bomb'},
    {id:'magnet_pulse', name:'Magnet Pulse', rarity:'Rare', color:'#22d3ee', chance:'0.30%', effect:'Pulls nearby pickups for 5 seconds. Best for economy and safe collection.', build:'Magnet / Coin'},
    {id:'overcharge_cell', name:'Overcharge Cell', rarity:'Rare', color:'#f97316', chance:'0.22%', effect:'Short speed and bomb damage boost. Best for burst windows.', build:'Overcharge Burst'},
    {id:'time_fragment', name:'Time Fragment', rarity:'Mode', color:'#fb923c', chance:'0.35% / 0.80% in Overheat', effect:'Adds time in Overheat; gives score and utility elsewhere.', build:'Overheat / Utility'},
    {id:'risk_core', name:'Risk Core', rarity:'Legendary', color:'#facc15', chance:'0.08%', effect:'Big coin payout in dangerous spots. Best for rerolls and revive economy.', build:'Risk Economy'}
];

const SPECIAL_ITEM_BY_ID = Object.fromEntries(SPECIAL_ITEMS.map(i => [i.id, i]));
const DEFAULT_ACTIVE_ITEMS = ['shield','crit_core'];

const MODE_CONFIGS = {
    normal: {
        id:'normal', name:'Normal Run', short:'Classic', desc:'5 zones, Inferno Rush, relics and the Final Boss unlock.',
        corrupted:false, bossRush:false, survival:false, turbo:false, overheat:false, rush:true, relics:true, baseAggro:1, dropMult:1, color:'#ff7a2f'
    },
    corrupted: {
        id:'corrupted', name:'Corrupted Run', short:'Chaos', desc:'Bosses keep their identity but steal attacks from other bosses.',
        corrupted:true, bossRush:false, survival:false, turbo:false, overheat:false, rush:true, relics:true, baseAggro:1.10, dropMult:1.04, color:'#c084fc'
    },
    bossrush: {
        id:'bossrush', name:'Boss Rush', short:'Fast', desc:'Boss, reward, boss. No Rush sections. Final boss is corrupted.',
        corrupted:false, bossRush:true, survival:false, turbo:false, overheat:false, rush:false, relics:true, baseAggro:1.06, dropMult:1.02, color:'#facc15'
    },
    survival: {
        id:'survival', name:'Survival Mode', short:'Endless', desc:'Endless bosses. Difficulty grows with time. Best time matters.',
        corrupted:false, bossRush:false, survival:true, turbo:false, overheat:false, rush:false, relics:true, baseAggro:1.00, dropMult:1.00, color:'#60a5fa'
    },
    turbo: {
        id:'turbo', name:'Turbo Rush', short:'Speed', desc:'Game speed and boss aggression rise slowly over the run.',
        corrupted:false, bossRush:false, survival:false, turbo:true, overheat:false, rush:true, relics:true, baseAggro:1.02, dropMult:1.00, color:'#fb7185'
    },
    overheat: {
        id:'overheat', name:'Overheat', short:'Timer', desc:'Time drains constantly. Coins add +1 second. Greed keeps you alive.',
        corrupted:false, bossRush:false, survival:false, turbo:false, overheat:true, rush:true, relics:true, baseAggro:1.02, dropMult:1.08, color:'#f97316'
    }
};

const BOSS_SKILLS = {
    drone: [
        {type:'shield', name:'Deflector Shields', maxCharges:1, recharge:4.8, cooldown:2.6, useChance:0.16, maxObjects:1, amount:1},
        {type:'laserTrap', name:'Target Lock', maxCharges:1, recharge:5.8, cooldown:3.4, useChance:0.10, maxObjects:1, amount:1}
    ],
    widow: [
        {type:'webWall', name:'Scrap Web', maxCharges:1, recharge:5.5, cooldown:3.0, useChance:0.12, maxObjects:1, amount:1},
        {type:'shield', name:'Junk Carapace', maxCharges:1, recharge:7.0, cooldown:4.2, useChance:0.08, maxObjects:1, amount:1}
    ],
    reaper: [
        {type:'coinStorm', name:'Tax Collection', maxCharges:2, recharge:3.2, cooldown:1.4, useChance:0.24, maxObjects:18, amount:5},
        {type:'laserTrap', name:'Golden Sentence', maxCharges:1, recharge:4.4, cooldown:2.2, useChance:0.16, maxObjects:2, amount:1}
    ],
    maw: [
        {type:'bulletRing', name:'Vault Belch', maxCharges:2, recharge:3.3, cooldown:1.4, useChance:0.26, maxObjects:22, amount:10},
        {type:'shield', name:'Gold Plating', maxCharges:1, recharge:4.7, cooldown:2.1, useChance:0.16, maxObjects:1, amount:1}
    ],
    serpent: [
        {type:'spiralBloom', name:'Void Coil', maxCharges:2, recharge:3.7, cooldown:1.3, useChance:0.24, maxObjects:24, amount:12},
        {type:'laserTrap', name:'Astral Cut', maxCharges:1, recharge:4.6, cooldown:2.2, useChance:0.14, maxObjects:2, amount:1}
    ],
    halo: [
        {type:'crossLaser', name:'Eclipse Cross', maxCharges:1, recharge:4.0, cooldown:2.0, useChance:0.22, maxObjects:2, amount:1},
        {type:'shield', name:'Gravity Ring', maxCharges:2, recharge:4.5, cooldown:2.0, useChance:0.18, maxObjects:2, amount:1}
    ],
    engine: [
        {type:'fireWall', name:'Heat Vent', maxCharges:2, recharge:3.6, cooldown:1.5, useChance:0.26, maxObjects:2, amount:1},
        {type:'bulletRing', name:'Pressure Burst', maxCharges:2, recharge:3.4, cooldown:1.4, useChance:0.20, maxObjects:20, amount:9}
    ],
    furnace: [
        {type:'hammerShock', name:'Hammer Shock', maxCharges:2, recharge:3.8, cooldown:1.6, useChance:0.26, maxObjects:18, amount:8},
        {type:'fireWall', name:'Royal Furnace', maxCharges:1, recharge:4.2, cooldown:2.1, useChance:0.16, maxObjects:2, amount:1}
    ],
    sun: [
        {type:'solarRing', name:'Solar Crown', maxCharges:2, recharge:3.5, cooldown:1.6, useChance:0.26, maxObjects:26, amount:16},
        {type:'crossLaser', name:'Sun Judgment', maxCharges:1, recharge:4.8, cooldown:2.5, useChance:0.16, maxObjects:2, amount:1}
    ],
    tyrant: [
        {type:'stolenAttack', name:'Astral Command', maxCharges:2, recharge:3.5, cooldown:1.5, useChance:0.27, maxObjects:25, amount:1},
        {type:'shield', name:'Imperial Guard', maxCharges:2, recharge:4.2, cooldown:2.0, useChance:0.18, maxObjects:2, amount:1}
    ],
    astrael: [
        {type:'solarRing', name:'Divine Crown', maxCharges:3, recharge:3.0, cooldown:1.1, useChance:0.32, maxObjects:32, amount:18},
        {type:'crossLaser', name:'God Judgment', maxCharges:2, recharge:3.6, cooldown:1.6, useChance:0.24, maxObjects:2, amount:1},
        {type:'stolenAttack', name:'Inferno Memory', maxCharges:2, recharge:4.0, cooldown:1.6, useChance:0.22, maxObjects:28, amount:1}
    ]
};

const SHIPS = {
    nova: {
        id: 'nova', name: 'Nova Wing', tag: 'Balanced',
        desc: 'Standard speed, standard hitbox, no special risk.',
        speed: 1.00, hitbox: 1.00, coinValue: 1.00, startingShield: 0,
        color: '#dbeafe', accent: '#60a5fa', trail: '#f97316',
        image: 'https://res.cloudinary.com/dlxc7gaan/image/upload/v1778258914/Nave_azul-removebg-preview_l1r2al.png'
    },
    razor: {
        id: 'razor', name: 'Razor Moth', tag: 'Fast',
        desc: 'Faster movement and smaller hitbox. Great for aggressive bomb grabs.',
        speed: 1.25, hitbox: 0.88, coinValue: 1.00, startingShield: 0,
        color: '#fda4af', accent: '#fb7185', trail: '#f43f5e',
        image: 'https://res.cloudinary.com/dlxc7gaan/image/upload/v1778258914/Nave_roja-removebg-preview_g9n0g0.png'
    },
    vault: {
        id: 'vault', name: 'Vault Kite', tag: 'Greed',
        desc: 'Coins are worth 50% more, but the ship is slightly larger.',
        speed: 1.00, hitbox: 1.12, coinValue: 1.50, startingShield: 0,
        color: '#fde68a', accent: '#facc15', trail: '#f59e0b',
        image: 'https://res.cloudinary.com/dlxc7gaan/image/upload/v1778258914/Nave_Amarilla-removebg-preview_gpnhvy.png'
    },
    aegis: {
        id: 'aegis', name: 'Aegis Beetle', tag: 'Safe',
        desc: 'Starts with one shield, but movement is slower.',
        speed: 0.86, hitbox: 1.00, coinValue: 1.00, startingShield: 1,
        color: '#bbf7d0', accent: '#34d399', trail: '#22c55e',
        image: 'https://res.cloudinary.com/dlxc7gaan/image/upload/v1778258914/Nave_Verde-removebg-preview_atbcko.png'
    }
};

const SHIP_IMAGES = {};
Object.values(SHIPS).forEach(ship => {
    if (!ship.image) return;
    const img = new Image();
    img.crossOrigin = 'anonymous';
    img.src = ship.image;
    SHIP_IMAGES[ship.id] = img;
});

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
    {id:'magnet', name:'Magnetic Orbit', rarity:'Common', type:'Item synergy', tags:['Magnet','Bombs'], synergy:'Combines with Magnet Pulse and Bomb Compass.', chance:'Common pool', desc:'Passive pull is stronger. During Magnet Pulse, bombs deal +1% extra damage.', apply: () => { mods.magnet += 90; mods.magnetBombDamage += 1; }},
    {id:'blue', name:'Blue Reactor', rarity:'Common', type:'Bomb build', tags:['Blue Bomb','Critical Core'], synergy:'Best with Critical Core and Lucky Fuse.', chance:'Common pool', desc:'Blue bombs deal +1% boss HP damage. Critical blue bombs gain +1% more.', apply: () => { mods.blueDamage += 1; mods.blueCritBonus += 1; }},
    {id:'purple', name:'Violet Catalyst', rarity:'Rare', type:'Bomb build', tags:['Purple Bomb','Critical Core'], synergy:'Best with Critical Core and Godspark Fragment.', chance:'Medium', desc:'Purple bombs deal +2% boss HP damage. Forced critical purple bombs gain +1% more.', apply: () => { mods.purpleDamage += 2; mods.forcedCritBonus += 1; }},
    {id:'solar', name:'Solar Fuse', rarity:'Legendary', type:'Bomb build', tags:['Golden Bomb','Risk Core'], synergy:'Best with Risk Core and Overcharge Cell.', chance:'Low', desc:'Golden bombs deal +10% boss HP damage. If Overcharged, golden bombs gain +3% more.', apply: () => { mods.goldDamage += 10; mods.goldOverchargeBonus += 3; }},
    {id:'coin', name:'Greed Lens', rarity:'Common', type:'Coin build', tags:['Coin','Risk Core'], synergy:'Feeds rerolls and revive economy.', chance:'Common pool', desc:'Coins are worth 50% more. Risk Core grants +50 extra coins.', apply: () => { mods.coinValue += 0.5; mods.riskCoinBonus += 50; }},
    {id:'slow', name:'Chrono Drift', rarity:'Rare', type:'Control', tags:['Time Fragment','Lasers'], synergy:'Pairs with Time Fragment and Laser Reader.', chance:'Medium', desc:'Enemy bullets move 10% slower. Time Fragments slow bullets briefly after pickup.', apply: () => { mods.bulletSlow *= 0.90; mods.timeSlowPulse += 1.5; }},
    {id:'hitbox', name:'Micro Hull', rarity:'Rare', type:'Defense', tags:['Shield','Power Up'], synergy:'Safer grabs for risky items.', chance:'Medium', desc:'Your hitbox becomes 18% smaller. Shields last 0.2 seconds longer as post hit safety.', apply: () => { mods.hitbox *= 0.82; mods.hitInvulnBonus += 0.2; }},
    {id:'luck', name:'Lucky Fuse', rarity:'Rare', type:'Drop build', tags:['Bombs','Critical Core'], synergy:'Makes bomb builds more consistent.', chance:'Medium', desc:'Bomb drop chances increase by 25%. Critical Core becomes slightly more common.', apply: () => { mods.bombLuck *= 1.25; mods.critCoreLuck += 0.20; }},
    {id:'heart', name:'Heart Signal', rarity:'Common', type:'Defense', tags:['Heart','Shield'], synergy:'Turns survival drops into tempo.', chance:'Common pool', desc:'Life drops become slightly more common. Picking a heart gives a small score burst.', apply: () => { mods.heartBonus += 0.25; mods.heartScoreBonus += 120; }},
    {id:'credit', name:'Emergency Credit', rarity:'Common', type:'Revive', tags:['Coin','Revive'], synergy:'Makes coin collection matter after death.', chance:'Common pool', desc:'Revive cost is reduced by 250 coins. Risk Core reduces the next revive by 50 more.', apply: () => { mods.reviveCost = Math.max(500, mods.reviveCost - 250); mods.riskReviveDiscount += 50; }},
    {id:'shield', name:'Broken Shield', rarity:'Rare', type:'Shield build', tags:['Shield','Bombs'], synergy:'Shield pickups empower your next bomb.', chance:'Medium', desc:'Gain one shield hit right now. Each future Shield pickup adds +2% to your next bomb.', apply: () => { player.shields += 1; mods.shieldBombBonus += 2; }},
    {id:'bombValue', name:'Fuse Collector', rarity:'Common', type:'Score build', tags:['Bombs','Coin'], synergy:'Bombs become score tools, not only damage.', chance:'Common pool', desc:'Bomb pickups grant bonus score. Coins collected during Overcharge grant more score.', apply: () => { mods.bombScore += 1; mods.overchargeCoinScore += 1; }},
    {id:'crit', name:'Critical Fuse', rarity:'Rare', type:'Critical build', tags:['Critical Core','Bombs'], synergy:'Critical Core becomes a build path.', chance:'Medium', desc:'Critical bombs become more common. Critical Core can store one extra charge.', apply: () => { mods.critChance += 0.06; mods.maxCriticalCharges += 1; }},
    {id:'emerald', name:'Emerald Battery', rarity:'Rare', type:'Power Up build', tags:['Power Up','Bombs'], synergy:'Power Up becomes an offensive window.', chance:'Medium', desc:'Invulnerable power ups last 0.25 seconds longer and add +1% to your next bomb.', apply: () => { mods.invulnBonus += 0.25; mods.invulnBombBonus += 1; }},
    {id:'overclock', name:'Overclock Thrusters', rarity:'Common', type:'Mobility', tags:['Overcharge Cell','Rush'], synergy:'Overcharge becomes easier to control.', chance:'Common pool', desc:'Your ship reacts 12% faster. Overcharge Cell lasts 0.5 seconds longer.', apply: () => { mods.shipSpeed *= 1.12; mods.overchargeDurationBonus += 0.5; }},
    {id:'rushcoin', name:'Rush Bounty', rarity:'Common', type:'Rush build', tags:['Coin','Inferno Rush'], synergy:'Reroll fuel between bosses.', chance:'Common pool', desc:'Inferno Rush coins are worth 40% more. Magnet Pulse lasts longer during Rush.', apply: () => { mods.rushCoinValue += 0.4; mods.rushMagnetBonus += 1.0; }},
    {id:'laserReader', name:'Laser Reader', rarity:'Rare', type:'Control', tags:['Lasers','Time Fragment'], synergy:'More warning, more fair dodges.', chance:'Medium', desc:'Boss lasers warn slightly longer before firing. Time Fragment clears one active laser warning if possible.', apply: () => { mods.laserWarning += 0.18; mods.timeLaserClear += 1; }},
    {id:'afterimage', name:'Afterimage Hull', rarity:'Rare', type:'Defense', tags:['Power Up','Boss kill'], synergy:'Good for aggressive boss transitions.', chance:'Medium', desc:'Gain 0.4 seconds of invulnerability after each boss defeat. Power Up gives +80 score.', apply: () => { mods.afterBossInvuln += 0.4; mods.powerScoreBonus += 80; }},
    {id:'scarlet', name:'Scarlet Geometry', rarity:'Rare', type:'Rush build', tags:['Inferno Rush','Shield'], synergy:'Makes Rush safer without removing danger.', chance:'Medium', desc:'Inferno Rush obstacles move 10% slower. Shields picked in Rush give +1 second score bonus window.', apply: () => { mods.rushSlow *= 0.90; mods.rushShieldScore += 1; }},
    {id:'godspark', name:'Godspark Fragment', rarity:'Legendary', type:'Critical build', tags:['Critical Core','Purple Bomb'], synergy:'Premium critical build relic.', chance:'Low', desc:'Critical bombs deal +2% additional boss damage. Critical Core adds +1% more to the next bomb.', apply: () => { mods.critBonus += 2; mods.critCoreDamageBonus += 1; }},
    {id:'shrapnel', name:'Shrapnel Bloom', rarity:'Rare', type:'Bomb control', tags:['Bombs','Shield'], synergy:'Bomb pickups create breathing room.', chance:'Medium', desc:'Bomb pickups destroy nearby enemy bullets. If shielded, clear radius is slightly larger.', apply: () => { mods.bombClearRadius += 95; mods.shieldClearBonus += 30; }},
    {id:'phantom', name:'Phantom Wake', rarity:'Common', type:'Defense', tags:['Hit','Power Up'], synergy:'Recovery after mistakes.', chance:'Common pool', desc:'After taking damage, invulnerability lasts 0.35 seconds longer. Power Up heals 1 shield if you have no shield.', apply: () => { mods.hitInvulnBonus += 0.35; mods.powerShieldIfEmpty += 1; }},
    {id:'rushshort', name:'Warp Shortcut', rarity:'Rare', type:'Rush build', tags:['Inferno Rush','Time Fragment'], synergy:'Shorter Rush, faster boss focus.', chance:'Medium', desc:'Inferno Rush sections are 10% shorter. Time Fragment grants bonus score outside Overheat.', apply: () => { mods.rushDurationMult *= 0.90; mods.timeScoreBonus += 180; }},
    {id:'guardian', name:'Guardian Spark', rarity:'Rare', type:'Shield build', tags:['Shield','Boss'], synergy:'Pairs with shield damage relics.', chance:'Medium', desc:'Start each new boss with one extra shield. If you pick Shield while already shielded, next bomb gets +1%.', apply: () => { mods.zoneShield += 1; mods.extraShieldBombBonus += 1; }},
    {id:'heartguard', name:'Heart Capacitor', rarity:'Common', type:'Defense', tags:['Heart','Shield'], synergy:'Hearts stay useful at full life.', chance:'Common pool', desc:'If you pick a heart at max life, gain a shield instead. That shield also adds +1% to the next bomb.', apply: () => { mods.heartShield += 1; mods.heartShieldBombBonus += 1; }},
    {id:'bombmagnet', name:'Bomb Compass', rarity:'Common', type:'Item synergy', tags:['Bombs','Magnet Pulse'], synergy:'Makes risky bomb grabs more reliable.', chance:'Common pool', desc:'Bombs pull toward your ship from farther away. Bombs collected during Magnet Pulse grant +1% damage.', apply: () => { mods.bombMagnet += 120; mods.magnetBombDamage += 1; }},
    {id:'goldinsurance', name:'Golden Insurance', rarity:'Rare', type:'Revive', tags:['Coin','Risk Core'], synergy:'Greed supports continuation.', chance:'Medium', desc:'First revive costs 300 fewer coins. Risk Core gives +25 more coins.', apply: () => { mods.reviveCost = Math.max(500, mods.reviveCost - 300); mods.riskCoinBonus += 25; }},
    {id:'flashguard', name:'Flash Guard', rarity:'Rare', type:'Power Up build', tags:['Power Up','Bullet clear'], synergy:'Power Up becomes a safe route through chaos.', chance:'Medium', desc:'The invulnerability power up clears nearby bullets. During Power Up, bombs gain +1% damage.', apply: () => { mods.powerClearRadius += 120; mods.invulnBombBonus += 1; }},
    {id:'stormcoin', name:'Storm Mint', rarity:'Legendary', type:'Coin build', tags:['Coin','Overcharge Cell'], synergy:'High score greed build.', chance:'Low', desc:'Coins grant more score and may create a visual burst. Overcharge coins are worth even more score.', apply: () => { mods.coinScoreBonus += 1; mods.overchargeCoinScore += 2; }},
    {id:'coolant', name:'Coolant Heart', rarity:'Common', type:'Overheat', tags:['Heart','Time Fragment'], synergy:'Overheat survival build.', chance:'Common pool', desc:'In Overheat, hearts add +2 seconds to heat. Time Fragment also grants +1 shield once per pickup.', apply: () => { mods.heatHeartBonus += 2; mods.timeFragmentShield += 1; }},
    {id:'tactician', name:'Tactician Glass', rarity:'Rare', type:'Control', tags:['Boss skills','Critical Core'], synergy:'More controlled chaos.', chance:'Medium', desc:'Boss skill cooldowns are 8% longer. Critical Core also delays the next boss skill slightly.', apply: () => { mods.bossSkillSlow *= 1.08; mods.critCoreSkillDelay += 0.25; }},
    {id:'paniccoin', name:'Panic Mint', rarity:'Common', type:'Coin build', tags:['Coin','Low life'], synergy:'Risky comeback economy.', chance:'Common pool', desc:'At 1 life, coins are worth 25% more. Critical Core at 1 life grants +1 shield score bonus.', apply: () => { mods.lowLifeCoinBonus += 0.25; mods.lowLifeCritScore += 120; }},
    {id:'rusharmor', name:'Warp Armor', rarity:'Rare', type:'Rush build', tags:['Shield','Inferno Rush'], synergy:'Rush defense that can feed bomb builds.', chance:'Medium', desc:'First hit in each Inferno Rush is blocked by a shield. Entering Rush gives next bomb +1%.', apply: () => { mods.rushShield += 1; mods.rushBombBonus += 1; }},
    {id:'laststand', name:'Last Stand Fuse', rarity:'Legendary', type:'Critical build', tags:['Critical Core','Low life'], synergy:'Dangerous but powerful.', chance:'Low', desc:'At 1 life, critical bombs deal +3% more damage. Critical Core at 1 life adds +1% more.', apply: () => { mods.lastStandCrit += 3; mods.lowLifeCritDamage += 1; }},
    {id:'cleanorbit', name:'Clean Orbit', rarity:'Rare', type:'Control', tags:['Bullet cap','Bombs'], synergy:'Keeps chaos readable.', chance:'Medium', desc:'Fewer enemy bullets stay on screen. Bomb clears award extra score.', apply: () => { mods.projectileCapBonus += 18; mods.clearScoreBonus += 3; }},
    {id:'overclockedbank', name:'Overclocked Bank', rarity:'Rare', type:'Revive', tags:['Coin','Boss kill'], synergy:'Rewards long runs and reroll discipline.', chance:'Medium', desc:'Revive cost is reduced after each boss defeated. Risk Core doubles that reduction once.', apply: () => { mods.scalingReviveDiscount += 80; mods.riskReviveDiscount += 40; }},
    {id:'magnetbank', name:'Magnet Bank', rarity:'Rare', type:'Item synergy', tags:['Magnet Pulse','Coin'], synergy:'Magnet Pulse becomes a money and reroll tool.', chance:'Medium', desc:'During Magnet Pulse, coins are worth 25% more and pull harder.', apply: () => { mods.magnetPulseCoinBonus += 0.25; mods.magnet += 45; }},
    {id:'volatilecore', name:'Volatile Risk Core', rarity:'Legendary', type:'Risk build', tags:['Risk Core','Bombs'], synergy:'Risk Core becomes a high damage gamble.', chance:'Low', desc:'Risk Core gives +6% to your next bomb but triggers a small bullet burst.', apply: () => { mods.riskCoreBombBonus += 6; mods.riskCoreBurst += 1; }},
    {id:'chargedheart', name:'Charged Heart', rarity:'Rare', type:'Defense', tags:['Heart','Critical Core'], synergy:'Healing supports offense.', chance:'Medium', desc:'Picking a heart also gives +1 Critical Core charge if you are not at full life.', apply: () => { mods.heartCritCharge += 1; }},
    {id:'overchargefuse', name:'Overcharge Fuse', rarity:'Legendary', type:'Overcharge build', tags:['Overcharge Cell','Bombs'], synergy:'Short burst damage build.', chance:'Low', desc:'Overcharge Cell lasts +1 second and bombs during Overcharge deal +2% more damage.', apply: () => { mods.overchargeDurationBonus += 1; mods.overchargeBonusFlat += 2; }},
    {id:'timebroker', name:'Time Broker', rarity:'Rare', type:'Overheat', tags:['Time Fragment','Coin'], synergy:'Overheat timer converts into economy.', chance:'Medium', desc:'Time Fragment gives +60 coins in Overheat and +300 score in other modes.', apply: () => { mods.timeFragmentCoins += 60; mods.timeScoreBonus += 300; }}
];

let state = 'menu';
let selectedShipId = 'nova';
let selectedModeId = 'normal';
let selectedLoadoutItems = DEFAULT_ACTIVE_ITEMS.slice();
let activeSpecialItems = DEFAULT_ACTIVE_ITEMS.slice();
let rewardNextFn = null;
let playerName = 'Pilot';
let seed = 1;
let rand = Math.random;
let last = performance.now();
let elapsed = 0;
let runId = 0;
let paused = false;
let particles = [];
let bullets = [];
let lasers = [];
let stars = [];
let rush = null;
let screenFlash = 0;
let screenShake = 0;
let relicChoices = [];
let usedRelics = [];
let mouse = {x: W/2, y: H - 84, active: false};
let player, boss, mods, runStats;
let musicVolume = clamp(Number(localStorage.getItem(VOLUME_KEY) || '0.30'), 0, 1);
let sfxVolume = clamp(Number(localStorage.getItem(SFX_VOLUME_KEY) || '0.85'), 0, 1);
let currentMusic = null;
let deathTimer = 0;
let resumeCountdown = 0;
let currentMusicKey = '';
let reviveState = 'playing';
let currentMode = 'normal';
let modeConfig = MODE_CONFIGS.normal;
let currentAttackName = 'Unknown pattern';
let selectedPracticeBoss = null;
let selectedPracticeItems = DEFAULT_ACTIVE_ITEMS.slice();
let selectedPracticeRelics = [];


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
    updatePersistentStats(result);
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

function relicLibraryHtml() {
    return RELICS.map(r => `
        <div class="libraryRelic">
            <div class="itemTitle">${r.name}</div>
            <div class="itemText">${r.desc}</div>
            <span class="rarity">${r.rarity}</span>
        </div>
    `).join('');
}

function isSecretUnlocked() {
    return localStorage.getItem(SECRET_UNLOCK_KEY) === '1';
}
function unlockSecretBoss() {
    localStorage.setItem(SECRET_UNLOCK_KEY, '1');
}

function loadStats() {
    const defaults = {
        runsPlayed:0, runsWon:0, runsLost:0, totalTime:0, bestTime:0,
        totalCoins:0, bombsUsed:0, hitsReceived:0, bossesDefeated:0,
        killedByBoss:{}, deathTypes:{}, shipsUsed:{}, relicsUsed:{}, modesPlayed:{}, deathsByStage:{}, defeatedBossMap:{}
    };
    try { return {...defaults, ...(JSON.parse(localStorage.getItem(STATS_KEY) || '{}'))}; }
    catch { return defaults; }
}
function saveStats(stats) { localStorage.setItem(STATS_KEY, JSON.stringify(stats)); }
function incMap(map, key, amt=1) { if (!key) key = 'Unknown'; map[key] = (map[key] || 0) + amt; }
function topMapLabel(map) {
    const entries = Object.entries(map || {}).sort((a,b)=>b[1]-a[1]);
    return entries.length ? `${entries[0][0]} (${entries[0][1]})` : 'None yet';
}
function playerStatsHtml() {
    const st = loadStats();
    const lost = st.runsLost || Math.max(0, (st.runsPlayed || 0) - (st.runsWon || 0));
    const stage = topMapLabel(st.deathsByStage);
    const relic = topMapLabel(st.relicsUsed);
    return `
        <div class="statLine" style="margin:10px 0 4px;">
            <div class="statBox"><div class="statValue">${st.runsPlayed}</div><div class="statLabel">Runs played</div></div>
            <div class="statBox"><div class="statValue">${st.runsWon}</div><div class="statLabel">Runs won</div></div>
            <div class="statBox"><div class="statValue">${lost}</div><div class="statLabel">Runs lost</div></div>
            <div class="statBox"><div class="statValue">${formatTime(st.bestTime)}</div><div class="statLabel">Best time</div></div>
            <div class="statBox"><div class="statValue">${st.totalCoins}</div><div class="statLabel">Total coins</div></div>
            <div class="statBox"><div class="statValue">${st.bombsUsed}</div><div class="statLabel">Bombs used</div></div>
            <div class="statBox"><div class="statValue">${st.hitsReceived}</div><div class="statLabel">Hits received</div></div>
            <div class="statBox"><div class="statValue">${st.bossesDefeated}</div><div class="statLabel">Bosses defeated</div></div>
        </div>
        <div class="sectionCard">
            <div class="itemText"><b>Most lethal boss:</b> ${escapeHtml(topMapLabel(st.killedByBoss))}</div>
            <div class="itemText"><b>Common death:</b> ${escapeHtml(topMapLabel(st.deathTypes))}</div>
            <div class="itemText"><b>Favorite ship:</b> ${escapeHtml(topMapLabel(st.shipsUsed))}</div>
            <div class="itemText"><b>Most played mode:</b> ${escapeHtml(topMapLabel(st.modesPlayed))}</div>
            <div class="itemText"><b>Stage where you die most:</b> ${escapeHtml(stage)}</div>
            <div class="itemText"><b>Most used relic:</b> ${escapeHtml(relic)}</div>
            <div class="itemText"><b>Total time played:</b> ${formatTime(st.totalTime || 0)}</div>
        </div>
    `;
}
function updatePersistentStats(result) {
    const st = loadStats();
    st.runsPlayed += 1;
    if (result.victory) st.runsWon += 1; else st.runsLost += 1;
    st.totalTime += Math.round(result.time || 0);
    st.bestTime = Math.max(st.bestTime || 0, Math.round(result.time || 0));
    st.totalCoins += result.coins || 0;
    st.bombsUsed += result.bombsUsed || 0;
    st.hitsReceived += result.hits || 0;
    st.bossesDefeated += result.bosses || 0;
    incMap(st.shipsUsed, result.ship || 'Unknown');
    incMap(st.modesPlayed, result.mode || 'normal');
    if (result.deathBoss) incMap(st.killedByBoss, result.deathBoss);
    if (result.deathCause) incMap(st.deathTypes, result.deathCause);
    if (result.stage) incMap(st.deathsByStage, result.stage);
    (result.relics || []).forEach(r => incMap(st.relicsUsed, r));
    if (!st.defeatedBossMap) st.defeatedBossMap = {};
    (result.defeatedBosses || []).forEach(n => { st.defeatedBossMap[canonicalBossName(n)] = true; });
    if (result.trueVictory) st.defeatedBossMap[SECRET_BOSS.name] = true;
    saveStats(st);
}
function modeLabel() { return (modeConfig && modeConfig.name) || 'Normal Run'; }
function modeIntensity() {
    if (!runStats) return 1;
    let mult = modeConfig.baseAggro || 1;
    if (modeConfig.turbo) mult *= clamp(1 + runStats.activeTime / 210, 1, 1.85);
    if (modeConfig.survival) mult *= clamp(1 + runStats.activeTime / 260 + runStats.bossesKilled * 0.035, 1, 1.95);
    if (modeConfig.overheat) mult *= clamp(1 + Math.max(0, 24 - (runStats.heat || 24)) / 80, 1, 1.25);
    return mult;
}
function getObjectCount(kind) {
    if (kind === 'bombs') return bullets.filter(o => o.type === 'bomb_blue' || o.type === 'bomb_purple' || o.type === 'bomb_gold').length;
    if (kind === 'coins') return bullets.filter(o => o.type === 'coin').length;
    if (kind === 'rareItems') return bullets.filter(o => ['shield','power_invuln','time_fragment','magnet_pulse','risk_core','overcharge_cell','crit_core'].includes(o.type)).length;
    return bullets.filter(o => o.type === kind).length;
}
function canSpawnKind(kind) {
    const projectileCap = Math.max(80, OBJECT_CAPS.totalProjectiles - (mods?.projectileCapBonus || 0));
    if (bullets.length >= projectileCap && kind === 'bullet') return false;
    if (kind === 'bomb_blue' || kind === 'bomb_purple' || kind === 'bomb_gold') return getObjectCount('bombs') < OBJECT_CAPS.bombs;
    if (kind === 'heart') return getObjectCount('heart') < OBJECT_CAPS.hearts;
    if (kind === 'power_invuln') return getObjectCount('rareItems') < OBJECT_CAPS.rareItems && getObjectCount('power_invuln') < OBJECT_CAPS.power_invuln;
    if (['shield','time_fragment','magnet_pulse','risk_core','overcharge_cell','crit_core'].includes(kind)) {
        return getObjectCount('rareItems') < OBJECT_CAPS.rareItems && getObjectCount(kind) < (OBJECT_CAPS[kind] || 1);
    }
    if (kind === 'coin') return getObjectCount('coins') < OBJECT_CAPS.coins;
    return bullets.length < projectileCap;
}
function createBossSkills(archetype) {
    const configs = (BOSS_SKILLS[archetype] || []).map(c => ({...c}));
    if (modeConfig.corrupted && archetype !== 'astrael') {
        configs.push({type:'stolenAttack', name:'Corrupted Memory', maxCharges:1, recharge:4.2, cooldown:2.0, useChance:0.18, maxObjects:24, amount:1});
    }
    if (modeConfig.bossRush && runStats && runStats.zone >= 5) {
        configs.push({type:'shield', name:'Final Guard', maxCharges:1, recharge:4.0, cooldown:1.8, useChance:0.22, maxObjects:2, amount:1});
    }
    return configs.map(c => ({...c, charges:c.maxCharges, rechargeTimer:0, cooldownTimer:0}));
}
function relicTypeText(r) {
    if (r && r.type) return r.type;
    const id = r.id || '';
    if (['blue','purple','solar','luck','crit','godspark','laststand','bombValue','shrapnel','bombmagnet'].includes(id)) return 'Bomb build';
    if (['magnet','coin','rushcoin','stormcoin','paniccoin','magnetbank'].includes(id)) return 'Coin build';
    if (['slow','laserReader','scarlet','tactician','cleanorbit'].includes(id)) return 'Control';
    if (['hitbox','shield','heart','emerald','afterimage','phantom','guardian','heartguard','flashguard','rusharmor'].includes(id)) return 'Defense';
    if (['credit','goldinsurance','overclockedbank'].includes(id)) return 'Revive';
    if (['overclock','rushshort','coolant','timebroker'].includes(id)) return 'Utility';
    return 'General';
}
function relicChanceText(r) {
    if (!r) return 'Pool roll';
    if (r.chance) return r.chance;
    if (r.rarity === 'Legendary') return 'Low';
    if (r.rarity === 'Rare') return 'Medium';
    return 'Common pool';
}
function relicTagsHtml(r) {
    const tags = (r.tags || []).slice(0, 3);
    if (!tags.length) return '';
    return `<div class="metaLine">${tags.map(t => `<span class="pill">${escapeHtml(t)}</span>`).join('')}</div>`;
}
function relicLibraryHtml(filter='All', query='') {
    const q = String(query || '').trim().toLowerCase();
    const rows = RELICS.filter(r => {
        const hay = `${r.name} ${r.desc} ${r.synergy || ''} ${relicTypeText(r)} ${(r.tags || []).join(' ')}`.toLowerCase();
        return (filter === 'All' || r.rarity === filter) && (!q || hay.includes(q));
    });
    if (!rows.length) return `<div class="smallNote" style="padding:12px;">No relics match this filter.</div>`;
    return rows.map(r => `
        <div class="libraryRelic">
            <div class="itemTitle">${r.name}</div>
            <div class="itemText">${r.desc}</div>
            ${r.synergy ? `<div class="smallNote"><b>Combo:</b> ${escapeHtml(r.synergy)}</div>` : ''}
            ${relicTagsHtml(r)}
            <div class="metaLine">
                <span class="rarity">${r.rarity}</span>
                <span class="rarity">${relicTypeText(r)}</span>
                <span class="rarity">Chance: ${relicChanceText(r)}</span>
            </div>
        </div>
    `).join('');
}
function itemDropsHtml() {
    const items = [
        ['Coin','Common','Adds coins and score. Purpose: fuels rerolls and revives. Combos with Greed Lens, Storm Mint and Magnet Bank.','8.5% base, capped'],
        ['Blue Bomb','Rare','Deals 5% boss HP damage. Purpose: steady boss damage. Combos with Blue Reactor, Lucky Fuse and Critical Core.','2% base chance'],
        ['Purple Bomb','Rare','Deals 10% boss HP damage. Purpose: high value damage windows. Combos with Violet Catalyst and Godspark Fragment.','1% base chance'],
        ['Golden Bomb','Legendary','Deals 50% boss HP damage. Purpose: rare comeback or boss finisher. Combos with Solar Fuse, Risk Core and Overcharge Cell.','0.01% base chance'],
        ['Heart','Rare','Restores 1 life. Purpose: recovery. Combos with Heart Capacitor, Coolant Heart and Charged Heart.','0.5% base chance'],
        ['Shield','Active Special','Grants 1 shield hit. Purpose: safe risky grabs. Only drops if selected or unlocked.','0.25% active chance'],
        ['Power Up','Active Special','Invulnerable for 3 seconds. Purpose: aggressive bomb collection window. Only drops if selected or unlocked.','0.45% active chance'],
        ['Critical Core','Active Special','Your next bomb is guaranteed critical. Purpose: create burst damage. Only drops if selected or unlocked.','0.35% active chance'],
        ['Time Fragment','Active Special','In Overheat, adds +5 seconds. Purpose: timer control. Only drops if selected or unlocked.','0.35% / 0.80% in Overheat'],
        ['Magnet Pulse','Active Special','Pulls nearby coins, bombs and hearts for 5 seconds. Purpose: safe collection route. Only drops if selected or unlocked.','0.30% active chance'],
        ['Risk Core','Active Legendary','Big coin payout, but appears in dangerous patterns. Purpose: reroll/revive economy. Only drops if selected or unlocked.','0.08% active chance'],
        ['Overcharge Cell','Active Special','For 6 seconds: faster ship and +25% bomb damage. Purpose: burst window. Only drops if selected or unlocked.','0.22% active chance']
    ];
    return items.map(([name, rarity, effect, chance]) => `
        <div class="dropCard">
            <div class="itemTitle">${name}</div>
            <div class="itemText">${effect}</div>
            <div class="metaLine"><span class="rarity">${rarity}</span><span class="rarity">${chance}</span></div>
        </div>
    `).join('');
}

function sanitizeActiveItems(items, cfg=modeConfig) {
    const cleaned = [];
    for (const id of (items || [])) {
        if (!SPECIAL_ITEM_BY_ID[id]) continue;
        if (!cleaned.includes(id)) cleaned.push(id);
    }
    for (const id of DEFAULT_ACTIVE_ITEMS) {
        if (cleaned.length >= START_ACTIVE_SPECIAL_ITEMS) break;
        if (!cleaned.includes(id)) cleaned.push(id);
    }
    return cleaned.slice(0, MAX_ACTIVE_SPECIAL_ITEMS);
}
function activeItemName(id) {
    return SPECIAL_ITEM_BY_ID[id]?.name || id;
}
function loadoutHtml(items=selectedLoadoutItems) {
    const chosen = [];
    for (const id of (items || [])) if (SPECIAL_ITEM_BY_ID[id] && !chosen.includes(id)) chosen.push(id);
    return chosen.slice(0, START_ACTIVE_SPECIAL_ITEMS).map(id => `<span class="tinyTag" style="border-color:${hexToRgba(SPECIAL_ITEM_BY_ID[id]?.color || '#fff8ec', .32)};">${escapeHtml(activeItemName(id))}</span>`).join('') || '<span class="tinyTag">Choose 2 special items</span>';
}
function itemCardsHtml(selectedItems=selectedLoadoutItems, limit=START_ACTIVE_SPECIAL_ITEMS) {
    const selected = [];
    for (const id of (selectedItems || [])) if (SPECIAL_ITEM_BY_ID[id] && !selected.includes(id)) selected.push(id);
    return SPECIAL_ITEMS.map(item => {
        const isSelected = selected.includes(item.id);
        return `
            <div class="activeItemCard ${isSelected ? 'selected' : ''}" data-item="${item.id}" style="border-color:${isSelected ? hexToRgba(item.color, .72) : hexToRgba(item.color, .20)};">
                <div class="itemTitle" style="color:${item.color};">${item.name}</div>
                <div class="itemText"><b>${item.build}</b><br>${item.effect}</div>
                <div class="metaLine"><span class="rarity">${item.rarity}</span><span class="rarity">${item.chance}</span></div>
            </div>
        `;
    }).join('');
}
function activeItemLegendHtml() {
    return SPECIAL_ITEMS.map(item => `
        <div class="dropCard">
            <div class="itemTitle" style="color:${item.color};">${item.name}</div>
            <div class="itemText">${item.effect}</div>
            <div class="metaLine"><span class="rarity">${item.rarity}</span><span class="rarity">${item.chance}</span></div>
        </div>
    `).join('');
}
function modeCardsHtml() {
    const modes = Object.values(MODE_CONFIGS).map(m => `
        <button class="modeCard" data-mode="${m.id}" style="border-color:${hexToRgba(m.color,0.28)};">
            <div class="modeTitle">${m.name}</div>
            <div class="modeDesc"><b>${m.short}</b><br>${m.desc}</div>
            <div class="modeMeta"><span class="pill">${m.rush ? 'Inferno Rush' : 'Direct'}</span><span class="pill">${m.relics ? 'Relics' : 'No relics'}</span></div>
        </button>
    `).join('');
    const unlocked = isSecretUnlocked();
    const finalCard = `
        <button class="modeCard ${unlocked ? '' : 'locked'}" data-mode="godtrial" ${unlocked ? '' : 'disabled'} style="border-color:${unlocked ? 'rgba(250,204,21,.55)' : 'rgba(255,255,255,.10)'};">
            <div class="modeTitle">Final Boss</div>
            <div class="modeDesc"><b>${unlocked ? 'God Trial' : 'Locked'}</b><br>${unlocked ? 'Fight Astrael, God of Inferno.' : 'Unlock requirement: complete the game first.'}</div>
            <div class="modeMeta"><span class="pill">Astrael</span><span class="pill">Standalone</span></div>
        </button>
    `;
    return modes + finalCard;
}
function shipCardsHtml() {
    return Object.values(SHIPS).map(s => `
        <div class="shipCard ${selectedShipId === s.id ? 'selected' : ''}" data-ship="${s.id}" style="--ship-glow:${hexToRgba(s.accent, 0.25)}; border-color:${selectedShipId === s.id ? hexToRgba(s.accent, 0.72) : 'rgba(255,255,255,0.10)'};">
            <div class="shipTop">
                <div class="shipSwatch" style="background:linear-gradient(135deg, ${s.color}, ${s.accent});"></div>
                <div class="itemTitle" style="margin-bottom:0;">${s.name}</div>
            </div>
            <div class="shipPreviewWrap">
                <img class="shipPreview" src="${s.image}" alt="${s.name}" loading="lazy" />
            </div>
            <div class="itemText"><b>${s.tag}</b><br>${s.desc}</div>
            <div class="shipMeta">
                <span class="pill">Life: 3</span>
                <span class="pill">Speed: ${Math.round(s.speed*100)}%</span>
                <span class="pill">Hitbox: ${Math.round(s.hitbox*100)}%</span>
                <span class="pill">Coins: ${Math.round(s.coinValue*100)}%</span>
            </div>
            <div class="itemText" style="margin-top:8px;"><b>Recommended:</b> ${s.id==='nova'?'Balanced runs':s.id==='razor'?'Aggressive bomb grabs':s.id==='vault'?'Greedy coin routes':'Safer boss learning'}</div>
        </div>
    `).join('');
}
function showOverlay(html) {
    overlay.classList.remove('hidden');
    overlay.innerHTML = html;
}
function hideOverlay() {
    overlay.classList.add('hidden');
    overlay.innerHTML = '';
}
function bindBack(btnId='backBtn') {
    const b = document.getElementById(btnId);
    if (b) b.addEventListener('click', () => { playSfx('click'); renderMenu(); });
}
function ensureMenuMusic() {
    if (currentMusicKey !== 'menu') playMusic('menu');
    else if (currentMusic) {
        currentMusic.loop = true;
        currentMusic.volume = musicVolume;
        currentMusic.play().catch(() => {});
    }
}
function syncNameFromInput() {
    const input = document.getElementById('nameInput');
    if (input) playerName = (input.value || 'Pilot').trim().slice(0, 18) || 'Pilot';
}
function renderMenu() {
    state = 'menu';
    paused = false;
    ensureMenuMusic();
    showOverlay(`
        <div class="card">
            <h1 class="title">Bullet Inferno</h1>
            <div class="subtitle">Arcade roguelike bullet hell. Dodge, collect bombs, break impossible bosses.</div>
            <div class="nameRow" style="grid-template-columns:1fr; max-width:420px;">
                <input id="nameInput" maxlength="18" placeholder="Pilot name" value="${escapeHtml(playerName)}" />
            </div>
            <div class="menuActions">
                <button class="menuActionBtn primaryAction" id="startMenuBtn">Start Run</button>
                <button class="menuActionBtn" id="practiceMenuBtn">Practice</button>
                <button class="menuActionBtn" id="libraryMenuBtn">Relic Library</button>
                <button class="menuActionBtn" id="statsMenuBtn">Stats</button>
                <button class="menuActionBtn" id="settingsMenuBtn">Settings</button>
            </div>
            <div class="sectionCard" style="text-align:center; max-width:700px; margin-left:auto; margin-right:auto;">
                <div class="itemTitle">Current pilot</div>
                <div class="itemText">Choose a mode, then choose a ship. Final Boss unlocks after clearing all 5 zones once.</div>
            </div>
            <div class="footerNote">Created by ScaiderGod</div>
        </div>
    `);
    const input = document.getElementById('nameInput');
    if (input) input.addEventListener('input', () => { playerName = input.value.slice(0,18) || 'Pilot'; });
    document.getElementById('startMenuBtn').addEventListener('click', () => { syncNameFromInput(); playSfx('click'); renderStartRun(); });
    document.getElementById('practiceMenuBtn').addEventListener('click', () => { syncNameFromInput(); playSfx('click'); renderPracticeBossSelect(); });
    document.getElementById('libraryMenuBtn').addEventListener('click', () => { syncNameFromInput(); playSfx('click'); renderRelicLibrary(); });
    document.getElementById('statsMenuBtn').addEventListener('click', () => { syncNameFromInput(); playSfx('click'); renderStats('player'); });
    document.getElementById('settingsMenuBtn').addEventListener('click', () => { syncNameFromInput(); playSfx('click'); renderSettings(); });
}
function renderStartRun() {
    state = 'menu';
    ensureMenuMusic();
    showOverlay(`
        <div class="card">
            <div class="navTop">
                <div><div class="navTitle">Start Run</div><div class="navSub">Select a mode first. Ship selection comes next.</div></div>
                <button class="secondary" id="backBtn">Back</button>
            </div>
            <div class="modeGrid">${modeCardsHtml()}</div>
            <details class="menuDetails">
                <summary>Item Drops</summary>
                <div class="smallNote">${CORE_DROP_LABEL} Special items must be selected in Active Items or unlocked after bosses.</div><div class="dropGrid">${itemDropsHtml()}</div>
            </details>
        </div>
    `);
    bindBack();
    document.querySelectorAll('.modeCard').forEach(btn => {
        btn.addEventListener('click', () => {
            const mode = btn.getAttribute('data-mode');
            if (mode === 'godtrial' && !isSecretUnlocked()) return;
            selectedModeId = mode || 'normal';
            playSfx('select');
            renderShipSelect();
        });
    });
}

function canonicalBossName(name) {
    return String(name || '').replace(/^Corrupted\s+/,'').trim();
}
function allPracticeBosses() {
    const list = [];
    BOSS_POOLS.forEach((pool, zi) => {
        pool.forEach(b => list.push({...b, zone: zi + 1, secret:false}));
    });
    list.push({...SECRET_BOSS, zone: 6, secret:true});
    return list;
}
function defeatedBossMap() {
    const map = {};
    const st = loadStats();
    Object.entries(st.defeatedBossMap || {}).forEach(([k,v]) => { if (v) map[canonicalBossName(k)] = true; });
    const board = loadBoard();
    board.forEach(r => {
        (r.defeatedBosses || []).forEach(n => map[canonicalBossName(n)] = true);
        if (r.trueVictory) map[SECRET_BOSS.name] = true;
    });
    const maxLegacy = Math.max(0, ...board.map(r => Number(r.bosses || 0)));
    // Legacy save files did not store exact boss names. If a player already reached a stage,
    // unlock the bosses from completed zones so Practice does not feel reset after updating.
    for (let z = 1; z <= Math.min(5, maxLegacy); z++) {
        (BOSS_POOLS[z-1] || []).forEach(b => map[canonicalBossName(b.name)] = true);
    }
    if (localStorage.getItem(SECRET_DEFEATED_KEY) === '1') map[SECRET_BOSS.name] = true;
    return map;
}
function isPracticeBossUnlocked(b) {
    const map = defeatedBossMap();
    if (b.secret) return !!map[SECRET_BOSS.name];
    return !!map[canonicalBossName(b.name)];
}
function practiceBossCardsHtml() {
    return allPracticeBosses().map((b, idx) => {
        const unlocked = isPracticeBossUnlocked(b);
        const label = b.secret ? 'Secret Boss' : `Zone ${b.zone}`;
        const desc = unlocked ? `${label} · ${b.subtitle || 'Practice target'}` : (b.secret ? 'Locked · Defeat Astrael first' : 'Locked · Defeat this boss in any run first');
        return `
            <button class="modeCard ${unlocked ? '' : 'locked'}" data-practice-boss="${idx}" ${unlocked ? '' : 'disabled'} style="border-color:${unlocked ? hexToRgba(b.color || '#fff8ec', .42) : 'rgba(255,255,255,.10)'};">
                <div class="modeTitle" style="color:${unlocked ? (b.color || '#fff8ec') : 'rgba(247,247,251,.55)'};">${b.name}</div>
                <div class="modeDesc"><b>${unlocked ? label : 'Locked'}</b><br>${escapeHtml(desc)}</div>
            </button>
        `;
    }).join('');
}
function renderPracticeBossSelect() {
    state = 'menu';
    ensureMenuMusic();
    showOverlay(`
        <div class="card">
            <div class="navTop">
                <div><div class="navTitle">Practice</div><div class="navSub">Choose one boss you have already defeated. Practice does not save to leaderboard.</div></div>
                <button class="secondary" id="backBtn">Back</button>
            </div>
            <div class="modeGrid">${practiceBossCardsHtml()}</div>
            <div class="smallNote">Secret Boss practice unlocks only after a God Clear. Regular bosses unlock after you defeat them in any run.</div>
        </div>
    `);
    bindBack();
    document.querySelectorAll('[data-practice-boss]').forEach(btn => {
        btn.addEventListener('click', () => {
            const idx = Number(btn.getAttribute('data-practice-boss'));
            const bossPick = allPracticeBosses()[idx];
            if (!bossPick || !isPracticeBossUnlocked(bossPick)) return;
            selectedPracticeBoss = bossPick;
            selectedPracticeItems = sanitizeActiveItems(selectedPracticeItems, MODE_CONFIGS.normal).slice(0, MAX_ACTIVE_SPECIAL_ITEMS);
            selectedPracticeRelics = selectedPracticeRelics.filter(id => RELICS.some(r => r.id === id)).slice(0, 4);
            playSfx('select');
            renderPracticeBuildSelect();
        });
    });
}
function practiceRelicCardsHtml() {
    return RELICS.map(r => {
        const selected = selectedPracticeRelics.includes(r.id);
        return `
            <div class="libraryRelic practicePick ${selected ? 'selected' : ''}" data-practice-relic="${r.id}">
                <div class="itemTitle">${r.name}</div>
                <div class="itemText">${r.desc}</div>
                <div class="metaLine"><span class="rarity">${r.rarity}</span><span class="rarity">${relicTypeText(r)}</span></div>
            </div>
        `;
    }).join('');
}
function renderPracticeBuildSelect() {
    if (!selectedPracticeBoss) { renderPracticeBossSelect(); return; }
    selectedPracticeItems = sanitizeActiveItems(selectedPracticeItems, MODE_CONFIGS.normal).slice(0, MAX_ACTIVE_SPECIAL_ITEMS);
    showOverlay(`
        <div class="card">
            <div class="navTop">
                <div><div class="navTitle">Practice Setup</div><div class="navSub">Boss selected: ${escapeHtml(selectedPracticeBoss.name)}. Choose active items and optional relics.</div></div>
                <button class="secondary" id="practiceBackBtn">Back to Bosses</button>
            </div>
            <div class="sectionCard" style="text-align:left;">
                <div class="itemTitle">Active Items</div>
                <div class="itemText">Choose up to ${MAX_ACTIVE_SPECIAL_ITEMS}. Core drops always stay active: coins, bombs and hearts.</div>
                <div class="loadoutBar">${loadoutHtml(selectedPracticeItems)}</div>
            </div>
            <div class="activeItemGrid">${itemCardsHtml(selectedPracticeItems, MAX_ACTIVE_SPECIAL_ITEMS)}</div>
            <details class="menuDetails" open>
                <summary>Practice Relics (${selectedPracticeRelics.length}/4)</summary>
                <div class="smallNote">Pick up to 4 relics to test builds. These relics are only for this practice fight.</div>
                <div class="compactList relicLibrary" style="grid-template-columns:repeat(2,1fr); max-height:300px;">${practiceRelicCardsHtml()}</div>
            </details>
            <div class="rowButtons">
                <button class="primary" id="startPracticeBtn">Start Practice</button>
                <button class="secondary" id="clearPracticeBuildBtn">Clear build</button>
            </div>
        </div>
    `);
    document.getElementById('practiceBackBtn').addEventListener('click', () => { playSfx('click'); renderPracticeBossSelect(); });
    document.querySelectorAll('.activeItemCard').forEach(card => {
        card.addEventListener('click', () => {
            const id = card.getAttribute('data-item');
            let current = [];
            for (const x of (selectedPracticeItems || [])) if (SPECIAL_ITEM_BY_ID[x] && !current.includes(x)) current.push(x);
            if (current.includes(id)) current = current.filter(x => x !== id);
            else {
                if (current.length >= MAX_ACTIVE_SPECIAL_ITEMS) current.shift();
                current.push(id);
            }
            selectedPracticeItems = current;
            playSfx('select');
            renderPracticeBuildSelect();
        });
    });
    document.querySelectorAll('[data-practice-relic]').forEach(card => {
        card.addEventListener('click', () => {
            const id = card.getAttribute('data-practice-relic');
            let current = selectedPracticeRelics.slice();
            if (current.includes(id)) current = current.filter(x => x !== id);
            else {
                if (current.length >= 4) current.shift();
                current.push(id);
            }
            selectedPracticeRelics = current;
            playSfx('select');
            renderPracticeBuildSelect();
        });
    });
    document.getElementById('clearPracticeBuildBtn').addEventListener('click', () => {
        selectedPracticeItems = [];
        selectedPracticeRelics = [];
        playSfx('click');
        renderPracticeBuildSelect();
    });
    document.getElementById('startPracticeBtn').addEventListener('click', () => { playSfx('start'); startPractice(); });
}
function renderShipSelect() {
    state = 'menu';
    ensureMenuMusic();
    const isGod = selectedModeId === 'godtrial';
    const modeName = isGod ? 'Final Boss: Astrael' : ((MODE_CONFIGS[selectedModeId] || MODE_CONFIGS.normal).name);
    showOverlay(`
        <div class="card">
            <div class="navTop">
                <div><div class="navTitle">Select Ship</div><div class="navSub">Mode selected: ${escapeHtml(modeName)}. Pick a ship that fits your run style.</div></div>
                <button class="secondary" id="modeBackBtn">Back to Modes</button>
            </div>
            <div class="shipGrid">${shipCardsHtml()}</div>
            <div class="rowButtons">
                <button class="primary" id="launchBtn">Continue</button>
            </div>
        </div>
    `);
    document.getElementById('modeBackBtn').addEventListener('click', () => { playSfx('click'); renderStartRun(); });
    document.querySelectorAll('.shipCard').forEach(card => {
        card.addEventListener('click', () => {
            selectedShipId = card.getAttribute('data-ship');
            playSfx('select');
            renderShipSelect();
        });
    });
    document.getElementById('launchBtn').addEventListener('click', () => {
        playSfx('click');
        renderItemLoadout();
    });
}
function renderItemLoadout() {
    state = 'menu';
    ensureMenuMusic();
    const isGod = selectedModeId === 'godtrial';
    const modeName = isGod ? 'Final Boss: Astrael' : ((MODE_CONFIGS[selectedModeId] || MODE_CONFIGS.normal).name);
    selectedLoadoutItems = sanitizeActiveItems(selectedLoadoutItems, MODE_CONFIGS[selectedModeId] || MODE_CONFIGS.normal).slice(0, START_ACTIVE_SPECIAL_ITEMS);
    showOverlay(`
        <div class="card">
            <div class="navTop">
                <div><div class="navTitle">Active Items</div><div class="navSub">Choose 2 special items for this run. Core drops always stay active: coins, bombs and hearts.</div></div>
                <button class="secondary" id="shipBackBtn">Back to Ships</button>
            </div>
            <div class="sectionCard" style="text-align:left;">
                <div class="itemTitle">Mode: ${escapeHtml(modeName)}</div>
                <div class="itemText">Only selected special items can drop at the start. After each boss, you can unlock 1 more special item before choosing a relic.</div>
                <div class="loadoutBar" id="loadoutBar">${loadoutHtml(selectedLoadoutItems)}</div>
            </div>
            <div class="activeItemGrid">${itemCardsHtml(selectedLoadoutItems, START_ACTIVE_SPECIAL_ITEMS)}</div>
            <div class="rowButtons">
                <button class="primary" id="launchBtn">Start Run</button>
            </div>
        </div>
    `);
    document.getElementById('shipBackBtn').addEventListener('click', () => { playSfx('click'); renderShipSelect(); });
    document.querySelectorAll('.activeItemCard').forEach(card => {
        card.addEventListener('click', () => {
            const id = card.getAttribute('data-item');
            let current = [];
            for (const x of (selectedLoadoutItems || [])) if (SPECIAL_ITEM_BY_ID[x] && !current.includes(x)) current.push(x);
            if (current.includes(id)) {
                if (current.length > 1) current = current.filter(x => x !== id);
            } else {
                if (current.length >= START_ACTIVE_SPECIAL_ITEMS) current.shift();
                current.push(id);
            }
            selectedLoadoutItems = current;
            playSfx('select');
            renderItemLoadout();
        });
    });
    document.getElementById('launchBtn').addEventListener('click', () => {
        selectedLoadoutItems = sanitizeActiveItems(selectedLoadoutItems, MODE_CONFIGS[selectedModeId] || MODE_CONFIGS.normal).slice(0, START_ACTIVE_SPECIAL_ITEMS);
        playSfx('start');
        if (selectedModeId === 'godtrial') startFinalBoss(); else startRun(selectedModeId || 'normal');
    });
}
function renderRelicLibrary(filter='All', query='') {
    state = 'menu';
    ensureMenuMusic();
    showOverlay(`
        <div class="card">
            <div class="navTop">
                <div><div class="navTitle">Relic Library</div><div class="navSub">Temporary run relics, organized by rarity and effect type.</div></div>
                <button class="secondary" id="backBtn">Back</button>
            </div>
            <div class="filterBar">
                ${['All','Common','Rare','Legendary'].map(f => `<button class="filterBtn ${filter===f?'active':''}" data-filter="${f}">${f}</button>`).join('')}
                <input class="searchInput" id="relicSearch" maxlength="30" placeholder="Search relic" value="${escapeHtml(query)}" />
            </div>
            <div class="compactList relicLibrary" style="grid-template-columns:repeat(2,1fr); max-height:420px;">${relicLibraryHtml(filter, query)}</div>
        </div>
    `);
    bindBack();
    document.querySelectorAll('.filterBtn').forEach(b => b.addEventListener('click', () => { playSfx('click'); renderRelicLibrary(b.getAttribute('data-filter') || 'All', document.getElementById('relicSearch')?.value || ''); }));
    const search = document.getElementById('relicSearch');
    if (search) search.addEventListener('input', () => renderRelicLibrary(filter, search.value));
}
function renderStats(tab='player') {
    state = 'menu';
    ensureMenuMusic();
    showOverlay(`
        <div class="card">
            <div class="navTop">
                <div><div class="navTitle">Stats</div><div class="navSub">Run history, local player stats and local leaderboard.</div></div>
                <button class="secondary" id="backBtn">Back</button>
            </div>
            <div class="tabBar">
                <button class="tabBtn ${tab==='player'?'active':''}" id="playerTab">Player Stats</button>
                <button class="tabBtn ${tab==='leaderboard'?'active':''}" id="leaderTab">Leaderboard</button>
            </div>
            <div>${tab==='player' ? playerStatsHtml() : boardHtml()}</div>
            <div class="dangerZone">
                <div class="rowButtons">
                    <button class="secondary" id="clearBtn">Clear leaderboard</button>
                    <button class="secondary" id="clearStatsBtn">Clear player stats</button>
                </div>
            </div>
        </div>
    `);
    bindBack();
    document.getElementById('playerTab').addEventListener('click', () => { playSfx('click'); renderStats('player'); });
    document.getElementById('leaderTab').addEventListener('click', () => { playSfx('click'); renderStats('leaderboard'); });
    document.getElementById('clearBtn').addEventListener('click', () => { localStorage.removeItem(STORAGE_KEY); playSfx('click'); renderStats('leaderboard'); });
    document.getElementById('clearStatsBtn').addEventListener('click', () => { localStorage.removeItem(STATS_KEY); localStorage.removeItem(LAST_DEATH_KEY); playSfx('click'); renderStats('player'); });
}
function renderSettings() {
    state = 'menu';
    ensureMenuMusic();
    showOverlay(`
        <div class="card">
            <div class="navTop">
                <div><div class="navTitle">Settings</div><div class="navSub">Audio controls are here so the main menu stays clean.</div></div>
                <button class="secondary" id="backBtn">Back</button>
            </div>
            <div class="settingsGrid">
                <div class="volumeRow">
                    <span>Music</span>
                    <input id="volumeSlider" type="range" min="0" max="100" value="${Math.round(musicVolume*100)}" />
                    <span id="volumeValue">${Math.round(musicVolume*100)}%</span>
                </div>
                <div class="volumeRow">
                    <span>Effects</span>
                    <input id="sfxSlider" type="range" min="0" max="100" value="${Math.round(sfxVolume*100)}" />
                    <span id="sfxValue">${Math.round(sfxVolume*100)}%</span>
                </div>
                <div class="rowButtons">
                    <button class="secondary" id="resetAudioBtn">Reset audio</button>
                </div>
            </div>
            <div class="smallNote">Music loops automatically. If the browser blocks it, click once inside the game and use Reset audio.</div>
        </div>
    `);
    bindBack();
    const slider = document.getElementById('volumeSlider');
    if (slider) slider.addEventListener('input', () => {
        updateMusicVolume(Number(slider.value) / 100);
        const label = document.getElementById('volumeValue');
        if (label) label.textContent = `${slider.value}%`;
        if (state === 'menu') playMusic('menu');
    });
    const sfxSlider = document.getElementById('sfxSlider');
    if (sfxSlider) sfxSlider.addEventListener('input', () => {
        updateSfxVolume(Number(sfxSlider.value) / 100);
        const label = document.getElementById('sfxValue');
        if (label) label.textContent = `${sfxSlider.value}%`;
        playSfx('click');
    });
    document.getElementById('resetAudioBtn').addEventListener('click', () => {
        playSfx('click');
        stopMusic();
        playMusic('menu');
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
        invulnBonus: 0,
        shipSpeed: 1,
        rushCoinValue: 0,
        laserWarning: 0,
        afterBossInvuln: 0,
        rushSlow: 1,
        critBonus: 0,
        bombClearRadius: 0,
        hitInvulnBonus: 0,
        rushDurationMult: 1,
        zoneShield: 0,
        heartShield: 0,
        bombMagnet: 0,
        powerClearRadius: 0,
        coinScoreBonus: 0,
        heatHeartBonus: 0,
        bossSkillSlow: 1,
        lowLifeCoinBonus: 0,
        rushShield: 0,
        lastStandCrit: 0,
        projectileCapBonus: 0,
        scalingReviveDiscount: 0,
        magnetBombDamage: 0,
        blueCritBonus: 0,
        forcedCritBonus: 0,
        goldOverchargeBonus: 0,
        riskCoinBonus: 0,
        timeSlowPulse: 0,
        critCoreLuck: 0,
        heartScoreBonus: 0,
        riskReviveDiscount: 0,
        shieldBombBonus: 0,
        overchargeCoinScore: 0,
        maxCriticalCharges: 0,
        invulnBombBonus: 0,
        overchargeDurationBonus: 0,
        rushMagnetBonus: 0,
        timeLaserClear: 0,
        powerScoreBonus: 0,
        rushShieldScore: 0,
        critCoreDamageBonus: 0,
        shieldClearBonus: 0,
        powerShieldIfEmpty: 0,
        timeScoreBonus: 0,
        extraShieldBombBonus: 0,
        heartShieldBombBonus: 0,
        timeFragmentShield: 0,
        critCoreSkillDelay: 0,
        lowLifeCritScore: 0,
        rushBombBonus: 0,
        lowLifeCritDamage: 0,
        clearScoreBonus: 0,
        magnetPulseCoinBonus: 0,
        riskCoreBombBonus: 0,
        riskCoreBurst: 0,
        heartCritCharge: 0,
        overchargeBonusFlat: 0,
        timeFragmentCoins: 0
    };
}

function startRun(mode='normal') {
    currentMode = mode || 'normal';
    modeConfig = MODE_CONFIGS[currentMode] || MODE_CONFIGS.normal;
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
        targetY: H - 90,
        magnetPulse: 0,
        overcharge: 0,
        nextBombBonus: 0,
        slowPulse: 0,
        criticalCharges: 0
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
        shieldsPicked: 0,
        timeFragments: 0,
        magnetPulses: 0,
        riskCores: 0,
        overcharges: 0,
        criticalCores: 0,
        hearts: 0,
        revives: 0,
        hits: 0,
        damageEvents: [],
        synergyTriggers: 0,
        deathCause: '',
        deathBoss: '',
        deathAttack: '',
        deathStage: '',
        deathQuote: '',
        mode: currentMode,
        heat: modeConfig.overheat ? 28 : null,
        survivalLevel: 1,
        seed,
        activeTime: 0,
        victory: false,
        secretTrial: false,
        activeItems: [],
        defeatedBosses: [],
        practice: false
    };
    activeSpecialItems = sanitizeActiveItems(selectedLoadoutItems, modeConfig).slice(0, START_ACTIVE_SPECIAL_ITEMS);
    runStats.activeItems = activeSpecialItems.slice();
    bullets = [];
    lasers = [];
    particles = [];
    rush = null;
    usedRelics = [];
    relicChoices = [];
    elapsed = 0;
    deathTimer = 0;
    resumeCountdown = 0;
    mouse.x = W/2;
    mouse.y = H - 90;
    stopMusic();
    spawnBoss(1);
    hideOverlay();
    state = 'playing';
    startRunEffects(false);
}

function startFinalBoss() {
    if (!isSecretUnlocked()) return;
    currentMode = 'godtrial';
    modeConfig = {...MODE_CONFIGS.normal, id:'godtrial', name:'God Trial', corrupted:false, bossRush:false, survival:false, turbo:false, overheat:false, rush:false, relics:false, baseAggro:1.18, dropMult:1.05, color:'#facc15'};
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
        targetY: H - 90,
        magnetPulse: 0,
        overcharge: 0,
        nextBombBonus: 0,
        slowPulse: 0,
        criticalCharges: 0
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
        shieldsPicked: 0,
        timeFragments: 0,
        magnetPulses: 0,
        riskCores: 0,
        overcharges: 0,
        criticalCores: 0,
        hearts: 0,
        revives: 0,
        hits: 0,
        damageEvents: [],
        synergyTriggers: 0,
        deathCause: '',
        deathBoss: '',
        deathAttack: '',
        deathStage: '',
        deathQuote: '',
        mode: currentMode,
        heat: null,
        survivalLevel: 1,
        seed,
        activeTime: 0,
        victory: false,
        secretTrial: true,
        activeItems: [],
        defeatedBosses: [],
        practice: false
    };
    activeSpecialItems = sanitizeActiveItems(selectedLoadoutItems, modeConfig).slice(0, START_ACTIVE_SPECIAL_ITEMS);
    runStats.activeItems = activeSpecialItems.slice();
    bullets = [];
    lasers = [];
    particles = [];
    rush = null;
    usedRelics = [];
    relicChoices = [];
    elapsed = 0;
    deathTimer = 0;
    resumeCountdown = 0;
    mouse.x = W/2;
    mouse.y = H - 90;
    stopMusic();
    spawnSecretBoss();
    hideOverlay();
    state = 'playing';
    startRunEffects(true);
}


function startPractice() {
    if (!selectedPracticeBoss || !isPracticeBossUnlocked(selectedPracticeBoss)) { renderPracticeBossSelect(); return; }
    currentMode = 'practice';
    modeConfig = {id:'practice', name:'Practice', corrupted:false, bossRush:false, survival:false, turbo:false, overheat:false, rush:false, relics:false, practice:true, baseAggro:0.95 + Math.max(0, (selectedPracticeBoss.zone || 1) - 1) * 0.08, dropMult:1.0, color:selectedPracticeBoss.color || '#60a5fa'};
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
        invuln: 1.4,
        ship,
        r: 10,
        targetX: W/2,
        targetY: H - 90,
        magnetPulse: 0,
        overcharge: 0,
        nextBombBonus: 0,
        slowPulse: 0,
        criticalCharges: 0
    };
    mods = resetMods(ship);
    runStats = {
        zone: selectedPracticeBoss.zone || 1,
        bossesKilled: 0,
        coins: 0,
        score: 0,
        bombs: {blue: 0, purple: 0, gold: 0},
        critBombs: 0,
        powerups: 0,
        shieldsPicked: 0,
        timeFragments: 0,
        magnetPulses: 0,
        riskCores: 0,
        overcharges: 0,
        criticalCores: 0,
        hearts: 0,
        revives: 0,
        hits: 0,
        damageEvents: [],
        synergyTriggers: 0,
        deathCause: '',
        deathBoss: '',
        deathAttack: '',
        deathStage: '',
        deathQuote: '',
        mode: currentMode,
        heat: null,
        survivalLevel: 1,
        seed,
        activeTime: 0,
        victory: false,
        secretTrial: !!selectedPracticeBoss.secret,
        activeItems: [],
        defeatedBosses: [],
        practice: true
    };
    activeSpecialItems = sanitizeActiveItems(selectedPracticeItems, modeConfig).slice(0, MAX_ACTIVE_SPECIAL_ITEMS);
    runStats.activeItems = activeSpecialItems.slice();
    bullets = [];
    lasers = [];
    particles = [];
    rush = null;
    usedRelics = [];
    relicChoices = [];
    elapsed = 0;
    deathTimer = 0;
    resumeCountdown = 0;
    mouse.x = W/2;
    mouse.y = H - 90;
    for (const id of selectedPracticeRelics || []) {
        const r = RELICS.find(x => x.id === id);
        if (r && typeof r.apply === 'function') {
            usedRelics.push(r.id);
            r.apply();
        }
    }
    stopMusic();
    spawnSpecificBoss(selectedPracticeBoss);
    hideOverlay();
    state = 'playing';
    startRunEffects(false);
}

function spawnSpecificBoss(template) {
    const zone = template.zone || 1;
    boss = {
        ...template,
        zone,
        x: W/2,
        y: 86,
        hp: template.secret ? 135 : 100,
        maxHp: template.secret ? 135 : 100,
        size: template.secret ? 76 : 46 + zone * 4,
        fireCooldown: 0.75,
        moveT: rand() * 10,
        hitTimer: 0,
        deathTimer: 0,
        dead: false,
        defeatedHandled: false,
        intro: 1.4,
        shields: 0,
        skills: createBossSkills(template.archetype),
        corrupted: false,
        stolenArchetype: template.secret ? 'sun' : null,
        secret: !!template.secret
    };
    addTextParticle(W/2, 220, `Practice: ${boss.name}`, boss.color, 1.6, 30);
    playBossMusic();
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
        fireCooldown: 0.72 + Math.max(0, 2 - zone) * 0.10,
        moveT: rand() * 10,
        hitTimer: 0,
        deathTimer: 0,
        dead: false,
        defeatedHandled: false,
        intro: 1.4,
        shields: 0,
        skills: createBossSkills(base.archetype),
        corrupted: !!modeConfig.corrupted || (!!modeConfig.bossRush && zone >= 5),
        stolenArchetype: null
    };
    if (boss.corrupted) {
        const all = ['drone','widow','reaper','maw','serpent','halo','engine','furnace','sun','tyrant'];
        boss.stolenArchetype = all[Math.floor(rand()*all.length)];
        boss.name = `Corrupted ${boss.name}`;
        boss.subtitle = `${boss.subtitle} · stolen ${boss.stolenArchetype}`;
        boss.color = '#c084fc';
    }
    addTextParticle(W/2, 220, `${modeConfig.bossRush ? 'Boss Rush' : modeConfig.survival ? 'Survival' : 'Zone'} ${zone}: ${boss.name}`, boss.color, 1.6, 30);
    if (mods && mods.zoneShield > 0) {
        player.shields += mods.zoneShield;
        addTextParticle(player.x, player.y - 28, `+${mods.zoneShield} Shield`, '#bfdbfe', 1.0, 18);
    }
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
        secret: true,
        shields: 0,
        skills: createBossSkills('astrael'),
        corrupted: false,
        stolenArchetype: 'sun'
    };
    addTextParticle(W/2, 220, 'FINAL TRIAL', '#fff8ec', 1.4, 34);
    addTextParticle(W/2, 265, boss.name, boss.color, 1.7, 30);
    playBossMusic();
}

function completeBoss() {
    const defeatedName = canonicalBossName(boss?.name || 'Unknown Boss');
    runStats.bossesKilled += 1;
    if (runStats.defeatedBosses && defeatedName) runStats.defeatedBosses.push(defeatedName);
    runStats.score += boss.secret ? 7000 : 1000 + boss.zone * 350 + Math.round(modeIntensity()*100);
    bullets = bullets.filter(o => o.type !== 'bullet');
    lasers = [];
    if (modeConfig.practice) {
        stopMusic();
        practiceVictory();
        return;
    }
    if (boss.secret) {
        stopMusic();
        trueVictory();
        return;
    }
    if (modeConfig.survival) {
        runStats.survivalLevel += 1;
        showPostBossReward();
        return;
    }
    if (boss.zone >= 5) {
        stopMusic();
        victory();
        return;
    }
    if (modeConfig.bossRush) {
        showPostBossReward();
        return;
    }
    if (modeConfig.rush) startInfernoRush(boss.zone);
    else showPostBossReward();
}


function startRunEffects(isGod=false) {
    screenFlash = isGod ? 0.85 : 0.55;
    screenShake = isGod ? 0.9 : 0.55;
    playSfx(isGod ? 'godStart' : 'runStart');
    addTextParticle(W/2, H/2 - 20, isGod ? 'GOD TRIAL' : 'RUN START', isGod ? '#facc15' : '#fff8ec', 1.1, isGod ? 44 : 38);
    addTextParticle(W/2, H/2 + 28, isGod ? 'Astrael awakens' : 'Survive the inferno', isGod ? '#f43f5e' : '#ff7a2f', 1.1, 22);
    for (let i=0; i<85; i++) addParticle(player.x, player.y, i%2 ? player.ship.accent : '#fff8ec', rand()*4+1, rand()*Math.PI*2, rand()*260+80, 0.8+rand()*0.7);
}

function startInfernoRush(zoneCleared) {
    const duration = clamp((RUSH_MIN_SECONDS + zoneCleared * 2.5) * (mods.rushDurationMult || 1), RUSH_MIN_SECONDS * 0.75, RUSH_MAX_SECONDS);
    rush = {
        zone: zoneCleared,
        duration,
        time: 0,
        spawn: 0.25,
        laser: 1.2,
        wall: 0.8,
        pulse: 0,
        pattern: zoneCleared % 4,
        nextZone: zoneCleared + 1
    };
    state = 'rush';
    hideOverlay();
    bullets = [];
    lasers = [];
    boss = null;
    player.invuln = Math.max(player.invuln, 1.0 + (mods.afterBossInvuln || 0));
    if (mods.rushShield > 0) player.shields += mods.rushShield;
    screenFlash = 0.75;
    screenShake = 0.75;
    playSfx('rushStart');
    addTextParticle(W/2, H/2 - 20, 'PHASE SHIFT', '#fff8ec', 1.2, 42);
    addTextParticle(W/2, H/2 + 26, `Inferno Rush ${Math.round(duration)}s`, '#ff7a2f', 1.2, 24);
    for (let i=0; i<120; i++) addParticle(W/2, H/2, i%2 ? '#ff7a2f' : '#fff8ec', rand()*4+1, rand()*Math.PI*2, rand()*420+120, 1.0+rand()*0.8);
}

function completeRush() {
    if (!rush) return;
    const zoneDone = rush.zone;
    const bonus = Math.round(250 + zoneDone * 100 + runStats.coins * 0.03);
    runStats.score += bonus;
    rush = null;
    bullets = [];
    lasers = [];
    stopMusic();
    playSfx('rushClear');
    screenFlash = 0.5;
    showPostBossReward();
}

function updateRush(dt) {
    if (!rush) return;
    rush.time += dt;
    rush.spawn -= dt;
    rush.wall -= dt;
    rush.pulse += dt;
    const difficulty = 1 + rush.zone * 0.16;
    if (rush.wall <= 0) {
        spawnRushWall(difficulty);
        rush.wall = Math.max(1.05, (1.70 - rush.zone*0.08) * mods.rushSlow + rand()*0.32);
    }
    if (rush.zone >= 2 && rush.spawn <= 0) {
        spawnRushWave(difficulty);
        rush.spawn = Math.max(0.34, (0.92 - rush.zone*0.055) * mods.rushSlow + rand()*0.22);
    }
    if (rush.time >= rush.duration) completeRush();
}

function spawnRushWave(difficulty) {
    if (!rush || rush.zone < 2) return;
    const speed = (150 + rush.zone * 18) * mods.rushSlow;
    const count = rush.zone === 2 ? 2 : rush.zone === 3 ? 3 : 4;
    for (let i=0; i<count; i++) {
        const y = 125 + rand()*(H-185);
        const wiggle = rush.zone >= 4 ? (rand()-0.5)*0.20 : 0;
        spawnShot(W+18 + i*52, y, Math.PI + wiggle, speed*(0.88+rand()*0.18), 6.0 + Math.min(2, rush.zone*0.35), 'bullet', 'Inferno Rush orb');
    }
    if (rush.zone >= 3 && rand() < 0.22) {
        const y = H/2 + (rand()-0.5)*150;
        spawnShot(W+25, y, Math.PI, speed*0.60, 8, 'coin', 'Rush coin lane');
    }
}

function spawnRushLaser(difficulty) {
    // v9.6: Inferno Rush now focuses on readable barrier lanes. Lasers are reserved for bosses.
    return false;
}

function spawnRushWall(difficulty) {
    const amp = Math.min(92, 28 + rush.zone * 13);
    const gapY = clamp(H/2 + Math.sin(elapsed*1.35 + rush.zone) * amp + (rand()-0.5)*(18 + rush.zone*5), 165, H-115);
    const gap = Math.max(92, 170 - rush.zone*12);
    const w = 28 + rush.zone*2;
    const wallSpeed = -175 - rush.zone*16;
    spawnLaser(W+42, 105, w, Math.max(0, gapY-gap/2-105), 0.05, 4.8 * mods.rushSlow, '#fb7185', 'wall', wallSpeed, 0, 'Inferno Rush barrier');
    spawnLaser(W+42, gapY+gap/2, w, Math.max(0, H-(gapY+gap/2)-24), 0.05, 4.8 * mods.rushSlow, '#fb7185', 'wall', wallSpeed, 0, 'Inferno Rush barrier');
    if (rush.zone >= 4 && rand() < 0.35) {
        const offset = rand() < 0.5 ? -58 : 58;
        const gy2 = clamp(gapY + offset, 165, H-115);
        spawnLaser(W+108, 105, Math.max(18, w-6), Math.max(0, gy2-gap/2-105), 0.05, 4.8 * mods.rushSlow, '#f97316', 'wall', wallSpeed*0.96, 0, 'Inferno Rush double barrier');
        spawnLaser(W+108, gy2+gap/2, Math.max(18, w-6), Math.max(0, H-(gy2+gap/2)-24), 0.05, 4.8 * mods.rushSlow, '#f97316', 'wall', wallSpeed*0.96, 0, 'Inferno Rush double barrier');
    }
}

function relicRollWeight(r) {
    let w = r.rarity === 'Legendary' ? 0.42 : (r.rarity === 'Rare' ? 1.15 : 2.35);
    const tags = r.tags || [];
    if (modeConfig?.overheat && (tags.includes('Time Fragment') || relicTypeText(r) === 'Overheat')) w *= 1.55;
    if (modeConfig?.rush && tags.includes('Inferno Rush')) w *= 1.25;
    if (player?.ship?.id === 'vault' && (tags.includes('Coin') || tags.includes('Risk Core'))) w *= 1.25;
    if (player?.ship?.id === 'aegis' && (tags.includes('Shield') || relicTypeText(r) === 'Defense')) w *= 1.18;
    if (usedRelics.includes('crit') && tags.includes('Critical Core')) w *= 1.18;
    if (usedRelics.includes('magnet') && (tags.includes('Magnet Pulse') || tags.includes('Bombs'))) w *= 1.12;
    if (usedRelics.includes('coin') && (tags.includes('Coin') || tags.includes('Risk Core'))) w *= 1.12;
    return Math.max(0.05, w);
}
function weightedRelicPick(pool) {
    const total = pool.reduce((sum, r) => sum + relicRollWeight(r), 0);
    let roll = rand() * total;
    for (let i = 0; i < pool.length; i++) {
        roll -= relicRollWeight(pool[i]);
        if (roll <= 0) return i;
    }
    return pool.length - 1;
}
function chooseRelics() {
    const repeatable = ['coin','blue','purple','heart','luck','bombValue','paniccoin'];
    const available = RELICS.filter(r => !usedRelics.includes(r.id) || repeatable.includes(r.id));
    const picks = [];
    while (picks.length < 3 && available.length) {
        const i = weightedRelicPick(available);
        const r = available.splice(i, 1)[0];
        picks.push(r);
    }
    return picks;
}
function currentBuildHint() {
    const labels = [];
    if (usedRelics.includes('coin') || usedRelics.includes('stormcoin') || player?.ship?.id === 'vault') labels.push('Coin economy');
    if (usedRelics.includes('crit') || usedRelics.includes('godspark') || usedRelics.includes('laststand')) labels.push('Critical bombs');
    if (usedRelics.includes('magnet') || usedRelics.includes('bombmagnet') || usedRelics.includes('magnetbank')) labels.push('Magnet pickups');
    if (usedRelics.includes('shield') || usedRelics.includes('guardian') || player?.ship?.id === 'aegis') labels.push('Shield offense');
    if (modeConfig?.overheat || usedRelics.includes('coolant') || usedRelics.includes('timebroker')) labels.push('Overheat timing');
    if (!labels.length) return 'No defined build yet. Reroll if all three choices fight your current ship or mode.';
    return `Current build tags: ${labels.slice(0,3).join(' · ')}. Active items: ${(activeSpecialItems || []).map(activeItemName).join(' · ') || 'None'}. Reroll when relic choices do not support your active item pool.`;
}
function activeItemRewardOptions() {
    const available = SPECIAL_ITEMS.filter(i => !(activeSpecialItems || []).includes(i.id));
    const picks = [];
    while (picks.length < 3 && available.length) {
        const i = Math.floor(rand() * available.length);
        picks.push(available.splice(i,1)[0]);
    }
    return picks;
}
function continueAfterItemReward() {
    if (typeof rewardNextFn === 'function') {
        const fn = rewardNextFn;
        rewardNextFn = null;
        fn();
    } else {
        showRelicChoice();
    }
}
function showItemUnlockReward(nextFn) {
    rewardNextFn = nextFn || showRelicChoice;
    if (!modeConfig.relics || (activeSpecialItems || []).length >= MAX_ACTIVE_SPECIAL_ITEMS) {
        continueAfterItemReward();
        return;
    }
    const options = activeItemRewardOptions();
    if (!options.length) {
        continueAfterItemReward();
        return;
    }
    state = 'itemReward';
    paused = false;
    const cards = options.map(item => `
        <div class="activeItemCard" data-reward-item="${item.id}" style="border-color:${hexToRgba(item.color, .36)};">
            <div class="itemTitle" style="color:${item.color};">${item.name}</div>
            <div class="itemText"><b>${item.build}</b><br>${item.effect}</div>
            <div class="metaLine"><span class="rarity">${item.rarity}</span><span class="rarity">${item.chance}</span></div>
        </div>
    `).join('');
    showOverlay(`
        <div class="card">
            <h1 class="title" style="font-size:40px;">Activate Item</h1>
            <div class="subtitle">Choose 1 more special item to add to this run's drop pool.</div>
            <div class="loadoutBar"><span class="tinyTag">Active now</span>${(activeSpecialItems || []).map(id => `<span class="tinyTag" style="border-color:${hexToRgba(SPECIAL_ITEM_BY_ID[id]?.color || '#fff8ec', .32)};">${escapeHtml(activeItemName(id))}</span>`).join('')}</div>
            <div class="activeItemGrid">${cards}</div>
            <div class="rowButtons"><button class="secondary" id="skipItemRewardBtn">Skip item</button></div>
            <div class="smallNote">This keeps battle drops readable. Reroll relics based on the items you activate.</div>
        </div>
    `);
    document.querySelectorAll('.activeItemCard[data-reward-item]').forEach(card => {
        card.addEventListener('click', () => {
            const id = card.getAttribute('data-reward-item');
            if (SPECIAL_ITEM_BY_ID[id] && !activeSpecialItems.includes(id)) {
                activeSpecialItems.push(id);
                runStats.activeItems = activeSpecialItems.slice();
                playSfx('powerup');
            }
            continueAfterItemReward();
        });
    });
    const skip = document.getElementById('skipItemRewardBtn');
    if (skip) skip.addEventListener('click', () => { playSfx('click'); continueAfterItemReward(); });
}
function showPostBossReward() {
    if (modeConfig.relics) showItemUnlockReward(showRelicChoice);
    else showRelicChoice();
}
function showRelicChoice() {
    state = 'relic';
    paused = false;
    relicChoices = chooseRelics();
    const relicHtml = relicChoices.map((r, idx) => `
        <div class="relicCard" data-relic="${idx}">
            <div class="itemTitle">${r.name}</div>
            <div class="itemText">${r.desc}</div>
            ${r.synergy ? `<div class="smallNote"><b>Combo:</b> ${escapeHtml(r.synergy)}</div>` : ''}
            ${relicTagsHtml(r)}
            <div class="metaLine"><span class="rarity">${r.rarity}</span><span class="rarity">${relicTypeText(r)}</span></div>
        </div>
    `).join('');
    const rerollDisabled = runStats.coins < 150 ? 'disabled' : '';
    showOverlay(`
        <div class="card">
            <h1 class="title" style="font-size:42px;">Boss Defeated</h1>
            <div class="subtitle">Choose one relic for this run. It disappears when the run ends. Mode: ${modeLabel()}.</div>
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
            <div class="smallNote">${currentBuildHint()}</div>
            <div class="smallNote">Active item pool: ${(activeSpecialItems || []).map(activeItemName).join(' · ') || 'None'}.</div><div class="smallNote">Next zone will start after selecting a relic.</div>
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
            if (modeConfig.survival) {
                runStats.zone = clamp(1 + Math.floor(runStats.bossesKilled / 2), 1, 5);
            } else {
                runStats.zone += 1;
            }
            if (mods.scalingReviveDiscount) mods.reviveCost = Math.max(500, mods.reviveCost - mods.scalingReviveDiscount);
            bullets = [];
            lasers = [];
            particles = [];
            rush = null;
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
        seed: runStats.seed,
        mode: modeLabel(),
        ship: player?.ship?.name || 'Unknown',
        bombsUsed: (runStats.bombs.blue + runStats.bombs.purple + runStats.bombs.gold),
        hits: runStats.hits || 0,
        relics: usedRelics.slice(),
        defeatedBosses: runStats.defeatedBosses ? runStats.defeatedBosses.slice() : [],
        stage: runStats.secretTrial ? 'God Trial' : `Zone ${runStats.zone}`
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
    localStorage.setItem(SECRET_DEFEATED_KEY, '1');
    addBoardEntry({
        name: playerName,
        victory: true,
        trueVictory: true,
        bosses: 6,
        coins: runStats.coins,
        score: runStats.score + 5000,
        time: runStats.activeTime,
        seed: runStats.seed,
        mode: modeLabel(),
        ship: player?.ship?.name || 'Unknown',
        bombsUsed: (runStats.bombs.blue + runStats.bombs.purple + runStats.bombs.gold),
        hits: runStats.hits || 0,
        relics: usedRelics.slice(),
        defeatedBosses: runStats.defeatedBosses ? runStats.defeatedBosses.slice() : [],
        stage: runStats.secretTrial ? 'God Trial' : `Zone ${runStats.zone}`
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


function practiceVictory() {
    playSfx('victory');
    state = 'practiceclear';
    runStats.victory = true;
    showOverlay(`
        <div class="card">
            <h1 class="title" style="font-size:46px;">Practice Clear</h1>
            <div class="subtitle">${escapeHtml(selectedPracticeBoss?.name || 'Boss')} defeated. This practice result was not saved to leaderboard.</div>
            ${resultStatsHtml()}
            <div class="rowButtons">
                <button class="primary" id="practiceAgainBtn">Practice Again</button>
                <button class="secondary" id="practiceMenuBtn2">Practice Menu</button>
                <button class="secondary" id="menuBtn">Main Menu</button>
            </div>
        </div>
    `);
    document.getElementById('practiceAgainBtn').addEventListener('click', () => startPractice());
    document.getElementById('practiceMenuBtn2').addEventListener('click', () => renderPracticeBossSelect());
    document.getElementById('menuBtn').addEventListener('click', () => renderMenu());
}

function practiceGameOver() {
    stopMusic();
    state = 'ended';
    showOverlay(`
        <div class="card">
            <h1 class="title" style="font-size:48px;">Practice Failed</h1>
            <div class="subtitle">Good. That means the boss is teaching you something.</div>
            ${deathReportHtml()}
            <div class="rowButtons">
                <button class="primary" id="practiceAgainBtn">Retry Practice</button>
                <button class="secondary" id="practiceMenuBtn2">Practice Menu</button>
                <button class="secondary" id="menuBtn">Main Menu</button>
            </div>
        </div>
    `);
    document.getElementById('practiceAgainBtn').addEventListener('click', () => startPractice());
    document.getElementById('practiceMenuBtn2').addEventListener('click', () => renderPracticeBossSelect());
    document.getElementById('menuBtn').addEventListener('click', () => renderMenu());
}

function permanentGameOver() {
    if (modeConfig.practice) { practiceGameOver(); return; }
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
        seed: runStats.seed,
        mode: modeLabel(),
        ship: player?.ship?.name || 'Unknown',
        bombsUsed: (runStats.bombs.blue + runStats.bombs.purple + runStats.bombs.gold),
        hits: runStats.hits || 0,
        relics: usedRelics.slice(),
        defeatedBosses: runStats.defeatedBosses ? runStats.defeatedBosses.slice() : [],
        deathBoss: runStats.deathBoss || (boss?.name || 'Unknown'),
        deathCause: runStats.deathCause || 'Unknown',
        stage: runStats.deathStage || `Zone ${runStats.zone}`
    });
    showOverlay(`
        <div class="card">
            <h1 class="title" style="font-size:48px;">Game Over</h1>
            <div class="subtitle">The inferno got you. Final result saved to the leaderboard.</div>
            ${deathReportHtml()}
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
    reviveState = rush ? 'rush' : 'playing';
    stopMusic();
    state = 'gameover';
    const canRevive = runStats.coins >= mods.reviveCost;
    showOverlay(`
        <div class="card">
            <h1 class="title" style="font-size:48px;">Game Over</h1>
            <div class="subtitle">Spend coins to buy one life and continue this run.</div>
            ${deathReportHtml()}
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
            player.dead = false;
            player.invuln = 2.5;
            player.x = W/2;
            player.y = H - 90;
            mouse.x = player.x;
            mouse.y = player.y;
            bullets = [];
            particles = [];
            hideOverlay();
            state = reviveState || 'playing';
            resumeCountdown = 3.0;
            if (state === 'playing') playBossMusic();
            addTextParticle(W/2, H/2, 'Revived', '#fff8ec', 1.0, 32);
        }
    });
    document.getElementById('endBtn').addEventListener('click', permanentGameOver);
}

function resultStatsHtml() {
    const bossLabel = runStats.secretTrial ? `${runStats.bossesKilled}/1` : (modeConfig.survival ? `${runStats.bossesKilled}` : `${runStats.bossesKilled}/5`);
    const bossText = runStats.secretTrial ? 'God defeated' : (modeConfig.survival ? 'Bosses defeated' : 'Bosses defeated');
    const heatText = modeConfig.overheat ? ` Overheat left: ${Math.max(0, runStats.heat || 0).toFixed(1)}s.` : '';
    return `
        <div class="statLine">
            <div class="statBox"><div class="statValue">${bossLabel}</div><div class="statLabel">${bossText}</div></div>
            <div class="statBox"><div class="statValue">${runStats.coins}</div><div class="statLabel">Coins</div></div>
            <div class="statBox"><div class="statValue">${formatTime(runStats.activeTime)}</div><div class="statLabel">Time</div></div>
            <div class="statBox"><div class="statValue">${runStats.score}</div><div class="statLabel">Score</div></div>
        </div>
        <div class="smallNote">Mode: ${modeLabel()}. Bombs: blue ${runStats.bombs.blue}, purple ${runStats.bombs.purple}, golden ${runStats.bombs.gold}. Critical bombs: ${runStats.critBombs || 0}. Power ups: ${runStats.powerups || 0}. Hits: ${runStats.hits || 0}.${heatText} Seed: ${runStats.seed}.</div>
        <div class="smallNote">Relics: ${usedRelics.length ? usedRelics.map(id => (RELICS.find(r=>r.id===id)?.name || id)).join(', ') : 'None yet'}.</div><div class="smallNote">Active items: ${(activeSpecialItems || []).map(activeItemName).join(', ') || 'None'}.</div>
    `;
}
function deathReportHtml() {
    const quotes = [
        'The inferno filed a complaint against your ship.',
        'That dodge was almost legal.',
        'The boss says thanks for the coins.',
        'Pilot status: toasted, but stylish.',
        'The run died. The addiction survived.'
    ];
    const quote = runStats.deathQuote || quotes[Math.floor(rand()*quotes.length)];
    runStats.deathQuote = quote;
    localStorage.setItem(LAST_DEATH_KEY, JSON.stringify({
        cause: runStats.deathCause || 'Unknown', boss: runStats.deathBoss || 'Unknown', attack: runStats.deathAttack || 'Unknown',
        time: runStats.activeTime, coins: runStats.coins, bombs: runStats.bombs, hits: runStats.hits || 0, mode: modeLabel(), stage: runStats.deathStage || `Zone ${runStats.zone}`
    }));
    return `
        ${resultStatsHtml()}
        <div class="leaderboard" style="margin-top:12px;">
            <div class="leaderTitle">Death Report</div>
            <div class="statLine" style="margin:10px;">
                <div class="statBox"><div class="statValue" style="font-size:18px;">${escapeHtml(runStats.deathCause || 'Unknown')}</div><div class="statLabel">Cause of death</div></div>
                <div class="statBox"><div class="statValue" style="font-size:18px;">${escapeHtml(runStats.deathBoss || 'Unknown')}</div><div class="statLabel">Boss</div></div>
                <div class="statBox"><div class="statValue" style="font-size:18px;">${escapeHtml(runStats.deathAttack || 'Unknown')}</div><div class="statLabel">Attack</div></div>
                <div class="statBox"><div class="statValue" style="font-size:18px;">${escapeHtml(runStats.deathStage || `Zone ${runStats.zone}`)}</div><div class="statLabel">Stage</div></div>
            </div>
            <div class="smallNote">${escapeHtml(quote)}</div>
        </div>
    `;
}

function damagePlayer(source={}) {
    if (player.invuln > 0 || (state !== 'playing' && state !== 'rush')) return;
    runStats.hits = (runStats.hits || 0) + 1;
    runStats.deathCause = source.cause || (state === 'rush' ? 'Rush collision' : 'Bullet');
    runStats.deathBoss = source.boss || (boss?.name || (rush ? 'Inferno Rush' : 'Unknown'));
    runStats.deathAttack = source.attack || currentAttackName || 'Unknown pattern';
    runStats.deathStage = source.stage || (rush ? `Inferno Rush ${rush.zone}` : (runStats.secretTrial ? 'God Trial' : `Zone ${runStats.zone}`));
    if (player.shields > 0) {
        player.shields -= 1;
        player.invuln = 1.25 + (mods.hitInvulnBonus || 0);
        addBurst(player.x, player.y, '#93c5fd', 26, 4.5, 1.2);
        playSfx('shield');
        addTextParticle(player.x, player.y - 22, 'Shield', '#bfdbfe', 0.8, 18);
        return;
    }
    player.lives -= 1;
    player.invuln = 1.6 + (mods.hitInvulnBonus || 0);
    addBurst(player.x, player.y, COLORS.red, 28, 5.5, 1.4);
    if (player.lives <= 0) {
        startDeathSequence();
    } else {
        playSfx('hit');
    }
}

function startDeathSequence() {
    if (state === 'death') return;
    reviveState = rush ? 'rush' : 'playing';
    state = 'death';
    deathTimer = 1.45;
    player.dead = true;
    player.invuln = 99;
    stopMusic();
    playSfx('destroy');
    screenFlash = 0.95;
    screenShake = 1.25;
    addTextParticle(W/2, H/2 - 38, 'SHIP DESTROYED', '#fff8ec', 1.35, 42);
    addTextParticle(W/2, H/2 + 8, 'Recovering signal...', '#fb7185', 1.2, 20);
    for (let i=0; i<180; i++) {
        const c = i % 3 === 0 ? '#fff8ec' : (i % 3 === 1 ? COLORS.red : player.ship.accent);
        addParticle(player.x, player.y, c, rand()*4+1.5, rand()*Math.PI*2, rand()*520+80, 1.0+rand()*0.8);
    }
}

function collectPickup(o) {
    if (o.type === 'coin') {
        const lowLife = player.lives <= 1 ? (1 + (mods.lowLifeCoinBonus || 0)) : 1;
        const magnetCoin = player.magnetPulse > 0 ? (1 + (mods.magnetPulseCoinBonus || 0)) : 1;
        const gained = Math.round(10 * mods.coinValue * lowLife * magnetCoin * (state === 'rush' ? (1 + (mods.rushCoinValue || 0)) : 1));
        runStats.coins += gained;
        if (modeConfig.overheat && runStats.heat !== null) {
            runStats.heat = Math.min(45, (runStats.heat || 0) + 1);
            addTextParticle(o.x, o.y - 14, '+1s', '#f97316', 0.55, 14);
        }
        const overchargeScore = player.overcharge > 0 ? (mods.overchargeCoinScore || 0) : 0;
        runStats.score += gained * (2 + (mods.coinScoreBonus || 0) + overchargeScore);
        addBurst(o.x, o.y, COLORS.coin, 8 + Math.round((mods.coinScoreBonus || 0) * 4), 2.5, 0.65);
        playSfx('coin');
    } else if (o.type === 'heart') {
        if (player.lives < player.maxLives) {
            player.lives += 1;
            runStats.hearts += 1;
            if (mods.heartCritCharge > 0) player.criticalCharges = Math.min(3 + (mods.maxCriticalCharges || 0), (player.criticalCharges || 0) + mods.heartCritCharge);
            runStats.score += (mods.heartScoreBonus || 0);
            addTextParticle(o.x, o.y, '+1 Life', COLORS.heart, 0.75, 16);
            if (modeConfig.overheat && mods.heatHeartBonus) runStats.heat = Math.min(45, (runStats.heat || 0) + mods.heatHeartBonus);
        } else {
            if (mods.heartShield > 0) {
                player.shields += mods.heartShield;
                player.nextBombBonus = (player.nextBombBonus || 0) + (mods.heartShieldBombBonus || 0);
                addTextParticle(o.x, o.y, `+${mods.heartShield} Shield`, '#bfdbfe', 0.75, 16);
            } else {
                runStats.score += 120;
                addTextParticle(o.x, o.y, 'Max', COLORS.heart, 0.65, 15);
            }
        }
        addBurst(o.x, o.y, COLORS.heart, 12, 3, 0.8);
        playSfx('heart');
    } else if (o.type === 'power_invuln') {
        const powerSeconds = INVULN_POWER_SECONDS + (mods.invulnBonus || 0);
        player.invuln = Math.max(player.invuln, powerSeconds);
        player.nextBombBonus = (player.nextBombBonus || 0) + (mods.invulnBombBonus || 0);
        if ((mods.powerShieldIfEmpty || 0) > 0 && (player.shields || 0) <= 0) player.shields += mods.powerShieldIfEmpty;
        runStats.powerups += 1;
        runStats.score += 250 + (mods.powerScoreBonus || 0);
        addBurst(o.x, o.y, COLORS.invuln, 24, 4.5, 1.0);
        if (mods.powerClearRadius > 0) clearBulletsNear(o.x, o.y, mods.powerClearRadius, COLORS.invuln);
        addTextParticle(o.x, o.y, 'Invulnerable', COLORS.invuln, 0.9, 18);
        playSfx('powerup');
    } else if (o.type === 'shield') {
        const alreadyShielded = (player.shields || 0) > 0;
        player.shields = Math.min(3, (player.shields || 0) + 1);
        player.nextBombBonus = (player.nextBombBonus || 0) + (mods.shieldBombBonus || 0) + (alreadyShielded ? (mods.extraShieldBombBonus || 0) : 0);
        runStats.shieldsPicked = (runStats.shieldsPicked || 0) + 1;
        runStats.score += 220 + (state === 'rush' ? Math.round((mods.rushShieldScore || 0) * 80) : 0);
        addBurst(o.x, o.y, COLORS.shield, 22, 3.7, 0.9);
        addTextParticle(o.x, o.y, '+1 Shield', COLORS.shield, 0.85, 18);
        playSfx('shield');
    } else if (o.type === 'time_fragment') {
        const gain = 5;
        if (modeConfig.overheat && runStats.heat !== null) {
            runStats.heat = Math.min(50, (runStats.heat || 0) + gain);
            runStats.coins += (mods.timeFragmentCoins || 0);
        }
        if (mods.timeFragmentShield > 0) player.shields = Math.min(3, (player.shields || 0) + mods.timeFragmentShield);
        if (mods.timeSlowPulse > 0) player.slowPulse = Math.max(player.slowPulse || 0, mods.timeSlowPulse);
        if (mods.timeLaserClear > 0) lasers = lasers.filter(l => l.warn <= 0);
        runStats.timeFragments = (runStats.timeFragments || 0) + 1;
        runStats.score += 260 + (mods.timeScoreBonus || 0);
        addBurst(o.x, o.y, COLORS.time, 22, 4.0, 0.9);
        addTextParticle(o.x, o.y, modeConfig.overheat ? `+${gain}s` : '+Score', COLORS.time, 0.8, 18);
        playSfx('powerup');
    } else if (o.type === 'magnet_pulse') {
        player.magnetPulse = Math.max(player.magnetPulse || 0, 5.0 + (state === 'rush' ? (mods.rushMagnetBonus || 0) : 0));
        runStats.magnetPulses = (runStats.magnetPulses || 0) + 1;
        runStats.score += 240;
        addBurst(o.x, o.y, COLORS.magnet, 26, 4.6, 1.0);
        addTextParticle(o.x, o.y, 'Magnet Pulse', COLORS.magnet, 0.9, 18);
        playSfx('powerup');
    } else if (o.type === 'risk_core') {
        const gained = 250 + (mods.riskCoinBonus || 0);
        runStats.coins += gained;
        runStats.score += 1200;
        player.nextBombBonus = (player.nextBombBonus || 0) + (mods.riskCoreBombBonus || 0);
        if (mods.riskReviveDiscount > 0) mods.reviveCost = Math.max(500, mods.reviveCost - mods.riskReviveDiscount);
        runStats.riskCores = (runStats.riskCores || 0) + 1;
        screenShake = Math.max(screenShake, 0.35);
        if (mods.riskCoreBurst > 0) {
            for (let i=0; i<8; i++) spawnShot(o.x, o.y, i*Math.PI/4, 92, 5.5, 'bullet', 'Risk Core burst');
        }
        addBurst(o.x, o.y, COLORS.risk, 38, 6.5, 1.05);
        addTextParticle(o.x, o.y, `+${gained} Coins`, COLORS.risk, 0.95, 20);
        playSfx('goldBomb');
    } else if (o.type === 'overcharge_cell') {
        player.overcharge = Math.max(player.overcharge || 0, 6.0 + (mods.overchargeDurationBonus || 0));
        player.invuln = Math.max(player.invuln || 0, 0.55);
        runStats.overcharges = (runStats.overcharges || 0) + 1;
        runStats.score += 360;
        addBurst(o.x, o.y, COLORS.overcharge, 32, 5.5, 1.0);
        addTextParticle(o.x, o.y, 'Overcharge', COLORS.overcharge, 0.9, 18);
        playSfx('powerup');
    } else if (o.type === 'crit_core') {
        player.criticalCharges = Math.min(3 + (mods.maxCriticalCharges || 0), (player.criticalCharges || 0) + 1);
        player.nextBombBonus = (player.nextBombBonus || 0) + (mods.critCoreDamageBonus || 0) + (player.lives <= 1 ? (mods.lowLifeCritDamage || 0) : 0);
        if (boss && mods.critCoreSkillDelay > 0) boss.skills.forEach(sk => sk.cooldownTimer += mods.critCoreSkillDelay);
        runStats.criticalCores = (runStats.criticalCores || 0) + 1;
        runStats.score += 260 + (player.lives <= 1 ? (mods.lowLifeCritScore || 0) : 0);
        addBurst(o.x, o.y, COLORS.crit, 26, 4.2, 1.0);
        addTextParticle(o.x, o.y, 'Next Bomb Critical', COLORS.crit, 0.9, 17);
        playSfx('crit');
    } else if (o.type === 'bomb_blue') {
        const forcedCrit = (player.criticalCharges || 0) > 0;
        if (forcedCrit) player.criticalCharges -= 1;
        player.lastBombForcedCrit = forcedCrit;
        hitBoss(mods.blueDamage, COLORS.blueBomb, 'blue', !!o.critical || forcedCrit, o.x, o.y);
    } else if (o.type === 'bomb_purple') {
        const forcedCrit = (player.criticalCharges || 0) > 0;
        if (forcedCrit) player.criticalCharges -= 1;
        player.lastBombForcedCrit = forcedCrit;
        hitBoss(mods.purpleDamage, COLORS.purpleBomb, 'purple', !!o.critical || forcedCrit, o.x, o.y);
    } else if (o.type === 'bomb_gold') {
        const forcedCrit = (player.criticalCharges || 0) > 0;
        if (forcedCrit) player.criticalCharges -= 1;
        player.lastBombForcedCrit = forcedCrit;
        hitBoss(mods.goldDamage, COLORS.goldBomb, 'gold', !!o.critical || forcedCrit, o.x, o.y);
    }
}

function clearBulletsNear(x, y, radius, color) {
    let cleared = 0;
    bullets = bullets.filter(b => {
        if (b.type === 'bullet' && dist(b.x, b.y, x, y) < radius) {
            cleared += 1;
            return false;
        }
        return true;
    });
    if (cleared > 0) {
        runStats.score += cleared * (8 + (mods.clearScoreBonus || 0));
        addBurst(x, y, color || '#fff8ec', Math.min(50, 10 + cleared), 3.8, 0.75);
        addTextParticle(x, y - 18, `Cleared ${cleared}`, color || '#fff8ec', 0.7, 15);
    }
}

function hitBoss(baseDmg, color, kind, critical=false, pickupX=null, pickupY=null) {
    if (!boss || boss.dead) return;
    const overchargeMult = player && player.overcharge > 0 ? 1.25 : 1;
    const forcedCrit = !!(player && player.lastBombForcedCrit);
    if (player) player.lastBombForcedCrit = false;
    const synergyRaw = (player?.nextBombBonus || 0)
        + (player?.magnetPulse > 0 ? (mods.magnetBombDamage || 0) : 0)
        + (player?.invuln > 0 ? (mods.invulnBombBonus || 0) : 0)
        + (player?.overcharge > 0 ? (mods.overchargeBonusFlat || 0) : 0)
        + (kind === 'gold' && player?.overcharge > 0 ? (mods.goldOverchargeBonus || 0) : 0)
        + (critical && kind === 'blue' ? (mods.blueCritBonus || 0) : 0)
        + (critical && forcedCrit ? (mods.forcedCritBonus || 0) : 0);
    const synergyBonus = clamp(Math.round(synergyRaw), 0, 12);
    if (player) player.nextBombBonus = 0;
    if (synergyBonus > 0 && runStats) runStats.synergyTriggers = (runStats.synergyTriggers || 0) + 1;
    if ((boss.shields || 0) > 0) {
        boss.shields -= 1;
        const pierceDmg = Math.max(1, Math.round((baseDmg + synergyBonus) * 0.35 * overchargeMult));
        boss.hp = Math.max(0, boss.hp - pierceDmg);
        boss.hitTimer = 0.24;
        runStats.bombs[kind] += 1;
        if (critical) runStats.critBombs += 1;
        runStats.score += 120 + pierceDmg * 40;
        addBurst(boss.x, boss.y, '#bfdbfe', 24, 4.5, 0.8);
        addTextParticle(boss.x, boss.y + boss.size + 12, `Shield Broken -${pierceDmg}%`, '#bfdbfe', 0.8, 18);
        playSfx('shield');
        if (mods.bombClearRadius > 0) clearBulletsNear(pickupX ?? player.x, pickupY ?? player.y, mods.bombClearRadius, color);
        if (boss.hp <= 0 && !boss.dead) {
            boss.dead = true;
            boss.deathTimer = 1.7;
            bullets = bullets.filter(o => o.type !== 'bullet');
            playSfx('bossDeath');
            for (let i=0; i<70; i++) addParticle(boss.x, boss.y, boss.color, rand()*7+2, rand()*Math.PI*2, rand()*210+70, 1.2 + rand()*0.9);
            addTextParticle(W/2, 220, `${boss.name} defeated`, '#fff8ec', 1.4, 28);
        }
        return;
    }
    const critBonus = critical ? Math.max(1, player.lives) + (mods.critBonus || 0) + (player.lives <= 1 ? (mods.lastStandCrit || 0) : 0) : 0;
    const dmg = Math.round((baseDmg + critBonus + synergyBonus) * overchargeMult);
    boss.hp = Math.max(0, boss.hp - dmg);
    boss.hitTimer = critical ? 0.32 : 0.22;
    runStats.bombs[kind] += 1;
    if (critical) runStats.critBombs += 1;
    runStats.score += Math.round(dmg * (critical ? 90 : 50) + mods.bombScore * 100);
    addBurst(boss.x, boss.y, critical ? COLORS.crit : color, critical ? 32 : (kind === 'gold' ? 34 : 18), critical ? 7 : (kind === 'gold' ? 8 : 4), critical ? 1.25 : 1.0);
    if (mods.bombClearRadius > 0) clearBulletsNear(pickupX ?? player.x, pickupY ?? player.y, mods.bombClearRadius, color);
    const txt = critical ? `CRIT -${dmg}%` : (synergyBonus > 0 ? `COMBO -${dmg}%` : `-${dmg}%`);
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

function specialItemChance(id) {
    if (!activeSpecialItems || !activeSpecialItems.includes(id)) return 0;
    const luck = mods.bombLuck * (modeConfig.dropMult || 1);
    const table = {
        shield: 0.25,
        power_invuln: 0.45,
        crit_core: 0.35 * (1 + (mods.critCoreLuck || 0)),
        magnet_pulse: 0.30,
        overcharge_cell: 0.22,
        time_fragment: modeConfig.overheat ? 0.80 : 0.35,
        risk_core: 0.08
    };
    return (table[id] || 0) * Math.max(0.65, Math.min(1.35, luck));
}
function projectileKind() {
    const luck = mods.bombLuck * (modeConfig.dropMult || 1);
    const pGold = 0.01 * luck;
    const pPurple = 1.00 * luck;
    const pBlue = 2.00 * luck;
    const pHeart = 0.45 + mods.heartBonus;
    const pCoin = modeConfig.overheat ? 9.0 : 7.0;
    const r = rand() * 100;
    let t = pGold;
    if (r < t) return 'bomb_gold';
    t += pPurple;
    if (r < t) return 'bomb_purple';
    t += pBlue;
    if (r < t) return 'bomb_blue';
    t += pHeart;
    if (r < t) return 'heart';

    const specials = (activeSpecialItems || []).filter(id => SPECIAL_ITEM_BY_ID[id]);
    for (const id of specials) {
        t += specialItemChance(id);
        if (r < t) return id;
    }
    t += pCoin;
    if (r < t) return 'coin';
    return 'bullet';
}

function spawnShot(x, y, angle, speed, radius=6, forceKind=null, attackLabel=null) {
    const kind = forceKind || projectileKind();
    if (!canSpawnKind(kind)) {
        if (kind === 'bullet' || !canSpawnKind('bullet')) return false;
        return spawnShot(x, y, angle, speed, radius, 'bullet', attackLabel);
    }
    const temporarySlow = player && player.slowPulse > 0 ? 0.88 : 1;
    let sp = speed * mods.bulletSlow * temporarySlow * (modeConfig.turbo ? clamp(1 + (runStats?.activeTime || 0) / 260, 1, 1.45) : 1);
    let r = radius;
    if (kind !== 'bullet') {
        sp *= 0.62;
        r = kind === 'bomb_gold' ? 13 : kind === 'bomb_purple' ? 11 : kind === 'bomb_blue' ? 10 : kind === 'heart' ? 10 : kind === 'power_invuln' ? 12 : kind === 'risk_core' ? 13 : kind === 'overcharge_cell' ? 12 : kind === 'shield' ? 11 : kind === 'time_fragment' ? 10 : kind === 'magnet_pulse' ? 11 : kind === 'crit_core' ? 11 : 8;
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
        source: boss ? boss.name : (rush ? 'Inferno Rush' : 'Unknown'),
        attack: attackLabel || currentAttackName || (rush ? 'Rush hazard' : 'Boss pattern'),
        wobble: rand() * Math.PI * 2,
        life: 0
    });
    return true;
}


function spawnLaser(x, y, w, h, warn=0.55, active=0.65, color='#ef4444', orientation='horizontal', vx=0, vy=0, attackLabel=null) {
    if (lasers.length >= OBJECT_CAPS.lasers) return false;
    lasers.push({x,y,w,h,warn,active,maxWarn:warn,maxActive:active,color,orientation,vx,vy,life:0,source:boss?boss.name:(rush?'Inferno Rush':'Unknown'),attack:attackLabel||currentAttackName||'Laser'});
    return true;
}

function updateLasers(dt) {
    const keep = [];
    for (const l of lasers) {
        l.life += dt;
        l.x += (l.vx || 0) * dt;
        l.y += (l.vy || 0) * dt;
        if (l.warn > 0) {
            l.warn -= dt;
        } else {
            l.active -= dt;
            if (rectCircleHit(l.x, l.y, l.w, l.h, player.x, player.y, player.r)) damagePlayer({cause:'Laser', attack:l.attack || 'Laser pattern', boss:l.source || (boss?.name || 'Inferno Rush')});
        }
        if (l.active > 0 && l.x > -120 && l.x < W+160 && l.y > -120 && l.y < H+160) keep.push(l);
    }
    lasers = keep;
}

function rectCircleHit(rx, ry, rw, rh, cx, cy, cr) {
    const nx = clamp(cx, rx, rx+rw);
    const ny = clamp(cy, ry, ry+rh);
    return dist(nx, ny, cx, cy) < cr;
}

function drawLasers() {
    for (const l of lasers) {
        ctx.save();
        if (l.warn > 0) {
            const pulse = 0.35 + Math.sin(elapsed*18)*0.18;
            ctx.globalAlpha = clamp(pulse + 0.18, 0.12, 0.72);
            ctx.strokeStyle = l.color;
            ctx.lineWidth = 3;
            ctx.setLineDash([14, 10]);
            ctx.strokeRect(l.x, l.y, l.w, l.h);
            ctx.setLineDash([]);
            ctx.fillStyle = hexToRgba(l.color, 0.08);
            ctx.fillRect(l.x, l.y, l.w, l.h);
        } else {
            const a = clamp(l.active / l.maxActive, 0, 1);
            ctx.globalAlpha = 0.88 * a + 0.2;
            ctx.shadowBlur = 26;
            ctx.shadowColor = l.color;
            ctx.fillStyle = hexToRgba(l.color, 0.62);
            ctx.fillRect(l.x, l.y, l.w, l.h);
            ctx.fillStyle = 'rgba(255,255,255,0.82)';
            if (l.w > l.h) ctx.fillRect(l.x, l.y + l.h*0.38, l.w, l.h*0.24);
            else ctx.fillRect(l.x + l.w*0.38, l.y, l.w*0.24, l.h);
        }
        ctx.restore();
    }
}

function bossAggro() {
    const phase = boss.hp < 35 ? 2 : boss.hp < 68 ? 1 : 0;
    return (1 + boss.zone * 0.18 + phase * 0.22) * modeIntensity();
}


function updateBossSkills(dt) {
    if (!boss || !boss.skills || boss.dead || boss.intro > 0) return;
    for (const sk of boss.skills) {
        sk.cooldownTimer = Math.max(0, sk.cooldownTimer - dt);
        if (sk.charges < sk.maxCharges) {
            sk.rechargeTimer -= dt;
            if (sk.rechargeTimer <= 0) {
                sk.charges += 1;
                sk.rechargeTimer = sk.recharge * (mods.bossSkillSlow || 1);
            }
        } else {
            sk.rechargeTimer = sk.recharge * (mods.bossSkillSlow || 1);
        }
        const chance = (sk.useChance || 0) * modeIntensity() * dt;
        if (sk.charges > 0 && sk.cooldownTimer <= 0 && rand() < chance) useBossSkill(sk);
    }
}
function useBossSkill(sk) {
    if (!boss || !sk || sk.charges <= 0) return false;
    if (sk.type === 'shield' && (boss.shields || 0) >= Math.min(OBJECT_CAPS.bossShields, sk.maxObjects || 1)) return false;
    sk.charges -= 1;
    sk.cooldownTimer = sk.cooldown || 1;
    sk.rechargeTimer = sk.recharge * (mods.bossSkillSlow || 1);
    currentAttackName = sk.name || sk.type;
    switch(sk.type) {
        case 'shield': {
            const before = boss.shields || 0;
            boss.shields = Math.min(Math.min(OBJECT_CAPS.bossShields, sk.maxObjects || 1), before + (sk.amount || 1));
            if (boss.shields > before) {
                addTextParticle(boss.x, boss.y + boss.size + 18, 'SHIELD', '#bfdbfe', 0.75, 17);
                addBurst(boss.x, boss.y, '#bfdbfe', 18, 3.2, 0.7);
                playSfx('shield');
            }
            break;
        }
        case 'laserTrap': maybeBossLaser(rand()<0.5?'vertical':'horizontal', 1, boss.accent || boss.color); break;
        case 'crossLaser': maybeBossLaser('cross', 1, boss.accent || boss.color); break;
        case 'webWall': spawnSkillWall(sk, '#f97316'); break;
        case 'fireWall': spawnSkillWall(sk, '#fb7185'); break;
        case 'coinStorm': fireCoinStorm(sk); break;
        case 'bulletRing': fireSkillRing(sk, 0, 1.0); break;
        case 'spiralBloom': fireSkillRing(sk, elapsed * 2.4, 0.85); break;
        case 'hammerShock': fireSkillHammer(sk); break;
        case 'solarRing': fireSkillRing(sk, elapsed * 1.2, 0.78); break;
        case 'stolenAttack': fireStolenAttack(); break;
        default: fireSkillRing(sk, 0, 0.9);
    }
    return true;
}
function spawnSkillWall(sk, color) {
    const gapY = 150 + rand()*(H-250);
    const gap = 110 - Math.min(25, boss.zone*4);
    spawnLaser(W+36, 110, 26, Math.max(0, gapY-gap/2-110), 0.14, 4.0, color, 'wall', -150-boss.zone*15, 0, sk.name);
    spawnLaser(W+36, gapY+gap/2, 26, Math.max(0, H-(gapY+gap/2)-24), 0.14, 4.0, color, 'wall', -150-boss.zone*15, 0, sk.name);
}
function fireCoinStorm(sk) {
    for (let i=0; i<(sk.amount || 5); i++) {
        const x = 50 + i*(W-100)/Math.max(1,(sk.amount||5)-1);
        spawnShot(x, -10, Math.PI/2 + (rand()-0.5)*0.12, 125 + boss.zone*16, 6.2, i%3===0 ? 'coin' : null, sk.name);
    }
}
function fireSkillRing(sk, rotate=0, speedMult=1) {
    const count = sk.amount || 10;
    const speed = (120 + boss.zone*22) * speedMult;
    for (let i=0;i<count;i++) spawnShot(boss.x, boss.y, rotate + i*Math.PI*2/count, speed, 5.8, null, sk.name);
}
function fireSkillHammer(sk) {
    const count = sk.amount || 8;
    for (let i=0;i<count;i++) {
        const a = Math.PI/2 + (i-(count-1)/2)*0.16;
        spawnShot(boss.x, boss.y+boss.size*0.35, a, 150 + boss.zone*20, 6.6, null, sk.name);
    }
    maybeBossLaser('horizontal', 0.75, '#f97316');
}
function fireStolenAttack() {
    const old = boss.archetype;
    const stolen = boss.stolenArchetype || ['drone','widow','reaper','maw','serpent','halo','engine','furnace','sun','tyrant'][Math.floor(rand()*10)];
    const oldName = currentAttackName;
    boss.archetype = stolen;
    currentAttackName = `Corrupted ${stolen}`;
    fireBossPattern(true);
    boss.archetype = old;
    currentAttackName = oldName;
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

    updateBossSkills(dt);
    boss.fireCooldown -= dt * modeIntensity();
    if (boss.fireCooldown <= 0 && boss.intro <= 0) {
        fireBossPattern();
        const ag = bossAggro();
        boss.fireCooldown = Math.max(0.16, (0.68 - boss.zone * 0.055) / ag);
    }
}


function maybeBossLaser(kind, chance, color=null) {
    if (!boss || rand() > chance) return;
    const warn = 0.48 + (mods.laserWarning || 0);
    const c = color || boss.accent || boss.color;
    if (kind === 'vertical') {
        const x = clamp(player.x + (rand()-0.5)*170, 35, W-55);
        spawnLaser(x, 100, 18 + boss.zone, H-125, warn, 0.52, c, 'vertical');
    } else if (kind === 'horizontal') {
        const y = clamp(player.y + (rand()-0.5)*145, 125, H-35);
        spawnLaser(0, y, W, 17 + boss.zone, warn, 0.52, c, 'horizontal');
    } else if (kind === 'cross') {
        spawnLaser(player.x-9, 105, 18, H-125, warn, 0.48, c, 'vertical');
        spawnLaser(0, player.y-9, W, 18, warn, 0.48, c, 'horizontal');
    }
}

function firePolygon(cx, cy, sides, radius, speed, rotate=0) {
    const pts = [];
    for (let i=0; i<sides; i++) pts.push({x:cx+Math.cos(rotate+i*Math.PI*2/sides)*radius, y:cy+Math.sin(rotate+i*Math.PI*2/sides)*radius});
    for (let i=0; i<sides; i++) {
        const a = Math.atan2(pts[i].y-cy, pts[i].x-cx);
        spawnShot(pts[i].x, pts[i].y, a, speed, 6.2);
    }
}

function fireBossPattern(fromSkill=false) {
    const attackNames = {
        drone:'Fan Burst', widow:'Scrap Web Pattern', reaper:'Golden Reaping', maw:'Vault Spit', serpent:'Void Spiral', halo:'Eclipse Ring',
        engine:'Heat Burst', furnace:'Forge Rain', sun:'Solar Supernova', tyrant:'Astral Geometry', astrael:'Divine Judgment'
    };
    if (!fromSkill) currentAttackName = attackNames[boss.archetype] || 'Boss pattern';
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
            maybeBossLaser('vertical', 0.16, '#7dd3fc');
            break;
        }
        case 'widow': {
            for (let side=-1; side<=1; side+=2) {
                for (let i=0; i<5+boss.zone; i++) {
                    const a = Math.PI/2 + side * (0.25 + i*0.11);
                    spawnShot(boss.x + side*28, boss.y+20, a, speed*0.96, 5.8);
                }
            }
            if (rand() < 0.28) {
                const gap = Math.floor(rand()*6);
                for (let i=0; i<8; i++) if (Math.abs(i-gap)>1) spawnLaser(40+i*(W-80)/7, 108, 10, H-135, 0.55+(mods.laserWarning||0), 0.45, boss.color, 'vertical');
            }
            break;
        }
        case 'reaper': {
            for (let i=0; i<9+boss.zone; i++) {
                const a = Math.PI/2 + Math.sin(elapsed*2+i)*0.7 + (i-(4+boss.zone/2))*0.055;
                spawnShot(boss.x + (i%2?22:-22), boss.y+28, a, speed*0.95, 6.2);
            }
            if (rand() < 0.22) for (let i=0;i<6;i++) spawnShot(70+i*(W-140)/5, -10, Math.PI/2, speed*0.72, 8, i%2 ? 'coin' : null);
            maybeBossLaser('horizontal', 0.14, '#fbbf24');
            break;
        }
        case 'maw': {
            for (let i=0; i<6+boss.zone; i++) {
                const x = 40 + rand()*(W-80);
                spawnShot(x, -10, Math.PI/2 + (rand()-0.5)*0.25, speed*0.78, 6.4);
            }
            if (rand() < 0.4) spawnShot(boss.x, boss.y+34, toPlayer, speed*1.2, 7.5);
            if (rand() < 0.18) firePolygon(boss.x, boss.y+20, 5, 38, speed*0.72, elapsed);
            break;
        }
        case 'serpent': {
            const base = elapsed * 2.4;
            for (let i=0; i<4+boss.zone; i++) {
                spawnShot(boss.x, boss.y+20, base + i*Math.PI*2/(4+boss.zone), speed*0.9, 5.8);
                spawnShot(boss.x, boss.y+20, -base + i*Math.PI*2/(4+boss.zone), speed*0.82, 5.8);
            }
            if (rand() < 0.18) {
                for (let i=0;i<3;i++) spawnShot(boss.x-70+i*70, boss.y+22, toPlayer + (i-1)*0.3, speed*1.25, 6.4);
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
            maybeBossLaser('cross', 0.16, '#818cf8');
            break;
        }
        case 'engine': {
            for (let burst=0; burst<2; burst++) {
                for (let i=0; i<6; i++) {
                    const a = toPlayer + (i-2.5)*0.13 + (burst?0.12:-0.12);
                    spawnShot(boss.x + (burst?30:-30), boss.y+25, a, speed*1.25, 5.4);
                }
            }
            maybeBossLaser('horizontal', 0.24, '#fb7185');
            break;
        }
        case 'furnace': {
            const gap = Math.floor(rand()*7);
            for (let i=0; i<11; i++) {
                if (Math.abs(i-gap) <= 1) continue;
                spawnShot(i*(W/10), -8, Math.PI/2, speed*0.88, 7);
            }
            for (let i=0; i<5; i++) spawnShot(boss.x, boss.y+32, Math.PI/2 + (i-2)*0.24, speed, 6.5);
            if (rand() < 0.22) firePolygon(boss.x, boss.y+20, 6, 50, speed*0.75, elapsed*0.7);
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
            maybeBossLaser('vertical', 0.20, '#facc15');
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
            if (rand() < 0.22) maybeBossLaser(rand()<0.5?'cross':'vertical', 1, '#f472b6');
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
            if (rand() < 0.24 + phase*0.05) maybeBossLaser(phase >= 3 ? 'cross' : (rand()<0.5?'vertical':'horizontal'), 1, '#facc15');
            if (phase >= 2 && rand() < 0.2) firePolygon(boss.x, boss.y, phase === 3 ? 8 : 5, 62, speed*0.7, elapsed*0.8);
            break;
        }
        default: {
            for (let i=0; i<nBase; i++) spawnShot(boss.x, boss.y, toPlayer + (i-nBase/2)*0.12, speed, 6);
        }
    }
}

function updatePlayer(dt) {
    if (!player || player.dead || (state !== 'playing' && state !== 'rush')) return;
    player.invuln = Math.max(0, player.invuln - dt);
    player.magnetPulse = Math.max(0, (player.magnetPulse || 0) - dt);
    player.overcharge = Math.max(0, (player.overcharge || 0) - dt);
    player.slowPulse = Math.max(0, (player.slowPulse || 0) - dt);
    const overchargeSpeed = player.overcharge > 0 ? 1.18 : 1;
    const smooth = clamp(dt * 9.5 * player.ship.speed * (mods.shipSpeed || 1) * overchargeSpeed, 0, 0.62);
    player.x = lerp(player.x, mouse.x, smooth);
    player.y = lerp(player.y, mouse.y, smooth);
    player.x = clamp(player.x, 18, W-18);
    player.y = clamp(player.y, 120, H-18);
    player.r = 10 * mods.hitbox;
}

function updateBullets(dt) {
    const keep = [];
    for (const o of bullets) {
        o.life += dt;
        o.rot += o.spin * dt;
        o.wobble += dt * 5;
        const isBombPickup = o.type === 'bomb_blue' || o.type === 'bomb_purple' || o.type === 'bomb_gold';
        const magnetRadius = (o.type !== 'bullet' ? mods.magnet : 0) + (isBombPickup ? (mods.bombMagnet || 0) : 0) + (o.type !== 'bullet' && player.magnetPulse > 0 ? 260 : 0);
        if (o.type !== 'bullet' && magnetRadius > 0) {
            const d = dist(o.x, o.y, player.x, player.y);
            if (d < magnetRadius && d > 1) {
                const pull = (1 - d/magnetRadius) * 380;
                o.vx += (player.x - o.x) / d * pull * dt;
                o.vy += (player.y - o.y) / d * pull * dt;
            }
        }
        if (o.type === 'bullet' && boss && (boss.archetype === 'serpent' || boss.archetype === 'halo')) {
            o.vx += Math.cos(o.wobble) * 6 * dt;
        }
        o.x += o.vx * dt;
        o.y += o.vy * dt;
        const pr = player.r;
        const hit = !player.dead && dist(o.x, o.y, player.x, player.y) < (o.r + pr);
        if (hit) {
            if (o.type === 'bullet') damagePlayer({cause:'Bullet', attack:o.attack || currentAttackName, boss:o.source || (boss?.name || 'Inferno Rush')});
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
    const zone = rush ? rush.zone : (runStats ? runStats.zone : 1);
    const grad = ctx.createRadialGradient(W/2, 80, 20, W/2, H/2, H);
    const bossColor = rush ? '#ff7a2f' : (boss ? boss.color : '#ff7a2f');
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
    ctx.fillText(rush ? 'INFERNO RUSH' : `ZONE ${zone}`, W/2, H/2 + 20);

    if (rush) {
        ctx.save();
        ctx.globalAlpha = 0.22;
        ctx.strokeStyle = '#ff7a2f';
        ctx.lineWidth = 2;
        for (let i=0;i<26;i++) {
            const yy = (i*37 + elapsed*260) % H;
            ctx.beginPath(); ctx.moveTo(W, yy); ctx.lineTo(0, yy - 90); ctx.stroke();
        }
        ctx.restore();
    }
}

function hexToRgba(hex, alpha) {
    const h = hex.replace('#','');
    const bigint = parseInt(h.length === 3 ? h.split('').map(c=>c+c).join('') : h, 16);
    const r = (bigint >> 16) & 255;
    const g = (bigint >> 8) & 255;
    const b = bigint & 255;
    return `rgba(${r},${g},${b},${alpha})`;
}


function drawRushUI() {
    if (!rush || !player) return;
    ctx.save();
    ctx.fillStyle = 'rgba(0,0,0,0.32)';
    roundRect(18, 14, W-36, 78, 16, true, false);
    const left = 32;
    ctx.textAlign = 'left';
    ctx.fillStyle = '#fff8ec';
    ctx.font = '900 22px Arial';
    ctx.fillText('INFERNO RUSH', left, 42);
    ctx.font = '12px Arial';
    ctx.fillStyle = 'rgba(247,247,251,0.65)';
    ctx.fillText(`Survive the warp after Zone ${rush.zone}`, left, 62);
    const barX = 250, barY = 30, barW = W - 410, barH = 14;
    const pct = clamp(rush.time / rush.duration, 0, 1);
    ctx.fillStyle = 'rgba(255,255,255,0.11)';
    roundRect(barX, barY, barW, barH, 8, true, false);
    ctx.fillStyle = '#ff7a2f';
    roundRect(barX, barY, barW*pct, barH, 8, true, false);
    ctx.textAlign = 'right';
    ctx.fillStyle = '#fff8ec';
    ctx.font = '900 15px Arial';
    ctx.fillText(`${Math.ceil(rush.duration - rush.time)}s`, W - 32, 40);
    ctx.font = '12px Arial';
    ctx.fillStyle = 'rgba(247,247,251,0.70)';
    ctx.fillText(`Coins ${runStats.coins}  Score ${runStats.score}`, W - 32, 61);
    ctx.textAlign = 'left';
    ctx.font = '900 13px Arial';
    ctx.fillStyle = '#fff8ec';
    ctx.fillText(`Lives ${'♥'.repeat(Math.max(0, player.lives))}`, left, 82);
    ctx.fillStyle = 'rgba(247,247,251,0.70)';
    ctx.fillText(` Shields ${player.shields}`, left+95, 82);
    if (player.invuln > 0) { ctx.fillStyle = COLORS.invuln; ctx.fillText(` Invulnerable ${player.invuln.toFixed(1)}s`, left+190, 82); }
    if ((player.nextBombBonus || 0) > 0) { ctx.fillStyle = COLORS.crit; ctx.fillText(` Combo +${Math.round(player.nextBombBonus)}%`, left+340, 82); }
    ctx.restore();
}

function drawUI() {
    if (!runStats) return;
    if (rush) return drawRushUI();
    if (!boss) return;
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
    const shieldTag = (boss.shields || 0) > 0 ? ` · Shields ${boss.shields}` : '';
    ctx.fillText(`HP ${Math.ceil(boss.hp)}%${shieldTag}`, W - 32, 38);
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
    const bossProg = modeConfig.survival ? ` Bosses ${runStats.bossesKilled}` : (runStats.secretTrial ? ` God Trial` : ` Bosses ${runStats.bossesKilled}/5`);
    ctx.fillText(`${bossProg} · ${modeConfig.short || 'Run'}`, x+505, y);
    if (modeConfig.overheat && runStats.heat !== null) {
        ctx.fillStyle = runStats.heat < 8 ? COLORS.red : '#f97316';
        ctx.fillText(` Heat ${Math.ceil(runStats.heat)}s`, x+690, y);
    }
    if (player.invuln > 0) {
        ctx.fillStyle = COLORS.invuln;
        ctx.fillText(` Invulnerable ${player.invuln.toFixed(1)}s`, modeConfig.overheat ? x+780 : x+610, y);
    }
    if ((player.nextBombBonus || 0) > 0) {
        ctx.fillStyle = COLORS.crit;
        ctx.fillText(` Combo +${Math.round(player.nextBombBonus)}%`, modeConfig.overheat ? x+895 : x+735, y);
    }
    if (boss.skills && boss.skills.length) {
        ctx.textAlign = 'right';
        ctx.fillStyle = 'rgba(247,247,251,0.60)';
        ctx.font = '11px Arial';
        const sk = boss.skills.slice(0,2).map(s => `${s.name}: ${s.charges}/${s.maxCharges}`).join('  ');
        ctx.fillText(sk, W-32, 103);
    }
    ctx.textAlign = 'right';
    ctx.fillStyle = 'rgba(247,247,251,0.70)';
    ctx.font = '900 13px Arial';
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
    if ((boss.shields || 0) > 0) drawBossShieldNodes(boss.shields, s, a);
    ctx.restore();
}
function drawBossShieldNodes(count, s, color) {
    ctx.save();
    ctx.shadowBlur = 18;
    ctx.shadowColor = '#bfdbfe';
    for (let i=0;i<count;i++) {
        const ang = elapsed*1.7 + i*Math.PI*2/count;
        const x = Math.cos(ang)*s*1.25;
        const y = Math.sin(ang)*s*0.85;
        ctx.fillStyle = '#bfdbfe';
        ctx.beginPath(); ctx.arc(x,y,8,0,Math.PI*2); ctx.fill();
        ctx.strokeStyle = 'rgba(255,255,255,0.85)'; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.arc(x,y,13,0,Math.PI*2); ctx.stroke();
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
        } else if (o.type === 'shield') {
            ctx.shadowBlur = 16; ctx.shadowColor = COLORS.shield;
            ctx.strokeStyle = COLORS.shield; ctx.lineWidth = 3;
            ctx.beginPath();
            for (let i=0;i<6;i++) { const a=-Math.PI/2+i*Math.PI*2/6; ctx.lineTo(Math.cos(a)*o.r, Math.sin(a)*o.r); }
            ctx.closePath(); ctx.stroke();
            ctx.fillStyle = hexToRgba(COLORS.shield, 0.35); ctx.fill();
        } else if (o.type === 'time_fragment') {
            ctx.shadowBlur = 16; ctx.shadowColor = COLORS.time;
            ctx.fillStyle = COLORS.time;
            ctx.beginPath(); ctx.moveTo(0,-o.r); ctx.lineTo(o.r*0.8,o.r); ctx.lineTo(-o.r*0.8,o.r); ctx.closePath(); ctx.fill();
            ctx.fillStyle = '#fff8ec'; ctx.fillRect(-2,-5,4,10);
        } else if (o.type === 'magnet_pulse') {
            ctx.shadowBlur = 18; ctx.shadowColor = COLORS.magnet;
            ctx.strokeStyle = COLORS.magnet; ctx.lineWidth = 4;
            ctx.beginPath(); ctx.arc(0,0,o.r,Math.PI*0.15,Math.PI*1.85); ctx.stroke();
            ctx.strokeStyle = '#fff8ec'; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(0,0,o.r*0.45,0,Math.PI*2); ctx.stroke();
        } else if (o.type === 'risk_core') {
            ctx.shadowBlur = 24; ctx.shadowColor = COLORS.risk;
            ctx.fillStyle = COLORS.risk;
            ctx.beginPath();
            for (let i=0;i<8;i++) { const rr = i%2 ? o.r*0.62 : o.r*1.15; const a=-Math.PI/2+i*Math.PI*2/8; ctx.lineTo(Math.cos(a)*rr, Math.sin(a)*rr); }
            ctx.closePath(); ctx.fill();
            ctx.strokeStyle = '#fff8ec'; ctx.lineWidth = 2; ctx.stroke();
        } else if (o.type === 'overcharge_cell') {
            ctx.shadowBlur = 18; ctx.shadowColor = COLORS.overcharge;
            ctx.fillStyle = COLORS.overcharge;
            ctx.beginPath(); ctx.moveTo(-o.r*0.25,-o.r); ctx.lineTo(o.r*0.45,-o.r*0.1); ctx.lineTo(o.r*0.05,-o.r*0.1); ctx.lineTo(o.r*0.35,o.r); ctx.lineTo(-o.r*0.45,0); ctx.lineTo(-o.r*0.05,0); ctx.closePath(); ctx.fill();
        } else if (o.type === 'crit_core') {
            ctx.shadowBlur = 22; ctx.shadowColor = COLORS.crit;
            ctx.fillStyle = COLORS.crit;
            ctx.beginPath();
            for (let i=0;i<4;i++) { const a=Math.PI/4+i*Math.PI/2; ctx.lineTo(Math.cos(a)*o.r*1.1, Math.sin(a)*o.r*1.1); }
            ctx.closePath(); ctx.fill();
            ctx.fillStyle = '#050511'; ctx.font = '900 10px Arial'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText('C',0,1);
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
    const shipImg = SHIP_IMAGES[player.ship.id];
    if (shipImg && shipImg.complete && shipImg.naturalWidth > 0) {
        const imgW = 44;
        const imgH = 44;
        ctx.save();
        ctx.shadowBlur = 18;
        ctx.shadowColor = shipAccent;
        ctx.drawImage(shipImg, -imgW/2, -imgH/2, imgW, imgH);
        ctx.restore();
        ctx.fillStyle = trail;
        ctx.shadowBlur = 12;
        ctx.shadowColor = trail;
        ctx.beginPath();
        ctx.moveTo(-5,17);
        ctx.lineTo(0,27+Math.sin(elapsed*28)*4);
        ctx.lineTo(5,17);
        ctx.fill();
    } else {
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
    }
    if (player.shields > 0) {
        ctx.strokeStyle = 'rgba(147,197,253,0.75)';
        ctx.lineWidth = 2;
        ctx.beginPath(); ctx.arc(0,0,24 + Math.sin(elapsed*5)*2,0,Math.PI*2); ctx.stroke();
    }
    if (player.magnetPulse > 0) {
        ctx.strokeStyle = hexToRgba(COLORS.magnet, 0.45);
        ctx.lineWidth = 2;
        ctx.beginPath(); ctx.arc(0,0,40 + Math.sin(elapsed*8)*4,0,Math.PI*2); ctx.stroke();
    }
    if (player.overcharge > 0) {
        ctx.strokeStyle = hexToRgba(COLORS.overcharge, 0.70);
        ctx.lineWidth = 3;
        ctx.beginPath(); ctx.arc(0,0,31 + Math.sin(elapsed*16)*3,0,Math.PI*2); ctx.stroke();
    }
    if ((player.criticalCharges || 0) > 0) {
        ctx.fillStyle = COLORS.crit;
        ctx.font = '900 12px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(`CRIT x${player.criticalCharges}`, 0, -34);
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
    if (!paused || (state !== 'playing' && state !== 'rush')) return;
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

function drawResumeCountdown() {
    if (resumeCountdown <= 0 || (state !== 'playing' && state !== 'rush')) return;
    ctx.save();
    ctx.fillStyle = 'rgba(0,0,0,0.38)';
    ctx.fillRect(0,0,W,H);
    const n = Math.ceil(resumeCountdown);
    ctx.textAlign = 'center';
    ctx.fillStyle = '#fff8ec';
    ctx.font = '900 90px Arial';
    ctx.fillText(n > 0 ? String(n) : 'GO', W/2, H/2);
    ctx.font = '18px Arial';
    ctx.fillStyle = 'rgba(247,247,251,0.72)';
    ctx.fillText('Get ready', W/2, H/2 + 48);
    ctx.restore();
}

function drawDeathOverlay() {
    if (state !== 'death') return;
    ctx.save();
    ctx.fillStyle = 'rgba(0,0,0,0.22)';
    ctx.fillRect(0,0,W,H);
    ctx.textAlign = 'center';
    ctx.fillStyle = '#fff8ec';
    ctx.font = '900 38px Arial';
    ctx.fillText('SHIP DESTROYED', W/2, H/2 - 78);
    ctx.font = '15px Arial';
    ctx.fillStyle = 'rgba(247,247,251,0.72)';
    ctx.fillText('Signal lost...', W/2, H/2 - 48);
    ctx.restore();
}


function drawScreenEffects() {
    if (screenFlash > 0) {
        ctx.save();
        ctx.globalAlpha = clamp(screenFlash, 0, 0.85);
        ctx.fillStyle = '#fff8ec';
        ctx.fillRect(0,0,W,H);
        ctx.restore();
    }
}

function updateMusicVolume(v) {
    musicVolume = clamp(Number(v) || 0, 0, 1);
    localStorage.setItem(VOLUME_KEY, String(musicVolume));
    if (currentMusic) currentMusic.volume = musicVolume;
}
function updateSfxVolume(v) {
    sfxVolume = clamp(Number(v) || 0, 0, 1);
    localStorage.setItem(SFX_VOLUME_KEY, String(sfxVolume));
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
    else if (state === 'rush' && currentMusic) currentMusic.play().catch(() => {});
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
        gain.gain.setValueAtTime(Math.max(0.0001, volume * (0.35 + sfxVolume * 1.45)), startAt);
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
        case 'runStart': playTone(180, 0.09, 'sawtooth', 0.040); playTone(420, 0.09, 'triangle', 0.030, 0.08); playTone(760, 0.12, 'sine', 0.024, 0.16); break;
        case 'godStart': playTone(90, 0.18, 'sawtooth', 0.060); playTone(220, 0.16, 'square', 0.040, 0.1); playTone(740, 0.18, 'triangle', 0.032, 0.24); break;
        case 'rushStart': playTone(140, 0.12, 'sawtooth', 0.050); playTone(500, 0.10, 'triangle', 0.035, 0.09); break;
        case 'rushClear': playTone(420, 0.08, 'triangle', 0.030); playTone(700, 0.08, 'sine', 0.026, 0.08); break;
        case 'countdown': playTone(420, 0.055, 'square', 0.034); break;
        case 'go': playTone(760, 0.075, 'triangle', 0.040); playTone(1040, 0.075, 'sine', 0.030, 0.05); break;
        default: playTone(500, 0.04, 'triangle', 0.018);
    }
}

document.addEventListener('click', (e) => {
    if (e.target.closest('button')) playSfx('click');
});

function update(dt) {
    screenFlash = Math.max(0, screenFlash - dt * 1.8);
    screenShake = Math.max(0, screenShake - dt * 1.5);
    if (state === 'death') {
        deathTimer -= dt;
        updateStars(dt * 0.4);
        updateParticles(dt);
        updateBullets(dt * 0.25);
        if (deathTimer <= 0) showGameOver();
        return;
    }
    if (resumeCountdown > 0 && (state === 'playing' || state === 'rush')) {
        const before = Math.ceil(resumeCountdown);
        resumeCountdown = Math.max(0, resumeCountdown - dt);
        if (Math.ceil(resumeCountdown) !== before && resumeCountdown > 0) playSfx('countdown');
        if (resumeCountdown === 0) playSfx('go');
        updateStars(dt * 0.7);
        updateParticles(dt * 0.6);
        return;
    }
    if ((state === 'playing' || state === 'rush') && !paused) {
        elapsed += dt;
        runStats.activeTime += dt;
        if (modeConfig.overheat && runStats.heat !== null) {
            runStats.heat -= dt;
            if (runStats.heat <= 0) {
                runStats.deathCause = 'Overheat';
                runStats.deathBoss = boss?.name || 'The timer';
                runStats.deathAttack = 'Heat reached zero';
                runStats.deathStage = rush ? `Inferno Rush ${rush.zone}` : `Zone ${runStats.zone}`;
                startDeathSequence();
                return;
            }
        }
        updateStars(dt * (state === 'rush' ? 2.4 : 1));
        updatePlayer(dt);
        if (state === 'playing') updateBoss(dt);
        if (state === 'rush') updateRush(dt);
        updateBullets(dt);
        updateLasers(dt);
        updateParticles(dt);
    } else {
        updateStars(dt * 0.5);
        updateParticles(dt * 0.5);
    }
}
function draw() {
    ctx.save();
    if (screenShake > 0) ctx.translate((rand()-0.5)*screenShake*14, (rand()-0.5)*screenShake*14);
    drawBackground();
    drawBoss();
    drawLasers();
    drawBullets();
    drawPlayer();
    drawParticles();
    drawUI();
    drawPause();
    drawResumeCountdown();
    drawDeathOverlay();
    ctx.restore();
    drawScreenEffects();
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
function togglePause() {
    if (state !== 'playing' && state !== 'rush') return;
    if (paused) {
        paused = false;
        resumeCountdown = 3.0;
        playSfx('countdown');
    } else {
        paused = true;
        resumeCountdown = 0;
        playSfx('pause');
    }
}

window.addEventListener('keydown', (e) => {
    if (e.key.toLowerCase() === 'p' && (state === 'playing' || state === 'rush')) togglePause();
    if (e.key === 'Escape' && (state === 'playing' || state === 'rush')) togglePause();
});

// Start with an empty scene behind the menu.
player = {x:W/2, y:H-90, lives:3, maxLives:3, shields:0, invuln:0, ship:SHIPS.nova, r:10, nextBombBonus:0, magnetPulse:0, overcharge:0, slowPulse:0, criticalCharges:0};
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

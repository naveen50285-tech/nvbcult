import os
import sys

def build_google_html():
    out_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Google</title>
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 48 48'%3E%3Cpath fill='%23EA4335' d='M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z'/%3E%3Cpath fill='%234285F4' d='M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z'/%3E%3Cpath fill='%23FBBC05' d='M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z'/%3E%3Cpath fill='%2334A853' d='M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z'/%3E%3C/svg%3E">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,300;0,400;0,500;0,700;1,400&family=Google+Sans:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #ffffff;
            --text-color: #202124;
            --muted-text: #70757a;
            --search-bg: #ffffff;
            --search-border: #dfe1e5;
            --search-hover-shadow: 0 1px 6px rgba(32,33,36,0.28);
            --btn-bg: #f8f9fa;
            --btn-color: #3c4043;
            --btn-border: #f8f9fa;
            --btn-hover-border: #dadce0;
            --btn-hover-bg: #f8f9fa;
            --footer-bg: #f2f2f2;
            --footer-text: #70757a;
            --footer-border: #dadce0;
            --link-blue: #1a0dab;
            --link-visited: #681da8;
            --snippet-gray: #4d5156;
            --card-border: #ebebeb;
            --active-tab-blue: #1a73e8;
            --waffle-hover: #f1f3f4;
            --dropdown-bg: #ffffff;
            --dropdown-hover: #f1f3f4;
            --modal-bg: #ffffff;
            --lens-border: #dadce0;
            --calc-btn: #f1f3f4;
            --calc-action: #dadce0;
            --calc-blue: #1a73e8;
        }

        body.dark-mode {
            --bg-color: #202124;
            --text-color: #e8eaed;
            --muted-text: #9aa0a6;
            --search-bg: #202124;
            --search-border: #5f6368;
            --search-hover-shadow: 0 1px 6px rgba(0,0,0,0.5);
            --btn-bg: #303134;
            --btn-color: #e8eaed;
            --btn-border: #303134;
            --btn-hover-border: #5f6368;
            --btn-hover-bg: #3c4043;
            --footer-bg: #171717;
            --footer-text: #9aa0a6;
            --footer-border: #3c4043;
            --link-blue: #8ab4f8;
            --link-visited: #c58af9;
            --snippet-gray: #bdc1c6;
            --card-border: #3c4043;
            --active-tab-blue: #8ab4f8;
            --waffle-hover: #303134;
            --dropdown-bg: #303134;
            --dropdown-hover: #3c4043;
            --modal-bg: #303134;
            --lens-border: #5f6368;
            --calc-btn: #3c4043;
            --calc-action: #5f6368;
            --calc-blue: #8ab4f8;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: Arial, sans-serif;
            font-size: 14px;
            color: var(--text-color);
            background-color: var(--bg-color);
            display: flex;
            flex-direction: column;
            min-height: 100vh;
            overflow-x: hidden;
            transition: background-color 0.2s, color 0.2s;
        }

        body.barrel-roll {
            animation: barrelRoll 1.5s cubic-bezier(0.25, 0.1, 0.25, 1);
        }
        @keyframes barrelRoll {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        body.askew {
            transform: rotate(1.5deg);
            transform-origin: top left;
        }

        a {
            color: inherit;
            text-decoration: none;
        }

        /* ==================== HOMEPAGE HEADER ==================== */
        .home-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 24px;
            height: 60px;
        }
        .home-header .left-links,
        .home-header .right-links {
            display: flex;
            align-items: center;
            gap: 16px;
        }
        .home-header a {
            font-size: 13px;
            color: var(--text-color);
            opacity: 0.87;
        }
        .home-header a:hover {
            text-decoration: underline;
            opacity: 1;
        }

        .icon-btn {
            background: none;
            border: none;
            cursor: pointer;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--text-color);
            transition: background-color 0.15s;
            position: relative;
        }
        .icon-btn:hover {
            background-color: var(--waffle-hover);
        }

        .user-avatar-btn {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: #1a73e8;
            color: #ffffff;
            font-weight: 500;
            font-size: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: none;
            cursor: pointer;
            box-shadow: 0 1px 2px rgba(0,0,0,0.2);
            transition: filter 0.15s;
        }
        .user-avatar-btn:hover {
            filter: brightness(0.92);
        }

        /* ==================== HOMEPAGE MAIN CONTENT ==================== */
        .home-main {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 0 20px 80px 20px;
        }

        .google-logo-wrapper {
            margin-bottom: 26px;
            text-align: center;
            user-select: none;
            cursor: pointer;
        }
        .google-logo-img {
            width: 272px;
            height: 92px;
            display: block;
        }
        .images-subtext {
            color: #4285f4;
            font-size: 16px;
            font-weight: 500;
            letter-spacing: -0.5px;
            margin-top: -6px;
            text-align: right;
            padding-right: 12px;
            display: none;
        }

        /* Search Pill Box */
        .search-pill-container {
            width: 100%;
            max-width: 584px;
            position: relative;
            margin-bottom: 28px;
            z-index: 100;
        }
        .search-pill {
            display: flex;
            align-items: center;
            height: 46px;
            background: var(--search-bg);
            border: 1px solid var(--search-border);
            border-radius: 24px;
            padding: 0 14px;
            transition: box-shadow 0.2s, border-color 0.2s;
        }
        .search-pill:hover,
        .search-pill.focused {
            box-shadow: var(--search-hover-shadow);
            border-color: transparent;
        }
        .search-pill.open-dropdown {
            border-bottom-left-radius: 0;
            border-bottom-right-radius: 0;
            border-bottom: 1px solid var(--card-border);
        }

        .search-icon {
            color: #9aa0a6;
            margin-right: 12px;
            display: flex;
            align-items: center;
        }
        .search-input {
            flex: 1;
            border: none;
            outline: none;
            background: transparent;
            font-size: 16px;
            color: var(--text-color);
            font-family: inherit;
        }

        .search-actions {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .action-icon {
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--muted-text);
            width: 28px;
            height: 28px;
            border-radius: 50%;
            transition: opacity 0.15s, transform 0.1s;
        }
        .action-icon:hover {
            opacity: 0.8;
            transform: scale(1.05);
        }
        .clear-btn {
            display: none;
            color: #70757a;
            border-right: 1px solid var(--card-border);
            padding-right: 10px;
            margin-right: -4px;
        }

        /* Autocomplete Suggestions */
        .suggestions-dropdown {
            position: absolute;
            top: 45px;
            left: 0;
            right: 0;
            background: var(--dropdown-bg);
            border: 1px solid transparent;
            border-top: none;
            border-bottom-left-radius: 24px;
            border-bottom-right-radius: 24px;
            box-shadow: var(--search-hover-shadow);
            display: none;
            overflow: hidden;
            padding-bottom: 12px;
        }
        .suggestion-item {
            display: flex;
            align-items: center;
            padding: 10px 18px;
            cursor: pointer;
            font-size: 15px;
            color: var(--text-color);
        }
        .suggestion-item:hover,
        .suggestion-item.active {
            background-color: var(--dropdown-hover);
        }
        .suggestion-item .item-icon {
            margin-right: 14px;
            color: #9aa0a6;
            display: flex;
            align-items: center;
        }
        .suggestion-item .item-text {
            flex: 1;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .suggestion-item .item-remove {
            color: #1a73e8;
            font-size: 12px;
            cursor: pointer;
            display: none;
        }
        .suggestion-item:hover .item-remove {
            display: block;
        }

        /* Buttons Row */
        .home-buttons {
            display: flex;
            gap: 12px;
            margin-bottom: 28px;
        }
        .btn-google {
            background-color: var(--btn-bg);
            color: var(--btn-color);
            border: 1px solid var(--btn-border);
            padding: 0 16px;
            height: 36px;
            border-radius: 4px;
            font-size: 14px;
            cursor: pointer;
            user-select: none;
            font-family: inherit;
            transition: border-color 0.15s, box-shadow 0.15s, background-color 0.15s;
        }
        .btn-google:hover {
            box-shadow: 0 1px 1px rgba(0,0,0,0.1);
            background-color: var(--btn-hover-bg);
            border-color: var(--btn-hover-border);
            color: var(--text-color);
        }

        /* Languages Strip */
        .home-languages {
            font-size: 13px;
            color: var(--muted-text);
            text-align: center;
        }
        .home-languages a {
            color: var(--link-blue);
            margin: 0 4px;
        }
        .home-languages a:hover {
            text-decoration: underline;
        }

        /* ==================== FOOTER ==================== */
        .google-footer {
            background: var(--footer-bg);
            color: var(--footer-text);
            font-size: 14px;
            border-top: 1px solid var(--footer-border);
        }
        .footer-location {
            padding: 15px 30px;
            border-bottom: 1px solid var(--footer-border);
            font-size: 15px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .footer-links-row {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            padding: 12px 30px;
        }
        .footer-links-group {
            display: flex;
            flex-wrap: wrap;
            gap: 24px;
        }
        .footer-links-row a {
            color: var(--footer-text);
        }
        .footer-links-row a:hover {
            text-decoration: underline;
        }

        /* ==================== SERP (RESULTS PAGE) ==================== */
        #serp-view {
            display: none;
            flex-direction: column;
            min-height: 100vh;
        }

        /* SERP Header */
        .serp-header {
            position: sticky;
            top: 0;
            background: var(--bg-color);
            z-index: 50;
            border-bottom: 1px solid var(--card-border);
            padding: 18px 24px 0 24px;
        }
        .serp-top-row {
            display: flex;
            align-items: center;
            gap: 28px;
            margin-bottom: 14px;
        }
        .serp-logo {
            cursor: pointer;
            user-select: none;
        }
        .serp-search-container {
            flex: 1;
            max-width: 692px;
            position: relative;
        }
        .serp-search-pill {
            display: flex;
            align-items: center;
            height: 44px;
            background: var(--search-bg);
            border-radius: 24px;
            box-shadow: 0 2px 5px 1px rgba(64,60,67,0.16);
            padding: 0 16px;
        }
        .serp-search-input {
            flex: 1;
            border: none;
            outline: none;
            background: transparent;
            font-size: 16px;
            color: var(--text-color);
            font-family: inherit;
        }
        .serp-search-tools {
            display: flex;
            align-items: center;
            gap: 12px;
            border-left: 1px solid var(--card-border);
            padding-left: 12px;
            margin-left: 8px;
        }
        .serp-right-actions {
            margin-left: auto;
            display: flex;
            align-items: center;
            gap: 16px;
        }

        /* SERP Tabs */
        .serp-tabs-bar {
            display: flex;
            align-items: center;
            margin-left: 148px;
            gap: 20px;
            font-size: 13px;
            color: var(--muted-text);
            user-select: none;
        }
        .serp-tab {
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 10px 4px 12px 4px;
            cursor: pointer;
            border-bottom: 3px solid transparent;
            font-weight: 500;
        }
        .serp-tab:hover {
            color: var(--text-color);
        }
        .serp-tab.active {
            color: var(--active-tab-blue);
            border-bottom-color: var(--active-tab-blue);
        }
        .serp-tools-btn {
            margin-left: auto;
            cursor: pointer;
            padding: 6px 12px;
            border-radius: 4px;
        }
        .serp-tools-btn:hover {
            background: var(--waffle-hover);
        }

        /* Filter Tools Bar */
        .serp-tools-drawer {
            display: none;
            margin-left: 148px;
            padding: 8px 0 12px 0;
            gap: 16px;
            font-size: 12px;
        }
        .tool-select {
            background: var(--btn-bg);
            color: var(--text-color);
            border: 1px solid var(--card-border);
            border-radius: 4px;
            padding: 4px 8px;
            outline: none;
            cursor: pointer;
        }

        /* SERP Content Area */
        .serp-content {
            flex: 1;
            padding: 12px 24px 60px 148px;
            max-width: 1280px;
        }
        .serp-stats {
            font-size: 14px;
            color: var(--muted-text);
            margin-bottom: 20px;
        }

        .serp-layout {
            display: flex;
            gap: 64px;
        }
        .serp-main-col {
            flex: 1;
            max-width: 652px;
        }
        .serp-sidebar-col {
            width: 368px;
        }

        /* Organic Result Card */
        .organic-result {
            margin-bottom: 32px;
        }
        .result-breadcrumb {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 12px;
            color: var(--text-color);
            margin-bottom: 4px;
        }
        .result-favicon {
            width: 18px;
            height: 18px;
            border-radius: 50%;
            background: #e8f0fe;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 11px;
            font-weight: 700;
            color: #1a73e8;
        }
        .result-url {
            color: var(--snippet-gray);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .result-title {
            font-size: 20px;
            line-height: 1.3;
            color: var(--link-blue);
            cursor: pointer;
            margin-bottom: 4px;
            font-family: 'Google Sans', Roboto, sans-serif;
            font-weight: 400;
        }
        .result-title:hover {
            text-decoration: underline;
        }
        .result-snippet {
            font-size: 14px;
            line-height: 1.58;
            color: var(--snippet-gray);
        }
        .sitelinks-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            margin-top: 14px;
            padding-left: 12px;
            border-left: 2px solid var(--card-border);
        }
        .sitelink-item a {
            font-size: 14px;
            color: var(--link-blue);
            font-weight: 500;
            display: block;
            margin-bottom: 2px;
        }
        .sitelink-item a:hover {
            text-decoration: underline;
        }
        .sitelink-snippet {
            font-size: 12px;
            color: var(--snippet-gray);
            line-height: 1.4;
        }

        /* Knowledge Graph Card */
        .knowledge-graph-card {
            border: 1px solid var(--card-border);
            border-radius: 8px;
            overflow: hidden;
            background: var(--bg-color);
        }
        .kg-header-img {
            width: 100%;
            height: 180px;
            object-fit: cover;
            display: block;
            background: #e0e0e0;
        }
        .kg-body {
            padding: 16px;
        }
        .kg-title {
            font-size: 24px;
            font-weight: 400;
            color: var(--text-color);
            font-family: 'Google Sans', Roboto, sans-serif;
        }
        .kg-subtitle {
            font-size: 14px;
            color: var(--muted-text);
            margin-bottom: 12px;
        }
        .kg-desc {
            font-size: 14px;
            line-height: 1.58;
            color: var(--text-color);
            margin-bottom: 16px;
        }
        .kg-desc a {
            color: var(--link-blue);
        }
        .kg-desc a:hover {
            text-decoration: underline;
        }
        .kg-facts {
            border-top: 1px solid var(--card-border);
            padding-top: 12px;
        }
        .kg-fact-row {
            margin-bottom: 8px;
            font-size: 13px;
            line-height: 1.5;
        }
        .kg-fact-row strong {
            color: var(--text-color);
            font-weight: 500;
        }

        /* People Also Ask (PAA) */
        .paa-card {
            border: 1px solid var(--card-border);
            border-radius: 8px;
            margin-bottom: 32px;
            overflow: hidden;
        }
        .paa-heading {
            padding: 14px 16px;
            font-size: 18px;
            font-weight: 500;
            border-bottom: 1px solid var(--card-border);
            font-family: 'Google Sans', Roboto, sans-serif;
        }
        .paa-item {
            border-bottom: 1px solid var(--card-border);
        }
        .paa-item:last-child {
            border-bottom: none;
        }
        .paa-question {
            padding: 14px 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
            font-size: 15px;
            color: var(--text-color);
            user-select: none;
        }
        .paa-question:hover {
            background-color: var(--dropdown-hover);
        }
        .paa-answer {
            display: none;
            padding: 12px 16px 16px 16px;
            font-size: 14px;
            line-height: 1.58;
            color: var(--snippet-gray);
            background: var(--bg-color);
        }

        /* Interactive Widgets */
        .interactive-widget-box {
            border: 1px solid var(--card-border);
            border-radius: 8px;
            padding: 18px;
            margin-bottom: 32px;
            background: var(--bg-color);
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        }

        /* Calculator Widget */
        .calc-display {
            background: var(--dropdown-bg);
            border: 1px solid var(--card-border);
            border-radius: 6px;
            padding: 12px 16px;
            text-align: right;
            margin-bottom: 14px;
        }
        .calc-history {
            font-size: 13px;
            color: var(--muted-text);
            min-height: 18px;
        }
        .calc-current {
            font-size: 28px;
            font-weight: 500;
            color: var(--text-color);
            font-family: 'Google Sans', monospace;
        }
        .calc-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 8px;
        }
        .calc-btn {
            height: 40px;
            border-radius: 4px;
            border: none;
            background: var(--calc-btn);
            color: var(--text-color);
            font-size: 15px;
            font-weight: 500;
            cursor: pointer;
            transition: filter 0.1s;
        }
        .calc-btn:hover {
            filter: brightness(0.92);
        }
        .calc-btn.action {
            background: var(--calc-action);
        }
        .calc-btn.equals {
            background: var(--calc-blue);
            color: #ffffff;
        }

        /* Flip Coin Widget */
        .coin-wrapper {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 16px 0;
        }
        .coin {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            background: linear-gradient(135deg, #ffd700, #ffa500);
            box-shadow: 0 4px 10px rgba(0,0,0,0.2), inset 0 0 10px rgba(255,255,255,0.6);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            font-weight: 700;
            color: #b8860b;
            margin-bottom: 16px;
            user-select: none;
            transition: transform 0.8s ease-out;
        }
        .coin.flipping {
            animation: flipAnimation 1.2s cubic-bezier(0.25, 0.1, 0.25, 1);
        }
        @keyframes flipAnimation {
            0% { transform: rotateY(0deg) scale(1); }
            50% { transform: rotateY(900deg) scale(1.2); }
            100% { transform: rotateY(1800deg) scale(1); }
        }

        /* Dice Widget */
        .dice-box {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 16px 0;
        }
        .dice {
            width: 80px;
            height: 80px;
            background: #ffffff;
            border: 2px solid #5f6368;
            border-radius: 12px;
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 36px;
            font-weight: 700;
            color: #1a73e8;
            margin-bottom: 16px;
            user-select: none;
        }
        .dice.rolling {
            animation: diceRoll 0.8s cubic-bezier(0.25, 0.1, 0.25, 1);
        }
        @keyframes diceRoll {
            0% { transform: rotate(0deg) scale(1); }
            50% { transform: rotate(360deg) scale(1.15); }
            100% { transform: rotate(720deg) scale(1); }
        }

        /* Timer / Stopwatch Widget */
        .timer-tabs {
            display: flex;
            border-bottom: 1px solid var(--card-border);
            margin-bottom: 16px;
        }
        .timer-tab {
            padding: 8px 16px;
            cursor: pointer;
            font-weight: 500;
            color: var(--muted-text);
            border-bottom: 2px solid transparent;
        }
        .timer-tab.active {
            color: var(--active-tab-blue);
            border-bottom-color: var(--active-tab-blue);
        }
        .timer-time {
            font-size: 48px;
            font-family: 'Google Sans', monospace;
            text-align: center;
            margin: 12px 0 20px 0;
            color: var(--text-color);
        }
        .timer-controls {
            display: flex;
            justify-content: center;
            gap: 12px;
        }

        /* Weather Widget */
        .weather-card {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .weather-left {
            display: flex;
            align-items: center;
            gap: 16px;
        }
        .weather-icon-lg {
            font-size: 48px;
        }
        .weather-temp {
            font-size: 46px;
            font-weight: 400;
            font-family: 'Google Sans', Roboto, sans-serif;
        }
        .weather-deg {
            font-size: 20px;
            color: var(--muted-text);
            vertical-align: super;
        }
        .weather-details {
            font-size: 13px;
            color: var(--muted-text);
            line-height: 1.6;
        }
        .forecast-row {
            display: flex;
            justify-content: space-between;
            margin-top: 16px;
            padding-top: 16px;
            border-top: 1px solid var(--card-border);
            text-align: center;
        }
        .forecast-day {
            font-size: 13px;
        }
        .forecast-icon {
            font-size: 22px;
            margin: 4px 0;
        }

        /* Images Tab Masonry Grid */
        .images-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
            gap: 16px;
            margin-top: 12px;
        }
        .image-card {
            border-radius: 8px;
            overflow: hidden;
            background: var(--card-border);
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .image-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        .image-card img {
            width: 100%;
            height: 140px;
            object-fit: cover;
            display: block;
        }
        .image-card-info {
            padding: 8px 10px;
            background: var(--bg-color);
        }
        .image-card-title {
            font-size: 12px;
            color: var(--text-color);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .image-card-source {
            font-size: 11px;
            color: var(--muted-text);
        }

        /* Videos Tab */
        .video-result {
            display: flex;
            gap: 16px;
            margin-bottom: 24px;
        }
        .video-thumb-wrapper {
            position: relative;
            width: 168px;
            height: 94px;
            border-radius: 8px;
            overflow: hidden;
            flex-shrink: 0;
        }
        .video-thumb-wrapper img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        .video-duration {
            position: absolute;
            bottom: 4px;
            right: 4px;
            background: rgba(0,0,0,0.8);
            color: #ffffff;
            font-size: 11px;
            font-weight: 500;
            padding: 1px 4px;
            border-radius: 2px;
        }
        .video-info .video-title {
            font-size: 17px;
            color: var(--link-blue);
            margin-bottom: 4px;
            cursor: pointer;
        }
        .video-info .video-meta {
            font-size: 13px;
            color: var(--muted-text);
            margin-bottom: 4px;
        }

        /* News Tab */
        .news-item {
            display: flex;
            justify-content: space-between;
            gap: 16px;
            padding-bottom: 20px;
            margin-bottom: 20px;
            border-bottom: 1px solid var(--card-border);
        }
        .news-publisher {
            font-size: 12px;
            color: var(--muted-text);
            margin-bottom: 4px;
            font-weight: 500;
        }
        .news-title {
            font-size: 18px;
            color: var(--link-blue);
            line-height: 1.4;
            cursor: pointer;
            margin-bottom: 6px;
        }
        .news-time {
            font-size: 12px;
            color: var(--muted-text);
        }
        .news-thumb {
            width: 100px;
            height: 70px;
            border-radius: 8px;
            object-fit: cover;
            flex-shrink: 0;
        }

        /* Maps Tab */
        .map-container {
            border: 1px solid var(--card-border);
            border-radius: 8px;
            overflow: hidden;
            background: #e8eaed;
            height: 400px;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .map-interactive-bg {
            width: 100%;
            height: 100%;
            object-fit: cover;
            filter: saturate(0.85);
        }
        .map-overlay-card {
            position: absolute;
            top: 20px;
            left: 20px;
            background: var(--bg-color);
            padding: 16px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            max-width: 280px;
        }

        /* Shopping Tab */
        .shopping-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
            gap: 16px;
        }
        .shop-card {
            border: 1px solid var(--card-border);
            border-radius: 8px;
            overflow: hidden;
            background: var(--bg-color);
            padding: 12px;
            cursor: pointer;
            transition: box-shadow 0.2s;
        }
        .shop-card:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.12);
        }
        .shop-card img {
            width: 100%;
            height: 140px;
            object-fit: contain;
            margin-bottom: 8px;
        }
        .shop-title {
            font-size: 13px;
            font-weight: 500;
            color: var(--text-color);
            margin-bottom: 4px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .shop-price {
            font-size: 15px;
            font-weight: 700;
            color: var(--text-color);
            margin-bottom: 4px;
        }
        .shop-store {
            font-size: 12px;
            color: var(--muted-text);
        }

        /* Related Searches Grid */
        .related-searches {
            margin-top: 40px;
            padding-top: 24px;
            border-top: 1px solid var(--card-border);
        }
        .related-heading {
            font-size: 18px;
            font-weight: 500;
            margin-bottom: 16px;
            font-family: 'Google Sans', Roboto, sans-serif;
        }
        .related-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
        }
        .related-chip {
            display: flex;
            align-items: center;
            gap: 12px;
            background: var(--btn-bg);
            border-radius: 20px;
            padding: 10px 16px;
            cursor: pointer;
            font-size: 14px;
            color: var(--text-color);
            transition: background 0.15s;
        }
        .related-chip:hover {
            background: var(--btn-hover-bg);
        }

        /* Gooooooogle Pagination */
        .google-pagination {
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 48px 0;
            gap: 8px;
            user-select: none;
        }
        .page-num {
            display: inline-flex;
            flex-direction: column;
            align-items: center;
            cursor: pointer;
            font-size: 13px;
            color: var(--link-blue);
        }
        .page-o {
            font-size: 26px;
            font-weight: 700;
            line-height: 1;
        }
        .page-num.active {
            color: var(--text-color);
            cursor: default;
        }

        /* ==================== MODALS & POPOVERS ==================== */
        /* Google Apps Waffle Popover */
        .apps-popover {
            position: absolute;
            top: 56px;
            right: 20px;
            width: 328px;
            max-height: 460px;
            background: var(--modal-bg);
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            border: 1px solid var(--card-border);
            padding: 16px 12px;
            display: none;
            overflow-y: auto;
            z-index: 1000;
        }
        .apps-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
            margin-bottom: 12px;
        }
        .app-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 10px 4px;
            border-radius: 8px;
            cursor: pointer;
            transition: background 0.15s;
            text-decoration: none;
            color: var(--text-color);
        }
        .app-item:hover {
            background: var(--waffle-hover);
        }
        .app-icon {
            width: 38px;
            height: 38px;
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .app-name {
            font-size: 12px;
            text-align: center;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 80px;
        }
        .apps-more-btn {
            display: block;
            text-align: center;
            padding: 8px;
            border: 1px solid var(--card-border);
            border-radius: 20px;
            color: var(--link-blue);
            font-size: 13px;
            font-weight: 500;
            cursor: pointer;
            margin-top: 8px;
        }
        .apps-more-btn:hover {
            background: var(--waffle-hover);
        }

        /* Account Popover */
        .account-popover {
            position: absolute;
            top: 56px;
            right: 20px;
            width: 340px;
            background: var(--modal-bg);
            border-radius: 16px;
            box-shadow: 0 4px 24px rgba(0,0,0,0.22);
            border: 1px solid var(--card-border);
            padding: 20px;
            display: none;
            z-index: 1000;
            text-align: center;
        }
        .acc-avatar-lg {
            width: 68px;
            height: 68px;
            border-radius: 50%;
            background: #1a73e8;
            color: #ffffff;
            font-size: 28px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 12px auto;
            font-weight: 500;
        }
        .acc-name {
            font-size: 17px;
            font-weight: 500;
            color: var(--text-color);
        }
        .acc-email {
            font-size: 13px;
            color: var(--muted-text);
            margin-bottom: 16px;
        }
        .acc-manage-btn {
            display: inline-block;
            border: 1px solid var(--card-border);
            border-radius: 20px;
            padding: 8px 20px;
            font-size: 13px;
            color: var(--text-color);
            margin-bottom: 20px;
            cursor: pointer;
        }
        .acc-manage-btn:hover {
            background: var(--waffle-hover);
        }
        .acc-footer-actions {
            border-top: 1px solid var(--card-border);
            padding-top: 14px;
            display: flex;
            justify-content: space-around;
            font-size: 13px;
            color: var(--text-color);
        }
        .acc-footer-actions span {
            cursor: pointer;
            padding: 6px 10px;
            border-radius: 4px;
        }
        .acc-footer-actions span:hover {
            background: var(--waffle-hover);
        }

        /* Settings Popover */
        .settings-popover {
            position: absolute;
            bottom: 48px;
            right: 30px;
            width: 220px;
            background: var(--modal-bg);
            border-radius: 8px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.2);
            border: 1px solid var(--card-border);
            padding: 8px 0;
            display: none;
            z-index: 1000;
        }
        .settings-item {
            padding: 10px 18px;
            font-size: 13px;
            color: var(--text-color);
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .settings-item:hover {
            background: var(--dropdown-hover);
        }

        /* Voice Search Modal Overlay */
        .voice-modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0,0,0,0.5);
            display: none;
            align-items: center;
            justify-content: center;
            z-index: 2000;
        }
        .voice-modal {
            background: var(--modal-bg);
            border-radius: 12px;
            padding: 36px 48px;
            width: 440px;
            text-align: center;
            position: relative;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }
        .voice-close-btn {
            position: absolute;
            top: 14px;
            right: 14px;
            background: none;
            border: none;
            cursor: pointer;
            font-size: 18px;
            color: var(--muted-text);
        }
        .voice-title {
            font-size: 22px;
            font-weight: 400;
            margin-bottom: 24px;
            color: var(--text-color);
            font-family: 'Google Sans', Roboto, sans-serif;
        }
        .voice-animation {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 12px;
            height: 60px;
            margin-bottom: 24px;
        }
        .v-dot {
            width: 14px;
            height: 14px;
            border-radius: 50%;
            animation: waveDot 1s infinite alternate;
        }
        .v-dot:nth-child(1) { background: #4285f4; animation-delay: 0s; }
        .v-dot:nth-child(2) { background: #ea4335; animation-delay: 0.2s; }
        .v-dot:nth-child(3) { background: #fbbc05; animation-delay: 0.4s; }
        .v-dot:nth-child(4) { background: #34a853; animation-delay: 0.6s; }
        @keyframes waveDot {
            0% { transform: translateY(12px) scale(0.8); }
            100% { transform: translateY(-12px) scale(1.3); }
        }
        .voice-subtext {
            font-size: 14px;
            color: var(--muted-text);
        }
        .voice-quick-prompts {
            margin-top: 18px;
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            justify-content: center;
        }
        .v-prompt {
            background: var(--btn-bg);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 6px 12px;
            font-size: 12px;
            cursor: pointer;
        }
        .v-prompt:hover {
            background: var(--btn-hover-bg);
        }

        /* Google Lens Modal */
        .lens-modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0,0,0,0.5);
            display: none;
            align-items: center;
            justify-content: center;
            z-index: 2000;
        }
        .lens-modal {
            background: var(--modal-bg);
            border-radius: 16px;
            padding: 32px;
            width: 520px;
            position: relative;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }
        .lens-drop-zone {
            border: 2px dashed var(--lens-border);
            border-radius: 12px;
            padding: 36px 20px;
            text-align: center;
            cursor: pointer;
            margin: 20px 0;
            transition: border-color 0.2s, background 0.2s;
        }
        .lens-drop-zone:hover {
            border-color: #1a73e8;
            background: rgba(26,115,232,0.04);
        }
        .lens-url-input-row {
            display: flex;
            gap: 8px;
        }
        .lens-url-input {
            flex: 1;
            padding: 10px 14px;
            border: 1px solid var(--card-border);
            border-radius: 20px;
            outline: none;
            background: transparent;
            color: var(--text-color);
            font-size: 14px;
        }

        /* Virtual Keyboard */
        .virtual-keyboard {
            position: fixed;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            background: #d1d5db;
            padding: 12px;
            border-top-left-radius: 12px;
            border-top-right-radius: 12px;
            box-shadow: 0 -4px 20px rgba(0,0,0,0.25);
            display: none;
            flex-direction: column;
            gap: 6px;
            z-index: 2000;
        }
        .keyboard-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 12px;
            font-weight: 500;
            color: #374151;
            margin-bottom: 4px;
            padding: 0 4px;
        }
        .kb-row {
            display: flex;
            gap: 6px;
            justify-content: center;
        }
        .kb-key {
            background: #ffffff;
            color: #111827;
            border: 1px solid #9ca3af;
            border-radius: 4px;
            min-width: 32px;
            height: 36px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 0 8px;
            user-select: none;
        }
        .kb-key:active {
            background: #e5e7eb;
        }
        .kb-key.wide {
            min-width: 60px;
        }
        .kb-key.space {
            min-width: 240px;
        }

        /* Responsive Breakpoints */
        @media (max-width: 900px) {
            .serp-layout {
                flex-direction: column-reverse;
                gap: 24px;
            }
            .serp-sidebar-col {
                width: 100%;
            }
            .serp-tabs-bar,
            .serp-tools-drawer,
            .serp-content {
                margin-left: 0;
                padding-left: 16px;
                padding-right: 16px;
            }
            .sitelinks-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>

    <!-- ==================== HOMEPAGE VIEW ==================== -->
    <div id="home-view" style="display: flex; flex-direction: column; min-height: 100vh;">
        <!-- Top Nav -->
        <header class="home-header">
            <div class="left-links">
                <a href="#" onclick="showInfoToast('Google About')">About</a>
                <a href="#" onclick="showInfoToast('Google Store')">Store</a>
            </div>
            <div class="right-links">
                <a href="https://mail.google.com" target="_blank">Gmail</a>
                <a href="#" onclick="activateTab('images')">Images</a>
                <button class="icon-btn" onclick="toggleAppsMenu(event)" title="Google apps">
                    <svg focusable="false" viewBox="0 0 24 24" width="24" height="24" fill="currentColor">
                        <path d="M6,8c1.1,0 2,-0.9 2,-2s-0.9,-2 -2,-2 -2,0.9 -2,2 0.9,2 2,2zM12,20c1.1,0 2,-0.9 2,-2s-0.9,-2 -2,-2 -2,0.9 -2,2 0.9,2 2,2zM6,20c1.1,0 2,-0.9 2,-2s-0.9,-2 -2,-2 -2,0.9 -2,2 0.9,2 2,2zM6,14c1.1,0 2,-0.9 2,-2s-0.9,-2 -2,-2 -2,0.9 -2,2 0.9,2 2,2zM12,14c1.1,0 2,-0.9 2,-2s-0.9,-2 -2,-2 -2,0.9 -2,2 0.9,2 2,2zM16,6c0,1.1 0.9,2 2,2s2,-0.9 2,-2 -0.9,-2 -2,-2 -2,0.9 -2,2zM12,8c1.1,0 2,-0.9 2,-2s-0.9,-2 -2,-2 -2,0.9 -2,2 0.9,2 2,2zM18,14c1.1,0 2,-0.9 2,-2s-0.9,-2 -2,-2 -2,0.9 -2,2 0.9,2 2,2zM18,20c1.1,0 2,-0.9 2,-2s-0.9,-2 -2,-2 -2,0.9 -2,2 0.9,2 2,2z"></path>
                    </svg>
                </button>
                <button class="user-avatar-btn" onclick="toggleAccountMenu(event)" title="Google Account: Karthick (karthick@gmail.com)">
                    K
                </button>
            </div>
        </header>

        <!-- Main Search Section -->
        <main class="home-main">
            <div class="google-logo-wrapper" onclick="goToHome()">
                <!-- Authentic Multi-Color Google SVG Logo -->
                <svg class="google-logo-img" viewBox="0 0 272 92" xmlns="http://www.w3.org/2000/svg">
                    <path fill="#4285F4" d="M115.75 47.18c0 12.77-9.99 22.18-22.25 22.18s-22.25-9.41-22.25-22.18C71.25 34.3 81.24 25 93.5 25s22.25 9.3 22.25 22.18zm-9.74 0c0-7.98-5.79-13.44-12.51-13.44S80.99 39.2 80.99 47.18c0 7.9 5.79 13.44 12.51 13.44s12.51-5.55 12.51-13.44z"/>
                    <path fill="#EA4335" d="M163.75 47.18c0 12.77-9.99 22.18-22.25 22.18s-22.25-9.41-22.25-22.18c0-12.87 9.99-22.18 22.25-22.18s22.25 9.3 22.25 22.18zm-9.74 0c0-7.98-5.79-13.44-12.51-13.44s-12.51 5.46-12.51 13.44c0 7.9 5.79 13.44 12.51 13.44s12.51-5.55 12.51-13.44z"/>
                    <path fill="#4285F4" d="M209.75 26.34v39.82c0 16.38-9.66 23.07-21.08 23.07-10.75 0-17.22-7.19-19.66-13.07l8.48-3.53c1.51 3.61 5.21 7.87 11.17 7.87 7.31 0 11.84-4.51 11.84-13v-3.19h-.34c-2.18 2.69-6.38 5.04-11.68 5.04-11.09 0-21.25-9.66-21.25-22.09 0-12.52 10.16-22.26 21.25-22.26 5.29 0 9.49 2.35 11.68 4.96h.34v-3.61h9.45zm-8.82 20.92c0-7.81-5.21-13.52-11.84-13.52-6.72 0-12.35 5.71-12.35 13.52 0 7.73 5.63 13.36 12.35 13.36 6.63 0 11.84-5.63 11.84-13.36z"/>
                    <path fill="#FBBC05" d="M45.5 39.2v8.57h20.84c-.84 4.54-4.71 13.36-20.84 13.36-14.03 0-25.54-11.6-25.54-25.88s11.51-25.88 25.54-25.88c7.98 0 13.36 3.44 16.47 6.47l6.72-6.55C68.91 4.7 60.17 0 45.5 0 20.33 0 0 20.33 0 45.5S20.33 91 45.5 91c26.22 0 43.61-18.4 43.61-44.45 0-3.03-.34-5.38-.76-7.35H45.5z"/>
                    <path fill="#34A853" d="M222.5 4.5h9.74v63.87h-9.74z"/>
                    <path fill="#EA4335" d="M260.67 36.42l7.73 5.13c-2.52 3.69-8.57 10.08-18.99 10.08-12.77 0-22.01-9.91-22.01-22.18 0-13.11 9.41-22.18 21.08-22.18 11.84 0 17.56 9.24 19.49 14.11l1.01 2.6-28.73 11.93c2.27 4.45 5.79 6.72 10.75 6.72 4.96 0 8.32-2.44 10.67-6.21zm-19.49-8.48l19.16-7.98c-1.09-2.77-4.37-4.7-8.32-4.7-4.95 0-10.08 4.37-10.84 12.68z"/>
                </svg>
                <div class="images-subtext" id="home-images-badge">images</div>
            </div>

            <!-- Search Bar Pill -->
            <div class="search-pill-container" id="search-container">
                <div class="search-pill" id="search-pill">
                    <div class="search-icon">
                        <svg focusable="false" viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
                            <path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"></path>
                        </svg>
                    </div>
                    <input type="text" class="search-input" id="main-search-input" autocomplete="off" spellcheck="false" autofocus>
                    <div class="search-actions">
                        <div class="action-icon clear-btn" id="clear-btn" title="Clear">
                            <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
                                <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
                            </svg>
                        </div>
                        <div class="action-icon" onclick="toggleVirtualKeyboard()" title="Screen Keyboard">
                            <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
                                <path d="M20 5H4c-1.1 0-1.99.9-1.99 2L2 17c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm-9 3h2v2h-2V8zm0 3h2v2h-2v-2zM8 8h2v2H8V8zm0 3h2v2H8v-2zm-1 2H5v-2h2v2zm0-3H5V8h2v2zm9 7H8v-2h8v2zm0-4h-2v-2h2v2zm0-3h-2V8h2v2zm3 3h-2v-2h2v2zm0-3h-2V8h2v2z"/>
                            </svg>
                        </div>
                        <div class="action-icon" onclick="openVoiceSearch()" title="Search by voice">
                            <svg viewBox="0 0 24 24" width="22" height="22">
                                <path fill="#4285f4" d="m12 15c1.66 0 3-1.34 3-3v-6c0-1.66-1.34-3-3-3s-3 1.34-3 3v6c0 1.66 1.34 3 3 3z"/>
                                <path fill="#34a853" d="m11 18.92h2v3h-2z"/>
                                <path fill="#fbbc05" d="m7.05 13.87-1.42 1.41c1.64 1.65 3.9 2.68 6.37 2.68v-2c-1.92 0-3.68-.78-4.95-2.09z"/>
                                <path fill="#ea4335" d="m19 12h-2c0 2.76-2.24 5-5 5v2c3.87 0 7-3.13 7-7z"/>
                            </svg>
                        </div>
                        <div class="action-icon" onclick="openLensModal()" title="Search by image">
                            <svg viewBox="0 0 24 24" width="22" height="22">
                                <path fill="#4285f4" d="M12 10.5a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3z"/>
                                <path fill="#ea4335" d="M15.5 4H14l-1.5-1.5h-5L6 4H4.5A2.5 2.5 0 0 0 2 6.5v11A2.5 2.5 0 0 0 4.5 20h11a2.5 2.5 0 0 0 2.5-2.5v-11A2.5 2.5 0 0 0 15.5 4zM12 15a4.5 4.5 0 1 1 0-9 4.5 4.5 0 0 1 0 9z"/>
                                <path fill="#fbbc05" d="M12 7.5a3 3 0 1 0 0 6 3 3 0 0 0 0-6z"/>
                                <path fill="#34a853" d="M18 6.5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0z"/>
                            </svg>
                        </div>
                    </div>
                </div>

                <!-- Autocomplete Dropdown -->
                <div class="suggestions-dropdown" id="suggestions-box"></div>
            </div>

            <!-- Home Buttons -->
            <div class="home-buttons">
                <button class="btn-google" onclick="performSearch()">Google Search</button>
                <button class="btn-google" id="lucky-btn" onclick="handleLucky()">I'm Feeling Lucky</button>
            </div>

            <!-- Language Offerings -->
            <div class="home-languages">
                Google offered in: 
                <a href="#" onclick="setSearchLanguage('hi')">हिन्दी</a>
                <a href="#" onclick="setSearchLanguage('bn')">বাংলা</a>
                <a href="#" onclick="setSearchLanguage('te')">తెలుగు</a>
                <a href="#" onclick="setSearchLanguage('mr')">मराठी</a>
                <a href="#" onclick="setSearchLanguage('ta')">தமிழ்</a>
                <a href="#" onclick="setSearchLanguage('gu')">ગુજરાતી</a>
                <a href="#" onclick="setSearchLanguage('kn')">ಕನ್ನಡ</a>
                <a href="#" onclick="setSearchLanguage('ml')">മലയാളം</a>
                <a href="#" onclick="setSearchLanguage('pa')">ਪੰਜਾਬੀ</a>
            </div>
        </main>

        <!-- Footer -->
        <footer class="google-footer">
            <div class="footer-location">
                <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
                    <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
                </svg>
                <span>India</span> • <span>From your IP address</span> • <a href="#" style="color:var(--footer-text)">Update location</a>
            </div>
            <div class="footer-links-row">
                <div class="footer-links-group">
                    <a href="https://about.google/" target="_blank">About</a>
                    <a href="https://ads.google.com/" target="_blank">Advertising</a>
                    <a href="https://www.google.com/services/" target="_blank">Business</a>
                    <a href="https://google.com/search/howsearchworks/" target="_blank">How Search works</a>
                </div>
                <div class="footer-links-group">
                    <a href="https://policies.google.com/privacy" target="_blank">Privacy</a>
                    <a href="https://policies.google.com/terms" target="_blank">Terms</a>
                    <a href="#" onclick="toggleSettingsMenu(event)">Settings</a>
                </div>
            </div>
        </footer>
    </div>

    <!-- ==================== SERP (RESULTS PAGE) VIEW ==================== -->
    <div id="serp-view">
        <header class="serp-header">
            <div class="serp-top-row">
                <div class="serp-logo" onclick="goToHome()">
                    <svg width="92" height="30" viewBox="0 0 272 92" xmlns="http://www.w3.org/2000/svg">
                        <path fill="#4285F4" d="M115.75 47.18c0 12.77-9.99 22.18-22.25 22.18s-22.25-9.41-22.25-22.18C71.25 34.3 81.24 25 93.5 25s22.25 9.3 22.25 22.18zm-9.74 0c0-7.98-5.79-13.44-12.51-13.44S80.99 39.2 80.99 47.18c0 7.9 5.79 13.44 12.51 13.44s12.51-5.55 12.51-13.44z"/>
                        <path fill="#EA4335" d="M163.75 47.18c0 12.77-9.99 22.18-22.25 22.18s-22.25-9.41-22.25-22.18c0-12.87 9.99-22.18 22.25-22.18s22.25 9.3 22.25 22.18zm-9.74 0c0-7.98-5.79-13.44-12.51-13.44s-12.51 5.46-12.51 13.44c0 7.9 5.79 13.44 12.51 13.44s12.51-5.55 12.51-13.44z"/>
                        <path fill="#4285F4" d="M209.75 26.34v39.82c0 16.38-9.66 23.07-21.08 23.07-10.75 0-17.22-7.19-19.66-13.07l8.48-3.53c1.51 3.61 5.21 7.87 11.17 7.87 7.31 0 11.84-4.51 11.84-13v-3.19h-.34c-2.18 2.69-6.38 5.04-11.68 5.04-11.09 0-21.25-9.66-21.25-22.09 0-12.52 10.16-22.26 21.25-22.26 5.29 0 9.49 2.35 11.68 4.96h.34v-3.61h9.45zm-8.82 20.92c0-7.81-5.21-13.52-11.84-13.52-6.72 0-12.35 5.71-12.35 13.52 0 7.73 5.63 13.36 12.35 13.36 6.63 0 11.84-5.63 11.84-13.36z"/>
                        <path fill="#FBBC05" d="M45.5 39.2v8.57h20.84c-.84 4.54-4.71 13.36-20.84 13.36-14.03 0-25.54-11.6-25.54-25.88s11.51-25.88 25.54-25.88c7.98 0 13.36 3.44 16.47 6.47l6.72-6.55C68.91 4.7 60.17 0 45.5 0 20.33 0 0 20.33 0 45.5S20.33 91 45.5 91c26.22 0 43.61-18.4 43.61-44.45 0-3.03-.34-5.38-.76-7.35H45.5z"/>
                        <path fill="#34A853" d="M222.5 4.5h9.74v63.87h-9.74z"/>
                        <path fill="#EA4335" d="M260.67 36.42l7.73 5.13c-2.52 3.69-8.57 10.08-18.99 10.08-12.77 0-22.01-9.91-22.01-22.18 0-13.11 9.41-22.18 21.08-22.18 11.84 0 17.56 9.24 19.49 14.11l1.01 2.6-28.73 11.93c2.27 4.45 5.79 6.72 10.75 6.72 4.96 0 8.32-2.44 10.67-6.21zm-19.49-8.48l19.16-7.98c-1.09-2.77-4.37-4.7-8.32-4.7-4.95 0-10.08 4.37-10.84 12.68z"/>
                    </svg>
                </div>
                <div class="serp-search-container">
                    <div class="serp-search-pill">
                        <input type="text" class="serp-search-input" id="serp-search-input" autocomplete="off">
                        <div class="action-icon" id="serp-clear-btn" style="display:none;" onclick="clearSerpInput()">
                            <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
                                <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
                            </svg>
                        </div>
                        <div class="serp-search-tools">
                            <div class="action-icon" onclick="openVoiceSearch()" title="Search by voice">
                                <svg viewBox="0 0 24 24" width="20" height="20">
                                    <path fill="#4285f4" d="m12 15c1.66 0 3-1.34 3-3v-6c0-1.66-1.34-3-3-3s-3 1.34-3 3v6c0 1.66 1.34 3 3 3z"/>
                                    <path fill="#34a853" d="m11 18.92h2v3h-2z"/>
                                    <path fill="#fbbc05" d="m7.05 13.87-1.42 1.41c1.64 1.65 3.9 2.68 6.37 2.68v-2c-1.92 0-3.68-.78-4.95-2.09z"/>
                                    <path fill="#ea4335" d="m19 12h-2c0 2.76-2.24 5-5 5v2c3.87 0 7-3.13 7-7z"/>
                                </svg>
                            </div>
                            <div class="action-icon" onclick="openLensModal()" title="Search by image">
                                <svg viewBox="0 0 24 24" width="20" height="20">
                                    <path fill="#4285f4" d="M12 10.5a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3z"/>
                                    <path fill="#ea4335" d="M15.5 4H14l-1.5-1.5h-5L6 4H4.5A2.5 2.5 0 0 0 2 6.5v11A2.5 2.5 0 0 0 4.5 20h11a2.5 2.5 0 0 0 2.5-2.5v-11A2.5 2.5 0 0 0 15.5 4zM12 15a4.5 4.5 0 1 1 0-9 4.5 4.5 0 0 1 0 9z"/>
                                    <path fill="#fbbc05" d="M12 7.5a3 3 0 1 0 0 6 3 3 0 0 0 0-6z"/>
                                    <path fill="#34a853" d="M18 6.5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0z"/>
                                </svg>
                            </div>
                            <div class="action-icon" onclick="performSerpSearch()" title="Search" style="color:#4285f4">
                                <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
                                    <path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"></path>
                                </svg>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="serp-right-actions">
                    <button class="icon-btn" onclick="toggleSettingsMenu(event)" title="Quick settings">
                        <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
                            <path d="M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.09.63-.09.94s.02.64.07.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z"/>
                        </svg>
                    </button>
                    <button class="icon-btn" onclick="toggleAppsMenu(event)" title="Google apps">
                        <svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor">
                            <path d="M6,8c1.1,0 2,-0.9 2,-2s-0.9,-2 -2,-2 -2,0.9 -2,2 0.9,2 2,2zM12,20c1.1,0 2,-0.9 2,-2s-0.9,-2 -2,-2 -2,0.9 -2,2 0.9,2 2,2zM6,20c1.1,0 2,-0.9 2,-2s-0.9,-2 -2,-2 -2,0.9 -2,2 0.9,2 2,2zM6,14c1.1,0 2,-0.9 2,-2s-0.9,-2 -2,-2 -2,0.9 -2,2 0.9,2 2,2zM12,14c1.1,0 2,-0.9 2,-2s-0.9,-2 -2,-2 -2,0.9 -2,2 0.9,2 2,2zM16,6c0,1.1 0.9,2 2,2s2,-0.9 2,-2 -0.9,-2 -2,-2 -2,0.9 -2,2zM12,8c1.1,0 2,-0.9 2,-2s-0.9,-2 -2,-2 -2,0.9 -2,2 0.9,2 2,2zM18,14c1.1,0 2,-0.9 2,-2s-0.9,-2 -2,-2 -2,0.9 -2,2 0.9,2 2,2zM18,20c1.1,0 2,-0.9 2,-2s-0.9,-2 -2,-2 -2,0.9 -2,2 0.9,2 2,2z"></path>
                        </svg>
                    </button>
                    <button class="user-avatar-btn" onclick="toggleAccountMenu(event)" title="Google Account: Karthick (karthick@gmail.com)">
                        K
                    </button>
                </div>
            </div>

            <!-- SERP Tabs Navigation -->
            <div class="serp-tabs-bar">
                <div class="serp-tab active" data-tab="all" onclick="switchSerpTab('all')">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
                        <path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
                    </svg>
                    All
                </div>
                <div class="serp-tab" data-tab="images" onclick="switchSerpTab('images')">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
                        <path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/>
                    </svg>
                    Images
                </div>
                <div class="serp-tab" data-tab="videos" onclick="switchSerpTab('videos')">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
                        <path d="M10 8.64L15.27 12 10 15.36V8.64M8 5v14l11-7L8 5z"/>
                    </svg>
                    Videos
                </div>
                <div class="serp-tab" data-tab="news" onclick="switchSerpTab('news')">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
                        <path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm-5 14H4v-4h11v4zm0-5H4V9h11v4zm5 5h-4V9h4v9z"/>
                    </svg>
                    News
                </div>
                <div class="serp-tab" data-tab="maps" onclick="switchSerpTab('maps')">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
                        <path d="M20.5 3l-.16.03L15 5.1 9 3 3.36 4.9c-.21.07-.36.25-.36.48V20.5c0 .28.22.5.5.5l.16-.03L9 18.9l6 2.1 5.64-1.9c.21-.07.36-.25.36-.48V3.5c0-.28-.22-.5-.5-.5zM15 19l-6-2.11V5l6 2.11V19z"/>
                    </svg>
                    Maps
                </div>
                <div class="serp-tab" data-tab="shopping" onclick="switchSerpTab('shopping')">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
                        <path d="M18 6h-2c0-2.21-1.79-4-4-4S8 3.79 8 6H6c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm-6-2c1.1 0 2 .9 2 2h-4c0-1.1.9-2 2-2zm6 16H6V8h2v2c0 .55.45 1 1 1s1-.45 1-1V8h4v2c0 .55.45 1 1 1s1-.45 1-1V8h2v12z"/>
                    </svg>
                    Shopping
                </div>
                <div class="serp-tools-btn" onclick="toggleSerpTools()">Tools</div>
            </div>

            <!-- Tools Filter Drawer -->
            <div class="serp-tools-drawer" id="tools-drawer">
                <select class="tool-select" onchange="filterTime(this.value)">
                    <option value="any">Any time</option>
                    <option value="h">Past hour</option>
                    <option value="d">Past 24 hours</option>
                    <option value="w">Past week</option>
                    <option value="m">Past month</option>
                    <option value="y">Past year</option>
                </select>
                <select class="tool-select" onchange="filterVerbatim(this.value)">
                    <option value="all">All results</option>
                    <option value="verbatim">Verbatim</option>
                </select>
            </div>
        </header>

        <!-- SERP Content -->
        <div class="serp-content">
            <div class="serp-stats" id="serp-stats">About 3,420,000,000 results (0.34 seconds)</div>

            <div class="serp-layout">
                <!-- Main Results Column -->
                <div class="serp-main-col">
                    <!-- Dynamic Interactive Widget Box (Calculator, Dice, Coin, Timer, Weather) -->
                    <div id="interactive-widget-container"></div>

                    <!-- Main Dynamic Results Container -->
                    <div id="results-container"></div>

                    <!-- Related Searches -->
                    <div class="related-searches" id="related-box" style="display:none;">
                        <h3 class="related-heading">Related searches</h3>
                        <div class="related-grid" id="related-grid"></div>
                    </div>

                    <!-- Pagination -->
                    <div class="google-pagination" id="pagination-box" style="display:none;">
                        <div class="page-num active">
                            <span class="page-o" style="color:#4285f4">G</span>
                            <span>1</span>
                        </div>
                        <div class="page-num" onclick="showPage(2)">
                            <span class="page-o" style="color:#ea4335">o</span>
                            <span>2</span>
                        </div>
                        <div class="page-num" onclick="showPage(3)">
                            <span class="page-o" style="color:#fbbc05">o</span>
                            <span>3</span>
                        </div>
                        <div class="page-num" onclick="showPage(4)">
                            <span class="page-o" style="color:#4285f4">o</span>
                            <span>4</span>
                        </div>
                        <div class="page-num" onclick="showPage(5)">
                            <span class="page-o" style="color:#34a853">o</span>
                            <span>5</span>
                        </div>
                        <div class="page-num" onclick="showPage(6)">
                            <span class="page-o" style="color:#ea4335">gle</span>
                            <span>Next</span>
                        </div>
                    </div>
                </div>

                <!-- Right Sidebar Knowledge Graph -->
                <div class="serp-sidebar-col" id="sidebar-col">
                    <div id="knowledge-graph-container"></div>
                </div>
            </div>
        </div>

        <!-- SERP Footer -->
        <footer class="google-footer">
            <div class="footer-location">
                <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
                    <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
                </svg>
                <span>India</span> • <span>From your IP address</span> • <a href="#" style="color:var(--footer-text)">Update location</a>
            </div>
            <div class="footer-links-row">
                <div class="footer-links-group">
                    <a href="#" onclick="showInfoToast('Search Help')">Help</a>
                    <a href="#" onclick="showInfoToast('Send Feedback')">Send feedback</a>
                    <a href="https://policies.google.com/privacy" target="_blank">Privacy</a>
                    <a href="https://policies.google.com/terms" target="_blank">Terms</a>
                </div>
            </div>
        </footer>
    </div>

    <!-- ==================== APPS WAFFLE POPOVER ==================== -->
    <div class="apps-popover" id="apps-popover">
        <div class="apps-grid">
            <a class="app-item" href="#" onclick="launchApp('Google Account')">
                <div class="app-icon"><svg viewBox="0 0 48 48" width="34" height="34"><circle cx="24" cy="24" r="20" fill="#1a73e8"/><path fill="#fff" d="M24 21a5 5 0 1 0 0-10 5 5 0 0 0 0 10zm0 4c-5.33 0-16 2.67-16 8v3h32v-3c0-5.33-10.67-8-16-8z"/></svg></div>
                <div class="app-name">Account</div>
            </a>
            <a class="app-item" href="#" onclick="goToHome()">
                <div class="app-icon"><svg viewBox="0 0 48 48" width="34" height="34"><path fill="#4285F4" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/><path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/><path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/><path fill="#EA4335" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/></svg></div>
                <div class="app-name">Search</div>
            </a>
            <a class="app-item" href="#" onclick="launchApp('Google Maps')">
                <div class="app-icon"><svg viewBox="0 0 48 48" width="34" height="34"><path fill="#4285F4" d="M24 4C14.06 4 6 12.06 6 22c0 13.5 18 22 18 22s18-8.5 18-22c0-9.94-8.06-18-18-18z"/><circle cx="24" cy="22" r="7" fill="#fff"/></svg></div>
                <div class="app-name">Maps</div>
            </a>
            <a class="app-item" href="https://www.youtube.com" target="_blank">
                <div class="app-icon"><svg viewBox="0 0 48 48" width="34" height="34"><path fill="#FF0000" d="M43.2 13.7c-.5-1.9-2-3.4-3.9-3.9C35.9 9 24 9 24 9s-11.9 0-15.3.8c-1.9.5-3.4 2-3.9 3.9C4 17.1 4 24 4 24s0 6.9.8 10.3c.5 1.9 2 3.4 3.9 3.9 3.4.8 15.3.8 15.3.8s11.9 0 15.3-.8c1.9-.5 3.4-2 3.9-3.9.8-3.4.8-10.3.8-10.3s0-6.9-.8-10.3z"/><polygon fill="#fff" points="20,30 30,24 20,18"/></svg></div>
                <div class="app-name">YouTube</div>
            </a>
            <a class="app-item" href="https://news.google.com" target="_blank">
                <div class="app-icon"><svg viewBox="0 0 48 48" width="34" height="34"><rect width="36" height="28" x="6" y="10" rx="4" fill="#4285F4"/><path fill="#fff" d="M14 16h20v4H14zm0 8h20v2H14zm0 4h12v2H14z"/></svg></div>
                <div class="app-name">News</div>
            </a>
            <a class="app-item" href="https://mail.google.com" target="_blank">
                <div class="app-icon"><svg viewBox="0 0 48 48" width="34" height="34"><path fill="#EA4335" d="M6 10h36v28H6z"/><path fill="#4285F4" d="M6 10l18 14L42 10z"/><path fill="#FBBC05" d="M6 38l14-14-14-10z"/><path fill="#34A853" d="M42 38L28 24l14-10z"/></svg></div>
                <div class="app-name">Gmail</div>
            </a>
            <a class="app-item" href="#" onclick="launchApp('Google Meet')">
                <div class="app-icon"><svg viewBox="0 0 48 48" width="34" height="34"><rect width="24" height="20" x="6" y="14" rx="3" fill="#00832d"/><polygon fill="#00ac47" points="30,20 42,12 42,36 30,28"/></svg></div>
                <div class="app-name">Meet</div>
            </a>
            <a class="app-item" href="#" onclick="launchApp('Google Drive')">
                <div class="app-icon"><svg viewBox="0 0 48 48" width="34" height="34"><path fill="#FFC107" d="M17 6h14l11 19H28z"/><path fill="#4CAF50" d="M6 25l6-10 16 27H14z"/><path fill="#2196F3" d="M28 34l6 10H8l6-10z"/></svg></div>
                <div class="app-name">Drive</div>
            </a>
            <a class="app-item" href="#" onclick="launchApp('Google Calendar')">
                <div class="app-icon"><svg viewBox="0 0 48 48" width="34" height="34"><rect width="36" height="36" x="6" y="6" rx="4" fill="#4285F4"/><rect width="36" height="10" x="6" y="6" rx="4" fill="#1976D2"/><text x="24" y="32" font-size="16" font-family="Google Sans, sans-serif" font-weight="bold" fill="#fff" text-anchor="middle">31</text></svg></div>
                <div class="app-name">Calendar</div>
            </a>
            <a class="app-item" href="https://translate.google.com" target="_blank">
                <div class="app-icon"><svg viewBox="0 0 48 48" width="34" height="34"><path fill="#4285F4" d="M6 8h36v32H6z"/><text x="18" y="28" font-size="16" font-weight="bold" fill="#fff">G</text><text x="30" y="30" font-size="16" font-weight="bold" fill="#fff">文</text></svg></div>
                <div class="app-name">Translate</div>
            </a>
            <a class="app-item" href="#" onclick="launchApp('Google Photos')">
                <div class="app-icon"><svg viewBox="0 0 48 48" width="34" height="34"><path fill="#EA4335" d="M24 14a10 10 0 0 1 10 10h-10z"/><path fill="#FBBC05" d="M34 24a10 10 0 0 1-10 10V24z"/><path fill="#34A853" d="M24 34a10 10 0 0 1-10-10h10z"/><path fill="#4285F4" d="M14 24a10 10 0 0 1 10-10v10z"/></svg></div>
                <div class="app-name">Photos</div>
            </a>
            <a class="app-item" href="#" onclick="launchApp('Gemini AI')">
                <div class="app-icon"><svg viewBox="0 0 48 48" width="34" height="34"><path fill="#1a73e8" d="M24 4C24 15.05 15.05 24 4 24c11.05 0 20 8.95 20 20 0-11.05 8.95-20 20-20-11.05 0-20-8.95-20-20z"/></svg></div>
                <div class="app-name">Gemini</div>
            </a>
        </div>
        <div class="apps-more-btn" onclick="showInfoToast('More from Google')">More from Google</div>
    </div>

    <!-- ==================== ACCOUNT POPOVER ==================== -->
    <div class="account-popover" id="account-popover">
        <div class="acc-avatar-lg">K</div>
        <div class="acc-name">Karthick</div>
        <div class="acc-email">karthick@gmail.com</div>
        <div class="acc-manage-btn" onclick="showInfoToast('Manage Google Account')">Manage your Google Account</div>
        <div class="acc-footer-actions">
            <span onclick="showInfoToast('Add account')">+ Add account</span>
            <span onclick="showInfoToast('Signed out')">Sign out</span>
        </div>
    </div>

    <!-- ==================== SETTINGS POPOVER ==================== -->
    <div class="settings-popover" id="settings-popover">
        <div class="settings-item" onclick="toggleDarkMode()">
            <span>Dark theme</span>
            <strong id="dark-theme-status">Off</strong>
        </div>
        <div class="settings-item" onclick="showInfoToast('Search settings')">Search settings</div>
        <div class="settings-item" onclick="showInfoToast('Advanced search')">Advanced search</div>
        <div class="settings-item" onclick="showInfoToast('Your data in Search')">Your data in Search</div>
        <div class="settings-item" onclick="showInfoToast('Search history')">Search history</div>
        <div class="settings-item" onclick="showInfoToast('Search help')">Search help</div>
    </div>

    <!-- ==================== VOICE SEARCH MODAL ==================== -->
    <div class="voice-modal-overlay" id="voice-modal" onclick="closeVoiceSearch(event)">
        <div class="voice-modal" onclick="event.stopPropagation()">
            <button class="voice-close-btn" onclick="closeVoiceModal()">&times;</button>
            <div class="voice-title" id="voice-title">Listening...</div>
            <div class="voice-animation">
                <div class="v-dot"></div>
                <div class="v-dot"></div>
                <div class="v-dot"></div>
                <div class="v-dot"></div>
            </div>
            <div class="voice-subtext" id="voice-transcript">Say something like "Weather today" or "Python 3.13"</div>
            <div class="voice-quick-prompts">
                <div class="v-prompt" onclick="simulateVoiceQuery('Google')">"Google"</div>
                <div class="v-prompt" onclick="simulateVoiceQuery('Weather today')">"Weather today"</div>
                <div class="v-prompt" onclick="simulateVoiceQuery('Calculator')">"Calculator"</div>
                <div class="v-prompt" onclick="simulateVoiceQuery('Do a barrel roll')">"Do a barrel roll"</div>
            </div>
        </div>
    </div>

    <!-- ==================== GOOGLE LENS MODAL ==================== -->
    <div class="lens-modal-overlay" id="lens-modal" onclick="closeLensModal(event)">
        <div class="lens-modal" onclick="event.stopPropagation()">
            <button class="voice-close-btn" onclick="closeLensModal()">&times;</button>
            <h3 style="font-size: 20px; font-weight: 500; margin-bottom: 8px;">Search any image with Google Lens</h3>
            <p style="font-size: 13px; color: var(--muted-text);">Drag an image here or upload a file</p>
            
            <div class="lens-drop-zone" onclick="document.getElementById('lens-file-input').click()">
                <svg viewBox="0 0 24 24" width="48" height="48" style="margin-bottom: 12px;">
                    <path fill="#4285f4" d="M12 10.5a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3z"/>
                    <path fill="#ea4335" d="M15.5 4H14l-1.5-1.5h-5L6 4H4.5A2.5 2.5 0 0 0 2 6.5v11A2.5 2.5 0 0 0 4.5 20h11a2.5 2.5 0 0 0 2.5-2.5v-11A2.5 2.5 0 0 0 15.5 4zM12 15a4.5 4.5 0 1 1 0-9 4.5 4.5 0 0 1 0 9z"/>
                    <path fill="#fbbc05" d="M12 7.5a3 3 0 1 0 0 6 3 3 0 0 0 0-6z"/>
                    <path fill="#34a853" d="M18 6.5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0z"/>
                </svg>
                <div style="font-size: 14px; font-weight: 500; color: #1a73e8;">Upload a file</div>
                <input type="file" id="lens-file-input" style="display:none;" onchange="handleLensFile(event)" accept="image/*">
            </div>

            <div style="display: flex; align-items: center; gap: 12px; margin: 16px 0; color: var(--muted-text); font-size: 13px;">
                <div style="flex:1; height:1px; background:var(--card-border)"></div>
                <span>OR</span>
                <div style="flex:1; height:1px; background:var(--card-border)"></div>
            </div>

            <div class="lens-url-input-row">
                <input type="text" class="lens-url-input" id="lens-url-input" placeholder="Paste image link" onkeydown="if(event.key==='Enter') searchLensUrl()">
                <button class="btn-google" style="border-radius: 20px; padding: 0 16px;" onclick="searchLensUrl()">Search</button>
            </div>
        </div>
    </div>

    <!-- ==================== VIRTUAL KEYBOARD ==================== -->
    <div class="virtual-keyboard" id="virtual-keyboard">
        <div class="keyboard-header">
            <span>Virtual Keyboard (Google English)</span>
            <span style="cursor:pointer;" onclick="toggleVirtualKeyboard()">&times;</span>
        </div>
        <div class="kb-row">
            <button class="kb-key" onclick="kbPress('q')">q</button>
            <button class="kb-key" onclick="kbPress('w')">w</button>
            <button class="kb-key" onclick="kbPress('e')">e</button>
            <button class="kb-key" onclick="kbPress('r')">r</button>
            <button class="kb-key" onclick="kbPress('t')">t</button>
            <button class="kb-key" onclick="kbPress('y')">y</button>
            <button class="kb-key" onclick="kbPress('u')">u</button>
            <button class="kb-key" onclick="kbPress('i')">i</button>
            <button class="kb-key" onclick="kbPress('o')">o</button>
            <button class="kb-key" onclick="kbPress('p')">p</button>
            <button class="kb-key wide" onclick="kbBackspace()">Bksp</button>
        </div>
        <div class="kb-row">
            <button class="kb-key" onclick="kbPress('a')">a</button>
            <button class="kb-key" onclick="kbPress('s')">s</button>
            <button class="kb-key" onclick="kbPress('d')">d</button>
            <button class="kb-key" onclick="kbPress('f')">f</button>
            <button class="kb-key" onclick="kbPress('g')">g</button>
            <button class="kb-key" onclick="kbPress('h')">h</button>
            <button class="kb-key" onclick="kbPress('j')">j</button>
            <button class="kb-key" onclick="kbPress('k')">k</button>
            <button class="kb-key" onclick="kbPress('l')">l</button>
            <button class="kb-key wide" onclick="performSearch()">Enter</button>
        </div>
        <div class="kb-row">
            <button class="kb-key" onclick="kbPress('z')">z</button>
            <button class="kb-key" onclick="kbPress('x')">x</button>
            <button class="kb-key" onclick="kbPress('c')">c</button>
            <button class="kb-key" onclick="kbPress('v')">v</button>
            <button class="kb-key" onclick="kbPress('b')">b</button>
            <button class="kb-key" onclick="kbPress('n')">n</button>
            <button class="kb-key" onclick="kbPress('m')">m</button>
            <button class="kb-key" onclick="kbPress('.')">.</button>
            <button class="kb-key" onclick="kbPress('-')">-</button>
        </div>
        <div class="kb-row">
            <button class="kb-key space" onclick="kbPress(' ')">Space</button>
        </div>
    </div>

    <!-- ==================== JAVASCRIPT LOGIC ==================== -->
    <script>
        // State
        let currentQuery = "";
        let currentTab = "all";
        let activeSuggestionIndex = -1;
        let suggestionsList = [];
        let timerInterval = null;
        let timerSeconds = 300;
        let stopwatchInterval = null;
        let stopwatchMs = 0;
        let luckyIndex = 0;
        const luckyPhrases = [
            "I'm Feeling Lucky",
            "I'm Feeling Doodly",
            "I'm Feeling Artistic",
            "I'm Feeling Curious",
            "I'm Feeling Trendy",
            "I'm Feeling Playful",
            "I'm Feeling Stellar"
        ];

        // Elements
        const homeView = document.getElementById("home-view");
        const serpView = document.getElementById("serp-view");
        const mainInput = document.getElementById("main-search-input");
        const serpInput = document.getElementById("serp-search-input");
        const clearBtn = document.getElementById("clear-btn");
        const serpClearBtn = document.getElementById("serp-clear-btn");
        const searchPill = document.getElementById("search-pill");
        const suggestionsBox = document.getElementById("suggestions-box");
        const resultsContainer = document.getElementById("results-container");
        const widgetContainer = document.getElementById("interactive-widget-container");
        const kgContainer = document.getElementById("knowledge-graph-container");
        const luckyBtn = document.getElementById("lucky-btn");

        // Initialization
        window.addEventListener("DOMContentLoaded", () => {
            // Check Dark Mode
            if (localStorage.getItem("google_dark_theme") === "true") {
                document.body.classList.add("dark-mode");
                document.getElementById("dark-theme-status").innerText = "On";
            }

            // Check URL Params
            const params = new URLSearchParams(window.location.search);
            const q = params.get("q");
            const tab = params.get("tab") || "all";
            if (q) {
                mainInput.value = q;
                serpInput.value = q;
                triggerSearch(q, tab);
            } else {
                mainInput.focus();
            }

            // Lucky Button Hover effect
            luckyBtn.addEventListener("mouseenter", () => {
                luckyIndex = (luckyIndex + 1) % luckyPhrases.length;
                luckyBtn.innerText = luckyPhrases[luckyIndex];
            });
            luckyBtn.addEventListener("mouseleave", () => {
                luckyBtn.innerText = "I'm Feeling Lucky";
            });

            // Global Click to close popovers
            document.addEventListener("click", (e) => {
                if (!e.target.closest("#apps-popover") && !e.target.closest("[title='Google apps']")) {
                    document.getElementById("apps-popover").style.display = "none";
                }
                if (!e.target.closest("#account-popover") && !e.target.closest(".user-avatar-btn")) {
                    document.getElementById("account-popover").style.display = "none";
                }
                if (!e.target.closest("#settings-popover") && !e.target.closest("[onclick*='toggleSettingsMenu']")) {
                    document.getElementById("settings-popover").style.display = "none";
                }
                if (!e.target.closest("#search-container")) {
                    hideSuggestions();
                }
            });

            // Setup Search Inputs
            setupSearchInput(mainInput, clearBtn);
            setupSearchInput(serpInput, serpClearBtn, true);
        });

        function setupSearchInput(inputEl, clearEl, isSerp = false) {
            inputEl.addEventListener("input", (e) => {
                const val = inputEl.value;
                if (val.trim()) {
                    clearEl.style.display = "flex";
                } else {
                    clearEl.style.display = "none";
                }
                if (!isSerp) {
                    fetchSuggestions(val);
                }
            });

            inputEl.addEventListener("focus", () => {
                searchPill.classList.add("focused");
                if (!isSerp && inputEl.value.trim() === "") {
                    fetchSuggestions("");
                }
            });

            inputEl.addEventListener("blur", () => {
                searchPill.classList.remove("focused");
            });

            inputEl.addEventListener("keydown", (e) => {
                if (e.key === "Enter") {
                    e.preventDefault();
                    hideSuggestions();
                    if (isSerp) {
                        performSerpSearch();
                    } else {
                        performSearch();
                    }
                } else if (e.key === "ArrowDown") {
                    e.preventDefault();
                    navigateSuggestions(1);
                } else if (e.key === "ArrowUp") {
                    e.preventDefault();
                    navigateSuggestions(-1);
                } else if (e.key === "Escape") {
                    hideSuggestions();
                }
            });

            clearEl.addEventListener("click", () => {
                inputEl.value = "";
                clearEl.style.display = "none";
                inputEl.focus();
                if (!isSerp) {
                    hideSuggestions();
                }
            });
        }

        // Autocomplete Suggestions
        async function fetchSuggestions(query) {
            try {
                const res = await fetch(`/api/google/suggest?q=${encodeURIComponent(query)}`);
                const data = await res.json();
                suggestionsList = data.suggestions || [];
                renderSuggestions(suggestionsList, query);
            } catch (err) {
                console.error("Suggestion error:", err);
            }
        }

        function renderSuggestions(list, query) {
            if (!list || list.length === 0) {
                hideSuggestions();
                return;
            }
            activeSuggestionIndex = -1;
            suggestionsBox.innerHTML = "";
            list.forEach((item, idx) => {
                const div = document.createElement("div");
                div.className = "suggestion-item";
                div.innerHTML = `
                    <div class="item-icon">
                        <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
                            <path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
                        </svg>
                    </div>
                    <div class="item-text">${highlightMatch(item, query)}</div>
                    <div class="item-remove" onclick="removeSuggestion(event, ${idx})">Delete</div>
                `;
                div.addEventListener("click", () => {
                    mainInput.value = item;
                    hideSuggestions();
                    performSearch();
                });
                suggestionsBox.appendChild(div);
            });
            suggestionsBox.style.display = "block";
            searchPill.classList.add("open-dropdown");
        }

        function highlightMatch(text, query) {
            if (!query) return text;
            const regex = new RegExp(`(${query})`, "gi");
            return text.replace(regex, "<strong>$1</strong>");
        }

        function hideSuggestions() {
            suggestionsBox.style.display = "none";
            searchPill.classList.remove("open-dropdown");
        }

        function navigateSuggestions(dir) {
            const items = suggestionsBox.querySelectorAll(".suggestion-item");
            if (!items.length) return;
            if (activeSuggestionIndex >= 0 && items[activeSuggestionIndex]) {
                items[activeSuggestionIndex].classList.remove("active");
            }
            activeSuggestionIndex += dir;
            if (activeSuggestionIndex >= items.length) activeSuggestionIndex = 0;
            if (activeSuggestionIndex < 0) activeSuggestionIndex = items.length - 1;
            items[activeSuggestionIndex].classList.add("active");
            mainInput.value = suggestionsList[activeSuggestionIndex];
        }

        function removeSuggestion(e, idx) {
            e.stopPropagation();
            suggestionsList.splice(idx, 1);
            renderSuggestions(suggestionsList, mainInput.value);
        }

        // Search Handlers
        function performSearch() {
            const query = mainInput.value.trim();
            if (!query) return;
            triggerSearch(query, "all");
        }

        function performSerpSearch() {
            const query = serpInput.value.trim();
            if (!query) return;
            triggerSearch(query, currentTab);
        }

        function clearSerpInput() {
            serpInput.value = "";
            serpClearBtn.style.display = "none";
            serpInput.focus();
        }

        function handleLucky() {
            const val = mainInput.value.trim() || "Google Gemini";
            triggerSearch(val, "all");
        }

        function goToHome() {
            homeView.style.display = "flex";
            serpView.style.display = "none";
            document.title = "Google";
            window.history.pushState({}, "", "/");
            mainInput.focus();
            document.body.classList.remove("barrel-roll", "askew");
        }

        function activateTab(tab) {
            currentTab = tab;
            if (tab === "images") {
                document.getElementById("home-images-badge").style.display = "block";
                mainInput.placeholder = "Search images";
            }
            mainInput.focus();
        }

        function switchSerpTab(tab) {
            currentTab = tab;
            document.querySelectorAll(".serp-tab").forEach(el => {
                if (el.dataset.tab === tab) el.classList.add("active");
                else el.classList.remove("active");
            });
            triggerSearch(currentQuery, tab);
        }

        async function triggerSearch(query, tab = "all") {
            currentQuery = query;
            currentTab = tab;

            // Easter eggs
            const qLower = query.toLowerCase().trim();
            document.body.classList.remove("barrel-roll", "askew");
            if (qLower === "do a barrel roll") {
                document.body.classList.add("barrel-roll");
                setTimeout(() => document.body.classList.remove("barrel-roll"), 1600);
            } else if (qLower === "askew" || qLower === "tilt") {
                document.body.classList.add("askew");
            }

            // Update UI State
            homeView.style.display = "none";
            serpView.style.display = "flex";
            serpInput.value = query;
            serpClearBtn.style.display = "flex";
            document.title = `${query} - Google Search`;
            window.history.pushState({ q: query, tab: tab }, "", `/?q=${encodeURIComponent(query)}&tab=${tab}`);

            // Fetch Search Data
            try {
                const res = await fetch(`/api/google/search?q=${encodeURIComponent(query)}&category=${tab}`);
                const data = await res.json();
                renderSerpResults(data, query, tab);
            } catch (err) {
                console.error("Search API error:", err);
            }
        }

        function renderSerpResults(data, query, tab) {
            // Stats
            const totalText = data.total_results || "3,420,000,000";
            const timeText = data.search_time || "0.34 seconds";
            document.getElementById("serp-stats").innerText = `About ${totalText} results (${timeText})`;

            // Render Interactive Widgets (Calculator, Dice, Coin, Timer, Weather)
            renderInteractiveWidget(query);

            // Render Knowledge Graph
            const kg = data.knowledge_panel || data.knowledge_graph;
            if (kg && tab === "all") {
                document.getElementById("sidebar-col").style.display = "block";
                kgContainer.innerHTML = `
                    <div class="knowledge-graph-card">
                        ${kg.image ? `<img src="${kg.image}" class="kg-header-img" alt="${kg.title}">` : ""}
                        <div class="kg-body">
                            <h2 class="kg-title">${kg.title}</h2>
                            <div class="kg-subtitle">${kg.subtitle || ""}</div>
                            <div class="kg-desc">
                                ${kg.description}
                                <br><a href="https://en.wikipedia.org/wiki/${encodeURIComponent(kg.title)}" target="_blank">Wikipedia</a>
                            </div>
                            <div class="kg-facts">
                                ${(kg.attributes || []).map(attr => `
                                    <div class="kg-fact-row">
                                        <strong>${attr.label}:</strong> ${attr.value}
                                    </div>
                                `).join("")}
                            </div>
                        </div>
                    </div>
                `;
            } else {
                kgContainer.innerHTML = "";
                if (tab !== "all") {
                    document.getElementById("sidebar-col").style.display = "none";
                }
            }

            // Results Container by Tab
            resultsContainer.innerHTML = "";
            const relatedBox = document.getElementById("related-box");
            const paginationBox = document.getElementById("pagination-box");

            if (tab === "all") {
                // People Also Ask
                if (data.people_also_ask && data.people_also_ask.length > 0) {
                    const paaHtml = `
                        <div class="paa-card">
                            <div class="paa-heading">People also ask</div>
                            ${data.people_also_ask.map((paa, i) => `
                                <div class="paa-item">
                                    <div class="paa-question" onclick="togglePaa(${i})">
                                        <span>${paa.question}</span>
                                        <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
                                            <path d="M7.41 8.59L12 13.17l4.59-4.58L18 10l-6 6-6-6 1.41-1.41z"/>
                                        </svg>
                                    </div>
                                    <div class="paa-answer" id="paa-ans-${i}">${paa.answer || paa.snippet}</div>
                                </div>
                            `).join("")}
                        </div>
                    `;
                    resultsContainer.innerHTML += paaHtml;
                }

                // Organic Results
                (data.organic_results || []).forEach(item => {
                    const sitelinksHtml = (item.sitelinks && item.sitelinks.length > 0) ? `
                        <div class="sitelinks-grid">
                            ${item.sitelinks.map(sl => `
                                <div class="sitelink-item">
                                    <a href="${item.url}" target="_blank">${sl.title}</a>
                                    <div class="sitelink-snippet">${sl.snippet}</div>
                                </div>
                            `).join("")}
                        </div>
                    ` : "";

                    const resHtml = `
                        <div class="organic-result">
                            <div class="result-breadcrumb">
                                <div class="result-favicon">${item.title.charAt(0)}</div>
                                <span class="result-url">${item.displayed_url}</span>
                            </div>
                            <h3 class="result-title" onclick="window.open('${item.url}', '_blank')">${item.title}</h3>
                            <div class="result-snippet">${item.snippet}</div>
                            ${sitelinksHtml}
                        </div>
                    `;
                    resultsContainer.innerHTML += resHtml;
                });

                // Related Searches
                const relList = data.related_searches || [];
                if (relList.length > 0) {
                    relatedBox.style.display = "block";
                    document.getElementById("related-grid").innerHTML = relList.map(term => `
                        <div class="related-chip" onclick="triggerSearch('${term}', 'all')">
                            <svg viewBox="0 0 24 24" width="18" height="18" fill="#9aa0a6">
                                <path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
                            </svg>
                            <span>${term}</span>
                        </div>
                    `).join("");
                } else {
                    relatedBox.style.display = "none";
                }
                paginationBox.style.display = "flex";

            } else if (tab === "images") {
                relatedBox.style.display = "none";
                paginationBox.style.display = "none";
                const imgList = data.images_results || data.image_results || [];
                const imgHtml = `
                    <div class="images-grid">
                        ${imgList.map(img => `
                            <div class="image-card" onclick="window.open('${img.url || img.thumbnail}', '_blank')">
                                <img src="${img.thumbnail}" alt="${img.title}" loading="lazy">
                                <div class="image-card-info">
                                    <div class="image-card-title">${img.title}</div>
                                    <div class="image-card-source">${img.source}</div>
                                </div>
                            </div>
                        `).join("")}
                    </div>
                `;
                resultsContainer.innerHTML = imgHtml;

            } else if (tab === "videos") {
                relatedBox.style.display = "none";
                paginationBox.style.display = "none";
                const vidList = data.videos_results || data.video_results || [];
                resultsContainer.innerHTML = vidList.map(vid => `
                    <div class="video-result" onclick="window.open('https://youtube.com', '_blank')">
                        <div class="video-thumb-wrapper">
                            <img src="${vid.thumbnail}" alt="${vid.title}">
                            <div class="video-duration">${vid.duration}</div>
                        </div>
                        <div class="video-info">
                            <div class="video-title">${vid.title}</div>
                            <div class="video-meta">${vid.channel} • ${vid.views} • ${vid.uploaded || 'Recent'}</div>
                            <div class="result-snippet">${vid.snippet || 'Watch detailed analysis and walkthrough on YouTube.'}</div>
                        </div>
                    </div>
                `).join("");

            } else if (tab === "news") {
                relatedBox.style.display = "none";
                paginationBox.style.display = "none";
                const newsItems = data.news_results || [];
                resultsContainer.innerHTML = newsItems.map(news => `
                    <div class="news-item" onclick="window.open('https://news.google.com', '_blank')">
                        <div>
                            <div class="news-publisher">${news.publisher || news.source || "Google News"}</div>
                            <div class="news-title">${news.title}</div>
                            <div class="news-time">${news.time}</div>
                            <div class="result-snippet" style="margin-top:4px;">${news.snippet || ''}</div>
                        </div>
                        ${news.thumbnail ? `<img src="${news.thumbnail}" class="news-thumb" alt="thumbnail">` : ''}
                    </div>
                `).join("");

            } else if (tab === "maps") {
                relatedBox.style.display = "none";
                paginationBox.style.display = "none";
                resultsContainer.innerHTML = `
                    <div class="map-container">
                        <img src="https://images.unsplash.com/photo-1524661135-423995f22d0b?w=1200&q=80" class="map-interactive-bg" alt="Map View">
                        <div class="map-overlay-card">
                            <h3 style="font-size: 16px; margin-bottom: 6px;">${query}</h3>
                            <p style="font-size: 12px; color: var(--muted-text); margin-bottom: 12px;">Top locations and geographic coordinates near you.</p>
                            <button class="btn-google" style="width: 100%; border-radius: 20px;" onclick="window.open('https://maps.google.com?q=${encodeURIComponent(query)}', '_blank')">Open in Google Maps</button>
                        </div>
                    </div>
                `;

            } else if (tab === "shopping") {
                relatedBox.style.display = "none";
                paginationBox.style.display = "none";
                resultsContainer.innerHTML = `
                    <div class="shopping-grid">
                        ${[1, 2, 3, 4, 5, 6].map(i => `
                            <div class="shop-card" onclick="window.open('https://shopping.google.com', '_blank')">
                                <img src="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&q=80" alt="Product">
                                <div class="shop-title">${query} Edition - Model ${i}</div>
                                <div class="shop-price">₹${(i * 1299).toLocaleString()}</div>
                                <div class="shop-store">Free delivery • Certified Seller</div>
                            </div>
                        `).join("")}
                    </div>
                `;
            }
        }

        // Accordion
        function togglePaa(index) {
            const ans = document.getElementById(`paa-ans-${index}`);
            if (ans.style.display === "block") {
                ans.style.display = "none";
            } else {
                ans.style.display = "block";
            }
        }

        // Interactive Widgets (Calculator, Dice, Coin, Timer, Weather)
        function renderInteractiveWidget(query) {
            const q = query.toLowerCase().trim();
            widgetContainer.innerHTML = "";

            if (q.includes("calculator") || q === "calc") {
                widgetContainer.innerHTML = `
                    <div class="interactive-widget-box">
                        <div class="calc-display">
                            <div class="calc-history" id="calc-hist"></div>
                            <div class="calc-current" id="calc-val">0</div>
                        </div>
                        <div class="calc-grid">
                            <button class="calc-btn action" onclick="calcAction('C')">C</button>
                            <button class="calc-btn action" onclick="calcAction('(')">(</button>
                            <button class="calc-btn action" onclick="calcAction(')')">)</button>
                            <button class="calc-btn action" onclick="calcAction('/')">÷</button>
                            <button class="calc-btn" onclick="calcAction('7')">7</button>
                            <button class="calc-btn" onclick="calcAction('8')">8</button>
                            <button class="calc-btn" onclick="calcAction('9')">9</button>
                            <button class="calc-btn action" onclick="calcAction('*')">×</button>
                            <button class="calc-btn" onclick="calcAction('4')">4</button>
                            <button class="calc-btn" onclick="calcAction('5')">5</button>
                            <button class="calc-btn" onclick="calcAction('6')">6</button>
                            <button class="calc-btn action" onclick="calcAction('-')">−</button>
                            <button class="calc-btn" onclick="calcAction('1')">1</button>
                            <button class="calc-btn" onclick="calcAction('2')">2</button>
                            <button class="calc-btn" onclick="calcAction('3')">3</button>
                            <button class="calc-btn action" onclick="calcAction('+')">+</button>
                            <button class="calc-btn" onclick="calcAction('0')">0</button>
                            <button class="calc-btn" onclick="calcAction('.')">.</button>
                            <button class="calc-btn action" onclick="calcAction('%')">%</button>
                            <button class="calc-btn equals" onclick="calcAction('=')">=</button>
                        </div>
                    </div>
                `;
            } else if (q.includes("flip a coin") || q === "coin flip") {
                widgetContainer.innerHTML = `
                    <div class="interactive-widget-box">
                        <div class="coin-wrapper">
                            <div class="coin" id="coin-element">HEADS</div>
                            <button class="btn-google" style="border-radius: 20px; padding: 0 24px;" onclick="flipCoin()">Flip Again</button>
                        </div>
                    </div>
                `;
            } else if (q.includes("roll a dice") || q.includes("dice roller")) {
                widgetContainer.innerHTML = `
                    <div class="interactive-widget-box">
                        <div class="dice-box">
                            <div class="dice" id="dice-element">6</div>
                            <button class="btn-google" style="border-radius: 20px; padding: 0 24px;" onclick="rollDice()">Roll Again</button>
                        </div>
                    </div>
                `;
            } else if (q.includes("timer") || q.includes("stopwatch")) {
                widgetContainer.innerHTML = `
                    <div class="interactive-widget-box">
                        <div class="timer-tabs">
                            <div class="timer-tab active" id="tab-timer" onclick="switchTimerTab('timer')">TIMER</div>
                            <div class="timer-tab" id="tab-stopwatch" onclick="switchTimerTab('stopwatch')">STOPWATCH</div>
                        </div>
                        <div id="timer-view">
                            <div class="timer-time" id="timer-display">05:00</div>
                            <div class="timer-controls">
                                <button class="btn-google" style="background:#1a73e8; color:#fff;" id="timer-start-btn" onclick="toggleTimer()">START</button>
                                <button class="btn-google" onclick="resetTimer()">RESET</button>
                            </div>
                        </div>
                        <div id="stopwatch-view" style="display:none;">
                            <div class="timer-time" id="stopwatch-display">00:00.00</div>
                            <div class="timer-controls">
                                <button class="btn-google" style="background:#1a73e8; color:#fff;" id="sw-start-btn" onclick="toggleStopwatch()">START</button>
                                <button class="btn-google" onclick="resetStopwatch()">RESET</button>
                            </div>
                        </div>
                    </div>
                `;
            } else if (q.includes("weather")) {
                widgetContainer.innerHTML = `
                    <div class="interactive-widget-box">
                        <div class="weather-card">
                            <div class="weather-left">
                                <div class="weather-icon-lg">☀️</div>
                                <div>
                                    <span class="weather-temp">29</span><span class="weather-deg">°C | °F</span>
                                    <div style="font-size: 14px; font-weight: 500;">Sunny</div>
                                </div>
                            </div>
                            <div class="weather-details">
                                <div>Precipitation: 0%</div>
                                <div>Humidity: 58%</div>
                                <div>Wind: 14 km/h</div>
                            </div>
                        </div>
                        <div class="forecast-row">
                            <div class="forecast-day"><div>Mon</div><div class="forecast-icon">☀️</div><div>30°</div></div>
                            <div class="forecast-day"><div>Tue</div><div class="forecast-icon">⛅</div><div>28°</div></div>
                            <div class="forecast-day"><div>Wed</div><div class="forecast-icon">🌧️</div><div>26°</div></div>
                            <div class="forecast-day"><div>Thu</div><div class="forecast-icon">⛅</div><div>29°</div></div>
                            <div class="forecast-day"><div>Fri</div><div class="forecast-icon">☀️</div><div>31°</div></div>
                            <div class="forecast-day"><div>Sat</div><div class="forecast-icon">☀️</div><div>32°</div></div>
                            <div class="forecast-day"><div>Sun</div><div class="forecast-icon">⛅</div><div>29°</div></div>
                        </div>
                    </div>
                `;
            }
        }

        // Calculator Logic
        let calcExpr = "";
        function calcAction(val) {
            const histEl = document.getElementById("calc-hist");
            const valEl = document.getElementById("calc-val");
            if (val === "C") {
                calcExpr = "";
                histEl.innerText = "";
                valEl.innerText = "0";
            } else if (val === "=") {
                try {
                    const result = Function(`'use strict'; return (${calcExpr})`)();
                    histEl.innerText = calcExpr + " =";
                    valEl.innerText = result;
                    calcExpr = String(result);
                } catch (e) {
                    valEl.innerText = "Error";
                }
            } else {
                calcExpr += val;
                valEl.innerText = calcExpr;
            }
        }

        // Coin Flip Logic
        function flipCoin() {
            const coin = document.getElementById("coin-element");
            coin.classList.add("flipping");
            setTimeout(() => {
                const result = Math.random() < 0.5 ? "HEADS" : "TAILS";
                coin.innerText = result;
                coin.classList.remove("flipping");
            }, 1000);
        }

        // Dice Roll Logic
        function rollDice() {
            const dice = document.getElementById("dice-element");
            dice.classList.add("rolling");
            setTimeout(() => {
                const num = Math.floor(Math.random() * 6) + 1;
                dice.innerText = num;
                dice.classList.remove("rolling");
            }, 700);
        }

        // Timer Logic
        function switchTimerTab(tab) {
            const tTab = document.getElementById("tab-timer");
            const sTab = document.getElementById("tab-stopwatch");
            const tView = document.getElementById("timer-view");
            const sView = document.getElementById("stopwatch-view");
            if (tab === "timer") {
                tTab.classList.add("active");
                sTab.classList.remove("active");
                tView.style.display = "block";
                sView.style.display = "none";
            } else {
                sTab.classList.add("active");
                tTab.classList.remove("active");
                sView.style.display = "block";
                tView.style.display = "none";
            }
        }

        function toggleTimer() {
            const btn = document.getElementById("timer-start-btn");
            if (timerInterval) {
                clearInterval(timerInterval);
                timerInterval = null;
                btn.innerText = "START";
            } else {
                btn.innerText = "STOP";
                timerInterval = setInterval(() => {
                    if (timerSeconds > 0) {
                        timerSeconds--;
                        updateTimerDisplay();
                    } else {
                        clearInterval(timerInterval);
                        timerInterval = null;
                        btn.innerText = "START";
                        alert("Time is up!");
                    }
                }, 1000);
            }
        }

        function resetTimer() {
            clearInterval(timerInterval);
            timerInterval = null;
            timerSeconds = 300;
            document.getElementById("timer-start-btn").innerText = "START";
            updateTimerDisplay();
        }

        function updateTimerDisplay() {
            const m = Math.floor(timerSeconds / 60);
            const s = timerSeconds % 60;
            document.getElementById("timer-display").innerText = `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
        }

        function toggleStopwatch() {
            const btn = document.getElementById("sw-start-btn");
            if (stopwatchInterval) {
                clearInterval(stopwatchInterval);
                stopwatchInterval = null;
                btn.innerText = "START";
            } else {
                btn.innerText = "STOP";
                const start = Date.now() - stopwatchMs;
                stopwatchInterval = setInterval(() => {
                    stopwatchMs = Date.now() - start;
                    const totalSec = Math.floor(stopwatchMs / 1000);
                    const m = Math.floor(totalSec / 60);
                    const s = totalSec % 60;
                    const ms = Math.floor((stopwatchMs % 1000) / 10);
                    document.getElementById("stopwatch-display").innerText = `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}.${String(ms).padStart(2, '0')}`;
                }, 20);
            }
        }

        function resetStopwatch() {
            clearInterval(stopwatchInterval);
            stopwatchInterval = null;
            stopwatchMs = 0;
            document.getElementById("sw-start-btn").innerText = "START";
            document.getElementById("stopwatch-display").innerText = "00:00.00";
        }

        // Tools and Filters
        function toggleSerpTools() {
            const drawer = document.getElementById("tools-drawer");
            drawer.style.display = drawer.style.display === "flex" ? "none" : "flex";
        }
        function filterTime(val) {
            triggerSearch(currentQuery, currentTab);
        }
        function filterVerbatim(val) {
            triggerSearch(currentQuery, currentTab);
        }
        function showPage(p) {
            window.scrollTo({ top: 0, behavior: 'smooth' });
            triggerSearch(currentQuery, currentTab);
        }

        // Popovers
        function toggleAppsMenu(e) {
            e.stopPropagation();
            const pop = document.getElementById("apps-popover");
            pop.style.display = pop.style.display === "block" ? "none" : "block";
            document.getElementById("account-popover").style.display = "none";
            document.getElementById("settings-popover").style.display = "none";
        }
        function toggleAccountMenu(e) {
            e.stopPropagation();
            const pop = document.getElementById("account-popover");
            pop.style.display = pop.style.display === "block" ? "none" : "block";
            document.getElementById("apps-popover").style.display = "none";
            document.getElementById("settings-popover").style.display = "none";
        }
        function toggleSettingsMenu(e) {
            e.stopPropagation();
            const pop = document.getElementById("settings-popover");
            pop.style.display = pop.style.display === "block" ? "none" : "block";
            document.getElementById("apps-popover").style.display = "none";
            document.getElementById("account-popover").style.display = "none";
        }
        function launchApp(name) {
            document.getElementById("apps-popover").style.display = "none";
            showInfoToast(`Opening ${name}...`);
        }

        // Dark Mode Toggle
        function toggleDarkMode() {
            const isDark = document.body.classList.toggle("dark-mode");
            localStorage.setItem("google_dark_theme", isDark ? "true" : "false");
            document.getElementById("dark-theme-status").innerText = isDark ? "On" : "Off";
            document.getElementById("settings-popover").style.display = "none";
        }

        // Voice Search Modal
        function openVoiceSearch() {
            document.getElementById("voice-modal").style.display = "flex";
            if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
                try {
                    const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
                    const recognition = new SpeechRec();
                    recognition.lang = 'en-US';
                    recognition.onresult = (event) => {
                        const transcript = event.results[0][0].transcript;
                        document.getElementById("voice-transcript").innerText = `"${transcript}"`;
                        setTimeout(() => {
                            closeVoiceModal();
                            triggerSearch(transcript, 'all');
                        }, 800);
                    };
                    recognition.start();
                } catch(e) {
                    console.log("Web Speech API:", e);
                }
            }
        }
        function closeVoiceModal() {
            document.getElementById("voice-modal").style.display = "none";
        }
        function closeVoiceSearch(e) {
            if (e.target.id === "voice-modal") closeVoiceModal();
        }
        function simulateVoiceQuery(text) {
            document.getElementById("voice-transcript").innerText = `"${text}"`;
            setTimeout(() => {
                closeVoiceModal();
                triggerSearch(text, 'all');
            }, 600);
        }

        // Google Lens Modal
        function openLensModal() {
            document.getElementById("lens-modal").style.display = "flex";
        }
        function closeLensModal(e) {
            if (!e || e.target.id === "lens-modal") {
                document.getElementById("lens-modal").style.display = "none";
            }
        }
        function handleLensFile(e) {
            const file = e.target.files[0];
            if (file) {
                closeLensModal();
                triggerSearch("Visual image match: " + file.name, "images");
            }
        }
        function searchLensUrl() {
            const url = document.getElementById("lens-url-input").value.trim();
            if (url) {
                closeLensModal();
                triggerSearch("Image search: " + url, "images");
            }
        }

        // Virtual Keyboard
        function toggleVirtualKeyboard() {
            const kb = document.getElementById("virtual-keyboard");
            kb.style.display = kb.style.display === "flex" ? "none" : "flex";
        }
        function kbPress(char) {
            mainInput.value += char;
            clearBtn.style.display = "flex";
            mainInput.focus();
        }
        function kbBackspace() {
            mainInput.value = mainInput.value.slice(0, -1);
            if (!mainInput.value) clearBtn.style.display = "none";
            mainInput.focus();
        }

        // Languages
        function setSearchLanguage(code) {
            const langNames = {
                hi: "हिन्दी", bn: "বাংলা", te: "తెలుగు", mr: "मराठी",
                ta: "தமிழ்", gu: "ગુજરાતી", kn: "ಕನ್ನಡ", ml: "മലയാളം", pa: "ਪੰਜਾਬੀ"
            };
            showInfoToast(`Language set to ${langNames[code] || code}`);
            mainInput.focus();
        }

        // Toast Feedback
        function showInfoToast(msg) {
            const toast = document.createElement("div");
            toast.innerText = msg;
            toast.style.cssText = `
                position: fixed;
                bottom: 24px;
                left: 24px;
                background: #323232;
                color: #fff;
                padding: 12px 20px;
                border-radius: 4px;
                font-size: 14px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                z-index: 9999;
                opacity: 0;
                transition: opacity 0.3s;
            `;
            document.body.appendChild(toast);
            setTimeout(() => toast.style.opacity = "1", 10);
            setTimeout(() => {
                toast.style.opacity = "0";
                setTimeout(() => toast.remove(), 300);
            }, 2500);
        }
    </script>
</body>
</html>
"""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Successfully generated Google official website at {out_path} ({len(html)} bytes)")

if __name__ == "__main__":
    build_google_html()

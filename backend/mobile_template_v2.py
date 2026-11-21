"""
backend/mobile_template_v2.py

Primary V2 Mobile Companion frontend HTML/CSS/JS string constant.
Re-exported as `INDEX_TEMPLATE_V2` by `backend/mobile_server.py`.
Zero-build compliant: pure Python string constant, no external .html files.
"""

INDEX_TEMPLATE_V2 = """
<!DOCTYPE html>
<html lang="en" class="arbor-offline-css">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>Arbor Companion</title>

  <style id="arbor-offline-fallback">
    .hidden { display: none !important; }
    body { margin: 0; font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f3f3f3; color: #191e1a; }
    button { cursor: pointer; }
    input, select, textarea { box-sizing: border-box; }
    /* Scoped offline vault stylesheet: ONLY active when Tailwind CDN has not loaded */
    html.arbor-offline-css *, html.arbor-offline-css *::before, html.arbor-offline-css *::after { box-sizing: border-box; }
    html.arbor-offline-css body { background: #f3f3f3 !important; color: #191e1a; min-height: 100vh; }
    html.arbor-offline-css svg { max-width: 24px; max-height: 24px; flex-shrink: 0; }
    html.arbor-offline-css .fixed { position: fixed; }
    html.arbor-offline-css .sticky { position: sticky; }
    html.arbor-offline-css .relative { position: relative; }
    html.arbor-offline-css .absolute { position: absolute; }
    html.arbor-offline-css .inset-0 { top: 0; right: 0; bottom: 0; left: 0; }
    html.arbor-offline-css .top-0 { top: 0; }
    html.arbor-offline-css .bottom-0 { bottom: 0; }
    html.arbor-offline-css .z-10 { z-index: 10; }
    html.arbor-offline-css .z-20 { z-index: 20; }
    html.arbor-offline-css .z-30 { z-index: 30; }
    html.arbor-offline-css .z-40 { z-index: 40; }
    html.arbor-offline-css .z-50 { z-index: 50; }
    html.arbor-offline-css .block { display: block; }
    html.arbor-offline-css .inline-flex { display: inline-flex; }
    html.arbor-offline-css .flex { display: flex; }
    html.arbor-offline-css .flex-col { flex-direction: column; }
    html.arbor-offline-css .flex-1 { flex: 1 1 0%; }
    html.arbor-offline-css .flex-none { flex: none; }
    html.arbor-offline-css .flex-wrap { flex-wrap: wrap; }
    html.arbor-offline-css .items-center { align-items: center; }
    html.arbor-offline-css .items-start { align-items: flex-start; }
    html.arbor-offline-css .justify-between { justify-content: space-between; }
    html.arbor-offline-css .justify-center { justify-content: center; }
    html.arbor-offline-css .grid { display: grid; }
    html.arbor-offline-css .grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    html.arbor-offline-css .grid-cols-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    html.arbor-offline-css .gap-1 { gap: 0.25rem; }
    html.arbor-offline-css .gap-1\\.5 { gap: 0.375rem; }
    html.arbor-offline-css .gap-2 { gap: 0.5rem; }
    html.arbor-offline-css .gap-2\\.5 { gap: 0.625rem; }
    html.arbor-offline-css .gap-3 { gap: 0.75rem; }
    html.arbor-offline-css .space-y-1 > * + * { margin-top: 0.25rem; }
    html.arbor-offline-css .space-y-1\\.5 > * + * { margin-top: 0.375rem; }
    html.arbor-offline-css .space-y-2 > * + * { margin-top: 0.5rem; }
    html.arbor-offline-css .space-y-2\\.5 > * + * { margin-top: 0.625rem; }
    html.arbor-offline-css .space-y-3 > * + * { margin-top: 0.75rem; }
    html.arbor-offline-css .w-full { width: 100%; }
    html.arbor-offline-css .h-full { height: 100%; }
    html.arbor-offline-css .min-w-0 { min-width: 0; }
    html.arbor-offline-css .overflow-hidden { overflow: hidden; }
    html.arbor-offline-css .overflow-y-auto { overflow-y: auto; }
    html.arbor-offline-css .overflow-x-auto { overflow-x: auto; }
    html.arbor-offline-css .whitespace-nowrap { white-space: nowrap; }
    html.arbor-offline-css .truncate { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    html.arbor-offline-css .p-1 { padding: 0.25rem; }
    html.arbor-offline-css .p-1\\.5 { padding: 0.375rem; }
    html.arbor-offline-css .p-2 { padding: 0.5rem; }
    html.arbor-offline-css .p-3 { padding: 0.75rem; }
    html.arbor-offline-css .p-3\\.5 { padding: 0.875rem; }
    html.arbor-offline-css .p-4 { padding: 1rem; }
    html.arbor-offline-css .px-1\\.5 { padding-left: 0.375rem; padding-right: 0.375rem; }
    html.arbor-offline-css .px-2 { padding-left: 0.5rem; padding-right: 0.5rem; }
    html.arbor-offline-css .px-2\\.5 { padding-left: 0.625rem; padding-right: 0.625rem; }
    html.arbor-offline-css .px-3 { padding-left: 0.75rem; padding-right: 0.75rem; }
    html.arbor-offline-css .px-3\\.5 { padding-left: 0.875rem; padding-right: 0.875rem; }
    html.arbor-offline-css .px-4 { padding-left: 1rem; padding-right: 1rem; }
    html.arbor-offline-css .py-0\\.5 { padding-top: 0.125rem; padding-bottom: 0.125rem; }
    html.arbor-offline-css .py-1 { padding-top: 0.25rem; padding-bottom: 0.25rem; }
    html.arbor-offline-css .py-1\\.5 { padding-top: 0.375rem; padding-bottom: 0.375rem; }
    html.arbor-offline-css .py-2 { padding-top: 0.5rem; padding-bottom: 0.5rem; }
    html.arbor-offline-css .py-2\\.5 { padding-top: 0.625rem; padding-bottom: 0.625rem; }
    html.arbor-offline-css .py-3 { padding-top: 0.75rem; padding-bottom: 0.75rem; }
    html.arbor-offline-css .mt-1 { margin-top: 0.25rem; }
    html.arbor-offline-css .mt-2 { margin-top: 0.5rem; }
    html.arbor-offline-css .mb-1 { margin-bottom: 0.25rem; }
    html.arbor-offline-css .mb-2 { margin-bottom: 0.5rem; }
    html.arbor-offline-css .rounded { border-radius: 5px; }
    html.arbor-offline-css .rounded-md { border-radius: 6px; }
    html.arbor-offline-css .rounded-lg { border-radius: 8px; }
    html.arbor-offline-css .rounded-xl { border-radius: 12px; }
    html.arbor-offline-css .rounded-2xl { border-radius: 16px; }
    html.arbor-offline-css .rounded-full { border-radius: 9999px; }
    html.arbor-offline-css .border { border: 1px solid #d4d8d5; }
    html.arbor-offline-css .border-2 { border: 2px solid #3a7d44; }
    html.arbor-offline-css .border-b { border-bottom: 1px solid #d4d8d5; }
    html.arbor-offline-css .border-t { border-top: 1px solid #d4d8d5; }
    html.arbor-offline-css .border-bordercol { border-color: #d4d8d5; }
    html.arbor-offline-css .border-stone-200 { border-color: #e2e5e2; }
    html.arbor-offline-css .border-fern { border-color: #3a7d44; }
    html.arbor-offline-css .border-amber-300 { border-color: #f59e0b; }
    html.arbor-offline-css .bg-canvas, html.arbor-offline-css .bg-alabaster { background-color: #f3f3f3; }
    html.arbor-offline-css .bg-surface, html.arbor-offline-css .bg-white { background-color: #ffffff; }
    html.arbor-offline-css .bg-stone-50, html.arbor-offline-css .bg-tonal1 { background-color: #f8f9fa; }
    html.arbor-offline-css .bg-stone-100, html.arbor-offline-css .bg-tonal2 { background-color: #eceeec; }
    html.arbor-offline-css .bg-stone-200 { background-color: #dfe3e0; }
    html.arbor-offline-css .bg-fern { background-color: #3a7d44; color: #ffffff; }
    html.arbor-offline-css .bg-fern-dark { background-color: #205438; color: #ffffff; }
    html.arbor-offline-css .bg-fern-light, html.arbor-offline-css .bg-emerald-50 { background-color: #eaf4ec; }
    html.arbor-offline-css .bg-amber-50 { background-color: #fffbeb; }
    html.arbor-offline-css .bg-amber-600 { background-color: #d97706; color: #ffffff; }
    html.arbor-offline-css .bg-red-50, html.arbor-offline-css .bg-brick-light { background-color: #fdf2f2; }
    html.arbor-offline-css .text-ink { color: #191e1a; }
    html.arbor-offline-css .text-muted, html.arbor-offline-css .text-ink-muted, html.arbor-offline-css .text-subdued { color: #535d56; }
    html.arbor-offline-css .text-white { color: #ffffff; }
    html.arbor-offline-css .text-fern { color: #3a7d44; }
    html.arbor-offline-css .text-fern-dark, html.arbor-offline-css .text-emerald-800 { color: #205438; }
    html.arbor-offline-css .text-amber-900, html.arbor-offline-css .text-amber-800 { color: #78350f; }
    html.arbor-offline-css .text-red-700, html.arbor-offline-css .text-brick { color: #b91c1c; }
    html.arbor-offline-css .text-center { text-align: center; }
    html.arbor-offline-css .text-right { text-align: right; }
    html.arbor-offline-css .uppercase { text-transform: uppercase; letter-spacing: 0.04em; }
    html.arbor-offline-css .font-sans { font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
    html.arbor-offline-css .font-serif { font-family: Georgia, Cambria, 'Times New Roman', serif; }
    html.arbor-offline-css .font-mono { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }
    html.arbor-offline-css .font-medium { font-weight: 500; }
    html.arbor-offline-css .font-semibold { font-weight: 600; }
    html.arbor-offline-css .font-bold { font-weight: 700; }
    html.arbor-offline-css .text-xs { font-size: 0.75rem; line-height: 1.05rem; }
    html.arbor-offline-css .text-sm { font-size: 0.875rem; line-height: 1.25rem; }
    html.arbor-offline-css .text-base { font-size: 1rem; line-height: 1.4rem; }
    html.arbor-offline-css .text-lg { font-size: 1.125rem; line-height: 1.5rem; }
    /* Key interactive surfaces in offline concrete-vault mode */
    html.arbor-offline-css header { background: #ffffff; border-bottom: 1px solid #d4d8d5; padding: 10px 14px; }
    html.arbor-offline-css button { border: 1px solid #d4d8d5; border-radius: 6px; padding: 6px 10px; background: #ffffff; color: #191e1a; font-size: 0.85rem; }
    html.arbor-offline-css button.bg-fern, html.arbor-offline-css #btnStampArmedShelf, html.arbor-offline-css #btnConfirmStampAndReview { background: #3a7d44; color: #ffffff; border-color: #205438; font-weight: 700; }
    html.arbor-offline-css button.bg-amber-600 { background: #d97706; color: #ffffff; border-color: #b45309; font-weight: 700; }
    html.arbor-offline-css input, html.arbor-offline-css select, html.arbor-offline-css textarea { border: 1px solid #c4c9c5; border-radius: 6px; padding: 6px 8px; background: #ffffff; color: #191e1a; font-size: 0.9rem; }
    html.arbor-offline-css #listView, html.arbor-offline-css #detailView, html.arbor-offline-css #batchLocationView { max-width: 540px; margin: 0 auto; min-height: 100vh; background: #f3f3f3; display: flex; flex-direction: column; }
    html.arbor-offline-css #specimenListContainer > * { background: #ffffff; border: 1px solid #d4d8d5; border-radius: 8px; padding: 10px 12px; margin-bottom: 8px; }
    html.arbor-offline-css #auditStationLaunchpad { background: #eaf4ec; border: 1px solid #a4cca9; border-radius: 8px; padding: 10px; margin: 8px 12px; }
    html.arbor-offline-css #armedShelfBanner { background: #eaf4ec; border: 1px solid #a4cca9; border-radius: 8px; padding: 8px 10px; margin-top: 8px; }
    html.arbor-offline-css .tab-btn { border: none; background: transparent; padding: 8px 6px; font-weight: 600; color: #535d56; }
    html.arbor-offline-css #tabIndicator { display: none; }
    html.arbor-offline-css #btnDetailMarkReviewed { width: 100%; min-height: 46px; background: #3a7d44; color: #ffffff; border: none; border-radius: 8px; font-weight: 700; font-size: 0.95rem; }
    html.arbor-offline-css #offlineBanner { background: #78350f; color: #ffffff; padding: 8px 14px; font-size: 0.8rem; font-weight: 600; }
    html.arbor-offline-css [id$="Modal"] { position: fixed; top: 0; right: 0; bottom: 0; left: 0; background: rgba(18, 22, 19, 0.6); display: flex; align-items: center; justify-content: center; padding: 16px; z-index: 50; }
    html.arbor-offline-css [id$="Modal"] > div { background: #ffffff; border: 1px solid #d4d8d5; border-radius: 12px; max-width: 440px; width: 100%; padding: 16px; max-height: 88vh; overflow-y: auto; box-shadow: 0 12px 32px rgba(0,0,0,0.28); }
    html.arbor-offline-css #toast { position: fixed; bottom: 80px; left: 50%; transform: translateX(-50%); background: #191e1a; color: #ffffff; padding: 10px 16px; border-radius: 9999px; z-index: 60; font-size: 0.85rem; box-shadow: 0 6px 20px rgba(0,0,0,0.25); }
  </style>
  <script>
    window._arborInitTailwindV2 = function() {
      if (typeof tailwind === 'undefined') return;
      tailwind.config = {
        theme: {
          extend: {
            colors: {
              alabaster: '#f3f3f3',
              canvas: '#f3f3f3',
              surface: '#ffffff',
              'surface-subtle': '#fbfbfb',
              ink: '#191e1a',
              'ink-muted': '#535d56',
              'ink-faint': '#848f87',
              muted: '#535d56',
              subdued: '#848f87',
              fern: {
                DEFAULT: '#3a7d44',
                dark: '#205438',
                light: '#eaf4ec',
                border: '#a4cca9'
              },
              'fern-dark': '#205438',
              'fern-light': '#eaf4ec',
              brick: {
                DEFAULT: '#c93a40',
                light: '#fdf2f2'
              },
              'brick-light': '#fdf2f2',
              slate: {
                DEFAULT: '#4a7b9d',
                light: '#f0f6fa'
              },
              'slate-light': '#f0f6fa',
              ember: {
                DEFAULT: '#d95c14',
                dark: '#b84a0c',
                light: '#fff3ec',
                border: '#f8c2a3'
              },
              'ember-light': '#fff3ec',
              bordercol: '#d4d8d5',
              'bordercol-subtle': '#ecefec',
              tonal1: '#f8f9fa',
              tonal2: '#eceeec'
            },
            fontFamily: {
              sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
              serif: ['Lora', 'Georgia', 'serif'],
              mono: ['"JetBrains Mono"', 'JetBrains Mono', 'Menlo', 'monospace']
            },
            boxShadow: {
              card: '0 1px 3px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.02)',
              pop: '0 4px 12px rgba(0,0,0,0.08)',
              dock: '0 -2px 10px rgba(0,0,0,0.05)',
              '2xs': '0 1px 2px rgba(0,0,0,0.03)'
            }
          }
        }
      };
      document.documentElement.classList.remove('arbor-offline-css');
    };
  </script>
  <!-- Tailwind CSS CDN (non-blocking defer so offline vaults render immediately via #arbor-offline-fallback) -->
  <script defer src="https://cdn.tailwindcss.com?plugins=forms,container-queries" onload="window._arborInitTailwindV2()" onerror="document.documentElement.classList.add('arbor-offline-css')"></script>
  <!-- Google Fonts (non-blocking): Lora (Botanical Latin), Inter (UI), JetBrains Mono (IDs & Coordinates) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Lora:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600&display=swap" rel="stylesheet" media="print" onload="this.media='all'">

  <style>
    .no-scrollbar::-webkit-scrollbar { display: none; }
    .no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
    .tap-highlight-transparent { -webkit-tap-highlight-color: transparent; }
    .tap-active:active { transform: scale(0.985); transition: transform 0.05s ease-out; }
    .touch-target-min { min-height: 44px; min-width: 44px; }
    .tab-slider { transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1); }
    #tabTrack { transition: transform 0.28s cubic-bezier(0.2, 0.8, 0.2, 1); }
    body {
      background-color: #121413;
      touch-action: pan-y;
      overscroll-behavior-y: none;
      -webkit-font-smoothing: antialiased;
    }
    .mobile-shell {
      max-width: 440px;
      min-height: 100vh;
      margin: 0 auto;
      background-color: #f3f3f3;
      position: relative;
      box-shadow: 0 0 50px rgba(0,0,0,0.4);
      display: flex;
      flex-direction: column;
    }
  </style>
</head>
<body class="min-h-screen py-0 md:py-6 flex justify-center items-center font-sans text-ink select-none">

  <div class="mobile-shell w-full overflow-hidden border-x border-stone-800 flex flex-col h-screen md:h-[900px] md:max-h-[94vh] relative">

    <!-- Offline Banner -->
    <div id="offlineBanner" class="hidden bg-ember-light border-b border-ember-border px-4 py-2 flex items-center justify-between gap-2 text-xs font-sans font-medium text-ember-dark shrink-0 z-50">
      <div class="flex items-center gap-2">
        <span class="text-sm">⚠</span>
        <span id="offlineBannerText">Host disconnected. Reconnecting...</span>
      </div>
      <button type="button" onclick="setupEventSource()" class="min-h-[30px] px-2.5 py-1 bg-ember text-white rounded font-bold text-[11px] tap-active">
        Retry
      </button>
    </div>

    <!-- ============================================================= -->
    <!-- SCREEN 1: VAULT LIST VIEW (#listView)                         -->
    <!-- ============================================================= -->
    <div id="listView" class="flex-1 flex flex-col h-full bg-canvas overflow-hidden">
      <!-- 1. Top Header -->
      <header class="sticky top-0 z-40 bg-surface/95 backdrop-blur-md border-b border-bordercol shrink-0">
        <div class="px-3.5 pt-3 pb-2 flex items-center justify-between">
          <div class="flex items-center space-x-2.5">
            <!-- Arbor "A" Badge -->
            <div class="w-7 h-7 rounded bg-fern-dark flex items-center justify-center text-white font-serif font-bold text-sm shadow-sm ring-1 ring-black/10">
              A
            </div>
            <div>
              <div class="flex items-center space-x-1.5 leading-none">
                <span class="font-bold text-[13px] tracking-tight text-ink font-sans">Arbor Companion</span>
                <span class="text-[10px] px-1 py-0.5 rounded bg-emerald-50 text-fern-dark font-mono font-medium border border-fern/30">v2</span>
              </div>
              <div class="text-[10.5px] font-mono text-ink-muted tracking-tight truncate max-w-[170px] mt-0.5" id="headerDbName">
                Loading database...
              </div>
            </div>
          </div>

          <!-- Top Utility Controls -->
          <div class="flex items-center space-x-1.5">
            <!-- Undo Button -->
            <button id="btnListUndo" onclick="undoLastEdit()" title="Undo recent edit" class="w-8 h-8 rounded-md bg-stone-100 border border-stone-200 text-stone-600 hover:text-ink flex items-center justify-center tap-active transition-colors">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M3 10h10a5 5 0 015 5v2m0 0l-4-4m4 4l4-4M3 10l4-4m-4 4l4 4"/>
              </svg>
            </button>

            <!-- Walk Mode (Wake Lock) Toggle -->
            <button id="btnListWakeLock" onclick="toggleWakeLock()" title="Keep screen awake during audit" class="w-8 h-8 rounded-md bg-stone-100 border border-stone-200 text-stone-600 hover:text-ink flex items-center justify-center tap-active transition-colors">
              <span id="listWakeLockIcon" class="text-xs">🌙</span>
            </button>

            <!-- Batch Location Registrator Trigger -->
            <button id="btnOpenBatchLocation" onclick="showBatchLocationView()" title="Open Batch Location Registrator" class="w-8 h-8 rounded-md bg-emerald-50 border border-fern/30 text-fern-dark hover:bg-emerald-100 flex items-center justify-center tap-active transition-colors">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
              </svg>
            </button>

            <!-- Settings Trigger -->
            <button onclick="openSettingsModal()" title="Application Settings" class="w-8 h-8 rounded-md bg-stone-100 border border-stone-200 text-stone-600 hover:text-ink flex items-center justify-center tap-active transition-colors">
              <span class="text-xs font-mono">⚙️</span>
            </button>

            <!-- Connection Status Pill -->
            <div onclick="openModal('connectionModal')" class="flex items-center space-x-1 px-2 py-1 rounded-full bg-emerald-50 border border-emerald-200 text-[10.5px] font-mono font-medium text-emerald-800 cursor-pointer">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
              <span id="pingBadge">42ms</span>
            </div>
          </div>
        </div>

        <!-- Search Bar Row -->
        <div class="px-3.5 pb-2.5 pt-0.5">
          <div class="relative flex items-center">
            <div class="absolute left-3 text-ink-faint pointer-events-none">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
              </svg>
            </div>
            <input 
              type="text" 
              inputmode="numeric"
              id="searchBox" 
              placeholder="Search accession # or taxonomy..." 
              oninput="handleSearchInput()"
              autocomplete="off"
              spellcheck="false"
              class="w-full pl-9 pr-22 py-2 bg-stone-100/90 hover:bg-stone-100 focus:bg-white text-xs font-mono text-ink placeholder:text-ink-faint placeholder:font-sans rounded-lg border border-stone-200 focus:border-fern focus:ring-1 focus:ring-fern focus:outline-none transition-all shadow-inner"
            />
            <div class="absolute right-2 flex items-center space-x-1">
              <button id="btnInputModeToggle" type="button" onclick="toggleSearchInputMode()" class="px-1.5 py-0.5 rounded bg-stone-200/60 hover:bg-stone-300 text-[10px] font-mono font-bold text-stone-600 transition-colors" title="Toggle numeric / text keyboard">
                123
              </button>
              <button id="searchClearBtn" onclick="clearSearch()" class="hidden w-6 h-6 flex items-center justify-center rounded-full bg-stone-200/80 hover:bg-stone-300 text-ink-muted hover:text-ink active:scale-95 text-xs font-bold leading-none transition-all" title="Clear search">
                ✕
              </button>
              <button id="btnFilterModalTrigger" onclick="openFilterModal()" title="Curatorial Filters" class="relative p-1.5 rounded-md hover:bg-stone-200/70 text-ink-muted hover:text-ink transition-colors">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"/>
                </svg>
                <span id="filterActiveBadge" class="hidden absolute top-1 right-1 w-1.5 h-1.5 rounded-full bg-fern ring-2 ring-white"></span>
              </button>
            </div>
          </div>
        </div>

        <!-- 1b. In-Vault Audit Station Launchpad & Armed Station Banner -->
        <div id="auditStationLaunchpad" class="px-3.5 py-1.5 bg-emerald-50/80 border-t border-b border-fern/20 text-xs">
          <!-- Active Station Pill (shown when armed) -->
          <div id="activeStationPill" class="hidden flex items-center justify-between">
            <div class="flex items-center gap-1.5 min-w-0">
              <span class="text-xs">🎯</span>
              <span class="font-mono text-[10px] text-muted">Auditing:</span>
              <span class="font-mono text-xs font-bold text-fern-dark truncate" id="activeStationPillText">Lid's hus · Cab 21 · Sh 01</span>
            </div>
            <button type="button" onclick="openStationSetup()" class="text-[10px] font-mono text-fern-dark hover:underline font-bold px-1.5 py-0.5 rounded hover:bg-emerald-100">
              [Change Shelf]
            </button>
          </div>

          <!-- Setup Card (shown when unanchored or when editing station) -->
          <div id="stationSetupCard" class="space-y-1.5">
            <div class="flex items-center justify-between">
              <span class="font-mono text-[10.5px] font-bold text-fern-dark flex items-center gap-1">
                <span>📍</span>
                <span>Active Audit Station</span>
              </span>
              <button type="button" onclick="dismissStationSetup()" class="text-[10px] font-mono text-muted hover:text-ink">
                Skip & Browse
              </button>
            </div>
            <div class="grid grid-cols-4 gap-1.5 text-xs font-mono">
              <div class="col-span-2 bg-white rounded border border-bordercol px-2 py-0.5">
                <span class="text-[9px] uppercase font-bold text-muted block">Bldg</span>
                <select id="launchBldgSelect" class="w-full bg-transparent font-bold text-ink outline-none text-xs">
                  <option value="Lid's hus">Lid's hus</option>
                  <option value="Økern">Økern</option>
                </select>
              </div>
              <div class="bg-white rounded border border-bordercol px-2 py-0.5">
                <span class="text-[9px] uppercase font-bold text-muted block">Cab</span>
                <input type="text" inputmode="numeric" id="launchCabInput" placeholder="21" class="w-full bg-transparent font-bold text-ink outline-none text-xs" />
              </div>
              <div class="bg-white rounded border border-bordercol px-2 py-0.5">
                <span class="text-[9px] uppercase font-bold text-muted block">Shelf</span>
                <input type="text" inputmode="numeric" id="launchShelfInput" placeholder="01" class="w-full bg-transparent font-bold text-ink outline-none text-xs" />
              </div>
            </div>
            <button type="button" onclick="applyStationSetup()" class="w-full py-1.5 px-3 bg-fern hover:bg-fern-dark text-white rounded text-xs font-mono font-bold shadow-2xs tap-active flex items-center justify-center gap-1.5">
              <span>🚀 Arm Station & Audit</span>
            </button>
          </div>
        </div>

        <!-- 1c. Vault Storage Location Quick Filter Bar (Collapsed by default during inventory) -->
        <div id="storageLocationFilterBar" class="hidden px-3.5 py-1.5 bg-stone-50 border-t border-stone-200 flex items-center gap-2">
          <span class="text-[11px] font-mono font-semibold text-ink-muted shrink-0">📍 Vault Loc:</span>
          <div class="flex-1 flex items-center gap-1.5 min-w-0">
            <select id="quickFilterCabinet" onchange="handleLocationFilterChange()" class="flex-1 min-w-0 bg-white border border-stone-300 rounded px-2 py-1 text-xs font-mono text-ink outline-none focus:border-fern">
              <option value="">All Cabinets</option>
            </select>
            <select id="quickFilterShelf" onchange="handleLocationFilterChange()" class="flex-1 min-w-0 bg-white border border-stone-300 rounded px-2 py-1 text-xs font-mono text-ink outline-none focus:border-fern">
              <option value="">All Shelves</option>
            </select>
            <button type="button" id="btnClearLocFilter" onclick="clearLocationFilter()" class="hidden text-xs text-stone-500 hover:text-stone-800 px-1 font-bold">✕</button>
          </div>
        </div>

        <!-- 2. Filter Pills Bar (Hidden by Default, Toggleable in Settings) -->
        <div id="filterPillsContainer" class="hidden px-3.5 pb-2 overflow-x-auto no-scrollbar flex items-center space-x-1.5 border-t border-stone-100 pt-2">
          <button onclick="setStatusFilter('all')" id="pill-all" class="filter-pill whitespace-nowrap px-2.5 py-1 rounded-full text-[11px] font-medium font-sans bg-ink text-white shadow-sm tap-active transition-all">
            All <span class="font-mono text-[10px] ml-0.5 opacity-90" id="pillCountAll">(0)</span>
          </button>
          <button onclick="setStatusFilter('pending')" id="pill-pending" class="filter-pill whitespace-nowrap px-2.5 py-1 rounded-full text-[11px] font-medium font-sans bg-stone-200/80 text-ink-muted hover:bg-stone-300 tap-active transition-all">
            🕒 Unreviewed <span class="font-mono text-[10px] ml-0.5" id="pillCountPending">(0)</span>
          </button>
          <button onclick="setStatusFilter('flagged')" id="pill-flagged" class="filter-pill whitespace-nowrap px-2.5 py-1 rounded-full text-[11px] font-medium font-sans bg-brick-light text-brick border border-brick/30 hover:bg-red-100 tap-active transition-all">
            ⚠ Flagged <span class="font-mono text-[10px] ml-0.5 font-bold" id="pillCountFlagged">(0)</span>
          </button>
          <button onclick="setStatusFilter('reviewed')" id="pill-reviewed" class="filter-pill whitespace-nowrap px-2.5 py-1 rounded-full text-[11px] font-medium font-sans bg-emerald-50 text-fern-dark border border-fern/30 hover:bg-emerald-100 tap-active transition-all">
            ✓ Reviewed <span class="font-mono text-[10px] ml-0.5" id="pillCountReviewed">(0)</span>
          </button>
          <button onclick="setStatusFilter('conflict')" id="pill-conflict" class="filter-pill whitespace-nowrap px-2.5 py-1 rounded-full text-[11px] font-medium font-sans bg-sky-50 text-sky-800 border border-sky-200 hover:bg-sky-100 tap-active transition-all">
            🔀 Conflicts <span class="font-mono text-[10px] ml-0.5" id="pillCountConflict">(0)</span>
          </button>
          <button onclick="setStatusFilter('unknown')" id="pill-unknown" class="filter-pill whitespace-nowrap px-2.5 py-1 rounded-full text-[11px] font-medium font-sans bg-amber-50 text-amber-900 border border-amber-200 hover:bg-amber-100 tap-active transition-all">
            ? Unknown <span class="font-mono text-[10px] ml-0.5" id="pillCountUnknown">(0)</span>
          </button>
          <button onclick="toggleNoImageFilter()" id="pill-no-image" class="filter-pill whitespace-nowrap px-2.5 py-1 rounded-full text-[11px] font-medium font-sans bg-stone-100 text-stone-600 border border-stone-200 hover:bg-stone-200 tap-active transition-all">
            📷 No Image
          </button>
        </div>

        <!-- Metrics & Sort Row -->
        <div class="px-3.5 py-2 bg-alabaster/70 border-t border-bordercol flex items-center justify-between text-[11px]">
          <div class="flex items-center gap-2 font-mono text-ink-muted">
            <span>Showing <span class="font-bold text-ink" id="matchingCount">0</span> matching records</span>
            <button type="button" id="btnOpenStationSetup" onclick="openStationSetup()" class="hidden text-[10px] font-mono font-bold text-fern-dark hover:underline px-1.5 py-0.5 rounded bg-emerald-50 border border-fern/30">
              📍 Set Target Shelf
            </button>
          </div>
          <div class="flex items-center space-x-1.5">
            <div class="relative inline-flex items-center">
              <select id="sortBySelect" onchange="handleSortChange()" class="appearance-none bg-white border border-bordercol rounded-md px-2 py-1 pr-6 text-[10.5px] font-mono text-ink focus:outline-none focus:border-fern shadow-2xs cursor-pointer">
                <option value="id_asc" selected>Accession ID (0894...)</option>
                <option value="location">⇅ Sort: Physical Location</option>
                <option value="name_asc">Scientific Name (A–Z)</option>
                <option value="name_desc">Scientific Name (Z–A)</option>
                <option value="flagged_first">Flagged / Problems First</option>
              </select>
              <div class="absolute right-1.5 pointer-events-none text-ink-faint">
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M19 9l-7 7-7-7" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/></svg>
              </div>
            </div>
          </div>
        </div>
      </header>

      <!-- 3. Specimen Card Feed -->
      <main class="flex-1 p-3.5 space-y-2.5 overflow-y-auto pb-24" id="specimenListContainer">
        <!-- Injected via JS -->
      </main>

      <!-- 4. Bottom Vault Progress Dock -->
      <footer class="sticky bottom-0 z-40 bg-surface/95 backdrop-blur-md border-t border-bordercol px-4 py-2.5 shadow-dock">
        <div class="flex items-center justify-between text-xs mb-1.5">
          <div class="flex items-center space-x-1.5 font-mono text-[11px]">
            <span class="w-2 h-2 rounded-full bg-fern inline-block"></span>
            <span class="text-ink font-semibold" id="listProgressText">0 / 0 Reviewed</span>
            <span class="text-ink-muted" id="listProgressPct">(0%)</span>
          </div>
          <div class="text-[10px] font-mono text-ink-muted flex items-center space-x-1">
            <svg class="w-3 h-3 text-fern" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7" stroke-linecap="round" stroke-linejoin="round"/></svg>
            <span>Auto-sync ready</span>
          </div>
        </div>
        <div class="w-full bg-stone-200 h-1.5 rounded-full overflow-hidden">
          <div class="bg-fern h-full transition-all duration-300 rounded-full" id="listProgressBar" style="width: 0%;"></div>
        </div>
      </footer>
    </div>


    <!-- ============================================================= -->
    <!-- SCREEN 2: SPECIMEN DETAIL VIEW (#detailView)                  -->
    <!-- ============================================================= -->
    <div id="detailView" class="hidden flex-1 flex flex-col h-full bg-alabaster overflow-hidden relative font-sans text-ink">
      <!-- 1. Sticky Top Navigation Bar -->
      <header class="flex-none bg-surface border-b border-bordercol px-3.5 py-2.5 flex items-center justify-between z-30">
        <!-- Back Button -->
        <button type="button" onclick="showListView()" class="flex items-center gap-1.5 px-2 py-1.5 min-h-[36px] -ml-1 text-xs font-semibold text-muted hover:text-ink active:bg-stone-100 rounded transition-colors tap-highlight-transparent">
          <svg class="w-4 h-4 text-ink stroke-[2.2]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path d="M15.75 19.5L8.25 12l7.5-7.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span class="font-mono">Vault List</span>
        </button>

        <!-- Steppers & Controls -->
        <div class="flex items-center gap-1.5">
          <!-- Detail Undo Button -->
          <button id="btnDetailUndo" onclick="undoLastEdit()" title="Undo edit" class="items-center gap-1 px-2 py-1 h-[32px] text-[10.5px] font-mono font-medium text-ember bg-orange-50 border border-orange-200 rounded active:scale-95 transition-all flex">
            <svg class="w-3.5 h-3.5 stroke-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path d="M9 15L3 9m0 0l6-6M3 9h12a6 6 0 010 12h-3" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>Undo</span>
          </button>

          <!-- Specimen Index Counter -->
          <span class="text-[11px] font-mono font-medium text-subdued tracking-tight bg-stone-100 px-2 py-1.5 rounded border border-bordercol/60">
            <span class="text-ink font-semibold" id="detailCurrentIdx">1</span><span class="text-stone-400 mx-0.5">/</span><span id="detailTotalCount">1</span>
          </span>

          <!-- Next / Prev Steppers -->
          <div class="inline-flex rounded border border-bordercol bg-alabaster p-0.5 shadow-2xs">
            <button type="button" class="w-7 h-7 flex items-center justify-center rounded hover:bg-surface text-ink active:bg-stone-200 transition-colors tap-highlight-transparent" onclick="navSpecimen(-1)" title="Previous Specimen">
              <svg class="w-4 h-4 stroke-[2.2]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M15 19l-7-7 7-7" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </button>
            <div class="w-[1px] bg-bordercol my-0.5"></div>
            <button type="button" class="w-7 h-7 flex items-center justify-center rounded hover:bg-surface text-ink active:bg-stone-200 transition-colors tap-highlight-transparent" onclick="navSpecimen(1)" title="Next Specimen">
              <svg class="w-4 h-4 stroke-[2.2]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M9 5l7 7-7 7" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </button>
          </div>
        </div>
      </header>

      <!-- 2. Sticky Specimen Identification Header -->
      <section class="flex-none bg-surface border-b border-bordercol px-4 pt-3 pb-3 z-20 shadow-2xs">
        <div class="flex items-center justify-between mb-1.5">
          <div class="flex items-center gap-2">
            <span class="font-mono text-xs font-bold text-ink tracking-tight px-1.5 py-0.5 bg-stone-100 border border-bordercol rounded" id="detailAccession">
              #2024-BOT-0894
            </span>
          </div>
          <!-- Interactive Status Pill -->
          <button type="button" class="flex items-center gap-1.5 text-[11px] font-mono font-semibold px-2 py-0.5 rounded border transition-colors tap-highlight-transparent bg-amber-50 text-amber-800 border-amber-300" id="badgeStatus" onclick="handleReviewButtonClick()">
            <span class="w-1.5 h-1.5 rounded-full bg-amber-500 animate-pulse" id="badgeStatusDot"></span>
            <span id="badgeStatusText">UNREVIEWED</span>
          </button>
        </div>

        <h1 class="text-[19px] leading-tight font-serif font-semibold italic text-ink tracking-tight flex items-baseline gap-1.5 truncate" id="detailScientificName">
          Betula pendula
        </h1>

        <div class="flex items-center flex-wrap gap-x-2.5 gap-y-0.5 mt-1.5 text-xs text-muted">
          <div class="flex items-center gap-1">
            <span class="text-subdued font-medium">Fam:</span>
            <span class="font-medium text-ink" id="detailFamily">Betulaceae</span>
          </div>
          <span class="text-bordercol">•</span>
          <div class="flex items-center gap-1 font-mono text-[11px]">
            <span class="text-subdued font-sans">Loc:</span>
            <span class="text-ink font-semibold" id="headerLocSummary">Cab 04 · Sh 02 · Fl -1</span>
          </div>
        </div>

        <!-- Armed Target Shelf Action Banner -->
        <div id="armedShelfBanner" class="mt-2 pt-2 border-t border-stone-100 flex items-center justify-between gap-2 text-xs">
          <div class="flex items-center gap-1.5 min-w-0">
            <span class="text-xs">🎯</span>
            <span class="font-mono text-[10px] text-muted truncate">Target Shelf:</span>
            <span class="font-mono text-[11px] font-bold text-fern-dark truncate" id="armedShelfHeaderLabel">None Armed</span>
          </div>
          <button type="button" id="btnStampArmedShelf" onclick="stampArmedLocation()" class="hidden px-2.5 py-1 rounded bg-fern hover:bg-fern-dark text-white font-mono font-bold text-[10px] shadow-2xs tap-active flex items-center gap-1">
            <span>📍</span>
            <span>Stamp Target</span>
          </button>
        </div>
      </section>

      <!-- 3. Segmented Tab Controller (Sticky) -->
      <nav class="flex-none bg-alabaster border-b border-bordercol px-3 pt-2 pb-1.5 z-20">
        <div class="relative bg-stone-200/90 p-1 rounded-[4px] flex items-center justify-between text-xs font-medium text-muted shadow-inner">
          <div class="tab-slider absolute top-1 bottom-1 w-[calc((100%-8px)/3)] bg-surface rounded shadow-sm border border-stone-300 pointer-events-none translate-x-0" id="tabIndicator" style="transform: translateX(0%);"></div>
          <button id="tabBtnDetails" class="tab-btn relative z-10 flex-1 py-1.5 min-h-[36px] flex items-center justify-center gap-1.5 font-semibold text-ink tap-highlight-transparent" data-tab-index="0" onclick="switchDetailTab('details')">
            <svg class="w-3.5 h-3.5 stroke-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
            <span>Details</span>
            <span class="font-mono text-[10px] font-bold px-1.5 rounded-full bg-slate-600 text-white shadow-2xs hidden" id="tabFolioBadge">0</span>
          </button>
          <button id="tabBtnLocation" class="tab-btn relative z-10 flex-1 py-1.5 min-h-[36px] flex items-center justify-center gap-1.5 text-muted tap-highlight-transparent" data-tab-index="1" onclick="switchDetailTab('location')">
            <svg class="w-3.5 h-3.5 stroke-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z"/><path d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z"/></svg>
            <span>Location</span>
            <span class="font-mono text-[10px] font-bold px-1.5 rounded-full shadow-2xs hidden" id="tabLocationBadge"></span>
          </button>
          <button id="tabBtnProblems" class="tab-btn relative z-10 flex-1 py-1.5 min-h-[36px] flex items-center justify-center gap-1.5 text-muted tap-highlight-transparent" data-tab-index="2" onclick="switchDetailTab('problems')">
            <svg class="w-3.5 h-3.5 text-brick stroke-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z"/></svg>
            <span>Problems</span>
            <span class="font-mono text-[10px] font-bold px-1.5 rounded-full bg-brick text-white shadow-2xs hidden" id="tabProblemBadge">0</span>
          </button>
        </div>
      </nav>

      <!-- 4. Horizontal Swipeable Tab Track -->
      <div class="flex-1 overflow-hidden relative" id="swipeArea">
        <div class="h-full flex w-[300%]" id="tabTrack" style="transform: translateX(0%);">

          <!-- ================= TAB 0: DETAILS & ARCHIVAL SCANS ================= -->
          <div class="w-1/3 h-full overflow-y-auto no-scrollbar p-4 space-y-3.5 pb-24" id="tabContentDetails">
            <!-- Image Viewer Container -->
            <div class="bg-surface border border-bordercol rounded p-3 shadow-2xs space-y-2" id="photoFolioContainer">
              <div class="flex items-center justify-between">
                <h3 class="text-xs font-bold text-ink uppercase tracking-wider font-sans">Archival Photo Folio</h3>
                <span class="text-[10px] font-mono text-muted" id="photoCountDisplay">0 Photos</span>
              </div>
              <div id="photoMainBox" class="relative w-full h-48 bg-stone-100 rounded border border-bordercol overflow-hidden flex items-center justify-center cursor-pointer" onclick="openPhotoViewerModal()">
                <img id="specimenImg" src="" alt="Specimen Scan" class="w-full h-full object-contain hidden" onload="onPhotoLoaded(this)" onerror="onPhotoError(this)"/>
              </div>
              <div id="photoPlaceholder" class="w-full"></div>
              <div id="photoThumbnailsRow" class="flex items-center gap-2 overflow-x-auto no-scrollbar pt-1">
                <!-- Thumbnails injected dynamically -->
              </div>
            </div>

            <!-- Registration & Observation Metadata Form Fields -->
            <div class="bg-surface border border-bordercol rounded p-3.5 shadow-2xs space-y-3" id="dynamicFormContainer">
              <!-- Form fields injected dynamically from schema -->
            </div>
          </div>

          <!-- ================= TAB 1: LOCATION ================= -->
          <div class="w-1/3 h-full overflow-y-auto no-scrollbar p-4 space-y-3.5 pb-24" id="tabContentLocation">
            <!-- 1. Copy from Previous Bar -->
            <div class="bg-surface border border-bordercol rounded p-2.5 shadow-2xs">
              <button class="w-full py-2.5 px-3 bg-stone-100 hover:bg-stone-200/80 active:bg-stone-300 border border-stone-300 rounded flex items-center justify-between text-left transition-all tap-highlight-transparent min-h-[44px]" id="btnCopyPrevSpecimen" onclick="handleCopyPreviousSpecimen()" type="button">
                <div class="flex items-center gap-2 truncate">
                  <span class="text-base leading-none">📋</span>
                  <div class="truncate">
                    <span class="text-xs font-bold text-ink block truncate" id="copyTitleSpan">Copy from Previous</span>
                    <span class="text-[10px] font-mono text-muted block truncate" id="copySubtitleSpan">Tap to duplicate physical coordinates</span>
                  </div>
                </div>
                <span class="text-[10px] font-mono font-bold px-2 py-1 bg-surface border border-stone-300 text-muted rounded shadow-2xs whitespace-nowrap ml-2">1-Tap Fill</span>
              </button>
            </div>

            <!-- 2. Main Physical Coordinate Audit Card -->
            <section class="bg-stone-50 border border-bordercol rounded-lg p-3 space-y-2.5 shadow-2xs">
              <div class="flex items-center justify-between">
                <div>
                  <h2 class="text-xs font-bold text-ink uppercase tracking-wider font-sans">Physical Coordinate Audit</h2>
                  <p class="text-[10px] font-mono text-subdued">Continuous numeric coordinates · Selected Specimen</p>
                </div>
                <span class="text-[10px] font-mono text-fern font-semibold flex items-center gap-1" id="locSyncIndicator">
                  <svg class="w-3.5 h-3.5 stroke-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M4.5 12.75l6 6 9-13.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
                  Synced
                </span>
              </div>

              <div class="grid grid-cols-2 gap-2">
                <!-- Building (Default blank: --) -->
                <div class="bg-white rounded p-1.5 border border-bordercol flex items-center justify-between">
                  <span class="font-mono text-[9px] uppercase font-bold text-muted">Bldg</span>
                  <select id="detailBuildingSelect" onchange="handleDetailBuildingChange(this.value)" class="bg-transparent font-mono text-xs font-bold text-ink outline-none text-right">
                    <option value="">--</option>
                  </select>
                </div>
                <!-- Floor (Continuous signed integer: -2, -1, 0, 1, 2... or — when unrecorded) -->
                <div class="bg-white rounded p-1.5 border border-bordercol flex items-center justify-between">
                  <span class="font-mono text-[9px] uppercase font-bold text-muted">Floor</span>
                  <div class="flex items-center gap-1">
                    <button type="button" class="w-5 h-5 rounded bg-stone-100 flex items-center justify-center font-mono font-bold text-xs" onclick="adjustCoordinate('floor', -1)">−</button>
                    <span class="font-mono text-xs font-bold text-ink px-1 min-w-[20px] text-center" id="detailFloorVal">—</span>
                    <button type="button" class="w-5 h-5 rounded bg-stone-100 flex items-center justify-center font-mono font-bold text-xs" onclick="adjustCoordinate('floor', 1)">+</button>
                  </div>
                </div>
                <!-- Cabinet (01, 02... or — when unrecorded) -->
                <div class="bg-white rounded p-2 border border-bordercol flex items-center justify-between">
                  <span class="font-mono text-[10px] uppercase font-bold text-muted">Cabinet</span>
                  <div class="flex items-center gap-1.5">
                    <button type="button" class="w-6 h-6 rounded bg-stone-100 flex items-center justify-center font-mono font-bold text-sm" onclick="adjustCoordinate('cab', -1)">−</button>
                    <input type="text" inputmode="numeric" pattern="[0-9]*" id="detailCabVal"
                      class="font-mono text-sm font-bold text-ink w-9 text-center bg-transparent border-b border-bordercol/30 focus:border-fern focus:bg-stone-50 rounded-xs outline-none transition-colors"
                      placeholder="—"
                      onclick="this.select()"
                      onfocus="this.select()"
                      onkeydown="if(event.key==='Enter') this.blur();"
                      onchange="handleDirectCoordinateInput('cab', this.value)"
                      onblur="handleDirectCoordinateBlur('cab', this)" />
                    <button type="button" class="w-6 h-6 rounded bg-stone-100 flex items-center justify-center font-mono font-bold text-sm" onclick="adjustCoordinate('cab', 1)">+</button>
                  </div>
                </div>
                <!-- Shelf (Highlighted Fern Border, 01, 02... or — when unrecorded) -->
                <div class="bg-white rounded p-2 border-2 border-fern flex items-center justify-between">
                  <span class="font-mono text-[10px] uppercase font-bold text-fern-dark">Shelf</span>
                  <div class="flex items-center gap-1.5">
                    <button type="button" class="w-6 h-6 rounded bg-stone-100 flex items-center justify-center font-mono font-bold text-sm" onclick="adjustCoordinate('shelf', -1)">−</button>
                    <input type="text" inputmode="numeric" pattern="[0-9]*" id="detailShelfVal"
                      class="font-mono text-sm font-bold text-fern-dark w-9 text-center bg-transparent border-b border-fern/40 focus:border-fern focus:bg-emerald-50/50 rounded-xs outline-none transition-colors"
                      placeholder="—"
                      onclick="this.select()"
                      onfocus="this.select()"
                      onkeydown="if(event.key==='Enter') this.blur();"
                      onchange="handleDirectCoordinateInput('shelf', this.value)"
                      onblur="handleDirectCoordinateBlur('shelf', this)" />
                    <button type="button" class="w-6 h-6 rounded bg-stone-100 flex items-center justify-center font-mono font-bold text-sm" onclick="adjustCoordinate('shelf', 1)">+</button>
                  </div>
                </div>
              </div>

              <!-- Stored As Pill Carousel (Config-Driven) -->
              <div class="pt-1">
                <div class="flex items-center justify-between mb-1">
                  <span class="font-mono text-[9px] uppercase text-muted font-bold">Stored As</span>
                  <span class="font-mono text-[10px] text-ink font-semibold" id="detailStoredAsLabel">Not Selected</span>
                </div>
                <div class="flex items-center gap-1.5 overflow-x-auto no-scrollbar py-0.5 whitespace-nowrap" id="detailStoredAsPills">
                  <!-- Dynamically populated via renderDetailStoredAsPills -->
                </div>
                <div id="detailStoredAsCustomContainer" class="hidden mt-1.5">
                  <input type="text" id="detailStoredAsCustomInput" oninput="onDetailCustomStorageInput(this.value)" placeholder="Enter custom storage..." class="w-full bg-white border border-bordercol rounded px-2 py-1 text-xs font-mono text-ink focus:outline-none focus:border-fern">
                </div>
              </div>

              <!-- Live Breadcrumb Trail -->
              <div class="bg-stone-100 border border-bordercol/60 rounded px-2.5 py-1.5 flex items-center justify-between text-[11px] font-mono mt-1">
                <div class="flex items-center gap-1 text-ink truncate">
                  <span class="text-subdued uppercase text-[9px] font-sans font-bold">Live:</span>
                  <span class="font-semibold truncate" id="liveLocBreadcrumb">Unrecorded location</span>
                </div>
                <span class="text-[10px] font-mono text-muted whitespace-nowrap ml-1" id="liveLocStatus">Coordinates</span>
              </div>
            </section>

            <!-- 3. Availability / Loan Status Card -->
            <div class="bg-surface border border-bordercol rounded p-3 shadow-2xs space-y-2">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-1.5">
                  <span class="w-2 h-2 rounded-full bg-fern" id="loanStatusDot"></span>
                  <h2 class="text-xs font-bold text-ink uppercase tracking-wider font-sans">Availability Status</h2>
                </div>
                <span class="text-[10px] font-mono font-semibold px-1.5 py-0.5 rounded bg-fern-light text-fern border border-fern/30" id="loanStateTag">In Collection</span>
              </div>
              <div class="grid grid-cols-2 p-1 bg-stone-100 border border-stone-200 rounded gap-1">
                <button class="py-1.5 px-2 rounded text-xs font-mono font-semibold flex items-center justify-center gap-1.5 transition-all bg-white text-ink border border-stone-300 min-h-[36px]" id="btnStatusAvailable" onclick="setLoanStatus(false)" type="button">
                  <svg class="w-3.5 h-3.5 text-fern stroke-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                  <span>In Collection</span>
                </button>
                <button class="py-1.5 px-2 rounded text-xs font-mono font-medium flex items-center justify-center gap-1.5 transition-all text-muted hover:text-ink min-h-[36px]" id="btnStatusLoan" onclick="setLoanStatus(true)" type="button">
                  <svg class="w-3.5 h-3.5 text-amber-600 stroke-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M13.5 6H5.25A2.25 2.25 0 003 8.25v10.5A2.25 2.25 0 005.25 21h10.5A2.25 2.25 0 0018 18.75V10.5m-10.5 6L21 3m0 0h-5.25M21 3v5.25"/></svg>
                  <span>Loaned Out</span>
                </button>
              </div>
            </div>
          </div>

          <!-- ================= TAB 2: PROBLEMS & CONFLICTS ================= -->
          <div class="w-1/3 h-full overflow-y-auto no-scrollbar p-4 space-y-3.5 pb-24" id="tabContentProblems">
            <!-- Quick Flag Button for Physical Damage or Misplacement -->
            <button type="button" onclick="openAddDiscrepancyModal()" class="w-full py-2.5 px-3 bg-amber-50 hover:bg-amber-100 text-amber-900 border border-amber-300 rounded font-bold text-xs flex items-center justify-center gap-1.5 tap-active shadow-2xs">
              <span>⚑</span>
              <span>Flag Specimen Issue (Damaged / Misplaced)</span>
            </button>

            <!-- 1. Problem Summary Banner -->
            <div id="problemSummaryBar" class="flex items-center justify-between p-3 bg-stone-100 border border-bordercol rounded-[3px] transition-colors duration-200">
              <div class="flex items-center gap-2">
                <span id="problemSummaryDot" class="w-2.5 h-2.5 rounded-full bg-stone-400"></span>
                <span id="problemSummaryCountText" class="text-xs font-bold text-ink uppercase font-mono">0 Active Discrepancies</span>
              </div>
              <span id="problemSummaryActionText" class="text-[10px] font-mono text-muted">Checking Data</span>
            </div>

            <!-- 2. Active Discrepancy Conflict Resolver Cards Container -->
            <div id="activeDiscrepanciesContainer" class="space-y-3">
              <!-- Dynamically populated per issue field -->
            </div>

            <!-- 3. Schema Data Integrity Flags Checklist -->
            <div class="bg-surface border border-bordercol rounded-[3px] p-3.5 shadow-2xs space-y-3">
              <div class="flex items-center justify-between border-b border-stone-100 pb-2">
                <div>
                  <h3 class="text-xs font-bold text-ink uppercase tracking-wider font-sans">Data Integrity Flags</h3>
                  <p class="text-[10px] font-mono text-subdued">Direct curatorial problem checklist</p>
                </div>
                <span class="text-[10px] font-mono text-muted" id="flaggedTotalBadge">0 Flagged</span>
              </div>
              <div class="grid grid-cols-2 gap-2" id="problemFlagsGrid">
                <!-- Dynamically populated from schema.ui_sections.problems -->
              </div>
            </div>
          </div>

        </div>
      </div>

      <!-- Sticky Action Bar in Detail View: Mark Reviewed & Flag Issue -->
      <footer class="flex-none bg-surface border-t border-bordercol px-4 py-2.5 shadow-[0_-2px_10px_rgba(0,0,0,0.05)] z-30">
        <div class="flex items-center justify-between gap-3">
          <button
            type="button"
            id="btnDetailMarkReviewed"
            onclick="handleReviewButtonClick()"
            class="flex-1 py-2.5 px-4 rounded font-sans font-bold text-xs flex items-center justify-center gap-2 border transition-all tap-active bg-emerald-50 text-fern-dark border-fern hover:bg-emerald-100"
          >
            <span id="btnDetailReviewedIcon" class="text-sm">✓</span>
            <span id="btnDetailReviewedLabel">Mark Reviewed</span>
          </button>
          <button
            type="button"
            onclick="openAddDiscrepancyModal()"
            class="px-3.5 py-2.5 bg-amber-50 hover:bg-amber-100 text-amber-900 border border-amber-300 rounded font-sans font-semibold text-xs flex items-center justify-center gap-1.5 tap-active"
            title="Flag Physical Issue"
          >
            <span>⚑</span>
            <span>Flag Issue</span>
          </button>
        </div>
        <p id="reviewHelperText" class="text-[10px] font-sans text-subdued text-center mt-1.5 truncate"></p>
      </footer>
    </div>


    <!-- ============================================================= -->
    <!-- SCREEN 3: BATCH LOCATION REGISTRATOR (#batchLocationView)     -->
    <!-- ============================================================= -->
    <div id="batchLocationView" class="hidden flex-1 flex flex-col h-full bg-surface overflow-hidden relative font-sans text-ink">
      <!-- 1. Batch Header -->
      <header class="flex-none bg-surface/90 backdrop-blur-md border-b border-bordercol px-3.5 py-3 flex items-center justify-between z-30 shadow-2xs">
        <div class="flex items-center gap-2 min-w-0">
          <button type="button" onclick="showListView()" class="min-h-[38px] min-w-[38px] flex items-center justify-center text-ink hover:text-fern active:scale-95">
            <svg class="w-5 h-5 stroke-[2.2]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M15.75 19.5L8.25 12l7.5-7.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </button>
          <div class="flex flex-col min-w-0">
            <span class="font-serif font-bold text-sm text-ink leading-tight truncate">Batch Location Registrator</span>
            <span class="font-mono text-[10px] text-muted truncate">Rapid shelf assignment · Active Collection</span>
          </div>
        </div>
        <div class="flex items-center gap-1.5">
          <button id="btnBatchWakeLock" onclick="toggleWakeLock()" title="Keep screen awake during audit" class="w-8 h-8 rounded-md bg-stone-100 border border-stone-200 text-stone-600 hover:text-ink flex items-center justify-center tap-active transition-colors">
            <span id="batchWakeLockIcon" class="text-xs">🌙</span>
          </button>
          <div class="flex items-center gap-1 px-2 py-1 rounded-full bg-emerald-50 border border-emerald-200 text-[10.5px] font-mono text-emerald-800">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
            <span>Live</span>
          </div>
        </div>
      </header>

      <!-- 2. Scrollable Batch Workflow -->
      <main class="flex-1 overflow-y-auto p-3.5 space-y-3 pb-36">
        <!-- Target Shelf Anchor Card -->
        <section class="bg-stone-50 border border-bordercol rounded-lg p-3 space-y-2.5 shadow-2xs">
          <div class="flex items-center justify-between gap-2">
            <span class="font-mono text-[10px] uppercase font-bold text-subdued tracking-wider">Target Physical Anchor</span>
            <div class="flex items-center gap-1.5">
              <button type="button" id="btnBatchCopyArmed" onclick="copyArmedShelfToBatch()" class="hidden px-2 py-0.5 rounded bg-fern-light border border-fern/40 text-fern-dark font-mono font-bold text-[10px] tap-active">⚡ Use Armed Shelf</button>
              <span class="font-mono text-[10px] text-fern font-bold">🔒 Locked Shelf Target</span>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-2">
            <!-- Building -->
            <div class="bg-white rounded p-1.5 border border-bordercol flex items-center justify-between">
              <span class="font-mono text-[9px] uppercase font-bold text-muted">Bldg</span>
              <select id="batchBuildingSelect" onchange="handleBatchBuildingChange(this.value)" class="bg-transparent font-mono text-xs font-bold text-ink outline-none text-right">
                <option value="">--</option>
              </select>
            </div>
            <!-- Floor (Continuous signed integer) -->
            <div class="bg-white rounded p-1.5 border border-bordercol flex items-center justify-between">
              <span class="font-mono text-[9px] uppercase font-bold text-muted">Floor</span>
              <div class="flex items-center gap-1">
                <button type="button" class="w-5 h-5 rounded bg-stone-100 flex items-center justify-center font-mono font-bold text-xs" onclick="adjustBatchCoord('floor', -1)">−</button>
                <span class="font-mono text-xs font-bold text-ink px-1 min-w-[20px] text-center" id="batchFloorVal">—</span>
                <button type="button" class="w-5 h-5 rounded bg-stone-100 flex items-center justify-center font-mono font-bold text-xs" onclick="adjustBatchCoord('floor', 1)">+</button>
              </div>
            </div>
            <!-- Cabinet -->
            <div class="bg-white rounded p-2 border border-bordercol flex items-center justify-between">
              <span class="font-mono text-[10px] uppercase font-bold text-muted">Cabinet</span>
              <div class="flex items-center gap-1.5">
                <button type="button" class="w-6 h-6 rounded bg-stone-100 flex items-center justify-center font-mono font-bold text-sm" onclick="adjustBatchCoord('cab', -1)">−</button>
                <input type="text" inputmode="numeric" pattern="[0-9]*" id="batchCabVal"
                  class="font-mono text-sm font-bold text-ink w-9 text-center bg-transparent border-b border-bordercol/30 focus:border-fern focus:bg-stone-50 rounded-xs outline-none transition-colors"
                  placeholder="—"
                  onclick="this.select()"
                  onfocus="this.select()"
                  onkeydown="if(event.key==='Enter') this.blur();"
                  onchange="handleDirectBatchCoordInput('cab', this.value)"
                  onblur="handleDirectBatchCoordBlur('cab', this)" />
                <button type="button" class="w-6 h-6 rounded bg-stone-100 flex items-center justify-center font-mono font-bold text-sm" onclick="adjustBatchCoord('cab', 1)">+</button>
              </div>
            </div>
            <!-- Shelf -->
            <div class="bg-white rounded p-2 border-2 border-fern flex items-center justify-between">
              <span class="font-mono text-[10px] uppercase font-bold text-fern-dark">Shelf</span>
              <div class="flex items-center gap-1.5">
                <button type="button" class="w-6 h-6 rounded bg-stone-100 flex items-center justify-center font-mono font-bold text-sm" onclick="adjustBatchCoord('shelf', -1)">−</button>
                <input type="text" inputmode="numeric" pattern="[0-9]*" id="batchShelfVal"
                  class="font-mono text-sm font-bold text-fern-dark w-9 text-center bg-transparent border-b border-fern/40 focus:border-fern focus:bg-emerald-50/50 rounded-xs outline-none transition-colors"
                  placeholder="—"
                  onclick="this.select()"
                  onfocus="this.select()"
                  onkeydown="if(event.key==='Enter') this.blur();"
                  onchange="handleDirectBatchCoordInput('shelf', this.value)"
                  onblur="handleDirectBatchCoordBlur('shelf', this)" />
                <button type="button" class="w-6 h-6 rounded bg-stone-100 flex items-center justify-center font-mono font-bold text-sm" onclick="adjustBatchCoord('shelf', 1)">+</button>
              </div>
            </div>
          </div>

          <!-- Stored As Pill Carousel -->
          <div class="pt-1">
            <div class="flex items-center justify-between mb-1">
              <span class="font-mono text-[9px] uppercase text-muted font-bold">Stored As</span>
              <span class="font-mono text-[10px] text-ink font-semibold" id="batchStoredAsLabel">Not Selected</span>
            </div>
            <div class="flex items-center gap-1.5 overflow-x-auto no-scrollbar py-0.5 whitespace-nowrap" id="batchStoredAsPills">
              <!-- Dynamically populated via renderBatchStoredAsPills -->
            </div>
            <div id="batchStoredAsCustomContainer" class="hidden mt-1.5">
              <input type="text" id="batchStoredAsCustomInput" placeholder="Enter custom storage..." class="w-full bg-white border border-bordercol rounded px-2 py-1 text-xs font-mono text-ink focus:outline-none focus:border-fern">
            </div>
          </div>
        </section>

        <!-- Advance to Next Shelf Button -->
        <button type="button" id="btnAdvanceNextShelf" onclick="advanceToNextShelf()" class="w-full py-2.5 px-3 bg-stone-100 hover:bg-emerald-50 text-ink hover:text-fern-dark rounded-lg border border-bordercol hover:border-fern/50 font-mono text-xs font-bold flex items-center justify-center gap-2 shadow-2xs tap-active transition-all">
          <svg class="w-4 h-4 text-fern stroke-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M4.5 10.5L12 3m0 0l7.5 7.5M12 3v18" stroke-linecap="round" stroke-linejoin="round"/></svg>
          <span id="btnAdvanceNextShelfText">Advance to Shelf 03</span>
        </button>

        <!-- Rapid Object ID Input Bar -->
        <section class="space-y-1">
          <label for="batchIdInput" class="font-mono text-[10px] uppercase text-muted font-bold flex items-center justify-between">
            <span>Type Object ID</span>
            <span class="text-fern lowercase">press enter to add</span>
          </label>
          <div class="relative flex items-center bg-white rounded-lg shadow-sm border border-bordercol focus-within:border-fern">
            <span class="pl-3 text-ink-faint font-mono text-xs">#</span>
            <input 
              type="text" 
              inputmode="numeric"
              id="batchIdInput" 
              placeholder="e.g. 0894 or 2024-BOT-0894..." 
              onkeydown="if(event.key==='Enter')addBatchItemFromInput()"
              autocomplete="off"
              class="w-full bg-transparent font-mono text-sm text-ink placeholder:text-stone-400 py-2.5 px-2 focus:outline-none"
            >
            <button type="button" id="btnBatchKeyboardMode" onclick="toggleBatchInputMode()" title="Switch between numeric (123) and text (ABC) keypad" class="px-2 py-1 rounded bg-stone-100 border border-stone-200 font-mono text-[10px] font-bold text-muted hover:text-ink tap-active">123</button>
            <button type="button" onclick="addBatchItemFromInput()" class="m-1 px-3 py-1.5 bg-fern hover:bg-fern-dark text-white rounded font-mono font-bold text-xs flex items-center gap-1 shadow-sm tap-active">
              <span>⏎</span>
              <span>Add</span>
            </button>
          </div>
        </section>

        <!-- Live Session Batch Stream -->
        <section class="space-y-2">
          <div class="flex items-center justify-between py-1 border-b border-stone-100">
            <div class="flex items-center gap-1.5">
              <span class="font-serif font-bold text-xs text-ink">Staged Specimens</span>
              <span class="font-mono text-[11px] text-fern font-bold" id="batchQueueCount">(0 items)</span>
            </div>
            <button type="button" onclick="clearBatchQueue()" class="text-[11px] font-mono text-brick hover:underline">
              Clear All
            </button>
          </div>

          <div class="space-y-2" id="batchStreamList">
            <!-- Dynamically populated batch items -->
            <div class="p-6 text-center text-stone-400 font-mono text-xs" id="batchEmptyPlaceholder">
              No items queued yet.<br>Type an Object ID above to begin.
            </div>
          </div>
        </section>
      </main>

      <!-- 3. Sticky Bottom Commit Bar -->
      <footer class="fixed bottom-0 inset-x-0 z-40 bg-surface/95 backdrop-blur-md border-t border-bordercol px-4 py-3 shadow-dock max-w-[440px] mx-auto">
        <div class="flex items-center justify-between gap-3">
          <div class="flex flex-col">
            <span class="font-mono text-[10px] text-muted uppercase">Ready to Sync</span>
            <span class="font-mono text-xs font-bold text-ink" id="batchCommitSummary">0 Accessions Queued</span>
          </div>
          <button type="button" onclick="commitBatchLocationUpdate()" class="flex-1 py-3 bg-fern hover:bg-fern-dark text-white font-sans font-bold text-xs rounded-lg flex items-center justify-center gap-2 shadow-sm tap-active transition-all">
            <svg class="w-4 h-4 stroke-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M12 16.5V9.75m0 0l3 3m-3-3l-3 3M6.75 19.5a4.5 4.5 0 01-1.41-8.775 5.25 5.25 0 0110.233-2.33 3 3 0 013.758 3.848A3.752 3.752 0 0118 19.5H6.75z"/></svg>
            <span>Commit Batch</span>
          </button>
        </div>
      </footer>
    </div>


    <!-- ============================================================= -->
    <!-- MODALS                                                        -->
    <!-- ============================================================= -->

    <!-- MODAL: Armed Shelf Confirmation (Non-Coercive) -->
    <div id="armedConfirmModal" class="hidden fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4">
      <div class="bg-surface border border-bordercol rounded-lg w-full max-w-sm shadow-xl overflow-hidden animate-in fade-in zoom-in-95 duration-150">
        <header class="p-3.5 bg-stone-100 border-b border-bordercol flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="text-base">📍</span>
            <h2 class="font-sans font-bold text-sm text-ink">Apply Armed Location?</h2>
          </div>
          <button type="button" onclick="cancelArmedModal()" class="text-ink-muted hover:text-ink font-bold text-sm">✕</button>
        </header>
        <div class="p-4 space-y-3.5">
          <p class="text-xs text-muted leading-relaxed">
            This specimen's registered location does not match your active audit target shelf.
          </p>
          <div class="space-y-2 bg-stone-50 p-3 rounded border border-bordercol/70 text-xs font-mono">
            <div class="flex items-center justify-between">
              <span class="text-muted">Current Record:</span>
              <span class="font-bold text-ink" id="armedModalCurLoc">Unrecorded</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-fern-dark font-bold">Armed Target:</span>
              <span class="font-bold text-fern-dark" id="armedModalTargetLoc">Cabinet 21, Shelf 02</span>
            </div>
          </div>
          <p class="text-[11px] text-muted italic">
            You can stamp the armed shelf or keep the existing/blank location. Both choices will safely mark the specimen reviewed.
          </p>
          <div class="space-y-2 pt-1">
            <button type="button" id="btnConfirmStampAndReview" onclick="confirmStampAndReview()" class="w-full py-2.5 px-3 bg-fern hover:bg-fern-dark text-white rounded font-sans font-bold text-xs flex items-center justify-center gap-1.5 shadow-sm tap-active transition-all">
              <span>✓ Yes, Stamp to Target & Review</span>
            </button>
            <button type="button" id="btnConfirmKeepAndReview" onclick="confirmKeepAndReview()" class="w-full py-2.5 px-3 bg-stone-100 hover:bg-stone-200 text-ink border border-stone-300 rounded font-sans font-bold text-xs flex items-center justify-center gap-1.5 tap-active transition-all">
              <span>✕ No, Keep Location & Review</span>
            </button>
            <button type="button" onclick="cancelArmedModal()" class="w-full py-1.5 text-center text-xs text-muted hover:text-ink font-sans">
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- MODAL: Settings -->
    <div id="settingsModal" class="hidden fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4">
      <div class="bg-surface border border-bordercol rounded w-full max-w-sm shadow-xl overflow-hidden animate-in fade-in zoom-in-95 duration-150">
        <header class="p-3.5 bg-tonal1 border-b border-tonal2 flex items-center justify-between">
          <h2 class="font-serif font-bold text-sm text-ink">Application Settings</h2>
          <button type="button" onclick="closeSettingsModal()" class="text-ink-muted hover:text-ink font-bold text-sm">✕</button>
        </header>
        <div class="p-4 space-y-4">
          <!-- Toggle Filter Pills on List View -->
          <div class="flex items-center justify-between p-2.5 bg-stone-50 border border-bordercol rounded">
            <div>
              <span class="block font-sans text-xs font-bold text-ink">Quick Filter Pills</span>
              <span class="block font-sans text-[10px] text-muted">Show horizontal filter pills on Vault List</span>
            </div>
            <input type="checkbox" id="settingShowFilterPills" onchange="toggleFilterPillsSetting(this.checked)" class="w-4 h-4 text-fern rounded border-bordercol focus:ring-fern">
          </div>

          <!-- Tactile Haptic Feedback (Adjustable & Toggleable) -->
          <div class="p-2.5 bg-stone-50 border border-bordercol rounded space-y-2">
            <div class="flex items-center justify-between">
              <div>
                <span class="block font-sans text-xs font-bold text-ink">Tactile Haptic Feedback</span>
                <span class="block font-sans text-[10px] text-muted">Vibrate on steppers, toggles, and flags</span>
              </div>
              <input type="checkbox" id="settingEnableHaptics" onchange="toggleHapticsSetting(this.checked)" class="w-4 h-4 text-fern rounded border-bordercol focus:ring-fern">
            </div>

            <!-- Intensity Segmented Control & Test Button -->
            <div id="hapticsIntensityContainer" class="pt-1.5 border-t border-stone-200/60 flex items-center justify-between gap-2">
              <div class="flex items-center rounded border border-bordercol overflow-hidden text-[10px] font-sans">
                <button type="button" onclick="setHapticsIntensity('light')" id="btnHapticLight" class="px-2 py-1 bg-surface text-ink hover:bg-stone-100 transition-all">Light</button>
                <button type="button" onclick="setHapticsIntensity('medium')" id="btnHapticMedium" class="px-2 py-1 bg-fern text-white font-bold transition-all">Medium</button>
                <button type="button" onclick="setHapticsIntensity('strong')" id="btnHapticStrong" class="px-2 py-1 bg-surface text-ink hover:bg-stone-100 transition-all">Strong</button>
              </div>
              <button type="button" onclick="testHapticFeedback()" class="px-2.5 py-1 text-[10px] font-mono font-semibold bg-stone-200/80 hover:bg-stone-300 text-stone-700 rounded active:scale-95 transition-all">
                ⚡ Test
              </button>
            </div>

            <!-- iOS Safari Fallback Note -->
            <p id="hapticsUnsupportedNote" class="hidden text-[9.5px] font-mono text-amber-700 bg-amber-50 p-1 rounded">
              ℹ️ Web Vibration API is not supported on iOS Safari.
            </p>
          </div>

          <div>
            <label class="block font-sans text-xs font-medium text-ink mb-1">Image URL Pattern Override</label>
            <input type="text" id="settingImageUrlPattern" placeholder="e.g. https://example.com/{id}.jpg" class="w-full bg-surface border border-bordercol rounded px-2.5 py-1.5 text-xs text-ink outline-none focus:border-fern">
            <p class="text-[10px] text-ink-muted mt-1">Available tokens: {id}, {num}, {num:04d}, {suffix}.</p>
          </div>

          <!-- ICEDIG Botanical Missing Data Standards Reference -->
          <div class="p-2.5 bg-stone-50 border border-bordercol rounded space-y-1.5">
            <span class="block font-sans text-xs font-bold text-ink">🌿 ICEDIG Missing Data Standards</span>
            <p class="font-sans text-[10px] text-muted">Use standard markers when label info is missing or obscure:</p>
            <div class="space-y-1 font-mono text-[10px]">
              <div class="flex justify-between items-center py-0.5 border-b border-stone-200/60">
                <span class="text-fern font-bold">unknown:missing</span>
                <span class="text-ink-muted text-[9.5px]">Omitted on label</span>
              </div>
              <div class="flex justify-between items-center py-0.5 border-b border-stone-200/60">
                <span class="text-fern font-bold">unknown:indecipherable</span>
                <span class="text-ink-muted text-[9.5px]">Illegible / damaged</span>
              </div>
              <div class="flex justify-between items-center py-0.5 border-b border-stone-200/60">
                <span class="text-fern font-bold">unknown:undigitized</span>
                <span class="text-ink-muted text-[9.5px]">Skipped during digitizing</span>
              </div>
              <div class="flex justify-between items-center py-0.5">
                <span class="text-fern font-bold">withheld</span>
                <span class="text-ink-muted text-[9.5px]">Conservation / legal</span>
              </div>
            </div>
          </div>

          <div class="pt-2 border-t border-tonal2 flex items-center justify-between gap-2">
            <button type="button" onclick="closeSettingsModal(); openWalkthroughModal(0);" class="px-2.5 py-1.5 border border-fern/40 bg-fern-light text-fern hover:bg-fern hover:text-white rounded text-[11px] font-bold transition-colors">🎓 3-Step Guide</button>
            <div class="flex items-center gap-2">
              <button type="button" onclick="closeSettingsModal()" class="px-3 py-1.5 border border-bordercol text-ink-muted hover:bg-surface rounded text-xs font-medium">Cancel</button>
              <button type="button" onclick="saveSettings()" class="px-3 py-1.5 bg-fern hover:bg-fern-dark text-white rounded text-xs font-bold">Save</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- MODAL: First-Time 3-Step Hallway Walkthrough -->
    <div id="walkthroughModal" class="hidden fixed inset-0 z-50 bg-black/70 backdrop-blur-xs flex items-center justify-center p-4">
      <div class="bg-surface border border-bordercol rounded-xl shadow-2xl w-full max-w-sm overflow-hidden">
        <div class="px-4 py-3 bg-fern text-white flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="text-base">🎓</span>
            <span class="font-sans font-bold text-xs tracking-wide uppercase">Hallway Quick Guide</span>
          </div>
          <button type="button" onclick="closeWalkthroughModal(true)" class="text-white/80 hover:text-white text-xs font-bold px-2 py-0.5 rounded">Skip</button>
        </div>
        <div class="p-4 space-y-3">
          <div id="walkthroughStepBadge" class="inline-block px-2 py-0.5 rounded-full bg-fern-light text-fern font-mono text-[10px] font-bold">STEP 1 OF 3</div>
          <h3 id="walkthroughTitle" class="font-sans font-bold text-base text-ink leading-snug">Search by Accession Number</h3>
          <p id="walkthroughBody" class="font-sans text-xs text-ink-muted leading-relaxed"></p>
          <div id="walkthroughCallout" class="p-2.5 rounded-lg bg-tonal border border-bordercol font-mono text-[11px] text-ink"></div>
          <div class="flex items-center justify-center gap-1.5 pt-1">
            <span id="wtDot0" class="w-2 h-2 rounded-full bg-fern"></span>
            <span id="wtDot1" class="w-2 h-2 rounded-full bg-stone-300"></span>
            <span id="wtDot2" class="w-2 h-2 rounded-full bg-stone-300"></span>
          </div>
        </div>
        <div class="px-4 py-3 bg-tonal border-t border-bordercol flex items-center justify-between gap-2">
          <button id="wtBackBtn" type="button" onclick="prevWalkthroughSlide()" class="hidden px-3 py-1.5 border border-bordercol bg-surface text-ink-muted rounded text-xs font-semibold">← Back</button>
          <button id="wtNextBtn" type="button" onclick="nextWalkthroughSlide()" class="ml-auto px-4 py-2 bg-fern hover:bg-fern-dark text-white rounded-lg text-xs font-bold shadow-xs">Next →</button>
        </div>
      </div>
    </div>

    <!-- MODAL: Stored As Bottom Sheet -->
    <div id="storedAsBottomSheet" class="hidden fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex flex-col justify-end" onclick="if(event.target===this)closeStoredAsBottomSheet()">
      <div class="bg-surface border-t border-bordercol rounded-t-xl p-4 space-y-3 max-h-[80vh] overflow-y-auto shadow-2xl">
        <div class="flex items-center justify-between pb-2 border-b border-stone-200">
          <div>
            <h3 class="text-xs font-bold text-ink uppercase tracking-wider font-sans">Additional Storage Vessels</h3>
            <p class="text-[10px] font-mono text-subdued">Select botanical archival method</p>
          </div>
          <button class="p-1 text-muted hover:text-ink font-mono text-sm" onclick="closeStoredAsBottomSheet()" type="button">✕</button>
        </div>
        <div class="space-y-1.5 font-mono text-xs" id="storedAsModalOptions">
          <!-- Populated dynamically -->
        </div>
      </div>
    </div>

    <!-- MODAL: Presets Configuration -->
    <div id="presetsConfigModal" class="hidden fixed inset-0 z-50 bg-black/65 backdrop-blur-xs flex items-center justify-center p-4" onclick="if(event.target===this)closePresetsModal()">
      <div class="bg-surface border border-stone-300 rounded-lg max-w-sm w-full p-4 space-y-3.5 shadow-2xl flex flex-col max-h-[88vh]">
        <div class="flex items-center justify-between pb-2 border-b border-stone-200">
          <div>
            <h3 class="text-xs font-bold text-ink uppercase tracking-wider font-sans">Customize Quick-Select</h3>
            <p class="text-[10px] font-mono text-subdued">Select 3 presets for the primary 2x2 grid</p>
          </div>
          <button class="p-1 text-muted hover:text-ink font-mono text-sm" onclick="closePresetsModal()" type="button">✕</button>
        </div>
        <div class="flex items-center justify-between text-[11px] font-mono bg-stone-100 px-2.5 py-1.5 rounded border border-stone-200">
          <span class="text-subdued uppercase text-[9px] font-bold">Selection count:</span>
          <span class="font-bold text-fern" id="presetSelectionCounter">3 of 3 selected</span>
        </div>
        <div class="space-y-1.5 overflow-y-auto no-scrollbar max-h-[50vh] pr-0.5" id="presetsSelectionList">
          <!-- Checkbox list of storage vessels -->
        </div>
        <div class="pt-2 border-t border-stone-200 flex items-center gap-2">
          <button class="flex-1 py-2 px-3 bg-stone-100 hover:bg-stone-200 text-ink text-xs font-mono font-medium rounded min-h-[38px]" onclick="closePresetsModal()" type="button">Cancel</button>
          <button class="flex-1 py-2 px-3 bg-fern hover:bg-fern-dark text-white text-xs font-mono font-semibold rounded min-h-[38px]" id="btnSavePresets" onclick="savePresetsFromModal()" type="button">Save Presets</button>
        </div>
      </div>
    </div>

    <!-- MODAL: Curatorial Advanced Filter -->
    <div id="filterModal" class="hidden fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4">
      <div class="bg-surface border border-bordercol rounded w-full max-w-md shadow-xl overflow-hidden flex flex-col max-h-[90vh]">
        <header class="p-3.5 bg-tonal1 border-b border-tonal2 flex items-center justify-between shrink-0">
          <h2 class="font-serif font-bold text-sm text-ink">Curatorial Advanced Filter</h2>
          <button type="button" onclick="closeFilterModal()" class="text-ink-muted hover:text-ink font-bold text-sm">✕</button>
        </header>
        <div class="p-4 overflow-y-auto space-y-4 flex-1">
          <div>
            <h3 class="font-sans text-xs font-bold text-ink mb-2 uppercase tracking-wider">Spatial Location</h3>
            <div id="filterModalLocations" class="space-y-2"></div>
          </div>
          <hr class="border-t border-tonal2">
          <div>
            <h3 class="font-sans text-xs font-bold text-ink mb-2 uppercase tracking-wider">Specific Problems & Verification</h3>
            <div id="filterModalProblems" class="space-y-1.5"></div>
          </div>
        </div>
        <footer class="p-3.5 bg-tonal1 border-t border-tonal2 flex gap-2 justify-end shrink-0">
          <button type="button" onclick="clearAdvancedFilters()" class="px-3 py-1.5 border border-bordercol text-ink-muted hover:text-ink rounded text-xs">Clear</button>
          <button type="button" onclick="applyAdvancedFilters()" class="px-4 py-1.5 bg-fern hover:bg-fern-dark text-white rounded text-xs font-bold">Apply</button>
        </footer>
      </div>
    </div>

    <!-- MODAL: Add Discrepancy Flag -->
    <div id="addDiscrepancyModal" class="hidden fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4">
      <div class="bg-surface border border-bordercol rounded w-full max-w-sm shadow-xl overflow-hidden">
        <header class="p-3.5 bg-tonal1 border-b border-tonal2 flex items-center justify-between">
          <h2 class="font-serif font-bold text-sm text-ink">⚑ Flag Specimen Discrepancy</h2>
          <button type="button" onclick="closeModal('addDiscrepancyModal')" class="text-ink-muted hover:text-ink font-bold text-sm">✕</button>
        </header>
        <form onsubmit="submitDiscrepancy(event)" class="p-4 space-y-3">
          <div>
            <label class="block font-sans text-xs font-medium text-ink mb-1">Target Field / Problem</label>
            <select id="discrepancyFieldSelect" class="w-full bg-surface border border-bordercol rounded px-2.5 py-1.5 text-xs text-ink outline-none focus:border-fern"></select>
          </div>
          <div>
            <label class="block font-sans text-xs font-medium text-ink mb-1">Discrepancy Note</label>
            <textarea id="discrepancyReasonInput" rows="3" required placeholder="Note observed curatorial discrepancy..." class="w-full bg-surface border border-bordercol rounded px-2.5 py-1.5 text-xs text-ink outline-none focus:border-fern"></textarea>
          </div>
          <div class="flex justify-end gap-2 pt-2 border-t border-tonal2">
            <button type="button" onclick="closeModal('addDiscrepancyModal')" class="px-3 py-1.5 border border-bordercol text-ink-muted rounded text-xs">Cancel</button>
            <button type="submit" class="px-4 py-1.5 bg-ember hover:bg-ember-dark text-white rounded text-xs font-bold">Flag Issue</button>
          </div>
        </form>
      </div>
    </div>

    <!-- MODAL: Edit Comment -->
    <div id="commentEditorModal" class="hidden fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4">
      <div class="bg-surface border border-bordercol rounded w-full max-w-sm shadow-xl overflow-hidden">
        <header class="p-3.5 bg-tonal1 border-b border-tonal2 flex items-center justify-between">
          <div class="flex items-center gap-2 text-fern-dark">
            <svg class="w-4 h-4 text-fern" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z"/></svg>
            <h2 class="font-serif font-bold text-sm text-ink" id="commentModalTitle">Edit Comment</h2>
          </div>
          <button type="button" onclick="closeCommentEditor()" class="text-ink-muted hover:text-ink font-bold text-sm">✕</button>
        </header>
        <div class="p-4 space-y-3">
          <div>
            <label class="block font-sans text-xs font-medium text-ink mb-1">Comment / Curatorial Notes</label>
            <textarea id="commentEditTextarea" rows="6" placeholder="Enter comments or curatorial notes..." class="w-full bg-surface border border-bordercol rounded p-2.5 text-xs font-mono text-ink outline-none focus:border-fern focus:ring-1 focus:ring-fern resize-none leading-relaxed"></textarea>
          </div>
          <div class="flex justify-end gap-2 pt-2 border-t border-tonal2">
            <button type="button" onclick="closeCommentEditor()" class="px-3 py-1.5 border border-bordercol text-ink-muted rounded text-xs font-mono">Cancel</button>
            <button type="button" onclick="saveCommentFromEditor()" class="px-4 py-1.5 bg-fern hover:bg-fern-dark text-white rounded text-xs font-bold font-mono">Save Comment</button>
          </div>
        </div>
      </div>
    </div>

    <!-- MODAL: Photo Fullscreen Viewer -->
    <div id="photoViewerModal" class="hidden fixed inset-0 z-50 bg-black/90 backdrop-blur-md flex flex-col justify-between p-4">
      <div class="flex items-center justify-between text-white">
        <span class="font-mono text-xs" id="photoViewerTitle">Specimen Photo</span>
        <div class="flex items-center gap-2">
          <button type="button" onclick="rotatePhoto()" class="px-2 py-1 bg-white/20 hover:bg-white/30 rounded text-xs font-mono">↻ Rotate</button>
          <button type="button" onclick="closePhotoViewerModal()" class="px-2.5 py-1 bg-white/20 hover:bg-white/30 rounded text-xs font-bold">✕</button>
        </div>
      </div>
      <div class="flex-1 flex items-center justify-center overflow-hidden my-2">
        <img id="photoViewerImg" src="" alt="Specimen Inspection" class="max-w-full max-h-full object-contain transition-transform">
      </div>
      <div class="flex items-center justify-center gap-3 text-white text-xs font-mono">
        <button type="button" onclick="zoomPhoto(-0.3)" class="px-3 py-1.5 bg-white/20 rounded font-bold">− Zoom</button>
        <span id="zoomLevelDisplay">1.0x</span>
        <button type="button" onclick="zoomPhoto(0.3)" class="px-3 py-1.5 bg-white/20 rounded font-bold">+ Zoom</button>
        <button type="button" onclick="resetPhotoTransform()" class="px-3 py-1.5 bg-white/20 rounded">Reset</button>
      </div>
    </div>

    <!-- MODAL: Connection Telemetry Status -->
    <div id="connectionModal" class="hidden fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4">
      <div class="bg-surface border border-bordercol rounded w-full max-w-sm p-4 shadow-xl space-y-3">
        <div class="flex items-center justify-between border-b border-tonal2 pb-2">
          <h3 class="font-serif font-bold text-sm text-ink">⚡ Desktop Host Link</h3>
          <button type="button" onclick="closeModal('connectionModal')" class="text-ink-muted font-bold text-sm">✕</button>
        </div>
        <div class="space-y-1.5 text-xs font-mono">
          <div class="flex justify-between py-1 border-b border-tonal2">
            <span class="text-muted">Connection Status:</span>
            <span class="text-fern font-bold">Online (Active)</span>
          </div>
          <div class="flex justify-between py-1 border-b border-tonal2">
            <span class="text-muted">Active Database:</span>
            <span class="text-ink font-bold truncate max-w-[170px]" id="connModalDbName">---</span>
          </div>
          <div class="flex justify-between py-1 border-b border-tonal2">
            <span class="text-muted">Reviewed Total:</span>
            <span class="text-ink" id="connModalReviewed">---</span>
          </div>
          <div class="flex justify-between py-1">
            <span class="text-muted">Ping / Latency:</span>
            <span class="text-fern font-bold" id="connModalPing">42ms</span>
          </div>
        </div>
        <button type="button" onclick="closeModal('connectionModal')" class="w-full py-2 bg-fern hover:bg-fern-dark text-white rounded text-xs font-bold">Done</button>
      </div>
    </div>

    <!-- Toast Notification -->
    <div id="toast" class="hidden fixed bottom-20 left-4 right-4 max-w-sm mx-auto bg-stone-900/95 text-white text-xs py-2.5 px-4 rounded-lg shadow-xl flex items-center justify-between z-50 transition-opacity">
      <span id="toastMsg" class="font-medium truncate mr-2">Edits saved & synchronized</span>
      <button id="toastActionBtn" class="hidden shrink-0 px-2.5 py-1 rounded bg-fern hover:bg-fern-dark text-white font-mono text-[11px] font-bold uppercase tracking-wider tap-active transition-colors">Undo</button>
    </div>

  </div>

  <!-- ============================================================= -->
  <!-- CLIENT LOGIC & REACTIVE CONTROLLER SCRIPT                     -->
  <!-- ============================================================= -->
  <script>
    const _urlParams = new URLSearchParams(window.location.search);
    const TOKEN = _urlParams.get('token') || "{{ token }}";

    // Master Client State
    const state = {
      activeSchema: null,
      objectList: [],
      totalMatching: 0,
      currentOid: null,
      currentRecord: null,
      activeStatusFilter: 'all',
      noImageFilterActive: false,
      activeAdvancedFilters: { locations: {}, problems: {} },
      activeSortBy: 'id_asc',
      searchQuery: '',
      isReviewed: false,
      showFilterPills: false,
      hapticsEnabled: localStorage.getItem('arbor_haptics_enabled') !== 'false',
      hapticsIntensity: localStorage.getItem('arbor_haptics_intensity') || 'medium',
      lastSavedLocation: {
        building: '',
        floor: '',
        cabinet: '',
        shelf: '',
        storedAs: ''
      },
      batchAnchor: {
        building: '',
        floor: '',
        cabinet: '',
        shelf: '',
        storedAs: ''
      },
      batchQueue: [], // array of { oid, sciName, prevLoc }
      customPresets: ['Herbarium Sheet', 'Standard Box', 'Free Standing'],
      allStorageOptions: [
        'Herbarium Sheet', 'Standard Box', 'Free Standing', 'Petri dish', 
        'Liquid / Glass Jar', 'Capsule / Envelope', 'Microscope Slide', 'Mounted platform', 'Oversized Folder'
      ],
      storedAsChoices: [],
      isWalkModeWanted: false,
      currentHistoricalData: null,
      problemToField: {}
    };

    let searchDebounceTimer = null;
    let autoSaveTimer = null;
    let isSaving = false;
    let dirtyFields = new Set();
    let currentTabIdx = 0;
    let wakeLockSentinel = null;
    let eventSource = null;
    let toastTimer = null;
    let toastHideTimer = null;

    // Load persisted settings
    try {
      state.showFilterPills = localStorage.getItem('arbor_show_filter_pills') === 'true';
      state.isWalkModeWanted = localStorage.getItem('arbor_walk_mode') === 'true';
      const savedPresets = localStorage.getItem('arbor_storage_presets');
      if (savedPresets) state.customPresets = JSON.parse(savedPresets);
      const savedLastLoc = localStorage.getItem('arbor_last_location');
      if (savedLastLoc) state.lastSavedLocation = JSON.parse(savedLastLoc);
    } catch(e) {}

    // -------------------------------------------------------------
    // INDEXEDDB OFFLINE MUTATION QUEUE & CACHE
    // -------------------------------------------------------------
    let db;
    function initIndexedDB() {
      return new Promise((resolve) => {
        if (!window.indexedDB) return resolve();
        try {
          const req = indexedDB.open('arbor_offline_db', 3);
          req.onupgradeneeded = (e) => {
            const dbInstance = e.target.result;
            if (!dbInstance.objectStoreNames.contains('queued_mutations')) {
              dbInstance.createObjectStore('queued_mutations', { keyPath: 'timestamp' });
            }
            if (!dbInstance.objectStoreNames.contains('api_cache')) {
              dbInstance.createObjectStore('api_cache', { keyPath: 'url' });
            }
            if (!dbInstance.objectStoreNames.contains('historical_cache')) {
              dbInstance.createObjectStore('historical_cache', { keyPath: 'oid' });
            }
          };
          req.onsuccess = (e) => {
            db = e.target.result;
            updateOfflineBannerQueueCount();
            resolve();
          };
          req.onerror = () => {
            console.warn('IndexedDB unavailable');
            resolve();
          };
        } catch(e) {
          resolve();
        }
      });
    }

    function cacheApiResponse(url, data) {
      if (!db || !data) return;
      try {
        const tx = db.transaction('api_cache', 'readwrite');
        tx.objectStore('api_cache').put({ url, data });
      } catch(e) {}
    }

    function getCachedApiResponse(url) {
      return new Promise((resolve) => {
        if (!db) return resolve(null);
        try {
          const tx = db.transaction('api_cache', 'readonly');
          const req = tx.objectStore('api_cache').get(url);
          req.onsuccess = () => resolve(req.result ? req.result.data : null);
          req.onerror = () => resolve(null);
        } catch(e) {
          resolve(null);
        }
      });
    }

    function getLocalStorageQueue() {
      try {
        const q = localStorage.getItem('arbor_offline_queue');
        return q ? JSON.parse(q) : [];
      } catch (e) {
        return [];
      }
    }

    function saveLocalStorageQueue(mutations) {
      try {
        localStorage.setItem('arbor_offline_queue', JSON.stringify(mutations || []));
      } catch (e) {
        console.error('Failed to save offline queue to localStorage', e);
      }
    }

    function queueMutation(payload) {
      if (!payload) return;
      try {
        const q = getLocalStorageQueue();
        const pKey = payload.timestamp || (payload.oid ? `${payload.oid}_${Date.now()}` : String(Date.now()));
        payload.timestamp = payload.timestamp || pKey;
        const existingIdx = q.findIndex(m => String(m.timestamp) === String(payload.timestamp) || (m.oid && payload.oid && String(m.oid) === String(payload.oid) && !m.timestamp));
        if (existingIdx >= 0) {
          q[existingIdx] = payload;
        } else {
          q.push(payload);
        }
        saveLocalStorageQueue(q);
      } catch (e) {
        console.error('Failed to queue mutation in localStorage', e);
      }

      if (db) {
        try {
          const tx = db.transaction('queued_mutations', 'readwrite');
          tx.objectStore('queued_mutations').put(payload);
        } catch(e) {}
      }
      updateOfflineBannerQueueCount();
    }

    function getQueuedMutations() {
      return new Promise((resolve) => {
        const localMutations = getLocalStorageQueue();
        if (!db) return resolve(localMutations);
        try {
          const tx = db.transaction('queued_mutations', 'readonly');
          const req = tx.objectStore('queued_mutations').getAll();
          req.onsuccess = () => {
            const idbMutations = req.result || [];
            const map = new Map();
            localMutations.forEach(m => map.set(String(m.timestamp || m.oid), m));
            idbMutations.forEach(m => map.set(String(m.timestamp || m.oid), m));
            resolve(Array.from(map.values()));
          };
          req.onerror = () => resolve(localMutations);
        } catch(e) {
          resolve(localMutations);
        }
      });
    }

    function clearQueuedMutations(timestamps) {
      try {
        let q = getLocalStorageQueue();
        if (timestamps && timestamps.length > 0) {
          const tsSet = new Set(timestamps.map(String));
          q = q.filter(m => !tsSet.has(String(m.timestamp)));
        } else {
          q = [];
        }
        saveLocalStorageQueue(q);
      } catch (e) {}

      if (db) {
        try {
          const tx = db.transaction('queued_mutations', 'readwrite');
          const store = tx.objectStore('queued_mutations');
          if (timestamps && timestamps.length > 0) {
            timestamps.forEach(ts => store.delete(ts));
          } else {
            store.clear();
          }
        } catch(e) {}
      }
      updateOfflineBannerQueueCount();
    }

    function updateOfflineBannerQueueCount() {
      const localQ = getLocalStorageQueue();
      const count = localQ.length;
      const banner = document.getElementById('offlineBanner');
      const bannerText = document.getElementById('offlineBannerText');
      if (!banner) return;
      if (count > 0) {
        banner.classList.remove('hidden');
        if (bannerText) {
          bannerText.textContent = `⚠️ Offline — ${count} edit${count > 1 ? 's' : ''} queued in device storage`;
        }
      } else if (navigator.onLine && eventSource && eventSource.readyState === EventSource.OPEN) {
        banner.classList.add('hidden');
      } else {
        banner.classList.remove('hidden');
        if (bannerText) {
          bannerText.textContent = 'Workstation disconnected. Offline mode active.';
        }
      }
    }

    let isFlushingMutations = false;
    async function flushQueuedMutations() {
      if (isFlushingMutations) return;
      const mutations = await getQueuedMutations();
      if (!mutations || mutations.length === 0) {
        updateOfflineBannerQueueCount();
        return;
      }
      isFlushingMutations = true;
      mutations.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));

      const banner = document.getElementById('offlineBanner');
      const bannerText = document.getElementById('offlineBannerText');
      if (bannerText) {
        bannerText.textContent = `🔄 Connected — Syncing ${mutations.length} queued edit${mutations.length > 1 ? 's' : ''}...`;
      }
      if (banner) banner.classList.remove('hidden');

      try {
        const res = await apiFetch('/api/batch_update', {
          method: 'POST',
          body: { updates: mutations }
        });
        if (res && (res.success || res.updated_count !== undefined)) {
          clearQueuedMutations(mutations.map(m => m.timestamp));
          showToast(`✓ Synced ${mutations.length} offline edits to workstation`);
          if (banner) banner.classList.add('hidden');
          fetchObjects(false);
          if (state.currentOid) {
            fetchObjectDetail(state.currentOid, false);
          }
        }
      } catch (err) {
        console.warn('Failed to flush queued mutations:', err);
        updateOfflineBannerQueueCount();
      } finally {
        isFlushingMutations = false;
      }
    }

    // API Helper
    async function apiFetch(url, options = {}) {
      options.headers = options.headers || {};
      if (TOKEN) options.headers['X-Session-Token'] = TOKEN;
      if (options.body && typeof options.body === 'object' && !(options.body instanceof FormData)) {
        options.headers['Content-Type'] = 'application/json';
        options.body = JSON.stringify(options.body);
      }
      const isCacheable = options.method !== 'POST' && (url.startsWith('/api/schema') || url.startsWith('/api/objects') || url.startsWith('/api/object/'));
      try {
        const res = await fetch(url, options);
        if (res.status === 401) {
          window.location.href = '/login?next=' + encodeURIComponent(window.location.pathname + window.location.search);
          return null;
        }
        let data = null;
        try {
          data = await res.json();
        } catch(jsonErr) {
          data = null;
        }
        if (isCacheable && data) {
          cacheApiResponse(url, data);
        }
        return data;
      } catch(err) {
        console.warn(`Fetch error on ${url}:`, err);
        if (isCacheable) {
          const cached = await getCachedApiResponse(url);
          if (cached) return cached;
        }
        throw err;
      }
    }

    function showToast(msg, options = null) {
      const toast = document.getElementById('toast');
      const msgEl = document.getElementById('toastMsg') || toast;
      const actionBtn = document.getElementById('toastActionBtn');
      if (!toast) return;

      if (toastTimer) clearTimeout(toastTimer);
      if (toastHideTimer) clearTimeout(toastHideTimer);

      msgEl.textContent = msg;

      if (actionBtn) {
        if (options && options.actionText && typeof options.onAction === 'function') {
          actionBtn.textContent = options.actionText;
          actionBtn.onclick = (e) => {
            e.stopPropagation();
            hideToast();
            options.onAction();
          };
          actionBtn.classList.remove('hidden');
        } else {
          actionBtn.classList.add('hidden');
          actionBtn.onclick = null;
        }
      }

      toast.classList.remove('hidden');
      toast.style.opacity = '1';

      const duration = (options && options.duration) ? options.duration : (options && options.onAction ? 5000 : 2200);
      toastTimer = setTimeout(hideToast, duration);
    }

    function hideToast() {
      const toast = document.getElementById('toast');
      if (!toast) return;
      if (toastTimer) clearTimeout(toastTimer);
      toast.style.opacity = '0';
      toastHideTimer = setTimeout(() => {
        toast.classList.add('hidden');
        const actionBtn = document.getElementById('toastActionBtn');
        if (actionBtn) actionBtn.classList.add('hidden');
      }, 200);
    }

    // -------------------------------------------------------------
    // AUDIT STATION LAUNCHPAD
    // -------------------------------------------------------------
    function getSchemaBuildingChoices() {
      let bldgChoices = [];
      if (state.activeSchema && state.activeSchema.ui_sections && Array.isArray(state.activeSchema.ui_sections.location)) {
        const bldgField = state.activeSchema.ui_sections.location.find(f => f && f.name === 'Building' && Array.isArray(f.choices));
        if (bldgField) bldgChoices = bldgField.choices;
      }
      if ((!bldgChoices || bldgChoices.length === 0) && state.activeSchema && state.activeSchema.vocabulary && Array.isArray(state.activeSchema.vocabulary.Building)) {
        bldgChoices = state.activeSchema.vocabulary.Building;
      }
      if (!bldgChoices || bldgChoices.length === 0) {
        bldgChoices = ['Økern', "Lid's hus"];
      }
      return bldgChoices;
    }

    function populateLaunchBuildingOptions(selectedVal = null) {
      const bldgSelect = document.getElementById('launchBldgSelect');
      if (!bldgSelect) return;
      const prev = selectedVal || bldgSelect.value || (state.armedLocation && state.armedLocation.building) || '';
      const choices = Array.from(new Set([...getSchemaBuildingChoices(), prev])).filter(Boolean);
      bldgSelect.innerHTML = choices.map(b => `<option value="${b.replace(/"/g, '&quot;')}">${b}</option>`).join('');
      if (prev && choices.includes(prev)) {
        bldgSelect.value = prev;
      }
    }

    function initStationLaunchpad() {
      let armed = state.armedLocation;
      if (!armed) {
        try {
          const raw = localStorage.getItem('arbor_armed_location');
          if (raw) {
            armed = JSON.parse(raw);
            state.armedLocation = armed;
          }
        } catch (e) {}
      }

      const launchpad = document.getElementById('auditStationLaunchpad');
      const activePill = document.getElementById('activeStationPill');
      const pillText = document.getElementById('activeStationPillText');
      const setupCard = document.getElementById('stationSetupCard');
      const bldgSelect = document.getElementById('launchBldgSelect');
      const cabInput = document.getElementById('launchCabInput');
      const shelfInput = document.getElementById('launchShelfInput');
      const reopenBtn = document.getElementById('btnOpenStationSetup');

      if (!launchpad || !activePill || !setupCard) return;

      populateLaunchBuildingOptions(armed ? armed.building : null);

      const hasArmed = Boolean(armed && (armed.cabinet || armed.shelf));

      if (hasArmed) {
        launchpad.classList.remove('hidden');
        if (reopenBtn) reopenBtn.classList.add('hidden');
        const bldg = armed.building || (bldgSelect ? bldgSelect.value : "Lid's hus");
        const cab = armed.cabinet ? String(armed.cabinet).padStart(2, '0') : '—';
        const shelf = armed.shelf ? String(armed.shelf).padStart(2, '0') : '—';
        if (pillText) pillText.textContent = `${bldg} · Cab ${cab} · Sh ${shelf}`;
        activePill.classList.remove('hidden');
        setupCard.classList.add('hidden');

        if (bldgSelect && armed.building) bldgSelect.value = armed.building;
        if (cabInput && armed.cabinet) cabInput.value = armed.cabinet;
        if (shelfInput && armed.shelf) shelfInput.value = armed.shelf;
      } else {
        launchpad.classList.remove('hidden');
        if (reopenBtn) reopenBtn.classList.add('hidden');
        activePill.classList.add('hidden');
        setupCard.classList.remove('hidden');
      }
    }

    function openStationSetup() {
      const launchpad = document.getElementById('auditStationLaunchpad');
      const activePill = document.getElementById('activeStationPill');
      const setupCard = document.getElementById('stationSetupCard');
      const cabInput = document.getElementById('launchCabInput');
      const reopenBtn = document.getElementById('btnOpenStationSetup');
      if (launchpad) launchpad.classList.remove('hidden');
      if (reopenBtn) reopenBtn.classList.add('hidden');
      if (activePill) activePill.classList.add('hidden');
      if (setupCard) setupCard.classList.remove('hidden');
      if (cabInput) {
        cabInput.focus();
        cabInput.select();
      }
    }

    function dismissStationSetup() {
      const launchpad = document.getElementById('auditStationLaunchpad');
      const setupCard = document.getElementById('stationSetupCard');
      const activePill = document.getElementById('activeStationPill');
      const reopenBtn = document.getElementById('btnOpenStationSetup');
      const armed = state.armedLocation;
      const hasArmed = Boolean(armed && (armed.cabinet || armed.shelf));

      if (hasArmed) {
        if (setupCard) setupCard.classList.add('hidden');
        if (activePill) activePill.classList.remove('hidden');
      } else {
        if (setupCard) setupCard.classList.add('hidden');
        if (launchpad) launchpad.classList.add('hidden');
        if (reopenBtn) reopenBtn.classList.remove('hidden');
      }
    }

    function applyStationSetup() {
      const bldgSelect = document.getElementById('launchBldgSelect');
      const cabInput = document.getElementById('launchCabInput');
      const shelfInput = document.getElementById('launchShelfInput');

      const bldg = bldgSelect ? bldgSelect.value : "Lid's hus";
      let cab = cabInput ? cabInput.value.trim() : '';
      let shelf = shelfInput ? shelfInput.value.trim() : '';

      if (!cab && !shelf) {
        showToast('Please enter at least a Cabinet or Shelf number');
        return;
      }

      if (cab && /^[0-9]+$/.test(cab)) cab = cab.padStart(2, '0');
      if (shelf && /^[0-9]+$/.test(shelf)) shelf = shelf.padStart(2, '0');

      state.armedLocation = {
        building: bldg,
        floor: '1',
        cabinet: cab,
        shelf: shelf,
        storedAs: ''
      };
      state.lastSavedLocation = { ...state.armedLocation };

      try {
        localStorage.setItem('arbor_armed_location', JSON.stringify(state.armedLocation));
        localStorage.setItem('arbor_last_location', JSON.stringify(state.lastSavedLocation));
      } catch (e) {}

      initStationLaunchpad();
      triggerHaptic('stepper');
      showToast(`🎯 Station armed: Cab ${cab || '—'} · Sh ${shelf || '—'}`);
    }

    // -------------------------------------------------------------
    // INITIALIZATION & SSE CONNECTION
    // -------------------------------------------------------------
    async function init() {
      await initIndexedDB();
      applyFilterPillVisibility();
      initStationLaunchpad();
      await fetchSchema();
      await fetchObjects();
      setupEventSource();
      flushQueuedMutations();
      window.addEventListener('online', () => {
        setupEventSource();
        flushQueuedMutations();
      });
      window.addEventListener('offline', () => {
        updateOfflineBannerQueueCount();
      });
      if (state.isWalkModeWanted) {
        acquireWakeLock(true);
      } else {
        updateWakeLockUI(false);
      }
      document.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'visible') {
          setupEventSource();
          if (state.isWalkModeWanted && !wakeLockSentinel) {
            acquireWakeLock(true);
          }
        }
      });
      if (typeof renderDetailStoredAsPills === 'function') {
        renderDetailStoredAsPills();
      }
    }

    let _v2ReconnectTimer = null;
    let _v2ReconnectDelay = 2000;

    function scheduleV2Reconnect() {
      if (_v2ReconnectTimer) return;
      _v2ReconnectTimer = setTimeout(() => {
        _v2ReconnectTimer = null;
        setupEventSource();
      }, _v2ReconnectDelay);
      _v2ReconnectDelay = Math.min(_v2ReconnectDelay * 1.5, 30000);
    }

    function setupEventSource() {
      if (_v2ReconnectTimer) {
        clearTimeout(_v2ReconnectTimer);
        _v2ReconnectTimer = null;
      }
      if (eventSource) {
        try { eventSource.close(); } catch(e) {}
        eventSource = null;
      }
      const sseUrl = '/api/events' + (TOKEN ? '?token=' + encodeURIComponent(TOKEN) : '');
      eventSource = new EventSource(sseUrl);
      eventSource.onopen = () => {
        _v2ReconnectDelay = 2000;
        flushQueuedMutations();
      };
      eventSource.onerror = () => {
        updateOfflineBannerQueueCount();
        if (eventSource) {
          try { eventSource.close(); } catch(e) {}
          eventSource = null;
        }
        scheduleV2Reconnect();
      };
      eventSource.onmessage = (e) => {
        try {
          const msg = JSON.parse(e.data);
          const events = msg.type === 'batch' && Array.isArray(msg.events) ? msg.events : [msg];
          let shouldRefreshList = false;
          for (const evt of events) {
            if (!evt || !evt.type) continue;
            if (evt.type === 'record_updated' || evt.type === 'object_updated') {
              const updatedId = String((evt.data && (evt.data.id || evt.data.oid)) || evt.id || '');
              if (state.currentOid && updatedId && updatedId === String(state.currentOid)) {
                fetchObjectDetail(state.currentOid, false);
              }
              shouldRefreshList = true;
            } else if (evt.type === 'push_navigation') {
              const targetId = String((evt.data && (evt.data.id || evt.data.oid)) || evt.id || '');
              if (targetId && typeof openDetailView === 'function') {
                openDetailView(targetId);
                if (typeof showToast === 'function') showToast(`Opened #${targetId} from desktop`, 'info');
              }
            } else if (evt.type === 'session_ended') {
              if (typeof showToast === 'function') {
                showToast('Desktop mobile session ended — reconnect to continue syncing', 'warning');
              }
            }
          }
          if (shouldRefreshList) {
            fetchObjects(false);
          }
        } catch(err) {}
      };
    }

    async function fetchSchema() {
      try {
        const data = await apiFetch('/api/schema');
        if (data) {
          state.activeSchema = data;
          state.problemToField = data.problem_to_field || {};
          state.icedigCodes = data.icedig_code_labels || {};
          document.getElementById('headerDbName').textContent = data.database_name || 'Active Database';
          document.getElementById('connModalDbName').textContent = data.database_name || 'Active Database';
          if (data.stored_as_choices && Array.isArray(data.stored_as_choices)) {
            const choices = [...data.stored_as_choices];
            ['Other', 'Custom'].forEach(opt => {
              if (!choices.includes(opt)) choices.push(opt);
            });
            state.storedAsChoices = choices;
            if (typeof renderBatchStoredAsPills === 'function') {
                renderBatchStoredAsPills();
            }
            if (typeof renderDetailStoredAsPills === 'function') {
                renderDetailStoredAsPills();
            }
          }
          if (typeof populateBatchBuildingOptions === 'function') {
            populateBatchBuildingOptions();
          }
          if (typeof populateDetailBuildingOptions === 'function') {
            populateDetailBuildingOptions();
          }
          if (typeof populateLaunchBuildingOptions === 'function') {
            populateLaunchBuildingOptions();
          }
        }
      } catch(err) {
        console.error('Failed to fetch schema:', err);
      }
    }

    // -------------------------------------------------------------
    // SCREEN 1: VAULT LIST VIEW LOGIC
    // -------------------------------------------------------------
    async function fetchObjects(showLoading = true) {
      const container = document.getElementById('specimenListContainer');
      if (showLoading && container) {
        container.innerHTML = `
          <div class="p-8 text-center text-ink-muted font-mono text-xs animate-pulse">
            Loading specimens from database...
          </div>
        `;
      }

      const params = new URLSearchParams();
      if (state.searchQuery) params.set('q', state.searchQuery);
      if (state.activeStatusFilter) params.set('status', state.activeStatusFilter);
      if (state.selectedCabinet) params.set('cabinet', state.selectedCabinet);
      if (state.selectedShelf) params.set('shelf', state.selectedShelf);
      if (state.activeSortBy) {
        if (state.activeSortBy === 'location') params.set('sort_by', 'cabinet');
        else if (state.activeSortBy === 'name_asc') { params.set('sort_by', 'genus'); params.set('sort_dir', 'asc'); }
        else if (state.activeSortBy === 'name_desc') { params.set('sort_by', 'genus'); params.set('sort_dir', 'desc'); }
        else if (state.activeSortBy === 'id_asc') { params.set('sort_by', 'id'); params.set('sort_dir', 'asc'); }
        else if (state.activeSortBy === 'flagged_first') { params.set('has_problems', 'true'); }
      }
      params.set('limit', '200');

      try {
        const res = await apiFetch('/api/objects?' + params.toString());
        if (res) {
          state.objectList = res.objects || [];
          state.totalMatching = res.total_matching || 0;
          renderObjectList();
          updateListMetrics(res.facets);
          // Populate Vault Location dropdowns
          const cabSel = document.getElementById('quickFilterCabinet');
          const shelfSel = document.getElementById('quickFilterShelf');
          if (cabSel && res.facets && res.facets.cabinets && cabSel.options.length <= 1) {
            res.facets.cabinets.forEach(c => {
              const opt = document.createElement('option');
              opt.value = c;
              opt.textContent = `Cab ${c}`;
              if (state.selectedCabinet === c) opt.selected = true;
              cabSel.appendChild(opt);
            });
          }
          if (shelfSel && res.facets && res.facets.shelves && shelfSel.options.length <= 1) {
            res.facets.shelves.forEach(s => {
              const opt = document.createElement('option');
              opt.value = s;
              opt.textContent = `Shelf ${s}`;
              if (state.selectedShelf === s) opt.selected = true;
              shelfSel.appendChild(opt);
            });
          }
        }
      } catch(err) {
        if (container) {
          container.innerHTML = `<div class="p-8 text-center text-brick font-mono text-xs">Failed to load objects.</div>`;
        }
      }
    }

    function renderObjectList() {
      const container = document.getElementById('specimenListContainer');
      if (!container) return;

      if (state.objectList.length === 0) {
        container.innerHTML = `
          <div class="p-12 text-center text-ink-muted flex flex-col items-center justify-center">
            <span class="text-3xl mb-2">🔍</span>
            <p class="font-sans font-semibold text-sm text-ink">No specimens found</p>
            <p class="text-xs text-muted mt-1 max-w-[240px]">Try adjusting your search query or filter criteria.</p>
            <button onclick="clearSearch()" class="mt-4 px-3 py-1.5 bg-white border border-bordercol rounded text-xs font-mono font-medium shadow-2xs tap-active">
              [ Clear Filter & Show All ]
            </button>
          </div>
        `;
        return;
      }

      container.innerHTML = state.objectList.map((obj, idx) => {
        const isRev = obj.review_status === 'reviewed';
        const hasFlags = obj.has_flags;
        const loc = obj.location || {};
        
        let locBreadcrumb = [];
        if (loc.building) locBreadcrumb.push(loc.building);
        if (loc.floor !== undefined && loc.floor !== null && String(loc.floor).trim() !== '') locBreadcrumb.push(`Fl ${loc.floor}`);
        if (loc.cabinet) locBreadcrumb.push(`Cab ${loc.cabinet}`);
        if (loc.shelf) locBreadcrumb.push(`Sh ${loc.shelf}`);
        const locStr = locBreadcrumb.length > 0 ? locBreadcrumb.join(' › ') : 'Unrecorded location';

        return `
          <article onclick="openDetailView('${obj.id}')" class="bg-surface border border-bordercol rounded p-3 shadow-2xs hover:border-fern/50 active:bg-stone-50 transition-all cursor-pointer flex flex-col gap-1.5 relative tap-active">
            <div class="flex items-start justify-between">
              <div class="flex items-center gap-2 min-w-0">
                <span class="font-mono text-[11px] font-bold text-ink px-1.5 py-0.5 bg-stone-100 border border-bordercol/80 rounded">
                  #${obj.accession_number || obj.id}
                </span>
                <span class="text-[10px] font-mono text-muted uppercase truncate">${obj.family || 'Taxon'}</span>
              </div>
              
              <div class="flex items-center gap-1.5 shrink-0">
                ${hasFlags ? '<span class="px-1.5 py-0.5 rounded text-[10px] font-bold bg-amber-50 text-amber-800 border border-amber-300">Taxon Issue ⚠</span>' : ''}
                ${isRev ? 
                  '<span class="px-1.5 py-0.5 rounded text-[10px] font-bold bg-emerald-50 text-fern-dark border border-fern/30">Reviewed ✓</span>' : 
                  '<span class="px-1.5 py-0.5 rounded text-[10px] font-bold bg-stone-100 text-stone-600 border border-stone-300">Pending</span>'
                }
              </div>
            </div>

            <div class="font-serif font-semibold italic text-[15px] text-ink leading-tight truncate">
              ${obj.scientific_name || 'Unidentified Specimen'}
            </div>

            <div class="flex items-center justify-between text-[11px] font-mono pt-1 border-t border-stone-100 text-muted">
              <span class="truncate text-ink-muted">${locStr}</span>
              ${loc.stored_as ? `<span class="text-[10px] px-1.5 py-0.2 bg-stone-100 rounded border border-bordercol/60 shrink-0">${loc.stored_as}</span>` : ''}
            </div>
          </article>
        `;
      }).join('');
    }

    function updateListMetrics(facets = {}) {
      document.getElementById('matchingCount').textContent = state.totalMatching;
      
      const rev = facets.reviewed_count || 0;
      const total = state.totalMatching || 1;
      const pct = Math.round((rev / total) * 100) || 0;

      document.getElementById('listProgressText').textContent = `${rev} / ${total} Reviewed`;
      document.getElementById('listProgressPct').textContent = `(${pct}%)`;
      document.getElementById('listProgressBar').style.width = `${pct}%`;

      document.getElementById('pillCountAll').textContent = `(${total})`;
      document.getElementById('pillCountPending').textContent = `(${facets.pending_count || 0})`;
      document.getElementById('pillCountFlagged').textContent = `(${facets.flagged_count || 0})`;
      document.getElementById('pillCountReviewed').textContent = `(${rev})`;
      document.getElementById('pillCountConflict').textContent = `(${facets.history_count || 0})`;
      document.getElementById('pillCountUnknown').textContent = `(${facets.unknown_count || 0})`;
    }

    function handleSearchInput() {
      const searchBox = document.getElementById('searchBox');
      const val = searchBox ? searchBox.value.trim() : '';
      const clearBtn = document.getElementById('searchClearBtn');
      if (val) clearBtn?.classList.remove('hidden');
      else clearBtn?.classList.add('hidden');
      debounceSearch();
    }

    function debounceSearch() {
      clearTimeout(searchDebounceTimer);
      searchDebounceTimer = setTimeout(() => {
        state.searchQuery = document.getElementById('searchBox')?.value.trim() || '';
        const clearBtn = document.getElementById('searchClearBtn');
        if (state.searchQuery) clearBtn?.classList.remove('hidden');
        else clearBtn?.classList.add('hidden');
        fetchObjects();
      }, 300);
    }

    function toggleSearchInputMode() {
      const searchBox = document.getElementById('searchBox');
      const btn = document.getElementById('btnInputModeToggle');
      if (!searchBox) return;
      const currentMode = searchBox.getAttribute('inputmode') || 'numeric';
      if (currentMode === 'numeric') {
        searchBox.setAttribute('inputmode', 'text');
        if (btn) btn.textContent = 'Aa';
        showToast('Keyboard: Text mode (Aa)');
      } else {
        searchBox.setAttribute('inputmode', 'numeric');
        if (btn) btn.textContent = '123';
        showToast('Keyboard: Numeric mode (123)');
      }
      searchBox.focus();
    }

    function clearSearch() {
      if (searchDebounceTimer) clearTimeout(searchDebounceTimer);
      const searchBox = document.getElementById('searchBox');
      if (searchBox) {
        searchBox.value = '';
        searchBox.focus();
      }
      state.searchQuery = '';
      document.getElementById('searchClearBtn')?.classList.add('hidden');
      fetchObjects();
    }

    function setStatusFilter(status) {
      state.activeStatusFilter = status;
      document.querySelectorAll('.filter-pill').forEach(el => {
        el.className = 'filter-pill whitespace-nowrap px-2.5 py-1 rounded-full text-[11px] font-medium font-sans bg-stone-200/80 text-ink-muted hover:bg-stone-300 tap-active transition-all';
      });
      const activeEl = document.getElementById('pill-' + status);
      if (activeEl) {
        activeEl.className = 'filter-pill whitespace-nowrap px-2.5 py-1 rounded-full text-[11px] font-medium font-sans bg-ink text-white shadow-sm tap-active transition-all';
      }
      fetchObjects();
    }

    function toggleNoImageFilter() {
      state.noImageFilterActive = !state.noImageFilterActive;
      const pill = document.getElementById('pill-no-image');
      if (state.noImageFilterActive) {
        pill.className = 'filter-pill whitespace-nowrap px-2.5 py-1 rounded-full text-[11px] font-medium font-sans bg-amber-50 text-amber-900 border border-amber-300 tap-active transition-all';
      } else {
        pill.className = 'filter-pill whitespace-nowrap px-2.5 py-1 rounded-full text-[11px] font-medium font-sans bg-stone-100 text-stone-600 border border-stone-200 hover:bg-stone-200 tap-active transition-all';
      }
      fetchObjects();
    }

    function handleSortChange() {
      state.activeSortBy = document.getElementById('sortBySelect').value;
      fetchObjects();
    }

    function toggleFilterPillsSetting(enabled) {
      state.showFilterPills = enabled;
      try { localStorage.setItem('arbor_show_filter_pills', enabled ? 'true' : 'false'); } catch(e) {}
      applyFilterPillVisibility();
    }

    function applyFilterPillVisibility() {
      const container = document.getElementById('filterPillsContainer');
      const settingInput = document.getElementById('settingShowFilterPills');
      if (settingInput) settingInput.checked = state.showFilterPills;
      if (container) {
        if (state.showFilterPills) container.classList.remove('hidden');
        else container.classList.add('hidden');
      }
    }

    // -------------------------------------------------------------
    // SCREEN 2: SPECIMEN DETAIL VIEW LOGIC
    // -------------------------------------------------------------
    async function openDetailView(oid) {
      forceSaveImmediate();
      state.currentOid = String(oid);
      showDetailView();
      await fetchObjectDetail(oid);
    }

    function showListView() {
      forceSaveImmediate();
      document.getElementById('listView').classList.remove('hidden');
      document.getElementById('detailView').classList.add('hidden');
      document.getElementById('batchLocationView').classList.add('hidden');
      initStationLaunchpad();
      const searchBox = document.getElementById('searchBox');
      if (searchBox) {
        searchBox.value = '';
        state.searchQuery = '';
        document.getElementById('searchClearBtn')?.classList.add('hidden');
        setTimeout(() => searchBox.focus(), 50);
      }
      fetchObjects();
    }

    function showDetailView() {
      document.getElementById('listView').classList.add('hidden');
      document.getElementById('detailView').classList.remove('hidden');
      document.getElementById('batchLocationView').classList.add('hidden');
    }

    function showBatchLocationView() {
      document.getElementById('listView').classList.add('hidden');
      document.getElementById('detailView').classList.add('hidden');
      document.getElementById('batchLocationView').classList.remove('hidden');
      if (typeof populateBatchBuildingOptions === 'function') {
        populateBatchBuildingOptions();
      }
      if (typeof loadBatchQueueFromStorage === 'function') {
        loadBatchQueueFromStorage();
      }
      updateBatchAnchorUI();
      if (typeof updateBatchArmedButton === 'function') {
        updateBatchArmedButton();
      }
      document.getElementById('batchIdInput')?.focus();
    }

    function updateBatchArmedButton() {
      const btn = document.getElementById('btnBatchCopyArmed');
      if (!btn) return;
      const armed = state.armedLocation || state.lastSavedLocation;
      const hasArmed = Boolean(armed && (armed.cabinet || armed.shelf));
      if (hasArmed) {
        const cab = String(armed.cabinet || '—').padStart(2, '0');
        const sh = String(armed.shelf || '—').padStart(2, '0');
        btn.textContent = `⚡ Use Cab ${cab} · Sh ${sh}`;
        btn.classList.remove('hidden');
      } else {
        btn.classList.add('hidden');
      }
    }

    function copyArmedShelfToBatch() {
      const armed = state.armedLocation || state.lastSavedLocation;
      if (!armed || (!armed.cabinet && !armed.shelf)) {
        showToast('No target shelf armed yet');
        return;
      }
      state.batchAnchor = state.batchAnchor || {};
      if (armed.building) state.batchAnchor.building = armed.building;
      if (armed.floor !== undefined && armed.floor !== null && String(armed.floor).trim() !== '') {
        state.batchAnchor.floor = String(armed.floor).trim();
      }
      if (armed.cabinet) state.batchAnchor.cabinet = String(armed.cabinet).trim();
      if (armed.shelf) state.batchAnchor.shelf = String(armed.shelf).trim();
      if (typeof populateBatchBuildingOptions === 'function') populateBatchBuildingOptions();
      updateBatchAnchorUI();
      if (typeof saveBatchQueueToStorage === 'function') saveBatchQueueToStorage();
      showToast('⚡ Copied armed target shelf to batch anchor');
    }

    function toggleBatchInputMode() {
      const input = document.getElementById('batchIdInput');
      const btn = document.getElementById('btnBatchKeyboardMode');
      if (!input || !btn) return;
      const isNumeric = (input.getAttribute('inputmode') || 'numeric') === 'numeric';
      if (isNumeric) {
        input.setAttribute('inputmode', 'text');
        btn.textContent = 'ABC';
      } else {
        input.setAttribute('inputmode', 'numeric');
        btn.textContent = '123';
      }
      input.focus();
    }

    async function fetchObjectDetail(oid, renderFull = true) {
      try {
        const [data, hist] = await Promise.all([
          apiFetch('/api/object/' + encodeURIComponent(oid)),
          apiFetch('/api/object/' + encodeURIComponent(oid) + '/history').catch(() => null)
        ]);
        if (data) {
          state.currentRecord = data;
          state.isReviewed = data.review_status === 'reviewed';
          state.currentHistoricalData = (hist && hist.historical_data) ? hist.historical_data : null;
          renderDetailView(renderFull);
        }
      } catch(err) {
        console.error('Failed to load specimen detail:', err);
      }
    }

    function renderDetailView(renderFull = true) {
      if (!state.currentRecord) return;
      const rec = state.currentRecord;
      const reg = rec.registration || {};
      const obs = rec.observation || {};

      // Accession Header
      document.getElementById('detailAccession').textContent = '#' + (rec.accession_number || rec.id);
      document.getElementById('detailScientificName').textContent = rec.scientific_name || 'Unidentified Specimen';
      document.getElementById('detailFamily').textContent = reg.Family || '—';

      // Tri-State Status Pill & Micro-Copy Reassurance
      const statusBtn = document.getElementById('badgeStatus');
      const statusText = document.getElementById('badgeStatusText');
      const statusDot = document.getElementById('badgeStatusDot');
      const detailRevBtn = document.getElementById('btnDetailMarkReviewed');
      const detailRevLabel = document.getElementById('btnDetailReviewedLabel');
      const detailRevIcon = document.getElementById('btnDetailReviewedIcon');
      
      const activeProblemsCount = countActiveProblemsOnRecord(rec);
      const hasFlags = (activeProblemsCount > 0) || Boolean(rec.has_flags);

      if (state.isReviewed) {
        if (hasFlags) {
          // Tri-State: REVIEWED WITH ISSUES (Amber #F57C00 / bg-amber-50)
          statusBtn.className = 'flex items-center gap-1.5 text-[11px] font-mono font-semibold px-2 py-0.5 rounded border transition-colors tap-highlight-transparent bg-amber-50 text-amber-900 border-amber-300';
          statusText.textContent = `REV + ${activeProblemsCount || 1} ISSUE${activeProblemsCount === 1 ? '' : 'S'}`;
          statusDot.className = 'w-1.5 h-1.5 rounded-full bg-amber-500';
          if (detailRevBtn) {
            detailRevBtn.className = 'flex-1 py-2.5 px-4 rounded font-sans font-bold text-xs flex items-center justify-center gap-2 border transition-all tap-active bg-amber-600 text-white border-amber-700 shadow-sm';
            if (detailRevLabel) detailRevLabel.textContent = `Reviewed (${activeProblemsCount || 1} Issues Queued)`;
            if (detailRevIcon) detailRevIcon.textContent = '⚠';
          }
        } else {
          // Tri-State: REVIEWED CLEAN (Emerald)
          statusBtn.className = 'flex items-center gap-1.5 text-[11px] font-mono font-semibold px-2 py-0.5 rounded border transition-colors tap-highlight-transparent bg-emerald-50 text-fern-dark border-fern/30';
          statusText.textContent = 'REVIEWED';
          statusDot.className = 'w-1.5 h-1.5 rounded-full bg-fern';
          if (detailRevBtn) {
            detailRevBtn.className = 'flex-1 py-2.5 px-4 rounded font-sans font-bold text-xs flex items-center justify-center gap-2 border transition-all tap-active bg-emerald-600 text-white border-emerald-700 shadow-sm';
            if (detailRevLabel) detailRevLabel.textContent = 'Reviewed (Tap to Unmark)';
            if (detailRevIcon) detailRevIcon.textContent = '✓';
          }
        }
      } else {
        // Tri-State: UNREVIEWED (Stone / Amber pulse)
        statusBtn.className = 'flex items-center gap-1.5 text-[11px] font-mono font-semibold px-2 py-0.5 rounded border transition-colors tap-highlight-transparent bg-stone-100 text-stone-700 border-stone-300';
        statusText.textContent = 'UNREVIEWED';
        statusDot.className = 'w-1.5 h-1.5 rounded-full bg-amber-500 animate-pulse';
        if (detailRevBtn) {
          detailRevBtn.className = 'flex-1 py-2.5 px-4 rounded font-sans font-bold text-xs flex items-center justify-center gap-2 border transition-all tap-active bg-emerald-50 text-fern-dark border-fern hover:bg-emerald-100 shadow-2xs';
          if (detailRevLabel) detailRevLabel.textContent = 'Mark Reviewed';
          if (detailRevIcon) detailRevIcon.textContent = '✓';
        }
      }

      // Reassurance micro-copy
      const helperEl = document.getElementById('reviewHelperText');
      if (helperEl) {
        if (state.isReviewed) {
          if (hasFlags) {
            helperEl.textContent = '✓ Location recorded. Issues flagged for desktop curation.';
          } else {
            helperEl.textContent = '✓ Location recorded & verified. Specimen clean.';
          }
        } else {
          if (hasFlags) {
            helperEl.textContent = 'Physical check needed. Unresolved issues will be preserved on review.';
          } else {
            helperEl.textContent = 'Verify physical label & location, then mark reviewed.';
          }
        }
      }

      // Specimen index in list
      const curIdx = state.objectList.findIndex(o => String(o.id) === String(rec.id));
      document.getElementById('detailCurrentIdx').textContent = curIdx >= 0 ? curIdx + 1 : 1;
      document.getElementById('detailTotalCount').textContent = state.objectList.length || state.totalMatching || 1;

      // Update Armed Target Shelf action banner
      updateArmedShelfBannerUI(obs);

      // Coordinate Steppers
      renderCoordinateSteppers(obs);

      // Building Dropdown Options (Blank by default if unrecorded)
      populateDetailBuildingOptions(obs.Building || '');

      // Stored As Selection
      renderDetailStoredAsPills(obs['Stored as'] || obs.Stored_As || '');

      // Loan Status
      renderLoanStatus(obs['Loaned out']);

      // Dynamic Form Fields in Details Tab
      renderDynamicForm(state.activeSchema, rec);

      // Photos in Details Tab
      renderPhotos(rec.images);

      // Problems & Discrepancies in Problems Tab
      renderProblemsAndDiscrepancies(rec);

      // Breadcrumb
      updateDetailLocBreadcrumbs(obs);
    }

    function escapeHtml(str) {
      if (str === null || str === undefined) return '';
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
    }

    function renderCoordinateSteppers(obs = {}) {
      // Floor (supports continuous signed numbers, em-dash if unset)
      const hasFloor = (obs.Floor !== undefined && obs.Floor !== null && String(obs.Floor).trim() !== '' && String(obs.Floor).trim() !== '—');
      const fl = hasFloor ? String(obs.Floor).trim() : '—';
      const flEl = document.getElementById('detailFloorVal');
      if (flEl) flEl.textContent = fl;

      // Cabinet (2-digit zero-padded, empty placeholder if unset)
      const hasCab = (obs.Cabinet !== undefined && obs.Cabinet !== null && String(obs.Cabinet).trim() !== '' && String(obs.Cabinet).trim() !== '—');
      const cab = hasCab ? String(obs.Cabinet).trim().padStart(2, '0') : '';
      const cabEl = document.getElementById('detailCabVal');
      if (cabEl) {
        if ('value' in cabEl) cabEl.value = cab;
        else cabEl.textContent = cab || '—';
      }

      // Shelf (2-digit zero-padded, empty placeholder if unset)
      const hasShelf = (obs.Shelf !== undefined && obs.Shelf !== null && String(obs.Shelf).trim() !== '' && String(obs.Shelf).trim() !== '—');
      const sh = hasShelf ? String(obs.Shelf).trim().padStart(2, '0') : '';
      const shEl = document.getElementById('detailShelfVal');
      if (shEl) {
        if ('value' in shEl) shEl.value = sh;
        else shEl.textContent = sh || '—';
      }
    }

    function handleDirectCoordinateInput(coord, val) {
      if (!state.currentRecord) return;
      state.currentRecord.observation = state.currentRecord.observation || {};
      const obs = state.currentRecord.observation;
      const cleanDigits = String(val || '').replace(/[^0-9]/g, '');

      if (coord === 'cab') {
        if (!cleanDigits) {
          obs.Cabinet = '';
        } else {
          const num = Math.max(1, parseInt(cleanDigits, 10));
          obs.Cabinet = String(num).padStart(2, '0');
        }
        markDirty('Cabinet');
      } else if (coord === 'shelf') {
        if (!cleanDigits) {
          obs.Shelf = '';
        } else {
          const num = Math.max(1, parseInt(cleanDigits, 10));
          obs.Shelf = String(num).padStart(2, '0');
        }
        markDirty('Shelf');
      }

      renderCoordinateSteppers(obs);
      updateDetailLocBreadcrumbs(obs);
      armActiveTargetLocation(obs);
      triggerAutoSave();
      triggerHaptic('stepper');
    }

    function handleDirectCoordinateBlur(coord, input) {
      if (!input) return;
      handleDirectCoordinateInput(coord, input.value);
    }

    function adjustCoordinate(coord, delta) {
      if (!state.currentRecord) return;
      state.currentRecord.observation = state.currentRecord.observation || {};
      const obs = state.currentRecord.observation;

      if (coord === 'floor') {
        const isUnset = (obs.Floor === undefined || obs.Floor === null || String(obs.Floor).trim() === '' || String(obs.Floor).trim() === '—');
        let next;
        if (isUnset) {
          next = delta > 0 ? 1 : -1;
        } else {
          const current = parseInt(obs.Floor, 10);
          next = isNaN(current) ? (delta > 0 ? 1 : -1) : current + delta;
        }
        obs.Floor = String(next);
        markDirty('Floor');
      } else if (coord === 'cab') {
        const isUnset = (obs.Cabinet === undefined || obs.Cabinet === null || String(obs.Cabinet).trim() === '' || String(obs.Cabinet).trim() === '—');
        let next;
        if (isUnset) {
          next = 1;
        } else {
          const current = parseInt(obs.Cabinet, 10);
          next = Math.max(1, (isNaN(current) ? 1 : current) + delta);
        }
        obs.Cabinet = String(next);
        markDirty('Cabinet');
      } else if (coord === 'shelf') {
        const isUnset = (obs.Shelf === undefined || obs.Shelf === null || String(obs.Shelf).trim() === '' || String(obs.Shelf).trim() === '—');
        let next;
        if (isUnset) {
          next = 1;
        } else {
          const current = parseInt(obs.Shelf, 10);
          next = Math.max(1, (isNaN(current) ? 1 : current) + delta);
        }
        obs.Shelf = String(next);
        markDirty('Shelf');
      }

      renderCoordinateSteppers(obs);
      updateDetailLocBreadcrumbs(obs);
      armActiveTargetLocation(obs);
      triggerAutoSave();
      triggerHaptic('stepper');
    }

    function populateDetailBuildingOptions(currentBldg) {
      const select = document.getElementById('detailBuildingSelect');
      if (!select) return;

      const bldgChoices = getSchemaBuildingChoices();

      const activeVal = (currentBldg !== undefined && currentBldg !== null)
        ? String(currentBldg).trim()
        : ((state.currentRecord && state.currentRecord.observation && state.currentRecord.observation.Building !== undefined)
            ? String(state.currentRecord.observation.Building).trim()
            : '');

      const allChoices = Array.from(new Set([...bldgChoices, activeVal])).filter(Boolean);

      let optionsHtml = '<option value="">--</option>';
      optionsHtml += allChoices.map(b => `<option value="${b.replace(/"/g, '&quot;')}">${b}</option>`).join('');

      select.innerHTML = optionsHtml;
      select.value = activeVal;
    }

    function handleDetailBuildingChange(val) {
      if (!state.currentRecord) return;
      state.currentRecord.observation = state.currentRecord.observation || {};
      state.currentRecord.observation.Building = val;
      markDirty('Building');
      updateDetailLocBreadcrumbs(state.currentRecord.observation);
      armActiveTargetLocation(state.currentRecord.observation);
      triggerAutoSave();
    }

    function renderDetailStoredAsPills(currentStored) {
      const container = document.getElementById('detailStoredAsPills');
      if (!container) return;
      const storedVal = currentStored !== undefined ? currentStored : (state.currentRecord?.observation?.['Stored as'] || '');
      let choices = state.storedAsChoices && state.storedAsChoices.length > 0
                      ? [...state.storedAsChoices]
                      : ['Herbarium Sheet', 'Box', 'Envelope', 'Jar', 'Packet', 'Other', 'Custom'];
      ['Other', 'Custom'].forEach(opt => {
        if (!choices.includes(opt)) choices.push(opt);
      });

      const isCustomVal = storedVal && !choices.includes(storedVal) && storedVal !== 'Custom' && storedVal !== 'Other';

      container.innerHTML = choices.map(opt => {
        const isSel = (opt === storedVal) || (opt === 'Custom' && isCustomVal);
        const className = isSel
          ? 'detail-storage-pill px-2.5 py-1 rounded-full text-[11px] font-mono border-2 border-fern bg-emerald-50 text-fern-dark font-semibold'
          : 'detail-storage-pill px-2.5 py-1 rounded-full text-[11px] font-mono border border-bordercol bg-white text-muted';
        const escapedOpt = opt.replace(/'/g, "\\'");
        return `
          <button type="button" onclick="selectDetailStoragePill('${escapedOpt}')" class="${className}">
            ${opt}
          </button>
        `;
      }).join('');

      const labelEl = document.getElementById('detailStoredAsLabel');
      if (labelEl) labelEl.textContent = storedVal || 'Not Selected';

      const customContainer = document.getElementById('detailStoredAsCustomContainer');
      const customInput = document.getElementById('detailStoredAsCustomInput');
      if (customContainer) {
        if (storedVal === 'Custom' || isCustomVal) {
          customContainer.classList.remove('hidden');
          if (customInput) {
            customInput.value = isCustomVal ? storedVal : (storedVal === 'Custom' ? '' : storedVal);
          }
        } else {
          customContainer.classList.add('hidden');
        }
      }
    }

    function selectDetailStoragePill(opt) {
      if (!state.currentRecord) return;
      state.currentRecord.observation = state.currentRecord.observation || {};
      const current = state.currentRecord.observation['Stored as'] || '';

      if (current === opt) {
        state.currentRecord.observation['Stored as'] = '';
      } else {
        state.currentRecord.observation['Stored as'] = opt;
      }
      markDirty('Stored as');
      renderDetailStoredAsPills(state.currentRecord.observation['Stored as']);
      updateDetailLocBreadcrumbs(state.currentRecord.observation);
      armActiveTargetLocation(state.currentRecord.observation);
      triggerAutoSave();
    }

    function onDetailCustomStorageInput(val) {
      if (!state.currentRecord) return;
      state.currentRecord.observation = state.currentRecord.observation || {};
      state.currentRecord.observation['Stored as'] = val;
      markDirty('Stored as');
      const labelEl = document.getElementById('detailStoredAsLabel');
      if (labelEl) labelEl.textContent = val || 'Custom';
      updateDetailLocBreadcrumbs(state.currentRecord.observation);
      triggerAutoSave();
    }

    // Availability / Loan Status
    function setLoanStatus(isLoaned) {
      if (!state.currentRecord) return;
      state.currentRecord.observation = state.currentRecord.observation || {};
      state.currentRecord.observation['Loaned out'] = isLoaned;
      markDirty('Loaned out');

      renderLoanStatus(isLoaned);
      triggerAutoSave();
    }

    function renderLoanStatus(isLoaned) {
      const isLoanedBool = (
        isLoaned === true ||
        isLoaned === 1 ||
        String(isLoaned).trim().toLowerCase() === 'true' ||
        String(isLoaned).trim() === '1' ||
        String(isLoaned).trim().toLowerCase() === 'yes'
      );

      const btnAvail = document.getElementById('btnStatusAvailable');
      const btnLoan = document.getElementById('btnStatusLoan');
      const tag = document.getElementById('loanStateTag');
      const dot = document.getElementById('loanStatusDot');

      if (isLoanedBool) {
        btnLoan.className = 'py-1.5 px-2 rounded text-xs font-mono font-semibold flex items-center justify-center gap-1.5 transition-all bg-white text-ink border border-stone-300 min-h-[36px]';
        btnAvail.className = 'py-1.5 px-2 rounded text-xs font-mono font-medium flex items-center justify-center gap-1.5 transition-all text-muted hover:text-ink min-h-[36px]';
        tag.textContent = 'Loaned Out';
        tag.className = 'text-[10px] font-mono font-semibold px-1.5 py-0.5 rounded bg-amber-50 text-amber-800 border border-amber-300';
        dot.className = 'w-2 h-2 rounded-full bg-amber-500';
      } else {
        btnAvail.className = 'py-1.5 px-2 rounded text-xs font-mono font-semibold flex items-center justify-center gap-1.5 transition-all bg-white text-ink border border-stone-300 min-h-[36px]';
        btnLoan.className = 'py-1.5 px-2 rounded text-xs font-mono font-medium flex items-center justify-center gap-1.5 transition-all text-muted hover:text-ink min-h-[36px]';
        tag.textContent = 'In Collection';
        tag.className = 'text-[10px] font-mono font-semibold px-1.5 py-0.5 rounded bg-fern-light text-fern border border-fern/30';
        dot.className = 'w-2 h-2 rounded-full bg-fern';
      }
    }

    function countActiveProblemsOnRecord(rec) {
      if (!rec) return 0;
      let cnt = 0;
      if (Array.isArray(rec.flagged_issues)) {
        cnt = rec.flagged_issues.filter(i => !i.resolved).length;
      }
      const obs = rec.observation || {};
      for (const [k, v] of Object.entries(obs)) {
        if (k.toLowerCase().includes('problem') && (v === true || String(v).toLowerCase() === 'true' || v === 1 || String(v) === '1')) {
          cnt++;
        }
      }
      return cnt;
    }

    // Active Armed Shelf & Intentional Location Stamping Engine
    function armActiveTargetLocation(loc = {}) {
      if (!loc) return;
      const armed = state.armedLocation || {};
      state.armedLocation = {
        building: loc.Building || loc.building || armed.building || '',
        floor: (loc.Floor !== undefined && loc.Floor !== '—') ? String(loc.Floor) : (armed.floor || ''),
        cabinet: (loc.Cabinet && loc.Cabinet !== '—') ? String(loc.Cabinet) : (armed.cabinet || ''),
        shelf: (loc.Shelf && loc.Shelf !== '—') ? String(loc.Shelf) : (armed.shelf || ''),
        storedAs: loc['Stored as'] || loc.storedAs || armed.storedAs || ''
      };
      state.lastSavedLocation = { ...state.armedLocation };
      try {
        localStorage.setItem('arbor_armed_location', JSON.stringify(state.armedLocation));
        localStorage.setItem('arbor_last_location', JSON.stringify(state.lastSavedLocation));
      } catch(e) {}
      updateArmedShelfBannerUI(state.currentRecord?.observation || {});
      initStationLaunchpad();
    }

    function stampArmedLocation() {
      if (!state.currentRecord) return;
      const armed = state.armedLocation || state.lastSavedLocation;
      if (!armed || (!armed.cabinet && !armed.shelf)) {
        showToast('No active target shelf armed');
        return;
      }
      state.currentRecord.observation = state.currentRecord.observation || {};
      const obs = state.currentRecord.observation;

      const prevLoc = {
        Building: obs.Building,
        Floor: obs.Floor,
        Cabinet: obs.Cabinet,
        Shelf: obs.Shelf,
        'Stored as': obs['Stored as']
      };
      const curCab = String(obs.Cabinet || '').trim();
      const wasRelocation = Boolean(curCab && curCab !== '—' && curCab !== String(armed.cabinet || '').trim());

      if (armed.building) { obs.Building = armed.building; markDirty('Building'); }
      if (armed.floor !== undefined && armed.floor !== '—') { obs.Floor = String(armed.floor); markDirty('Floor'); }
      if (armed.cabinet && armed.cabinet !== '—') { obs.Cabinet = String(armed.cabinet); markDirty('Cabinet'); }
      if (armed.shelf && armed.shelf !== '—') { obs.Shelf = String(armed.shelf); markDirty('Shelf'); }
      if (armed.storedAs) { obs['Stored as'] = armed.storedAs; markDirty('Stored as'); }

      renderCoordinateSteppers(obs);
      populateDetailBuildingOptions(obs.Building);
      renderDetailStoredAsPills(obs['Stored as']);
      updateDetailLocBreadcrumbs(obs);
      updateArmedShelfBannerUI(obs);
      triggerAutoSave();
      triggerHaptic('copy_prev');

      const armedCab = String(armed.cabinet || '—').padStart(2, '0');
      const armedShelf = String(armed.shelf || '—').padStart(2, '0');
      if (wasRelocation) {
        showToast(`⚠️ Relocated from Cab ${prevLoc.Cabinet || '?'} to Cab ${armedCab}`, {
          actionText: '↩ Undo',
          duration: 5000,
          onAction: () => {
            if (prevLoc.Building !== undefined) { obs.Building = prevLoc.Building; markDirty('Building'); }
            if (prevLoc.Floor !== undefined) { obs.Floor = prevLoc.Floor; markDirty('Floor'); }
            if (prevLoc.Cabinet !== undefined) { obs.Cabinet = prevLoc.Cabinet; markDirty('Cabinet'); }
            if (prevLoc.Shelf !== undefined) { obs.Shelf = prevLoc.Shelf; markDirty('Shelf'); }
            if (prevLoc['Stored as'] !== undefined) { obs['Stored as'] = prevLoc['Stored as']; markDirty('Stored as'); }
            renderCoordinateSteppers(obs);
            populateDetailBuildingOptions(obs.Building);
            renderDetailStoredAsPills(obs['Stored as']);
            updateDetailLocBreadcrumbs(obs);
            updateArmedShelfBannerUI(obs);
            triggerAutoSave();
            showToast('↩ Relocation undone');
          }
        });
      } else {
        showToast(`📍 Stamped to Cab ${armedCab} · Sh ${armedShelf}`);
      }
    }

    function updateArmedShelfBannerUI(obs = {}) {
      const banner = document.getElementById('armedShelfBanner');
      const label = document.getElementById('armedShelfHeaderLabel');
      const stampBtn = document.getElementById('btnStampArmedShelf');
      if (!banner || !label) return;

      const armed = state.armedLocation || state.lastSavedLocation;
      const hasArmed = Boolean(armed && (armed.cabinet || armed.shelf));

      if (!hasArmed) {
        label.textContent = 'None Armed (Set below)';
        if (stampBtn) stampBtn.classList.add('hidden');
        return;
      }

      const armedCab = String(armed.cabinet || '—').padStart(2, '0');
      const armedShelf = String(armed.shelf || '—').padStart(2, '0');
      label.textContent = `Cab ${armedCab} · Sh ${armedShelf}`;

      const normCoord = (v) => {
        const s = String(v ?? '').trim();
        if (!s || s === '—') return '';
        if (/^\\d+$/.test(s)) return s.replace(/^0+/, '') || '0';
        return s.toLowerCase();
      };

      const armedBldg = normCoord(armed.building);
      const armedFloor = normCoord(armed.floor);
      const armedCabNorm = normCoord(armed.cabinet);
      const armedShelfNorm = normCoord(armed.shelf);

      const curBldg = normCoord(obs.Building);
      const curFloor = normCoord(obs.Floor);
      const curCab = String(obs.Cabinet || '').trim();
      const curCabNorm = normCoord(obs.Cabinet);
      const curShelfNorm = normCoord(obs.Shelf);

      const bldgMatches = !armedBldg || (curBldg === armedBldg);
      const floorMatches = !armedFloor || (curFloor === armedFloor);
      const matches = bldgMatches && floorMatches && (curCabNorm === armedCabNorm) && (curShelfNorm === armedShelfNorm);

      if (stampBtn) {
        if (matches) {
          stampBtn.classList.add('hidden');
        } else {
          stampBtn.classList.remove('hidden');
          const hasExistingLoc = Boolean(curCabNorm || curShelfNorm || curBldg || curFloor);
          const isRelocating = hasExistingLoc && !matches;
          if (isRelocating) {
            stampBtn.className = 'px-2.5 py-1 rounded bg-amber-600 hover:bg-amber-700 text-white font-mono font-bold text-[10px] shadow-2xs tap-active flex items-center gap-1 transition-all';
            stampBtn.innerHTML = `<span>⚠️</span><span>Relocate to Cab ${armedCab}</span>`;
          } else {
            stampBtn.className = 'px-2.5 py-1 rounded bg-fern hover:bg-fern-dark text-white font-mono font-bold text-[10px] shadow-2xs tap-active flex items-center gap-1 transition-all';
            stampBtn.innerHTML = `<span>⚡</span><span>Stamp Target (Cab ${armedCab})</span>`;
          }
        }
      }
    }

    // Copy from Previous Logic
    function handleCopyPreviousSpecimen() {
      stampArmedLocation();
    }

    function updateDetailLocBreadcrumbs(obs = {}) {
      let locBreadcrumb = [];
      if (obs.Building && String(obs.Building).trim()) locBreadcrumb.push(obs.Building);
      if (obs.Floor !== undefined && obs.Floor !== null && String(obs.Floor).trim() !== '' && String(obs.Floor).trim() !== '—') locBreadcrumb.push(`Floor ${obs.Floor}`);
      if (obs.Cabinet && String(obs.Cabinet).trim() && String(obs.Cabinet).trim() !== '—') locBreadcrumb.push(`Cab ${String(obs.Cabinet).trim().padStart(2, '0')}`);
      if (obs.Shelf && String(obs.Shelf).trim() && String(obs.Shelf).trim() !== '—') locBreadcrumb.push(`Sh ${String(obs.Shelf).trim().padStart(2, '0')}`);
      const locStr = locBreadcrumb.length > 0 ? locBreadcrumb.join(' › ') : 'Unrecorded location';

      const liveEl = document.getElementById('liveLocBreadcrumb');
      if (liveEl) liveEl.textContent = locStr;
      const headerEl = document.getElementById('headerLocSummary');
      if (headerEl) headerEl.textContent = locBreadcrumb.length > 0 ? locBreadcrumb.join(' · ') : 'Unrecorded';
      const statusEl = document.getElementById('liveLocStatus');
      if (statusEl) {
        if (locBreadcrumb.length > 0) {
          statusEl.textContent = '✓ Validated';
          statusEl.className = 'text-[10px] font-mono text-fern font-bold whitespace-nowrap ml-1';
        } else {
          statusEl.textContent = 'Coordinates';
          statusEl.className = 'text-[10px] font-mono text-muted whitespace-nowrap ml-1';
        }
      }

      // Update Tab Location Badge
      const locBadge = document.getElementById('tabLocationBadge');
      if (locBadge) {
        locBadge.classList.remove('hidden');
        if (obs.Cabinet && String(obs.Cabinet).trim() && String(obs.Cabinet).trim() !== '—') {
          locBadge.textContent = `Cab ${String(obs.Cabinet).trim().padStart(2, '0')}`;
          locBadge.className = 'font-mono text-[10px] font-bold px-1.5 rounded-full bg-emerald-600 text-white shadow-2xs';
        } else {
          locBadge.textContent = 'Unset ⚠️';
          locBadge.className = 'font-mono text-[10px] font-bold px-1.5 rounded-full bg-amber-500 text-white shadow-2xs';
        }
      }

      // Safe update of armed shelf banner without passive cache corruption
      updateArmedShelfBannerUI(obs);
    }

    // Smart Non-Coercive Review Handler
    function handleReviewButtonClick() {
      if (!state.currentRecord) return;
      const armed = state.armedLocation || state.lastSavedLocation;
      const hasArmed = Boolean(armed && (armed.cabinet || armed.shelf));

      // If already reviewed (unmarking) or no target shelf armed, toggle directly
      if (state.isReviewed || !hasArmed) {
        toggleReviewed();
        return;
      }

      const obs = state.currentRecord.observation || {};
      const curCab = String(obs.Cabinet || '').trim();
      const curShelf = String(obs.Shelf || '').trim();

      const normCoord = (v) => {
        const s = String(v ?? '').trim();
        if (!s || s === '—') return '';
        if (/^\\d+$/.test(s)) return s.replace(/^0+/, '') || '0';
        return s.toLowerCase();
      };
      const armedBldg = normCoord(armed.building);
      const armedFloor = normCoord(armed.floor);
      const bldgMatches = !armedBldg || (normCoord(obs.Building) === armedBldg);
      const floorMatches = !armedFloor || (normCoord(obs.Floor) === armedFloor);
      const matches = bldgMatches && floorMatches &&
        (normCoord(obs.Cabinet) === normCoord(armed.cabinet)) &&
        (normCoord(obs.Shelf) === normCoord(armed.shelf));
      if (matches) {
        toggleReviewed();
        return;
      }

      // Current location differs or is blank -> prompt non-coercive choice
      openArmedConfirmModal(armed, curCab, curShelf);
    }

    function openArmedConfirmModal(armed, curCab, curShelf) {
      const modal = document.getElementById('armedConfirmModal');
      if (!modal) {
        toggleReviewed();
        return;
      }
      const curText = (curCab || curShelf) ? `Cabinet ${curCab || '—'}, Shelf ${curShelf || '—'}` : 'Unrecorded';
      const armedText = `Cabinet ${armed.cabinet || '—'}, Shelf ${armed.shelf || '—'}`;

      document.getElementById('armedModalCurLoc').textContent = curText;
      document.getElementById('armedModalTargetLoc').textContent = armedText;
      modal.classList.remove('hidden');
    }

    function confirmStampAndReview() {
      const modal = document.getElementById('armedConfirmModal');
      if (modal) modal.classList.add('hidden');

      stampArmedLocation();
      if (!state.isReviewed) {
        toggleReviewed();
      }
      showToast('✓ Stamped to target shelf & marked reviewed');
    }

    function confirmKeepAndReview() {
      const modal = document.getElementById('armedConfirmModal');
      if (modal) modal.classList.add('hidden');

      // PRESERVES USER INTENT: Keep location unchanged and safely mark reviewed!
      if (!state.isReviewed) {
        toggleReviewed();
      }
      showToast('✓ Kept current location & marked reviewed');
    }

    function cancelArmedModal() {
      const modal = document.getElementById('armedConfirmModal');
      if (modal) modal.classList.add('hidden');
    }

    function toggleReviewed() {
      state.isReviewed = !state.isReviewed;
      triggerHaptic(state.isReviewed ? 'reviewed_on' : 'reviewed_off');
      if (state.currentRecord) {
        state.currentRecord.observation = state.currentRecord.observation || {};
        state.currentRecord.observation.Reviewed = state.isReviewed;
        markDirty('Reviewed');
        triggerAutoSave();
      }
      renderDetailView(false);
    }

    function navSpecimen(delta) {
      if (state.objectList.length === 0) return;
      const curIdx = state.objectList.findIndex(o => String(o.id) === String(state.currentOid));
      if (curIdx < 0) return;
      const nextIdx = Math.max(0, Math.min(state.objectList.length - 1, curIdx + delta));
      if (nextIdx !== curIdx) {
        openDetailView(state.objectList[nextIdx].id);
      }
    }

    // -------------------------------------------------------------
    // TAB CONTROLLER & GESTURES
    // -------------------------------------------------------------
    function switchDetailTab(tab) {
      let idx = 0;
      if (typeof tab === 'number') idx = tab;
      else if (tab === 'details') idx = 0;
      else if (tab === 'location') idx = 1;
      else if (tab === 'problems') idx = 2;
      switchTab(idx);
    }

    function switchTab(idx) {
      currentTabIdx = idx;
      const indicator = document.getElementById('tabIndicator');
      const track = document.getElementById('tabTrack');
      if (indicator) indicator.style.transform = `translateX(${idx * 100}%)`;
      if (track) track.style.transform = `translateX(-${(idx * 100) / 3}%)`;

      document.querySelectorAll('.tab-btn').forEach((btn, i) => {
        if (i === idx) {
          btn.classList.add('font-semibold', 'text-ink');
          btn.classList.remove('text-muted');
        } else {
          btn.classList.remove('font-semibold', 'text-ink');
          btn.classList.add('text-muted');
        }
      });
    }

    // -------------------------------------------------------------
    // DETAILS & PROBLEMS FORM RENDERING
    // -------------------------------------------------------------
    function renderDynamicForm(schema, record) {
      const container = document.getElementById('dynamicFormContainer');
      if (!container || !schema) return;
      const reg = record.registration || {};
      const obs = record.observation || {};

      let html = '<h3 class="text-xs font-bold text-ink uppercase tracking-wider font-sans mb-2">Botanical Registration</h3>';
      const fields = ['Genus', 'Species', 'Family', 'Author', 'Collector', 'Collection Date', 'Collection place', 'Box label'];
      
      html += '<div class="space-y-2 font-mono text-xs">';
      fields.forEach(f => {
        let val = '';
        if (f === 'Collection place') {
          val = (obs['Collection place'] !== undefined && obs['Collection place'] !== '') ? obs['Collection place'] :
                ((obs['Collection Place'] !== undefined && obs['Collection Place'] !== '') ? obs['Collection Place'] :
                ((reg['Collection place'] !== undefined && reg['Collection place'] !== '') ? reg['Collection place'] :
                ((reg['Collection Place'] !== undefined && reg['Collection Place'] !== '') ? reg['Collection Place'] : '')));
        } else if (f === 'Box label') {
          val = (obs['Box label'] !== undefined && obs['Box label'] !== '') ? obs['Box label'] :
                ((obs['Box Label'] !== undefined && obs['Box Label'] !== '') ? obs['Box Label'] :
                ((reg['Box label'] !== undefined && reg['Box label'] !== '') ? reg['Box label'] :
                ((reg['Box Label'] !== undefined && reg['Box Label'] !== '') ? reg['Box Label'] : '')));
        } else {
          val = obs[f] !== undefined && obs[f] !== '' ? obs[f] : (reg[f] || '');
        }

        const isBoxLabel = (f === 'Box label');
        const strVal = String(val || '').trim();
        const isMultiline = isBoxLabel && strVal && (strVal.indexOf('\\n') !== -1 || strVal.indexOf('\\r') !== -1 || strVal.length > 28);

        if (isMultiline) {
          html += `
            <div class="py-1.5 border-b border-stone-100 space-y-1">
              <div class="flex items-center justify-between">
                <span class="text-muted text-[11px]">${f}:</span>
                <span class="text-[9.5px] font-mono text-subdued">(Full label)</span>
              </div>
              <div class="font-semibold text-ink text-left text-xs whitespace-pre-wrap break-words bg-stone-50 border border-stone-200/60 rounded p-2 leading-relaxed">
                ${escapeHtml(strVal)}
              </div>
            </div>
          `;
        } else {
          html += `
            <div class="flex items-center justify-between py-1 border-b border-stone-100">
              <span class="text-muted text-[11px]">${f}:</span>
              <span class="font-semibold text-ink text-right break-words max-w-[200px]">${escapeHtml(strVal) || '—'}</span>
            </div>
          `;
        }
      });
      html += '</div>';

      // Comment section below Botanical Registration
      const commentRaw = (obs['Comment'] !== undefined && obs['Comment'] !== null && String(obs['Comment']).trim() !== '')
        ? String(obs['Comment']).trim()
        : ((reg['Comment'] !== undefined && reg['Comment'] !== null && String(reg['Comment']).trim() !== '')
          ? String(reg['Comment']).trim()
          : ((obs['Comments'] !== undefined && obs['Comments'] !== null && String(obs['Comments']).trim() !== '')
            ? String(obs['Comments']).trim()
            : ((reg['Comments'] !== undefined && reg['Comments'] !== null && String(reg['Comments']).trim() !== '')
              ? String(reg['Comments']).trim()
              : '')));
      const hasComment = Boolean(commentRaw);

      html += `
        <div class="mt-4 pt-3 border-t border-bordercol/60 space-y-2">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-1.5">
              <svg class="w-3.5 h-3.5 text-fern" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z"/>
              </svg>
              <h4 class="text-xs font-bold text-ink uppercase tracking-wider font-sans">Comment</h4>
            </div>
            <button type="button" onclick="openCommentEditor()" class="px-2.5 py-1 text-[11px] font-mono font-medium text-fern hover:text-fern-dark bg-emerald-50 hover:bg-emerald-100 border border-fern/30 rounded flex items-center gap-1 transition-colors touch-target-min">
              <svg class="w-3 h-3 text-fern" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
              <span>${hasComment ? 'Edit Comment' : 'Write Comment'}</span>
            </button>
          </div>
          <div onclick="openCommentEditor()" class="min-h-[72px] p-2.5 bg-stone-50 hover:bg-stone-100/70 border border-stone-200/80 rounded cursor-pointer transition-colors" title="Tap to write or edit comment">
            <p class="font-mono text-xs text-ink whitespace-pre-wrap break-words leading-relaxed ${hasComment ? '' : 'text-subdued italic'}">
              ${hasComment ? escapeHtml(commentRaw) : 'No comment recorded. Tap to write a comment...'}
            </p>
          </div>
        </div>
      `;

      container.innerHTML = html;
    }

    function openCommentEditor() {
      if (!state.currentRecord) return;
      const reg = state.currentRecord.registration || {};
      const obs = state.currentRecord.observation || {};
      const currentComment = (obs['Comment'] !== undefined && obs['Comment'] !== null && String(obs['Comment']).trim() !== '')
        ? String(obs['Comment']).trim()
        : ((reg['Comment'] !== undefined && reg['Comment'] !== null && String(reg['Comment']).trim() !== '')
          ? String(reg['Comment']).trim()
          : ((obs['Comments'] !== undefined && obs['Comments'] !== null && String(obs['Comments']).trim() !== '')
            ? String(obs['Comments']).trim()
            : ((reg['Comments'] !== undefined && reg['Comments'] !== null && String(reg['Comments']).trim() !== '')
              ? String(reg['Comments']).trim()
              : '')));

      const textarea = document.getElementById('commentEditTextarea');
      if (textarea) textarea.value = currentComment;
      const title = document.getElementById('commentModalTitle');
      if (title) title.textContent = `Comment — #${state.currentRecord.id || state.currentOid}`;
      openModal('commentEditorModal');
      setTimeout(() => textarea?.focus(), 100);
    }

    function closeCommentEditor() {
      closeModal('commentEditorModal');
    }

    function saveCommentFromEditor() {
      if (!state.currentRecord) return;
      const textarea = document.getElementById('commentEditTextarea');
      const newVal = textarea ? textarea.value.trim() : '';

      state.currentRecord.observation = state.currentRecord.observation || {};
      state.currentRecord.registration = state.currentRecord.registration || {};
      state.currentRecord.observation.Comment = newVal;
      state.currentRecord.registration.Comment = newVal;
      markDirty('Comment');

      closeCommentEditor();
      renderDynamicForm(state.activeSchema, state.currentRecord);
      triggerAutoSave();
      showToast(newVal ? '✓ Comment saved & synchronized' : '✓ Comment cleared');
    }

    let currentPhotoCandidates = [];
    let currentPhotoCandidateIdx = 0;

    function renderPhotos(images = {}) {
      const urls = (images.local_endpoints && images.local_endpoints.length > 0)
        ? images.local_endpoints
        : (images.online_urls || []);

      currentPhotoCandidates = urls;
      currentPhotoCandidateIdx = 0;

      const thumbsRow = document.getElementById('photoThumbnailsRow');
      if (thumbsRow) thumbsRow.innerHTML = '';

      if (!urls || urls.length === 0) {
        collapseEmptyPhotoFolio('None registered');
        return;
      }

      const countDisp = document.getElementById('photoCountDisplay');
      if (countDisp) countDisp.textContent = 'Testing candidate...';
      tryLoadPhotoCandidate(0);
    }

    function tryLoadPhotoCandidate(idx) {
      if (!currentPhotoCandidates || idx >= currentPhotoCandidates.length) {
        collapseEmptyPhotoFolio('None verified online');
        return;
      }
      currentPhotoCandidateIdx = idx;
      const url = currentPhotoCandidates[idx];
      const img = document.getElementById('specimenImg');
      if (img) {
        img.src = url;
      }
    }

    function onPhotoLoaded(imgEl) {
      const target = imgEl || document.getElementById('specimenImg');
      if (!target) return;
      if (target.naturalWidth >= 50 && target.naturalHeight >= 50) {
        expandVerifiedPhotoFolio(target.src);
      } else {
        tryLoadPhotoCandidate(currentPhotoCandidateIdx + 1);
      }
    }

    function onPhotoError() {
      tryLoadPhotoCandidate(currentPhotoCandidateIdx + 1);
    }

    function expandVerifiedPhotoFolio(verifiedUrl) {
      const mainBox = document.getElementById('photoMainBox');
      const img = document.getElementById('specimenImg');
      const placeholder = document.getElementById('photoPlaceholder');
      const countDisp = document.getElementById('photoCountDisplay');
      const tabBadge = document.getElementById('tabFolioBadge');
      const thumbsRow = document.getElementById('photoThumbnailsRow');
      const viewerImg = document.getElementById('photoViewerImg');

      if (mainBox) mainBox.classList.remove('hidden');
      if (img) img.classList.remove('hidden');
      if (placeholder) placeholder.classList.add('hidden');
      if (viewerImg) viewerImg.src = verifiedUrl;
      if (countDisp) countDisp.textContent = '1 Verified Scan';
      if (tabBadge) {
        tabBadge.textContent = '📷';
        tabBadge.classList.remove('hidden');
      }

      if (thumbsRow && currentPhotoCandidates.length > 1) {
        thumbsRow.innerHTML = currentPhotoCandidates.map((u, i) => `
          <img src="${u}" onclick="selectPhoto(${i}, '${u}')" class="w-12 h-12 rounded border ${i === currentPhotoCandidateIdx ? 'border-fern ring-2 ring-fern/30' : 'border-bordercol'} object-cover cursor-pointer hover:border-fern">
        `).join('');
      } else if (thumbsRow) {
        thumbsRow.innerHTML = '';
      }
    }

    function collapseEmptyPhotoFolio(reason = 'None verified') {
      const mainBox = document.getElementById('photoMainBox');
      const img = document.getElementById('specimenImg');
      const placeholder = document.getElementById('photoPlaceholder');
      const countDisp = document.getElementById('photoCountDisplay');
      const thumbsRow = document.getElementById('photoThumbnailsRow');
      const tabBadge = document.getElementById('tabFolioBadge');

      if (mainBox) mainBox.classList.add('hidden');
      if (img) img.classList.add('hidden');
      if (thumbsRow) thumbsRow.innerHTML = '';
      if (tabBadge) tabBadge.classList.add('hidden');
      if (countDisp) countDisp.textContent = 'No photo';

      if (placeholder) {
        placeholder.innerHTML = `
          <div class="py-1 px-2.5 bg-stone-100 rounded border border-bordercol/70 flex items-center justify-between text-xs font-mono text-muted">
            <span class="flex items-center gap-1.5 text-stone-500">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
              Scan: ${reason}
            </span>
            <span class="text-[10px] text-stone-400 italic">Viewport reclaimed</span>
          </div>
        `;
        placeholder.classList.remove('hidden');
      }
    }

    function selectPhoto(idx, url) {
      currentPhotoCandidateIdx = idx;
      const img = document.getElementById('specimenImg');
      const viewerImg = document.getElementById('photoViewerImg');
      if (img) img.src = url;
      if (viewerImg) viewerImg.src = url;
      expandVerifiedPhotoFolio(url);
    }

    function openPhotoViewerModal() {
      document.getElementById('photoViewerModal')?.classList.remove('hidden');
    }

    function closePhotoViewerModal() {
      document.getElementById('photoViewerModal')?.classList.add('hidden');
    }

    let photoZoom = 1;
    let photoRotation = 0;
    function zoomPhoto(delta) {
      photoZoom = Math.min(Math.max(photoZoom + delta, 0.5), 4);
      updatePhotoTransform();
    }
    function rotatePhoto() {
      photoRotation = (photoRotation + 90) % 360;
      updatePhotoTransform();
    }
    function resetPhotoTransform() {
      photoZoom = 1;
      photoRotation = 0;
      updatePhotoTransform();
    }
    function updatePhotoTransform() {
      const img = document.getElementById('photoViewerImg');
      document.getElementById('zoomLevelDisplay').textContent = `${photoZoom.toFixed(1)}x`;
      if (img) img.style.transform = `scale(${photoZoom}) rotate(${photoRotation}deg)`;
    }

    function isProblemActiveOnRecord(probName, rec) {
      if (!rec) return false;
      const obs = rec.observation || {};
      const reg = rec.registration || {};
      const v = obs[probName] !== undefined ? obs[probName] : reg[probName];
      if (typeof v === 'boolean') return v;
      if (typeof v === 'number') return v === 1;
      const s = String(v || '').trim().toLowerCase();
      return ['true', '1', 'yes', 'x'].includes(s);
    }

    function renderProblemsAndDiscrepancies(rec) {
      if (!rec) return;
      const obs = rec.observation || {};
      const reg = rec.registration || {};

      let problemDefs = (state.activeSchema && state.activeSchema.ui_sections && Array.isArray(state.activeSchema.ui_sections.problems))
        ? [...state.activeSchema.ui_sections.problems]
        : [];

      if (problemDefs.length === 0) {
        problemDefs = [
          { name: 'Author_Problem', label: 'Author Discrepancy', maps_to: 'Author' },
          { name: 'Family_Problem', label: 'Family Discrepancy', maps_to: 'Family' },
          { name: 'Genus_Problem', label: 'Genus Discrepancy', maps_to: 'Genus' },
          { name: 'Species_Problem', label: 'Species Discrepancy', maps_to: 'Species' },
          { name: 'Collector_Problem', label: 'Collector Discrepancy', maps_to: 'Collector' },
          { name: 'Date_Problem', label: 'Date Discrepancy', maps_to: 'Collection Date' },
          { name: 'Locality_Problem', label: 'Locality Discrepancy', maps_to: 'Locality' },
          { name: 'County_Problem', label: 'County Discrepancy', maps_to: 'County' },
          { name: 'Country_Problem', label: 'Country Discrepancy', maps_to: 'Country' },
          { name: 'Location_Problem', label: 'Location Discrepancy', maps_to: 'Cabinet' },
          { name: 'General_Problem', label: 'General Discrepancy', maps_to: 'Notes' }
        ];
      }

      // Collect all active discrepancies
      const activeProblems = [];
      problemDefs.forEach(pDef => {
        if (isProblemActiveOnRecord(pDef.name, rec)) {
          activeProblems.push({
            name: pDef.name,
            label: pDef.label || pDef.name,
            maps_to: pDef.maps_to || state.problemToField[pDef.name] || (pDef.name.endsWith('_Problem') ? pDef.name.replace(/_Problem$/, '') : pDef.name)
          });
        }
      });

      if (Array.isArray(rec.flagged_issues)) {
        rec.flagged_issues.forEach(iss => {
          const id = iss.id || iss.field;
          if (id && !activeProblems.some(p => p.name === id) && isProblemActiveOnRecord(id, rec)) {
            activeProblems.push({
              name: id,
              label: iss.field || iss.reason || id,
              maps_to: iss.field || state.problemToField[id] || (id.endsWith('_Problem') ? id.replace(/_Problem$/, '') : id)
            });
          }
        });
      }

      const count = activeProblems.length;

      // 1. Tab Badge
      const tabBadge = document.getElementById('tabProblemBadge');
      if (tabBadge) {
        if (count > 0) {
          tabBadge.textContent = count;
          tabBadge.classList.remove('hidden');
        } else {
          tabBadge.classList.add('hidden');
        }
      }

      // 2. Summary Banner
      const summaryBar = document.getElementById('problemSummaryBar');
      const summaryDot = document.getElementById('problemSummaryDot');
      const summaryCountText = document.getElementById('problemSummaryCountText');
      const summaryActionText = document.getElementById('problemSummaryActionText');
      if (summaryBar) {
        if (count > 0) {
          summaryBar.className = 'flex items-center justify-between p-3 bg-brick-light/50 border border-brick/30 rounded-[3px] transition-colors duration-200';
          if (summaryDot) summaryDot.className = 'w-2.5 h-2.5 rounded-full bg-brick animate-pulse';
          if (summaryCountText) {
            summaryCountText.className = 'text-xs font-bold text-brick uppercase font-mono';
            summaryCountText.textContent = `${count} Active Discrepanc${count === 1 ? 'y' : 'ies'}`;
          }
          if (summaryActionText) {
            summaryActionText.className = 'text-[10px] font-mono text-brick font-semibold';
            summaryActionText.textContent = 'Review & Resolve';
          }
        } else {
          summaryBar.className = 'flex items-center justify-between p-3 bg-emerald-50/70 border border-fern/30 rounded-[3px] transition-colors duration-200';
          if (summaryDot) summaryDot.className = 'w-2.5 h-2.5 rounded-full bg-fern';
          if (summaryCountText) {
            summaryCountText.className = 'text-xs font-bold text-fern-dark uppercase font-mono';
            summaryCountText.textContent = '0 Discrepancies · Clean Data';
          }
          if (summaryActionText) {
            summaryActionText.className = 'text-[10px] font-mono text-fern font-medium';
            summaryActionText.textContent = 'All Validated';
          }
        }
      }

      // 3. Discrepancy Cards Container
      const container = document.getElementById('activeDiscrepanciesContainer');
      if (container) {
        if (count === 0) {
          container.innerHTML = `
            <div class="p-6 bg-surface border border-bordercol rounded-[3px] text-center space-y-2">
              <div class="w-8 h-8 rounded-full bg-emerald-50 text-fern border border-fern/30 flex items-center justify-center mx-auto text-base">✓</div>
              <div class="text-xs font-mono font-bold text-ink">No Curatorial Discrepancies</div>
              <p class="text-[11px] text-subdued font-sans max-w-xs mx-auto">This specimen currently has no flagged discrepancies. You can toggle data integrity flags below if curatorial attention is needed.</p>
            </div>
          `;
        } else {
          container.innerHTML = activeProblems.map(p => {
            const probName = p.name;
            const label = p.label;
            const targetField = p.maps_to;
            const currentVal = (obs[targetField] !== undefined && obs[targetField] !== '') ? obs[targetField] : ((reg[targetField] !== undefined && reg[targetField] !== '') ? reg[targetField] : '—');

            const histMap = state.currentHistoricalData ? (state.currentHistoricalData[targetField] || {}) : {};
            const histEntries = Object.entries(histMap);

            let histHtml = '';
            if (histEntries.length > 0) {
              histHtml = `
                <div class="space-y-1.5">
                  <span class="text-[9px] uppercase font-bold text-muted block">Historical Records / Prior Determinations</span>
                  <div class="space-y-1.5">
                    ${histEntries.map(([hVal, sources]) => {
                      const sourcesStr = Array.isArray(sources) ? sources.join(', ') : String(sources);
                      const safeVal = escapeHtml(hVal);
                      const jsVal = safeVal.replace(/'/g, "\\'");
                      return `
                        <div class="p-2 bg-emerald-50/50 border border-fern/30 rounded flex items-center justify-between gap-2">
                          <div class="truncate min-w-0">
                            <span class="font-mono text-xs font-bold text-ink block truncate">${safeVal}</span>
                            <span class="text-[9px] font-mono text-fern-dark block truncate">Sources: ${escapeHtml(sourcesStr)}</span>
                          </div>
                          <button type="button" onclick="resolveFieldDiscrepancy('${targetField}', '${probName}', '${jsVal}', true)" class="flex-none px-2.5 py-1 bg-fern hover:bg-fern-dark text-white rounded text-[10px] font-mono font-bold shadow-2xs">
                            Apply Fix
                          </button>
                        </div>
                      `;
                    }).join('')}
                  </div>
                </div>
              `;
            } else {
              histHtml = `
                <div class="p-2 bg-stone-50 border border-dashed border-stone-200 rounded text-[10.5px] font-mono text-muted text-center">
                  No earlier historical determinations found for this field.
                </div>
              `;
            }

            return `
              <div class="bg-surface border border-bordercol rounded-[3px] p-3.5 shadow-2xs space-y-3">
                <div class="flex items-center justify-between border-b border-stone-100 pb-2">
                  <div class="flex items-center gap-1.5 truncate mr-2">
                    <span class="w-2 h-2 rounded-full bg-brick flex-none"></span>
                    <span class="text-xs font-mono font-bold text-ink truncate">${escapeHtml(targetField)}</span>
                    <span class="text-[10px] font-mono text-brick bg-brick-light px-1.5 py-0.5 rounded border border-brick/20 font-medium whitespace-nowrap">${escapeHtml(label)}</span>
                  </div>
                  <button type="button" onclick="resolveFieldDiscrepancy('${targetField}', '${probName}', undefined, true)" class="flex-none text-[10px] font-mono text-muted hover:text-ink px-2 py-1 rounded bg-stone-100 hover:bg-stone-200 border border-stone-200">
                    Dismiss Flag
                  </button>
                </div>

                <div class="bg-stone-50 border border-stone-200 rounded p-2 text-xs font-mono flex items-center justify-between">
                  <div class="truncate mr-2">
                    <span class="text-[9px] uppercase font-bold text-muted block">Current Value</span>
                    <span class="font-bold text-ink truncate">${escapeHtml(currentVal)}</span>
                  </div>
                  <span class="text-[10px] text-muted whitespace-nowrap bg-white px-1.5 py-0.5 rounded border border-stone-200">Active</span>
                </div>

                ${histHtml}

                <div class="pt-1">
                  <span class="text-[9px] uppercase font-bold text-muted block mb-1">Manual Override</span>
                  <div class="flex items-center gap-1.5">
                    <input type="text" id="manualInput_${probName}" placeholder="Enter new value..." class="flex-1 bg-white border border-bordercol rounded px-2.5 py-1.5 text-xs font-mono text-ink focus:outline-none focus:border-fern" />
                    <button type="button" onclick="applyManualProblemResolution('${targetField}', '${probName}')" class="px-2.5 py-1.5 rounded bg-stone-100 hover:bg-stone-200 active:bg-stone-300 border border-stone-300 text-ink text-xs font-mono font-semibold min-h-[34px] whitespace-nowrap">
                      Apply Manual
                    </button>
                  </div>
                </div>

                <div class="pt-1">
                  <button type="button" onclick="toggleIcedigTray('${probName}')" class="w-full flex items-center justify-between px-2.5 py-1.5 rounded bg-stone-50 hover:bg-stone-100 border border-stone-200 text-ink text-xs font-mono font-medium transition-colors">
                    <span class="flex items-center gap-1.5">
                      <span class="text-fern font-bold">?</span>
                      <span>Set as Unknown (ICEDIG)...</span>
                    </span>
                    <span id="icedigArrow_${probName}" class="text-[10px] text-muted">▼</span>
                  </button>

                  <div id="icedigTray_${probName}" class="hidden mt-2 p-2 bg-stone-50 border border-bordercol rounded space-y-1.5">
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-1.5">
                      ${(() => {
                        const icedigMap = (state.icedigCodes && Object.keys(state.icedigCodes).length > 0)
                          ? state.icedigCodes
                          : ((state.activeSchema && state.activeSchema.icedig_code_labels) || {
                              "unknown:missing": "unknown:missing  (blank on original label)",
                              "unknown:indecipherable": "unknown:indecipherable  (illegible on label)",
                              "unknown:undigitized": "unknown:undigitized  (skipped during digitisation)",
                              "withheld": "withheld  (known but intentionally hidden)"
                            });

                        return Object.entries(icedigMap).map(([code, fullLabel]) => {
                          const isSel = (String(currentVal).trim().toLowerCase() === code.toLowerCase());
                          let subText = '';
                          const parenMatch = fullLabel.match(/\\((.*?)\\)/);
                          if (parenMatch) {
                            subText = parenMatch[1];
                          } else if (fullLabel.includes('  ')) {
                            subText = fullLabel.split(/\\s{2,}/)[1] || '';
                          } else {
                            subText = fullLabel.replace(code, '').trim();
                          }

                          const pillClass = isSel
                            ? 'w-full text-left p-2 rounded border-2 border-fern bg-emerald-50 text-fern-dark font-semibold shadow-2xs transition-all'
                            : 'w-full text-left p-2 rounded border border-bordercol bg-white text-ink hover:border-fern/50 hover:bg-stone-50 active:scale-[0.99] transition-all';

                          const jsCode = code.replace(/'/g, "\\'");
                          return `
                            <button type="button" onclick="resolveFieldDiscrepancy('${targetField}', '${probName}', '${jsCode}', true)" class="${pillClass}">
                              <div class="flex items-center justify-between gap-1">
                                <span class="font-mono text-xs font-bold truncate">${escapeHtml(code)}</span>
                                ${isSel ? '<span class="text-[10px] text-fern font-bold flex-none">✓</span>' : ''}
                              </div>
                              ${subText ? `<span class="text-[9.5px] font-sans text-subdued block leading-tight mt-0.5 truncate">${escapeHtml(subText)}</span>` : ''}
                            </button>
                          `;
                        }).join('')
                      })()}
                    </div>
                  </div>
                </div>
              </div>
            `;
          }).join('');
        }
      }

      // 4. Schema Data Integrity Flags Checklist Grid
      const flagsGrid = document.getElementById('problemFlagsGrid');
      const flaggedBadge = document.getElementById('flaggedTotalBadge');
      if (flaggedBadge) {
        flaggedBadge.textContent = `${count} Flagged`;
      }
      if (flagsGrid) {
        flagsGrid.innerHTML = problemDefs.map(pDef => {
          const probName = pDef.name;
          const isAct = isProblemActiveOnRecord(probName, rec);
          const label = pDef.label || probName;
          return `
            <button type="button" onclick="toggleProblemFlag('${probName}')" class="p-2.5 rounded border text-left flex items-start justify-between transition-all tap-highlight-transparent min-h-[44px] ${isAct ? 'border-brick bg-brick-light text-brick font-semibold' : 'border-stone-200 bg-white text-muted hover:border-stone-300'}">
              <div class="min-w-0 pr-1">
                <span class="text-xs font-mono block truncate ${isAct ? 'text-brick' : 'text-ink'}">${escapeHtml(label)}</span>
                <span class="text-[9px] font-mono block truncate opacity-70">${probName}</span>
              </div>
              <span class="w-3.5 h-3.5 rounded-full flex-none mt-0.5 flex items-center justify-center text-[9px] font-bold ${isAct ? 'bg-brick text-white' : 'border border-stone-300'}">
                ${isAct ? '✓' : ''}
              </span>
            </button>
          `;
        }).join('');
      }
    }

    function toggleIcedigTray(probName) {
      const tray = document.getElementById(`icedigTray_${probName}`);
      const arrow = document.getElementById(`icedigArrow_${probName}`);
      if (!tray) return;
      const isHidden = tray.classList.contains('hidden');
      if (isHidden) {
        tray.classList.remove('hidden');
        if (arrow) arrow.textContent = '▲';
      } else {
        tray.classList.add('hidden');
        if (arrow) arrow.textContent = '▼';
      }
    }

    function applyManualProblemResolution(targetField, probName) {
      const inp = document.getElementById(`manualInput_${probName}`);
      if (!inp) return;
      const val = inp.value.trim();
      if (!val) {
        showToast('Please enter a value before applying');
        return;
      }
      resolveFieldDiscrepancy(targetField, probName, val, true);
    }

    function resolveFieldDiscrepancy(targetField, probName, newVal, clearFlag = true) {
      if (!state.currentRecord) return;
      state.currentRecord.observation = state.currentRecord.observation || {};
      state.currentRecord.registration = state.currentRecord.registration || {};

      if (targetField && newVal !== undefined) {
        state.currentRecord.observation[targetField] = newVal;
        state.currentRecord.registration[targetField] = newVal;
        markDirty(targetField);
      }

      if (clearFlag && probName) {
        state.currentRecord.observation[probName] = false;
        markDirty(probName);
      }

      triggerAutoSave();
      renderProblemsAndDiscrepancies(state.currentRecord);
      renderDynamicForm(state.activeSchema, state.currentRecord);
      showToast(newVal !== undefined ? `✓ Applied resolution for ${targetField}` : `✓ Dismissed flag for ${probName}`);
    }

    function toggleProblemFlag(probName) {
      if (!state.currentRecord) return;
      state.currentRecord.observation = state.currentRecord.observation || {};
      const isAct = isProblemActiveOnRecord(probName, state.currentRecord);
      const nextVal = !isAct;
      state.currentRecord.observation[probName] = nextVal;
      markDirty(probName);
      triggerAutoSave();
      triggerHaptic('discrepancy');
      renderProblemsAndDiscrepancies(state.currentRecord);
      showToast(nextVal ? `⚠ Flagged ${probName}` : `✓ Cleared flag ${probName}`);
    }

    // -------------------------------------------------------------
    // SCREEN 3: BATCH LOCATION REGISTRATOR LOGIC
    // -------------------------------------------------------------
    function handleBatchBuildingChange(val) {
      state.batchAnchor.building = val;
      updateBatchAnchorUI();
    }

    function populateBatchBuildingOptions() {
      const select = document.getElementById('batchBuildingSelect');
      if (!select) return;

      let bldgChoices = [];
      if (state.activeSchema && state.activeSchema.ui_sections && Array.isArray(state.activeSchema.ui_sections.location)) {
        const bldgField = state.activeSchema.ui_sections.location.find(f => f && f.name === 'Building' && Array.isArray(f.choices));
        if (bldgField) {
          bldgChoices = bldgField.choices;
        }
      }
      if ((!bldgChoices || bldgChoices.length === 0) && state.activeSchema && state.activeSchema.vocabulary && Array.isArray(state.activeSchema.vocabulary.Building)) {
        bldgChoices = state.activeSchema.vocabulary.Building;
      }
      if (!bldgChoices || bldgChoices.length === 0) {
        bldgChoices = ['Økern', "Lid's hus"];
      }

      const currentVal = (state.batchAnchor.building !== undefined && state.batchAnchor.building !== null)
        ? String(state.batchAnchor.building).trim()
        : '';
      const allChoices = Array.from(new Set([...bldgChoices, currentVal])).filter(Boolean);

      let optionsHtml = '<option value="">--</option>';
      optionsHtml += allChoices.map(b => `<option value="${b.replace(/"/g, '&quot;')}">${b}</option>`).join('');
      select.innerHTML = optionsHtml;
      select.value = currentVal;
      state.batchAnchor.building = currentVal;
    }

    function updateBatchAnchorUI() {
      const bldgSelect = document.getElementById('batchBuildingSelect');
      if (bldgSelect) {
        if (state.batchAnchor.building) {
          if (!Array.from(bldgSelect.options).some(o => o.value === state.batchAnchor.building)) {
            const opt = document.createElement('option');
            opt.value = state.batchAnchor.building;
            opt.textContent = state.batchAnchor.building;
            bldgSelect.appendChild(opt);
          }
          bldgSelect.value = state.batchAnchor.building;
        } else {
          bldgSelect.value = '';
        }
      }

      const hasFloor = (state.batchAnchor.floor !== undefined && state.batchAnchor.floor !== null && String(state.batchAnchor.floor).trim() !== '' && String(state.batchAnchor.floor).trim() !== '—');
      const floorEl = document.getElementById('batchFloorVal');
      if (floorEl) floorEl.textContent = hasFloor ? String(state.batchAnchor.floor).trim() : '—';

      const hasCab = (state.batchAnchor.cabinet !== undefined && state.batchAnchor.cabinet !== null && String(state.batchAnchor.cabinet).trim() !== '' && String(state.batchAnchor.cabinet).trim() !== '—');
      const cabVal = hasCab ? String(state.batchAnchor.cabinet).trim().padStart(2, '0') : '';
      const cabEl = document.getElementById('batchCabVal');
      if (cabEl) {
        if ('value' in cabEl) cabEl.value = cabVal;
        else cabEl.textContent = cabVal || '—';
      }

      const hasShelf = (state.batchAnchor.shelf !== undefined && state.batchAnchor.shelf !== null && String(state.batchAnchor.shelf).trim() !== '' && String(state.batchAnchor.shelf).trim() !== '—');
      const shelfVal = hasShelf ? String(state.batchAnchor.shelf).trim().padStart(2, '0') : '';
      const shelfEl = document.getElementById('batchShelfVal');
      if (shelfEl) {
        if ('value' in shelfEl) shelfEl.value = shelfVal;
        else shelfEl.textContent = shelfVal || '—';
      }

      document.getElementById('batchStoredAsLabel').textContent = state.batchAnchor.storedAs || 'Not Selected';
      
      const nextShelf = hasShelf ? (parseInt(state.batchAnchor.shelf, 10) || 1) + 1 : 1;
      document.getElementById('btnAdvanceNextShelfText').textContent = `Advance to Shelf ${String(nextShelf).padStart(2, '0')}`;

      if (typeof renderBatchStoredAsPills === 'function') {
          renderBatchStoredAsPills();
      }
      renderBatchQueue();
    }

    function adjustBatchCoord(coord, delta) {
      if (coord === 'floor') {
        const isUnset = (state.batchAnchor.floor === undefined || state.batchAnchor.floor === null || String(state.batchAnchor.floor).trim() === '' || String(state.batchAnchor.floor).trim() === '—');
        let next;
        if (isUnset) {
          next = delta > 0 ? 1 : -1;
        } else {
          const parsed = parseInt(state.batchAnchor.floor, 10);
          next = isNaN(parsed) ? (delta > 0 ? 1 : -1) : parsed + delta;
        }
        state.batchAnchor.floor = String(next);
      } else if (coord === 'cab') {
        const isUnset = (state.batchAnchor.cabinet === undefined || state.batchAnchor.cabinet === null || String(state.batchAnchor.cabinet).trim() === '' || String(state.batchAnchor.cabinet).trim() === '—');
        let next;
        if (isUnset) {
          next = 1;
        } else {
          const cur = parseInt(state.batchAnchor.cabinet, 10);
          next = Math.max(1, (isNaN(cur) ? 1 : cur) + delta);
        }
        state.batchAnchor.cabinet = String(next).padStart(2, '0');
      } else if (coord === 'shelf') {
        const isUnset = (state.batchAnchor.shelf === undefined || state.batchAnchor.shelf === null || String(state.batchAnchor.shelf).trim() === '' || String(state.batchAnchor.shelf).trim() === '—');
        let next;
        if (isUnset) {
          next = 1;
        } else {
          const cur = parseInt(state.batchAnchor.shelf, 10);
          next = Math.max(1, (isNaN(cur) ? 1 : cur) + delta);
        }
        state.batchAnchor.shelf = String(next).padStart(2, '0');
      }
      updateBatchAnchorUI();
      saveBatchQueueToStorage();
    }

    function handleDirectBatchCoordInput(coord, val) {
      const cleanDigits = String(val || '').replace(/[^0-9]/g, '');
      if (coord === 'cab') {
        if (!cleanDigits) {
          state.batchAnchor.cabinet = '';
        } else {
          const num = Math.max(1, parseInt(cleanDigits, 10));
          state.batchAnchor.cabinet = String(num).padStart(2, '0');
        }
      } else if (coord === 'shelf') {
        if (!cleanDigits) {
          state.batchAnchor.shelf = '';
        } else {
          const num = Math.max(1, parseInt(cleanDigits, 10));
          state.batchAnchor.shelf = String(num).padStart(2, '0');
        }
      }
      updateBatchAnchorUI();
      saveBatchQueueToStorage();
    }

    function handleDirectBatchCoordBlur(coord, input) {
      if (!input) return;
      handleDirectBatchCoordInput(coord, input.value);
    }

    function renderBatchStoredAsPills() {
      const container = document.getElementById('batchStoredAsPills');
      if (!container) return;
      let choices = state.storedAsChoices && state.storedAsChoices.length > 0
                      ? [...state.storedAsChoices]
                      : [...state.customPresets]; // Fallback
      ['Other', 'Custom'].forEach(opt => {
        if (!choices.includes(opt)) choices.push(opt);
      });

      container.innerHTML = choices.map(opt => {
        const isSel = (opt === state.batchAnchor.storedAs);
        const className = isSel
          ? 'batch-storage-pill px-2.5 py-1 rounded-full text-[11px] font-mono border-2 border-fern bg-emerald-50 text-fern-dark font-semibold'
          : 'batch-storage-pill px-2.5 py-1 rounded-full text-[11px] font-mono border border-bordercol bg-white text-muted';
        const escapedOpt = opt.replace(/'/g, "\\'");
        return `
          <button type="button" onclick="selectBatchStoragePill(this, '${escapedOpt}')" class="${className}">
            ${opt}
          </button>
        `;
      }).join('');

      const customContainer = document.getElementById('batchStoredAsCustomContainer');
      if (customContainer) {
          if (state.batchAnchor.storedAs === 'Custom') {
              customContainer.classList.remove('hidden');
          } else {
              customContainer.classList.add('hidden');
          }
      }
    }

    function selectBatchStoragePill(btn, opt) {
      if (state.batchAnchor.storedAs === opt) {
        // Deselect
        state.batchAnchor.storedAs = '';
        document.getElementById('batchStoredAsLabel').textContent = 'Not Selected';
      } else {
        // Select
        state.batchAnchor.storedAs = opt;
        document.getElementById('batchStoredAsLabel').textContent = opt;
      }
      renderBatchStoredAsPills();
    }

    function saveBatchQueueToStorage() {
      try {
        sessionStorage.setItem('arbor_batch_queue', JSON.stringify(state.batchQueue || []));
        sessionStorage.setItem('arbor_batch_anchor', JSON.stringify(state.batchAnchor || {}));
      } catch(e) {}
    }

    function loadBatchQueueFromStorage() {
      try {
        const q = sessionStorage.getItem('arbor_batch_queue');
        if (q) {
          const parsed = JSON.parse(q);
          if (Array.isArray(parsed)) state.batchQueue = parsed;
        }
        const a = sessionStorage.getItem('arbor_batch_anchor');
        if (a) {
          const parsedA = JSON.parse(a);
          if (parsedA && typeof parsedA === 'object') {
            state.batchAnchor = Object.assign(state.batchAnchor, parsedA);
          }
        }
      } catch(e) {}
    }

    function advanceToNextShelf() {
      const hasShelf = (state.batchAnchor.shelf !== undefined && state.batchAnchor.shelf !== null && String(state.batchAnchor.shelf).trim() !== '' && String(state.batchAnchor.shelf).trim() !== '—');
      const cur = hasShelf ? (parseInt(state.batchAnchor.shelf, 10) || 1) : 0;
      state.batchAnchor.shelf = String(cur + 1).padStart(2, '0');
      updateBatchAnchorUI();
      saveBatchQueueToStorage();
      showToast(`⚡ Advanced to Shelf ${String(state.batchAnchor.shelf).padStart(2, '0')} (${state.batchQueue.length} items staged)`);
      document.getElementById('batchIdInput')?.focus();
    }

    async function addBatchItemFromInput() {
      const input = document.getElementById('batchIdInput');
      if (!input || !input.value.trim()) return;
      const rawOid = input.value.trim();
      input.value = '';

      // Check if already in queue
      if (state.batchQueue.some(i => String(i.oid) === String(rawOid))) {
        showToast(`Item #${rawOid} already in queue`);
        return;
      }

      // Gate 1: Custom Storage Validation
      let currentStoredAs = state.batchAnchor.storedAs || '';
      if (currentStoredAs === 'Custom') {
        const customInp = document.getElementById('batchStoredAsCustomInput');
        const customText = customInp ? customInp.value.trim() : '';
        if (!customText) {
          showToast('Please specify a custom storage value or mark as other');
          customInp?.focus();
          return;
        }
        currentStoredAs = customText;
      }

      // Snapshot target location at time of addition
      const hasFloor = (state.batchAnchor.floor !== undefined && state.batchAnchor.floor !== null && String(state.batchAnchor.floor).trim() !== '' && String(state.batchAnchor.floor).trim() !== '—');
      const hasCab = (state.batchAnchor.cabinet !== undefined && state.batchAnchor.cabinet !== null && String(state.batchAnchor.cabinet).trim() !== '' && String(state.batchAnchor.cabinet).trim() !== '—');
      const hasShelf = (state.batchAnchor.shelf !== undefined && state.batchAnchor.shelf !== null && String(state.batchAnchor.shelf).trim() !== '' && String(state.batchAnchor.shelf).trim() !== '—');

      const targetLocation = {
        Building: state.batchAnchor.building || '',
        Floor: hasFloor ? String(state.batchAnchor.floor).trim() : '',
        Cabinet: hasCab ? String(state.batchAnchor.cabinet).trim().padStart(2, '0') : '',
        Shelf: hasShelf ? String(state.batchAnchor.shelf).trim().padStart(2, '0') : '',
        'Stored as': currentStoredAs
      };

      // Fetch quick details from server or local list
      let sciName = 'Vascular Specimen';
      let prevLoc = 'Unrecorded';
      const existing = state.objectList.find(o => String(o.id) === String(rawOid));
      if (existing) {
        sciName = existing.scientific_name || 'Vascular Specimen';
        const l = existing.location || {};
        const flStr = (l.floor !== undefined && l.floor !== null) ? l.floor : '';
        prevLoc = `${l.building || ''} Fl ${flStr} Cab ${l.cabinet || ''} Sh ${l.shelf || ''}`.trim() || 'Unrecorded';
      }

      state.batchQueue.unshift({
        oid: rawOid,
        sciName: sciName,
        prevLoc: prevLoc,
        targetLocation: targetLocation
      });

      saveBatchQueueToStorage();
      renderBatchQueue();
    }

    function removeBatchItem(idx) {
      if (idx < 0 || idx >= state.batchQueue.length) return;
      const removed = state.batchQueue[idx];
      state.batchQueue.splice(idx, 1);
      saveBatchQueueToStorage();
      renderBatchQueue();
      showToast(`Removed #${removed.oid}`, {
        actionText: 'Undo',
        onAction: () => {
          const insertIdx = Math.min(idx, state.batchQueue.length);
          state.batchQueue.splice(insertIdx, 0, removed);
          saveBatchQueueToStorage();
          renderBatchQueue();
          showToast(`Restored #${removed.oid}`);
        }
      });
    }

    function clearBatchQueue() {
      if (!state.batchQueue || state.batchQueue.length === 0) return;
      const previousQueue = [...state.batchQueue];
      state.batchQueue = [];
      saveBatchQueueToStorage();
      renderBatchQueue();
      showToast(`Cleared ${previousQueue.length} items`, {
        actionText: 'Undo',
        onAction: () => {
          state.batchQueue = previousQueue;
          saveBatchQueueToStorage();
          renderBatchQueue();
          showToast(`Restored ${previousQueue.length} items`);
        }
      });
    }

    function renderBatchQueue() {
      const container = document.getElementById('batchStreamList');
      const countEl = document.getElementById('batchQueueCount');
      const summaryEl = document.getElementById('batchCommitSummary');

      const count = state.batchQueue.length;
      if (countEl) countEl.textContent = `(${count} items)`;
      if (summaryEl) summaryEl.textContent = `${count} Accessions Queued`;

      if (count === 0) {
        if (container) container.innerHTML = `
          <div class="p-6 text-center text-stone-400 font-mono text-xs" id="batchEmptyPlaceholder">
            No items queued yet.<br>Type an Object ID above to begin.
          </div>
        `;
        return;
      }

      container.innerHTML = state.batchQueue.map((item, idx) => {
        const t = item.targetLocation || {};
        const cabStr = String(t.Cabinet || '1').padStart(2, '0');
        const shStr = String(t.Shelf || '1').padStart(2, '0');
        const bldgStr = t.Building || 'Økern';
        const flStr = t.Floor !== undefined ? t.Floor : '-1';
        const targetLocStr = `${bldgStr} · Fl ${flStr} · Cab ${cabStr} · Sh ${shStr}`;
        const storedBadge = t['Stored as']
          ? `<span class="px-1.5 py-0.5 rounded bg-emerald-50 border border-fern/30 text-[9px] font-mono font-medium text-fern-dark truncate max-w-[120px]" title="${t['Stored as']}">${t['Stored as']}</span>`
          : '';

        return `
          <article class="relative bg-white rounded border border-bordercol p-3 shadow-2xs flex flex-col gap-1.5">
            <div class="flex items-start justify-between">
              <div class="flex flex-col min-w-0">
                <div class="flex items-center gap-1.5">
                  <span class="font-mono text-xs font-bold text-fern-dark">#${item.oid}</span>
                  <span class="text-[9px] font-mono px-1 py-0.2 bg-emerald-50 text-fern rounded border border-fern/30">QUEUED</span>
                </div>
                <div class="font-serif italic text-xs text-ink truncate">${item.sciName}</div>
              </div>
              <button type="button" onclick="removeBatchItem(${idx})" class="text-stone-400 hover:text-brick p-1 text-sm font-bold">✕</button>
            </div>
            <div class="flex items-center justify-between text-[10px] font-mono pt-1 border-t border-stone-100 gap-2">
              <div class="flex items-center gap-1 text-muted truncate min-w-0">
                <span class="truncate max-w-[110px]">${item.prevLoc}</span>
                <span class="text-fern font-bold">→</span>
                <span class="font-semibold text-fern-dark truncate">${targetLocStr}</span>
              </div>
              ${storedBadge}
            </div>
          </article>
        `;
      }).join('');
    }

    async function commitBatchLocationUpdate() {
      if (state.batchQueue.length === 0) {
        showToast('No items in batch to commit');
        return;
      }

      // Gate 2: Validate all staged items
      for (const item of state.batchQueue) {
        if (item.targetLocation && item.targetLocation['Stored as'] === 'Custom') {
          showToast('Please specify a custom storage value or mark as other');
          return;
        }
      }

      const payload = {
        items: state.batchQueue.map(i => ({
          oid: i.oid,
          location: i.targetLocation
        })),
        timestamp: new Date().toISOString()
      };

      try {
        const res = await apiFetch('/api/batch_location_update', {
          method: 'POST',
          body: payload
        });

        if (res && res.success) {
          showToast(`✓ Batch committed! Relocated ${res.updated_count} specimens`);
          state.batchQueue = [];
          saveBatchQueueToStorage();
          renderBatchQueue();
          fetchObjects(false);
        } else {
          showToast('Batch commit error');
        }
      } catch(err) {
        console.warn('Batch location network error, queuing offline:', err);
        state.batchQueue.forEach(i => {
          queueMutation({
            id: i.oid,
            observation: i.targetLocation,
            timestamp: payload.timestamp
          });
        });
        showToast(`💾 Queued ${state.batchQueue.length} batch locations for offline sync`);
        state.batchQueue = [];
        saveBatchQueueToStorage();
        renderBatchQueue();
      }
    }

    // -------------------------------------------------------------
    // AUTOSAVE & UNDO
    // -------------------------------------------------------------
    function markDirty(field) {
      dirtyFields.add(field);
    }

    function triggerAutoSave() {
      clearTimeout(autoSaveTimer);
      autoSaveTimer = setTimeout(saveRecord, 800);
    }

    function forceSaveImmediate() {
      if (dirtyFields.size > 0) {
        clearTimeout(autoSaveTimer);
        saveRecord();
      }
    }

    async function saveRecord() {
      if (!state.currentRecord || dirtyFields.size === 0 || isSaving) return;
      isSaving = true;

      const obsPayload = {};
      const regPayload = {};
      const fullObs = state.currentRecord.observation || {};
      const fullReg = state.currentRecord.registration || {};

      dirtyFields.forEach(f => {
        if (f in fullObs) obsPayload[f] = fullObs[f];
        if (f in fullReg) regPayload[f] = fullReg[f];
      });

      const payload = {
        id: state.currentRecord.id,
        observation: obsPayload,
        registration: regPayload,
        reviewed: state.isReviewed,
        timestamp: new Date().toISOString()
      };

      try {
        const res = await apiFetch('/api/update', {
          method: 'POST',
          body: payload
        });
        if (res && res.success) {
          dirtyFields.clear();
          triggerHaptic('save_success');
          showToast('✓ Saved & synchronized');
        } else if (res && res.error) {
          showToast(`⚠️ Sync failed: ${res.error}`);
        } else {
          queueMutation(payload);
          dirtyFields.clear();
          showToast('💾 Saved offline (queued for sync)');
        }
      } catch(err) {
        console.warn('Network save error, queuing offline:', err);
        queueMutation(payload);
        dirtyFields.clear();
        showToast('💾 Saved offline (queued for sync)');
      } finally {
        isSaving = false;
      }
    }

    async function undoLastEdit() {
      try {
        const res = await apiFetch('/api/undo', {
          method: 'POST',
          body: { oid: state.currentOid }
        });
        if (res && res.success) {
          showToast('↩ Undid last edit');
          if (state.currentOid) fetchObjectDetail(state.currentOid);
          fetchObjects(false);
        }
      } catch(err) {
        showToast('Nothing to undo');
      }
    }

    // -------------------------------------------------------------
    // SETTINGS, WALK MODE, MODAL HELPERS
    // -------------------------------------------------------------
    function openModal(id) {
      document.getElementById(id)?.classList.remove('hidden');
    }

    function closeModal(id) {
      document.getElementById(id)?.classList.add('hidden');
    }

    function openSettingsModal() {
      document.getElementById('settingShowFilterPills').checked = state.showFilterPills;
      updateHapticsUI();
      openModal('settingsModal');
    }

    function closeSettingsModal() {
      closeModal('settingsModal');
    }

    async function saveSettings() {
      const pattern = document.getElementById('settingImageUrlPattern').value.trim();
      if (pattern) {
        await apiFetch('/api/settings', {
          method: 'POST',
          body: { image_url_pattern_override: pattern }
        });
      }
      closeSettingsModal();
      showToast('✓ Settings saved');
    }

    function updateWakeLockUI(active) {
      ['listWakeLockIcon', 'batchWakeLockIcon'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.textContent = active ? '☀️' : '🌙';
      });
      ['btnListWakeLock', 'btnBatchWakeLock'].forEach(id => {
        const btn = document.getElementById(id);
        if (btn) {
          if (active) {
            btn.className = 'w-8 h-8 rounded-md bg-amber-100 border border-amber-300 text-amber-900 shadow-xs ring-1 ring-amber-300 font-bold flex items-center justify-center tap-active transition-colors';
          } else {
            btn.className = 'w-8 h-8 rounded-md bg-stone-100 border border-stone-200 text-stone-600 hover:text-ink flex items-center justify-center tap-active transition-colors';
          }
        }
      });
    }

    async function acquireWakeLock(silent = false) {
      if (!('wakeLock' in navigator)) {
        if (!silent) showToast('Wake Lock not supported on this browser');
        return false;
      }
      try {
        if (wakeLockSentinel) {
          try { await wakeLockSentinel.release(); } catch(e) {}
          wakeLockSentinel = null;
        }
        wakeLockSentinel = await navigator.wakeLock.request('screen');
        updateWakeLockUI(true);
        wakeLockSentinel.addEventListener('release', () => {
          wakeLockSentinel = null;
          if (!state.isWalkModeWanted) {
            updateWakeLockUI(false);
          }
        });
        if (!silent) showToast('☀️ Walk Mode active (screen awake)');
        return true;
      } catch(err) {
        if (!silent) showToast('Wake Lock unavailable on this device');
        return false;
      }
    }

    async function releaseWakeLock(silent = false) {
      state.isWalkModeWanted = false;
      try { localStorage.setItem('arbor_walk_mode', 'false'); } catch(e) {}
      if (wakeLockSentinel) {
        try { await wakeLockSentinel.release(); } catch(e) {}
        wakeLockSentinel = null;
      }
      updateWakeLockUI(false);
      if (!silent) showToast('🌙 Walk Mode disabled');
    }

    async function toggleWakeLock() {
      if (state.isWalkModeWanted || wakeLockSentinel) {
        await releaseWakeLock();
      } else {
        state.isWalkModeWanted = true;
        try { localStorage.setItem('arbor_walk_mode', 'true'); } catch(e) {}
        await acquireWakeLock();
      }
    }

    function openFilterModal() {
      const locContainer = document.getElementById('filterModalLocations');
      if (locContainer && locContainer.children.length === 0) {
        const locFields = (activeSchema && activeSchema.ui_sections && activeSchema.ui_sections.location) || [
          { name: 'Cabinet' }, { name: 'Shelf' }, { name: 'Room' }, { name: 'Box' }
        ];
        locContainer.innerHTML = locFields.map(f => `
          <div class="flex items-center justify-between gap-2 text-xs">
            <label class="font-mono text-muted text-[11px] w-24 shrink-0">${f.name}:</label>
            <input type="text" id="filterModal_loc_${f.name}" placeholder="Any ${f.name}..." class="flex-1 bg-stone-50 border border-bordercol rounded px-2 py-1 text-xs font-mono text-ink outline-none focus:border-fern" />
          </div>
        `).join('');
      }
      openModal('filterModal');
    }

    function closeFilterModal() {
      closeModal('filterModal');
    }

    function clearAdvancedFilters() {
      state.activeAdvancedFilters = { locations: {}, problems: {} };
      state.selectedCabinet = '';
      state.selectedShelf = '';
      const cabSelect = document.getElementById('quickFilterCabinet');
      const shelfSelect = document.getElementById('quickFilterShelf');
      if (cabSelect) cabSelect.value = '';
      if (shelfSelect) shelfSelect.value = '';
      closeFilterModal();
      fetchObjects();
    }

    function applyAdvancedFilters() {
      const locFields = (activeSchema && activeSchema.ui_sections && activeSchema.ui_sections.location) || [
        { name: 'Cabinet' }, { name: 'Shelf' }, { name: 'Room' }, { name: 'Box' }
      ];
      locFields.forEach(f => {
        const inp = document.getElementById(`filterModal_loc_${f.name}`);
        if (inp && inp.value.trim()) {
          if (f.name.toLowerCase() === 'cabinet') state.selectedCabinet = inp.value.trim();
          if (f.name.toLowerCase() === 'shelf') state.selectedShelf = inp.value.trim();
        }
      });
      closeFilterModal();
      fetchObjects();
    }

    function openAddDiscrepancyModal(defaultField = '') {
      const select = document.getElementById('discrepancyFieldSelect');
      if (select) {
        const options = [
          { val: 'Physical_Damage_Problem', label: 'Physical Specimen Damaged' },
          { val: 'Location_Problem', label: 'Physical Specimen Misplaced' },
          { val: 'Taxon_Problem', label: 'Taxon / Identification Issue' },
          { val: 'General_Problem', label: 'General Specimen Issue' }
        ];
        if (activeSchema && activeSchema.ui_sections && activeSchema.ui_sections.problems) {
          activeSchema.ui_sections.problems.forEach(p => {
            if (p.name && !options.some(o => o.val === p.name)) {
              options.push({ val: p.name, label: p.name.replace(/_/g, ' ') });
            }
          });
        }
        select.innerHTML = options.map(o => `<option value="${o.val}" ${o.val === defaultField ? 'selected' : ''}>${o.label}</option>`).join('');
      }
      const noteInput = document.getElementById('discrepancyReasonInput');
      if (noteInput) noteInput.value = '';
      openModal('addDiscrepancyModal');
    }

    async function submitDiscrepancy(e) {
      e.preventDefault();
      const field = document.getElementById('discrepancyFieldSelect').value;
      const note = document.getElementById('discrepancyReasonInput').value.trim();
      if (!field || !note || !state.currentRecord) return;

      state.currentRecord.observation = state.currentRecord.observation || {};
      const probField = field.endsWith('_Problem') ? field : `${field}_Problem`;
      const noteField = field.endsWith('_Problem') ? `${field.slice(0, -8)}_Note` : `${field}_Note`;
      state.currentRecord.observation[probField] = true;
      state.currentRecord.observation[noteField] = note;
      state.currentRecord.observation['Notes'] = note;
      markDirty(probField);
      markDirty(noteField);
      markDirty('Notes');

      closeModal('addDiscrepancyModal');
      triggerAutoSave();
      triggerHaptic('discrepancy');
      renderDetailView(false);
      showToast(`⚑ Issue flagged: ${note}`);
    }

    function handleLocationFilterChange() {
      const cabSelect = document.getElementById('quickFilterCabinet');
      const shelfSelect = document.getElementById('quickFilterShelf');
      state.selectedCabinet = cabSelect ? cabSelect.value : '';
      state.selectedShelf = shelfSelect ? shelfSelect.value : '';
      const clearBtn = document.getElementById('btnClearLocFilter');
      if (clearBtn) {
        if (state.selectedCabinet || state.selectedShelf) clearBtn.classList.remove('hidden');
        else clearBtn.classList.add('hidden');
      }
      fetchObjects();
    }

    function clearLocationFilter() {
      state.selectedCabinet = '';
      state.selectedShelf = '';
      const cabSelect = document.getElementById('quickFilterCabinet');
      const shelfSelect = document.getElementById('quickFilterShelf');
      if (cabSelect) cabSelect.value = '';
      if (shelfSelect) shelfSelect.value = '';
      const clearBtn = document.getElementById('btnClearLocFilter');
      if (clearBtn) clearBtn.classList.add('hidden');
      fetchObjects();
    }

    // -------------------------------------------------------------
    // ACCIDENTAL UNLOAD & LIFECYCLE GUARDS
    // -------------------------------------------------------------
    window.addEventListener('beforeunload', (e) => {
      const hasQueued = (typeof queuedMutations !== 'undefined' && queuedMutations.length > 0);
      if (dirtyFields.size > 0 || hasQueued) {
        e.preventDefault();
        e.returnValue = '';
        return '';
      }
    });

    window.addEventListener('pagehide', () => {
      if (dirtyFields.size > 0) {
        forceSaveImmediate();
      }
    });

    document.addEventListener('visibilitychange', () => {
      if (document.visibilityState === 'hidden' && dirtyFields.size > 0) {
        forceSaveImmediate();
      }
    });

    // -------------------------------------------------------------
    // TACTILE HAPTIC ENGINE (ADJUSTABLE & TOGGLEABLE)
    // -------------------------------------------------------------
    const HAPTIC_PROFILES = {
      light: {
        stepper: 8,
        reviewed_on: [15, 25, 15],
        reviewed_off: 12,
        copy_prev: [10, 20, 10],
        discrepancy: [25, 25, 25],
        scan: 15,
        save_success: 10
      },
      medium: {
        stepper: 15,
        reviewed_on: [25, 40, 25],
        reviewed_off: 20,
        copy_prev: [15, 30, 15],
        discrepancy: [45, 40, 45],
        scan: 30,
        save_success: [12, 24]
      },
      strong: {
        stepper: 28,
        reviewed_on: [40, 60, 40],
        reviewed_off: 35,
        copy_prev: [25, 40, 25],
        discrepancy: [70, 50, 70],
        scan: 50,
        save_success: [20, 40]
      }
    };

    function triggerHaptic(actionType) {
      if (!state.hapticsEnabled) return;
      if (typeof navigator === 'undefined' || !('vibrate' in navigator)) return;
      const intensity = state.hapticsIntensity || 'medium';
      const pattern = HAPTIC_PROFILES[intensity]?.[actionType] || HAPTIC_PROFILES['medium']?.[actionType];
      if (pattern) {
        try {
          navigator.vibrate(pattern);
        } catch (e) {}
      }
    }

    function toggleHapticsSetting(enabled) {
      state.hapticsEnabled = !!enabled;
      try { localStorage.setItem('arbor_haptics_enabled', state.hapticsEnabled ? 'true' : 'false'); } catch(e) {}
      updateHapticsUI();
    }

    function setHapticsIntensity(intensity) {
      if (!['light', 'medium', 'strong'].includes(intensity)) return;
      state.hapticsIntensity = intensity;
      try { localStorage.setItem('arbor_haptics_intensity', intensity); } catch(e) {}
      updateHapticsUI();
      triggerHaptic('stepper');
    }

    function testHapticFeedback() {
      triggerHaptic('reviewed_on');
    }

    function updateHapticsUI() {
      const toggle = document.getElementById('settingEnableHaptics');
      if (toggle) toggle.checked = state.hapticsEnabled;

      const container = document.getElementById('hapticsIntensityContainer');
      if (container) {
        if (state.hapticsEnabled) {
          container.classList.remove('opacity-40', 'pointer-events-none');
        } else {
          container.classList.add('opacity-40', 'pointer-events-none');
        }
      }

      const cur = state.hapticsIntensity || 'medium';
      ['light', 'medium', 'strong'].forEach(lvl => {
        const btn = document.getElementById('btnHaptic' + lvl.charAt(0).toUpperCase() + lvl.slice(1));
        if (btn) {
          if (lvl === cur) {
            btn.className = 'px-2 py-1 bg-fern text-white font-bold transition-all';
          } else {
            btn.className = 'px-2 py-1 bg-surface text-ink hover:bg-stone-100 transition-all';
          }
        }
      });

      const note = document.getElementById('hapticsUnsupportedNote');
      if (note) {
        if (typeof navigator !== 'undefined' && !('vibrate' in navigator)) {
          note.classList.remove('hidden');
        } else {
          note.classList.add('hidden');
        }
      }
    }

    // 3-Step First-Run Hallway Walkthrough
    const WALKTHROUGH_SLIDES = [
      {
        badge: 'STEP 1 OF 3 · FAST LOOKUP',
        title: 'Search by Accession Number',
        body: 'Pull a physical specimen box and type its catalog number into the search bar. Leading zeros and prefixes are handled automatically.',
        callout: 'Tip: Typing "001" or "O-V-1" both find Specimen #1. Use [123 / Aa] to switch between number pad and plant names.'
      },
      {
        badge: 'STEP 2 OF 3 · ARMED TARGET SHELF',
        title: 'Set Your Cabinet Once, Stamp in 1 Tap',
        body: 'Set your current Cabinet & Shelf once. Opening a specimen never overwrites its coordinates — tap the green Stamp Target banner to stamp 30+ items on the same shelf in 1 tap.',
        callout: '⚡ Armed Target: Cab 21 · Sh 01  →  [ Stamp Target ]'
      },
      {
        badge: 'STEP 3 OF 3 · MARK REVIEWED',
        title: 'Flag Issues & Still Mark Reviewed',
        body: 'Found a crushed box or unreadable label? Check the problem flag and still tap ✓ Mark Reviewed. The badge turns amber (REV + ISSUES) so your office desktop queues it for follow-up.',
        callout: '🟠 REV + 1 ISSUE = Physically verified + safely queued for office triage.'
      }
    ];
    let _wtIndex = 0;

    function renderWalkthroughSlide() {
      const s = WALKTHROUGH_SLIDES[_wtIndex] || WALKTHROUGH_SLIDES[0];
      const badge = document.getElementById('walkthroughStepBadge');
      const title = document.getElementById('walkthroughTitle');
      const body = document.getElementById('walkthroughBody');
      const callout = document.getElementById('walkthroughCallout');
      const backBtn = document.getElementById('wtBackBtn');
      const nextBtn = document.getElementById('wtNextBtn');
      if (badge) badge.textContent = s.badge;
      if (title) title.textContent = s.title;
      if (body) body.textContent = s.body;
      if (callout) callout.textContent = s.callout;
      if (backBtn) backBtn.classList.toggle('hidden', _wtIndex === 0);
      if (nextBtn) {
        nextBtn.textContent = (_wtIndex === WALKTHROUGH_SLIDES.length - 1) ? 'Set My Cabinet & Start →' : 'Next →';
      }
      for (let i = 0; i < WALKTHROUGH_SLIDES.length; i++) {
        const dot = document.getElementById('wtDot' + i);
        if (dot) {
          dot.className = i === _wtIndex ? 'w-2.5 h-2.5 rounded-full bg-fern' : 'w-2 h-2 rounded-full bg-stone-300';
        }
      }
    }

    function openWalkthroughModal(startIdx = 0) {
      _wtIndex = startIdx;
      renderWalkthroughSlide();
      const modal = document.getElementById('walkthroughModal');
      if (modal) modal.classList.remove('hidden');
    }

    function closeWalkthroughModal(markSeen = true) {
      const modal = document.getElementById('walkthroughModal');
      if (modal) modal.classList.add('hidden');
      if (markSeen) {
        try { localStorage.setItem('arbor_v2_walkthrough_seen', 'true'); } catch(e) {}
      }
    }

    function nextWalkthroughSlide() {
      if (_wtIndex < WALKTHROUGH_SLIDES.length - 1) {
        _wtIndex += 1;
        renderWalkthroughSlide();
      } else {
        closeWalkthroughModal(true);
      }
    }

    function prevWalkthroughSlide() {
      if (_wtIndex > 0) {
        _wtIndex -= 1;
        renderWalkthroughSlide();
      }
    }

    function maybeShowFirstRunWalkthrough() {
      try {
        if (localStorage.getItem('arbor_v2_walkthrough_seen') !== 'true') {
          openWalkthroughModal(0);
        }
      } catch(e) {}
    }

    // Register Service Worker for offline vault resilience
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('/service-worker.js').catch(err => console.warn('ServiceWorker registration error:', err));
    }

    // Start App
    if (document.readyState === 'loading') {
      window.addEventListener('DOMContentLoaded', () => { init(); maybeShowFirstRunWalkthrough(); });
    } else {
      init();
      maybeShowFirstRunWalkthrough();
    }
  </script>
</body>
</html>

"""

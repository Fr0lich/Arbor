"""
backend/mobile_template_v1.py

Legacy V1 Mobile Companion frontend HTML/CSS/JS string constant.
Re-exported as `INDEX_TEMPLATE` by `backend/mobile_server.py`.
Zero-build compliant: pure Python string constant, no external .html files.
"""

# WARNING TO AI AGENTS: DO NOT CREATE OR MODIFY AN EXTERNAL `mobile_frontend.html` FILE.
# The user explicitly prefers maintaining a Vanilla HTML/JS frontend directly within this
# INDEX_TEMPLATE string to ensure the Python server remains self-contained without
# external build dependencies or file resolution issues. All frontend modifications for
# the mobile application MUST be done inside this string below.
INDEX_TEMPLATE = """
<!DOCTYPE html>
<html lang="en" class="arbor-offline-css">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>Arbor Mobile Companion</title>
  <style id="arbor-offline-fallback">
    .hidden { display: none !important; }
    body { margin: 0; font-family: system-ui, -apple-system, sans-serif; background: #f3f3f3; color: #191e1a; }
    button { cursor: pointer; }
    input, select, textarea { box-sizing: border-box; }
    html.arbor-offline-css *, html.arbor-offline-css *::before, html.arbor-offline-css *::after { box-sizing: border-box; }
    html.arbor-offline-css .fixed { position: fixed; }
    html.arbor-offline-css .sticky { position: sticky; }
    html.arbor-offline-css .relative { position: relative; }
    html.arbor-offline-css .absolute { position: absolute; }
    html.arbor-offline-css .inset-0 { top: 0; right: 0; bottom: 0; left: 0; }
    html.arbor-offline-css .top-0 { top: 0; }
    html.arbor-offline-css .bottom-0 { bottom: 0; }
    html.arbor-offline-css .z-20 { z-index: 20; }
    html.arbor-offline-css .z-30 { z-index: 30; }
    html.arbor-offline-css .z-40 { z-index: 40; }
    html.arbor-offline-css .z-50 { z-index: 50; }
    html.arbor-offline-css .flex { display: flex; }
    html.arbor-offline-css .flex-col { flex-direction: column; }
    html.arbor-offline-css .flex-1 { flex: 1 1 0%; }
    html.arbor-offline-css .items-center { align-items: center; }
    html.arbor-offline-css .justify-between { justify-content: space-between; }
    html.arbor-offline-css .justify-center { justify-content: center; }
    html.arbor-offline-css .grid { display: grid; }
    html.arbor-offline-css .grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    html.arbor-offline-css .gap-1 { gap: 0.25rem; }
    html.arbor-offline-css .gap-2 { gap: 0.5rem; }
    html.arbor-offline-css .gap-3 { gap: 0.75rem; }
    html.arbor-offline-css .w-full { width: 100%; }
    html.arbor-offline-css .min-w-0 { min-width: 0; }
    html.arbor-offline-css .truncate { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    html.arbor-offline-css .p-2 { padding: 0.5rem; }
    html.arbor-offline-css .p-3 { padding: 0.75rem; }
    html.arbor-offline-css .p-4 { padding: 1rem; }
    html.arbor-offline-css .px-2 { padding-left: 0.5rem; padding-right: 0.5rem; }
    html.arbor-offline-css .px-3 { padding-left: 0.75rem; padding-right: 0.75rem; }
    html.arbor-offline-css .px-4 { padding-left: 1rem; padding-right: 1rem; }
    html.arbor-offline-css .py-1 { padding-top: 0.25rem; padding-bottom: 0.25rem; }
    html.arbor-offline-css .py-2 { padding-top: 0.5rem; padding-bottom: 0.5rem; }
    html.arbor-offline-css .py-3 { padding-top: 0.75rem; padding-bottom: 0.75rem; }
    html.arbor-offline-css .rounded, html.arbor-offline-css .rounded-md { border-radius: 6px; }
    html.arbor-offline-css .rounded-lg { border-radius: 8px; }
    html.arbor-offline-css .rounded-xl { border-radius: 12px; }
    html.arbor-offline-css .rounded-full { border-radius: 9999px; }
    html.arbor-offline-css .border { border: 1px solid #d4d8d5; }
    html.arbor-offline-css .border-b { border-bottom: 1px solid #d4d8d5; }
    html.arbor-offline-css .border-t { border-top: 1px solid #d4d8d5; }
    html.arbor-offline-css .bg-surface, html.arbor-offline-css .bg-white { background-color: #ffffff; }
    html.arbor-offline-css .bg-canvas { background-color: #f3f3f3; }
    html.arbor-offline-css .bg-fern { background-color: #3a7d44; color: #ffffff; }
    html.arbor-offline-css .text-white { color: #ffffff; }
    html.arbor-offline-css .text-ink { color: #191e1a; }
    html.arbor-offline-css .text-xs { font-size: 0.75rem; line-height: 1rem; }
    html.arbor-offline-css .text-sm { font-size: 0.875rem; line-height: 1.25rem; }
    html.arbor-offline-css .font-bold { font-weight: 700; }
    html.arbor-offline-css .font-semibold { font-weight: 600; }
    html.arbor-offline-css .font-mono { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }
    html.arbor-offline-css .font-serif { font-family: Georgia, Cambria, serif; }
    html.arbor-offline-css button { border: 1px solid #d4d8d5; border-radius: 6px; padding: 6px 10px; background: #ffffff; color: #191e1a; }
    html.arbor-offline-css button.bg-fern, html.arbor-offline-css #btnMarkReviewed { background: #3a7d44; color: #ffffff; border-color: #2c6034; font-weight: 700; }
    html.arbor-offline-css input, html.arbor-offline-css select, html.arbor-offline-css textarea { border: 1px solid #c4c9c5; border-radius: 6px; padding: 6px 8px; background: #ffffff; color: #191e1a; }
    html.arbor-offline-css [id$="Modal"] { background: rgba(20, 24, 21, 0.55); display: flex; align-items: center; justify-content: center; padding: 16px; }
    html.arbor-offline-css [id$="Modal"] > div { background: #ffffff; border-radius: 12px; max-width: 460px; width: 100%; padding: 16px; box-shadow: 0 12px 32px rgba(0,0,0,0.25); }
    html.arbor-offline-css #toast { position: fixed; bottom: 72px; left: 50%; transform: translateX(-50%); background: #191e1a; color: #ffffff; padding: 10px 16px; border-radius: 9999px; z-index: 60; font-size: 0.85rem; }
  </style>
  <script>
    window._arborInitTailwindV1 = function() {
      if (typeof tailwind === 'undefined') return;
      tailwind.config = {
        theme: {
          extend: {
            colors: {
              fern: {
                DEFAULT: '#3a7d44',
                dark: '#2c6034',
                light: '#eff7f1',
                border: '#a4cca9'
              },
              ember: {
                DEFAULT: '#d95c14',
                dark: '#b84a0c',
                light: '#fff3ec',
                border: '#f8c2a3'
              },
              canvas: '#f3f3f3',
              surface: '#ffffff',
              tonal1: '#f8f9fa',
              tonal2: '#eceeec',
              tonal3: '#dfe3e0',
              bordercol: '#d4d8d5',
              borderdark: '#b3b9b4',
              ink: {
                DEFAULT: '#191e1a',
                muted: '#535d56',
                faint: '#848f87'
              }
            },
            fontFamily: {
              sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
              serif: ['Lora', 'Georgia', 'serif'],
              mono: ['JetBrains Mono', 'Menlo', 'Monaco', 'Consolas', 'monospace'],
            }
          }
        }
      };
      document.documentElement.classList.remove('arbor-offline-css');
    };
  </script>
  <script defer src="https://cdn.tailwindcss.com" onload="window._arborInitTailwindV1()" onerror="document.documentElement.classList.add('arbor-offline-css')"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Lora:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600&display=swap" rel="stylesheet" media="print" onload="this.media='all'">
  <style>
    .touch-target-min { min-height: 44px; min-width: 44px; }
    .touch-press:active { transform: scale(0.985); filter: brightness(0.97); }
    .search-active:focus-within {
      border-color: #d95c14 !important;
      box-shadow: 0 0 0 2px rgba(217, 92, 20, 0.2) !important;
    }
    .no-scrollbar::-webkit-scrollbar { display: none; }
    .no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
    ::-webkit-scrollbar { width: 4px; height: 4px; }
    ::-webkit-scrollbar-track { background: #f3f3f3; }
    ::-webkit-scrollbar-thumb { background: #c8ccc9; border-radius: 2px; }
    .acc-open .acc-icon { transform: rotate(180deg); }
    @keyframes spinSlow { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
    .animate-spin-slow { animation: spinSlow 8s linear infinite; }
  </style>
</head>
<body class="bg-canvas text-ink min-h-screen antialiased select-none font-sans">

  <div class="w-full h-screen flex flex-col relative overflow-hidden bg-canvas mx-auto max-w-md border-x border-bordercol shadow-xl">

    <!-- Persistent Offline / Disconnected Warning Banner -->
    <div id="offlineBanner" class="hidden bg-ember-light border-b border-ember-border px-4 py-2 flex items-center justify-between gap-2 text-xs font-sans font-medium text-ember-dark shrink-0 transition-all shadow-xs" role="alert" aria-live="assertive">
      <div class="flex items-center gap-2" id="offlineBannerContent">
        <span class="text-sm">⚠</span>
        <span>Connection to host lost. Reconnecting...</span>
      </div>
      <button
        type="button"
        id="btnOfflineRetry"
        onclick="setupEventSource()"
        class="min-h-[32px] px-2.5 py-1 bg-ember text-white rounded-[2px] font-bold text-[11px] touch-press shrink-0"
      >
        Retry
      </button>
    </div>

    <!-- Persistent App Header & Search Bar -->
    <header class="sticky top-0 z-30 bg-surface border-b border-bordercol px-4 pt-3 pb-2.5 shadow-xs shrink-0">
      <div class="flex items-center justify-between mb-2.5">
        <div class="flex items-center gap-2">
          <div class="w-7 h-7 rounded-[2px] bg-fern text-white flex items-center justify-center font-serif font-bold text-sm">
            A
          </div>
          <div>
            <h1 class="font-serif font-bold text-base text-ink leading-tight">
              Arbor Companion
            </h1>
            <div class="font-mono text-[10px] text-ink-muted truncate max-w-[170px]" id="headerDbName">
              Connecting to database...
            </div>
          </div>
        </div>

        <div class="flex items-center gap-1.5">
          <!-- Settings Modal Trigger -->
          <button
            type="button"
            onclick="openSettingsModal()"
            class="p-2 bg-surface hover:bg-tonal1 border border-bordercol rounded-[2px] text-ink transition-colors touch-target-min flex items-center justify-center shrink-0"
            title="Settings"
          >
            <span class="text-ink text-sm font-mono">⚙️</span>
          </button>

          <!-- Recent Changes Drawer Trigger -->
          <button
            type="button"
            onclick="openRecentEditsModal()"
            class="p-2 bg-surface hover:bg-tonal1 border border-bordercol rounded-[2px] text-ink transition-colors touch-target-min flex items-center justify-center shrink-0"
            title="Recent Changes"
          >
            <span class="text-ink text-sm font-mono">↩</span>
          </button>

          <!-- Screen Wake Lock / Walk Mode Toggle -->
          <button
            type="button"
            id="btnWakeLock"
            onclick="toggleWakeLock()"
            class="p-2 rounded-[2px] border transition-colors touch-target-min bg-ink text-surface border-ink hover:bg-ink-muted flex items-center justify-center"
            title="Toggle Walk Mode (Prevent Screen Sleep)"
          >
            <span id="wakeLockIcon" class="text-sm leading-none">🌙</span>
          </button>

          <!-- Desktop Connection Pill Button -->
          <button
            type="button"
            onclick="openModal('connectionModal')"
            id="connStatusBtn"
            class="flex items-center gap-1.5 px-2.5 py-1.5 bg-surface hover:bg-tonal1 border border-bordercol rounded-[2px] text-xs transition-colors touch-target-min"
            title="Desktop Connection Status"
            aria-live="polite"
          >
            <span class="relative flex h-2 w-2">
              <span id="connPingDotAnimate" class="animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 bg-ember"></span>
              <span id="connPingDot" class="relative inline-flex rounded-full h-2 w-2 bg-ember"></span>
            </span>
            <span class="font-mono text-[11px] font-medium text-ink" id="pingBadge">
              Connecting...
            </span>
          </button>
        </div>
      </div>

      <!-- Persistent Search Input Box -->
      <div class="relative flex items-center gap-2">
        <div class="relative flex-1 flex items-center bg-tonal1 border border-bordercol rounded-[2px] transition-all search-active">
          <span class="text-ink-faint ml-2.5 shrink-0 text-xs">🔍</span>
          <input
            type="text"
            id="searchBox"
            oninput="debounceSearch()"
            placeholder="Search taxonomy, accession, collector, cabinet..."
            class="w-full bg-transparent px-2.5 py-2 font-sans text-xs text-ink placeholder:text-ink-faint outline-none"
          />
          <button
            type="button"
            id="searchClearBtn"
            onclick="clearSearch()"
            class="hidden p-1 mr-1.5 text-ink-faint hover:text-ink text-xs font-bold"
          >
            ✕
          </button>
        </div>

        <!-- Advanced Filter Modal Trigger -->
        <button
          type="button"
          id="btnFilterModalTrigger"
          onclick="openFilterModal()"
          class="relative p-2 bg-surface hover:bg-tonal1 border border-bordercol rounded-[2px] text-ink transition-colors touch-target-min flex items-center justify-center shrink-0"
          title="Advanced Filter"
        >
          <span class="text-ink text-sm font-mono">⚙</span>
          <span id="filterActiveBadge" class="hidden absolute -top-1 -right-1 w-2.5 h-2.5 bg-fern rounded-full ring-2 ring-surface"></span>
        </button>
      </div>
    </header>

    <!-- Storage Location Vault Filter Bar -->
    <div id="storageLocationFilterBar" class="px-3.5 py-1.5 bg-stone-50 border-b border-bordercol flex items-center gap-2 text-xs">
      <span class="font-mono text-[11px] font-bold text-ink-muted shrink-0">📍 Vault Loc:</span>
      <div class="flex-1 flex items-center gap-1.5 min-w-0">
        <select id="quickFilterCabinet" onchange="handleV1LocationFilterChange()" class="flex-1 min-w-0 bg-surface border border-bordercol rounded-[2px] px-2 py-1 text-xs font-mono text-ink outline-none">
          <option value="">All Cabinets</option>
        </select>
        <select id="quickFilterShelf" onchange="handleV1LocationFilterChange()" class="flex-1 min-w-0 bg-surface border border-bordercol rounded-[2px] px-2 py-1 text-xs font-mono text-ink outline-none">
          <option value="">All Shelves</option>
        </select>
        <button type="button" id="btnClearLocFilterV1" onclick="clearV1LocationFilter()" class="hidden px-1.5 py-0.5 text-xs text-ink-muted hover:text-ink font-bold font-mono">✕</button>
      </div>
    </div>

    <!-- ========================================== -->
    <!-- VIEW: SPECIMEN LIST                        -->
    <!-- ========================================== -->
    <div id="listView" class="flex-1 flex flex-col h-full bg-canvas overflow-hidden">
      <!-- List View Filter & Sort Controls -->
      <div class="bg-surface border-b border-bordercol px-4 pt-1.5 pb-2 shadow-xs shrink-0">
        <!-- Filter Pill Tabs -->
        <div class="flex items-center gap-2 overflow-x-auto no-scrollbar pb-1" id="filterPills">
          <button
            type="button"
            onclick="setStatusFilter('all')"
            id="pill-all"
            class="min-h-[44px] px-3.5 py-2 rounded-[2px] font-sans text-xs font-medium whitespace-nowrap border transition-colors touch-press flex items-center justify-center bg-ink text-white border-ink"
          >
            All (0)
          </button>

          <button
            type="button"
            onclick="setStatusFilter('pending')"
            id="pill-pending"
            class="min-h-[44px] px-3.5 py-2 rounded-[2px] font-sans text-xs font-medium whitespace-nowrap border transition-colors touch-press flex items-center gap-1.5 bg-surface text-ink-muted border-bordercol hover:bg-tonal1"
          >
            <span>🕒</span>
            <span>Unreviewed (0)</span>
          </button>

          <button
            type="button"
            onclick="setStatusFilter('flagged')"
            id="pill-flagged"
            class="min-h-[44px] px-3.5 py-2 rounded-[2px] font-sans text-xs font-medium whitespace-nowrap border transition-colors touch-press flex items-center gap-1.5 bg-ember-light text-ember-dark border-ember-border hover:bg-ember-light/80"
          >
            <span>⚠</span>
            <span>Flagged (0)</span>
          </button>

          <button
            type="button"
            onclick="setStatusFilter('reviewed')"
            id="pill-reviewed"
            class="min-h-[44px] px-3.5 py-2 rounded-[2px] font-sans text-xs font-medium whitespace-nowrap border transition-colors touch-press flex items-center gap-1.5 bg-fern-light text-fern-dark border-fern-border hover:bg-fern-light/80"
          >
            <span>✓</span>
            <span>Reviewed (0)</span>
          </button>

          <button
            type="button"
            onclick="setStatusFilter('conflict')"
            id="pill-conflict"
            class="min-h-[44px] px-3.5 py-2 rounded-[2px] font-sans text-xs font-medium whitespace-nowrap border transition-colors touch-press flex items-center gap-1.5 bg-[#e0f2fe] text-[#0369a1] border-[#bae6fd] hover:bg-[#bae6fd]"
          >
            <span>🔀</span>
            <span>Conflict (0)</span>
          </button>

          <button
            type="button"
            onclick="setStatusFilter('unknown')"
            id="pill-unknown"
            class="min-h-[44px] px-3.5 py-2 rounded-[2px] font-sans text-xs font-medium whitespace-nowrap border transition-colors touch-press flex items-center gap-1.5 bg-[#fef9c3] text-[#854d0e] border-[#fde047] hover:bg-[#fef08a]"
          >
            <span>?</span>
            <span>Unknown (0)</span>
          </button>

          <div class="w-px h-6 bg-bordercol mx-0.5 shrink-0"></div>

          <button
            type="button"
            onclick="toggleNoImageFilter()"
            id="pill-no-image"
            class="min-h-[44px] px-3.5 py-2 rounded-[2px] font-sans text-xs font-medium whitespace-nowrap border transition-colors touch-press flex items-center gap-1.5 bg-surface text-ink-muted border-bordercol hover:bg-tonal1"
          >
            <span>📷</span>
            <span>No Image</span>
          </button>
        </div>

        <!-- Results Counter & Sort Dropdown -->
        <div class="flex items-center justify-between mt-2 pt-2 border-t border-tonal2 text-[11px]">
          <span class="font-mono text-ink-muted" id="listSummaryText">
            Showing <strong class="text-ink" id="matchingCount">0</strong> records
          </span>

          <div class="flex items-center gap-1 text-ink-muted">
            <span class="text-xs">⇅</span>
            <select
              id="sortBySelect"
              onchange="handleSortChange()"
              class="bg-transparent font-sans text-[11px] font-medium text-ink outline-none cursor-pointer"
            >
              <option value="id-asc" selected>Accession / ID Number</option>
              <option value="location">Sort by Physical Location</option>
              <option value="name-asc">Scientific Name (A-Z)</option>
              <option value="name-desc">Scientific Name (Z-A)</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Scrollable List -->
      <main id="specimenListContainer" class="flex-1 overflow-y-auto p-3 space-y-2.5 pb-24">
        <!-- Specimen cards injected dynamically -->
      </main>
    </div>


    <!-- ========================================== -->
    <!-- VIEW: SPECIMEN DETAIL                      -->
    <!-- ========================================== -->
    <div id="detailView" class="hidden flex-1 flex flex-col h-full bg-canvas overflow-hidden relative">
      <!-- Sticky Top Header -->
      <header class="sticky top-0 z-30 bg-surface border-b border-bordercol px-4 py-2.5 shadow-xs shrink-0 flex items-center justify-between">
        <button
          type="button"
          onclick="showListView()"
          class="flex items-center gap-1.5 text-xs font-sans font-medium text-ink hover:text-fern py-1 px-1.5 -ml-1 rounded-[2px] transition-colors touch-target-min"
        >
          <span class="font-bold text-sm">&lt;</span>
          <span>Vault List</span>
        </button>

        <div class="flex items-center gap-2">
          <!-- Undo Button (shown conditionally after edit) -->
          <button
            type="button"
            id="btnMobileUndo"
            onclick="undoLastEdit()"
            class="hidden items-center gap-1 text-[11px] font-sans font-bold bg-ember-light text-ember-dark border border-ember-border px-2 py-1 rounded-[2px] hover:bg-ember/10 transition-colors touch-target-min"
          >
            <span>↩</span>
            <span>Undo</span>
          </button>

          <span class="font-mono text-xs text-ink-muted" id="detailNavIndex">
            1 of 1
          </span>
          <div class="flex items-center border border-bordercol rounded-[2px] bg-tonal1 overflow-hidden">
            <button
              type="button"
              id="btnPrevSpecimen"
              onclick="navSpecimen(-1)"
              class="p-1.5 hover:bg-tonal2 disabled:opacity-30 text-ink transition-colors touch-target-min"
              title="Previous specimen"
            >
              <span class="font-bold text-xs">&lt;</span>
            </button>
            <div class="w-[1px] h-4 bg-bordercol"></div>
            <button
              type="button"
              id="btnNextSpecimen"
              onclick="navSpecimen(1)"
              class="p-1.5 hover:bg-tonal2 disabled:opacity-30 text-ink transition-colors touch-target-min"
              title="Next specimen"
            >
              <span class="font-bold text-xs">&gt;</span>
            </button>
          </div>
        </div>
      </header>

      <!-- Scrollable Specimen Form Content -->
      <main class="flex-1 overflow-y-auto p-3.5 space-y-3.5 pb-36">

        <!-- Presence Warning Banner (Shown when another worker is viewing this object) -->
        <div id="detailPresenceBanner" class="hidden flex items-center gap-2 p-3 bg-amber-50 border border-amber-300 rounded-[2px] text-amber-900 text-xs font-sans font-medium">
          <span class="text-sm">⚠️</span>
          <span id="detailPresenceText">Warning: Another worker is currently viewing this record.</span>
        </div>

        <!-- Top Specimen Summary Card -->
        <div class="bg-surface border border-bordercol rounded-[2px] p-4 shadow-xs">
          <div class="flex items-start justify-between gap-2 mb-2">
            <div>
              <div class="font-mono text-xs font-bold text-ink-muted tracking-wider" id="detailAccession">
                #---
              </div>
              <div class="font-mono text-[11px] text-ink-faint" id="detailTopLocation">
                Location: ---
              </div>
            </div>

            <div id="detailReviewStatusBadge">
              <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-[2px] text-[10px] font-sans font-medium bg-tonal1 text-ink-muted border border-bordercol">
                🕒 UNREVIEWED
              </span>
            </div>
          </div>

          <h2 id="detailScientificName" class="font-serif italic font-bold text-xl text-ink leading-snug mb-1">
            Loading specimen...
          </h2>

          <div class="flex items-center gap-2 text-xs font-sans text-ink-muted" id="detailTaxonSubline">
            <span id="detailAuthor" class="font-medium text-ink"></span>
            <span>•</span>
            <span id="detailFamily"></span>
          </div>
        </div>

        <!-- Active Problems Alert Banner (Dynamically shown if problems/unknowns exist) -->
        <div id="detailProblemBanner" class="hidden bg-ember-light border border-ember-border rounded-[2px] p-3 shadow-xs space-y-1.5">
          <div class="flex items-center justify-between">
            <span class="text-xs font-bold text-ember-dark flex items-center gap-1">
              <span>⚠</span>
              <span>Active Problems Detected</span>
            </span>
          </div>
          <div id="detailProblemBadges" class="flex flex-wrap items-center gap-1.5 pt-1">
            <!-- Problem chips injected here -->
          </div>
        </div>


        <!-- Archival Scans / Photo Gallery Card -->
        <div class="bg-surface border border-bordercol rounded-[2px] p-3 space-y-2.5">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-1.5 text-xs font-sans font-semibold text-ink">
              <span>📷</span>
              <span>Attached Archival Scans</span>
              <span id="photoCountBadge" class="font-mono text-[10px] text-ink-muted bg-tonal1 border border-tonal3 px-1.5 py-0.2 rounded-[2px]">
                0 available
              </span>
            </div>

            <button
              type="button"
              onclick="openFullscreenPhoto()"
              class="text-[11px] font-sans font-medium text-fern hover:text-fern-dark flex items-center gap-1 transition-colors touch-target-min py-1 px-1"
            >
              <span>↗</span>
              <span>Fullscreen</span>
            </button>
          </div>

          <!-- Photo Container -->
          <div
            id="photoMainContainer"
            onclick="loadInitialPhoto()"
            class="relative w-full h-16 bg-ink/5 rounded-[2px] border border-bordercol overflow-hidden cursor-pointer group flex items-center justify-center transition-all duration-300"
          >
            <div id="photoPlaceholder" class="p-2 text-center text-xs text-ink-muted flex flex-col items-center gap-0.5">
              <span class="text-xl">📷</span>
              <p class="font-semibold text-fern" id="photoPlaceholderText">Tap to Load Archival Scans</p>
            </div>
            <img
              id="specimenImg"
              src=""
              alt="Archival Specimen Plate"
              class="hidden w-full h-full object-contain group-hover:scale-[1.02] transition-transform duration-200"
              onload="onPhotoLoaded()"
              onerror="onPhotoError()"
            />
            <div id="photoWatermark" class="hidden absolute bottom-1.5 left-1.5 bg-white/90 backdrop-blur-xs font-mono text-[9px] text-ink-muted px-1.5 py-0.5 rounded-[1px] border border-bordercol">
              Archival Scan
            </div>
          </div>

          <!-- Thumbnail Strip -->
          <div id="photoThumbStrip" class="hidden flex items-center gap-2 overflow-x-auto pb-1 no-scrollbar">
            <!-- Thumbnails injected dynamically -->
          </div>
        </div>

        <!-- Dynamic Form Groups Container (Injected from config.py) -->
        <div id="detailAccordionsContainer" class="space-y-3.5">
          <!-- Rendered dynamically by renderDynamicForm() -->
        </div>

        <!-- Problem Discrepancies Card -->
        <div class="bg-surface border border-bordercol rounded-[2px] p-3.5 space-y-3">
          <div class="flex items-center justify-between border-b border-tonal2 pb-2">
            <div class="flex items-center gap-2">
              <span class="text-ember font-bold text-sm">⚑</span>
              <h3 class="font-sans font-bold text-xs text-ink uppercase tracking-wider">
                Flagged Problems & Issues
              </h3>
            </div>
            <button
              type="button"
              onclick="openAddDiscrepancyModal()"
              class="text-xs font-medium text-ember hover:text-ember-dark flex items-center gap-1 border border-ember-border bg-ember-light px-2 py-0.5 rounded-[2px] transition-colors touch-target-min"
            >
              <span>+</span>
              <span>Flag Issue</span>
            </button>
          </div>

          <!-- Active Discrepancies List -->
          <div id="activeDiscrepanciesList" class="space-y-2">
            <!-- Discrepancy items injected dynamically -->
          </div>

          <!-- Problem Flags Quick-Toggle Grid -->
          <div id="problemFlagsGrid" class="pt-2 border-t border-tonal2 space-y-2">
            <p class="font-mono text-[10px] uppercase font-bold text-ink-muted">Quick Problem Toggles:</p>
            <div id="problemTogglesContainer" class="grid grid-cols-2 gap-2 text-xs">
              <!-- Checkboxes dynamically generated from ui_sections.problems -->
            </div>
          </div>
        </div>

      </main>

      <!-- Sticky Action Bar (Fixed to Screen Bottom) -->
      <footer class="fixed bottom-0 left-0 right-0 z-40 bg-surface border-t border-bordercol shadow-[0_-4px_16px_rgba(0,0,0,0.08)] max-w-md mx-auto">
        <div class="px-4 py-2.5">
          <!-- Mini Status Ticker Bar -->
          <div class="flex items-center justify-between text-[11px] mb-2 pb-1.5 border-b border-tonal2">
            <div class="flex items-center gap-1.5" aria-live="polite">
              <span class="relative flex h-2 w-2">
                <span id="footerConnDotAnimate" class="animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 bg-fern"></span>
                <span id="footerConnDot" class="relative inline-flex rounded-full h-2 w-2 bg-fern"></span>
              </span>
              <span class="font-mono text-ink-muted" id="footerTickerHost">
                Host Connected
              </span>
            </div>

            <div class="flex items-center gap-1" id="footerSyncStatus">
              <span class="font-mono text-fern-dark font-medium hidden" id="footerSyncStatusText">✓ Edit saved</span>
            </div>
          </div>

          <!-- Primary Action Button: Full-Width Mark Reviewed -->
          <button
            type="button"
            id="btnMarkReviewed"
            onclick="toggleReviewed()"
            class="w-full py-3.5 px-4 rounded-[2px] font-sans font-bold text-sm flex items-center justify-center gap-2 border-2 transition-all touch-target-min touch-press bg-surface text-ink border-bordercol hover:bg-tonal1 shadow-xs"
          >
            <span class="text-fern-dark text-base">✓</span>
            <span id="btnReviewedLabel">Mark Reviewed</span>
          </button>
        </div>
      </footer>
    </div>


    <!-- ========================================== -->
    <!-- MODAL: FULLSCREEN PHOTO VIEWER             -->
    <!-- ========================================== -->
    <div id="photoViewerModal" class="hidden fixed inset-0 z-50 bg-black/95 backdrop-blur-md flex flex-col">
      <!-- Modal Header -->
      <header class="p-3 bg-black/40 text-white flex items-center justify-between border-b border-white/10 shrink-0">
        <div class="flex items-center gap-2 text-xs font-mono">
          <span class="text-fern-light font-bold" id="photoViewerTitle">Specimen Plate</span>
          <span class="text-white/60" id="photoViewerCounter">(1/1)</span>
        </div>
        <button
          type="button"
          onclick="closeModal('photoViewerModal')"
          class="p-2 text-white/80 hover:text-white rounded-[2px] text-lg font-bold touch-target-min"
        >
          ✕
        </button>
      </header>

      <!-- Viewport -->
      <div
        id="photoViewport"
        class="flex-1 relative overflow-hidden flex items-center justify-center p-2 cursor-grab active:cursor-grabbing select-none"
        onmousedown="startPhotoDrag(event)"
        ontouchstart="startPhotoTouch(event)"
      >
        <img
          id="photoViewerImg"
          src=""
          alt="High Resolution Scan"
          class="max-w-full max-h-full object-contain transition-transform duration-75 origin-center"
          style="transform: scale(1) rotate(0deg) translate(0px, 0px);"
        />
      </div>

      <!-- Controls Footer -->
      <footer class="p-3 bg-black/60 text-white flex items-center justify-between border-t border-white/10 shrink-0 text-xs font-mono">
        <div class="flex items-center gap-2">
          <button type="button" onclick="zoomPhoto(-0.5)" class="px-3 py-2 bg-white/10 hover:bg-white/20 rounded-[2px] touch-target-min">− Zoom</button>
          <span id="zoomLevelDisplay" class="text-white/80 min-w-[40px] text-center">1.0x</span>
          <button type="button" onclick="zoomPhoto(0.5)" class="px-3 py-2 bg-white/10 hover:bg-white/20 rounded-[2px] touch-target-min">+ Zoom</button>
        </div>

        <div class="flex items-center gap-2">
          <button type="button" onclick="rotatePhoto()" class="px-3 py-2 bg-white/10 hover:bg-white/20 rounded-[2px] touch-target-min" title="Rotate 90°">↻ Rotate</button>
          <button type="button" onclick="resetPhotoTransform()" class="px-3 py-2 bg-white/10 hover:bg-white/20 rounded-[2px] touch-target-min">Reset</button>
        </div>
      </footer>
    </div>


    <!-- ========================================== -->
    <!-- MODAL: APP SETTINGS                        -->
    <!-- ========================================== -->
    <div id="settingsModal" class="hidden fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4">
      <div class="bg-surface border border-bordercol rounded-[2px] w-full max-w-md shadow-xl overflow-hidden animate-in fade-in zoom-in-95 duration-150">
        <header class="p-3.5 bg-tonal1 border-b border-tonal2 flex items-center justify-between">
          <div class="flex items-center gap-2 text-ink">
            <span class="text-sm">⚙️</span>
            <h2 class="font-serif font-bold text-sm text-ink">
              Application Settings
            </h2>
          </div>
          <button
            type="button"
            onclick="closeSettingsModal()"
            class="p-1 text-ink-faint hover:text-ink rounded-[2px] text-sm font-bold touch-press"
          >
            ✕
          </button>
        </header>

        <div class="p-4 space-y-4">
          <!-- Tactile Haptic Feedback (Adjustable & Toggleable) -->
          <div class="p-2.5 bg-stone-50 border border-bordercol rounded-[2px] space-y-2">
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
            <input type="text" id="settingImageUrlPattern" placeholder="e.g. https://example.com/{id}.jpg" class="w-full bg-surface border border-bordercol rounded-[2px] px-2.5 py-1.5 text-xs text-ink outline-none focus:border-fern" />
            <p class="text-[10px] text-ink-muted mt-1">Available tokens: {id}, {num}, {num:04d}, {suffix}. Leave blank to use desktop defaults.</p>
          </div>

          <div class="pt-2 border-t border-tonal2 flex justify-end gap-2">
            <button type="button" onclick="closeSettingsModal()" class="px-3 py-1.5 border border-bordercol text-ink-muted hover:bg-surface rounded-[2px] text-xs font-medium touch-press">Cancel</button>
            <button type="button" onclick="saveSettings()" class="px-3 py-1.5 bg-fern hover:bg-fern-dark text-white rounded-[2px] text-xs font-bold transition-colors touch-press">Save</button>
          </div>
        </div>
      </div>
    </div>


    <!-- ========================================== -->
    <!-- MODAL: LOCATION PRESETS SETTINGS           -->
    <!-- ========================================== -->
    <div id="presetSettingsModal" class="hidden fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4">
      <div class="bg-surface border border-bordercol rounded-[2px] w-full max-w-md shadow-xl overflow-hidden animate-in fade-in zoom-in-95 duration-150">
        <header class="p-3.5 bg-tonal1 border-b border-tonal2 flex items-center justify-between">
          <div class="flex items-center gap-2 text-ink">
            <span class="text-sm">⚙️</span>
            <h2 class="font-serif font-bold text-sm text-ink">
              Location Presets Settings
            </h2>
          </div>
          <button
            type="button"
            onclick="closePresetSettings()"
            class="p-1 text-ink-faint hover:text-ink rounded-[2px] text-sm font-bold touch-press"
          >
            ✕
          </button>
        </header>

        <div class="p-4 space-y-4">
          <!-- Tactile Haptic Feedback (Adjustable & Toggleable) -->
          <div class="p-2.5 bg-stone-50 border border-bordercol rounded-[2px] space-y-2">
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
            <h3 class="font-bold text-xs text-ink uppercase tracking-wider mb-2">Saved Presets</h3>
            <div id="presetSettingsList" class="max-h-48 overflow-y-auto space-y-1">
               <!-- Preset items injected dynamically -->
            </div>
          </div>

          <div class="pt-2 border-t border-tonal2">
            <button type="button" onclick="toggleNewPresetForm()" class="w-full py-2 bg-fern hover:bg-fern-dark text-white rounded-[2px] text-xs font-bold transition-colors mb-2 cursor-pointer touch-press">
              + Save Current Location as New Preset
            </button>
            <div id="newPresetForm" class="hidden space-y-2 mt-2 p-3 bg-tonal1 border border-bordercol rounded-[2px]">
              <label class="block font-sans text-xs font-medium text-ink">New Preset Name</label>
              <input type="text" id="newPresetNameInput" placeholder="e.g., Cabinet A, Shelf 2" class="w-full bg-surface border border-bordercol rounded-[2px] px-2.5 py-1.5 text-xs text-ink outline-none focus:border-fern" />
              <div class="flex justify-end gap-2 mt-2">
                <button type="button" onclick="toggleNewPresetForm()" class="px-3 py-1.5 border border-bordercol text-ink-muted hover:bg-surface rounded-[2px] text-xs font-medium touch-press">Cancel</button>
                <button type="button" onclick="saveNewLocPreset()" class="px-3 py-1.5 bg-fern hover:bg-fern-dark text-white rounded-[2px] text-xs font-bold transition-colors touch-press">Save</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ========================================== -->
    <!-- ========================================== -->
    <!-- MODAL: RECENT EDITS DRAWER                 -->
    <!-- ========================================== -->
    <div id="recentEditsModal" class="hidden fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex justify-end">
      <div class="bg-surface w-full max-w-sm h-full shadow-xl overflow-hidden flex flex-col animate-in slide-in-from-right duration-200 border-l border-bordercol">
        <header class="p-3.5 bg-tonal1 border-b border-tonal2 flex items-center justify-between shrink-0">
          <div class="flex items-center gap-2">
            <span class="text-sm">↩</span>
            <h2 class="font-serif font-bold text-sm text-ink">
              Recent Changes
            </h2>
          </div>
          <button
            type="button"
            onclick="closeRecentEditsModal()"
            class="p-1 text-ink-faint hover:text-ink rounded-[2px] text-sm font-bold"
          >
            ✕
          </button>
        </header>

        <div class="p-4 overflow-y-auto space-y-3 flex-1 bg-canvas" id="recentEditsList">
          <!-- Dynamically populated -->
        </div>
      </div>
    </div>


    <!-- ========================================== -->
    <!-- MODAL: ADVANCED FILTER                     -->
    <!-- ========================================== -->
    <div id="filterModal" class="hidden fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4">
      <div class="bg-surface border border-bordercol rounded-[2px] w-full max-w-md shadow-xl overflow-hidden animate-in fade-in zoom-in-95 duration-150 flex flex-col max-h-[90vh]">
        <header class="p-3.5 bg-tonal1 border-b border-tonal2 flex items-center justify-between shrink-0">
          <div class="flex items-center gap-2">
            <span class="text-sm">⚙</span>
            <h2 class="font-serif font-bold text-sm text-ink">
              Advanced Filter
            </h2>
          </div>
          <button
            type="button"
            onclick="closeFilterModal()"
            class="p-1 text-ink-faint hover:text-ink rounded-[2px] text-sm font-bold"
          >
            ✕
          </button>
        </header>

        <div class="p-4 overflow-y-auto space-y-6 flex-1">
          <!-- Locations -->
          <div>
            <h3 class="font-sans text-xs font-bold text-ink mb-3 uppercase tracking-wider">Location Filters</h3>
            <div id="filterModalLocations" class="space-y-3">
              <!-- Dynamically populated -->
            </div>
          </div>

          <hr class="border-t border-tonal2" />

          <!-- Specific Problems -->
          <div>
            <h3 class="font-sans text-xs font-bold text-ink mb-3 uppercase tracking-wider">Specific Problems</h3>
            <div id="filterModalProblems" class="space-y-2">
              <!-- Dynamically populated -->
            </div>
          </div>
        </div>

        <footer class="p-3.5 bg-tonal1 border-t border-tonal2 flex gap-3 justify-end shrink-0">
          <button
            type="button"
            onclick="clearAdvancedFilters()"
            class="px-4 py-2 font-sans font-medium text-xs text-ink-muted hover:text-ink transition-colors rounded-[2px]"
          >
            Clear All
          </button>
          <button
            type="button"
            onclick="applyAdvancedFilters()"
            class="px-5 py-2 bg-fern hover:bg-fern-dark text-white font-sans font-bold text-xs transition-colors rounded-[2px]"
          >
            Apply Filters
          </button>
        </footer>
      </div>
    </div>


    <!-- ========================================== -->
    <!-- MODAL: ADD DISCREPANCY                     -->
    <!-- ========================================== -->
    <div id="addDiscrepancyModal" class="hidden fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4">
      <div class="bg-surface border border-bordercol rounded-[2px] w-full max-w-md shadow-xl overflow-hidden animate-in fade-in zoom-in-95 duration-150">
        <header class="p-3.5 bg-tonal1 border-b border-tonal2 flex items-center justify-between">
          <div class="flex items-center gap-2 text-ember">
            <span class="text-sm">⚑</span>
            <h2 class="font-serif font-bold text-sm text-ink">
              Flag Specimen Discrepancy
            </h2>
          </div>
          <button
            type="button"
            onclick="closeModal('addDiscrepancyModal')"
            class="p-1 text-ink-faint hover:text-ink rounded-[2px] text-sm font-bold"
          >
            ✕
          </button>
        </header>

        <form onsubmit="submitDiscrepancy(event)" class="p-4 space-y-3.5">
          <div>
            <label class="block font-sans text-xs font-medium text-ink mb-1">
              Target Field
            </label>
            <select
              id="discrepancyFieldSelect"
              class="w-full bg-surface border border-bordercol rounded-[2px] px-3 py-2 text-xs text-ink outline-none focus:border-fern"
            >
              <!-- Populated dynamically from schema -->
            </select>
          </div>

          <div>
            <label class="block font-sans text-xs font-medium text-ink mb-1">
              Severity Level
            </label>
            <div class="grid grid-cols-3 gap-2">
              <label class="border border-bordercol rounded-[2px] p-2 flex items-center gap-1.5 text-xs cursor-pointer hover:bg-tonal1">
                <input type="radio" name="severity" value="warning" checked class="text-ember">
                <span class="text-ember-dark font-medium">Warning</span>
              </label>
              <label class="border border-bordercol rounded-[2px] p-2 flex items-center gap-1.5 text-xs cursor-pointer hover:bg-tonal1">
                <input type="radio" name="severity" value="critical" class="text-red-600">
                <span class="text-red-700 font-medium">Critical</span>
              </label>
              <label class="border border-bordercol rounded-[2px] p-2 flex items-center gap-1.5 text-xs cursor-pointer hover:bg-tonal1">
                <input type="radio" name="severity" value="inquiry" class="text-blue-600">
                <span class="text-blue-700 font-medium">Inquiry</span>
              </label>
            </div>
          </div>

          <div>
            <label class="block font-sans text-xs font-medium text-ink mb-1">
              Discrepancy Reason / Note *
            </label>
            <textarea
              id="discrepancyReasonInput"
              rows="3"
              required
              placeholder="e.g. Inscription handwriting does not match genus determination..."
              class="w-full bg-surface border border-bordercol rounded-[2px] px-3 py-2 text-xs text-ink outline-none focus:border-fern"
            ></textarea>
          </div>

          <div class="p-2.5 bg-amber-500/10 border border-amber-500/30 rounded-[2px] space-y-2">
            <label class="flex items-center gap-2 cursor-pointer select-none">
              <input type="checkbox" id="discrepancyUnvalCheck" onchange="document.getElementById('discrepancyUnvalContainer').classList.toggle('hidden', !this.checked)" class="w-4 h-4 text-amber-600 rounded cursor-pointer">
              <span class="text-xs font-bold text-amber-800 dark:text-amber-300">Flag as Unvalidated Source</span>
            </label>
            <div id="discrepancyUnvalContainer" class="hidden">
              <input type="text" id="discrepancyUnvalNoteInput" placeholder="Explain why source is unvalidated (optional)..." class="w-full bg-surface border border-amber-500/30 rounded-[2px] px-2.5 py-1.5 text-xs text-ink outline-none">
            </div>
          </div>

          <div class="flex items-center justify-end gap-2 pt-2 border-t border-tonal2">
            <button
              type="button"
              onclick="closeModal('addDiscrepancyModal')"
              class="px-3 py-2 border border-bordercol text-ink-muted hover:bg-tonal1 rounded-[2px] text-xs font-medium"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="px-4 py-2 bg-ember hover:bg-ember-dark text-white rounded-[2px] text-xs font-bold transition"
            >
              Flag Issue
            </button>
          </div>
        </form>
      </div>
    </div>


    <!-- ========================================== -->
    <!-- MODAL: LEAVE DATABASE CONFIRMATION         -->
    <!-- ========================================== -->
    <div id="leaveConfirmModal" class="hidden fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4">
      <div class="bg-surface border border-bordercol rounded-[2px] w-full max-w-sm p-4 shadow-xl space-y-3">
        <div class="flex items-center justify-between border-b border-tonal2 pb-2">
          <h3 class="font-serif font-bold text-sm text-ink">⚠️ Leave Database?</h3>
          <button type="button" onclick="cancelLeaveModal()" class="text-ink-muted font-bold text-sm">✕</button>
        </div>

        <p class="font-sans text-xs text-ink-muted leading-relaxed">
          do you want to leave the database? (you might need to resync)
        </p>

        <div class="flex items-center gap-2 pt-2">
          <button
            type="button"
            onclick="cancelLeaveModal()"
            class="flex-1 py-2 border border-bordercol bg-tonal1 hover:bg-tonal2 text-ink rounded-[2px] text-xs font-bold transition"
          >
            Cancel
          </button>
          <button
            type="button"
            onclick="confirmLeaveModal()"
            class="flex-1 py-2 bg-ember hover:bg-ember-dark text-white rounded-[2px] text-xs font-bold transition"
          >
            Leave
          </button>
        </div>
      </div>
    </div>

    <!-- ========================================== -->
    <!-- MODAL: CONNECTION STATUS                   -->
    <!-- ========================================== -->
    <div id="connectionModal" class="hidden fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4">
      <div class="bg-surface border border-bordercol rounded-[2px] w-full max-w-sm p-4 shadow-xl space-y-3">
        <div class="flex items-center justify-between border-b border-tonal2 pb-2">
          <h3 class="font-serif font-bold text-sm text-ink">⚡ Desktop Host Linked</h3>
          <button type="button" onclick="closeModal('connectionModal')" class="text-ink-muted font-bold text-sm">✕</button>
        </div>

        <div class="space-y-1.5 text-xs font-mono">
          <div class="flex justify-between py-1 border-b border-tonal2">
            <span class="text-ink-muted">Host Status:</span>
            <span class="text-fern-dark font-bold">Online (Active)</span>
          </div>
          <div class="flex justify-between py-1 border-b border-tonal2">
            <span class="text-ink-muted">Database:</span>
            <span class="text-ink font-bold" id="connModalDbName">---</span>
          </div>
          <div class="flex justify-between py-1 border-b border-tonal2">
            <span class="text-ink-muted">Reviewed Total:</span>
            <span class="text-ink" id="connModalReviewed">---</span>
          </div>
          <div class="flex justify-between py-1">
            <span class="text-ink-muted">Latency / Ping:</span>
            <span class="text-fern-dark font-bold" id="connModalPing">12ms</span>
          </div>
        </div>

        <button
          type="button"
          onclick="closeModal('connectionModal')"
          class="w-full py-2 bg-fern hover:bg-fern-dark text-white rounded-[2px] text-xs font-bold"
        >
          Done
        </button>
      </div>
    </div>

    <!-- ========================================== -->
    <!-- MODAL: ICEDIG MISSING DATA BOTTOM SHEET   -->
    <!-- ========================================== -->
    <div id="icedigBottomSheetModal" class="hidden fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-end sm:items-center justify-center p-0 sm:p-4">
      <div class="bg-surface border-t sm:border border-bordercol rounded-t-xl sm:rounded-[2px] w-full max-w-md shadow-2xl overflow-hidden max-h-[90vh] flex flex-col animate-in slide-in-from-bottom duration-150">
        <header class="p-3.5 bg-tonal1 border-b border-tonal2 flex items-center justify-between">
          <div class="flex items-center gap-2 text-amber-700 dark:text-amber-400">
            <span class="text-sm font-bold">∅</span>
            <h2 id="icedigModalTitle" class="font-serif font-bold text-sm text-ink">
              Missing Data Status
            </h2>
          </div>
          <button
            type="button"
            onclick="closeIcedigBottomSheet()"
            class="p-1 text-ink-faint hover:text-ink rounded-[2px] text-sm font-bold cursor-pointer"
          >
            ✕
          </button>
        </header>

        <div class="p-4 space-y-3 overflow-y-auto">
          <div id="icedigOverwriteNotice" class="hidden p-2.5 bg-amber-500/10 border border-amber-500/30 rounded-[2px] text-xs text-amber-800 dark:text-amber-300 font-medium">
            ⚠️ Overwriting current value: <span id="icedigCurrentValPreview" class="font-bold"></span>
          </div>

          <div class="text-[11px] font-sans text-ink-muted uppercase tracking-wider font-bold">
            Select ICEDIG D4.1 Standard Code:
          </div>

          <div class="space-y-2">
            <button
              type="button"
              onclick="applyIcedigChoice('unknown:missing')"
              class="w-full text-left p-3 rounded-[2px] border border-bordercol bg-surface hover:bg-amber-500/10 hover:border-amber-400 transition-colors cursor-pointer touch-press"
            >
              <div class="flex items-center justify-between">
                <span class="font-bold text-xs text-ink">📄 Blank on Physical Label</span>
                <code class="text-[10px] bg-tonal1 px-1.5 py-0.5 rounded text-ink-muted font-mono">unknown:missing</code>
              </div>
              <p class="text-[11px] text-ink-muted mt-0.5">Information was looked for but is genuinely absent on the physical specimen label.</p>
            </button>

            <button
              type="button"
              onclick="applyIcedigChoice('unknown:indecipherable')"
              class="w-full text-left p-3 rounded-[2px] border border-bordercol bg-surface hover:bg-amber-500/10 hover:border-amber-400 transition-colors cursor-pointer touch-press"
            >
              <div class="flex items-center justify-between">
                <span class="font-bold text-xs text-ink">🔍 Illegible / Damaged Label</span>
                <code class="text-[10px] bg-tonal1 px-1.5 py-0.5 rounded text-ink-muted font-mono">unknown:indecipherable</code>
              </div>
              <p class="text-[11px] text-ink-muted mt-0.5">Text is physically present but cannot be read due to handwriting, fading, or damage.</p>
            </button>

            <button
              type="button"
              onclick="applyIcedigChoice('unknown:undigitized')"
              class="w-full text-left p-3 rounded-[2px] border border-bordercol bg-surface hover:bg-amber-500/10 hover:border-amber-400 transition-colors cursor-pointer touch-press"
            >
              <div class="flex items-center justify-between">
                <span class="font-bold text-xs text-ink">⏭️ Skipped in Digitization</span>
                <code class="text-[10px] bg-tonal1 px-1.5 py-0.5 rounded text-ink-muted font-mono">unknown:undigitized</code>
              </div>
              <p class="text-[11px] text-ink-muted mt-0.5">Field was intentionally omitted from this digitization workflow pass.</p>
            </button>

            <button
              type="button"
              onclick="applyIcedigChoice('withheld')"
              class="w-full text-left p-3 rounded-[2px] border border-bordercol bg-surface hover:bg-amber-500/10 hover:border-amber-400 transition-colors cursor-pointer touch-press"
            >
              <div class="flex items-center justify-between">
                <span class="font-bold text-xs text-ink">🔒 Sensitive / Withheld</span>
                <code class="text-[10px] bg-tonal1 px-1.5 py-0.5 rounded text-ink-muted font-mono">withheld</code>
              </div>
              <p class="text-[11px] text-ink-muted mt-0.5">Data exists but is redacted for policy, privacy, or species protection reasons.</p>
            </button>
          </div>

          <div class="pt-2 border-t border-bordercol flex items-center justify-between gap-2">
            <button
              type="button"
              onclick="applyIcedigChoice('')"
              class="px-3 py-2 text-xs text-ink-muted hover:text-ember rounded border border-bordercol hover:bg-tonal1 cursor-pointer touch-press"
            >
              Clear Field (Blank)
            </button>
            <button
              type="button"
              onclick="closeIcedigBottomSheet()"
              class="px-4 py-2 bg-tonal1 hover:bg-tonal2 text-ink text-xs font-bold rounded border border-bordercol cursor-pointer touch-press"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Floating Toast Notification -->
    <div id="toast" class="hidden fixed bottom-24 left-4 right-4 max-w-sm mx-auto bg-fern-dark text-white text-xs font-bold py-2.5 px-4 rounded-[2px] shadow-lg text-center z-50 transition-opacity">
      Edits saved & synchronized
    </div>

  </div>

  <!-- ========================================== -->
  <!-- CLIENT APPLICATION SCRIPT                  -->
  <!-- ========================================== -->
  <script>
    const _urlParams = new URLSearchParams(window.location.search);
    const TOKEN = _urlParams.get('token') || "{{ token }}";
    let activeSchema = null;
    let objectList = [];
    let currentOid = null;
    let currentRecord = null;
    let isReviewed = false;
    let activeStatusFilter = 'all';
    let noImageFilterActive = false;
    let activeAdvancedFilters = { locations: {}, problems: {} };
    let activeSortBy = 'id-asc';
    let searchQuery = '';
    let searchDebounceTimer = null;
    let autoSaveTimer = null;
    let isSaving = false;
    let hasPendingSave = false;
    let dirtyFields = new Set();
    let currentUnvalidatedMap = {};
    let wakeLockSentinel = null;
    let isWalkModeWanted = false;
    try { isWalkModeWanted = localStorage.getItem('arbor_walk_mode') === 'true'; } catch(e) {}

    let locationPresets = {};
    let lastSelectedPreset = "Default";
    let historicalData = {};
    let revertState = {}; // field: originalValue
    let presenceHeartbeatTimer = null;

    async function sendPresence(oid) {
      try {
        const res = await apiFetch('/api/presence', {
          method: 'POST',
          body: JSON.stringify({ oid: oid ? String(oid) : null })
        });
        if (res && currentOid && String(oid) === String(currentOid)) {
          updatePresenceBanner(res.other_viewers_count || 0);
        }
      } catch (err) {
        console.warn('sendPresence error:', err);
      }
    }

    function updatePresenceBanner(otherCount) {
      const banner = document.getElementById('detailPresenceBanner');
      const text = document.getElementById('detailPresenceText');
      if (!banner) return;
      if (otherCount > 0) {
        if (text) {
          text.textContent = otherCount === 1
            ? 'Warning: Another worker is currently viewing this record.'
            : `Warning: ${otherCount} other workers are currently viewing this record.`;
        }
        banner.classList.remove('hidden');
      } else {
        banner.classList.add('hidden');
      }
    }

    async function fetchHistoricalData(oid) {
      try {
        const cachedData = await getCachedHistoricalData(oid);
        if (cachedData) {
          historicalData = cachedData;
          injectHistoricalData();
        }

        const data = await apiFetch(`/api/object/${encodeURIComponent(oid)}/history`);
        if (data) {
          historicalData = data.historical_data || {};
          cacheHistoricalData(oid, historicalData);
          injectHistoricalData();
        }
      } catch (err) {
        console.error("Failed to fetch historical data:", err);
      }
    }

    function injectHistoricalData() {
        if (!historicalData || Object.keys(historicalData).length === 0) {
            return;
        }

        for (const [field, valuesMap] of Object.entries(historicalData)) {
            if (Object.keys(valuesMap).length === 0) continue;

            const fNameClean = field.replace(/[^a-zA-Z0-9_]/g, '_');
            const toggleBtn = document.getElementById(`history_toggle_${fNameClean}`);
            const container = document.getElementById(`history_container_${fNameClean}`);

            if (!toggleBtn || !container) continue;

            let currentVal = '';
            if (currentRecord.registration && currentRecord.registration[field] !== undefined) {
               currentVal = currentRecord.registration[field];
            } else if (currentRecord.observation && currentRecord.observation[field] !== undefined) {
               currentVal = currentRecord.observation[field];
            }
            let currentValDisp = currentVal ? String(currentVal) : "[BLANK]";

            let suggestionsHtml = '';
            for (const [val, sources] of Object.entries(valuesMap)) {
                const encodedVal = val.replace(/'/g, "\\'").replace(/"/g, '&quot;');
                const sourceStr = sources.join(', ');
                suggestionsHtml += `
                    <div id="hist_sug_${fNameClean}_${encodedVal}" class="p-2.5 mt-1.5 bg-surface border border-bordercol rounded-[2px] cursor-pointer touch-target-min touch-press transition group" onclick="stageHistoricalValue('${field}', '${encodedVal}')">
                        <div class="flex items-center justify-between gap-2">
                            <div class="font-mono text-xs text-ink group-[.staged]:font-bold group-[.staged]:text-ember truncate">${encodedVal}</div>
                            <button type="button" class="hidden group-[.staged]:inline-flex min-h-[36px] bg-ember text-white px-3 py-1.5 text-xs rounded-[2px] font-bold shadow-xs items-center justify-center shrink-0" onclick="event.stopPropagation(); applyHistoricalValue('${field}', '${encodedVal}')">Apply</button>
                        </div>
                        <div class="font-sans text-[10px] text-ink-muted mt-1">Sources: <span class="font-mono">${sourceStr}</span></div>
                    </div>
                `;
            }

            let undoBtn = '';
            if (revertState.hasOwnProperty(field)) {
                 const orig = revertState[field].replace(/'/g, "\\'").replace(/"/g, '&quot;');
                 undoBtn = `<button type="button" onclick="undoHistoricalValue('${field}', '${orig}')" class="text-[11px] text-ember hover:underline font-bold bg-ember-light px-2 py-1 border border-ember-border rounded-[2px] touch-press">Undo Change</button>`;
            }

            container.innerHTML = `
                <div class="flex items-center justify-between mb-1.5">
                    <span class="text-[10px] font-sans font-bold text-ink-muted uppercase tracking-wider">History Suggestions</span>
                    ${undoBtn}
                </div>
                <div class="text-xs font-mono text-ink-muted mb-2">Current: <span class="text-ink font-semibold">${currentValDisp}</span></div>
                ${suggestionsHtml}
            `;

            // Unhide the toggle button since there is history available
            toggleBtn.classList.remove('hidden');
        }
    }

    function toggleHistoryContainer(field) {
        const fNameClean = field.replace(/[^a-zA-Z0-9_]/g, '_');
        const container = document.getElementById(`history_container_${fNameClean}`);
        if (container) {
            container.classList.toggle('hidden');
        }
    }

    function stageHistoricalValue(field, value) {
        const fNameClean = field.replace(/[^a-zA-Z0-9_]/g, '_');
        const container = document.getElementById(`history_container_${fNameClean}`);
        if (!container) return;

        // Reset all suggestion cards in this container
        const suggestions = container.querySelectorAll('[id^="hist_sug_"]');
        suggestions.forEach(sug => {
            sug.classList.remove('staged', 'bg-ember-light', 'border-ember', 'ring-1', 'ring-ember');
            sug.classList.add('bg-surface', 'border-bordercol');
        });

        // Apply distinct staged styling to selected card
        const suggestionId = `hist_sug_${fNameClean}_${value}`;
        const selectedSug = document.getElementById(suggestionId);
        if (selectedSug) {
            selectedSug.classList.remove('bg-surface', 'border-bordercol');
            selectedSug.classList.add('staged', 'bg-ember-light', 'border-ember', 'ring-1', 'ring-ember');
        }
    }

    async function applyHistoricalValue(field, value) {
        // Find input element for this field
        const inputs = document.querySelectorAll(`[data-field="${field}"]`);
        if (inputs.length === 0) {
            showToast(`Field ${field} not found in form`, true);
            return;
        }

        const input = inputs[0];

        // Save revert state if not already saved
        if (!revertState.hasOwnProperty(field)) {
             revertState[field] = input.type === 'checkbox' ? (input.checked ? 'true' : 'false') : input.value;
        }

        // Apply
        if (input.type === 'checkbox') {
             input.checked = (value.toLowerCase() === 'true' || value === '1' || value === 'yes');
        } else {
             input.value = value;
        }
        markDirty(field);

        // Micro-interaction: Flash the updated input with fern border to confirm receipt
        input.classList.add('ring-2', 'ring-fern', 'border-fern');
        setTimeout(() => {
            input.classList.remove('ring-2', 'ring-fern', 'border-fern');
        }, 1200);

        // Clear related problems locally
        if (currentRecord.observation) {
            const probKeys = Object.keys(currentRecord.observation).filter(k => k === field + '_Problem' || (activeSchema.ui_sections.problems && activeSchema.ui_sections.problems.some(p => p.name === k && p.target === field))); // Assuming target might exist, or just clear exact match

            // For Arbor, problem fields usually match `${field}_Problem` or similar, let's clear it
            const exactProb = `${field}_Problem`;
            if (currentRecord.observation.hasOwnProperty(exactProb)) {
                 currentRecord.observation[exactProb] = false;
                 const probToggle = document.getElementById(`prob_${exactProb}`);
                 if (probToggle) probToggle.checked = false;
                 markDirty(exactProb);
            }
        }

        // Trigger save and update UI
        triggerAutoSave();
        showToast(`Applied historical value for ${field}`);

        // Update local currentRecord so rendering reflects changes
        if (currentRecord.registration && currentRecord.registration[field] !== undefined) {
             currentRecord.registration[field] = value;
        } else if (currentRecord.observation && currentRecord.observation[field] !== undefined) {
             currentRecord.observation[field] = value;
        }

        // Re-inject history UI for this field to show new current value
        injectHistoricalData();

        // Hide the container after application
        const fNameClean = field.replace(/[^a-zA-Z0-9_]/g, '_');
        const container = document.getElementById(`history_container_${fNameClean}`);
        if (container) {
            container.classList.add('hidden');
        }
    }

    async function undoHistoricalValue(field, originalValue) {
        if (!revertState.hasOwnProperty(field)) return;

        const inputs = document.querySelectorAll(`[data-field="${field}"]`);
        if (inputs.length > 0) {
            const input = inputs[0];
            if (input.type === 'checkbox') {
                 input.checked = (originalValue.toLowerCase() === 'true' || originalValue === '1' || originalValue === 'yes');
            } else {
                 input.value = originalValue;
            }
        }
        markDirty(field);

        if (currentRecord.registration && currentRecord.registration[field] !== undefined) {
             currentRecord.registration[field] = originalValue;
        } else if (currentRecord.observation && currentRecord.observation[field] !== undefined) {
             currentRecord.observation[field] = originalValue;
        }

        const exactProb = `${field}_Problem`;
        if (currentRecord.observation && currentRecord.observation.hasOwnProperty(exactProb)) {
             currentRecord.observation[exactProb] = true;
             const probToggle = document.getElementById(`prob_${exactProb}`);
             if (probToggle) probToggle.checked = true;
             markDirty(exactProb);
        }

        delete revertState[field];

        triggerAutoSave();
        showToast(`Reverted ${field} to original value`);
        injectHistoricalData();
    }



    // Photo viewer state
    let photoUrls = [];
    let currentPhotoIdx = 0;
    let photoZoom = 1;
    let photoRotation = 0;
    let photoPan = { x: 0, y: 0 };
    let isDraggingPhoto = false;
    let photoDragStart = { x: 0, y: 0 };

    async function apiFetch(url, options = {}) {
      options.headers = options.headers || {};
      options.headers['X-Session-Token'] = TOKEN;
      if (options.body && typeof options.body === 'string' && !options.headers['Content-Type']) {
        options.headers['Content-Type'] = 'application/json';
      }
      const sep = url.includes('?') ? '&' : '?';
      const fullUrl = `${url}${sep}token=${encodeURIComponent(TOKEN)}`;
      const isCacheable = options.method !== 'POST' && (url.startsWith('/api/schema') || url.startsWith('/api/objects'));

      try {
        const res = await fetch(fullUrl, options);
        if (!res.ok) {
          console.warn(`API response status ${res.status} for ${url}`);
        }
        let data = {};
        try {
          data = await res.json();
        } catch (jsonErr) {
          data = {};
        }
        if (data && typeof data === 'object') {
          data._status = res.status;
          data.status = res.status;
          data._ok = res.ok;
        }
        if (isCacheable) {
          cacheApiResponse(url, data);
        }
        return data;
      } catch (err) {
        console.error(`Fetch error on ${url}:`, err);
        if (isCacheable) {
          const cached = await getCachedApiResponse(url);
          if (cached) return cached;
        }
        return {};
      }
    }

    let toastTimeout = null;
    let currentToastUndoCb = null;

    function showToast(msg, isError = false) {
      const toast = document.getElementById('toast');
      if (!toast) return;
      if (toastTimeout) clearTimeout(toastTimeout);
      currentToastUndoCb = null;
      toast.innerHTML = `<span>${msg}</span>`;
      toast.className = `fixed bottom-24 left-4 right-4 max-w-sm mx-auto ${isError ? 'bg-ember-dark' : 'bg-fern-dark'} text-white text-xs font-bold py-2.5 px-4 rounded-[2px] shadow-lg text-center z-50 transition-opacity`;
      toast.classList.remove('hidden');
      toastTimeout = setTimeout(() => toast.classList.add('hidden'), 2200);
    }

    function showToastWithUndo(msg, undoCallback) {
      const toast = document.getElementById('toast');
      if (!toast) return;
      if (toastTimeout) clearTimeout(toastTimeout);
      currentToastUndoCb = undoCallback;
      toast.innerHTML = `
        <div class="flex items-center justify-between gap-3 px-1">
          <span class="truncate">${msg}</span>
          <button type="button" onclick="triggerToastUndo()" class="underline font-bold text-amber-300 hover:text-white text-xs uppercase tracking-wider cursor-pointer touch-press">
            UNDO
          </button>
        </div>
      `;
      toast.className = `fixed bottom-24 left-4 right-4 max-w-sm mx-auto bg-stone-900 text-white text-xs font-bold py-2.5 px-4 rounded-[2px] shadow-xl border border-bordercol z-50 transition-opacity`;
      toast.classList.remove('hidden');
      toastTimeout = setTimeout(() => {
        toast.classList.add('hidden');
        currentToastUndoCb = null;
      }, 5000);
    }

    function triggerToastUndo() {
      if (typeof currentToastUndoCb === 'function') {
        currentToastUndoCb();
        currentToastUndoCb = null;
      }
      const toast = document.getElementById('toast');
      if (toast) toast.classList.add('hidden');
    }

    let currentIcedigTarget = null;
    let icedigUndoState = null;

    function openIcedigBottomSheet(section, fName) {
      const inputId = `input_${section}_${fName.replace(/[^a-zA-Z0-9_]/g, '_')}`;
      const inputEl = document.getElementById(inputId);
      const currentVal = inputEl ? inputEl.value : '';

      currentIcedigTarget = { section, fName, inputId, previousVal: currentVal };

      const titleEl = document.getElementById('icedigModalTitle');
      if (titleEl) titleEl.textContent = `Missing Data Status: ${fName}`;

      const noticeEl = document.getElementById('icedigOverwriteNotice');
      const previewEl = document.getElementById('icedigCurrentValPreview');
      if (noticeEl && previewEl) {
        if (currentVal && !isValueUnknown(currentVal)) {
          previewEl.textContent = `"${currentVal}"`;
          noticeEl.classList.remove('hidden');
        } else {
          noticeEl.classList.add('hidden');
        }
      }

      openModal('icedigBottomSheetModal');
    }

    function closeIcedigBottomSheet() {
      closeModal('icedigBottomSheetModal');
      currentIcedigTarget = null;
    }

    function applyIcedigChoice(code) {
      if (!currentIcedigTarget) return;
      const { section, fName, inputId, previousVal } = currentIcedigTarget;
      const inputEl = document.getElementById(inputId);

      if (inputEl) {
        inputEl.value = code;
        markDirty(fName);

        const hasUkn = isValueUnknown(code);
        inputEl.className = `w-full min-h-[44px] border rounded-[2px] px-3 py-2 text-xs outline-none ${
          hasUkn
            ? 'border-l-4 border-l-[#FBC02D] bg-[#fef9c3] border-[#fde047] text-[#854d0e] font-medium focus:border-[#eab308]'
            : 'border-bordercol bg-surface text-ink focus:border-fern'
        }`;

        // Update local currentRecord if available
        if (currentRecord) {
          if (section === 'registration' && currentRecord.registration) {
            currentRecord.registration[fName] = code;
          } else if (section === 'observation' && currentRecord.observation) {
            currentRecord.observation[fName] = code;
          }
        }

        // Save undo state & show toast
        icedigUndoState = { section, fName, inputId, valueToRestore: previousVal };
        showToastWithUndo(`Set ${fName} to ${code || 'blank'}`, () => {
          if (icedigUndoState && icedigUndoState.inputId === inputId) {
            inputEl.value = icedigUndoState.valueToRestore;
            markDirty(fName);
            if (currentRecord) {
              if (section === 'registration' && currentRecord.registration) {
                currentRecord.registration[fName] = icedigUndoState.valueToRestore;
              } else if (section === 'observation' && currentRecord.observation) {
                currentRecord.observation[fName] = icedigUndoState.valueToRestore;
              }
            }
            triggerAutoSave();
            saveCurrentEdits();
          }
        });

        triggerAutoSave();
        saveCurrentEdits();
      }

      closeIcedigBottomSheet();
    }

    function openModal(id) {
      document.getElementById(id).classList.remove('hidden');
    }

    function closeModal(id) {
      document.getElementById(id).classList.add('hidden');
    }

    let isLeavingApp = false;
    let hasUnsavedChanges = false;

    function openLeaveModal() {
      openModal('leaveConfirmModal');
    }

    function cancelLeaveModal() {
      closeModal('leaveConfirmModal');
      // Re-push list state so history is restored at [root] -> [list]
      window.history.pushState({ view: 'list' }, '');
    }

    function confirmLeaveModal() {
      isLeavingApp = true;
      closeModal('leaveConfirmModal');
      if (window.history.length > 1) {
        window.history.back();
      } else {
        window.location.href = '/login';
      }
    }

    window.addEventListener('beforeunload', (e) => {
      if (hasUnsavedChanges) {
        e.preventDefault();
        e.returnValue = 'You have unsaved offline changes. Are you sure you want to leave?';
        return e.returnValue;
      }
    });

    window.addEventListener('popstate', async (event) => {
      if (isLeavingApp) return;

      const state = event.state;

      // If we popped to list view:
      if (state && state.view === 'list') {
        closeModal('leaveConfirmModal');
        closeModal('photoViewerModal');
        closeModal('presetSettingsModal');
        closeModal('filterModal');
        closeModal('addDiscrepancyModal');
        closeModal('connectionModal');
        await showListView(false);
      } else if (state && state.view === 'detail') {
        closeModal('leaveConfirmModal');
        if (state.id && state.id !== currentOid) {
          await loadSpecimen(state.id, true);
        } else {
          showDetailView();
        }
      } else {
        // Popped past list view (e.g. state is 'root' or null) -> user clicked back on List View
        openLeaveModal();
      }
    });


    async function init() {
      if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/service-worker.js').catch(err => console.error('ServiceWorker registration failed: ', err));
      }

      try {
        await initIndexedDB();
      } catch (e) {
        console.warn('Offline DB init failed', e);
      }

      // 0. Initialize SPA History State for Back Button handling
      if (!window.history.state || window.history.state.view !== 'list') {
        window.history.replaceState({ view: 'root' }, '');
        window.history.pushState({ view: 'list' }, '');
      }

      // 1. Immediately initiate live SSE connection in background so desktop detects phone right away
      setupEventSource();
      if (isWalkModeWanted) {
        acquireWakeLock(true);
      }
      document.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'visible') {
          _reconnectDelay = 2000;
          if (_reconnectTimer) clearTimeout(_reconnectTimer);
          setupEventSource();  // closes stale connection and opens a fresh one
          if (isWalkModeWanted && !wakeLockSentinel) {
            acquireWakeLock(true);
          }
        }
      });
      window.addEventListener('online', () => {
        _reconnectDelay = 2000;
        if (_reconnectTimer) clearTimeout(_reconnectTimer);
        setupEventSource();
      });
      window.addEventListener('offline', () => {
        stopPing();
        if (_reconnectTimer) clearTimeout(_reconnectTimer);
        if (_evtSource) { _evtSource.close(); _evtSource = null; }
        updateConnectionState('disconnected');
      });

      try {
        // 2. Fetch Schema from Master config.py
        activeSchema = await apiFetch('/api/schema');
        const dbName = (activeSchema && activeSchema.database_name) ? activeSchema.database_name : 'Active Database';
        document.getElementById('headerDbName').textContent = dbName;
        document.getElementById('connModalDbName').textContent = dbName;

        // 3. Fetch Initial List
        await fetchList();

        // 4. Fetch Location Presets
        const presetsRes = await apiFetch('/api/presets');
        if (presetsRes && presetsRes.success) {
          locationPresets = presetsRes.presets || {};
        }

        // 5. Populate Discrepancy Field Select Options
        populateDiscrepancyFields();

        // 6. Update Advanced Filter Indicator
        updateFilterIndicator();
      } catch (err) {
        console.error("Initialization error:", err);
        document.getElementById('headerDbName').textContent = 'Active Database';
        fetchList();
      }
    }

    let _evtSource = null;
    let _reconnectDelay = 2000;
    const _maxReconnectDelay = 16000;
    let _pingInterval = null;
    let _missedPings = 0;
    let _reconnectTimer = null;

    function startPing() {
      stopPing();
      _missedPings = 0;
      _pingInterval = setInterval(async () => {
        if (!navigator.onLine) {
           _missedPings = 3; // Force immediate disconnect if browser knows it's offline
        } else {
           try {
             const res = await fetch('/api/ping?token=' + encodeURIComponent(TOKEN));
             if (res.ok) {
               _missedPings = 0;
             } else {
               _missedPings++;
             }
           } catch (e) {
             _missedPings++;
           }
        }

        if (_missedPings >= 3) {
          stopPing();
          if (_evtSource) {
            _evtSource.close();
            _evtSource = null;
          }
          updateConnectionState('disconnected');
          scheduleReconnect();
        }
      }, 10000);
    }

    function stopPing() {
      if (_pingInterval) {
        clearInterval(_pingInterval);
        _pingInterval = null;
      }
    }

    function scheduleReconnect() {
      if (_reconnectTimer) clearTimeout(_reconnectTimer);
      _reconnectTimer = setTimeout(() => {
        setupEventSource();
        _reconnectDelay = Math.min(_reconnectDelay * 2, _maxReconnectDelay);
      }, _reconnectDelay);
    }

    let db;
    function initIndexedDB() {
      return new Promise((resolve, reject) => {
        const request = indexedDB.open('arbor_offline_db', 3);
        request.onupgradeneeded = (e) => {
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
        request.onsuccess = (e) => {
          db = e.target.result;
          resolve();
        };
        request.onerror = (e) => {
          console.error('IndexedDB init error:', e);
          reject(e);
        };
      });
    }

    function cacheApiResponse(url, data) {
      if (!db) return;
      try {
        const tx = db.transaction('api_cache', 'readwrite');
        tx.objectStore('api_cache').put({ url, data });
      } catch (e) { console.error('Cache API error', e); }
    }

    function getCachedApiResponse(url) {
      return new Promise((resolve) => {
        if (!db) return resolve(null);
        try {
          const tx = db.transaction('api_cache', 'readonly');
          const req = tx.objectStore('api_cache').get(url);
          req.onsuccess = () => resolve(req.result ? req.result.data : null);
          req.onerror = () => resolve(null);
        } catch (e) {
          resolve(null);
        }
      });
    }

    function cacheHistoricalData(oid, data) {
      if (!db) return;
      try {
        const tx = db.transaction('historical_cache', 'readwrite');
        tx.objectStore('historical_cache').put({ oid, data });
      } catch (e) { console.error('Cache history error', e); }
    }

    function getCachedHistoricalData(oid) {
      return new Promise((resolve) => {
        if (!db) return resolve(null);
        try {
          const tx = db.transaction('historical_cache', 'readonly');
          const req = tx.objectStore('historical_cache').get(oid);
          req.onsuccess = () => resolve(req.result ? req.result.data : null);
          req.onerror = () => resolve(null);
        } catch (e) {
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
        console.error('LocalStorage queue error', e);
      }

      if (db) {
        try {
          const tx = db.transaction('queued_mutations', 'readwrite');
          tx.objectStore('queued_mutations').put(payload);
        } catch (e) {}
      }
      updateOfflineBannerQueueCount();
      hasUnsavedChanges = true;
    }

    function getQueuedMutations() {
      return new Promise((resolve) => {
        const localMutations = getLocalStorageQueue();
        if (!db) return resolve(localMutations);
        try {
          const tx = db.transaction('queued_mutations', 'readonly');
          const store = tx.objectStore('queued_mutations');
          const req = store.getAll();
          req.onsuccess = () => {
            const idbMutations = req.result || [];
            const map = new Map();
            localMutations.forEach(m => map.set(String(m.timestamp || m.oid), m));
            idbMutations.forEach(m => map.set(String(m.timestamp || m.oid), m));
            resolve(Array.from(map.values()));
          };
          req.onerror = () => resolve(localMutations);
        } catch (e) {
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
        } catch (e) {}
      }
      updateOfflineBannerQueueCount();
    }

    function updateOfflineBannerQueueCount() {
      const localQ = getLocalStorageQueue();
      const count = localQ.length;
      hasUnsavedChanges = count > 0;
      const banner = document.getElementById('footerSyncStatus');
      if (banner) {
        if (count > 0) {
          banner.innerHTML = `<span class="font-mono text-ember-dark font-medium">Offline (${count} edits queued in storage)</span>`;
        } else if (navigator.onLine) {
          banner.innerHTML = '<span class="font-mono text-fern-dark font-medium" id="footerSyncStatusText">✓ Synced</span>';
        }
      }
    }

    async function flushQueuedMutations() {
      const mutations = await getQueuedMutations();
      if (mutations.length === 0) return;
      // Sort by timestamp just in case
      mutations.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));

      const offlineBanner = document.getElementById('offlineBanner');
      const bannerContent = document.getElementById('offlineBannerContent');
      const retryBtn = document.getElementById('btnOfflineRetry');
      const footerStatus = document.getElementById('footerSyncStatus');

      // Prominent syncing visual feedback
      if (offlineBanner && bannerContent) {
        offlineBanner.className = 'bg-fern-light border-b border-fern-border px-4 py-2 flex items-center justify-between gap-2 text-xs font-sans font-medium text-fern-dark shrink-0 transition-all shadow-xs';
        offlineBanner.classList.remove('hidden');
        bannerContent.innerHTML = `
          <svg class="animate-spin h-3.5 w-3.5 text-fern shrink-0" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span class="font-bold">Syncing ${mutations.length} queued edit${mutations.length > 1 ? 's' : ''} to host...</span>
        `;
        if (retryBtn) retryBtn.classList.add('hidden');
      }
      if (footerStatus) {
        footerStatus.innerHTML = `<span class="flex items-center gap-1.5 font-mono text-fern-dark font-medium animate-pulse"><span>Syncing queued edits (${mutations.length})...</span></span>`;
      }

      try {
        const res = await apiFetch('/api/batch_update', {
          method: 'POST',
          body: JSON.stringify({ updates: mutations })
        });
        if (res && (res.success || res.updated_count !== undefined)) {
          clearQueuedMutations(mutations.map(m => m.timestamp));
          showToast(`✓ Reconnected: ${mutations.length} queued edits synced to host`);
          if (footerStatus) {
            footerStatus.innerHTML = '<span class="font-mono text-fern-dark font-medium" id="footerSyncStatusText">✓ All synced</span>';
          }
        }
      } catch (err) {
        console.error('Failed to flush queued mutations', err);
        showToast('Sync failed; will retry when connected', true);
      } finally {
        if (offlineBanner && navigator.onLine) {
          offlineBanner.classList.add('hidden');
        }
      }
    }

    function updateConnectionState(state) {
      const badge = document.getElementById('pingBadge');
      const footerHost = document.getElementById('footerTickerHost');
      const dotHeader = document.getElementById('connPingDot');
      const dotHeaderAnim = document.getElementById('connPingDotAnimate');
      const dotFooter = document.getElementById('footerConnDot');
      const dotFooterAnim = document.getElementById('footerConnDotAnimate');
      const offlineBanner = document.getElementById('offlineBanner');
      const bannerContent = document.getElementById('offlineBannerContent');
      const retryBtn = document.getElementById('btnOfflineRetry');
      const syncStatusText = document.getElementById('footerSyncStatusText');

      if (state === 'connected') {
        if (badge) badge.textContent = 'Live';
        if (footerHost) footerHost.textContent = 'Host Connected';
        if (offlineBanner) offlineBanner.classList.add('hidden');
        [dotHeader, dotFooter].forEach(d => { if (d) d.className = 'relative inline-flex rounded-full h-2 w-2 bg-fern'; });
        [dotHeaderAnim, dotFooterAnim].forEach(d => { if (d) d.className = 'animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 bg-fern'; });
      } else if (state === 'connecting') {
        if (badge) badge.textContent = 'Connecting...';
        if (footerHost) footerHost.textContent = 'Connecting to host...';
        [dotHeader, dotFooter].forEach(d => { if (d) d.className = 'relative inline-flex rounded-full h-2 w-2 bg-ember'; });
        [dotHeaderAnim, dotFooterAnim].forEach(d => { if (d) d.className = 'animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 bg-ember'; });
      } else {
        if (badge) badge.textContent = 'Offline';
        if (footerHost) footerHost.textContent = 'Host Disconnected';
        if (offlineBanner) {
          offlineBanner.className = 'bg-ember-light border-b border-ember-border px-4 py-2 flex items-center justify-between gap-2 text-xs font-sans font-medium text-ember-dark shrink-0 transition-all shadow-xs';
          offlineBanner.classList.remove('hidden');
        }
        if (bannerContent) {
          bannerContent.innerHTML = `<span class="text-sm">⚠</span><span>Connection to host lost. Reconnecting...</span>`;
        }
        if (retryBtn) retryBtn.classList.remove('hidden');
        [dotHeader, dotFooter].forEach(d => { if (d) d.className = 'relative inline-flex rounded-full h-2 w-2 bg-ember-dark'; });
        [dotHeaderAnim, dotFooterAnim].forEach(d => { if (d) d.className = 'hidden'; });
        if (syncStatusText) syncStatusText.classList.add('hidden');
      }
    }

    async function fetchStatus() {
      try {
        const res = await apiFetch('/api/status');
        if (res && res.database_name) {
          const dbEl = document.getElementById('headerDbName');
          if (dbEl) dbEl.textContent = res.database_name;
          const modalDb = document.getElementById('connModalDbName');
          if (modalDb) modalDb.textContent = res.database_name;
        }
      } catch (e) {
        console.warn('fetchStatus error', e);
      }
    }

    function setupEventSource() {
      try {
        if (_reconnectTimer) clearTimeout(_reconnectTimer);
        if (_evtSource) { _evtSource.close(); _evtSource = null; }
        updateConnectionState('connecting');
        _evtSource = new EventSource(`/api/events?token=${encodeURIComponent(TOKEN)}`);

        _evtSource.onopen = function() {
          updateConnectionState('connected');
          _reconnectDelay = 2000;
          startPing();
          flushQueuedMutations();
          fetchStatus();
          if (currentOid && dirtyFields.size === 0) {
            loadSpecimen(currentOid, true);
          } else if (!currentOid && activeSchema && objectList.length === 0) {
            fetchList();
          }
        };

        _evtSource.onerror = function() {
          stopPing();
          if (_evtSource) { _evtSource.close(); _evtSource = null; }
          updateConnectionState('disconnected');
          scheduleReconnect();
        };

        _evtSource.onmessage = function(e) {
          try {
            const data = JSON.parse(e.data);
            const eventsToProcess = data.type === 'batch' ? data.events : [data];

            let needsListRender = false;
            let needsListFetch = false;

            for (const evt of eventsToProcess) {
              if (evt.type === 'record_updated' || evt.type === 'object_updated') {
                const updatedId = String(evt.data ? (evt.data.id || evt.data.oid) : '');
                if (evt.data && (evt.data.has_flags !== undefined || evt.data.review_status !== undefined)) {
                  const listItem = objectList.find(o => String(o.id) === updatedId);
                  if (listItem) {
                    Object.assign(listItem, evt.data);
                    if (!document.getElementById('listView').classList.contains('hidden')) {
                      needsListRender = true;
                    }
                  }
                  if (currentRecord && String(currentRecord.id) === updatedId) {
                    Object.assign(currentRecord, evt.data);
                    if (evt.data.review_status) isReviewed = (evt.data.review_status === 'reviewed');
                    updateReviewButtonUI();
                  }
                } else {
                  if (!document.getElementById('listView').classList.contains('hidden')) {
                    needsListFetch = true;
                  } else if (currentRecord && String(currentRecord.id) === updatedId) {
                    apiFetch(`/api/object/${encodeURIComponent(updatedId)}`).then(freshData => {
                      if (currentOid === updatedId) {
                        currentRecord = freshData;
                        isReviewed = (freshData.review_status === 'reviewed');
                        updateReviewButtonUI();
                      }
                    }).catch(() => {});
                  }
                }
              } else if (evt.type === 'presence_updated' && evt.data) {
                const updatedOid = String(evt.data.oid || '');
                if (currentOid && String(currentOid) === updatedOid) {
                  const totalViewers = evt.data.viewers_count || 0;
                  const otherCount = Math.max(0, totalViewers - 1);
                  updatePresenceBanner(otherCount);
                }
              } else if (evt.type === 'session_ended') {
                showSessionEndedOverlay();
              } else if (evt.type === 'push_navigation') {
                showPushNavigationOverlay(evt.data.id);
              } else if (evt.type === 'filter_synced') {
                const payload = evt.data;
                searchQuery = payload.q || "";
                const searchBox = document.getElementById('searchBox');
                if (searchBox) searchBox.value = searchQuery;

                const searchClearBtn = document.getElementById('searchClearBtn');
                if (searchClearBtn) {
                  if (searchQuery) searchClearBtn.classList.remove('hidden');
                  else searchClearBtn.classList.add('hidden');
                }

                activeAdvancedFilters.locations = payload.locations || {};
                activeAdvancedFilters.problems = payload.specific_problems || [];

                noImageFilterActive = payload.no_image || false;
                const noImagePill = document.getElementById('pill-no-image');
                if (noImagePill) {
                  if (noImageFilterActive) {
                    noImagePill.className = 'px-3 py-1 rounded-[2px] font-sans text-xs font-medium whitespace-nowrap border flex items-center gap-1.5 transition-colors bg-ink text-white border-ink';
                  } else {
                    noImagePill.className = 'px-3 py-1 rounded-[2px] font-sans text-xs font-medium whitespace-nowrap border flex items-center gap-1.5 transition-colors bg-surface text-ink-muted border-bordercol hover:bg-tonal1';
                  }
                }

                setStatusFilter(payload.status || 'all').then(() => {
                  showToast("📱 Synced batch with Desktop (" + objectList.length + " matching records)");
                });

                if (!document.getElementById('detailView').classList.contains('hidden')) {
                  showListView(false);
                }
              }
            }

            if (needsListFetch) {
              fetchList();
            } else if (needsListRender) {
              renderList();
            }

          } catch(err) {}
        };
      } catch(err) {
        updateConnectionState('disconnected');
      }
    }

    function showPushNavigationOverlay(oid) {
      const existing = document.getElementById('pushNavOverlay');
      if (existing) existing.remove();

      const overlay = document.createElement('div');
      overlay.id = 'pushNavOverlay';
      overlay.className = 'fixed bottom-4 left-4 right-4 z-[100] flex flex-col bg-surface border border-bordercol rounded-xl shadow-2xl p-4 transform transition-all';
      overlay.innerHTML = `
        <div class="flex items-start gap-3">
          <div class="flex-shrink-0 flex items-center justify-center w-10 h-10 bg-lake-light text-lake-dark rounded-full">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <div class="flex-1">
            <h2 class="text-base font-serif font-bold text-ink mb-1">Object Pushed: ${oid}</h2>
            <p class="font-sans text-sm text-ink-muted mb-3">
              The desktop app sent this object. View it now?
            </p>
            <div class="flex gap-2">
              <button id="btnDeclinePush" class="flex-1 py-2 px-3 bg-canvas text-ink-muted font-sans font-bold text-xs rounded-[2px] border border-bordercol touch-press touch-target-min">
                Decline
              </button>
              <button id="btnAcceptPush" class="flex-1 py-2 px-3 bg-fern text-white font-sans font-bold text-xs rounded-[2px] touch-press touch-target-min">
                View Object
              </button>
            </div>
          </div>
        </div>
      `;
      document.body.appendChild(overlay);

      document.getElementById('btnDeclinePush').addEventListener('click', () => {
        overlay.remove();
      });

      document.getElementById('btnAcceptPush').addEventListener('click', () => {
        overlay.remove();
        loadSpecimen(oid);
      });
    }

    function showSessionEndedOverlay() {
      // Close active SSE connection
      if (_evtSource) {
        _evtSource.close();
        _evtSource = null;
      }

      const overlay = document.createElement('div');
      overlay.className = 'fixed inset-0 z-[100] flex flex-col items-center justify-center bg-surface px-6 text-center';
      overlay.innerHTML = `
        <div class="mb-6 rounded-full bg-ember-light p-4">
          <svg class="h-10 w-10 text-ember-dark" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
        <h2 class="font-serif text-2xl font-bold text-ink mb-2">Session Ended</h2>
        <p class="font-sans text-ink-muted mb-8 max-w-sm">
          The desktop application has closed this session.
          To continue editing, start a new session on your desktop.
        </p>
        <button onclick="window.location.reload()" class="w-full max-w-[200px] py-3.5 px-4 rounded-[2px] font-sans font-bold text-sm bg-fern text-white border-2 border-fern-dark shadow-md touch-target-min touch-press">
          Refresh & Try Again
        </button>
      `;
      document.body.appendChild(overlay);
    }

    function updateWakeLockUI(active) {
      const btn = document.getElementById('btnWakeLock');
      const icon = document.getElementById('wakeLockIcon');
      if (!btn || !icon) return;
      if (active) {
        btn.className = 'p-2 rounded-[2px] border transition-all touch-target-min bg-amber-400 text-black border-amber-600 ring-2 ring-amber-300 shadow-xs font-bold flex items-center justify-center';
        icon.innerText = '☀️';
        icon.classList.add('animate-spin-slow');
      } else {
        btn.className = 'p-2 rounded-[2px] border transition-colors touch-target-min bg-ink text-surface border-ink hover:bg-ink-muted flex items-center justify-center';
        icon.innerText = '🌙';
        icon.classList.remove('animate-spin-slow');
      }
    }

    async function acquireWakeLock(silent = false) {
      if (!('wakeLock' in navigator)) {
        if (!silent) showToast('Wake Lock API not supported on this browser', true);
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
          if (!isWalkModeWanted) {
            updateWakeLockUI(false);
          }
        });
        if (!silent) showToast('Walk Mode Active (Screen Sleep Prevented)');
        return true;
      } catch (err) {
        if (!silent) showToast('Wake Lock unavailable on this device', true);
        return false;
      }
    }

    async function releaseWakeLock(silent = false) {
      isWalkModeWanted = false;
      try { localStorage.setItem('arbor_walk_mode', 'false'); } catch (e) {}
      if (wakeLockSentinel) {
        try {
          await wakeLockSentinel.release();
        } catch (e) {}
        wakeLockSentinel = null;
      }
      updateWakeLockUI(false);
      if (!silent) showToast('Walk Mode Deactivated (Sleep Allowed)');
    }

    async function toggleWakeLock() {
      if (isWalkModeWanted || wakeLockSentinel) {
        await releaseWakeLock();
      } else {
        isWalkModeWanted = true;
        try { localStorage.setItem('arbor_walk_mode', 'true'); } catch (e) {}
        await acquireWakeLock();
      }
    }

    // ==========================================
    // SPECIMEN LIST RENDERING & SEARCH
    // ==========================================
    function debounceSearch() {
      clearTimeout(searchDebounceTimer);
      searchQuery = document.getElementById('searchBox').value.trim();
      const clearBtn = document.getElementById('searchClearBtn');
      if (searchQuery) clearBtn.classList.remove('hidden');
      else clearBtn.classList.add('hidden');
      const detailView = document.getElementById('detailView');
      if (detailView && !detailView.classList.contains('hidden')) {
        showListView(false);
      }
      searchDebounceTimer = setTimeout(fetchList, 350);
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
      document.getElementById('searchBox').value = '';
      document.getElementById('searchClearBtn').classList.add('hidden');
      searchQuery = '';
      const detailView = document.getElementById('detailView');
      if (detailView && !detailView.classList.contains('hidden')) {
        showListView(false);
      }
      fetchList();
    }

    function renderStatusBadge(item) {
      if (!item) return '';
      const isRev = (item.review_status === 'reviewed') || (item.reviewed === true) || (item.is_reviewed === true);
      const hasFlags = Boolean(item.has_flags);
      const problemsHaveHistory = Boolean(item.problems_have_history !== undefined ? item.problems_have_history : item.has_history);
      const hasUnknown = Boolean(item.has_unknown);

      let label, bg, fg, border, icon;
      if (isRev && hasFlags) {
        label = 'REV+ERR';
        bg = '#F57C00';
        fg = '#ffffff';
        border = '#F57C00';
        icon = '⚠';
      } else if (isRev) {
        label = 'OK';
        bg = '#2E7D32';
        fg = '#ffffff';
        border = '#2E7D32';
        icon = '✓';
      } else if (hasFlags && problemsHaveHistory) {
        label = 'ERR+HIS';
        bg = '#7B1FA2';
        fg = '#ffffff';
        border = '#7B1FA2';
        icon = '⚠';
      } else if (hasFlags) {
        label = 'ERR';
        bg = '#C62828';
        fg = '#ffffff';
        border = '#C62828';
        icon = '⚠';
      } else if (problemsHaveHistory) {
        label = 'CFCT';
        bg = '#0284C7';
        fg = '#ffffff';
        border = '#0284C7';
        icon = '🔀';
      } else if (hasUnknown) {
        label = 'UKN';
        bg = '#FBC02D';
        fg = '#2c302e';
        border = '#FBC02D';
        icon = '?';
      } else {
        label = 'UNREV';
        bg = '#45475a';
        fg = '#ffffff';
        border = '#45475a';
        icon = '🕒';
      }

      return `<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-[2px] text-[10px] font-sans font-semibold" style="background-color: ${bg}; color: ${fg}; border: 1px solid ${border};">${icon} ${label}</span>`;
    }

    function setStatusFilter(status) {
      activeStatusFilter = status;
      const filterStyles = {
        all: {
          active: 'bg-ink text-white border-ink font-semibold',
          inactive: 'bg-surface text-ink-muted border-bordercol hover:bg-tonal1'
        },
        pending: {
          active: 'bg-[#45475a] text-white border-[#45475a] shadow-xs font-semibold',
          inactive: 'bg-surface text-ink-muted border-bordercol hover:bg-tonal1'
        },
        flagged: {
          active: 'bg-[#C62828] text-white border-[#C62828] shadow-xs font-semibold',
          inactive: 'bg-ember-light text-ember-dark border-ember-border hover:bg-ember-light/80'
        },
        reviewed: {
          active: 'bg-[#2E7D32] text-white border-[#2E7D32] shadow-xs font-semibold',
          inactive: 'bg-fern-light text-fern-dark border-fern-border hover:bg-fern-light/80'
        },
        conflict: {
          active: 'bg-[#0284C7] text-white border-[#0284C7] shadow-xs font-semibold',
          inactive: 'bg-[#e0f2fe] text-[#0369a1] border-[#bae6fd] hover:bg-[#bae6fd]'
        },
        unknown: {
          active: 'bg-[#FBC02D] text-[#2c302e] border-[#FBC02D] shadow-xs font-semibold',
          inactive: 'bg-[#fef9c3] text-[#854d0e] border-[#fde047] hover:bg-[#fef08a]'
        }
      };

      ['all', 'pending', 'flagged', 'reviewed', 'conflict', 'unknown'].forEach(s => {
        const pill = document.getElementById(`pill-${s}`);
        if (!pill) return;
        const isSelected = (s === status);
        const styleRule = filterStyles[s] || filterStyles.all;
        pill.className = `min-h-[44px] px-3.5 py-2 rounded-[2px] font-sans text-xs font-medium whitespace-nowrap border transition-colors touch-press flex items-center justify-center gap-1.5 ${isSelected ? styleRule.active : styleRule.inactive}`;
      });
      return fetchList();
    }

    function handleSortChange() {
      activeSortBy = document.getElementById('sortBySelect').value;
      renderList();
    }

    function toggleNoImageFilter() {
      noImageFilterActive = !noImageFilterActive;
      const pill = document.getElementById('pill-no-image');
      if (noImageFilterActive) {
        pill.className = 'px-3 py-1 rounded-[2px] font-sans text-xs font-medium whitespace-nowrap border flex items-center gap-1.5 transition-colors bg-ink text-white border-ink';
      } else {
        pill.className = 'px-3 py-1 rounded-[2px] font-sans text-xs font-medium whitespace-nowrap border flex items-center gap-1.5 transition-colors bg-surface text-ink-muted border-bordercol hover:bg-tonal1';
      }
      fetchList();
    }

    function cycleTriState(btn) {
      const row = btn.closest('[data-prob-name]');
      if (!row) return;
      const pName = row.getAttribute('data-prob-name');
      const currState = row.getAttribute('data-state') || 'ignore';
      let nextState = 'ignore';
      if (currState === 'ignore') nextState = 'has';
      else if (currState === 'has') nextState = 'not';
      else nextState = 'ignore';

      row.setAttribute('data-state', nextState);
      updateTriStateVisual(row, nextState);
    }

    function updateTriStateVisual(row, state) {
      const badge = row.querySelector('.tristate-badge');
      const icon = row.querySelector('.tristate-icon');
      if (!badge || !icon) return;

      if (state === 'has') {
        row.className = 'flex items-center justify-between p-2.5 rounded-[2px] border border-fern bg-fern-light/30 transition-colors cursor-pointer touch-press';
        badge.className = 'tristate-badge px-2.5 py-1 text-[11px] font-bold rounded-[2px] bg-fern text-white shadow-xs';
        badge.textContent = 'HAS (✓)';
        icon.textContent = '✓';
        icon.className = 'tristate-icon text-sm font-bold text-fern';
      } else if (state === 'not') {
        row.className = 'flex items-center justify-between p-2.5 rounded-[2px] border border-ember bg-ember-light/30 transition-colors cursor-pointer touch-press';
        badge.className = 'tristate-badge px-2.5 py-1 text-[11px] font-bold rounded-[2px] bg-ember text-white shadow-xs';
        badge.textContent = 'NOT (−)';
        icon.textContent = '−';
        icon.className = 'tristate-icon text-sm font-bold text-ember';
      } else {
        row.className = 'flex items-center justify-between p-2.5 rounded-[2px] border border-bordercol bg-surface hover:bg-tonal1 transition-colors cursor-pointer touch-press';
        badge.className = 'tristate-badge px-2.5 py-1 text-[11px] font-bold rounded-[2px] bg-tonal2 text-ink-muted';
        badge.textContent = 'IGNORE';
        icon.textContent = '□';
        icon.className = 'tristate-icon text-sm font-normal text-ink-faint';
      }
    }

    function openFilterModal() {
      // Populate Location Filters
      const locContainer = document.getElementById('filterModalLocations');
      locContainer.innerHTML = '';
      if (activeSchema && activeSchema.ui_sections && activeSchema.ui_sections.location) {
        activeSchema.ui_sections.location.forEach(field => {
          if (field.type === 'checkbox') return; // Skip bool locations for simplicity

          let inputHtml = '';
          if (field.type === 'choice' && field.choices) {
            inputHtml = `
              <select id="filter_loc_${field.name}" class="w-full bg-surface border border-bordercol rounded-[2px] px-2.5 py-1.5 text-xs font-sans text-ink outline-none focus:border-fern cursor-pointer">
                <option value="">Any ${field.name}</option>
                ${field.choices.map(c => `<option value="${c}" ${activeAdvancedFilters.locations[field.name] === c ? 'selected' : ''}>${c}</option>`).join('')}
              </select>
            `;
          } else {
            inputHtml = `
              <input type="text" id="filter_loc_${field.name}" placeholder="Any ${field.name}..." value="${activeAdvancedFilters.locations[field.name] || ''}" class="w-full bg-surface border border-bordercol rounded-[2px] px-2.5 py-1.5 text-xs font-sans text-ink placeholder:text-ink-faint outline-none focus:border-fern" />
            `;
          }

          locContainer.innerHTML += `
            <div>
              <label class="block text-[11px] font-bold text-ink-muted mb-1">${field.name}</label>
              ${inputHtml}
            </div>
          `;
        });
      }

      // Populate Specific Problems & History with Tri-State Controls
      const probContainer = document.getElementById('filterModalProblems');
      probContainer.innerHTML = '';

      // Static items
      let staticProblems = [
        { name: "Any_Problem", label: "Any problem (all flags)" },
        { name: "Historical_Data", label: "Historical Data (Has / No History)" },
        { name: "Images_Missing", label: "Missing Images" }
      ];

      let dynamicProblems = [];
      if (activeSchema && activeSchema.ui_sections && activeSchema.ui_sections.problems) {
        dynamicProblems = activeSchema.ui_sections.problems.map(p => {
          return { name: p.name, label: p.name.replace('_Problem', '').replace(/_/g, ' ') };
        });
      }

      const allProblems = staticProblems.concat(dynamicProblems);

      allProblems.forEach(p => {
        const currState = (activeAdvancedFilters.problems && activeAdvancedFilters.problems[p.name]) || 'ignore';
        probContainer.innerHTML += `
          <div
            data-prob-name="${p.name}"
            data-state="${currState}"
            onclick="cycleTriState(this)"
            class="flex items-center justify-between p-2.5 rounded-[2px] border border-bordercol bg-surface hover:bg-tonal1 transition-colors cursor-pointer touch-press"
          >
            <div class="flex items-center gap-2.5">
              <span class="tristate-icon text-sm text-ink-faint font-mono">□</span>
              <span class="text-xs font-sans font-medium text-ink">${p.label}</span>
            </div>
            <span class="tristate-badge px-2.5 py-1 text-[11px] font-bold rounded-[2px] bg-tonal2 text-ink-muted">IGNORE</span>
          </div>
        `;
      });

      // Apply initial visual state styling
      probContainer.querySelectorAll('[data-prob-name]').forEach(row => {
        const st = row.getAttribute('data-state') || 'ignore';
        updateTriStateVisual(row, st);
      });

      openModal('filterModal');
    }

    function closeFilterModal() {
      closeModal('filterModal');
    }

    function updateFilterIndicator() {
      const badge = document.getElementById('filterActiveBadge');
      const btn = document.getElementById('btnFilterModalTrigger');
      if (!badge) return;
      const hasLocs = activeAdvancedFilters.locations && Object.values(activeAdvancedFilters.locations).some(v => Boolean(v && String(v).trim()));
      const hasProbs = activeAdvancedFilters.problems && Object.keys(activeAdvancedFilters.problems).length > 0;
      const isActive = hasLocs || hasProbs;
      if (isActive) {
        badge.classList.remove('hidden');
        if (btn) {
          btn.classList.add('border-fern', 'bg-fern-light/40', 'text-fern-dark');
        }
      } else {
        badge.classList.add('hidden');
        if (btn) {
          btn.classList.remove('border-fern', 'bg-fern-light/40', 'text-fern-dark');
        }
      }
    }

    function applyAdvancedFilters() {
      // Gather Locations
      activeAdvancedFilters.locations = {};
      if (activeSchema && activeSchema.ui_sections && activeSchema.ui_sections.location) {
        activeSchema.ui_sections.location.forEach(field => {
          if (field.type === 'checkbox') return;
          const el = document.getElementById(`filter_loc_${field.name}`);
          if (el && el.value.trim()) {
            activeAdvancedFilters.locations[field.name] = el.value.trim();
          }
        });
      }

      // Gather Problems with tri-state
      activeAdvancedFilters.problems = {};
      const probRows = document.querySelectorAll('#filterModalProblems [data-prob-name]');
      probRows.forEach(row => {
        const pName = row.getAttribute('data-prob-name');
        const pState = row.getAttribute('data-state');
        if (pName && (pState === 'has' || pState === 'not')) {
          activeAdvancedFilters.problems[pName] = pState;
        }
      });

      updateFilterIndicator();
      closeFilterModal();
      fetchList();
    }

    function clearAdvancedFilters() {
      activeAdvancedFilters = { locations: {}, problems: {} };
      if (activeSchema && activeSchema.ui_sections && activeSchema.ui_sections.location) {
        activeSchema.ui_sections.location.forEach(field => {
          const el = document.getElementById(`filter_loc_${field.name}`);
          if (el) el.value = '';
        });
      }
      const probRows = document.querySelectorAll('#filterModalProblems [data-prob-name]');
      probRows.forEach(row => {
        row.setAttribute('data-state', 'ignore');
        updateTriStateVisual(row, 'ignore');
      });

      updateFilterIndicator();
      closeFilterModal();
      fetchList();
    }

    async function fetchList() {
      try {
        let url = `/api/objects?limit=150&q=${encodeURIComponent(searchQuery)}`;
        if (activeStatusFilter !== 'all') {
          url += `&status=${encodeURIComponent(activeStatusFilter)}`;
        }
        if (activeQuickCabinet) {
          url += `&cabinet=${encodeURIComponent(activeQuickCabinet)}`;
        }
        if (activeQuickShelf) {
          url += `&shelf=${encodeURIComponent(activeQuickShelf)}`;
        }

        // Append Location Filters
        for (const [key, val] of Object.entries(activeAdvancedFilters.locations || {})) {
          url += `&loc_${encodeURIComponent(key)}=${encodeURIComponent(val)}`;
        }

        // Append Specific Problems (key:state serialized)
        const probEntries = [];
        for (const [pName, pState] of Object.entries(activeAdvancedFilters.problems || {})) {
          if (pState === 'has' || pState === 'not') {
            probEntries.push(`${pName}:${pState}`);
          }
        }

        if (noImageFilterActive && !probEntries.some(p => p.startsWith('Images_Missing:'))) {
          probEntries.push('Images_Missing:has');
        }

        if (probEntries.length > 0) {
          url += `&specific_problems=${encodeURIComponent(probEntries.join(','))}`;
        }

        const res = await apiFetch(url);
        objectList = res.objects || [];

        // Update counts safely
        const facets = res.facets || {};
        const cabSel = document.getElementById('quickFilterCabinet');
        const shelfSel = document.getElementById('quickFilterShelf');
        if (cabSel && facets.cabinets && cabSel.options.length <= 1) {
          facets.cabinets.forEach(c => {
            const opt = document.createElement('option');
            opt.value = c;
            opt.textContent = `Cab ${c}`;
            if (activeQuickCabinet === c) opt.selected = true;
            cabSel.appendChild(opt);
          });
        }
        if (shelfSel && facets.shelves && shelfSel.options.length <= 1) {
          facets.shelves.forEach(s => {
            const opt = document.createElement('option');
            opt.value = s;
            opt.textContent = `Shelf ${s}`;
            if (activeQuickShelf === s) opt.selected = true;
            shelfSel.appendChild(opt);
          });
        }
        const revCount = facets.reviewed_count || 0;
        const pendCount = facets.pending_count || 0;
        const flaggedCount = facets.flagged_count !== undefined 
          ? facets.flagged_count 
          : objectList.filter(o => o.has_flags).length;
        const historyCount = facets.history_count !== undefined
          ? facets.history_count
          : objectList.filter(o => o.has_history).length;
        const unknownCount = facets.unknown_count !== undefined
          ? facets.unknown_count
          : objectList.filter(o => o.has_unknown).length;
        const total = res.total_matching !== undefined ? res.total_matching : objectList.length;

        document.getElementById('matchingCount').textContent = total;
        document.getElementById('pill-all').textContent = `All (${total})`;
        document.getElementById('pill-pending').innerHTML = `<span>🕒</span> <span>Unreviewed (${pendCount})</span>`;
        document.getElementById('pill-flagged').innerHTML = `<span>⚠</span> <span>Flagged (${flaggedCount})</span>`;
        document.getElementById('pill-reviewed').innerHTML = `<span>✓</span> <span>Reviewed (${revCount})</span>`;
        const pillConf = document.getElementById('pill-conflict');
        if (pillConf) pillConf.innerHTML = `<span>🔀</span> <span>Conflict (${historyCount})</span>`;
        const pillUkn = document.getElementById('pill-unknown');
        if (pillUkn) pillUkn.innerHTML = `<span>?</span> <span>Unknown (${unknownCount})</span>`;
        document.getElementById('connModalReviewed').textContent = `${revCount} / ${total} items`;

        renderList();
      } catch (err) {
        console.error("Failed to fetch specimen list:", err);
      }
    }

    // Substring-based highlight without regex escaping hazards
    function highlightMatch(text, query) {
      if (!query || !text) return text || '';
      const str = String(text);
      const q = query.trim().toLowerCase();
      if (!q) return str;
      const idx = str.toLowerCase().indexOf(q);
      if (idx === -1) return str;
      const match = str.substring(idx, idx + q.length);
      return str.substring(0, idx) + '<mark class="bg-ember-light text-ember font-semibold px-0.5 rounded-[1px]">' + match + '</mark>' + str.substring(idx + q.length);
    }

    function renderList() {
      const container = document.getElementById('specimenListContainer');
      if (objectList.length === 0) {
        container.innerHTML = `
          <div class="bg-surface border border-bordercol rounded-[2px] p-8 text-center mt-4">
            <span class="text-3xl text-ink-faint">🌿</span>
            <p class="font-serif font-bold text-base text-ink mt-2">No specimens match filter</p>
            <p class="font-sans text-xs text-ink-muted mt-1">If no database is currently loaded, please open an Excel database in Arbor Desktop.</p>
          </div>
        `;
        return;
      }

      // Sort in-place if requested
      const sorted = [...objectList].sort((a, b) => {
        if (activeSortBy === 'name-asc') return (a.scientific_name || '').localeCompare(b.scientific_name || '');
        if (activeSortBy === 'name-desc') return (b.scientific_name || '').localeCompare(a.scientific_name || '');
        if (activeSortBy === 'id-asc') return (a.id || '').localeCompare(b.id || '', undefined, { numeric: true });
        return 0; // default server order
      });

      container.innerHTML = sorted.map(s => {
        const statusBadge = renderStatusBadge(s);

        let locStr = [];
        if (s.location) {
          if (s.location.building) locStr.push(s.location.building);
          if (s.location.floor) locStr.push(`Fl ${s.location.floor}`);
          if (s.location.cabinet) locStr.push(`Cab ${s.location.cabinet}`);
          if (s.location.stored_as) locStr.push(s.location.stored_as);
        }
        const locDisplay = locStr.join(' • ') || 'Location unrecorded';

        return `
          <div
            onclick="loadSpecimen('${s.id}')"
            class="bg-surface border border-bordercol hover:border-borderdark rounded-[2px] p-3.5 transition-all cursor-pointer touch-press shadow-xs"
          >
            <div class="flex items-center justify-between mb-1.5">
              <div class="flex items-center gap-1.5">
                <span class="font-mono text-xs font-bold text-ink-muted">
                  ${highlightMatch(s.accession_number || s.id, searchQuery)}
                </span>
                ${s.family ? `<span class="font-sans text-[10px] text-ink-faint bg-tonal1 px-1.5 py-0.2 rounded-[1px] border border-tonal3">${highlightMatch(s.family, searchQuery)}</span>` : ''}
              </div>
              <div class="flex items-center gap-1">
                ${s.has_flags ? '<span class="px-1.5 py-0.5 rounded text-[10px] font-bold bg-amber-50 text-amber-800 border border-amber-300">Taxon Issue ⚠</span>' : ''}
                ${(s.review_status === 'reviewed' || s.reviewed) ? 
                  '<span class="px-1.5 py-0.5 rounded text-[10px] font-bold bg-emerald-50 text-fern-dark border border-fern/30">Reviewed ✓</span>' : 
                  '<span class="px-1.5 py-0.5 rounded text-[10px] font-bold bg-stone-100 text-stone-600 border border-stone-300">Pending</span>'
                }
                ${s.has_unvalidated ? `<span class="inline-flex items-center px-1.5 py-0.5 rounded-[2px] text-[10px] font-bold bg-amber-500/20 text-amber-600 dark:text-amber-400 border border-amber-500/40">UNVAL</span>` : ''}
              </div>
            </div>

            <h2 class="font-serif italic font-bold text-base text-ink leading-snug">
              ${highlightMatch(s.scientific_name, searchQuery)}
            </h2>

            <div class="flex items-center gap-2 text-xs font-sans text-ink-muted mt-0.5">
              ${s.author ? `<span class="text-ink font-medium">${highlightMatch(s.author, searchQuery)}</span>` : ''}
              ${s.collector ? `<span>•</span> <span class="truncate max-w-[140px]">👤 ${highlightMatch(s.collector, searchQuery)}</span>` : ''}
            </div>

            <div class="flex items-center justify-between mt-2.5 pt-2 border-t border-tonal2 text-xs">
              <div class="flex items-center gap-1.5 text-ink truncate max-w-[240px]">
                <span class="text-fern text-xs">📍</span>
                <span class="font-mono text-[11px] text-ink-muted truncate">${locDisplay}</span>
              </div>
              <div class="flex items-center gap-1 text-[11px] font-sans font-medium text-fern shrink-0">
                <span>Inspect</span>
                <span>&gt;</span>
              </div>
            </div>
          </div>
        `;
      }).join('');

      prefetchVisibleHistory(sorted);
    }

    async function prefetchVisibleHistory(list) {
      // Pre-fetch the first 10 items in background
      const limit = Math.min(10, list.length);
      for (let i = 0; i < limit; i++) {
        const item = list[i];
        if (!item || !item.id) continue;

        try {
          const cachedData = await getCachedHistoricalData(item.id);
          if (!cachedData) {
            // Not in cache, fetch and store
            const res = await apiFetch(`/api/object/${encodeURIComponent(item.id)}/history`);
            if (res && res.historical_data) {
              cacheHistoricalData(item.id, res.historical_data);
            }
          }
        } catch (err) {
          console.error(`Failed to prefetch history for ${item.id}`, err);
        }
      }
    }

    async function showListView(manageHistory = true) {
      if (presenceHeartbeatTimer) {
        clearInterval(presenceHeartbeatTimer);
        presenceHeartbeatTimer = null;
      }
      sendPresence(null);
      updatePresenceBanner(0);

      if (autoSaveTimer !== null) {
        clearTimeout(autoSaveTimer);
        autoSaveTimer = null;
        if (currentOid) {
          await saveCurrentEdits();
        }
      }

      // If triggered from top-left UI back button while in detail view, pop history
      if (manageHistory && window.history.state && window.history.state.view === 'detail') {
        window.history.back();
        return;
      }

      document.getElementById('detailView').classList.add('hidden');
      document.getElementById('listView').classList.remove('hidden');
      fetchList();
    }

    function showDetailView() {
      document.getElementById('listView').classList.add('hidden');
      document.getElementById('detailView').classList.remove('hidden');
    }

    // ==========================================
    // SPECIMEN DETAIL VIEW & DYNAMIC FORM ENGINE
    // ==========================================
    async function loadSpecimen(oid, fromHistory = false) {
      // Flush any pending debounced save for the outgoing specimen BEFORE currentOid changes.
      // Without this, navigating via prev/next saves the old form data under the new specimen's OID.
      if (autoSaveTimer !== null) {
        clearTimeout(autoSaveTimer);
        autoSaveTimer = null;
        if (currentOid && currentOid !== oid) {
          await saveCurrentEdits();
        }
      }
      currentOid = oid;
      dirtyFields.clear();

      if (presenceHeartbeatTimer) clearInterval(presenceHeartbeatTimer);
      sendPresence(oid);
      presenceHeartbeatTimer = setInterval(() => {
        if (currentOid && !document.getElementById('detailView').classList.contains('hidden')) {
          sendPresence(currentOid);
        }
      }, 8000);

      if (!fromHistory) {
        if (window.history.state && window.history.state.view === 'detail') {
          window.history.replaceState({ view: 'detail', id: oid }, '');
        } else {
          window.history.pushState({ view: 'detail', id: oid }, '');
        }
      }

      showDetailView();

      // Reset scroll position to top
      document.querySelector('#detailView main').scrollTop = 0;

      // Update Nav Index
      const idx = objectList.findIndex(o => o.id === oid);
      if (idx !== -1) {
        document.getElementById('detailNavIndex').textContent = `${idx + 1} of ${objectList.length}`;
        document.getElementById('btnPrevSpecimen').disabled = (idx === 0);
        document.getElementById('btnNextSpecimen').disabled = (idx === objectList.length - 1);
      }

      // Set Instant Loading State (Clears stale specimen data)
      document.getElementById('detailAccession').textContent = `#${oid}`;
      document.getElementById('detailScientificName').innerHTML = '<span class="text-ink-muted animate-pulse font-serif italic">Loading specimen record...</span>';
      document.getElementById('detailAuthor').textContent = '';
      document.getElementById('detailFamily').textContent = '';
      document.getElementById('detailTopLocation').textContent = 'Location: Retrieving...';
      document.getElementById('detailReviewStatusBadge').innerHTML = '<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-[2px] text-[10px] font-sans font-medium bg-tonal2 text-ink-muted border border-bordercol animate-pulse">⏳ LOADING</span>';
      
      // Skeleton placeholders for accordions
      document.getElementById('detailAccordionsContainer').innerHTML = `
        <div class="bg-surface border border-bordercol rounded-[2px] p-4 space-y-3 animate-pulse">
          <div class="h-4 bg-tonal2 rounded-[2px] w-1/3"></div>
          <div class="h-9 bg-tonal1 rounded-[2px] w-full"></div>
          <div class="h-9 bg-tonal1 rounded-[2px] w-full"></div>
        </div>
      `;

      // Reset Photo State
      document.getElementById('photoPlaceholder').classList.remove('hidden');
      document.getElementById('specimenImg').classList.add('hidden');
      document.getElementById('photoWatermark').classList.add('hidden');
      document.getElementById('specimenImg').src = '';
      const thumbStrip = document.getElementById('photoThumbStrip');
      if (thumbStrip) {
        thumbStrip.classList.add('hidden');
        thumbStrip.innerHTML = '';
      }

      // Hide Undo button on explicit specimen navigation
      const undoBtn = document.getElementById('btnMobileUndo');
      if (undoBtn) {
          undoBtn.classList.add('hidden');
          undoBtn.classList.remove('flex');
      }

      try {
        const data = await apiFetch(`/api/object/${encodeURIComponent(oid)}`);
        currentRecord = data;
        isReviewed = (data.review_status === 'reviewed');

        if (data.other_viewers_count !== undefined) {
          updatePresenceBanner(data.other_viewers_count);
        }

        // Top Summary Info
        document.getElementById('detailAccession').textContent = `#${data.accession_number || data.id}`;
        document.getElementById('detailScientificName').textContent = data.scientific_name || 'Specimen';
        document.getElementById('detailAuthor').textContent = data.registration ? (data.registration.Author || '') : '';
        document.getElementById('detailFamily').textContent = data.registration ? (data.registration.Family || '') : '';

        let locStr = [];
        if (data.observation) {
          if (data.observation.Building) locStr.push(data.observation.Building);
          if (data.observation.Floor) locStr.push(`Floor ${data.observation.Floor}`);
          if (data.observation.Cabinet) locStr.push(`Cab ${data.observation.Cabinet}`);
          if (data.observation["Stored as"]) locStr.push(data.observation["Stored as"]);
        }
        document.getElementById('detailTopLocation').textContent = locStr.length > 0 ? `Location: ${locStr.join(' • ')}` : 'Location: Unrecorded';

        updateReviewButtonUI();

        // Load Photos & Thumbnails
        photoUrls = (data.images && data.images.online_urls) ? data.images.online_urls : [];
        document.getElementById('photoCountBadge').textContent = `${photoUrls.length} available`;
        const mainContainer = document.getElementById('photoMainContainer');
        const placeholder = document.getElementById('photoPlaceholder');
        const specimenImg = document.getElementById('specimenImg');
        const watermark = document.getElementById('photoWatermark');

        // Reset to collapsed state
        mainContainer.classList.remove('h-52');
        mainContainer.classList.add('h-16');
        mainContainer.setAttribute('onclick', 'loadInitialPhoto()');
        const placeholderText = document.getElementById('photoPlaceholderText');

        if (photoUrls.length > 0) {
          currentPhotoIdx = 0;
          placeholder.innerHTML = `
            <span class="text-xl">📷</span>
            <p class="font-semibold text-fern" id="photoPlaceholderText">Tap to Load ${photoUrls.length} Archival Scan${photoUrls.length > 1 ? 's' : ''}</p>
          `;
          placeholder.classList.remove('hidden');
          specimenImg.classList.add('hidden');
          watermark.classList.add('hidden');
          mainContainer.classList.add('cursor-pointer');
          mainContainer.classList.remove('cursor-default');
          const strip = document.getElementById('photoThumbStrip');
          if (strip) { strip.classList.add('hidden'); strip.innerHTML = ''; }
        } else {
          placeholder.innerHTML = `
            <span class="text-xl text-ink-faint">📷</span>
            <p class="font-sans text-[11px] font-semibold text-ink-muted">No Archival Scans Attached</p>
          `;
          placeholder.classList.remove('hidden');
          specimenImg.classList.add('hidden');
          watermark.classList.add('hidden');
          mainContainer.classList.remove('cursor-pointer');
          mainContainer.classList.add('cursor-default');
          const strip = document.getElementById('photoThumbStrip');
          if (strip) { strip.classList.add('hidden'); strip.innerHTML = ''; }
        }

        // Render Dynamic Forms Driven by config.py
        currentUnvalidatedMap = {};
        if (data.unvalidated_sources && Array.isArray(data.unvalidated_sources)) {
          data.unvalidated_sources.forEach(u => {
            if (u.field) currentUnvalidatedMap[u.field] = u.comment || '';
          });
        }
        renderDynamicForm(activeSchema, data);

        // Update Problem Summary Banner
        const banner = document.getElementById('detailProblemBanner');
        const badgeContainer = document.getElementById('detailProblemBadges');
        const activeProbFields = [];
        const unknownFields = [];

        if (activeSchema && activeSchema.ui_sections) {
          const allFields = (activeSchema.ui_sections.registration || []).concat(activeSchema.ui_sections.location || []);
          allFields.forEach(f => {
            const val = (data.registration && data.registration[f.name] !== undefined) ? data.registration[f.name] : (data.observation ? data.observation[f.name] : '');
            if (isFieldProblemActive(f.name, 'registration', data) || isFieldProblemActive(f.name, 'observation', data)) {
              if (!activeProbFields.includes(f.name)) activeProbFields.push(f.name);
            } else if (isValueUnknown(val)) {
              if (!unknownFields.includes(f.name)) unknownFields.push(f.name);
            }
          });
        }

        if (activeProbFields.length > 0 || unknownFields.length > 0) {
          banner.classList.remove('hidden');
          let chipsHtml = '';
          activeProbFields.forEach(fName => {
            const inputId = `input_registration_${fName.replace(/[^a-zA-Z0-9_]/g, '_')}`;
            chipsHtml += `
              <button
                type="button"
                onclick="scrollToField('${inputId}', '${fName}')"
                class="px-2 py-1 bg-[#C62828] text-white text-[11px] font-bold rounded-[2px] shadow-xs flex items-center gap-1 touch-press hover:bg-[#b71c1c]"
                title="Jump to ${fName}"
              >
                <span>⚠</span>
                <span>${fName}</span>
              </button>
            `;
          });
          unknownFields.forEach(fName => {
            const inputId = `input_registration_${fName.replace(/[^a-zA-Z0-9_]/g, '_')}`;
            chipsHtml += `
              <button
                type="button"
                onclick="scrollToField('${inputId}', '${fName}')"
                class="px-2 py-1 bg-[#FBC02D] text-[#2c302e] text-[11px] font-bold rounded-[2px] shadow-xs flex items-center gap-1 touch-press hover:bg-[#f9a825]"
                title="Jump to ${fName}"
              >
                <span>?</span>
                <span>${fName}</span>
              </button>
            `;
          });
          badgeContainer.innerHTML = chipsHtml;
        } else {
          banner.classList.add('hidden');
          badgeContainer.innerHTML = '';
        }

        // Render Problems & Discrepancies
        renderDiscrepancies(data);

        // Fetch Historical Data
        revertState = {};
        fetchHistoricalData(oid);

      } catch (err) {
        console.error("Failed to load specimen details:", err);
        document.getElementById('detailScientificName').textContent = 'Error Loading Specimen';
        showToast('Failed to load specimen data from host', true);
      }
    }

    function navSpecimen(offset) {
      const idx = objectList.findIndex(o => o.id === currentOid);
      if (idx !== -1 && objectList[idx + offset]) {
        loadSpecimen(objectList[idx + offset].id);
      }
    }

    function isFieldProblemActive(fieldName, section, record) {
      if (!record) return false;
      const issues = record.flagged_issues || [];
      if (issues.some(iss => (iss.field === fieldName || iss.id === fieldName) && !iss.resolved)) {
        return true;
      }
      const obs = record.observation || {};
      const reg = record.registration || {};

      // 1. Direct Problem Column Check (e.g. Genus_Problem)
      const directProb = `${fieldName}_Problem`;
      if (obs[directProb] === true || String(obs[directProb]).toLowerCase() === 'true' || obs[directProb] === '1' ||
          reg[directProb] === true || String(reg[directProb]).toLowerCase() === 'true' || reg[directProb] === '1') {
        return true;
      }

      // 2. Mapped Problem Columns from Schema
      if (activeSchema && activeSchema.ui_sections && activeSchema.ui_sections.problems) {
        for (const p of activeSchema.ui_sections.problems) {
          const target = p.maps_to || p.target;
          if (target === fieldName || (!target && p.name.replace(/_Problem$/, '') === fieldName)) {
            const pVal = (obs[p.name] !== undefined) ? obs[p.name] : reg[p.name];
            if (pVal === true || String(pVal).toLowerCase() === 'true' || pVal === '1' || pVal === 'x') {
              return true;
            }
          }
        }
      }

      // 3. Location section general problem
      if (section === 'observation' && (obs.Loc_Problem === true || String(obs.Loc_Problem).toLowerCase() === 'true' || obs.Loc_Problem === '1')) {
        return true;
      }

      return false;
    }

    function isValueUnknown(val) {
      if (val === null || val === undefined) return false;
      const s = String(val).trim().toLowerCase();
      return ['ukjent', 'unknown', '?', '-', 'nan',
              'unknown:missing', 'unknown:indecipherable',
              'unknown:undigitized', 'withheld'].includes(s);
    }

    function scrollToField(inputId, fName) {
      let el = document.getElementById(inputId);
      if (!el && fName) {
        el = document.getElementById(`input_observation_${fName.replace(/[^a-zA-Z0-9_]/g, '_')}`);
      }
      if (el) {
        const accordion = el.closest('.accordion');
        if (accordion) {
          const content = accordion.querySelector('.acc-content');
          const icon = accordion.querySelector('.acc-icon');
          if (content && content.classList.contains('hidden')) {
            content.classList.remove('hidden');
            content.classList.add('block');
            accordion.classList.add('acc-open');
            if (icon) icon.textContent = '▲';
          }
        }
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        el.focus();
        el.classList.add('ring-2', 'ring-ember');
        setTimeout(() => el.classList.remove('ring-2', 'ring-ember'), 1500);
      }
    }

    async function toggleFieldProblem(fieldName) {
      if (!currentRecord) return;
      if (currentRecord.flagged_issues) {
        currentRecord.flagged_issues = currentRecord.flagged_issues.filter(i => i.field !== fieldName && i.id !== fieldName);
      }
      currentRecord.observation = currentRecord.observation || {};
      const probCol = `${fieldName}_Problem`;
      if (currentRecord.observation[probCol] !== undefined) {
        currentRecord.observation[probCol] = false;
      }
      if (activeSchema && activeSchema.ui_sections && activeSchema.ui_sections.problems) {
        for (const p of activeSchema.ui_sections.problems) {
          if (p.maps_to === fieldName || p.target === fieldName) {
            currentRecord.observation[p.name] = false;
          }
        }
      }
      if (fieldName === 'Location') {
        currentRecord.observation.Loc_Problem = false;
      }

      renderDynamicForm(activeSchema, currentRecord);
      renderDiscrepancies(currentRecord);
      updateReviewButtonUI();
      await saveCurrentEdits();
      showToast(`Resolved problem for ${fieldName}`);
    }

    // ==========================================
    // DYNAMIC SCHEMA-DRIVEN FORM GENERATOR
    // ==========================================
    function renderDynamicForm(schema, record) {
      const container = document.getElementById('detailAccordionsContainer');
      if (!schema || !schema.ui_sections) {
        container.innerHTML = '';
        return;
      }

      const uiSec = schema.ui_sections;
      const regGroups = uiSec.reg_groups || [];
      const regFields = uiSec.registration || [];
      const locFields = uiSec.location || [];

      let html = '';

      // 1. Render Registration Groups from config.py
      regGroups.forEach((grp, gIdx) => {
        const isTaxonomy = grp.name.toLowerCase().includes('tax');
        const icon = isTaxonomy ? '🧬' : (grp.name.toLowerCase().includes('collect') ? '📦' : (grp.name.toLowerCase().includes('obj') ? '🌿' : (grp.name.toLowerCase().includes('note') ? '📝' : '🔒')));

        let grpProbCount = 0;
        let grpUknCount = 0;
        let fieldsHtml = '';

        grp.fields.forEach(fName => {
          const fDef = regFields.find(f => f.name === fName) || { name: fName, type: 'text' };
          const val = (record.registration && record.registration[fName] !== undefined) ? record.registration[fName] : '';
          if (isFieldProblemActive(fName, 'registration', record)) grpProbCount++;
          else if (isValueUnknown(val)) grpUknCount++;
          fieldsHtml += renderFieldInput(fDef, val, 'registration', record);
        });

        const isOpen = (grpProbCount > 0 || grpUknCount > 0);

        let badgesHtml = '';
        if (grpProbCount > 0) {
          badgesHtml += `<span class="px-1.5 py-0.5 rounded-[2px] text-[11px] font-bold bg-[#C62828] text-white flex items-center gap-0.5 shadow-xs"><span>⚠</span><span>${grpProbCount}</span></span>`;
        }
        if (grpUknCount > 0) {
          badgesHtml += `<span class="px-1.5 py-0.5 rounded-[2px] text-[11px] font-bold bg-[#FBC02D] text-[#2c302e] flex items-center gap-0.5 shadow-xs"><span>?</span><span>${grpUknCount}</span></span>`;
        }

        html += `
          <div class="bg-surface border border-bordercol rounded-[2px] shadow-xs overflow-hidden accordion ${isOpen ? 'acc-open' : ''}">
            <button
              type="button"
              onclick="toggleAccordion(this)"
              class="w-full p-3 flex items-center justify-between bg-tonal1 hover:bg-tonal2 transition focus:outline-none touch-press border-b border-bordercol text-left"
            >
              <div class="flex items-center gap-2.5">
                <span class="text-base">${icon}</span>
                <div>
                  <div class="flex items-center gap-1.5">
                    <h3 class="font-bold text-xs text-ink uppercase tracking-wider">${grp.name}</h3>
                    ${badgesHtml}
                  </div>
                  <p class="text-[10px] text-ink-muted">${grp.fields.join(' • ')}</p>
                </div>
              </div>
              <span class="acc-icon text-ink-muted font-bold transition-transform duration-200 text-xs">${isOpen ? '▲' : '▼'}</span>
            </button>
            <div class="p-3.5 space-y-3 acc-content ${isOpen ? 'block' : 'hidden'}">
              ${fieldsHtml}
            </div>
          </div>
        `;
      });

      // Render any ungrouped registration fields (ensures 100% of schema fields are always editable)
      const groupedFieldNames = new Set(regGroups.flatMap(g => g.fields || []));
      const ungroupedFields = regFields.filter(f => !groupedFieldNames.has(f.name));
      if (ungroupedFields.length > 0) {
        let ungrpProbCount = 0;
        let ungrpUknCount = 0;
        let ungrpFieldsHtml = '';

        ungroupedFields.forEach(fDef => {
          const val = (record.registration && record.registration[fDef.name] !== undefined) ? record.registration[fDef.name] : '';
          if (isFieldProblemActive(fDef.name, 'registration', record)) ungrpProbCount++;
          else if (isValueUnknown(val)) ungrpUknCount++;
          ungrpFieldsHtml += renderFieldInput(fDef, val, 'registration', record);
        });

        const isUngrpOpen = (ungrpProbCount > 0 || ungrpUknCount > 0);
        let ungrpBadgesHtml = '';
        if (ungrpProbCount > 0) {
          ungrpBadgesHtml += `<span class="px-1.5 py-0.5 rounded-[2px] text-[11px] font-bold bg-[#C62828] text-white flex items-center gap-0.5 shadow-xs"><span>⚠</span><span>${ungrpProbCount}</span></span>`;
        }
        if (ungrpUknCount > 0) {
          ungrpBadgesHtml += `<span class="px-1.5 py-0.5 rounded-[2px] text-[11px] font-bold bg-[#FBC02D] text-[#2c302e] flex items-center gap-0.5 shadow-xs"><span>?</span><span>${ungrpUknCount}</span></span>`;
        }

        html += `
          <div class="bg-surface border border-bordercol rounded-[2px] shadow-xs overflow-hidden accordion ${isUngrpOpen ? 'acc-open' : ''}">
            <button
              type="button"
              onclick="toggleAccordion(this)"
              class="w-full p-3 flex items-center justify-between bg-tonal1 hover:bg-tonal2 transition focus:outline-none touch-press border-b border-bordercol text-left"
            >
              <div class="flex items-center gap-2.5">
                <span class="text-base">📋</span>
                <div>
                  <div class="flex items-center gap-1.5">
                    <h3 class="font-bold text-xs text-ink uppercase tracking-wider">Additional Fields</h3>
                    ${ungrpBadgesHtml}
                  </div>
                  <p class="text-[10px] text-ink-muted">${ungroupedFields.map(f => f.name).join(' • ')}</p>
                </div>
              </div>
              <span class="acc-icon text-ink-muted font-bold transition-transform duration-200 text-xs">${isUngrpOpen ? '▲' : '▼'}</span>
            </button>
            <div class="p-3.5 space-y-3 acc-content ${isUngrpOpen ? 'block' : 'hidden'}">
              ${ungrpFieldsHtml}
            </div>
          </div>
        `;
      }

      // 2. Render Physical Location Group from config.py
      if (locFields.length > 0) {
        let locFieldsHtml = '';
        let locProbCount = 0;
        let locUknCount = 0;

        locFields.forEach(fDef => {
          const val = (record.observation && record.observation[fDef.name] !== undefined) ? record.observation[fDef.name] : '';
          if (isFieldProblemActive(fDef.name, 'observation', record)) locProbCount++;
          else if (isValueUnknown(val)) locUknCount++;
          locFieldsHtml += renderFieldInput(fDef, val, 'observation', record);
        });

        const isLocOpen = (locProbCount > 0 || locUknCount > 0);

        let locBadgesHtml = '';
        if (locProbCount > 0) {
          locBadgesHtml += `<span class="px-1.5 py-0.5 rounded-[2px] text-[11px] font-bold bg-[#C62828] text-white flex items-center gap-0.5 shadow-xs"><span>⚠</span><span>${locProbCount}</span></span>`;
        }
        if (locUknCount > 0) {
          locBadgesHtml += `<span class="px-1.5 py-0.5 rounded-[2px] text-[11px] font-bold bg-[#FBC02D] text-[#2c302e] flex items-center gap-0.5 shadow-xs"><span>?</span><span>${locUknCount}</span></span>`;
        }

        let presetOptions = `<option value="Default" ${lastSelectedPreset === 'Default' ? 'selected' : ''}>Default</option>`;
        Object.keys(locationPresets).forEach(pName => {
          if (pName !== 'Default') {
            presetOptions += `<option value="${pName}" ${lastSelectedPreset === pName ? 'selected' : ''}>${pName}</option>`;
          }
        });

        html += `
          <div class="bg-surface border border-bordercol rounded-[2px] shadow-xs overflow-hidden accordion ${isLocOpen ? 'acc-open' : ''}">
            <button
              type="button"
              onclick="toggleAccordion(this)"
              class="w-full p-3 flex items-center justify-between bg-tonal1 hover:bg-tonal2 transition focus:outline-none touch-press border-b border-bordercol text-left"
            >
              <div class="flex items-center gap-2.5">
                <span class="text-base">📍</span>
                <div>
                  <div class="flex items-center gap-1.5">
                    <h3 class="font-bold text-xs text-ink uppercase tracking-wider">Physical Storage Location</h3>
                    ${locBadgesHtml}
                  </div>
                  <p class="text-[10px] text-ink-muted">Museum coordinates & storage trait</p>
                </div>
              </div>
              <span class="acc-icon text-ink-muted font-bold transition-transform duration-200 text-xs">${isLocOpen ? '▲' : '▼'}</span>
            </button>
            <div class="p-3.5 space-y-3 acc-content ${isLocOpen ? 'block' : 'hidden'}">
              <div class="flex items-center gap-2 mb-4">
                <select id="locPresetSelect" class="flex-grow bg-surface border border-bordercol rounded-[2px] px-2 py-1.5 text-xs font-sans text-ink outline-none focus:border-fern">
                  ${presetOptions}
                </select>
                <button type="button" onclick="applyLocPreset()" class="px-3 py-1.5 bg-tonal1 hover:bg-tonal2 text-ink text-xs font-bold rounded-[2px] border border-bordercol transition-colors cursor-pointer touch-press">
                  Apply Preset
                </button>
                <button type="button" onclick="openPresetSettings()" class="px-2 py-1.5 bg-surface hover:bg-tonal1 text-ink text-xs rounded-[2px] border border-bordercol transition-colors cursor-pointer touch-press" title="Preset Settings">
                  ⚙️
                </button>
              </div>
              ${locFieldsHtml}
            </div>
          </div>
        `;
      }

      container.innerHTML = html;
    }

    function renderFieldInput(field, value, section, record) {
      const fName = field.name;
      const fType = field.type || 'text';
      const isReadOnly = !!field.readonly;
      const inputId = `input_${section}_${fName.replace(/[^a-zA-Z0-9_]/g, '_')}`;

      const toggleBtnId = `history_toggle_${fName.replace(/[^a-zA-Z0-9_]/g, '_')}`;
      const containerId = `history_container_${fName.replace(/[^a-zA-Z0-9_]/g, '_')}`;

      const hasProb = isFieldProblemActive(fName, section, record);
      const hasUkn = isValueUnknown(value);

      const problemBadge = hasProb
        ? `<span class="inline-flex items-center justify-center px-1.5 py-0.2 rounded-[2px] text-[10px] font-bold bg-[#C62828] text-white shadow-xs ml-1" title="Problem Flagged">⚠</span>`
        : (hasUkn
          ? `<span class="inline-flex items-center justify-center px-1.5 py-0.2 rounded-[2px] text-[10px] font-bold bg-[#FBC02D] text-[#2c302e] shadow-xs ml-1" title="Unknown Value">?</span>`
          : '');

      const inputStyle = hasProb
        ? 'border-l-4 border-l-[#C62828] bg-ember-light border-ember text-ember-dark font-medium focus:border-ember'
        : (hasUkn
          ? 'border-l-4 border-l-[#FBC02D] bg-[#fef9c3] border-[#fde047] text-[#854d0e] font-medium focus:border-[#eab308]'
          : 'border-bordercol bg-surface text-ink focus:border-fern');

      const flagBtn = hasProb
        ? `<button
            type="button"
            onclick="toggleFieldProblem('${fName}')"
            class="min-h-[44px] px-2.5 py-1.5 text-xs font-sans font-bold text-white bg-[#C62828] hover:bg-[#b71c1c] border border-[#C62828] rounded-[2px] touch-target-min touch-press ml-1 flex items-center gap-1 shadow-xs"
            title="Problem active for ${fName} (tap to resolve)"
          >
            <span>⚑</span>
            <span>Flagged</span>
          </button>`
        : `<button
            type="button"
            onclick="openAddDiscrepancyModal('${fName}')"
            class="min-h-[44px] px-2.5 py-1.5 text-xs font-sans font-medium text-ink-muted hover:text-ember bg-tonal1 hover:bg-tonal2 border border-bordercol rounded-[2px] touch-target-min touch-press ml-1 flex items-center gap-1"
            title="Flag discrepancy for ${fName}"
          >
            <span>⚑</span>
            <span>Flag</span>
          </button>`;

      const icedigBtn = `
        <button
          type="button"
          onclick="openIcedigBottomSheet('${section}', '${fName}')"
          class="min-h-[44px] px-2.5 py-1.5 text-xs font-sans font-medium text-ink-muted hover:text-amber-700 bg-tonal1 hover:bg-amber-500/10 border border-bordercol rounded-[2px] touch-target-min touch-press ml-1 flex items-center gap-1"
          title="Set ICEDIG Missing Data Status for ${fName}"
        >
          <span>∅</span>
          <span>Unknown</span>
        </button>
      `;

      const historyControls = `
        <button
          type="button"
          id="${toggleBtnId}"
          onclick="toggleHistoryContainer('${fName}')"
          class="hidden min-h-[44px] px-2.5 py-1.5 text-xs font-sans font-medium text-ember bg-ember-light border border-ember-border rounded-[2px] touch-target-min touch-press ml-1 flex items-center gap-1"
          title="View historical value suggestions"
        >
          <span>📖</span>
          <span>History</span>
        </button>
        ${!isReadOnly ? flagBtn : ''}
        ${!isReadOnly && fType !== 'checkbox' && fType !== 'bool' ? icedigBtn : ''}
      `;

      const historyContainerHtml = `
        <div id="${containerId}" class="hidden mt-2 p-2.5 bg-tonal1 border border-bordercol rounded-[2px] shadow-xs">
           <!-- History suggestions injected here -->
        </div>
      `;

      // Choice / Select
      if (fType === 'choice' && Array.isArray(field.choices)) {
        const optionsHtml = ['<option value="">Select option...</option>']
          .concat(field.choices.map(c => `<option value="${c}" ${String(value) === String(c) ? 'selected' : ''}>${c}</option>`))
          .join('');

        return `
          <div class="space-y-1">
            <div class="flex items-center justify-between min-h-[32px]">
              <label for="${inputId}" class="text-xs font-bold text-ink flex items-center gap-1">
                <span>${fName}</span>
                ${problemBadge}
              </label>
              <div class="flex items-center">${historyControls}</div>
            </div>
            <select
              id="${inputId}"
              data-section="${section}"
              data-field="${fName}"
              onchange="markDirty('${fName}'); triggerAutoSave()" onblur="saveCurrentEdits()"
              class="w-full min-h-[44px] border rounded-[2px] px-3 py-2 text-xs outline-none cursor-pointer ${inputStyle}"
            >
              ${optionsHtml}
            </select>
            ${historyContainerHtml}
          </div>
        `;
      }

      // Checkbox
      if (fType === 'checkbox' || fType === 'bool') {
        const isChecked = (String(value).toLowerCase() === 'true' || value === true || value === '1' || value === 'yes');
        return `
          <div class="space-y-1">
            <div class="flex items-center justify-between min-h-[44px] py-1 ${hasProb ? 'bg-ember-light p-2 rounded-[2px] border border-ember' : ''}">
              <label for="${inputId}" class="flex-1 text-xs font-bold text-ink cursor-pointer flex items-center gap-1">
                <span>${fName}</span>
                ${problemBadge}
              </label>
              <div class="flex items-center gap-1.5">
                ${historyControls}
                <label class="min-w-[44px] min-h-[44px] flex items-center justify-center cursor-pointer">
                  <input
                    type="checkbox"
                    id="${inputId}"
                    data-section="${section}"
                    data-field="${fName}"
                    ${isChecked ? 'checked' : ''}
                    onchange="markDirty('${fName}'); triggerAutoSave()"
                    class="w-5 h-5 text-fern rounded-[2px] border-bordercol focus:ring-fern cursor-pointer"
                  />
                </label>
              </div>
            </div>
            ${historyContainerHtml}
          </div>
        `;
      }

      // Multiline
      if (fType === 'multiline') {
        return `
          <div class="space-y-1">
            <div class="flex items-center justify-between min-h-[32px]">
              <label for="${inputId}" class="text-xs font-bold text-ink flex items-center gap-1">
                <span>${fName}</span>
                ${problemBadge}
              </label>
              <div class="flex items-center">${historyControls}</div>
            </div>
            <textarea
              id="${inputId}"
              data-section="${section}"
              data-field="${fName}"
              rows="2"
              oninput="markDirty('${fName}'); triggerAutoSave()" onblur="saveCurrentEdits()"
              class="w-full border rounded-[2px] px-3 py-2 text-xs outline-none ${inputStyle}"
            >${value || ''}</textarea>
            ${historyContainerHtml}
          </div>
        `;
      }

      // Standard Text or Readonly
      return `
        <div class="space-y-1">
          <div class="flex items-center justify-between min-h-[32px]">
            <label for="${inputId}" class="text-xs font-bold text-ink flex items-center gap-1">
              <span>${fName}</span>
              ${problemBadge}
              ${isReadOnly ? '<span class="text-[9px] text-ink-faint font-normal font-mono">(Locked)</span>' : ''}
            </label>
            <div class="flex items-center">${historyControls}</div>
          </div>
          <input
            type="text"
            id="${inputId}"
            data-section="${section}"
            data-field="${fName}"
            value="${value || ''}"
            ${isReadOnly ? 'readonly class="w-full min-h-[44px] bg-tonal1 border border-bordercol rounded-[2px] px-3 py-2 text-xs text-ink-muted font-mono outline-none"' : `class="w-full min-h-[44px] border rounded-[2px] px-3 py-2 text-xs outline-none ${inputStyle}" oninput="markDirty('${fName}'); handleVocabInput(this, '${fName}')" onchange="markDirty('${fName}'); handleVocabChange(this)" onblur="saveCurrentEdits()"`}
            ${activeSchema && activeSchema.vocabulary && activeSchema.vocabulary[fName] && !isReadOnly ? `list="datalist_${section}_${fName}"` : ''}
          />
          ${activeSchema && activeSchema.vocabulary && activeSchema.vocabulary[fName] && !isReadOnly ? `
          <datalist id="datalist_${section}_${fName}">
            ${activeSchema.vocabulary[fName].map(v => `<option value="${v}"></option>`).join('')}
          </datalist>
          ` : ''}
          ${historyContainerHtml}
        </div>
      `;
    }

    function toggleUnvalidatedField(section, fName) {
      if (!currentUnvalidatedMap) currentUnvalidatedMap = {};
      const fKey = fName.replace(/[ ]+/g, '_');
      const container = document.getElementById(`unval_container_${section}_${fKey}`);
      const btn = document.getElementById(`unval_btn_${section}_${fKey}`);
      const input = document.getElementById(`unval_input_${section}_${fKey}`);

      if (currentUnvalidatedMap[fName] !== undefined) {
        delete currentUnvalidatedMap[fName];
        if (container) container.classList.add('hidden');
        if (btn) {
          btn.innerHTML = '<span>?</span>';
          btn.className = 'min-h-[44px] px-2 py-1 text-xs font-bold rounded-[2px] touch-target-min touch-press ml-1 flex items-center justify-center transition-all text-ink-faint hover:bg-tonal2 border border-bordercol';
        }
      } else {
        currentUnvalidatedMap[fName] = (input ? input.value : '') || '';
        if (container) container.classList.remove('hidden');
        if (btn) {
          btn.innerHTML = '<span>❓</span>';
          btn.className = 'min-h-[44px] px-2 py-1 text-xs font-bold rounded-[2px] touch-target-min touch-press ml-1 flex items-center justify-center transition-all bg-amber-500/20 text-amber-600 dark:text-amber-400 border border-amber-500/40';
        }
        if (input) input.focus();
      }
      markDirty(fName);
      triggerAutoSave();
    }

    function onUnvalCommentChange(fName, val) {
      if (!currentUnvalidatedMap) currentUnvalidatedMap = {};
      currentUnvalidatedMap[fName] = val;
      markDirty(fName);
    }

    function toggleAccordion(btn) {
      const acc = btn.closest('.accordion');
      acc.classList.toggle('acc-open');
      const content = acc.querySelector('.acc-content');
      const icon = acc.querySelector('.acc-icon');
      if (acc.classList.contains('acc-open')) {
        content.classList.remove('hidden');
        if (icon) icon.textContent = '▲';
      } else {
        content.classList.add('hidden');
        if (icon) icon.textContent = '▼';
      }
    }

    // ==========================================
    // UNDO & RECENT EDITS
    // ==========================================
    async function undoLastEdit(oid = null) {
      try {
        const payload = oid ? { oid: oid } : {};
        const res = await apiFetch('/api/undo', {
          method: 'POST',
          body: JSON.stringify(payload)
        });

        if (res.success) {
          showToast(`✓ Undo successful`);
          const undoBtn = document.getElementById('btnMobileUndo');
          if (undoBtn) {
            undoBtn.classList.remove('flex');
            undoBtn.classList.add('hidden');
          }

          if (document.getElementById('recentEditsModal') && !document.getElementById('recentEditsModal').classList.contains('hidden')) {
              await openRecentEditsModal();
          }

          if (currentRecord && String(res.restored.id) === String(currentOid)) {
            Object.assign(currentRecord, res.restored);
            isReviewed = currentRecord.review_status === 'reviewed';
            renderDynamicForm(activeSchema, currentRecord);
            renderDiscrepancies(currentRecord);
            updateReviewButtonUI();
          }

          const listItem = objectList.find(o => String(o.id) === String(res.restored.id));
          if (listItem) {
            Object.assign(listItem, res.restored);
            if (!document.getElementById('listView').classList.contains('hidden')) {
              renderList();
            }
          }
        } else {
          showToast(res.error || 'Undo failed', true);
        }
      } catch (err) {
        showToast('Undo failed', true);
        console.error(err);
      }
    }

    async function openRecentEditsModal() {
      const modal = document.getElementById('recentEditsModal');
      const listContainer = document.getElementById('recentEditsList');

      try {
        const res = await apiFetch('/api/recent_edits');
        if (res.edits && res.edits.length > 0) {
          listContainer.innerHTML = res.edits.map(edit => `
            <div class="bg-surface border border-bordercol rounded-[2px] p-3 text-sm flex flex-col gap-2 shadow-xs">
              <div class="flex items-center justify-between">
                <span class="font-mono text-xs font-medium text-ink bg-tonal1 px-1.5 py-0.5 rounded-[2px]">${edit.oid}</span>
                <span class="text-[10px] text-ink-muted">${edit.time}</span>
              </div>
              <div class="text-xs text-ink break-words">${edit.summary}</div>
              <div class="flex justify-end border-t border-tonal2 mt-1 pt-2">
                 <button type="button" onclick="undoLastEdit('${edit.oid}')" class="text-[11px] font-bold text-ember hover:bg-ember/10 px-2 py-1 border border-ember-border bg-ember-light rounded-[2px] touch-press">Revert</button>
              </div>
            </div>
          `).join('');
        } else {
          listContainer.innerHTML = `
            <div class="text-center p-6 text-ink-faint text-xs">
              <div class="text-2xl mb-2">∅</div>
              No recent edits in this session.
            </div>
          `;
        }
      } catch (err) {
        listContainer.innerHTML = `<div class="text-center p-4 text-ember text-xs">Error loading history.</div>`;
      }

      modal.classList.remove('hidden');
    }

    function closeRecentEditsModal() {
      document.getElementById('recentEditsModal').classList.add('hidden');
    }

    // ==========================================
    // LOCATION PRESETS LOGIC
    // ==========================================
    function applyLocPreset() {
      const select = document.getElementById('locPresetSelect');
      if (!select) return;
      const pName = select.value;
      if (!pName || pName === "Default") return;

      const presetData = locationPresets[pName];
      if (!presetData) return;

      lastSelectedPreset = pName;
      let changed = false;

      // Ensure activeSchema and location fields exist
      if (activeSchema && activeSchema.ui_sections && activeSchema.ui_sections.location) {
        activeSchema.ui_sections.location.forEach(field => {
          const inputId = `input_observation_${field.name.replace(/[^a-zA-Z0-9_]/g, '_')}`;
          const input = document.getElementById(inputId);
          if (input && presetData[field.name] !== undefined) {
             const newVal = presetData[field.name];
             if (input.type === 'checkbox') {
               const checkedVal = (String(newVal).toLowerCase() === 'true' || newVal === true || newVal === '1');
               if (input.checked !== checkedVal) {
                  input.checked = checkedVal;
                  changed = true;
                  markDirty(field.name);
               }
             } else {
               if (input.value !== newVal) {
                 input.value = newVal;
                 changed = true;
                 markDirty(field.name);
               }
             }
          }
        });
      }

      if (changed) {
        if (currentRecord && currentRecord.observation && activeSchema && activeSchema.ui_sections && activeSchema.ui_sections.location) {
          activeSchema.ui_sections.location.forEach(field => {
            if (presetData[field.name] !== undefined) {
              currentRecord.observation[field.name] = presetData[field.name];
            }
          });
        }
        showToast(`Applied Preset: ${pName}`);
        triggerAutoSave();
        if (typeof updateDetailProblemBanner === 'function' && currentRecord) updateDetailProblemBanner(currentRecord);
        if (typeof renderDiscrepancies === 'function' && currentRecord) renderDiscrepancies(currentRecord);
      }
    }

    // -------------------------------------------------------------
    // TACTILE HAPTIC ENGINE (V1 PARITY)
    // -------------------------------------------------------------
    const HAPTIC_PROFILES = {
      light: { stepper: 8, reviewed_on: [15, 25, 15], reviewed_off: 12, copy_prev: [10, 20, 10], discrepancy: [25, 25, 25], scan: 15 },
      medium: { stepper: 15, reviewed_on: [25, 40, 25], reviewed_off: 20, copy_prev: [15, 30, 15], discrepancy: [45, 40, 45], scan: 30 },
      strong: { stepper: 28, reviewed_on: [40, 60, 40], reviewed_off: 35, copy_prev: [25, 40, 25], discrepancy: [70, 50, 70], scan: 50 }
    };

    let v1HapticsEnabled = localStorage.getItem('arbor_haptics_enabled') !== 'false';
    let v1HapticsIntensity = localStorage.getItem('arbor_haptics_intensity') || 'medium';

    function triggerHaptic(actionType) {
      if (!v1HapticsEnabled) return;
      if (typeof navigator === 'undefined' || !('vibrate' in navigator)) return;
      const intensity = v1HapticsIntensity || 'medium';
      const pattern = HAPTIC_PROFILES[intensity]?.[actionType] || HAPTIC_PROFILES['medium']?.[actionType];
      if (pattern) {
        try { navigator.vibrate(pattern); } catch (e) {}
      }
    }

    function toggleHapticsSetting(enabled) {
      v1HapticsEnabled = !!enabled;
      try { localStorage.setItem('arbor_haptics_enabled', v1HapticsEnabled ? 'true' : 'false'); } catch(e) {}
      updateHapticsUI();
    }

    function setHapticsIntensity(intensity) {
      if (!['light', 'medium', 'strong'].includes(intensity)) return;
      v1HapticsIntensity = intensity;
      try { localStorage.setItem('arbor_haptics_intensity', intensity); } catch(e) {}
      updateHapticsUI();
      triggerHaptic('stepper');
    }

    function testHapticFeedback() {
      triggerHaptic('reviewed_on');
    }

    function updateHapticsUI() {
      const toggle = document.getElementById('settingEnableHaptics');
      if (toggle) toggle.checked = v1HapticsEnabled;

      const container = document.getElementById('hapticsIntensityContainer');
      if (container) {
        if (v1HapticsEnabled) {
          container.classList.remove('opacity-40', 'pointer-events-none');
        } else {
          container.classList.add('opacity-40', 'pointer-events-none');
        }
      }

      const cur = v1HapticsIntensity || 'medium';
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

    async function openSettingsModal() {
      openModal('settingsModal');
      updateHapticsUI();
      const input = document.getElementById('settingImageUrlPattern');
      try {
        const res = await apiFetch('/api/settings');
        if (res && res.success) {
          input.value = res.image_url_pattern_override || '';
        }
      } catch (err) {
        console.error("Failed to load settings:", err);
      }
    }

    function closeSettingsModal() {
      closeModal('settingsModal');
    }

    async function saveSettings() {
      const pattern = document.getElementById('settingImageUrlPattern').value.trim();
      try {
        const res = await apiFetch('/api/settings', {
          method: 'POST',
          body: JSON.stringify({ image_url_pattern_override: pattern })
        });
        if (res && res.success) {
          showToast("Settings saved.");
          closeSettingsModal();
        } else {
          showToast("Failed to save settings.", true);
        }
      } catch (err) {
        console.error("Failed to save settings:", err);
        showToast("Error saving settings.", true);
      }
    }

    function openPresetSettings() {
      renderPresetSettingsList();
      openModal('presetSettingsModal');
    }

    function closePresetSettings() {
      closeModal('presetSettingsModal');
    }

    function renderPresetSettingsList() {
      const container = document.getElementById('presetSettingsList');
      if (!container) return;

      const keys = Object.keys(locationPresets).filter(k => k !== 'Default');
      if (keys.length === 0) {
        container.innerHTML = '<p class="text-xs text-ink-faint italic py-2">No custom presets saved yet.</p>';
        return;
      }

      container.innerHTML = keys.map(k => `
        <div class="flex items-center justify-between p-2.5 border-b border-bordercol bg-surface hover:bg-tonal1 rounded-[2px] transition-colors mb-1 shadow-xs">
          <span class="text-sm font-sans text-ink">${k}</span>
          <button type="button" onclick="deleteLocPreset('${k}')" class="px-2 py-1 text-xs font-bold text-ember border border-ember bg-ember-light hover:bg-ember rounded-[2px] hover:text-white transition-colors cursor-pointer touch-press">Delete</button>
        </div>
      `).join('');
    }

    async function deleteLocPreset(name) {
      if (!confirm(`Delete location preset "${name}"?`)) return;

      try {
        const res = await apiFetch('/api/presets', {
          method: 'POST',
          body: JSON.stringify({ action: "delete", name: name })
        });

        if (res && res.success) {
          locationPresets = res.presets || {};
          if (lastSelectedPreset === name) lastSelectedPreset = "Default";
          renderPresetSettingsList();
          showToast(`Preset deleted.`);
          // Repopulate dynamic form to update select options
          renderDynamicForm(activeSchema, currentRecord);
        } else {
          showToast(`Failed to delete preset.`, true);
        }
      } catch (err) {
        console.error("Error deleting preset:", err);
        showToast("Error deleting preset", true);
      }
    }

    function toggleNewPresetForm() {
      const form = document.getElementById('newPresetForm');
      if (form.classList.contains('hidden')) {
        form.classList.remove('hidden');
        document.getElementById('newPresetNameInput').focus();
      } else {
        form.classList.add('hidden');
      }
    }

    async function saveNewLocPreset() {
      const nameInput = document.getElementById('newPresetNameInput');
      const name = nameInput.value.trim();

      if (!name) {
        alert("Please enter a name for the preset.");
        return;
      }
      if (name.toLowerCase() === "default") {
        alert("Cannot overwrite Default preset.");
        return;
      }

      const vals = {};
      if (activeSchema && activeSchema.ui_sections && activeSchema.ui_sections.location) {
        activeSchema.ui_sections.location.forEach(field => {
          const inputId = `input_observation_${field.name.replace(/[^a-zA-Z0-9_]/g, '_')}`;
          const input = document.getElementById(inputId);
          if (input) {
             if (input.type === 'checkbox') {
               vals[field.name] = input.checked ? "True" : "False";
             } else {
               vals[field.name] = input.value;
             }
          }
        });
      }

      try {
        const res = await apiFetch('/api/presets', {
          method: 'POST',
          body: JSON.stringify({ action: "save", name: name, values: vals })
        });

        if (res && res.success) {
          locationPresets = res.presets || {};
          lastSelectedPreset = name;
          nameInput.value = "";
          toggleNewPresetForm();
          renderPresetSettingsList();
          showToast(`Preset "${name}" saved.`);
          // Repopulate dynamic form to update select options and set it to active
          renderDynamicForm(activeSchema, currentRecord);
          // Set dropdown
          setTimeout(() => {
             const sel = document.getElementById('locPresetSelect');
             if(sel) sel.value = name;
          }, 50);
        } else {
          showToast(`Failed to save preset.`, true);
        }
      } catch (err) {
        console.error("Error saving preset:", err);
        showToast("Error saving preset", true);
      }
    }

    // ==========================================
    // DISCREPANCY & PROBLEM TOGGLES
    // ==========================================
    function renderDiscrepancies(record) {
      const listContainer = document.getElementById('activeDiscrepanciesList');
      const togglesContainer = document.getElementById('problemTogglesContainer');

      const issues = record.flagged_issues || [];
      if (issues.length === 0) {
        listContainer.innerHTML = `<p class="text-xs text-ink-faint italic">No active discrepancies flagged for this specimen.</p>`;
      } else {
        listContainer.innerHTML = issues.map((iss, idx) => `
          <div class="bg-ember-light border border-ember-border p-2.5 rounded-[2px] flex items-start justify-between gap-2 text-xs">
            <div>
              <span class="font-bold text-ember-dark">${iss.field || 'General'}:</span>
              <p class="text-ember-dark mt-0.5">${iss.reason || 'Flagged problem'}</p>
            </div>
            <button
              type="button"
              onclick="resolveDiscrepancy('${iss.id}')"
              class="min-h-[44px] px-3 py-1.5 bg-surface hover:bg-ember-light border border-ember-border text-ember-dark font-bold text-xs rounded-[2px] shrink-0 touch-target-min touch-press flex items-center justify-center"
            >
              Resolve
            </button>
          </div>
        `).join('');
      }

      // Quick Toggles from ui_sections.problems
      if (activeSchema && activeSchema.ui_sections && activeSchema.ui_sections.problems) {
        const probs = activeSchema.ui_sections.problems;
        togglesContainer.innerHTML = probs.map(p => {
          const pName = p.name;
          const pLabel = pName.replace('_Problem', '').replace(/_/g, ' ');
          const isFlagged = (record.observation && (String(record.observation[pName]).toLowerCase() === 'true' || record.observation[pName] === true || record.observation[pName] === '1'));
          return `
            <label class="touch-target-min min-h-[44px] flex items-center gap-2 p-2.5 border rounded-[2px] transition-colors touch-press cursor-pointer ${isFlagged ? 'border-ember bg-ember-light text-ember-dark font-semibold' : 'border-bordercol bg-surface text-ink hover:bg-tonal1'}">
              <input
                type="checkbox"
                id="prob_${pName}"
                ${isFlagged ? 'checked' : ''}
                onchange="toggleProblemFlag('${pName}')"
                class="w-4 h-4 text-ember rounded-[2px] border-bordercol focus:ring-ember cursor-pointer shrink-0"
              />
              <span class="truncate font-sans text-xs select-none">${pLabel}</span>
            </label>
          `;
        }).join('');
      }
    }

    let activeQuickCabinet = '';
    let activeQuickShelf = '';

    function handleV1LocationFilterChange() {
      const cab = document.getElementById('quickFilterCabinet');
      const shelf = document.getElementById('quickFilterShelf');
      activeQuickCabinet = cab ? cab.value : '';
      activeQuickShelf = shelf ? shelf.value : '';
      const clearBtn = document.getElementById('btnClearLocFilterV1');
      if (clearBtn) {
        if (activeQuickCabinet || activeQuickShelf) clearBtn.classList.remove('hidden');
        else clearBtn.classList.add('hidden');
      }
      loadObjects();
    }

    function clearV1LocationFilter() {
      activeQuickCabinet = '';
      activeQuickShelf = '';
      const cab = document.getElementById('quickFilterCabinet');
      const shelf = document.getElementById('quickFilterShelf');
      if (cab) cab.value = '';
      if (shelf) shelf.value = '';
      const clearBtn = document.getElementById('btnClearLocFilterV1');
      if (clearBtn) clearBtn.classList.add('hidden');
      loadObjects();
    }

    function populateDiscrepancyFields() {
      const select = document.getElementById('discrepancyFieldSelect');
      if (!select) return;
      const coreOptions = [
        'Physical Specimen Damaged',
        'Physical Specimen Misplaced',
        'Taxon / Identification Issue',
        'General Specimen Issue'
      ];
      const reg = (activeSchema && activeSchema.ui_sections && activeSchema.ui_sections.registration || []).map(f => f.name);
      const loc = (activeSchema && activeSchema.ui_sections && activeSchema.ui_sections.location || []).map(f => f.name);
      const all = coreOptions.concat(reg).concat(loc);
      select.innerHTML = all.map(f => `<option value="${f}">${f}</option>`).join('');
    }

    function openAddDiscrepancyModal(fieldName) {
      if (fieldName) {
        document.getElementById('discrepancyFieldSelect').value = fieldName;
      }
      const unvalCheck = document.getElementById('discrepancyUnvalCheck');
      const unvalInput = document.getElementById('discrepancyUnvalNoteInput');
      const unvalCont = document.getElementById('discrepancyUnvalContainer');
      if (unvalCheck && unvalInput && unvalCont) {
        const hasUnval = (currentUnvalidatedMap && fieldName && currentUnvalidatedMap[fieldName] !== undefined);
        unvalCheck.checked = !!hasUnval;
        unvalInput.value = hasUnval ? currentUnvalidatedMap[fieldName] : '';
        if (hasUnval) unvalCont.classList.remove('hidden');
        else unvalCont.classList.add('hidden');
      }
      openModal('addDiscrepancyModal');
    }

    function updateDetailProblemBanner(data) {
      const banner = document.getElementById('detailProblemBanner');
      const badgeContainer = document.getElementById('detailProblemBadges');
      if (!banner || !badgeContainer || !data) return;
      const activeProbFields = [];
      const unknownFields = [];

      if (activeSchema && activeSchema.ui_sections) {
        const allFields = (activeSchema.ui_sections.registration || []).concat(activeSchema.ui_sections.location || []);
        allFields.forEach(f => {
          const val = (data.registration && data.registration[f.name] !== undefined) ? data.registration[f.name] : (data.observation ? data.observation[f.name] : '');
          if (isFieldProblemActive(f.name, 'registration', data) || isFieldProblemActive(f.name, 'observation', data)) {
            if (!activeProbFields.includes(f.name)) activeProbFields.push(f.name);
          } else if (isValueUnknown(val)) {
            if (!unknownFields.includes(f.name)) unknownFields.push(f.name);
          }
        });
      }

      if (activeProbFields.length > 0 || unknownFields.length > 0) {
        banner.classList.remove('hidden');
        let chipsHtml = '';
        activeProbFields.forEach(fName => {
          const inputId = `input_registration_${fName.replace(/[^a-zA-Z0-9_]/g, '_')}`;
          chipsHtml += `
            <button
              type="button"
              onclick="scrollToField('${inputId}', '${fName}')"
              class="px-2 py-1 bg-[#C62828] text-white text-[11px] font-bold rounded-[2px] shadow-xs flex items-center gap-1 touch-press hover:bg-[#b71c1c]"
              title="Jump to ${fName}"
            >
              <span>⚠</span>
              <span>${fName}</span>
            </button>
          `;
        });
        unknownFields.forEach(fName => {
          const inputId = `input_registration_${fName.replace(/[^a-zA-Z0-9_]/g, '_')}`;
          chipsHtml += `
            <button
              type="button"
              onclick="scrollToField('${inputId}', '${fName}')"
              class="px-2 py-1 bg-[#FBC02D] text-[#2c302e] text-[11px] font-bold rounded-[2px] shadow-xs flex items-center gap-1 touch-press hover:bg-[#f9a825]"
              title="Jump to ${fName}"
            >
              <span>?</span>
              <span>${fName}</span>
            </button>
          `;
        });
        badgeContainer.innerHTML = chipsHtml;
      } else {
        banner.classList.add('hidden');
        badgeContainer.innerHTML = '';
      }
    }

    async function submitDiscrepancy(e) {
      e.preventDefault();
      const field = document.getElementById('discrepancyFieldSelect').value;
      const reason = document.getElementById('discrepancyReasonInput').value.trim();
      const severity = document.querySelector('input[name="severity"]:checked').value;

      if (!reason) return;

      // Handle unvalidated source if checked
      const unvalCheck = document.getElementById('discrepancyUnvalCheck');
      const unvalNote = document.getElementById('discrepancyUnvalNoteInput');
      if (unvalCheck && unvalCheck.checked) {
        if (!currentUnvalidatedMap) currentUnvalidatedMap = {};
        currentUnvalidatedMap[field] = (unvalNote ? unvalNote.value.trim() : '') || reason;
        markDirty(field);
      } else if (unvalCheck && !unvalCheck.checked && currentUnvalidatedMap && currentUnvalidatedMap[field] !== undefined) {
        delete currentUnvalidatedMap[field];
        markDirty(field);
      }

      // Add to flagged issues locally and trigger save
      currentRecord.flagged_issues = currentRecord.flagged_issues || [];
      currentRecord.flagged_issues.push({
        id: `flag_${Date.now()}`,
        field: field,
        severity: severity,
        reason: reason,
        resolved: false
      });

      // Match corresponding problem toggle if it exists
      const matchProb = `${field}_Problem`;
      if (currentRecord.observation) {
        currentRecord.observation[matchProb] = true;
        markDirty(matchProb);
      }

      closeModal('addDiscrepancyModal');
      document.getElementById('discrepancyReasonInput').value = '';
      renderDynamicForm(activeSchema, currentRecord);
      updateDetailProblemBanner(currentRecord);
      renderDiscrepancies(currentRecord);
      await saveCurrentEdits();
      showToast('Discrepancy flagged on host');
    }

    async function resolveDiscrepancy(issId) {
      if (!currentRecord || !currentRecord.flagged_issues) return;
      currentRecord.flagged_issues = currentRecord.flagged_issues.filter(i => i.id !== issId);
      renderDynamicForm(activeSchema, currentRecord);
      updateDetailProblemBanner(currentRecord);
      renderDiscrepancies(currentRecord);
      await saveCurrentEdits();
      showToast('Discrepancy resolved');
    }

    async function toggleProblemFlag(probName) {
      const el = document.getElementById(`prob_${probName}`);
      if (!el || !currentRecord) return;
      currentRecord.observation = currentRecord.observation || {};
      currentRecord.observation[probName] = el.checked;
      markDirty(probName);

      const probs = (activeSchema && activeSchema.ui_sections && activeSchema.ui_sections.problems) ? activeSchema.ui_sections.problems : [];
      let hasProb = false;
      for (const p of probs) {
        const v = currentRecord.observation[p.name];
        if (v === true || String(v).toLowerCase() === 'true' || v === '1') {
          hasProb = true;
          break;
        }
      }
      currentRecord.has_flags = hasProb;
      updateReviewButtonUI();
      renderDynamicForm(activeSchema, currentRecord);
      updateDetailProblemBanner(currentRecord);

      await saveCurrentEdits();
    }

    // ==========================================
    // AUTO-SAVE & PRIMARY ACTION: MARK REVIEWED
    // ==========================================


    function handleVocabInput(input, fName) {
      markDirty(fName);
      triggerAutoSave();
    }

    function handleVocabChange(input) {
      if (input.value && input.value.trim() !== '') {
        const val = input.value.trim();
        const fName = input.getAttribute('data-field');
        if (val !== '?') {
            // Check if matches vocab but different casing
            if (activeSchema && activeSchema.vocabulary && activeSchema.vocabulary[fName]) {
                const match = activeSchema.vocabulary[fName].find(v => v.toLowerCase() === val.toLowerCase());
                if (match) {
                    input.value = match;
                } else {
                    input.value = val; // Trimmed
                }
            } else {
                input.value = val; // Trimmed
            }
        }
      }
      const fName = input.getAttribute('data-field');
      markDirty(fName);
      triggerAutoSave();
    }

    function markDirty(fieldName) {
      if (fieldName) dirtyFields.add(fieldName);
    }

    function triggerAutoSave() {
      const syncStatus = document.getElementById('footerSyncStatus');
      syncStatus.innerHTML = `<span class='flex items-center gap-1.5 font-mono text-ember font-medium animate-pulse'><svg class="animate-spin h-3 w-3 text-ember" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg><span>Saving changes...</span></span>`;
      const btnRev = document.getElementById('btnMarkReviewed');
      if (btnRev) btnRev.disabled = true;
      clearTimeout(autoSaveTimer);
      autoSaveTimer = setTimeout(saveCurrentEdits, 800);  // 800ms per guide requirement
    }

    async function saveCurrentEdits() {
      if (autoSaveTimer) {
        clearTimeout(autoSaveTimer);
        autoSaveTimer = null;
      }
      if (!currentOid) return;

      if (isSaving) {
        hasPendingSave = true;
        return;
      }
      isSaving = true;

      try {
        while (true) {
          hasPendingSave = false;
          const btnRev = document.getElementById('btnMarkReviewed');

          const regPayload = {};
          const obsPayload = {};

          // Collect all dynamic inputs
          document.querySelectorAll('[data-section="registration"]').forEach(input => {
            const f = input.getAttribute('data-field');
            if (dirtyFields.has(f)) {
              regPayload[f] = (input.type === 'checkbox') ? input.checked : input.value;
            }
          });

          document.querySelectorAll('[data-section="observation"]').forEach(input => {
            const f = input.getAttribute('data-field');
            if (dirtyFields.has(f)) {
              if (input.type === 'checkbox') {
                obsPayload[f] = input.checked;
              } else {
                obsPayload[f] = input.value;
              }
            }
          });

          // Merge problem flags
          if (currentRecord && currentRecord.observation) {
            Object.keys(currentRecord.observation).forEach(k => {
              if (k.endsWith('_Problem') || k.startsWith('Unknown_')) {
                if (dirtyFields.has(k)) {
                  obsPayload[k] = currentRecord.observation[k];
                }
              }
            });
          }

          // If nothing was dirtied, and review status wasn't checked, we technically don't need to save,
          // but the server handles empty updates gracefully.
          dirtyFields.clear();

          const unvalSourcesList = Object.entries(currentUnvalidatedMap || {}).map(([field, comment]) => ({ field, comment }));

          const payload = {
            id: currentOid,
            reviewed: isReviewed,
            registration: regPayload,
            observation: obsPayload,
            unvalidated_sources: unvalSourcesList,
            timestamp: new Date().toISOString()
          };

          if (!navigator.onLine || (document.getElementById('pingBadge') && document.getElementById('pingBadge').textContent === 'Offline')) {
            queueMutation(payload);
            if (btnRev) btnRev.disabled = false;

            // Optimistically update UI models to prevent local interruption
            if (currentRecord) {
              currentRecord.review_status = isReviewed ? 'reviewed' : 'pending';
              currentRecord.unvalidated_sources = unvalSourcesList;
              updateReviewButtonUI();
            }

            const listItem = objectList.find(o => String(o.id) === String(currentOid));
            if (listItem) {
              listItem.review_status = isReviewed ? 'reviewed' : 'pending';
              listItem.has_unvalidated = (unvalSourcesList.length > 0);
            }

            if (!hasPendingSave) break;
            continue;
          }
          if (btnRev) btnRev.disabled = false;

          try {
            const res = await apiFetch('/api/update', {
              method: 'POST',
              body: JSON.stringify(payload)
            });

            // Check for conflict response (409) or conflict message
            if (res && (res._status === 409 || res.status === 409 || (typeof res.error === 'string' && res.error.includes('Conflict')))) {
              showToast(`⚠️ ${res.error || 'Conflict: Host modified this record'}`, true);
              const syncStatus = document.getElementById('footerSyncStatus');
              if (syncStatus) {
                syncStatus.innerHTML = '<span class="font-mono text-ember font-medium" id="footerSyncStatusText">⚠️ Host conflict</span>';
              }
              if (btnRev) btnRev.disabled = false;
              if (!hasPendingSave) break;
              continue;
            }

            if (res && res.error && res.error !== 'Failed to fetch') {
              showToast(`⚠️ ${res.error}`, true);
              if (btnRev) btnRev.disabled = false;
              if (!hasPendingSave) break;
              continue;
            }

            // Handle case where fetch returns a network error or empty object instead of throwing
            if (!res || res.error === 'Failed to fetch' || (Object.keys(res).length === 0)) {
               throw new Error('Network failure');
            }

            document.getElementById('footerSyncStatus').innerHTML = '<span class="font-mono text-fern-dark font-medium" id="footerSyncStatusText">✓ Edit saved</span>';
            if (btnRev) btnRev.disabled = false;
            const undoBtn = document.getElementById('btnMobileUndo');
            if (undoBtn) undoBtn.classList.remove('hidden');
            if (undoBtn) undoBtn.classList.add('flex');

            if (res && res.success && currentRecord && (String(currentRecord.id) === String(currentOid) || String(currentRecord.accession_number) === String(currentOid))) {
              if (res.has_flags !== undefined) currentRecord.has_flags = res.has_flags;
              if (res.has_history !== undefined) currentRecord.has_history = res.has_history;
              if (res.has_unknown !== undefined) currentRecord.has_unknown = res.has_unknown;
              if (res.review_status !== undefined) currentRecord.review_status = res.review_status;
              updateReviewButtonUI();

              const listItem = objectList.find(o => String(o.id) === String(currentOid));
              if (listItem) {
                if (res.has_flags !== undefined) listItem.has_flags = res.has_flags;
                if (res.has_history !== undefined) listItem.has_history = res.has_history;
                if (res.has_unknown !== undefined) listItem.has_unknown = res.has_unknown;
                if (res.review_status !== undefined) listItem.review_status = res.review_status;
              }
            }

            // Hide 'Edit saved' message if we determine we're actually disconnected
            if (document.getElementById('pingBadge') && document.getElementById('pingBadge').textContent === 'Offline') {
                document.getElementById('footerSyncStatusText').classList.add('hidden');
            }
          } catch (err) {
            queueMutation(payload);
            if (btnRev) btnRev.disabled = false;

            // Optimistically update UI models to prevent local interruption
            if (currentRecord) {
              currentRecord.review_status = isReviewed ? 'reviewed' : 'pending';
              updateReviewButtonUI();
            }

            const listItem = objectList.find(o => String(o.id) === String(currentOid));
            if (listItem) {
              listItem.review_status = isReviewed ? 'reviewed' : 'pending';
            }
          }

          if (!hasPendingSave) {
            break;
          }
        }
      } finally {
        isSaving = false;
      }
    }

    function updateReviewButtonUI() {
      const btn = document.getElementById('btnMarkReviewed');
      const label = document.getElementById('btnReviewedLabel');
      const badgeContainer = document.getElementById('detailReviewStatusBadge');

      if (isReviewed) {
        btn.className = 'w-full py-3.5 px-4 rounded-[2px] font-sans font-bold text-sm flex items-center justify-center gap-2 border-2 transition-all touch-target-min touch-press bg-fern text-white border-fern-dark shadow-md';
        label.textContent = '✓ Reviewed (Tap to undo)';
      } else {
        btn.className = 'w-full py-3.5 px-4 rounded-[2px] font-sans font-bold text-sm flex items-center justify-center gap-2 border-2 transition-all touch-target-min touch-press bg-surface text-ink border-bordercol hover:bg-tonal1 shadow-xs';
        label.textContent = 'Mark Reviewed';
      }

      if (currentRecord) {
        currentRecord.review_status = isReviewed ? 'reviewed' : 'pending';
        badgeContainer.innerHTML = renderStatusBadge(currentRecord);
      } else {
        badgeContainer.innerHTML = renderStatusBadge({ review_status: isReviewed ? 'reviewed' : 'pending' });
      }
    }

    async function toggleReviewed() {
      isReviewed = !isReviewed;
      updateReviewButtonUI();
      await saveCurrentEdits();
      showToast(isReviewed ? '✓ Specimen marked as Reviewed' : 'Specimen marked Unreviewed');
    }

    // ==========================================
    // FULLSCREEN PHOTO VIEWER MODAL & THUMBNAIL STRIP
    // ==========================================
    function renderPhotoThumbnails() {
      const strip = document.getElementById('photoThumbStrip');
      if (!strip) return;
      if (!photoUrls || photoUrls.length <= 1) {
        strip.classList.add('hidden');
        strip.innerHTML = '';
        return;
      }

      strip.classList.remove('hidden');
      strip.innerHTML = photoUrls.map((url, idx) => `
        <button
          type="button"
          onclick="selectSpecimenPhoto(${idx})"
          class="min-w-[44px] min-h-[44px] w-12 h-12 rounded-[2px] border-2 overflow-hidden shrink-0 touch-target-min touch-press transition-all ${idx === currentPhotoIdx ? 'border-fern ring-2 ring-fern-border' : 'border-bordercol opacity-70 hover:opacity-100'}"
          title="View Scan ${idx + 1}"
          aria-label="View archival scan ${idx + 1}"
        >
          <img src="${url}" alt="Thumbnail ${idx + 1}" class="w-full h-full object-cover" />
        </button>
      `).join('');
    }

    function loadInitialPhoto() {
      if (!photoUrls || photoUrls.length === 0) return;
      const mainContainer = document.getElementById('photoMainContainer');
      const placeholder = document.getElementById('photoPlaceholder');
      const specimenImg = document.getElementById('specimenImg');

      mainContainer.classList.remove('h-16');
      mainContainer.classList.add('h-52');
      mainContainer.setAttribute('onclick', 'openFullscreenPhoto()');

      placeholder.innerHTML = `
        <span class="text-2xl text-ink-faint animate-spin-slow">⏳</span>
        <p class="font-semibold text-fern">Loading...</p>
      `;

      specimenImg.src = photoUrls[0];
      renderPhotoThumbnails();
    }

    function selectSpecimenPhoto(idx) {
      if (!photoUrls || !photoUrls[idx]) return;
      currentPhotoIdx = idx;
      const mainImg = document.getElementById('specimenImg');
      mainImg.src = photoUrls[idx];
      document.getElementById('photoPlaceholder').classList.add('hidden');
      mainImg.classList.remove('hidden');
      renderPhotoThumbnails();
    }

    function openFullscreenPhoto() {
      if (!photoUrls || photoUrls.length === 0) return;
      photoZoom = 1;
      photoRotation = 0;
      photoPan = { x: 0, y: 0 };
      updatePhotoTransform();
      document.getElementById('photoViewerImg').src = photoUrls[currentPhotoIdx] || photoUrls[0];
      document.getElementById('photoViewerCounter').textContent = `(${currentPhotoIdx + 1}/${photoUrls.length})`;
      openModal('photoViewerModal');
    }

    function onPhotoLoaded() {
      document.getElementById('photoPlaceholder').classList.add('hidden');
      document.getElementById('specimenImg').classList.remove('hidden');
      document.getElementById('photoWatermark').classList.remove('hidden');
    }

    function onPhotoError() {
      document.getElementById('photoPlaceholder').innerHTML = `
        <span class="text-2xl text-ink-faint">📷</span>
        <p class="font-semibold text-ink-muted">Photo scan unavailable</p>
      `;
    }

    function zoomPhoto(delta) {
      photoZoom = Math.min(Math.max(photoZoom + delta, 1), 4);
      if (photoZoom === 1) photoPan = { x: 0, y: 0 };
      updatePhotoTransform();
    }

    function rotatePhoto() {
      photoRotation = (photoRotation + 90) % 360;
      updatePhotoTransform();
    }

    function resetPhotoTransform() {
      photoZoom = 1;
      photoRotation = 0;
      photoPan = { x: 0, y: 0 };
      updatePhotoTransform();
    }

    function updatePhotoTransform() {
      const img = document.getElementById('photoViewerImg');
      document.getElementById('zoomLevelDisplay').textContent = `${photoZoom.toFixed(1)}x`;
      img.style.transform = `scale(${photoZoom}) rotate(${photoRotation}deg) translate(${photoPan.x}px, ${photoPan.y}px)`;
    }

    function startPhotoDrag(e) {
      if (photoZoom > 1) {
        isDraggingPhoto = true;
        photoDragStart = { x: e.clientX - photoPan.x, y: e.clientY - photoPan.y };
        window.addEventListener('mousemove', onPhotoDrag);
        window.addEventListener('mouseup', stopPhotoDrag);
      }
    }

    function onPhotoDrag(e) {
      if (isDraggingPhoto && photoZoom > 1) {
        photoPan = { x: e.clientX - photoDragStart.x, y: e.clientY - photoDragStart.y };
        updatePhotoTransform();
      }
    }

    function stopPhotoDrag() {
      isDraggingPhoto = false;
      window.removeEventListener('mousemove', onPhotoDrag);
      window.removeEventListener('mouseup', stopPhotoDrag);
    }

    function startPhotoTouch(e) {
      if (e.touches.length === 1 && photoZoom > 1) {
        isDraggingPhoto = true;
        photoDragStart = { x: e.touches[0].clientX - photoPan.x, y: e.touches[0].clientY - photoPan.y };
        window.addEventListener('touchmove', onPhotoTouchMove);
        window.addEventListener('touchend', stopPhotoTouch);
      }
    }

    function onPhotoTouchMove(e) {
      if (isDraggingPhoto && e.touches.length === 1 && photoZoom > 1) {
        photoPan = { x: e.touches[0].clientX - photoDragStart.x, y: e.touches[0].clientY - photoDragStart.y };
        updatePhotoTransform();
      }
    }

    function stopPhotoTouch() {
      isDraggingPhoto = false;
      window.removeEventListener('touchmove', onPhotoTouchMove);
      window.removeEventListener('touchend', stopPhotoTouch);
    }

    // Initialize application
    init();
  </script>
</body>
</html>

"""

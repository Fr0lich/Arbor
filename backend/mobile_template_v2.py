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
    html.arbor-offline-css button.bg-emerald-600, html.arbor-offline-css button.bg-emerald-700 { background: #059669; color: #ffffff; border-color: #047857; font-weight: 700; }
    html.arbor-offline-css button.bg-amber-600 { background: #d97706; color: #ffffff; border-color: #b45309; font-weight: 700; }
    html.arbor-offline-css button.bg-amber-500 { background: #f59e0b; color: #ffffff; border-color: #d97706; font-weight: 700; }
    html.arbor-offline-css button.bg-ember { background: #d95c14; color: #ffffff; border-color: #b84a0c; font-weight: 700; }
    html.arbor-offline-css button.bg-brick { background: #c93a40; color: #ffffff; border-color: #991b1b; font-weight: 700; }
    html.arbor-offline-css button.bg-stone-900 { background: #1c1917; color: #ffffff; border-color: #1c1917; font-weight: 700; }
    html.arbor-offline-css #btnOldNames { background: #f8f9fa; color: #191e1a; border: 1px solid #d4d8d5; min-height: 36px; padding: 4px 10px; font-weight: 600; }
    html.arbor-offline-css input, html.arbor-offline-css select, html.arbor-offline-css textarea { border: 1px solid #c4c9c5; border-radius: 6px; padding: 6px 8px; background: #ffffff; color: #191e1a; font-size: 0.9rem; }
    html.arbor-offline-css #listView, html.arbor-offline-css #detailView, html.arbor-offline-css #batchLocationView { max-width: 540px; margin: 0 auto; min-height: 100vh; background: #f3f3f3; display: flex; flex-direction: column; }
    html.arbor-offline-css #specimenListContainer > * { background: #ffffff; border: 1px solid #d4d8d5; border-radius: 8px; padding: 10px 12px; margin-bottom: 8px; }
    html.arbor-offline-css #auditStationLaunchpad { background: #eaf4ec; border: 1px solid #a4cca9; border-radius: 8px; padding: 10px; margin: 8px 12px; }
    html.arbor-offline-css #armedShelfBanner { background: #eaf4ec; border: 1px solid #a4cca9; border-radius: 8px; padding: 8px 10px; margin-top: 8px; }
    html.arbor-offline-css .tab-btn { border: none; background: transparent; padding: 8px 6px; font-weight: 600; color: #535d56; min-height: 40px; }
    html.arbor-offline-css .tab-btn.text-ink { background: #ffffff; border-radius: 6px; border-bottom: 2px solid #3a7d44; box-shadow: 0 1px 2px rgba(0,0,0,0.08); color: #191e1a; }
    html.arbor-offline-css #tabIndicator { display: none; }
    html.arbor-offline-css #btnDetailMarkReviewed { width: 100%; min-height: 44px; background: #eaf4ec; color: #205438; border: 1px solid #3a7d44; border-radius: 8px; font-weight: 700; font-size: 0.95rem; }
    html.arbor-offline-css #btnDetailMarkReviewed.bg-emerald-600 { background: #059669; color: #ffffff; border-color: #047857; }
    html.arbor-offline-css #btnDetailMarkReviewed.bg-amber-600 { background: #d97706; color: #ffffff; border-color: #b45309; }
    html.arbor-offline-css #offlineBanner { background: #78350f; color: #ffffff; padding: 8px 14px; font-size: 0.8rem; font-weight: 600; }
    html.arbor-offline-css .left-0 { left: 0; }
    html.arbor-offline-css .right-0 { right: 0; }
    html.arbor-offline-css .shrink-0 { flex-shrink: 0; }
    html.arbor-offline-css .w-5 { width: 1.25rem; }
    html.arbor-offline-css .h-5 { height: 1.25rem; }
    html.arbor-offline-css .min-h-\\[36px\\] { min-height: 36px; }
    html.arbor-offline-css .min-h-\\[40px\\] { min-height: 40px; }
    html.arbor-offline-css .min-h-\\[44px\\] { min-height: 44px; }
    html.arbor-offline-css .rounded-t-xl { border-top-left-radius: 12px; border-top-right-radius: 12px; }
    html.arbor-offline-css .rounded-t-2xl { border-top-left-radius: 16px; border-top-right-radius: 16px; }
    html.arbor-offline-css .max-h-\\[85vh\\] { max-height: 85vh; }
    html.arbor-offline-css button.inline-flag-btn { border: none; padding: 0; background: transparent; min-width: 40px; min-height: 40px; display: inline-flex; align-items: center; justify-content: center; flex-shrink: 0; }
    html.arbor-offline-css button.inline-flag-btn > span { width: 20px; height: 20px; border-radius: 4px; border: 1px solid #c4c9c5; display: inline-flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; }
    @keyframes coachPulse {
      0%, 100% { outline: 3px solid #3a7d44; outline-offset: 2px; box-shadow: 0 0 0 4px rgba(58, 125, 68, 0.25); }
      50% { outline: 3px solid #52b765; outline-offset: 3px; box-shadow: 0 0 0 7px rgba(82, 183, 101, 0.35); }
    }
    .coach-target {
      animation: coachPulse 1.4s ease-in-out infinite;
      border-radius: 6px;
      position: relative;
      z-index: 35;
    }
    html.arbor-offline-css .coach-target {
      outline: 3px solid #3a7d44 !important;
      outline-offset: 2px;
      box-shadow: 0 0 0 5px rgba(58, 125, 68, 0.28);
    }
    html.arbor-offline-css #coachCard {
      position: fixed; left: 12px; right: 12px; bottom: 92px; max-width: 440px; margin: 0 auto;
      background: #181c19; color: #f3f6f4; border: 2px solid #3a7d44; border-radius: 12px;
      padding: 14px; box-shadow: 0 12px 28px rgba(0,0,0,0.45); z-index: 40;
    }
    html.arbor-offline-css #coachCard.coach-on-list { bottom: 16px; }
    html.arbor-offline-css #coachCard button { min-height: 40px; padding: 6px 12px; border-radius: 8px; font-weight: 600; }
    html.arbor-offline-css [id$="Modal"] { position: fixed; top: 0; right: 0; bottom: 0; left: 0; background: rgba(18, 22, 19, 0.6); display: flex; align-items: center; justify-content: center; padding: 16px; z-index: 50; }
    html.arbor-offline-css [id$="Modal"] > div { background: #ffffff; border: 1px solid #d4d8d5; border-radius: 12px; max-width: 440px; width: 100%; padding: 16px; max-height: 88vh; overflow-y: auto; box-shadow: 0 12px 32px rgba(0,0,0,0.28); }
    html.arbor-offline-css [id$="Sheet"] { position: fixed; top: 0; right: 0; bottom: 0; left: 0; background: rgba(18, 22, 19, 0.6); display: flex; flex-direction: column; justify-content: flex-end; align-items: center; z-index: 50; }
    html.arbor-offline-css [id$="Sheet"] > div { background: #ffffff; border-top: 1px solid #d4d8d5; border-radius: 16px 16px 0 0; max-width: 440px; width: 100%; padding: 16px; max-height: 85vh; overflow-y: auto; box-shadow: 0 -8px 28px rgba(0,0,0,0.24); }
    html.arbor-offline-css #toast { position: fixed; bottom: 96px; left: 50%; transform: translateX(-50%); background: #191e1a; color: #ffffff; padding: 10px 16px; border-radius: 9999px; z-index: 60; font-size: 0.85rem; box-shadow: 0 6px 20px rgba(0,0,0,0.25); }
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
    select.arbor-compact-select {
      background-image: none !important;
      padding-right: 1.5rem !important;
      white-space: nowrap;
      text-overflow: ellipsis;
    }
    .tab-slider { transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1); }
    #tabTrack { transition: transform 0.28s cubic-bezier(0.2, 0.8, 0.2, 1); }
    @keyframes arborShimmer {
      0% { background-position: 200% 0; }
      100% { background-position: -200% 0; }
    }
    .arbor-skeleton {
      background: linear-gradient(90deg, #e7e5e4 25%, #f5f5f4 50%, #e7e5e4 75%);
      background-size: 200% 100%;
      animation: arborShimmer 1.4s ease-in-out infinite;
      border-radius: 6px;
    }
    @media (prefers-reduced-motion: reduce) {
      .arbor-skeleton { animation: none; background: #e7e5e4; }
    }
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
      <button type="button" onclick="setupEventSource()" class="min-h-[38px] px-3 py-1.5 bg-ember text-white rounded font-bold text-[11px] tap-active">
        Retry
      </button>
    </div>

    <!-- ============================================================= -->
    <!-- SCREEN 1: VAULT LIST VIEW (#listView)                         -->
    <!-- ============================================================= -->
    <div id="listView" class="flex-1 flex flex-col h-full bg-canvas overflow-hidden">
      <!-- 1. Top Header -->
      <header class="sticky top-0 z-40 bg-surface/95 backdrop-blur-md border-b border-bordercol shrink-0">
        <div class="px-3.5 pt-2.5 pb-2 flex items-center justify-between gap-2">
          <div class="flex items-center space-x-2 min-w-0">
            <!-- Arbor "A" Badge -->
            <div class="w-7 h-7 shrink-0 rounded bg-fern-dark flex items-center justify-center text-white font-serif font-bold text-sm shadow-sm ring-1 ring-black/10">
              A
            </div>
            <div class="min-w-0">
              <div class="flex items-center space-x-1.5 leading-none">
                <span class="font-bold text-[13px] tracking-tight text-ink font-sans truncate">Arbor</span>
                <span class="text-[10px] px-1 py-0.5 rounded bg-emerald-50 text-fern-dark font-mono font-medium border border-fern/30">v2</span>
              </div>
              <div class="text-[10.5px] font-mono text-ink-muted tracking-tight truncate max-w-[140px] mt-0.5" id="headerDbName">
                Loading database...
              </div>
            </div>
          </div>

          <!-- Top Utility Controls (compact & 360px-safe) -->
          <div class="flex items-center space-x-1 shrink-0">
            <!-- Undo Button (shown when edits exist) -->
            <button id="btnListUndo" onclick="undoLastEdit()" title="Undo recent edit" class="hidden w-10 h-10 rounded-md bg-stone-100 border border-stone-200 text-stone-600 hover:text-ink flex items-center justify-center tap-active transition-colors">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M3 10h10a5 5 0 015 5v2m0 0l-4-4m4 4l4-4M3 10l4-4m-4 4l4 4"/>
              </svg>
            </button>

            <!-- Walk Mode (Wake Lock) Toggle -->
            <button id="btnListWakeLock" onclick="toggleWakeLock()" title="Keep screen awake during audit" class="w-10 h-10 rounded-md bg-stone-100 border border-stone-200 text-stone-600 hover:text-ink flex items-center justify-center tap-active transition-colors">
              <span id="listWakeLockIcon" class="text-xs">🌙</span>
            </button>

            <!-- Field Guide ("What the Fields Mean") Trigger -->
            <button id="btnOpenFieldGuide" onclick="openFieldGuideModal()" title="What the fields & badges mean" class="w-10 h-10 rounded-md bg-emerald-50 border border-fern/30 text-fern-dark hover:bg-emerald-100 flex items-center justify-center font-mono font-bold text-xs tap-active transition-colors">
              ?
            </button>

            <!-- Settings Trigger -->
            <button onclick="openSettingsModal()" title="Application Settings" class="w-10 h-10 rounded-md bg-stone-100 border border-stone-200 text-stone-600 hover:text-ink flex items-center justify-center tap-active transition-colors">
              <span class="text-xs font-mono">⚙️</span>
            </button>

            <!-- Connection Status Pill -->
            <div onclick="openModal('connectionModal')" class="flex items-center space-x-1 px-2 py-1.5 rounded-full bg-emerald-50 border border-emerald-200 text-[10px] font-mono font-medium text-emerald-800 cursor-pointer">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
              <span id="pingBadge">42ms</span>
            </div>
          </div>
        </div>

        <!-- Search Bar Row -->
        <div class="px-3.5 pb-2 pt-0.5">
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
              placeholder="Search object # or plant name..." 
              oninput="handleSearchInput()"
              autocomplete="off"
              spellcheck="false"
              class="w-full min-h-[42px] pl-10 pr-28 py-2 bg-stone-100/90 hover:bg-stone-100 focus:bg-white text-xs font-mono text-ink placeholder:text-ink-faint placeholder:font-sans rounded-lg border border-stone-200 focus:border-fern focus:ring-1 focus:ring-fern focus:outline-none transition-all shadow-inner"
            />
            <div class="absolute right-1 flex items-center space-x-0.5">
              <button id="btnInputModeToggle" type="button" onclick="toggleSearchInputMode()" class="min-w-[40px] min-h-[40px] px-1.5 rounded-md bg-stone-200/70 hover:bg-stone-300 text-[11px] font-mono font-bold text-stone-700 flex items-center justify-center transition-colors tap-active" title="Toggle numeric / text keyboard">
                123
              </button>
              <button id="searchClearBtn" onclick="clearSearch()" class="hidden min-w-[40px] min-h-[40px] flex items-center justify-center rounded-md bg-stone-200/80 hover:bg-stone-300 text-ink-muted hover:text-ink active:scale-95 text-xs font-bold leading-none transition-all" title="Clear search">
                ✕
              </button>
              <button id="btnFilterModalTrigger" onclick="openFilterModal()" title="Curatorial Filters" class="relative min-w-[40px] min-h-[40px] flex items-center justify-center rounded-md hover:bg-stone-200/70 text-ink-muted hover:text-ink transition-colors tap-active">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"/>
                </svg>
                <span id="filterActiveBadge" class="hidden absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-fern ring-2 ring-white"></span>
              </button>
            </div>
          </div>
        </div>

        <!-- 1b. Compact 1-Line Current Shelf Bar (tapping opens #stationSetupSheet bottom sheet) -->
        <div id="auditStationLaunchpad" class="px-3 py-1.5 bg-emerald-50/80 border-t border-b border-fern/20 text-xs">
          <div id="activeStationPill" class="flex items-center justify-between gap-1.5">
            <div class="flex items-center gap-1 min-w-0">
              <span class="text-xs shrink-0">📍</span>
              <span class="font-mono text-[10px] text-muted shrink-0">Shelf:</span>
              <span class="font-mono text-[11px] font-bold text-fern-dark truncate" id="activeStationPillText">Not set</span>
            </div>
            <button type="button" id="btnStationSheetTrigger" onclick="openStationSetup()" class="text-[11px] font-mono text-fern-dark bg-white/90 hover:bg-emerald-100 border border-fern/30 font-bold px-2.5 py-1 min-h-[40px] rounded shrink-0 whitespace-nowrap tap-active">
              Set Shelf
            </button>
          </div>
          <!-- Auto-dismissing first-time coach nudge (hides automatically once a shelf is set) -->
          <div id="listCoachNudge" class="hidden mt-1.5 pt-1.5 border-t border-fern/15 flex items-center justify-between gap-2 text-[11px] text-fern-dark">
            <span>👆 First step: tap <strong>Set Shelf</strong> where you’re standing, then search an object number.</span>
            <button type="button" onclick="dismissListCoachNudge()" class="px-1.5 py-0.5 text-muted hover:text-ink font-bold shrink-0" aria-label="Dismiss tip">✕</button>
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

        <!-- 2. Filter Pills Bar (Hidden by Default, Toggleable in Settings — Desktop Badge Parity) -->
        <div id="filterPillsContainer" class="hidden px-3.5 pb-2 overflow-x-auto no-scrollbar flex items-center gap-1.5 border-t border-stone-100 pt-2" style="-webkit-mask-image: linear-gradient(to right, black 92%, transparent 100%); mask-image: linear-gradient(to right, black 92%, transparent 100%);">
          <button onclick="setStatusFilter('all')" id="pill-all" class="filter-pill whitespace-nowrap px-3 py-1.5 min-h-[34px] rounded-full text-[11px] font-medium font-sans bg-ink text-white shadow-sm tap-active transition-all shrink-0">
            All <span class="font-mono text-[10px] ml-0.5 opacity-90" id="pillCountAll">(0)</span>
          </button>
          <button onclick="setStatusFilter('pending')" id="pill-pending" class="filter-pill whitespace-nowrap px-3 py-1.5 min-h-[34px] rounded-full text-[11px] font-medium font-sans bg-stone-200/80 text-ink-muted hover:bg-stone-300 tap-active transition-all shrink-0">
            UNREV <span class="font-mono text-[10px] ml-0.5" id="pillCountPending">(0)</span>
          </button>
          <button onclick="setStatusFilter('flagged')" id="pill-flagged" class="filter-pill whitespace-nowrap px-3 py-1.5 min-h-[34px] rounded-full text-[11px] font-medium font-sans bg-amber-50 text-amber-900 border border-amber-300 hover:bg-amber-100 tap-active transition-all shrink-0">
            ⚠ Flagged <span class="font-mono text-[10px] ml-0.5 font-bold" id="pillCountFlagged">(0)</span>
          </button>
          <button onclick="setStatusFilter('reviewed')" id="pill-reviewed" class="filter-pill whitespace-nowrap px-3 py-1.5 min-h-[34px] rounded-full text-[11px] font-medium font-sans bg-emerald-50 text-fern-dark border border-fern/30 hover:bg-emerald-100 tap-active transition-all shrink-0">
            ✓ REV <span class="font-mono text-[10px] ml-0.5" id="pillCountReviewed">(0)</span>
          </button>
          <button onclick="setStatusFilter('conflict')" id="pill-conflict" class="filter-pill whitespace-nowrap px-3 py-1.5 min-h-[34px] rounded-full text-[11px] font-medium font-sans bg-sky-50 text-sky-900 border border-sky-200 hover:bg-sky-100 tap-active transition-all shrink-0">
            CFCT <span class="font-mono text-[10px] ml-0.5" id="pillCountConflict">(0)</span>
          </button>
          <button onclick="setStatusFilter('unknown')" id="pill-unknown" class="filter-pill whitespace-nowrap px-3 py-1.5 min-h-[34px] rounded-full text-[11px] font-medium font-sans bg-stone-100 text-stone-700 border border-stone-200 hover:bg-stone-200 tap-active transition-all shrink-0">
            ? Unknown <span class="font-mono text-[10px] ml-0.5" id="pillCountUnknown">(0)</span>
          </button>
          <button onclick="toggleNoImageFilter()" id="pill-no-image" class="filter-pill whitespace-nowrap px-3 py-1.5 min-h-[34px] rounded-full text-[11px] font-medium font-sans bg-stone-100 text-stone-600 border border-stone-200 hover:bg-stone-200 tap-active transition-all shrink-0">
            📷 No Photo
          </button>
        </div>

        <!-- Metrics & Sort Row -->
        <div class="px-3.5 py-1.5 bg-alabaster/70 border-t border-bordercol flex items-center justify-between gap-2 text-[11px]">
          <div class="flex items-center gap-2 font-mono text-ink-muted min-w-0">
            <span class="truncate">Showing <span class="font-bold text-ink" id="matchingCount">0</span> records</span>
            <button type="button" id="btnOpenStationSetup" onclick="openStationSetup()" class="hidden min-h-[40px] text-[10.5px] font-mono font-bold text-fern-dark hover:underline px-2 py-1 rounded bg-emerald-50 border border-fern/30 shrink-0 whitespace-nowrap">
              📍 My Current Shelf
            </button>
          </div>
          <div class="flex items-center shrink-0">
            <select id="sortBySelect" onchange="handleSortChange()" class="arbor-compact-select min-h-[40px] bg-white border border-bordercol rounded-md pl-2.5 py-1 text-[11px] font-mono text-ink focus:outline-none focus:border-fern shadow-2xs cursor-pointer">
              <option value="id_asc" selected>Object # (1, 2, 3...)</option>
              <option value="location">⇅ Sort: Storage Location</option>
              <option value="name_asc">Scientific Name (A–Z)</option>
              <option value="name_desc">Scientific Name (Z–A)</option>
              <option value="flagged_first">Flagged / Problems First</option>
            </select>
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
      <header class="flex-none bg-surface border-b border-bordercol px-3 py-2 flex items-center justify-between gap-1 z-30">
        <!-- Back Button -->
        <button type="button" onclick="showListView()" class="flex items-center gap-1 px-2 py-1.5 min-h-[40px] -ml-1 text-xs font-semibold text-muted hover:text-ink active:bg-stone-100 rounded transition-colors tap-highlight-transparent shrink-0">
          <svg class="w-4 h-4 text-ink stroke-[2.2]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path d="M15.75 19.5L8.25 12l7.5-7.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span class="font-mono">List</span>
        </button>

        <!-- Steppers & Controls -->
        <div class="flex items-center gap-1">
          <!-- Field Guide ("What the Fields Mean") Trigger -->
          <button id="btnDetailFieldGuide" type="button" onclick="openFieldGuideModal()" title="What the fields & badges mean" class="w-10 h-10 rounded bg-emerald-50 border border-fern/30 text-fern-dark hover:bg-emerald-100 flex items-center justify-center font-mono font-bold text-xs tap-active transition-colors">
            ?
          </button>

          <!-- Detail Undo Button -->
          <button id="btnDetailUndo" onclick="undoLastEdit()" title="Undo edit" class="items-center gap-1 px-2.5 py-1 min-h-[40px] text-[11px] font-mono font-medium text-ember bg-orange-50 border border-orange-200 rounded active:scale-95 transition-all flex">
            <svg class="w-3.5 h-3.5 stroke-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path d="M9 15L3 9m0 0l6-6M3 9h12a6 6 0 010 12h-3" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>Undo</span>
          </button>

          <!-- Specimen Index Counter -->
          <span class="text-[11px] font-mono font-medium text-subdued tracking-tight bg-stone-100 px-1.5 py-1.5 rounded border border-bordercol/60">
            <span class="text-ink font-semibold" id="detailCurrentIdx">1</span><span class="text-stone-400 mx-0.5">/</span><span id="detailTotalCount">1</span>
          </span>

          <!-- Next / Prev Steppers (glove-friendly 40px touch targets) -->
          <div class="inline-flex rounded border border-bordercol bg-alabaster p-0.5 shadow-2xs">
            <button type="button" class="w-10 h-10 flex items-center justify-center rounded hover:bg-surface text-ink active:bg-stone-200 transition-colors tap-highlight-transparent" onclick="navSpecimen(-1)" title="Previous Specimen">
              <svg class="w-4 h-4 stroke-[2.2]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M15 19l-7-7 7-7" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </button>
            <div class="w-[1px] bg-bordercol my-0.5"></div>
            <button type="button" class="w-10 h-10 flex items-center justify-center rounded hover:bg-surface text-ink active:bg-stone-200 transition-colors tap-highlight-transparent" onclick="navSpecimen(1)" title="Next Specimen">
              <svg class="w-4 h-4 stroke-[2.2]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M9 5l7 7-7 7" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </button>
          </div>
        </div>
      </header>

      <!-- 2. Sticky Specimen Identification Header (compact for more form room) -->
      <section class="flex-none bg-surface border-b border-bordercol px-4 pt-2 pb-2 z-20 shadow-2xs">
        <div class="flex items-center justify-between gap-2 mb-1.5">
          <div class="flex items-center gap-1.5 min-w-0">
            <span class="font-mono text-xs font-bold text-ink tracking-tight px-1.5 py-0.5 bg-stone-100 border border-bordercol rounded shrink-0" id="detailAccession">
              #2024-BOT-0894
            </span>
            <span id="badgeLoanedHeader" onclick="event.stopPropagation(); showBadgeTooltip(this, 'LOAN')" role="button" tabindex="0" class="hidden inline-flex items-center gap-1 text-[10.5px] font-mono font-bold px-2 py-0.5 rounded bg-amber-100 text-amber-900 border border-amber-300 shrink-0 whitespace-nowrap cursor-help">
              ↗ Loaned Out
            </span>
          </div>
          <!-- Interactive Status Pill -->
          <button type="button" class="flex items-center gap-1.5 text-[11px] font-mono font-semibold px-2.5 py-1 min-h-[32px] rounded border transition-colors tap-highlight-transparent bg-amber-50 text-amber-800 border-amber-300 shrink-0" id="badgeStatus" onclick="handleReviewButtonClick()">
            <span class="w-1.5 h-1.5 rounded-full bg-amber-500 animate-pulse" id="badgeStatusDot"></span>
            <span id="badgeStatusText">UNREVIEWED</span>
          </button>
        </div>

        <h1 class="text-[19px] leading-tight font-serif font-semibold italic text-ink tracking-tight flex items-baseline gap-1.5 truncate" id="detailScientificName">
          Betula pendula
        </h1>

        <div class="flex items-center justify-between gap-2 mt-1.5 text-xs text-muted">
          <div class="min-w-0 flex-1 space-y-0.5">
            <div class="flex items-center gap-1 truncate">
              <span class="text-subdued font-medium shrink-0">Fam:</span>
              <span class="font-medium text-ink truncate" id="detailFamily">Betulaceae</span>
            </div>
            <div class="flex items-center gap-1 font-mono text-[11px] truncate">
              <span class="text-subdued font-sans shrink-0">Loc:</span>
              <span class="text-ink font-semibold truncate" id="headerLocSummary">Cab 04 · Sh 02 · Fl -1</span>
            </div>
          </div>
          <button type="button" id="btnOldNames" onclick="openOldNamesSheet()" class="px-3 py-1.5 min-h-[40px] rounded-full border border-bordercol bg-tonal1 hover:bg-stone-200/70 text-[11px] font-semibold text-ink-muted flex items-center gap-1 tap-active shrink-0" title="View older synonyms and family names for this specimen">
            <span>📜</span><span>Old names</span>
          </button>
        </div>

        <!-- Current Shelf Quick-Save Banner -->
        <div id="armedShelfBanner" class="mt-2 pt-2 border-t border-stone-100 flex items-center justify-between gap-1.5 text-xs">
          <div class="flex items-center gap-1 min-w-0">
            <span class="text-xs shrink-0">📍</span>
            <span class="font-mono text-[10px] text-muted shrink-0">Shelf:</span>
            <span class="font-mono text-[11px] font-bold text-fern-dark truncate" id="armedShelfHeaderLabel">Not set</span>
          </div>
          <button type="button" id="btnStampArmedShelf" onclick="stampArmedLocation()" class="hidden min-h-[40px] px-2.5 py-1.5 rounded bg-fern hover:bg-fern-dark text-white font-mono font-bold text-[11px] shadow-2xs tap-active flex items-center gap-1 shrink-0 whitespace-nowrap">
            <span>📍</span>
            <span>Save to Shelf</span>
          </button>
        </div>
      </section>

      <!-- 3. Segmented Tab Controller (Sticky: Data · Location · Problems) -->
      <nav class="flex-none bg-alabaster border-b border-bordercol px-3 pt-1.5 pb-1 z-20">
        <div class="relative bg-stone-200/90 p-1 rounded-[4px] flex items-center justify-between text-xs font-medium text-muted shadow-inner">
          <div class="tab-slider absolute top-1 bottom-1 w-[calc((100%-8px)/3)] bg-surface rounded shadow-sm border border-stone-300 pointer-events-none translate-x-0" id="tabIndicator" style="transform: translateX(0%);"></div>
          <button id="tabBtnDetails" class="tab-btn relative z-10 flex-1 py-1.5 min-h-[40px] flex items-center justify-center gap-1 font-semibold text-ink whitespace-nowrap tap-highlight-transparent" data-tab-index="0" onclick="switchDetailTab('details')">
            <svg class="w-3.5 h-3.5 stroke-2 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
            <span>Data</span>
            <span class="font-mono text-[10px] font-bold px-1.5 rounded-full bg-brick text-white shadow-2xs hidden shrink-0" id="tabDetailsFlagsBadge" style="background:#c93a40;color:#ffffff;">0</span>
            <span class="font-mono text-[10px] font-bold px-1.5 rounded-full bg-slate-600 text-white shadow-2xs hidden shrink-0" id="tabFolioBadge">0</span>
          </button>
          <button id="tabBtnLocation" class="tab-btn relative z-10 flex-1 py-1.5 min-h-[40px] flex items-center justify-center gap-1 text-muted whitespace-nowrap tap-highlight-transparent" data-tab-index="1" onclick="switchDetailTab('location')">
            <svg class="w-3.5 h-3.5 stroke-2 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z"/><path d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z"/></svg>
            <span>Location</span>
            <span class="font-mono text-[10px] font-bold px-1.5 rounded-full shadow-2xs hidden whitespace-nowrap shrink-0" id="tabLocationBadge"></span>
          </button>
          <button id="tabBtnHistory" class="tab-btn relative z-10 flex-1 py-1.5 min-h-[40px] flex items-center justify-center gap-1 text-muted whitespace-nowrap tap-highlight-transparent" data-tab-index="2" onclick="switchDetailTab('history')">
            <svg class="w-3.5 h-3.5 text-sky-700 stroke-2 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25"/></svg>
            <span>Problems</span>
            <span class="font-mono text-[10px] font-bold px-1.5 rounded-full text-white shadow-2xs hidden shrink-0" id="tabHistoryBadge" style="background:#4a7b9d;color:#ffffff;">0</span>
          </button>
        </div>
      </nav>

      <!-- 4. Horizontal Swipeable Tab Track -->
      <div class="flex-1 overflow-hidden relative" id="swipeArea">
        <!-- Detail Loading & Error Recovery Overlay (blocks accidental taps on previous specimen) -->
        <div id="detailLoadingOverlay" class="hidden absolute inset-0 z-20 bg-alabaster/95 flex flex-col items-center justify-center p-6 text-center">
          <div id="detailLoadingSpinner" class="flex flex-col items-center gap-3">
            <div class="w-8 h-8 border-2 border-forest/25 border-t-forest rounded-full animate-spin"></div>
            <p class="text-sm font-semibold text-ink">Loading specimen…</p>
          </div>
          <div id="detailLoadingError" class="hidden flex flex-col items-center gap-3 max-w-xs">
            <p class="text-sm font-semibold text-red-700" id="detailLoadingErrorMsg">Could not load specimen.</p>
            <div class="flex items-center gap-2">
              <button type="button" onclick="retryCurrentSpecimen()" class="px-4 py-2 min-h-[40px] rounded-md bg-emerald-700 text-white text-xs font-semibold shadow-sm" style="background:#2d5a3c;color:#ffffff;">Retry</button>
              <button type="button" onclick="showListView()" class="px-4 py-2 min-h-[40px] rounded-md border border-bordercol bg-surface text-ink text-xs font-semibold">Back to List</button>
            </div>
          </div>
        </div>
        <div class="h-full flex w-[300%]" id="tabTrack" style="transform: translateX(0%);">

          <!-- ================= TAB 0: DETAILS & ARCHIVAL SCANS ================= -->
          <div class="w-1/3 h-full overflow-y-auto no-scrollbar p-4 space-y-3.5 pb-24" id="tabContentDetails">
            <!-- Image Viewer Container -->
            <div class="bg-surface border border-bordercol rounded p-3 shadow-2xs space-y-2" id="photoFolioContainer">
              <div class="flex items-center justify-between">
                <h3 class="text-xs font-bold text-ink uppercase tracking-wider font-sans">Specimen Photos</h3>
                <span class="text-[10px] font-mono text-muted" id="photoCountDisplay">0 Photos</span>
              </div>
              <div id="photoMainBox" class="relative w-full h-48 bg-stone-100 rounded border border-bordercol overflow-hidden flex items-center justify-center cursor-pointer" onclick="openPhotoViewerModal()">
                <img id="specimenImg" alt="Specimen Scan" class="w-full h-full object-contain hidden" onload="if(window.onPhotoLoaded)onPhotoLoaded(this)" onerror="if(window.onPhotoError)onPhotoError(this)"/>
              </div>
              <div id="photoPlaceholder" class="w-full"></div>
              <div id="photoThumbnailsRow" class="flex items-center gap-2 overflow-x-auto no-scrollbar pt-1">
                <!-- Thumbnails injected dynamically -->
              </div>
            </div>

            <!-- Compact Flagged-Fields Jump Chip (shown when ≥1 problem checkbox is active) -->
            <button type="button" id="detailsFlagSummaryChip" onclick="scrollToFirstFlaggedField()" class="hidden w-full text-left px-3 py-2 min-h-[40px] rounded bg-amber-50 border border-amber-300 text-amber-900 text-xs font-sans font-semibold flex items-center justify-between gap-2 tap-active">
              <span id="detailsFlagSummaryText" class="truncate">⚠ 0 flagged</span>
              <span class="font-mono text-[10px] text-amber-800 shrink-0">Jump ↓</span>
            </button>

            <!-- Registration & Observation Metadata Form Fields (with inline problem checkboxes) -->
            <div class="bg-surface border border-bordercol rounded p-3.5 shadow-2xs space-y-3" id="dynamicFormContainer">
              <!-- Form fields injected dynamically from schema -->
            </div>

            <!-- Photo & Media Issues Checklist (Non-field flags like Images Issue; Other_problem lives above Comment) -->
            <div class="bg-surface border border-bordercol rounded p-3.5 shadow-2xs space-y-2.5" id="physicalIssuesCard">
              <div class="flex items-center justify-between border-b border-stone-100 pb-2">
                <div>
                  <h3 class="text-xs font-bold text-ink uppercase tracking-wider font-sans">Photo &amp; Media Issues</h3>
                  <p class="text-[10.5px] font-sans text-subdued">Flag missing or blurry photo problems here</p>
                </div>
                <span class="text-[10px] font-mono text-muted" id="flaggedTotalBadge">0 Flagged</span>
              </div>
              <div class="grid grid-cols-2 gap-2" id="problemFlagsGrid">
                <!-- Dynamically populated from non-field schema.ui_sections.problems (excluding Other_problem) -->
              </div>
            </div>
          </div>

          <!-- ================= TAB 1: LOCATION ================= -->
          <div class="w-1/3 h-full overflow-y-auto no-scrollbar p-4 space-y-3.5 pb-24" id="tabContentLocation">
            <!-- 1. Copy from Previous Bar (auto-hidden when My Current Shelf is already set) -->
            <div id="copyPrevSpecimenCard" class="bg-surface border border-bordercol rounded p-2.5 shadow-2xs">
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

            <!-- 2. Main Storage Location Card -->
            <section class="bg-stone-50 border border-bordercol rounded-lg p-3 space-y-2.5 shadow-2xs">
              <div class="flex items-center justify-between">
                <div>
                  <h2 class="text-xs font-bold text-ink uppercase tracking-wider font-sans">Storage Location</h2>
                  <p class="text-[10px] font-sans text-subdued">Where this object lives so we can find it again</p>
                </div>
                <span class="text-[10px] font-mono text-fern font-semibold flex items-center gap-1 shrink-0" id="locSyncIndicator">
                  <svg class="w-3.5 h-3.5 stroke-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M4.5 12.75l6 6 9-13.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
                  Synced
                </span>
              </div>

              <div class="grid grid-cols-2 gap-2">
                <!-- Building (Default blank: --) -->
                <div class="bg-white rounded px-2 py-1 border border-bordercol flex items-center justify-between gap-1">
                  <span class="font-mono text-[9px] uppercase font-bold text-muted shrink-0">Bldg</span>
                  <select id="detailBuildingSelect" onchange="handleDetailBuildingChange(this.value)" class="arbor-compact-select bg-transparent border-0 py-1 min-h-[40px] font-mono text-xs font-bold text-ink outline-none focus:ring-0 text-right min-w-0 flex-1">
                    <option value="">--</option>
                  </select>
                </div>
                <!-- Floor (Continuous signed integer: -2, -1, 0, 1, 2... or — when unrecorded) -->
                <div class="bg-white rounded p-2 border border-bordercol flex items-center justify-between gap-1">
                  <span class="font-mono text-[9px] uppercase font-bold text-muted shrink-0">Floor</span>
                  <div class="flex items-center gap-1">
                    <button type="button" class="w-9 h-9 rounded bg-stone-100 flex items-center justify-center font-mono font-bold text-base shrink-0" onclick="adjustCoordinate('floor', -1)">−</button>
                    <span class="font-mono text-xs font-bold text-ink px-0.5 min-w-[20px] text-center" id="detailFloorVal">—</span>
                    <button type="button" class="w-9 h-9 rounded bg-stone-100 flex items-center justify-center font-mono font-bold text-base shrink-0" onclick="adjustCoordinate('floor', 1)">+</button>
                  </div>
                </div>
                <!-- Cabinet (01, 02... or — when unrecorded) -->
                <div class="bg-white rounded p-2 border border-bordercol space-y-1">
                  <span class="font-mono text-[10px] uppercase font-bold text-muted block">Cabinet</span>
                  <div class="flex items-center justify-between gap-1">
                    <button type="button" class="w-9 h-9 rounded bg-stone-100 flex items-center justify-center font-mono font-bold text-base shrink-0" onclick="adjustCoordinate('cab', -1)">−</button>
                    <input type="text" inputmode="numeric" pattern="[0-9]*" id="detailCabVal"
                      class="font-mono text-base font-bold text-ink w-14 min-w-[48px] text-center bg-transparent border-b border-bordercol/40 focus:border-fern focus:bg-stone-50 rounded-xs outline-none transition-colors px-1"
                      placeholder="—"
                      onclick="this.select()"
                      onfocus="this.select()"
                      onkeydown="if(event.key==='Enter') this.blur();"
                      onchange="handleDirectCoordinateInput('cab', this.value)"
                      onblur="handleDirectCoordinateBlur('cab', this)" />
                    <button type="button" class="w-9 h-9 rounded bg-stone-100 flex items-center justify-center font-mono font-bold text-base shrink-0" onclick="adjustCoordinate('cab', 1)">+</button>
                  </div>
                </div>
                <!-- Shelf (Highlighted Fern Border, 01, 02... or — when unrecorded) -->
                <div class="bg-white rounded p-2 border-2 border-fern space-y-1">
                  <span class="font-mono text-[10px] uppercase font-bold text-fern-dark block">Shelf</span>
                  <div class="flex items-center justify-between gap-1">
                    <button type="button" class="w-9 h-9 rounded bg-stone-100 flex items-center justify-center font-mono font-bold text-base shrink-0" onclick="adjustCoordinate('shelf', -1)">−</button>
                    <input type="text" inputmode="numeric" pattern="[0-9]*" id="detailShelfVal"
                      class="font-mono text-base font-bold text-fern-dark w-14 min-w-[48px] text-center bg-transparent border-b border-fern/40 focus:border-fern focus:bg-emerald-50/50 rounded-xs outline-none transition-colors px-1"
                      placeholder="—"
                      onclick="this.select()"
                      onfocus="this.select()"
                      onkeydown="if(event.key==='Enter') this.blur();"
                      onchange="handleDirectCoordinateInput('shelf', this.value)"
                      onblur="handleDirectCoordinateBlur('shelf', this)" />
                    <button type="button" class="w-9 h-9 rounded bg-stone-100 flex items-center justify-center font-mono font-bold text-base shrink-0" onclick="adjustCoordinate('shelf', 1)">+</button>
                  </div>
                </div>
              </div>

              <!-- Stored As Selector (Opens clean full-width Bottom Sheet) -->
              <div class="pt-1">
                <button type="button" id="btnOpenDetailStoredAs" onclick="openDetailStoredAsSheet()" class="w-full min-h-[44px] bg-white hover:bg-stone-50 border border-bordercol rounded px-3 py-2 flex items-center justify-between gap-2 text-left tap-active transition-colors">
                  <div class="min-w-0">
                    <span class="font-mono text-[9px] uppercase text-muted font-bold block leading-none mb-0.5">Stored As</span>
                    <span class="font-mono text-xs text-ink font-semibold block truncate" id="detailStoredAsLabel">Not Selected</span>
                  </div>
                  <span class="text-xs font-mono text-fern-dark font-bold shrink-0">Choose ▾</span>
                </button>
                <div class="hidden" id="detailStoredAsPills"></div>
                <div id="detailStoredAsCustomContainer" class="hidden mt-1.5">
                  <input type="text" id="detailStoredAsCustomInput" oninput="onDetailCustomStorageInput(this.value)" placeholder="Enter custom storage..." class="w-full min-h-[40px] bg-white border border-bordercol rounded px-2.5 py-2 text-xs font-mono text-ink focus:outline-none focus:border-fern">
                </div>
              </div>

              <!-- Live Breadcrumb Trail -->
              <div class="bg-stone-100 border border-bordercol/60 rounded px-2.5 py-1.5 flex items-center justify-between gap-1.5 text-[11px] font-mono mt-1">
                <div class="flex items-center gap-1.5 text-ink min-w-0 flex-1 flex-wrap">
                  <span class="text-subdued uppercase text-[9px] font-sans font-bold shrink-0">Saved:</span>
                  <span class="font-semibold break-words" id="liveLocBreadcrumb">Unrecorded location</span>
                </div>
                <span class="hidden" id="liveLocStatus"></span>
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
                <button class="py-2 px-2 rounded text-xs font-mono font-semibold flex items-center justify-center gap-1.5 transition-all bg-white text-ink border border-stone-300 min-h-[42px]" id="btnStatusAvailable" onclick="setLoanStatus(false)" type="button">
                  <svg class="w-3.5 h-3.5 text-fern stroke-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                  <span>In Collection</span>
                </button>
                <button class="py-2 px-2 rounded text-xs font-mono font-medium flex items-center justify-center gap-1.5 transition-all text-muted hover:text-ink min-h-[42px]" id="btnStatusLoan" onclick="setLoanStatus(true)" type="button">
                  <svg class="w-3.5 h-3.5 text-amber-600 stroke-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M13.5 6H5.25A2.25 2.25 0 003 8.25v10.5A2.25 2.25 0 005.25 21h10.5A2.25 2.25 0 0018 18.75V10.5m-10.5 6L21 3m0 0h-5.25M21 3v5.25"/></svg>
                  <span>Loaned Out</span>
                </button>
              </div>
            </div>
          </div>

          <!-- ================= TAB 2: HISTORY (PROBLEM RESOLUTION) ================= -->
          <div class="w-1/3 h-full overflow-y-auto no-scrollbar p-4 space-y-3.5 pb-24" id="tabContentHistory">
            <!-- 0. Problem Resolution Heading -->
            <div class="space-y-0.5">
              <h3 class="text-sm font-serif font-bold text-ink">Problem Resolution</h3>
              <p class="text-[11px] font-sans text-muted">Compare with the label in your hand.</p>
            </div>

            <!-- 1. Historical Summary Banner -->
            <div id="problemSummaryBar" class="flex items-center justify-between p-3 bg-stone-100 border border-bordercol rounded-[3px] transition-colors duration-200">
              <div class="flex items-center gap-2">
                <span id="problemSummaryDot" class="w-2.5 h-2.5 rounded-full bg-stone-400"></span>
                <span id="problemSummaryCountText" class="text-xs font-bold text-ink uppercase font-mono">Nothing to resolve</span>
              </div>
              <span id="problemSummaryActionText" class="text-[10px] font-mono text-muted">Checking Books</span>
            </div>

            <!-- 2. Historical Suggestion & Conflict Resolver Cards Container -->
            <div id="activeDiscrepanciesContainer" class="space-y-3">
              <!-- Dynamically populated with older catalog book comparisons -->
            </div>
          </div>

        </div>
      </div>

      <!-- Sticky Action Bar in Detail View: Mark Reviewed & Needs Specialist -->
      <footer class="flex-none bg-surface border-t border-bordercol px-4 py-2.5 shadow-[0_-2px_10px_rgba(0,0,0,0.05)] z-30">
        <div class="flex items-center justify-between gap-3">
          <button
            type="button"
            id="btnDetailMarkReviewed"
            onclick="handleReviewButtonClick()"
            class="flex-1 min-h-[42px] py-2.5 px-4 rounded font-sans font-bold text-xs flex items-center justify-center gap-2 border transition-all tap-active bg-emerald-50 text-fern-dark border-fern hover:bg-emerald-100"
          >
            <span id="btnDetailReviewedIcon" class="text-sm">✓</span>
            <span id="btnDetailReviewedLabel">Mark Reviewed</span>
          </button>
          <button
            type="button"
            id="btnDetailNeedsSpecialist"
            onclick="handleBottomNeedsSpecialistClick()"
            aria-pressed="false"
            class="min-h-[42px] px-3.5 py-2.5 bg-white hover:bg-stone-50 text-muted border border-stone-300 rounded font-sans font-semibold text-xs flex items-center justify-center gap-1.5 transition-colors tap-active"
            title="Flag broken objects or storage, or mixed specimen for a specialist"
          >
            <span>⚑</span>
            <span>Needs Specialist</span>
          </button>
        </div>
        <p id="reviewHelperText" class="text-[10.5px] leading-snug font-sans text-subdued text-center mt-1.5"></p>
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
            <div class="bg-white rounded p-1.5 border border-bordercol flex items-center justify-between gap-1">
              <span class="font-mono text-[9px] uppercase font-bold text-muted shrink-0">Bldg</span>
              <select id="batchBuildingSelect" onchange="handleBatchBuildingChange(this.value)" class="arbor-compact-select bg-transparent border-0 p-0 min-h-[36px] font-mono text-xs font-bold text-ink outline-none focus:ring-0 text-right min-w-0">
                <option value="">--</option>
              </select>
            </div>
            <!-- Floor (Continuous signed integer) -->
            <div class="bg-white rounded p-1.5 border border-bordercol flex items-center justify-between gap-1">
              <span class="font-mono text-[9px] uppercase font-bold text-muted shrink-0">Floor</span>
              <div class="flex items-center gap-1">
                <button type="button" class="min-w-[36px] min-h-[36px] rounded bg-stone-100 hover:bg-stone-200 flex items-center justify-center font-mono font-bold text-sm tap-active" onclick="adjustBatchCoord('floor', -1)">−</button>
                <span class="font-mono text-xs font-bold text-ink px-0.5 min-w-[20px] text-center" id="batchFloorVal">—</span>
                <button type="button" class="min-w-[36px] min-h-[36px] rounded bg-stone-100 hover:bg-stone-200 flex items-center justify-center font-mono font-bold text-sm tap-active" onclick="adjustBatchCoord('floor', 1)">+</button>
              </div>
            </div>
            <!-- Cabinet -->
            <div class="bg-white rounded p-1.5 border border-bordercol flex items-center justify-between gap-1">
              <span class="font-mono text-[9px] uppercase font-bold text-muted shrink-0">Cab</span>
              <div class="flex items-center gap-1">
                <button type="button" class="min-w-[36px] min-h-[36px] rounded bg-stone-100 hover:bg-stone-200 flex items-center justify-center font-mono font-bold text-sm tap-active" onclick="adjustBatchCoord('cab', -1)">−</button>
                <input type="text" inputmode="numeric" pattern="[0-9]*" id="batchCabVal"
                  class="font-mono text-sm font-bold text-ink w-8 text-center bg-transparent border-b border-bordercol/30 focus:border-fern focus:bg-stone-50 rounded-xs outline-none transition-colors"
                  placeholder="—"
                  onclick="this.select()"
                  onfocus="this.select()"
                  onkeydown="if(event.key==='Enter') this.blur();"
                  onchange="handleDirectBatchCoordInput('cab', this.value)"
                  onblur="handleDirectBatchCoordBlur('cab', this)" />
                <button type="button" class="min-w-[36px] min-h-[36px] rounded bg-stone-100 hover:bg-stone-200 flex items-center justify-center font-mono font-bold text-sm tap-active" onclick="adjustBatchCoord('cab', 1)">+</button>
              </div>
            </div>
            <!-- Shelf -->
            <div class="bg-white rounded p-1.5 border-2 border-fern flex items-center justify-between gap-1">
              <span class="font-mono text-[9px] uppercase font-bold text-fern-dark shrink-0">Shelf</span>
              <div class="flex items-center gap-1">
                <button type="button" class="min-w-[36px] min-h-[36px] rounded bg-stone-100 hover:bg-stone-200 flex items-center justify-center font-mono font-bold text-sm tap-active" onclick="adjustBatchCoord('shelf', -1)">−</button>
                <input type="text" inputmode="numeric" pattern="[0-9]*" id="batchShelfVal"
                  class="font-mono text-sm font-bold text-fern-dark w-8 text-center bg-transparent border-b border-fern/40 focus:border-fern focus:bg-emerald-50/50 rounded-xs outline-none transition-colors"
                  placeholder="—"
                  onclick="this.select()"
                  onfocus="this.select()"
                  onkeydown="if(event.key==='Enter') this.blur();"
                  onchange="handleDirectBatchCoordInput('shelf', this.value)"
                  onblur="handleDirectBatchCoordBlur('shelf', this)" />
                <button type="button" class="min-w-[36px] min-h-[36px] rounded bg-stone-100 hover:bg-stone-200 flex items-center justify-center font-mono font-bold text-sm tap-active" onclick="adjustBatchCoord('shelf', 1)">+</button>
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
            <h2 class="font-sans font-bold text-sm text-ink">Save Current Shelf Location?</h2>
          </div>
          <button type="button" onclick="cancelArmedModal()" class="text-ink-muted hover:text-ink font-bold text-sm min-w-[32px] min-h-[32px]">✕</button>
        </header>
        <div class="p-4 space-y-3.5">
          <p class="text-xs text-muted leading-relaxed">
            This specimen's saved location does not match your Current Shelf.
          </p>
          <div class="space-y-2 bg-stone-50 p-3 rounded border border-bordercol/70 text-xs font-mono">
            <div class="flex items-center justify-between">
              <span class="text-muted">Saved Location:</span>
              <span class="font-bold text-ink" id="armedModalCurLoc">Unrecorded</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-fern-dark font-bold">Current Shelf:</span>
              <span class="font-bold text-fern-dark" id="armedModalTargetLoc">Cabinet 21, Shelf 02</span>
            </div>
          </div>
          <p class="text-[11px] text-muted italic">
            You can save your Current Shelf or keep the existing location. Both choices will safely mark the specimen reviewed.
          </p>
          <div class="space-y-2 pt-1">
            <button type="button" id="btnConfirmStampAndReview" onclick="confirmStampAndReview()" class="w-full py-2.5 px-3 min-h-[40px] bg-fern hover:bg-fern-dark text-white rounded font-sans font-bold text-xs flex items-center justify-center gap-1.5 shadow-sm tap-active transition-all">
              <span>✓ Yes, Save Shelf & Review</span>
            </button>
            <button type="button" id="btnConfirmKeepAndReview" onclick="confirmKeepAndReview()" class="w-full py-2.5 px-3 min-h-[40px] bg-stone-100 hover:bg-stone-200 text-ink border border-stone-300 rounded font-sans font-bold text-xs flex items-center justify-center gap-1.5 tap-active transition-all">
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

          <!-- Advanced Tools (Hidden from main top bar to keep hallway view simple) -->
          <div class="p-2.5 bg-stone-50 border border-bordercol rounded space-y-1.5">
            <span class="block font-sans text-xs font-bold text-ink">Advanced Tools</span>
            <button type="button" id="btnOpenBatchLocation" onclick="closeSettingsModal(); showBatchLocationView();" class="w-full min-h-[40px] px-3 py-2 rounded bg-white hover:bg-emerald-50 border border-bordercol hover:border-fern/40 text-left flex items-center justify-between gap-2 tap-active transition-colors">
              <div>
                <span class="block font-sans text-xs font-semibold text-ink">Batch Location Registrator</span>
                <span class="block font-sans text-[10px] text-muted">Queue multiple object numbers for one shelf</span>
              </div>
              <span class="text-xs font-mono text-fern-dark font-bold">Open →</span>
            </button>
          </div>

          <!-- Phone Tutorial & Contextual Tips -->
          <div id="settingsPhoneTutorialSection" class="p-2.5 bg-emerald-50/50 border border-fern/30 rounded space-y-2.5">
            <div class="flex items-center justify-between gap-2">
              <span class="block font-sans text-xs font-bold text-ink">🎓 Phone tutorial</span>
              <label class="flex items-center gap-1.5 text-[11px] font-sans text-ink-muted cursor-pointer">
                <input type="checkbox" id="settingEnableCoachTips" onchange="toggleCoachTipsEnabled(this.checked)" class="w-4 h-4 accent-fern rounded" />
                <span>Tips on</span>
              </label>
            </div>
            <div class="grid grid-cols-1 gap-1.5">
              <button type="button" id="btnStartTraineeTutorial" onclick="closeSettingsModal(); startPhoneTutorial('trainee');" class="w-full min-h-[40px] px-3 py-2 rounded bg-fern hover:bg-fern-dark text-white text-xs font-bold text-left flex items-center justify-between tap-active transition-colors" style="background:#3a7d44;color:#ffffff;">
                <span>Start Trainee tutorial</span>
                <span class="font-mono text-[10px] opacity-90">5 steps →</span>
              </button>
              <button type="button" id="btnStartHelperTutorial" onclick="closeSettingsModal(); startPhoneTutorial('helper');" class="w-full min-h-[40px] px-3 py-2 rounded bg-white hover:bg-emerald-50 border border-fern/40 text-fern-dark text-xs font-bold text-left flex items-center justify-between tap-active transition-colors">
                <span>Start Helper tutorial</span>
                <span class="font-mono text-[10px]">4 steps →</span>
              </button>
            </div>
            <div class="pt-1.5 border-t border-fern/20 space-y-1">
              <div class="flex items-center justify-between">
                <span class="text-[10.5px] font-mono font-bold uppercase text-ink-muted">Tips seen</span>
                <button type="button" id="btnResetCoachTips" onclick="resetCoachTips()" class="text-[11px] font-mono font-semibold text-fern-dark hover:underline px-2 py-1 min-h-[32px]">Reset tips</button>
              </div>
              <div id="settingsTipsList" class="space-y-1 text-[11px] font-sans text-ink"></div>
            </div>
          </div>

          <div class="pt-2 border-t border-tonal2 flex items-center justify-end gap-2">
            <button type="button" onclick="closeSettingsModal()" class="px-4 py-2 min-h-[40px] border border-bordercol text-ink-muted hover:bg-surface rounded text-xs font-medium">Cancel</button>
            <button type="button" onclick="saveSettings()" class="px-4 py-2 min-h-[40px] bg-fern hover:bg-fern-dark text-white rounded text-xs font-bold">Save</button>
          </div>
        </div>
      </div>
    </div>

    <!-- MODAL: What the Fields Mean (Mirrors the Specimen Page) -->
    <div id="fieldGuideModal" class="hidden fixed inset-0 z-50 bg-black/70 backdrop-blur-xs flex items-center justify-center p-3">
      <div class="bg-surface border border-bordercol rounded-xl shadow-2xl w-full max-w-md max-h-[88vh] flex flex-col overflow-hidden">
        <div class="flex-none px-4 py-2.5 bg-fern text-white flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="text-base">📖</span>
            <span class="font-sans font-bold text-xs tracking-wide uppercase">What the Fields Mean</span>
          </div>
          <button type="button" onclick="closeFieldGuideModal()" class="min-h-[40px] px-3 py-1.5 text-white/95 hover:text-white hover:bg-white/10 text-xs font-bold rounded tap-active">✕ Close</button>
        </div>
        <div id="fieldGuideBody" class="flex-1 overflow-y-auto p-3.5 space-y-3 text-xs font-sans text-ink bg-canvas">
          <!-- Populated dynamically by openFieldGuideModal() to mirror the specimen page -->
        </div>
        <div class="flex-none px-3.5 py-2.5 bg-surface border-t border-bordercol flex items-center justify-between gap-2">
          <button type="button" onclick="closeFieldGuideModal(); openSettingsTutorialSection();" class="min-h-[40px] px-3 py-2 rounded bg-fern-light border border-fern/40 text-fern-dark font-bold text-xs tap-active">🎓 Phone tutorial…</button>
          <button type="button" onclick="closeFieldGuideModal()" class="min-h-[40px] px-4 py-2 rounded bg-fern text-white font-bold text-xs tap-active">Got it</button>
        </div>
      </div>
    </div>

    <!-- FLOATING COACH CARD: Hands-On Phone Tutorial & Contextual Tips (above sticky bottom bar, below modals) -->
    <div id="coachCard" class="hidden fixed left-3 right-3 bottom-[92px] max-w-[440px] mx-auto z-40 bg-[#181c19] text-[#f3f6f4] border-2 border-[#3a7d44] rounded-xl shadow-2xl p-3.5 space-y-2.5" role="region" aria-label="Phone tutorial coach">
      <div class="flex items-center justify-between gap-2">
        <span id="coachBadge" class="inline-block px-2 py-0.5 rounded-full bg-[#1e3a24] text-[#85e89d] font-mono text-[10px] font-bold tracking-wide uppercase">TRAINEE · STEP 1 OF 5</span>
        <button type="button" id="coachExitBtn" onclick="exitPhoneTutorial()" class="min-w-[40px] min-h-[40px] -my-1.5 -mr-1.5 rounded-lg text-[#a2aba5] hover:text-white hover:bg-white/10 flex items-center justify-center text-sm font-bold tap-active" aria-label="Exit tutorial" title="Exit tutorial">✕</button>
      </div>
      <h3 id="coachTitle" class="font-sans font-bold text-sm text-white leading-snug"></h3>
      <p id="coachBody" aria-live="polite" class="font-sans text-xs text-[#e8ebe9] leading-relaxed"></p>
      <div id="coachStatus" class="hidden font-mono text-[11px] font-semibold text-[#85e89d]"></div>
      <!-- Chooser Mode Actions -->
      <div id="coachChooserActions" class="hidden space-y-1.5 pt-1">
        <button type="button" onclick="startPhoneTutorial('trainee')" class="w-full min-h-[42px] px-3 py-2 rounded-lg bg-[#3a7d44] hover:bg-[#4c9a58] text-white text-xs font-bold text-left tap-active">I've done the desktop tutorial</button>
        <button type="button" onclick="startPhoneTutorial('helper')" class="w-full min-h-[42px] px-3 py-2 rounded-lg bg-[#263128] hover:bg-[#314234] border border-[#52b765]/50 text-[#e8ebe9] text-xs font-bold text-left tap-active">I'm new / helping out today</button>
        <button type="button" onclick="dismissPhoneTutorialChooser()" class="w-full min-h-[40px] px-3 py-1.5 rounded-lg text-[#a2aba5] hover:text-white text-xs font-medium text-center tap-active">Not now</button>
      </div>
      <!-- Step Mode Actions -->
      <div id="coachStepActions" class="hidden pt-1 flex items-center justify-between gap-2">
        <div class="flex items-center gap-1.5">
          <button type="button" id="coachBackBtn" onclick="coachPrevStep()" class="min-h-[40px] px-3 py-1.5 rounded-lg bg-[#212622] hover:bg-[#2c332e] border border-white/10 text-[#e8ebe9] text-xs font-semibold tap-active">← Back</button>
          <button type="button" id="coachSkipBtn" onclick="coachNextStep()" class="min-h-[40px] px-3 py-1.5 rounded-lg bg-[#212622] hover:bg-[#2c332e] border border-white/10 text-[#a2aba5] hover:text-white text-xs font-medium tap-active">Skip step</button>
        </div>
        <button type="button" id="coachNextBtn" onclick="coachNextStep()" class="min-h-[40px] px-4 py-1.5 rounded-lg bg-[#3a7d44] hover:bg-[#4c9a58] text-white text-xs font-bold tap-active">Next →</button>
      </div>
      <!-- Tip Mode Actions -->
      <div id="coachTipActions" class="hidden pt-1 flex items-center justify-between gap-2">
        <button type="button" onclick="disableCoachTipsFromCard()" class="min-h-[40px] px-3 py-1.5 rounded-lg text-[#a2aba5] hover:text-white text-xs font-medium tap-active">Don't show tips</button>
        <button type="button" onclick="dismissCoachTip()" class="min-h-[40px] px-4 py-1.5 rounded-lg bg-[#3a7d44] hover:bg-[#4c9a58] text-white text-xs font-bold tap-active">Got it</button>
      </div>
    </div>

    <!-- MODAL: Old Names / Synonyms Bottom Sheet (1-tap, read-only) -->
    <div id="oldNamesSheet" class="hidden fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex flex-col justify-end" onclick="if(event.target===this)closeOldNamesSheet()">
      <div id="oldNamesSheetCard" class="w-full max-w-[440px] mx-auto bg-surface border-t border-bordercol rounded-t-xl p-4 space-y-3 max-h-[82vh] flex flex-col shadow-2xl">
        <div class="w-10 h-1 bg-stone-300 rounded-full mx-auto -mt-1 shrink-0"></div>
        <div class="flex items-start justify-between gap-2 pb-2 border-b border-stone-200 shrink-0">
          <div class="min-w-0">
            <h3 class="text-xs font-bold text-ink uppercase tracking-wider font-sans">Old Names &amp; Synonyms</h3>
            <p id="oldNamesRegisteredLbl" class="text-sm font-serif italic text-ink-muted truncate mt-0.5">—</p>
          </div>
          <button type="button" onclick="closeOldNamesSheet()" class="min-w-[40px] min-h-[40px] rounded-md text-muted hover:text-ink hover:bg-stone-100 flex items-center justify-center text-base font-bold tap-active" aria-label="Close">✕</button>
        </div>

        <div id="oldNamesBody" class="overflow-y-auto space-y-3 flex-1 pr-0.5 text-sm">
          <!-- Populated dynamically on tap -->
        </div>

        <!-- Optional quiet filter / GBIF fallback box (avoid typing unless needed) -->
        <div class="pt-2 border-t border-stone-200 space-y-2 shrink-0">
          <input type="text" id="oldNamesFilterInput" oninput="filterOldNamesList()" placeholder="Don't see the label name? Filter or check…" class="w-full min-h-[40px] px-3 py-2 text-xs rounded-md border border-bordercol bg-alabaster text-ink focus:outline-none focus:border-fern" autocomplete="off" />
          <div id="oldNamesGbifFallback" class="hidden flex items-center justify-between gap-2">
            <span class="text-[11px] text-muted">No match in loaded list.</span>
            <button type="button" id="btnCheckLabelGbif" onclick="checkLabelAgainstGbif()" class="px-3.5 py-2 min-h-[40px] rounded-md text-xs font-semibold text-white shrink-0 tap-active" style="background:#2d5a3c;color:#ffffff;">Check in GBIF</button>
          </div>
          <div id="oldNamesVerdictBox" class="hidden rounded-md p-2.5 text-xs space-y-2"></div>
        </div>
      </div>
    </div>

    <!-- MODAL: Stored As Bottom Sheet -->
    <div id="storedAsBottomSheet" class="hidden fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex flex-col justify-end" onclick="if(event.target===this)closeStoredAsBottomSheet()">
      <div id="storedAsSheetCard" class="w-full max-w-[440px] mx-auto bg-surface border-t border-bordercol rounded-t-xl p-4 space-y-3 max-h-[80vh] overflow-y-auto shadow-2xl transition-transform">
        <div class="w-10 h-1 bg-stone-300 rounded-full mx-auto -mt-1 mb-1"></div>
        <div class="flex items-center justify-between pb-2 border-b border-stone-200">
          <div>
            <h3 class="text-xs font-bold text-ink uppercase tracking-wider font-sans">Stored As</h3>
            <p class="text-[10.5px] font-sans text-subdued">Choose what container holds this object</p>
          </div>
          <button class="min-w-[40px] min-h-[40px] flex items-center justify-center rounded-lg hover:bg-stone-100 text-muted hover:text-ink font-mono text-sm tap-active" onclick="closeStoredAsBottomSheet()" type="button">✕</button>
        </div>
        <div class="space-y-1.5 font-mono text-xs" id="storedAsModalOptions">
          <!-- Populated dynamically -->
        </div>
      </div>
    </div>

    <!-- MODAL: My Current Shelf Bottom Sheet (Swipe-down to dismiss) -->
    <div id="stationSetupSheet" class="hidden fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex flex-col justify-end" onclick="if(event.target===this)closeStationSetupSheet()">
      <div id="stationSetupSheetCard" class="w-full max-w-[440px] mx-auto bg-surface border-t border-bordercol rounded-t-xl p-4 space-y-3.5 shadow-2xl" style="background:#ffffff;">
        <div class="w-10 h-1 bg-stone-300 rounded-full mx-auto -mt-1"></div>
        <div class="flex items-start justify-between gap-2 pb-2 border-b border-stone-200">
          <div>
            <h3 class="text-xs font-bold text-ink uppercase tracking-wider font-sans">📍 My Current Shelf</h3>
            <p class="text-[11px] font-sans text-subdued mt-0.5">Standing at a shelf? Set it once, then save it to each box in 1 tap.</p>
          </div>
          <button type="button" onclick="closeStationSetupSheet()" class="min-w-[40px] min-h-[40px] rounded-md text-muted hover:text-ink hover:bg-stone-100 flex items-center justify-center text-base font-bold tap-active" aria-label="Close">✕</button>
        </div>
        <div class="grid grid-cols-2 gap-2.5 text-xs font-mono">
          <div class="bg-stone-50 rounded border border-bordercol px-2.5 py-2">
            <span class="text-[9.5px] uppercase font-bold text-muted block mb-0.5">Building</span>
            <select id="launchBldgSelect" class="arbor-compact-select w-full min-h-[40px] bg-transparent border-0 p-0 font-bold text-ink outline-none focus:ring-0 text-xs">
              <option value="Lid's hus">Lid's hus</option>
              <option value="Økern">Økern</option>
            </select>
          </div>
          <div class="bg-stone-50 rounded border border-bordercol px-2.5 py-2">
            <span class="text-[9.5px] uppercase font-bold text-muted block mb-0.5">Floor</span>
            <select id="launchFloorSelect" class="arbor-compact-select w-full min-h-[40px] bg-transparent border-0 p-0 font-bold text-ink outline-none focus:ring-0 text-xs">
              <option value="1" selected>1</option>
              <option value="2">2</option>
              <option value="3">3</option>
              <option value="4">4</option>
              <option value="-1">-1</option>
              <option value="-2">-2</option>
            </select>
          </div>
          <div class="bg-stone-50 rounded border border-bordercol px-2.5 py-2">
            <span class="text-[9.5px] uppercase font-bold text-muted block mb-0.5">Cabinet</span>
            <input type="text" inputmode="numeric" id="launchCabInput" placeholder="21" class="w-full min-h-[40px] bg-transparent border-0 p-0 font-bold text-ink outline-none focus:ring-0 text-sm" />
          </div>
          <div class="bg-stone-50 rounded border-2 border-fern px-2.5 py-2">
            <span class="text-[9.5px] uppercase font-bold text-fern-dark block mb-0.5">Shelf</span>
            <input type="text" inputmode="numeric" id="launchShelfInput" placeholder="01" class="w-full min-h-[40px] bg-transparent border-0 p-0 font-bold text-fern-dark outline-none focus:ring-0 text-sm" />
          </div>
        </div>
        <div class="flex items-center gap-2 pt-1">
          <button type="button" onclick="clearStationSetup()" class="min-h-[44px] px-3.5 py-2 rounded border border-bordercol bg-stone-100 hover:bg-stone-200 text-ink-muted font-sans font-semibold text-xs tap-active">Clear</button>
          <button type="button" onclick="applyStationSetup()" class="flex-1 min-h-[44px] py-2.5 px-4 bg-fern hover:bg-fern-dark text-white rounded font-mono font-bold text-xs shadow-sm tap-active flex items-center justify-center gap-1.5" style="background:#2d5a3c;color:#ffffff;">
            <span>📍 Set Current Shelf</span>
          </button>
        </div>
      </div>
    </div>

    <!-- MODAL: Curatorial Advanced Filter -->
    <div id="filterModal" class="hidden fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4">
      <div class="bg-surface border border-bordercol rounded w-full max-w-md shadow-xl overflow-hidden flex flex-col max-h-[90vh]">
        <header class="p-3.5 bg-tonal1 border-b border-tonal2 flex items-center justify-between shrink-0">
          <h2 class="font-serif font-bold text-sm text-ink">Curatorial Advanced Filter</h2>
          <button type="button" onclick="closeFilterModal()" class="min-w-[40px] min-h-[40px] flex items-center justify-center rounded hover:bg-stone-200/70 text-ink-muted hover:text-ink font-bold text-sm tap-active">✕</button>
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
          <button type="button" onclick="clearAdvancedFilters()" class="min-h-[40px] px-4 py-2 border border-bordercol bg-white text-ink-muted hover:text-ink rounded text-xs font-semibold tap-active">Clear</button>
          <button type="button" onclick="applyAdvancedFilters()" class="min-h-[40px] px-5 py-2 bg-fern hover:bg-fern-dark text-white rounded text-xs font-bold tap-active">Apply</button>
        </footer>
      </div>
    </div>

    <!-- MODAL: ICEDIG Field Picker Bottom Sheet (Unified for Details & History tabs) -->
  <div id="icedigFieldSheet" class="hidden fixed inset-0 z-50 bg-black/50 backdrop-blur-xs flex items-end sm:items-center justify-center p-0 sm:p-4" onclick="if (event.target === this) closeFieldIcedigSheet()">
    <div class="w-full sm:max-w-md bg-surface rounded-t-xl sm:rounded-xl border border-bordercol shadow-xl p-4 space-y-3">
      <div class="flex items-center justify-between border-b border-stone-200 pb-2">
        <div>
          <h3 class="font-serif font-bold text-sm text-ink" id="icedigSheetTitle">ICEDIG Status</h3>
          <p class="text-[11px] font-sans text-muted mt-0.5">Only use <code class="font-mono">unknown:missing</code> if no historical ledger has a conflicting value.</p>
        </div>
        <button type="button" onclick="closeFieldIcedigSheet()" class="min-w-[40px] min-h-[40px] flex items-center justify-center rounded hover:bg-stone-100 text-ink-muted font-bold text-sm tap-active">✕</button>
      </div>
      <div id="icedigSheetConflictWarn" class="hidden p-2.5 rounded bg-amber-50 border border-amber-300 text-[11px] font-sans text-amber-900">
        <strong>Heads up:</strong> Older catalog books have a value for this field — swipe to <strong>History</strong> to compare before setting <code class="font-mono">unknown:missing</code>.
      </div>
      <div id="icedigSheetOptions" class="grid grid-cols-1 gap-1.5"></div>
      <div class="flex justify-end pt-1">
        <button type="button" onclick="closeFieldIcedigSheet()" class="min-h-[40px] px-3.5 py-1.5 border border-bordercol text-ink-muted rounded text-xs font-mono tap-active">Cancel</button>
      </div>
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
          <button type="button" onclick="closeCommentEditor()" class="min-w-[40px] min-h-[40px] flex items-center justify-center rounded hover:bg-stone-200/70 text-ink-muted hover:text-ink font-bold text-sm tap-active">✕</button>
        </header>
        <div class="p-4 space-y-3">
          <div>
            <label class="block font-sans text-xs font-medium text-ink mb-1">Comment / Curatorial Notes</label>
            <textarea id="commentEditTextarea" rows="6" placeholder="Enter comments or curatorial notes..." class="w-full bg-surface border border-bordercol rounded p-2.5 text-xs font-mono text-ink outline-none focus:border-fern focus:ring-1 focus:ring-fern resize-none leading-relaxed"></textarea>
          </div>
          <div class="flex justify-end gap-2 pt-2 border-t border-tonal2">
            <button type="button" onclick="closeCommentEditor()" class="min-h-[38px] px-3 py-1.5 border border-bordercol text-ink-muted rounded text-xs font-mono tap-active">Cancel</button>
            <button type="button" onclick="saveCommentFromEditor()" class="min-h-[38px] px-4 py-1.5 bg-fern hover:bg-fern-dark text-white rounded text-xs font-bold font-mono tap-active">Save Comment</button>
          </div>
        </div>
      </div>
    </div>

    <!-- MODAL: Photo Fullscreen Viewer -->
    <div id="photoViewerModal" class="hidden fixed inset-0 z-50 bg-black/90 backdrop-blur-md flex flex-col justify-between p-4">
      <div class="flex items-center justify-between text-white gap-2">
        <span class="font-mono text-xs truncate" id="photoViewerTitle">Specimen Photo</span>
        <div class="flex items-center gap-2 shrink-0">
          <button type="button" onclick="rotatePhoto()" class="min-h-[40px] px-3 py-2 bg-white/20 hover:bg-white/30 rounded text-xs font-mono tap-active">↻ Rotate</button>
          <button type="button" onclick="closePhotoViewerModal()" class="min-w-[40px] min-h-[40px] flex items-center justify-center bg-white/20 hover:bg-white/30 rounded text-sm font-bold tap-active">✕</button>
        </div>
      </div>
      <div id="photoViewerViewport" class="relative flex-1 flex items-center justify-center overflow-hidden my-2" style="touch-action: none;">
        <button id="btnPhotoPrev" type="button" onclick="stepViewerPhoto(-1)" class="hidden absolute left-1 z-10 min-w-[40px] min-h-[40px] rounded-full bg-black/60 hover:bg-black/80 text-white text-lg font-bold flex items-center justify-center tap-active" title="Previous Photo">‹</button>
        <img id="photoViewerImg" src="" alt="Specimen Inspection" class="max-w-full max-h-full object-contain select-none" draggable="false">
        <button id="btnPhotoNext" type="button" onclick="stepViewerPhoto(1)" class="hidden absolute right-1 z-10 min-w-[40px] min-h-[40px] rounded-full bg-black/60 hover:bg-black/80 text-white text-lg font-bold flex items-center justify-center tap-active" title="Next Photo">›</button>
      </div>
      <div class="flex items-center justify-center gap-2.5 text-white text-xs font-mono">
        <button type="button" onclick="zoomPhoto(-0.3)" class="min-h-[40px] px-3.5 py-2 bg-white/20 hover:bg-white/30 rounded font-bold tap-active">− Zoom</button>
        <span id="zoomLevelDisplay" class="min-w-[42px] text-center">1.0x</span>
        <button type="button" onclick="zoomPhoto(0.3)" class="min-h-[40px] px-3.5 py-2 bg-white/20 hover:bg-white/30 rounded font-bold tap-active">+ Zoom</button>
        <button type="button" onclick="resetPhotoTransform()" class="min-h-[40px] px-3.5 py-2 bg-white/20 hover:bg-white/30 rounded tap-active">Reset</button>
      </div>
    </div>

    <!-- MODAL: Connection Telemetry Status -->
    <div id="connectionModal" class="hidden fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4">
      <div class="bg-surface border border-bordercol rounded w-full max-w-sm p-4 shadow-xl space-y-3">
        <div class="flex items-center justify-between border-b border-tonal2 pb-2">
          <h3 class="font-serif font-bold text-sm text-ink">⚡ Desktop Host Link</h3>
          <button type="button" onclick="closeModal('connectionModal')" class="min-w-[40px] min-h-[40px] flex items-center justify-center rounded hover:bg-stone-200/70 text-ink-muted font-bold text-sm tap-active">✕</button>
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
    <div id="toast" class="hidden fixed bottom-24 left-4 right-4 max-w-sm mx-auto bg-stone-900/95 text-white text-xs py-2.5 px-4 rounded-lg shadow-xl flex items-center justify-between gap-2 z-50 transition-opacity">
      <span id="toastMsg" class="font-medium truncate">Edits saved & synchronized</span>
      <button id="toastActionBtn" class="hidden shrink-0 min-h-[40px] px-3 py-1.5 rounded bg-fern hover:bg-fern-dark text-white font-mono text-[11px] font-bold uppercase tracking-wider tap-active transition-colors">Undo</button>
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
      armedLocation: null,
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

    let _toastHasActiveAction = false;

    function showToast(msg, options = null) {
      const toast = document.getElementById('toast');
      const msgEl = document.getElementById('toastMsg') || toast;
      const actionBtn = document.getElementById('toastActionBtn');
      if (!toast) return;

      // Never let a passive background auto-save toast clobber an active Undo action toast
      if (options && options.passive && _toastHasActiveAction) {
        return;
      }

      if (toastTimer) clearTimeout(toastTimer);
      if (toastHideTimer) clearTimeout(toastHideTimer);

      msgEl.textContent = msg;

      if (actionBtn) {
        const actLabel = options && (options.actionText || options.actionLabel);
        const actFn = options && (typeof options.onAction === 'function' ? options.onAction : (typeof options.action === 'function' ? options.action : null));
        if (actLabel && actFn) {
          _toastHasActiveAction = true;
          actionBtn.textContent = actLabel;
          actionBtn.onclick = (e) => {
            e.stopPropagation();
            _toastHasActiveAction = false;
            hideToast();
            actFn();
          };
          actionBtn.classList.remove('hidden');
        } else {
          _toastHasActiveAction = false;
          actionBtn.classList.add('hidden');
          actionBtn.onclick = null;
        }
      }

      toast.classList.remove('hidden');
      toast.style.opacity = '1';

      const hasAction = Boolean(options && (typeof options.onAction === 'function' || typeof options.action === 'function'));
      const duration = (options && options.duration) ? options.duration : (hasAction ? 5000 : 2200);
      toastTimer = setTimeout(hideToast, duration);
    }

    function hideToast() {
      const toast = document.getElementById('toast');
      if (!toast) return;
      if (toastTimer) clearTimeout(toastTimer);
      _toastHasActiveAction = false;
      toast.style.opacity = '0';
      toastHideTimer = setTimeout(() => {
        toast.classList.add('hidden');
        const actionBtn = document.getElementById('toastActionBtn');
        if (actionBtn) actionBtn.classList.add('hidden');
        if (typeof _flushPendingCoachTip === 'function') _flushPendingCoachTip();
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

      const pillText = document.getElementById('activeStationPillText');
      const triggerBtn = document.getElementById('btnStationSheetTrigger');
      const bldgSelect = document.getElementById('launchBldgSelect');
      const floorSelect = document.getElementById('launchFloorSelect');
      const cabInput = document.getElementById('launchCabInput');
      const shelfInput = document.getElementById('launchShelfInput');

      populateLaunchBuildingOptions(armed ? armed.building : null);
      if (floorSelect && armed && armed.floor !== undefined && armed.floor !== null && String(armed.floor).trim() !== '') {
        floorSelect.value = String(armed.floor).trim();
      }

      const hasArmed = Boolean(armed && (armed.cabinet || armed.shelf));
      const copyPrevCard = document.getElementById('copyPrevSpecimenCard');
      if (copyPrevCard) copyPrevCard.classList.toggle('hidden', hasArmed);

      if (hasArmed) {
        const bldgRaw = String(armed.building || '').trim();
        const bldgShort = bldgRaw ? (bldgRaw.length > 6 ? bldgRaw.split(' ')[0] : bldgRaw) + ' · ' : '';
        const fl = (armed.floor !== undefined && armed.floor !== null && String(armed.floor).trim() !== '') ? `Fl ${armed.floor} · ` : '';
        const cab = armed.cabinet ? String(armed.cabinet).padStart(2, '0') : '—';
        const shelf = armed.shelf ? String(armed.shelf).padStart(2, '0') : '—';
        if (pillText) pillText.textContent = `${bldgShort}${fl}Cab ${cab} · Sh ${shelf}`;
        if (triggerBtn) triggerBtn.textContent = 'Change';
        if (bldgSelect && armed.building) bldgSelect.value = armed.building;
        if (cabInput && armed.cabinet) cabInput.value = armed.cabinet;
        if (shelfInput && armed.shelf) shelfInput.value = armed.shelf;
      } else {
        if (pillText) pillText.textContent = 'Not set';
        if (triggerBtn) triggerBtn.textContent = 'Set Shelf';
      }

      // Show the 1-line "Set Shelf" coach nudge only while unset & walkthrough enabled
      const coachNudge = document.getElementById('listCoachNudge');
      if (coachNudge) {
        let dismissed = false;
        try { dismissed = sessionStorage.getItem('arbor_v2_coach_nudge_dismissed') === 'true'; } catch(e) {}
        const showNudge = !hasArmed && !dismissed && (typeof ARBOR_SHOW_WALKTHROUGH === 'undefined' || ARBOR_SHOW_WALKTHROUGH);
        coachNudge.classList.toggle('hidden', !showNudge);
      }
    }

    function dismissListCoachNudge() {
      const el = document.getElementById('listCoachNudge');
      if (el) el.classList.add('hidden');
      try { sessionStorage.setItem('arbor_v2_coach_nudge_dismissed', 'true'); } catch(e) {}
    }

    function openStationSetup() {
      const sheet = document.getElementById('stationSetupSheet');
      const cabInput = document.getElementById('launchCabInput');
      if (sheet) sheet.classList.remove('hidden');
      if (cabInput) {
        setTimeout(() => {
          cabInput.focus();
          cabInput.select();
        }, 60);
      }
    }

    function closeStationSetupSheet() {
      const sheet = document.getElementById('stationSetupSheet');
      if (sheet) sheet.classList.add('hidden');
    }

    function dismissStationSetup() {
      closeStationSetupSheet();
    }

    function clearStationSetup() {
      state.armedLocation = null;
      try { localStorage.removeItem('arbor_armed_location'); } catch (e) {}
      const cabInput = document.getElementById('launchCabInput');
      const shelfInput = document.getElementById('launchShelfInput');
      if (cabInput) cabInput.value = '';
      if (shelfInput) shelfInput.value = '';
      initStationLaunchpad();
      if (state.currentRecord) updateArmedShelfBannerUI(state.currentRecord.observation || {});
      closeStationSetupSheet();
      showToast('Current Shelf cleared');
    }

    function applyStationSetup() {
      const bldgSelect = document.getElementById('launchBldgSelect');
      const floorSelect = document.getElementById('launchFloorSelect');
      const cabInput = document.getElementById('launchCabInput');
      const shelfInput = document.getElementById('launchShelfInput');

      const bldg = bldgSelect ? bldgSelect.value : "Lid's hus";
      const floor = floorSelect ? floorSelect.value : '1';
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
        floor: floor,
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
      if (state.currentRecord) updateArmedShelfBannerUI(state.currentRecord.observation || {});
      closeStationSetupSheet();
      initTouchGestures();
      initPhotoViewerTouchGestures();
      triggerHaptic('stepper');
      showToast(`📍 Current Shelf set: Cab ${cab || '—'} · Sh ${shelf || '—'}`);
      if (typeof coachTick === 'function') coachTick();
    }

    // -------------------------------------------------------------
    // INITIALIZATION & SSE CONNECTION
    // -------------------------------------------------------------
    async function init() {
      await initIndexedDB();
      applyFilterPillVisibility();
      initStationLaunchpad();
      initTouchGestures();
      initPhotoViewerTouchGestures();
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
              invalidatePrefetchCache(updatedId || null);
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
          state.icedigCodeList = Array.isArray(data.icedig_codes) ? data.icedig_codes : [];
          state.specialistQuickTags = Array.isArray(data.specialist_quick_tags) ? data.specialist_quick_tags : [];
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
    function renderListSkeleton(count = 6) {
      let html = '<div class="divide-y divide-stone-200 bg-white" aria-busy="true" aria-label="Loading specimens">';
      for (let i = 0; i < count; i++) {
        html += `
          <div class="px-4 py-3 flex items-center justify-between gap-3">
            <div class="flex-1 min-w-0 space-y-2">
              <div class="flex items-center gap-2">
                <div class="arbor-skeleton h-3.5 w-16"></div>
                <div class="arbor-skeleton h-3.5 w-20"></div>
              </div>
              <div class="arbor-skeleton h-4 w-3/4"></div>
              <div class="arbor-skeleton h-3 w-1/2"></div>
            </div>
            <div class="arbor-skeleton h-6 w-14 shrink-0"></div>
          </div>`;
      }
      html += '</div>';
      return html;
    }

    async function fetchObjects(showLoading = true) {
      const container = document.getElementById('specimenListContainer');
      if (showLoading && container) {
        container.innerHTML = renderListSkeleton(6);
      }

      const params = new URLSearchParams();
      if (state.searchQuery) params.set('q', state.searchQuery);
      if (state.activeStatusFilter) params.set('status', state.activeStatusFilter);
      if (state.selectedCabinet) params.set('cabinet', state.selectedCabinet);
      if (state.selectedShelf) params.set('shelf', state.selectedShelf);
      if (state.activeAdvancedFilters && state.activeAdvancedFilters.locations) {
        Object.entries(state.activeAdvancedFilters.locations).forEach(([k, v]) => {
          const val = String(v || '').trim();
          if (val && k.toLowerCase() !== 'cabinet' && k.toLowerCase() !== 'shelf') {
            params.set(`loc_${k}`, val);
          }
        });
      }
      if (state.activeAdvancedFilters && state.activeAdvancedFilters.problems) {
        const activeProbs = Object.entries(state.activeAdvancedFilters.problems)
          .filter(([, checked]) => Boolean(checked))
          .map(([name]) => name);
        if (activeProbs.length > 0) {
          params.set('specific_problems', activeProbs.join(','));
        }
      }
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
        const isLoaned = Boolean(
          obj.loaned_out === true ||
          String(loc.loaned_out || '').trim().toLowerCase() === 'true' ||
          String(loc.loaned_out || '').trim() === '1'
        );
        
        let locBreadcrumb = [];
        if (loc.building) {
          const bRaw = String(loc.building).trim();
          const bShort = bRaw.length > 6 ? bRaw.split(' ')[0] : bRaw;
          locBreadcrumb.push(bShort);
        }
        if (loc.floor !== undefined && loc.floor !== null && String(loc.floor).trim() !== '') locBreadcrumb.push(`Fl ${loc.floor}`);
        if (loc.cabinet) locBreadcrumb.push(`Cab ${loc.cabinet}`);
        if (loc.shelf) locBreadcrumb.push(`Sh ${loc.shelf}`);
        const locStr = locBreadcrumb.length > 0 ? locBreadcrumb.join(' › ') : 'Unrecorded location';

        const hasActionable = (obj.has_actionable_problems !== undefined) ? Boolean(obj.has_actionable_problems) : hasFlags;
        const isSpecNote = Boolean(obj.is_specialist_note);

        return `
          <article onclick="openDetailView('${obj.id}')" class="bg-surface border border-bordercol rounded p-3 shadow-2xs hover:border-fern/50 active:bg-stone-50 transition-all cursor-pointer flex flex-col gap-1.5 relative tap-active">
            <div class="flex items-start justify-between gap-2">
              <div class="flex items-center gap-2 min-w-0">
                <span class="font-mono text-[11px] font-bold text-ink px-1.5 py-0.5 bg-stone-100 border border-bordercol/80 rounded shrink-0">
                  #${obj.accession_number || obj.id}
                </span>
                <span class="text-[10px] font-mono text-muted uppercase truncate">${obj.family || 'Taxon'}</span>
              </div>
              
              <div class="flex items-center gap-1 shrink-0">
                ${isLoaned ? '<span onclick="event.stopPropagation(); showBadgeTooltip(this, \\'LOAN\\')" role="button" class="px-1.5 py-0.5 rounded font-mono text-[10px] font-bold bg-amber-100 text-amber-900 border border-amber-300 cursor-help">↗ Loaned</span>' : ''}
                ${isRev && hasActionable
                  ? '<span onclick="event.stopPropagation(); showBadgeTooltip(this, \\'REV+ERR\\')" role="button" class="px-1.5 py-0.5 rounded font-mono text-[10px] font-bold bg-amber-50 text-amber-900 border border-amber-300 cursor-help">[REV+ERR]</span>'
                  : (isRev && isSpecNote
                    ? '<span onclick="event.stopPropagation(); showBadgeTooltip(this, \\'REV+NOTE\\')" role="button" class="px-1.5 py-0.5 rounded font-mono text-[10px] font-bold bg-teal-50 text-teal-800 border border-teal-300 cursor-help">[REV+NOTE]</span>'
                    : (isRev
                      ? '<span onclick="event.stopPropagation(); showBadgeTooltip(this, \\'REV\\')" role="button" class="px-1.5 py-0.5 rounded font-mono text-[10px] font-bold bg-emerald-50 text-fern-dark border border-fern/30 cursor-help">[REV]</span>'
                      : (hasActionable
                        ? '<span onclick="event.stopPropagation(); showBadgeTooltip(this, \\'FLAGGED\\')" role="button" class="px-1.5 py-0.5 rounded font-mono text-[10px] font-bold bg-amber-50 text-amber-800 border border-amber-300 cursor-help">Flagged ⚠</span>'
                        : (isSpecNote
                          ? '<span onclick="event.stopPropagation(); showBadgeTooltip(this, \\'NOTE\\')" role="button" class="px-1.5 py-0.5 rounded font-mono text-[10px] font-bold bg-indigo-50 text-indigo-800 border border-indigo-300 cursor-help">[NOTE]</span>'
                          : '<span onclick="event.stopPropagation(); showBadgeTooltip(this, \\'UNREV\\')" role="button" class="px-1.5 py-0.5 rounded font-mono text-[10px] font-bold bg-stone-100 text-stone-600 border border-stone-300 cursor-help">[UNREV]</span>'
                        )
                      )
                    )
                  )
                }
              </div>
            </div>

            <div class="font-serif font-semibold italic text-[15px] text-ink leading-tight truncate">
              ${obj.scientific_name || 'Unidentified Specimen'}
            </div>

            <div class="flex items-center justify-between gap-2 text-[11px] font-mono pt-1 border-t border-stone-100 text-muted">
              <span class="truncate text-ink-muted">${locStr}</span>
              ${loc.stored_as ? `<span class="text-[10px] px-1.5 py-0.5 bg-stone-100 rounded border border-bordercol/60 shrink-0 max-w-[46%] truncate">${loc.stored_as}</span>` : ''}
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
    function setDetailLoadingState(mode, errMsg) {
      const overlay = document.getElementById('detailLoadingOverlay');
      const spinner = document.getElementById('detailLoadingSpinner');
      const errBox = document.getElementById('detailLoadingError');
      const errText = document.getElementById('detailLoadingErrorMsg');
      if (!overlay) return;
      if (mode === 'loading') {
        overlay.classList.remove('hidden');
        if (spinner) spinner.classList.remove('hidden');
        if (errBox) errBox.classList.add('hidden');
      } else if (mode === 'error') {
        overlay.classList.remove('hidden');
        if (spinner) spinner.classList.add('hidden');
        if (errBox) errBox.classList.remove('hidden');
        if (errText) errText.textContent = errMsg || 'Could not load specimen. Check connection and retry.';
      } else {
        overlay.classList.add('hidden');
      }
    }

    function retryCurrentSpecimen() {
      if (state.currentOid) {
        setDetailLoadingState('loading');
        fetchObjectDetail(state.currentOid);
      }
    }

    async function openDetailView(oid) {
      forceSaveImmediate();
      state.currentOid = String(oid);
      state.currentRecord = null;
      const listMatch = Array.isArray(state.objectList)
        ? state.objectList.find(o => String(o.id) === String(oid))
        : null;
      const displayAcc = (listMatch && listMatch.accession_number) ? listMatch.accession_number : oid;
      const accEl = document.getElementById('detailAccession');
      const nameEl = document.getElementById('detailScientificName');
      const famEl = document.getElementById('detailFamily');
      if (accEl) accEl.textContent = '#' + String(displayAcc);
      if (nameEl) nameEl.textContent = 'Loading specimen…';
      if (famEl) famEl.textContent = '…';
      setDetailLoadingState('loading');
      // Always reset synchronously to Details tab so History/Location never flash on specimen switch
      if (typeof switchTab === 'function') switchTab(0);
      showDetailView();
      window.scrollTo(0, 0);
      document.documentElement.scrollTop = 0;
      document.body.scrollTop = 0;
      document.querySelectorAll('#tabTrack > div').forEach(pane => { pane.scrollTop = 0; });
      await fetchObjectDetail(oid);
      requestAnimationFrame(() => {
        window.scrollTo(0, 0);
        document.documentElement.scrollTop = 0;
        document.querySelectorAll('#tabTrack > div').forEach(pane => { pane.scrollTop = 0; });
      });
    }

    // Predictive Back (History API) state
    let _historyDepth = 0;

    function showListView(opts = {}) {
      forceSaveImmediate();
      if (typeof dismissCoachTip === 'function') dismissCoachTip();
      if (typeof coachState !== 'undefined') coachState.pendingTip = null;
      const listEl = document.getElementById('listView');
      const detailEl = document.getElementById('detailView');
      const batchEl = document.getElementById('batchLocationView');
      if (detailEl) {
        detailEl.style.transition = '';
        detailEl.style.transform = '';
        detailEl.style.boxShadow = '';
        detailEl.classList.add('hidden');
      }
      if (listEl) {
        listEl.style.transition = '';
        listEl.style.transform = '';
        listEl.style.opacity = '';
        listEl.style.pointerEvents = '';
        listEl.classList.remove('hidden');
      }
      if (batchEl) batchEl.classList.add('hidden');
      if (!opts.fromPopState && _historyDepth > 0) {
        _historyDepth = 0;
        try { history.replaceState({ view: 'list' }, ''); } catch (e) {}
      }
      initStationLaunchpad();
      initTouchGestures();
      initPhotoViewerTouchGestures();
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
      const detailEl = document.getElementById('detailView');
      detailEl.style.transition = '';
      detailEl.style.transform = '';
      detailEl.style.boxShadow = '';
      detailEl.classList.remove('hidden');
      document.getElementById('batchLocationView').classList.add('hidden');
      try {
        if (_historyDepth === 0) {
          history.pushState({ view: 'detail', oid: state.currentOid }, '');
          _historyDepth = 1;
        } else {
          history.replaceState({ view: 'detail', oid: state.currentOid }, '');
        }
      } catch (e) {}
    }

    function showBatchLocationView() {
      document.getElementById('listView').classList.add('hidden');
      document.getElementById('detailView').classList.add('hidden');
      document.getElementById('batchLocationView').classList.remove('hidden');
      try {
        if (_historyDepth === 0) {
          history.pushState({ view: 'batch' }, '');
          _historyDepth = 1;
        }
      } catch (e) {}
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
      const armed = state.armedLocation;
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
      const armed = state.armedLocation;
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

    // ── 1-Tap Old Names & Synonyms Sheet (Read-Only) ───────────────────────
    let _oldNamesData = null;
    let _oldNamesShowMore = false;

    function closeOldNamesSheet() {
      const el = document.getElementById('oldNamesSheet');
      if (el) el.classList.add('hidden');
    }

    async function openOldNamesSheet() {
      if (!state.currentOid) return;
      const sheet = document.getElementById('oldNamesSheet');
      const body = document.getElementById('oldNamesBody');
      const regLbl = document.getElementById('oldNamesRegisteredLbl');
      const filterEl = document.getElementById('oldNamesFilterInput');
      const fbEl = document.getElementById('oldNamesGbifFallback');
      const vEl = document.getElementById('oldNamesVerdictBox');
      if (!sheet || !body) return;

      _oldNamesData = null;
      _oldNamesShowMore = false;
      if (filterEl) filterEl.value = '';
      if (fbEl) fbEl.classList.add('hidden');
      if (vEl) { vEl.classList.add('hidden'); vEl.innerHTML = ''; }

      const rec = state.currentRecord || {};
      const reg = rec.registration || {};
      const curName = rec.scientific_name || [reg.Genus, reg.Species].filter(Boolean).join(' ') || 'Current Specimen';
      if (regLbl) regLbl.textContent = curName + (reg.Family ? ' (' + reg.Family + ')' : '');

      body.innerHTML = '<div class="py-6 flex flex-col items-center justify-center gap-2 text-muted text-xs"><div class="w-6 h-6 border-2 border-stone-300 border-t-emerald-700 rounded-full animate-spin"></div><span>Loading known old names…</span></div>';
      sheet.classList.remove('hidden');

      const oid = state.currentOid;
      try {
        const data = await apiFetch('/api/object/' + encodeURIComponent(oid) + '/synonyms');
        if (state.currentOid !== String(oid)) return;
        _oldNamesData = data;
        renderOldNamesSheet();
      } catch (err) {
        if (state.currentOid !== String(oid)) return;
        body.innerHTML = '<div class="p-3 rounded-md bg-amber-50 border border-amber-200 text-amber-900 text-xs">Offline or server unreachable — could not load old names right now.</div>';
      }
    }

    function _escHtmlOldNames(s) {
      return String(s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }

    function renderOldNamesSheet() {
      const body = document.getElementById('oldNamesBody');
      const filterEl = document.getElementById('oldNamesFilterInput');
      const fbEl = document.getElementById('oldNamesGbifFallback');
      if (!body || !_oldNamesData) return;

      const q = (filterEl ? filterEl.value : '').trim().toLowerCase();
      const matchQ = (txt) => !q || String(txt || '').toLowerCase().includes(q);

      const localHist = (_oldNamesData.local_history || []).filter(x => matchQ(x.name + ' ' + (x.source || '')));
      const oldFams = (_oldNamesData.old_families || []).filter(x => matchQ(x.name + ' ' + (x.note || '')));
      const primary = (_oldNamesData.primary_synonyms || []).filter(x => matchQ(x.name + ' ' + (x.author || '')));
      const others = (_oldNamesData.other_synonyms || []).filter(x => matchQ(x.name + ' ' + (x.author || '')));

      const totalVisible = localHist.length + oldFams.length + primary.length + others.length;
      let html = '';

      if (localHist.length) {
        html += '<div><div class="text-[10px] font-bold uppercase tracking-wider text-muted mb-1">Past Names in This Museum</div><div class="space-y-1">';
        localHist.forEach(item => {
          html += '<div class="px-2.5 py-1.5 rounded bg-tonal border border-bordercol flex items-center justify-between gap-2"><span class="font-serif italic text-xs text-ink">' + _escHtmlOldNames(item.name) + '</span><span class="text-[10px] text-muted shrink-0">' + _escHtmlOldNames(item.source) + '</span></div>';
        });
        html += '</div></div>';
      }

      if (oldFams.length) {
        html += '<div><div class="text-[10px] font-bold uppercase tracking-wider text-muted mb-1">Old Family Names</div><div class="space-y-1">';
        oldFams.forEach(item => {
          html += '<div class="px-2.5 py-1.5 rounded bg-emerald-50/70 border border-emerald-200/80 flex items-center justify-between gap-2"><span class="font-semibold text-xs text-ink">' + _escHtmlOldNames(item.name) + '</span><span class="text-[10px] text-muted text-right">' + _escHtmlOldNames(item.note) + '</span></div>';
        });
        html += '</div></div>';
      }

      const _plainSynonymKind = (k) => {
        const s = String(k || '').trim().toLowerCase();
        if (s.includes('basionym')) return 'Original name';
        if (s.includes('homotypic')) return 'Direct rename';
        if (s.includes('heterotypic')) return 'Older synonym';
        return k || 'Old name';
      };

      if (primary.length) {
        html += '<div><div class="text-[10px] font-bold uppercase tracking-wider text-muted mb-1">Most Likely Old Names (Direct Renames)</div><div class="space-y-1">';
        primary.forEach(item => {
          html += '<div class="px-2.5 py-1.5 rounded bg-surface border border-bordercol flex items-baseline justify-between gap-2"><div class="min-w-0"><span class="font-serif italic text-xs font-semibold text-ink">' + _escHtmlOldNames(item.name) + '</span>' + (item.author ? ' <span class="text-[11px] text-muted">' + _escHtmlOldNames(item.author) + '</span>' : '') + '</div><span class="text-[10px] font-mono text-muted shrink-0">' + _escHtmlOldNames(_plainSynonymKind(item.kind)) + '</span></div>';
        });
        html += '</div></div>';
      }

      if (others.length) {
        if (q || _oldNamesShowMore || primary.length === 0) {
          html += '<div><div class="text-[10px] font-bold uppercase tracking-wider text-muted mb-1">Other Known Old Names (' + others.length + ')</div><div class="space-y-1">';
          others.forEach(item => {
            html += '<div class="px-2.5 py-1.5 rounded bg-surface border border-stone-200 flex items-baseline justify-between gap-2"><div class="min-w-0"><span class="font-serif italic text-xs text-ink">' + _escHtmlOldNames(item.name) + '</span>' + (item.author ? ' <span class="text-[11px] text-muted">' + _escHtmlOldNames(item.author) + '</span>' : '') + '</div><span class="text-[10px] font-mono text-subdued shrink-0">' + _escHtmlOldNames(item.kind ? _plainSynonymKind(item.kind) : '') + '</span></div>';
          });
          html += '</div></div>';
        } else {
          html += '<button type="button" onclick="toggleMoreOldNames()" class="w-full py-2 min-h-[40px] rounded-md border border-bordercol bg-tonal text-xs font-semibold text-ink-muted">Show ' + others.length + ' more old names ▾</button>';
        }
      }

      if (_oldNamesData.offline) {
        html += '<div class="p-2.5 rounded-md bg-amber-50 border border-amber-200 text-amber-900 text-[11px]">Offline — showing local history &amp; old family names only. Connect to internet for full GBIF synonyms.</div>';
      } else if (totalVisible === 0) {
        html += '<div class="py-3 text-center text-xs text-muted">' + (q ? 'No loaded old names match "' + _escHtmlOldNames(q) + '".' : 'No older synonyms recorded for this name.') + '</div>';
      }

      html += '<p class="text-[11px] text-subdued pt-1">Read-only reference: if the physical label matches an old name above, keep the modern registered name.</p>';
      body.innerHTML = html;

      if (fbEl) {
        if (q.length >= 3 && totalVisible === 0) fbEl.classList.remove('hidden');
        else fbEl.classList.add('hidden');
      }
    }

    function filterOldNamesList() {
      const vEl = document.getElementById('oldNamesVerdictBox');
      if (vEl) { vEl.classList.add('hidden'); vEl.innerHTML = ''; }
      renderOldNamesSheet();
    }

    function toggleMoreOldNames() {
      _oldNamesShowMore = true;
      renderOldNamesSheet();
    }

    async function checkLabelAgainstGbif() {
      if (!state.currentOid) return;
      const filterEl = document.getElementById('oldNamesFilterInput');
      const vEl = document.getElementById('oldNamesVerdictBox');
      const btn = document.getElementById('btnCheckLabelGbif');
      const label = (filterEl ? filterEl.value : '').trim();
      if (!label || !vEl) return;

      if (btn) { btn.disabled = true; btn.textContent = 'Checking…'; }
      try {
        const res = await apiFetch('/api/object/' + encodeURIComponent(state.currentOid) + '/check-label', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ label_name: label })
        });
        vEl.classList.remove('hidden');
        if (res.verdict === 'synonym_match') {
          vEl.className = 'rounded-md p-2.5 text-xs bg-emerald-50 border border-emerald-200 text-emerald-900 space-y-1';
          vEl.innerHTML = '<div class="font-bold">✓ Known Old Name Match</div><div>' + _escHtmlOldNames(res.message) + '</div>';
        } else if (res.verdict === 'different_species') {
          vEl.className = 'rounded-md p-2.5 text-xs bg-amber-50 border border-amber-300 text-amber-950 space-y-2';
          vEl.innerHTML = '<div class="font-bold">⚠ Different Species</div><div>' + _escHtmlOldNames(res.message) + '</div><button type="button" onclick="flagOldNamesMismatch()" class="px-3 py-1.5 min-h-[36px] rounded bg-amber-700 text-white text-xs font-semibold" style="background:#b45309;color:#ffffff;">Flag Taxon Mismatch &amp; Add Note</button>';
        } else {
          vEl.className = 'rounded-md p-2.5 text-xs bg-tonal border border-bordercol text-ink-muted space-y-1';
          vEl.innerHTML = '<div class="font-bold">? Not Confirmed</div><div>' + _escHtmlOldNames(res.message) + '</div>';
        }
      } catch (err) {
        vEl.classList.remove('hidden');
        vEl.className = 'rounded-md p-2.5 text-xs bg-amber-50 border border-amber-200 text-amber-900';
        vEl.textContent = 'Offline or unreachable — leave a note in Comment if unsure.';
      } finally {
        if (btn) { btn.disabled = false; btn.textContent = 'Check in GBIF'; }
      }
    }

    function flagOldNamesMismatch() {
      const filterEl = document.getElementById('oldNamesFilterInput');
      const label = (filterEl ? filterEl.value : '').trim();
      closeOldNamesSheet();
      if (typeof switchDetailTab === 'function') switchDetailTab(2);
      const commentEl = document.getElementById('commentEditTextarea') || document.querySelector('[data-field="Comment"]');
      if (commentEl && label) {
        const prefix = commentEl.value.trim() ? commentEl.value.trim() + ' | ' : '';
        commentEl.value = prefix + 'Label reads: ' + label;
        commentEl.dispatchEvent(new Event('input', { bubbles: true }));
      }
      if (typeof showToast === 'function') showToast('Added label note — toggle the problem flag if needed.');
    }

    // Adjacent-record prefetch cache (LRU, max 10 entries, 60s TTL)
    const detailPrefetchCache = new Map();
    const DETAIL_PREFETCH_MAX = 10;
    const DETAIL_PREFETCH_TTL_MS = 60000;

    function invalidatePrefetchCache(oid = null) {
      if (oid === null || oid === undefined) {
        detailPrefetchCache.clear();
      } else {
        detailPrefetchCache.delete(String(oid));
      }
    }

    function _putPrefetchCache(oid, data, hist) {
      const key = String(oid);
      if (detailPrefetchCache.has(key)) detailPrefetchCache.delete(key);
      detailPrefetchCache.set(key, { data, hist, fetchedAt: Date.now() });
      while (detailPrefetchCache.size > DETAIL_PREFETCH_MAX) {
        const oldestKey = detailPrefetchCache.keys().next().value;
        detailPrefetchCache.delete(oldestKey);
      }
    }

    function prefetchAdjacentSpecimens(currentOid) {
      if (!navigator.onLine || !Array.isArray(state.objectList) || state.objectList.length < 2) return;
      const idx = state.objectList.findIndex(o => String(o.id) === String(currentOid));
      if (idx === -1) return;
      const neighbors = [];
      if (idx + 1 < state.objectList.length) neighbors.push(String(state.objectList[idx + 1].id));
      if (idx - 1 >= 0) neighbors.push(String(state.objectList[idx - 1].id));

      neighbors.forEach((nOid) => {
        const existing = detailPrefetchCache.get(nOid);
        if (existing && (Date.now() - existing.fetchedAt) < DETAIL_PREFETCH_TTL_MS) return;
        Promise.all([
          apiFetch('/api/object/' + encodeURIComponent(nOid)),
          apiFetch('/api/object/' + encodeURIComponent(nOid) + '/history').catch(() => null)
        ]).then(([data, hist]) => {
          if (!data) return;
          _putPrefetchCache(nOid, data, hist);
          const imgs = data.images && Array.isArray(data.images.urls) ? data.images.urls : [];
          if (imgs.length > 0 && imgs[0]) {
            const preImg = new Image();
            preImg.src = imgs[0];
          }
        }).catch(() => {});
      });
    }

    async function fetchObjectDetail(oid, renderFull = true) {
      const key = String(oid);
      const cached = detailPrefetchCache.get(key);
      if (cached && (Date.now() - cached.fetchedAt) < DETAIL_PREFETCH_TTL_MS) {
        if (state.currentOid !== key) return;
        state.currentRecord = cached.data;
        state.isReviewed = cached.data.review_status === 'reviewed';
        state.currentHistoricalData = (cached.hist && cached.hist.historical_data) ? cached.hist.historical_data : null;
        renderDetailView(renderFull);
        setDetailLoadingState('ready');
        prefetchAdjacentSpecimens(key);
        return;
      }

      try {
        const [data, hist] = await Promise.all([
          apiFetch('/api/object/' + encodeURIComponent(oid)),
          apiFetch('/api/object/' + encodeURIComponent(oid) + '/history').catch(() => null)
        ]);
        if (data) {
          if (state.currentOid !== key) return; // Ignore stale response if user switched specimens
          _putPrefetchCache(key, data, hist);
          state.currentRecord = data;
          state.isReviewed = data.review_status === 'reviewed';
          state.currentHistoricalData = (hist && hist.historical_data) ? hist.historical_data : null;
          renderDetailView(renderFull);
          setDetailLoadingState('ready');
          prefetchAdjacentSpecimens(key);
        } else {
          if (state.currentOid !== key) return;
          setDetailLoadingState('error', 'Specimen not found or empty response.');
        }
      } catch(err) {
        console.error('Failed to load specimen detail:', err);
        if (state.currentOid === key) {
          const nameEl = document.getElementById('detailScientificName');
          if (nameEl) nameEl.textContent = 'Failed to load specimen';
          setDetailLoadingState('error', 'Connection error loading #' + key + '.');
          if (typeof showToast === 'function') showToast('Could not load #' + key + ' — tap Retry.', true);
        }
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
      const isSpecialistNote = isProblemActiveOnRecord('Other_problem', rec);
      const bottomSpecBtn = document.getElementById('btnDetailNeedsSpecialist');
      if (bottomSpecBtn) {
        bottomSpecBtn.setAttribute('aria-pressed', isSpecialistNote ? 'true' : 'false');
        bottomSpecBtn.className = isSpecialistNote
          ? 'min-h-[42px] px-3.5 py-2.5 bg-teal-50 text-teal-800 border border-teal-400 rounded font-sans font-semibold text-xs flex items-center justify-center gap-1.5 transition-colors tap-active'
          : 'min-h-[42px] px-3.5 py-2.5 bg-white hover:bg-stone-50 text-muted border border-stone-300 rounded font-sans font-semibold text-xs flex items-center justify-center gap-1.5 transition-colors tap-active';
      }
      const actionableProblemsCount = Math.max(0, activeProblemsCount - (isSpecialistNote ? 1 : 0));
      const hasActionableFlags = actionableProblemsCount > 0;
      const hasFlags = hasActionableFlags;

      if (state.isReviewed) {
        if (hasActionableFlags) {
          // Tri-State: REVIEWED WITH ACTIONABLE ISSUES (Amber #F57C00 / bg-amber-50)
          const issueCount = actionableProblemsCount;
          statusBtn.className = 'flex items-center gap-1.5 text-[11px] font-mono font-semibold px-2 py-0.5 rounded border transition-colors tap-highlight-transparent bg-amber-50 text-amber-900 border-amber-300';
          statusText.textContent = `[REV+ERR] · ${issueCount}`;
          statusDot.className = 'w-1.5 h-1.5 rounded-full bg-amber-500';
          if (detailRevBtn) {
            detailRevBtn.className = 'flex-1 py-2.5 px-4 rounded font-sans font-bold text-xs flex items-center justify-center gap-2 border transition-all tap-active bg-amber-600 text-white border-amber-700 shadow-sm';
            if (detailRevLabel) detailRevLabel.textContent = `Reviewed (${issueCount} Issue${issueCount === 1 ? '' : 's'} Queued)`;
            if (detailRevIcon) detailRevIcon.textContent = '⚠';
          }
        } else if (isSpecialistNote) {
          // Tier 2: REVIEWED WITH SPECIALIST NOTE ONLY (Calm Teal — distinct from REV, CFCT, and REV+ERR)
          statusBtn.className = 'flex items-center gap-1.5 text-[11px] font-mono font-semibold px-2 py-0.5 rounded border transition-colors tap-highlight-transparent bg-teal-50 text-teal-800 border-teal-300';
          statusText.textContent = '[REV+NOTE]';
          statusDot.className = 'w-1.5 h-1.5 rounded-full bg-teal-600';
          if (detailRevBtn) {
            detailRevBtn.className = 'flex-1 py-2.5 px-4 rounded font-sans font-bold text-xs flex items-center justify-center gap-2 border transition-all tap-active bg-teal-700 text-white border-teal-800 shadow-sm';
            if (detailRevLabel) detailRevLabel.textContent = 'Reviewed (Specialist Note)';
            if (detailRevIcon) detailRevIcon.textContent = '📝';
          }
        } else {
          // Tri-State: REVIEWED CLEAN (Emerald)
          statusBtn.className = 'flex items-center gap-1.5 text-[11px] font-mono font-semibold px-2 py-0.5 rounded border transition-colors tap-highlight-transparent bg-emerald-50 text-fern-dark border-fern/30';
          statusText.textContent = '[REV]';
          statusDot.className = 'w-1.5 h-1.5 rounded-full bg-fern';
          if (detailRevBtn) {
            detailRevBtn.className = 'flex-1 py-2.5 px-4 rounded font-sans font-bold text-xs flex items-center justify-center gap-2 border transition-all tap-active bg-emerald-600 text-white border-emerald-700 shadow-sm';
            if (detailRevLabel) detailRevLabel.textContent = 'Reviewed (Tap to Unmark)';
            if (detailRevIcon) detailRevIcon.textContent = '✓';
          }
        }
      } else if (hasActionableFlags) {
        // Tri-State: UNREVIEWED WITH ACTIVE FLAGS (Amber/Brick cue matching List View)
        const issueCount = actionableProblemsCount;
        statusBtn.className = 'flex items-center gap-1.5 text-[11px] font-mono font-semibold px-2 py-0.5 rounded border transition-colors tap-highlight-transparent bg-amber-50 text-amber-900 border-amber-300';
        statusText.textContent = `[UNREV] · ⚠ ${issueCount}`;
        statusDot.className = 'w-1.5 h-1.5 rounded-full bg-brick';
        if (detailRevBtn) {
          detailRevBtn.className = 'flex-1 py-2.5 px-4 rounded font-sans font-bold text-xs flex items-center justify-center gap-2 border transition-all tap-active bg-emerald-50 text-fern-dark border-fern hover:bg-emerald-100 shadow-2xs';
          if (detailRevLabel) detailRevLabel.textContent = 'Mark Reviewed';
          if (detailRevIcon) detailRevIcon.textContent = '✓';
        }
      } else if (isSpecialistNote) {
        // Tier 2: UNREVIEWED WITH SPECIALIST NOTE ONLY (Indigo-Slate — distinct from UNREV and CFCT)
        statusBtn.className = 'flex items-center gap-1.5 text-[11px] font-mono font-semibold px-2 py-0.5 rounded border transition-colors tap-highlight-transparent bg-indigo-50 text-indigo-800 border-indigo-300';
        statusText.textContent = '[NOTE]';
        statusDot.className = 'w-1.5 h-1.5 rounded-full bg-indigo-500';
        if (detailRevBtn) {
          detailRevBtn.className = 'flex-1 py-2.5 px-4 rounded font-sans font-bold text-xs flex items-center justify-center gap-2 border transition-all tap-active bg-emerald-50 text-fern-dark border-fern hover:bg-emerald-100 shadow-2xs';
          if (detailRevLabel) detailRevLabel.textContent = 'Mark Reviewed';
          if (detailRevIcon) detailRevIcon.textContent = '✓';
        }
      } else {
        // Tri-State: UNREVIEWED (Stone / Amber pulse)
        statusBtn.className = 'flex items-center gap-1.5 text-[11px] font-mono font-semibold px-2 py-0.5 rounded border transition-colors tap-highlight-transparent bg-stone-100 text-stone-700 border-stone-300';
        statusText.textContent = '[UNREV]';
        statusDot.className = 'w-1.5 h-1.5 rounded-full bg-amber-500 animate-pulse';
        if (detailRevBtn) {
          detailRevBtn.className = 'flex-1 py-2.5 px-4 rounded font-sans font-bold text-xs flex items-center justify-center gap-2 border transition-all tap-active bg-emerald-50 text-fern-dark border-fern hover:bg-emerald-100 shadow-2xs';
          if (detailRevLabel) detailRevLabel.textContent = 'Mark Reviewed';
          if (detailRevIcon) detailRevIcon.textContent = '✓';
        }
      }

      // Reassurance micro-copy (truthful about whether location is actually recorded)
      const hasLocation = Boolean(
        String(obs.Building || '').trim() ||
        String(obs.Floor ?? '').trim() ||
        String(obs.Cabinet || '').trim() ||
        String(obs.Shelf || '').trim()
      );
      const helperEl = document.getElementById('reviewHelperText');
      if (helperEl) {
        if (state.isReviewed) {
          if (hasActionableFlags) {
            helperEl.textContent = hasLocation
              ? '✓ Checked & location saved. Flagged issues queued for the desk.'
              : '✓ Marked reviewed with flagged issues queued for the desk (no location set).';
          } else if (isSpecialistNote) {
            helperEl.textContent = hasLocation
              ? '✓ Checked & location saved. Flagged as Needs Specialist [REV+NOTE].'
              : '✓ Marked reviewed with Needs Specialist note [REV+NOTE].';
          } else {
            helperEl.textContent = hasLocation
              ? '✓ Physical check & location saved. Specimen clean.'
              : '✓ Marked reviewed (location not recorded yet).';
          }
        } else {
          if (hasActionableFlags) {
            helperEl.textContent = 'Physical check needed. Flagged issues stay saved when you mark reviewed.';
          } else if (isSpecialistNote) {
            helperEl.textContent = 'Physical check needed. Needs Specialist note stays saved as [REV+NOTE].';
          } else {
            helperEl.textContent = 'Check the real object & save its location, then mark reviewed.';
          }
        }
      }

      // Specimen index in list
      const curIdx = state.objectList.findIndex(o => String(o.id) === String(rec.id));
      document.getElementById('detailCurrentIdx').textContent = curIdx >= 0 ? curIdx + 1 : 1;
      document.getElementById('detailTotalCount').textContent = state.totalMatching || state.objectList.length || 1;

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
      if (typeof coachTick === 'function') coachTick();
      if (typeof maybeShowTip === 'function') {
        const totalFlagged = countActiveProblemsOnRecord(rec);
        const hasOnlySpecialist = isProblemActiveOnRecord('Other_problem', rec);
        const actionableCnt = Math.max(0, totalFlagged - (hasOnlySpecialist ? 1 : 0));
        const histBadgeEl = document.getElementById('tabHistoryBadge');
        const histCnt = histBadgeEl && !histBadgeEl.classList.contains('hidden') ? (parseInt(histBadgeEl.textContent, 10) || 0) : 0;
        if (actionableCnt > 0 || histCnt > 0) {
          maybeShowTip('tip_flagged');
        }
      }
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

    function _getStoredAsChoicesList() {
      let choices = state.storedAsChoices && state.storedAsChoices.length > 0
        ? [...state.storedAsChoices]
        : ['Herbarium Sheet', 'Box', 'Envelope', 'Jar', 'Packet', 'Other', 'Custom'];
      ['Other', 'Custom'].forEach(opt => {
        if (!choices.includes(opt)) choices.push(opt);
      });
      return choices;
    }

    function renderDetailStoredAsPills(currentStored) {
      const storedVal = currentStored !== undefined ? currentStored : (state.currentRecord?.observation?.['Stored as'] || '');
      const choices = _getStoredAsChoicesList();
      const isCustomVal = Boolean(storedVal && !choices.includes(storedVal) && storedVal !== 'Custom' && storedVal !== 'Other');

      const labelEl = document.getElementById('detailStoredAsLabel');
      if (labelEl) {
        labelEl.textContent = storedVal || 'Not Selected';
        labelEl.className = storedVal
          ? 'font-mono text-xs text-fern-dark font-bold block truncate'
          : 'font-mono text-xs text-ink-muted font-medium block truncate';
      }

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

    function openDetailStoredAsSheet() {
      const sheet = document.getElementById('storedAsBottomSheet');
      const optionsEl = document.getElementById('storedAsModalOptions');
      if (!sheet || !optionsEl) return;

      const current = state.currentRecord?.observation?.['Stored as'] || '';
      const choices = _getStoredAsChoicesList();
      const isCustomVal = Boolean(current && !choices.includes(current) && current !== 'Custom' && current !== 'Other');

      let html = `
        <button type="button" onclick="selectDetailStorageOption('')" class="w-full min-h-[44px] px-3.5 py-2.5 rounded-lg border ${!current ? 'border-fern bg-emerald-50 text-fern-dark font-bold' : 'border-bordercol bg-white text-ink-muted'} flex items-center justify-between text-left tap-active">
          <span>Not Selected (Clear)</span>
          ${!current ? '<span class="text-fern-dark font-bold">✓</span>' : ''}
        </button>
      `;

      choices.forEach(opt => {
        const isSel = (opt === current) || (opt === 'Custom' && isCustomVal);
        const safeArg = JSON.stringify(opt).replace(/"/g, '&quot;');
        const displayLabel = (opt === 'Custom' && isCustomVal) ? `Custom (${current})` : opt;
        html += `
          <button type="button" onclick="selectDetailStorageOption(${safeArg})" class="w-full min-h-[44px] px-3.5 py-2.5 rounded-lg border ${isSel ? 'border-2 border-fern bg-emerald-50 text-fern-dark font-bold' : 'border-bordercol bg-white text-ink'} flex items-center justify-between gap-2 text-left tap-active">
            <span class="truncate">${displayLabel}</span>
            ${isSel ? '<span class="text-fern-dark font-bold shrink-0">✓</span>' : ''}
          </button>
        `;
      });

      optionsEl.innerHTML = html;
      sheet.classList.remove('hidden');
    }

    function closeStoredAsBottomSheet() {
      const sheet = document.getElementById('storedAsBottomSheet');
      if (sheet) sheet.classList.add('hidden');
    }

    function selectDetailStorageOption(opt) {
      closeStoredAsBottomSheet();
      if (!state.currentRecord) return;
      state.currentRecord.observation = state.currentRecord.observation || {};
      state.currentRecord.observation['Stored as'] = opt;
      markDirty('Stored as');
      renderDetailStoredAsPills(opt);
      updateDetailLocBreadcrumbs(state.currentRecord.observation);
      armActiveTargetLocation(state.currentRecord.observation);
      triggerAutoSave();
      if (opt === 'Custom') {
        const customInput = document.getElementById('detailStoredAsCustomInput');
        if (customInput) setTimeout(() => customInput.focus(), 60);
      }
    }

    function selectDetailStoragePill(opt) {
      selectDetailStorageOption(opt);
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

    function _formatTodayDDMMYYYY() {
      const d = new Date();
      const dd = String(d.getDate()).padStart(2, '0');
      const mm = String(d.getMonth() + 1).padStart(2, '0');
      const yyyy = d.getFullYear();
      return `${dd}.${mm}.${yyyy}`;
    }

    // Availability / Loan Status
    function setLoanStatus(isLoaned) {
      if (!state.currentRecord) return;
      state.currentRecord.observation = state.currentRecord.observation || {};
      state.currentRecord.observation['Loaned out'] = isLoaned;
      markDirty('Loaned out');

      if (isLoaned) {
        if (!String(state.currentRecord.observation['Loaned out date'] || '').trim()) {
          state.currentRecord.observation['Loaned out date'] = _formatTodayDDMMYYYY();
          markDirty('Loaned out date');
        }
      } else {
        if (state.currentRecord.observation['Loaned out date']) {
          state.currentRecord.observation['Loaned out date'] = '';
          markDirty('Loaned out date');
        }
      }

      renderLoanStatus(isLoaned);
      triggerAutoSave();
      showToast(isLoaned ? '↗ Marked Loaned Out' : '✓ Marked In Collection');
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
      const headerPill = document.getElementById('badgeLoanedHeader');
      const loanDate = String(state.currentRecord?.observation?.['Loaned out date'] || '').trim();

      if (headerPill) {
        if (isLoanedBool) {
          headerPill.textContent = loanDate ? `↗ Loaned · ${loanDate}` : '↗ Loaned Out';
          headerPill.classList.remove('hidden');
        } else {
          headerPill.classList.add('hidden');
        }
      }

      if (isLoanedBool) {
        if (btnLoan) btnLoan.className = 'py-2 px-2 rounded text-xs font-mono font-semibold flex items-center justify-center gap-1.5 transition-all bg-white text-ink border border-stone-300 min-h-[42px]';
        if (btnAvail) btnAvail.className = 'py-2 px-2 rounded text-xs font-mono font-medium flex items-center justify-center gap-1.5 transition-all text-muted hover:text-ink min-h-[42px]';
        if (tag) {
          tag.textContent = loanDate ? `Loaned Out · ${loanDate}` : 'Loaned Out';
          tag.className = 'text-[10px] font-mono font-semibold px-1.5 py-0.5 rounded bg-amber-50 text-amber-800 border border-amber-300';
        }
        if (dot) dot.className = 'w-2 h-2 rounded-full bg-amber-500';
      } else {
        if (btnAvail) btnAvail.className = 'py-2 px-2 rounded text-xs font-mono font-semibold flex items-center justify-center gap-1.5 transition-all bg-white text-ink border border-stone-300 min-h-[42px]';
        if (btnLoan) btnLoan.className = 'py-2 px-2 rounded text-xs font-mono font-medium flex items-center justify-center gap-1.5 transition-all text-muted hover:text-ink min-h-[42px]';
        if (tag) {
          tag.textContent = 'In Collection';
          tag.className = 'text-[10px] font-mono font-semibold px-1.5 py-0.5 rounded bg-fern-light text-fern border border-fern/30';
        }
        if (dot) dot.className = 'w-2 h-2 rounded-full bg-fern';
      }
    }

    function countActiveProblemsOnRecord(rec) {
      if (!rec) return 0;
      const activeKeys = new Set();
      const obs = rec.observation || {};
      for (const [k, v] of Object.entries(obs)) {
        if (k.toLowerCase().includes('problem') && (v === true || String(v).toLowerCase() === 'true' || v === 1 || String(v) === '1')) {
          activeKeys.add(k.toLowerCase());
        }
      }
      if (Array.isArray(rec.flagged_issues)) {
        rec.flagged_issues.forEach(i => {
          if (i && !i.resolved) {
            const key = String(i.problem || i.field || i.name || i.id || '').trim().toLowerCase();
            if (key) activeKeys.add(key);
          }
        });
      }
      return activeKeys.size;
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
      initTouchGestures();
      initPhotoViewerTouchGestures();
    }

    function stampArmedLocation() {
      if (!state.currentRecord) return;
      const armed = state.armedLocation;
      if (!armed || (!armed.cabinet && !armed.shelf)) {
        showToast('Set My Current Shelf first');
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
      renderDetailView(false);
      triggerAutoSave();
      triggerHaptic('copy_prev');

      const armedCab = String(armed.cabinet || '—').padStart(2, '0');
      const armedShelf = String(armed.shelf || '—').padStart(2, '0');
      const undoStamp = () => {
        if (!state.currentRecord) return;
        state.currentRecord.observation = state.currentRecord.observation || {};
        const liveObs = state.currentRecord.observation;
        liveObs.Building = prevLoc.Building !== undefined ? prevLoc.Building : '';
        markDirty('Building');
        liveObs.Floor = prevLoc.Floor !== undefined ? prevLoc.Floor : '';
        markDirty('Floor');
        liveObs.Cabinet = prevLoc.Cabinet !== undefined ? prevLoc.Cabinet : '';
        markDirty('Cabinet');
        liveObs.Shelf = prevLoc.Shelf !== undefined ? prevLoc.Shelf : '';
        markDirty('Shelf');
        if (prevLoc['Stored as'] !== undefined) { liveObs['Stored as'] = prevLoc['Stored as']; markDirty('Stored as'); }
        renderCoordinateSteppers(liveObs);
        populateDetailBuildingOptions(liveObs.Building);
        renderDetailStoredAsPills(liveObs['Stored as']);
        updateDetailLocBreadcrumbs(liveObs);
        updateArmedShelfBannerUI(liveObs);
        renderDetailView(false);
        triggerAutoSave();
        showToast(wasRelocation ? '↩ Move undone' : '↩ Shelf save undone');
      };

      const toastMsg = wasRelocation
        ? `⚠️ Moved from Cab ${prevLoc.Cabinet || '?'} to Cab ${armedCab} · Sh ${armedShelf}`
        : `📍 Saved to Cab ${armedCab} · Sh ${armedShelf}`;
      if (typeof coachTick === 'function') coachTick();

      showToast(toastMsg, {
        actionText: '↩ Undo',
        duration: 5000,
        onAction: undoStamp
      });
    }

    function updateArmedShelfBannerUI(obs = {}) {
      const banner = document.getElementById('armedShelfBanner');
      const label = document.getElementById('armedShelfHeaderLabel');
      const stampBtn = document.getElementById('btnStampArmedShelf');
      if (!banner || !label) return;

      const armed = state.armedLocation;
      const hasArmed = Boolean(armed && (armed.cabinet || armed.shelf));

      if (!hasArmed) {
        label.textContent = 'Not set (optional)';
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
          label.textContent = `✓ On Cab ${armedCab} · Sh ${armedShelf}`;
        } else {
          stampBtn.classList.remove('hidden');
          const hasExistingLoc = Boolean(curCabNorm || curShelfNorm || curBldg || curFloor);
          const isRelocating = hasExistingLoc && !matches;
          if (isRelocating) {
            stampBtn.className = 'min-h-[40px] px-3 py-1.5 rounded bg-amber-600 hover:bg-amber-700 text-white font-mono font-bold text-[11px] shadow-2xs tap-active flex items-center gap-1 transition-all shrink-0 whitespace-nowrap';
            stampBtn.innerHTML = `<span>⚠️</span><span>Move to Cab ${armedCab} · Sh ${armedShelf}</span>`;
          } else {
            stampBtn.className = 'min-h-[40px] px-3 py-1.5 rounded bg-fern hover:bg-fern-dark text-white font-mono font-bold text-[11px] shadow-2xs tap-active flex items-center gap-1 transition-all shrink-0 whitespace-nowrap';
            stampBtn.innerHTML = `<span>📍</span><span>Save to Cab ${armedCab} · Sh ${armedShelf}</span>`;
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
      if (obs.Floor !== undefined && obs.Floor !== null && String(obs.Floor).trim() !== '' && String(obs.Floor).trim() !== '—') locBreadcrumb.push(`Fl ${obs.Floor}`);
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
          locBadge.className = 'font-mono text-[10px] font-bold px-1.5 rounded-full bg-emerald-600 text-white shadow-2xs whitespace-nowrap shrink-0';
        } else {
          locBadge.textContent = 'Unset';
          locBadge.className = 'font-mono text-[10px] font-bold px-1.5 rounded-full bg-amber-500 text-white shadow-2xs whitespace-nowrap shrink-0';
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
        const wasReviewed = state.isReviewed;
        toggleReviewed();
        // Gentle non-blocking reminder if newly marked reviewed with no saved location
        if (!wasReviewed && state.isReviewed && !_toastHasActiveAction) {
          const obsNow = (state.currentRecord && state.currentRecord.observation) || {};
          const cabNow = String(obsNow.Cabinet || '').trim();
          const shelfNow = String(obsNow.Shelf || '').trim();
          const noLoc = (!cabNow || cabNow === '—') && (!shelfNow || shelfNow === '—');
          if (noLoc) {
            showToast("✓ Reviewed. Tip: save where it's stored first", {
              actionLabel: '📍 Set Shelf',
              action: () => (state.armedLocation ? stampArmedLocation() : openStationSetup()),
              duration: 6000
            });
          }
        }
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
      if (typeof coachTick === 'function') coachTick();
      if (state.isReviewed && state.currentRecord && typeof maybeShowTip === 'function') {
        const actionableCnt = countActiveProblemsOnRecord(state.currentRecord);
        if (actionableCnt > 0) {
          maybeShowTip('tip_rev_err');
        }
      }
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
      else if (tab === 'history' || tab === 'problems') idx = 2;
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

      if (idx === 2 && typeof maybeShowTip === 'function') {
        maybeShowTip('tip_history');
      }
    }

    let _touchGesturesBound = false;
    function initTouchGestures() {
      if (_touchGesturesBound) return;
      _touchGesturesBound = true;

      // 1. Horizontal swipe between Details / Location / Problems tabs on #swipeArea
      const swipeArea = document.getElementById('swipeArea');
      if (swipeArea) {
        let startX = 0;
        let startY = 0;
        let startTime = 0;
        let tracking = false;

        swipeArea.addEventListener('touchstart', (e) => {
          if (!e.touches || e.touches.length !== 1) {
            tracking = false;
            return;
          }
          const target = e.target;
          if (target && target.closest && target.closest('input, textarea, select, [data-no-swipe]')) {
            tracking = false;
            return;
          }
          // Skip if starting inside an actively horizontally-scrollable strip
          const hScroll = target && target.closest ? target.closest('.overflow-x-auto') : null;
          if (hScroll && hScroll.scrollWidth > hScroll.clientWidth + 4) {
            tracking = false;
            return;
          }
          startX = e.touches[0].clientX;
          if (startX <= 28) {
            // Yield left-edge touches to predictive back gesture
            tracking = false;
            return;
          }
          startY = e.touches[0].clientY;
          startTime = Date.now();
          tracking = true;
        }, { passive: true });

        swipeArea.addEventListener('touchend', (e) => {
          if (!tracking || !e.changedTouches || e.changedTouches.length === 0) return;
          tracking = false;
          const dx = e.changedTouches[0].clientX - startX;
          const dy = e.changedTouches[0].clientY - startY;
          const dt = Date.now() - startTime;
          if (dt > 700) return;
          if (Math.abs(dx) >= 52 && Math.abs(dx) > Math.abs(dy) * 1.5) {
            const nextIdx = dx < 0
              ? Math.min(2, currentTabIdx + 1)
              : Math.max(0, currentTabIdx - 1);
            if (nextIdx !== currentTabIdx) {
              switchTab(nextIdx);
              if (typeof triggerHaptic === 'function') triggerHaptic('light');
            }
          }
        }, { passive: true });
      }

      // 2. Predictive Back: History API popstate + left-edge interactive drag-to-back on #detailView
      window.addEventListener('popstate', () => {
        const openModal = document.querySelector('.fixed.inset-0.z-50:not(.hidden)');
        if (openModal) {
          openModal.classList.add('hidden');
          return;
        }
        const detailEl = document.getElementById('detailView');
        const batchEl = document.getElementById('batchLocationView');
        if ((detailEl && !detailEl.classList.contains('hidden')) || (batchEl && !batchEl.classList.contains('hidden'))) {
          _historyDepth = 0;
          showListView({ fromPopState: true });
        }
      });

      const detailViewEl = document.getElementById('detailView');
      const listViewEl = document.getElementById('listView');
      if (detailViewEl && listViewEl) {
        let edgeStartX = 0;
        let edgeStartY = 0;
        let edgeDx = 0;
        let edgeTracking = false;
        let edgeCommitted = false;

        detailViewEl.addEventListener('touchstart', (e) => {
          if (!e.touches || e.touches.length !== 1) return;
          if (e.touches[0].clientX > 28) return;
          if (document.querySelector('.fixed.inset-0.z-50:not(.hidden)')) return;
          edgeStartX = e.touches[0].clientX;
          edgeStartY = e.touches[0].clientY;
          edgeDx = 0;
          edgeTracking = true;
          edgeCommitted = false;
        }, { passive: true });

        detailViewEl.addEventListener('touchmove', (e) => {
          if (!edgeTracking || !e.touches || e.touches.length !== 1) return;
          const dx = e.touches[0].clientX - edgeStartX;
          const dy = e.touches[0].clientY - edgeStartY;
          if (!edgeCommitted) {
            if (Math.abs(dy) > Math.abs(dx) && Math.abs(dy) > 10) {
              edgeTracking = false;
              return;
            }
            if (dx > 12) {
              edgeCommitted = true;
              listViewEl.classList.remove('hidden');
              listViewEl.style.pointerEvents = 'none';
              detailViewEl.style.transition = 'none';
              detailViewEl.style.boxShadow = '-8px 0 24px rgba(0,0,0,0.18)';
            } else {
              return;
            }
          }
          edgeDx = Math.max(0, dx);
          const progress = Math.min(1, edgeDx / Math.max(1, window.innerWidth));
          detailViewEl.style.transform = `translateX(${edgeDx}px)`;
          listViewEl.style.transform = `scale(${0.97 + 0.03 * progress})`;
          listViewEl.style.opacity = String(0.7 + 0.3 * progress);
        }, { passive: true });

        detailViewEl.addEventListener('touchend', () => {
          if (!edgeTracking) return;
          edgeTracking = false;
          if (!edgeCommitted) return;
          const threshold = window.innerWidth * 0.30;
          detailViewEl.style.transition = 'transform 0.2s cubic-bezier(0.2, 0.8, 0.2, 1)';
          listViewEl.style.transition = 'transform 0.2s ease, opacity 0.2s ease';
          if (edgeDx >= threshold) {
            detailViewEl.style.transform = `translateX(${window.innerWidth}px)`;
            listViewEl.style.transform = 'scale(1)';
            listViewEl.style.opacity = '1';
            setTimeout(() => showListView(), 190);
          } else {
            detailViewEl.style.transform = 'translateX(0)';
            setTimeout(() => {
              listViewEl.classList.add('hidden');
              listViewEl.style.transform = '';
              listViewEl.style.opacity = '';
              listViewEl.style.pointerEvents = '';
              detailViewEl.style.boxShadow = '';
            }, 200);
          }
        }, { passive: true });
      }

      // 3. Swipe-down to dismiss bottom sheets (#storedAsBottomSheet & #stationSetupSheet)
      function _bindSheetSwipeDismiss(cardId, closeFn) {
        const sheetCard = document.getElementById(cardId);
        if (!sheetCard) return;
        let sheetStartY = 0;
        let sheetDragY = 0;
        let sheetDragging = false;

        sheetCard.addEventListener('touchstart', (e) => {
          if (!e.touches || e.touches.length !== 1) return;
          if (e.target && e.target.closest && e.target.closest('input, select, textarea')) return;
          if (sheetCard.scrollTop > 2) return;
          sheetStartY = e.touches[0].clientY;
          sheetDragY = 0;
          sheetDragging = true;
          sheetCard.style.transition = 'none';
        }, { passive: true });

        sheetCard.addEventListener('touchmove', (e) => {
          if (!sheetDragging || !e.touches || e.touches.length !== 1) return;
          const dy = e.touches[0].clientY - sheetStartY;
          if (dy > 0) {
            sheetDragY = dy;
            sheetCard.style.transform = `translateY(${Math.min(dy, 260)}px)`;
          } else {
            sheetDragY = 0;
            sheetCard.style.transform = '';
          }
        }, { passive: true });

        sheetCard.addEventListener('touchend', () => {
          if (!sheetDragging) return;
          sheetDragging = false;
          sheetCard.style.transition = '';
          if (sheetDragY >= 85) {
            sheetCard.style.transform = '';
            closeFn();
          } else {
            sheetCard.style.transform = '';
          }
          sheetDragY = 0;
        }, { passive: true });
      }
      _bindSheetSwipeDismiss('storedAsSheetCard', closeStoredAsBottomSheet);
      _bindSheetSwipeDismiss('stationSetupSheetCard', closeStationSetupSheet);
    }

    // -------------------------------------------------------------
    // DETAILS & INLINE PROBLEM CHECKBOXES RENDERING
    // -------------------------------------------------------------
    const INLINE_DETAIL_FIELDS = ['Genus', 'Species', 'Family', 'Author', 'Collector', 'Collection Date', 'Collection place', 'Box label'];

    function _buildFieldToProblemMap(schema) {
      const map = {};
      const defs = (schema && schema.ui_sections && Array.isArray(schema.ui_sections.problems))
        ? schema.ui_sections.problems
        : [];
      defs.forEach(p => {
        if (!p || !p.name) return;
        const target = String(p.maps_to || state.problemToField[p.name] || '').trim();
        if (target && target.toLowerCase() !== 'other') {
          map[target.toLowerCase()] = p.name;
        }
      });
      return map;
    }

    function scrollToFirstFlaggedField() {
      const first = document.querySelector('#tabContentDetails [data-flagged-row="true"]');
      if (first && typeof first.scrollIntoView === 'function') {
        first.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    }

    function renderDynamicForm(schema, record) {
      const container = document.getElementById('dynamicFormContainer');
      if (!container || !schema) return;
      const reg = record.registration || {};
      const obs = record.observation || {};
      const fieldToProb = _buildFieldToProblemMap(schema);

      let html = '<div class="flex items-center justify-between gap-2 mb-0.5">';
      html += '<h3 class="text-xs font-bold text-ink uppercase tracking-wider font-sans">Registration Data</h3>';
      html += '<span class="text-[10px] font-mono text-subdued">Checkbox = Issue</span>';
      html += '</div>';
      html += '<p class="text-[11px] text-muted mb-2 leading-snug">Compare with the real object. Tap a value to set an ICEDIG code, or tap the checkbox to flag an issue.</p>';

      const _icedigCodeSet = new Set(
        (Array.isArray(state.icedigCodeList) && state.icedigCodeList.length > 0)
          ? state.icedigCodeList.map(i => String(i.code || '').toLowerCase())
          : ['unknown:missing', 'unknown:indecipherable', 'unknown:undigitized', 'withheld']
      );

      html += '<div class="space-y-1.5 font-mono text-xs">';
      INLINE_DETAIL_FIELDS.forEach(f => {
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

        const probName = fieldToProb[f.toLowerCase()] || null;
        const isFlagged = probName ? isProblemActiveOnRecord(probName, record) : false;
        const rowBg = isFlagged ? 'bg-red-50/70 border-brick/40 rounded px-2' : 'border-stone-100';
        const safeFieldEsc = escapeHtml(f).replace(/'/g, "\\'");
        const safeProbEsc = escapeHtml(probName || '').replace(/'/g, "\\'");
        const chkHtml = probName ? `
          <button type="button" data-no-swipe="true" onclick="toggleProblemFlag('${probName}')" title="${isFlagged ? 'Clear issue flag on ' + f : 'Flag issue on ' + f}" aria-pressed="${isFlagged ? 'true' : 'false'}" class="inline-flag-btn min-w-[40px] min-h-[40px] -mr-1.5 flex items-center justify-center shrink-0 tap-active">
            <span class="w-5 h-5 rounded flex items-center justify-center text-[11px] font-bold border transition-colors ${isFlagged ? 'bg-brick border-brick text-white' : 'bg-white border-stone-300 text-transparent'}" style="${isFlagged ? 'background:#c93a40;border-color:#c93a40;color:#ffffff;' : ''}">✓</span>
          </button>
        ` : '';

        const isBoxLabel = (f === 'Box label');
        const strVal = String(val || '').trim();
        const isIcedigVal = _icedigCodeSet.has(strVal.toLowerCase());
        const isMultiline = isBoxLabel && strVal && !isIcedigVal && (strVal.indexOf('\\n') !== -1 || strVal.indexOf('\\r') !== -1 || strVal.length > 28);

        if (isMultiline) {
          html += `
            <div data-flagged-row="${isFlagged ? 'true' : 'false'}" class="py-1.5 border-b ${rowBg} space-y-1">
              <div class="flex items-center justify-between gap-1">
                <div class="flex items-center gap-1.5 min-w-0">
                  <span class="text-muted text-[11px] ${isFlagged ? 'text-brick font-bold' : ''}">${f}:</span>
                  <span class="text-[9.5px] font-mono text-subdued">(Full label)</span>
                </div>
                ${chkHtml}
              </div>
              <button type="button" data-no-swipe="true" onclick="openFieldIcedigSheet('${safeFieldEsc}', '${safeProbEsc}')" title="Tap to set ICEDIG code for ${escapeHtml(f)}" class="w-full font-semibold text-ink text-left text-xs whitespace-pre-wrap break-words bg-stone-50 hover:bg-stone-100 border border-stone-200/60 rounded p-2 leading-relaxed tap-active">
                ${escapeHtml(strVal)}
              </button>
            </div>
          `;
        } else {
          const valDisplayHtml = isIcedigVal
            ? `<span class="inline-flex items-center gap-1 px-1.5 py-0.5 rounded bg-amber-50 text-amber-900 border border-amber-300 font-mono text-[11px] font-semibold">${escapeHtml(strVal)}<span class="text-[9px] text-amber-700">▾</span></span>`
            : (strVal
                ? `<span class="font-semibold text-ink text-right break-words">${escapeHtml(strVal)}</span>`
                : `<span class="text-subdued font-mono text-[11px]">— <span class="text-[9px] opacity-70">▾</span></span>`);
          html += `
            <div data-flagged-row="${isFlagged ? 'true' : 'false'}" class="flex items-center justify-between gap-2 py-0.5 border-b ${rowBg}">
              <span class="text-muted text-[11px] shrink-0 ${isFlagged ? 'text-brick font-bold' : ''}">${f}:</span>
              <div class="flex items-center justify-end gap-1.5 min-w-0 flex-1">
                <button type="button" data-no-swipe="true" onclick="openFieldIcedigSheet('${safeFieldEsc}', '${safeProbEsc}')" title="Tap to set ICEDIG code for ${escapeHtml(f)}" class="min-w-[44px] min-h-[40px] px-2 py-1 rounded hover:bg-stone-100/80 flex items-center justify-end text-right max-w-full tap-active">
                  ${valDisplayHtml}
                </button>
                ${chkHtml}
              </div>
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
      const isSpecFlagged = isProblemActiveOnRecord('Other_problem', record);

      const quickTags = (Array.isArray(state.specialistQuickTags) && state.specialistQuickTags.length > 0)
        ? state.specialistQuickTags
        : [
            { label: '+ Damaged', text: 'Damaged' },
            { label: '+ Broken Object / Storage', text: 'Broken object or storage' },
            { label: '+ Mixed Specimen', text: 'Mixed specimen' },
            { label: '+ Needs Specialist ID', text: 'Needs specialist ID' }
          ];
      const quickTagsHtml = quickTags.map(t => {
        const lbl = escapeHtml(t.label || '');
        const valEsc = escapeHtml(t.text || t.label || '').replace(/'/g, "\\'");
        return `<button type="button" data-no-swipe="true" onclick="appendMobileSpecialistTag('${valEsc}')" class="min-h-[36px] px-2.5 py-1.5 rounded text-[11px] font-mono bg-slate-50 hover:bg-slate-100 text-slate-700 border border-slate-200 tap-active">${lbl}</button>`;
      }).join('');

      html += `
        <div id="commentSection" class="mt-4 pt-3 border-t border-bordercol/60 space-y-2">
          <div class="flex items-center justify-between gap-2">
            <div class="flex items-center gap-1.5">
              <svg class="w-3.5 h-3.5 text-fern" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z"/>
              </svg>
              <h4 class="text-xs font-bold text-ink uppercase tracking-wider font-sans">Comment</h4>
            </div>
            <div class="flex items-center gap-1.5">
              <button type="button" data-no-swipe="true" onclick="toggleProblemFlag('Other_problem')" aria-pressed="${isSpecFlagged ? 'true' : 'false'}" class="px-2.5 py-1 text-[11px] font-mono font-semibold rounded border flex items-center gap-1 transition-colors min-h-[40px] tap-active ${isSpecFlagged ? 'bg-teal-50 text-teal-800 border-teal-400' : 'bg-white text-muted border-stone-300 hover:border-teal-400'}">
                <span class="w-3.5 h-3.5 rounded flex items-center justify-center text-[9px] font-bold ${isSpecFlagged ? 'bg-teal-700 text-white' : 'border border-stone-300 text-transparent'}">✓</span>
                <span>Needs Specialist</span>
              </button>
              <button type="button" onclick="openCommentEditor()" class="px-2.5 py-1 text-[11px] font-mono font-medium text-fern hover:text-fern-dark bg-emerald-50 hover:bg-emerald-100 border border-fern/30 rounded flex items-center gap-1 transition-colors touch-target-min">
                <svg class="w-3 h-3 text-fern" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
                <span>${hasComment ? 'Edit' : 'Write'}</span>
              </button>
            </div>
          </div>
          <div id="specialistQuickTagsRow" class="flex flex-wrap gap-1.5 rounded transition-all">
            ${quickTagsHtml}
          </div>
          ${(isSpecFlagged && !hasComment) ? '<p class="text-[11px] font-sans italic text-amber-700">Add a short note for the specialist (for blank/unreadable label fields, tap the field value to set an ICEDIG code).</p>' : ''}
          <div onclick="openCommentEditor()" class="min-h-[72px] p-2.5 bg-stone-50 hover:bg-stone-100/70 border border-stone-200/80 rounded cursor-pointer transition-colors" title="Tap to write or edit comment">
            <p class="font-mono text-xs text-ink whitespace-pre-wrap break-words leading-relaxed ${hasComment ? '' : 'text-subdued italic'}">${hasComment ? escapeHtml(commentRaw) : 'No comment recorded. Tap to write a comment...'}</p>
          </div>
        </div>
      `;

      container.innerHTML = html;
    }

    function _resolveCanonicalRegFieldName(fieldName) {
      if (!fieldName) return fieldName;
      const lower = String(fieldName).trim().toLowerCase();
      const regFields = (state.activeSchema && state.activeSchema.ui_sections && Array.isArray(state.activeSchema.ui_sections.registration))
        ? state.activeSchema.ui_sections.registration
        : [];
      for (const f of regFields) {
        if (f && f.name && String(f.name).trim().toLowerCase() === lower) {
          return f.name;
        }
      }
      const reg = (state.currentRecord && state.currentRecord.registration) || {};
      for (const k of Object.keys(reg)) {
        if (k.trim().toLowerCase() === lower) return k;
      }
      return fieldName;
    }

    function openFieldIcedigSheet(fieldName, probName) {
      if (!state.currentRecord) return;
      const canonicalField = _resolveCanonicalRegFieldName(fieldName);
      const sheet = document.getElementById('icedigFieldSheet');
      const titleEl = document.getElementById('icedigSheetTitle');
      const optsEl = document.getElementById('icedigSheetOptions');
      const warnEl = document.getElementById('icedigSheetConflictWarn');
      if (!sheet || !optsEl) return;
      if (titleEl) titleEl.textContent = `ICEDIG Status — ${canonicalField}`;
      const reg = state.currentRecord.registration || {};
      const obs = state.currentRecord.observation || {};
      const rawCur = (obs[canonicalField] !== undefined && String(obs[canonicalField]).trim() !== '')
        ? obs[canonicalField]
        : (reg[canonicalField] !== undefined ? reg[canonicalField] : (reg[fieldName] || ''));
      const currentVal = String(rawCur || '').trim().toLowerCase();

      // Check if historical books have a differing value for this field
      if (warnEl) {
        const histObj = state.currentHistoricalData || {};
        const hKey = Object.keys(histObj).find(k => k.toLowerCase() === canonicalField.toLowerCase());
        const hMap = hKey ? histObj[hKey] : null;
        const hasHistConflict = Boolean(hMap && Object.keys(hMap).some(v => String(v || '').trim().toLowerCase() !== currentVal));
        warnEl.classList.toggle('hidden', !hasHistConflict);
      }

      const codeList = (Array.isArray(state.icedigCodeList) && state.icedigCodeList.length > 0)
        ? state.icedigCodeList
        : Object.entries(
            (state.icedigCodes && Object.keys(state.icedigCodes).length > 0)
              ? state.icedigCodes
              : {
                  "unknown:missing": "unknown:missing  (blank on original label)",
                  "unknown:indecipherable": "unknown:indecipherable  (illegible on label)",
                  "unknown:undigitized": "unknown:undigitized  (skipped during digitisation)",
                  "withheld": "withheld  (known but intentionally hidden)"
                }
          ).map(([code, fullLabel]) => ({
            code,
            description: String(fullLabel || '').replace(code, '').replace(/^\\s*\\(/, '').replace(/\\)\\s*$/, '').trim()
          }));

      const safeField = canonicalField.replace(/'/g, "\\'");
      const safeProb = String(probName || '').replace(/'/g, "\\'");
      let optsHtml = codeList.map(item => {
        const code = item.code;
        const desc = item.description || '';
        const isSel = currentVal === code.toLowerCase();
        const jsCode = code.replace(/'/g, "\\'");
        return `
          <button type="button" onclick="applyDetailsFieldIcedig('${safeField}', '${safeProb}', '${jsCode}')" class="w-full min-h-[44px] text-left p-2.5 rounded border transition-all tap-active ${isSel ? 'border-2 border-fern bg-emerald-50 text-fern-dark font-semibold' : 'border-bordercol bg-white text-ink hover:bg-stone-50'}">
            <div class="font-mono text-xs font-bold">${escapeHtml(code)} ${isSel ? '✓' : ''}</div>
            <div class="text-[10.5px] font-sans text-muted mt-0.5">${escapeHtml(desc)}</div>
          </button>
        `;
      }).join('');

      if (currentVal) {
        optsHtml += `
          <button type="button" onclick="applyDetailsFieldIcedig('${safeField}', '${safeProb}', '')" class="w-full min-h-[40px] text-left px-2.5 py-2 rounded border border-stone-300 bg-stone-50 hover:bg-stone-100 text-ink-muted font-mono text-xs font-semibold tap-active mt-1">
            ✕ Clear field value
          </button>
        `;
      }

      optsEl.innerHTML = optsHtml;
      sheet.classList.remove('hidden');
      if (typeof maybeShowTip === 'function') {
        maybeShowTip('tip_icedig', { allowOverModal: true });
      }
    }

    function closeFieldIcedigSheet() {
      const sheet = document.getElementById('icedigFieldSheet');
      if (sheet) sheet.classList.add('hidden');
    }

    function applyDetailsFieldIcedig(fieldName, probName, code) {
      closeFieldIcedigSheet();
      const canonicalField = _resolveCanonicalRegFieldName(fieldName);
      if (probName) {
        resolveFieldDiscrepancy(canonicalField, probName, code, Boolean(code));
      } else if (state.currentRecord) {
        state.currentRecord.registration = state.currentRecord.registration || {};
        state.currentRecord.observation = state.currentRecord.observation || {};
        state.currentRecord.registration[canonicalField] = code;
        state.currentRecord.observation[canonicalField] = code;
        markDirty(canonicalField);
        renderDetailView(false);
        triggerAutoSave();
      }
    }

    function appendMobileSpecialistTag(tagText) {
      if (!state.currentRecord) return;
      state.currentRecord.observation = state.currentRecord.observation || {};
      const obs = state.currentRecord.observation;
      const existing = String(obs['Comment'] || '').trim();
      if (existing.toLowerCase().indexOf(tagText.toLowerCase()) === -1) {
        obs['Comment'] = existing ? (existing + '; ' + tagText) : tagText;
        markDirty('Comment');
      }
      obs['Other_problem'] = true;
      markDirty('Other_problem');
      renderDetailView(false);
      triggerAutoSave();
      showToast('Added "' + tagText + '" & flagged Needs Specialist', 'info');
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
      if (countDisp) countDisp.textContent = 'Checking for photos...';
      tryLoadPhotoCandidate(0);
    }

    function tryLoadPhotoCandidate(idx) {
      if (!currentPhotoCandidates || idx >= currentPhotoCandidates.length) {
        collapseEmptyPhotoFolio('No photos attached');
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
      const photoTotal = (currentPhotoCandidates && currentPhotoCandidates.length) ? currentPhotoCandidates.length : 1;
      if (countDisp) countDisp.textContent = `${photoTotal} Photo${photoTotal === 1 ? '' : 's'}`;
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

    function collapseEmptyPhotoFolio(reason = 'No photos attached') {
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
          <div class="py-1.5 px-2.5 bg-stone-100 rounded border border-bordercol/70 flex items-center justify-between text-xs font-sans text-muted">
            <span class="flex items-center gap-1.5 text-stone-500">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
              ${reason}
            </span>
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
      const modal = document.getElementById('photoViewerModal');
      if (modal) modal.classList.remove('hidden');
      updatePhotoViewerControls();
      initPhotoViewerTouchGestures();
    }

    function updatePhotoViewerControls() {
      const total = (currentPhotoCandidates && currentPhotoCandidates.length) ? currentPhotoCandidates.length : 0;
      const titleEl = document.getElementById('photoViewerTitle');
      const prevBtn = document.getElementById('btnPhotoPrev');
      const nextBtn = document.getElementById('btnPhotoNext');
      if (titleEl) {
        titleEl.textContent = total > 1
          ? `Specimen Photo (${currentPhotoCandidateIdx + 1} / ${total})`
          : 'Specimen Photo';
      }
      if (prevBtn && nextBtn) {
        if (total > 1) {
          prevBtn.classList.remove('hidden');
          nextBtn.classList.remove('hidden');
        } else {
          prevBtn.classList.add('hidden');
          nextBtn.classList.add('hidden');
        }
      }
    }

    function stepViewerPhoto(delta) {
      if (!currentPhotoCandidates || currentPhotoCandidates.length <= 1) return;
      const total = currentPhotoCandidates.length;
      const nextIdx = (currentPhotoCandidateIdx + delta + total) % total;
      resetPhotoTransform();
      selectPhoto(nextIdx, currentPhotoCandidates[nextIdx]);
      updatePhotoViewerControls();
    }

    function closePhotoViewerModal() {
      document.getElementById('photoViewerModal')?.classList.add('hidden');
    }

    let photoZoom = 1;
    let photoRotation = 0;
    let photoPanX = 0;
    let photoPanY = 0;
    let _photoTouchBound = false;

    function zoomPhoto(delta) {
      photoZoom = Math.min(Math.max(photoZoom + delta, 0.5), 4.5);
      if (photoZoom <= 1.02) {
        photoPanX = 0;
        photoPanY = 0;
      }
      updatePhotoTransform();
    }
    function rotatePhoto() {
      photoRotation = (photoRotation + 90) % 360;
      updatePhotoTransform();
    }
    function resetPhotoTransform() {
      photoZoom = 1;
      photoRotation = 0;
      photoPanX = 0;
      photoPanY = 0;
      updatePhotoTransform();
    }
    function updatePhotoTransform() {
      const img = document.getElementById('photoViewerImg');
      const disp = document.getElementById('zoomLevelDisplay');
      if (disp) disp.textContent = `${photoZoom.toFixed(1)}x`;
      if (img) img.style.transform = `translate(${photoPanX.toFixed(1)}px, ${photoPanY.toFixed(1)}px) scale(${photoZoom}) rotate(${photoRotation}deg)`;
    }

    function initPhotoViewerTouchGestures() {
      if (_photoTouchBound) return;
      const viewport = document.getElementById('photoViewerViewport');
      if (!viewport) return;
      _photoTouchBound = true;

      let pinchStartDist = 0;
      let pinchStartZoom = 1;
      let panStartX = 0;
      let panStartY = 0;
      let panBaseX = 0;
      let panBaseY = 0;
      let isPanning = false;
      let lastTapTime = 0;

      function _touchDist(t0, t1) {
        return Math.hypot(t1.clientX - t0.clientX, t1.clientY - t0.clientY);
      }

      viewport.addEventListener('touchstart', (e) => {
        if (!e.touches) return;
        if (e.touches.length === 2) {
          isPanning = false;
          pinchStartDist = _touchDist(e.touches[0], e.touches[1]) || 1;
          pinchStartZoom = photoZoom;
        } else if (e.touches.length === 1) {
          const now = Date.now();
          if (now - lastTapTime < 280) {
            // Double-tap toggles between 1.0x centered and 2.2x close inspection
            if (photoZoom > 1.2) {
              resetPhotoTransform();
            } else {
              photoZoom = 2.2;
              photoPanX = 0;
              photoPanY = 0;
              updatePhotoTransform();
            }
            lastTapTime = 0;
            isPanning = false;
            return;
          }
          lastTapTime = now;
          if (photoZoom > 1.05) {
            isPanning = true;
            panStartX = e.touches[0].clientX;
            panStartY = e.touches[0].clientY;
            panBaseX = photoPanX;
            panBaseY = photoPanY;
          }
        }
      }, { passive: true });

      viewport.addEventListener('touchmove', (e) => {
        if (!e.touches) return;
        if (e.touches.length === 2 && pinchStartDist > 0) {
          e.preventDefault();
          const dist = _touchDist(e.touches[0], e.touches[1]);
          photoZoom = Math.min(Math.max(pinchStartZoom * (dist / pinchStartDist), 0.8), 4.5);
          if (photoZoom <= 1.02) {
            photoPanX = 0;
            photoPanY = 0;
          }
          updatePhotoTransform();
        } else if (e.touches.length === 1 && isPanning && photoZoom > 1.05) {
          e.preventDefault();
          const maxOffset = Math.max(120, viewport.clientWidth * (photoZoom - 1) * 0.65);
          const dx = e.touches[0].clientX - panStartX;
          const dy = e.touches[0].clientY - panStartY;
          photoPanX = Math.min(Math.max(panBaseX + dx, -maxOffset), maxOffset);
          photoPanY = Math.min(Math.max(panBaseY + dy, -maxOffset), maxOffset);
          updatePhotoTransform();
        }
      }, { passive: false });

      viewport.addEventListener('touchend', (e) => {
        if (!e.touches || e.touches.length < 2) {
          pinchStartDist = 0;
        }
        if (!e.touches || e.touches.length === 0) {
          isPanning = false;
        }
      }, { passive: true });

      // Mouse-drag panning when zoomed (desktop/tablet preview support)
      let mousePanning = false;
      viewport.addEventListener('mousedown', (e) => {
        if (e.button !== 0 || photoZoom <= 1.05 || e.target.closest('button')) return;
        mousePanning = true;
        panStartX = e.clientX;
        panStartY = e.clientY;
        panBaseX = photoPanX;
        panBaseY = photoPanY;
      });
      window.addEventListener('mousemove', (e) => {
        if (!mousePanning || photoZoom <= 1.05) return;
        const maxOffset = Math.max(120, viewport.clientWidth * (photoZoom - 1) * 0.65);
        photoPanX = Math.min(Math.max(panBaseX + (e.clientX - panStartX), -maxOffset), maxOffset);
        photoPanY = Math.min(Math.max(panBaseY + (e.clientY - panStartY), -maxOffset), maxOffset);
        updatePhotoTransform();
      });
      window.addEventListener('mouseup', () => { mousePanning = false; });
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
          { name: 'Other_problem', label: 'Needs Specialist', maps_to: 'Comment' }
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

      // Actionable desk/media problems exclude Other_problem (Needs Specialist)
      const actionableActiveProblems = activeProblems.filter(p => String(p.name || '').toLowerCase() !== 'other_problem');
      const count = actionableActiveProblems.length;

      // 1. Tab 0 (Details) Red Flag Badge & Jump Chip (actionable issues only)
      const detailsFlagBadge = document.getElementById('tabDetailsFlagsBadge');
      if (detailsFlagBadge) {
        if (count > 0) {
          detailsFlagBadge.textContent = count;
          detailsFlagBadge.classList.remove('hidden');
        } else {
          detailsFlagBadge.classList.add('hidden');
        }
      }
      const flagChip = document.getElementById('detailsFlagSummaryChip');
      const flagChipText = document.getElementById('detailsFlagSummaryText');
      if (flagChip && flagChipText) {
        if (count > 0) {
          const names = actionableActiveProblems.slice(0, 3).map(p => humanizeProblemName(p.name));
          const extra = count > 3 ? ` +${count - 3}` : '';
          flagChipText.textContent = `⚠ ${count} flagged: ${names.join(', ')}${extra}`;
          flagChip.classList.remove('hidden');
        } else {
          flagChip.classList.add('hidden');
        }
      }

      // 2. Build Historical Resolver cards list (all fields with historical book data + flagged mapped fields)
      const histObj = state.currentHistoricalData || {};
      const fieldToProb = _buildFieldToProblemMap(state.activeSchema);
      const historyCardsMap = new Map();

      // First include every field that actually has historical suggestions differing from the current value
      const normHistVal = (v) => String(v ?? '').trim().toLowerCase();
      let histSuggestionFieldCount = 0;
      Object.entries(histObj).forEach(([fieldName, hMap]) => {
        if (!hMap || Object.keys(hMap).length === 0) return;
        const curRaw = (obs[fieldName] !== undefined && String(obs[fieldName]).trim() !== '')
          ? obs[fieldName]
          : ((reg[fieldName] !== undefined && String(reg[fieldName]).trim() !== '') ? reg[fieldName] : '');
        const curNorm = normHistVal(curRaw);
        const differingEntries = Object.entries(hMap).filter(([hVal]) => normHistVal(hVal) !== curNorm);
        if (differingEntries.length === 0) return;
        histSuggestionFieldCount++;
        const probName = fieldToProb[fieldName.toLowerCase()] || '';
        historyCardsMap.set(fieldName.toLowerCase(), {
          targetField: fieldName,
          probName: probName,
          isFlagged: probName ? isProblemActiveOnRecord(probName, rec) : false,
          histEntries: differingEntries,
        });
      });

      // Also include flagged data fields so curators can apply manual overrides or ICEDIG codes on History tab
      activeProblems.forEach(p => {
        const targetField = p.maps_to;
        const isGeneralFlag = !targetField || targetField === p.name || p.name.toLowerCase() === 'other_problem';
        if (isGeneralFlag) return;
        const key = targetField.toLowerCase();
        if (!historyCardsMap.has(key)) {
          const hMap = histObj[targetField] || {};
          const curRaw = (obs[targetField] !== undefined && String(obs[targetField]).trim() !== '')
            ? obs[targetField]
            : ((reg[targetField] !== undefined && String(reg[targetField]).trim() !== '') ? reg[targetField] : '');
          const curNorm = normHistVal(curRaw);
          const differingEntries = Object.entries(hMap).filter(([hVal]) => normHistVal(hVal) !== curNorm);
          historyCardsMap.set(key, {
            targetField: targetField,
            probName: p.name,
            isFlagged: true,
            histEntries: differingEntries,
          });
        } else {
          const existing = historyCardsMap.get(key);
          existing.probName = existing.probName || p.name;
          existing.isFlagged = true;
        }
      });

      const historyCards = Array.from(historyCardsMap.values());

      // Tab 2 (History) Slate-Blue Badge
      const tabHistBadge = document.getElementById('tabHistoryBadge');
      if (tabHistBadge) {
        if (histSuggestionFieldCount > 0) {
          tabHistBadge.textContent = histSuggestionFieldCount;
          tabHistBadge.classList.remove('hidden');
        } else {
          tabHistBadge.classList.add('hidden');
        }
      }

      // 3. History Summary Banner
      const summaryBar = document.getElementById('problemSummaryBar');
      const summaryDot = document.getElementById('problemSummaryDot');
      const summaryCountText = document.getElementById('problemSummaryCountText');
      const summaryActionText = document.getElementById('problemSummaryActionText');
      if (summaryBar) {
        if (histSuggestionFieldCount > 0) {
          summaryBar.className = 'flex items-center justify-between p-3 bg-sky-50 border border-sky-200 rounded-[3px] transition-colors duration-200';
          if (summaryDot) summaryDot.className = 'w-2.5 h-2.5 rounded-full bg-sky-700';
          if (summaryCountText) {
            summaryCountText.className = 'text-xs font-bold text-sky-900 uppercase font-mono';
            summaryCountText.textContent = `${historyCards.length} to resolve`;
          }
          if (summaryActionText) {
            summaryActionText.className = 'text-[10px] font-mono text-sky-800 font-semibold';
            summaryActionText.textContent = 'Compare & Apply';
          }
        } else if (historyCards.length > 0) {
          summaryBar.className = 'flex items-center justify-between p-3 bg-amber-50 border border-amber-300 rounded-[3px] transition-colors duration-200';
          if (summaryDot) summaryDot.className = 'w-2.5 h-2.5 rounded-full bg-amber-600';
          if (summaryCountText) {
            summaryCountText.className = 'text-xs font-bold text-amber-900 uppercase font-mono';
            summaryCountText.textContent = `${historyCards.length} to resolve`;
          }
          if (summaryActionText) {
            summaryActionText.className = 'text-[10px] font-mono text-amber-800 font-semibold';
            summaryActionText.textContent = 'Manual Edit / ICEDIG';
          }
        } else {
          summaryBar.className = 'flex items-center justify-between p-3 bg-emerald-50/70 border border-fern/30 rounded-[3px] transition-colors duration-200';
          if (summaryDot) summaryDot.className = 'w-2.5 h-2.5 rounded-full bg-fern';
          if (summaryCountText) {
            summaryCountText.className = 'text-xs font-bold text-fern-dark uppercase font-mono';
            summaryCountText.textContent = 'Nothing to resolve';
          }
          if (summaryActionText) {
            summaryActionText.className = 'text-[10px] font-mono text-fern font-medium';
            summaryActionText.textContent = 'All clear';
          }
        }
      }

      // 4. Historical Resolver Cards Container
      const container = document.getElementById('activeDiscrepanciesContainer');
      if (container) {
        if (historyCards.length === 0) {
          container.innerHTML = `
            <div class="p-6 bg-surface border border-bordercol rounded-[3px] text-center space-y-2.5">
              <div class="w-8 h-8 rounded-full bg-emerald-50 text-fern border border-fern/30 flex items-center justify-center mx-auto text-base">✓</div>
              <div class="text-xs font-mono font-bold text-ink">No problems to resolve</div>
              <p class="text-[11px] text-subdued font-sans max-w-xs mx-auto">This specimen has no open field problems or older catalog conflicts. Swipe back to <strong>Details</strong> to inspect fields or add a specialist note.</p>
              <button type="button" onclick="openOldNamesSheet()" class="mt-1 px-3.5 py-2 min-h-[40px] rounded-full border border-bordercol bg-stone-50 hover:bg-stone-100 text-xs font-semibold text-ink inline-flex items-center gap-1.5 tap-active">
                <span>📜</span><span>Check Old Names &amp; Synonyms</span>
              </button>
            </div>
          `;
        } else {
          container.innerHTML = historyCards.map(item => {
            const targetField = item.targetField;
            const probName = item.probName || '';
            const safeProbKey = probName || targetField.replace(/[^A-Za-z0-9_]/g, '_');
            const currentVal = (obs[targetField] !== undefined && obs[targetField] !== '') ? obs[targetField] : ((reg[targetField] !== undefined && reg[targetField] !== '') ? reg[targetField] : '—');
            const histEntries = item.histEntries || [];

            let histHtml = '';
            if (histEntries.length > 0) {
              histHtml = `
                <div class="space-y-1.5">
                  <span class="text-[9px] uppercase font-bold text-muted block">Historical Suggestions</span>
                  <div class="space-y-1.5">
                    ${histEntries.map(([hVal, sources]) => {
                      const sourcesStr = Array.isArray(sources) ? sources.join(', ') : String(sources);
                      const safeVal = escapeHtml(hVal);
                      const jsVal = safeVal.replace(/'/g, "\\'");
                      return `
                        <div class="p-2 bg-emerald-50/50 border border-fern/30 rounded flex items-center justify-between gap-2">
                          <div class="truncate min-w-0">
                            <span class="font-mono text-xs font-bold text-ink block truncate">${safeVal}</span>
                            <span class="text-[9px] font-mono text-fern-dark block truncate">Source: ${escapeHtml(sourcesStr)}</span>
                          </div>
                          <button type="button" onclick="resolveFieldDiscrepancy('${targetField}', '${probName}', '${jsVal}', true)" class="flex-none min-h-[36px] px-3 py-1 bg-fern hover:bg-fern-dark text-white rounded text-[11px] font-mono font-bold shadow-2xs tap-active" style="background:#2d5a3c;color:#ffffff;">
                            Apply
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
                  No older catalog suggestions for this field.
                </div>
              `;
            }

            const statusChip = item.isFlagged
              ? '<span class="text-[10px] font-mono text-brick bg-brick-light px-1.5 py-0.5 rounded border border-brick/20 font-medium whitespace-nowrap">Flagged</span>'
              : '<span class="text-[10px] font-mono text-sky-900 bg-sky-50 px-1.5 py-0.5 rounded border border-sky-200 font-medium whitespace-nowrap">CFCT</span>';

            const dismissBtn = (item.isFlagged && probName)
              ? `<button type="button" onclick="resolveFieldDiscrepancy('${targetField}', '${probName}', undefined, true)" title="✓ Value is Correct (Clear Flag)" aria-label="✓ Value is Correct (Clear Flag)" class="flex-none text-[10px] font-mono text-muted hover:text-ink px-2.5 py-1 min-h-[36px] rounded bg-stone-100 hover:bg-stone-200 border border-stone-200">✓ Value is Correct</button>`
              : '';

            return `
              <div class="bg-surface border border-bordercol rounded-[3px] p-3.5 shadow-2xs space-y-3">
                <div class="flex items-center justify-between border-b border-stone-100 pb-2">
                  <div class="flex items-center gap-1.5 truncate mr-2">
                    <span class="w-2 h-2 rounded-full ${item.isFlagged ? 'bg-brick' : 'bg-sky-700'} flex-none"></span>
                    <span class="text-xs font-mono font-bold text-ink truncate">${escapeHtml(targetField)}</span>
                    ${statusChip}
                  </div>
                  ${dismissBtn}
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
                  <span class="text-[9px] uppercase font-bold text-muted block mb-1">Type a Value Manually</span>
                  <div class="flex items-center gap-1.5">
                    <input type="text" id="manualInput_${safeProbKey}" placeholder="Enter new value..." class="flex-1 min-h-[38px] bg-white border border-bordercol rounded px-2.5 py-1.5 text-xs font-mono text-ink focus:outline-none focus:border-fern" />
                    <button type="button" onclick="applyManualProblemResolution('${targetField}', '${safeProbKey}', '${probName}')" class="px-3 py-1.5 rounded bg-stone-100 hover:bg-stone-200 active:bg-stone-300 border border-stone-300 text-ink text-xs font-mono font-semibold min-h-[38px] whitespace-nowrap">
                      Apply
                    </button>
                  </div>
                </div>

                <div class="pt-1">
                  <button type="button" onclick="openFieldIcedigSheet('${escapeHtml(targetField).replace(/'/g, "\\'")}', '${escapeHtml(probName || '').replace(/'/g, "\\'")}')" class="w-full min-h-[40px] flex items-center justify-between px-2.5 py-1.5 rounded bg-stone-50 hover:bg-stone-100 border border-stone-200 text-ink text-xs font-mono font-medium transition-colors tap-active">
                    <span>ICEDIG ▾</span>
                    <span class="text-[10px] text-muted"></span>
                  </button>
                </div>
              </div>
            `;
          }).join('');
        }
      }

      // 5. Photo & Media Issues Grid (in Tab 0 Details — non-field flags excluding Other_problem which lives above Comment)
      const flagsCard = document.getElementById('physicalIssuesCard');
      const flagsGrid = document.getElementById('problemFlagsGrid');
      const flaggedBadge = document.getElementById('flaggedTotalBadge');
      const inlineProbSet = new Set(Object.values(fieldToProb));
      if (flaggedBadge) {
        flaggedBadge.textContent = `${count} Flagged`;
      }
      if (flagsGrid) {
        const nonFieldDefs = problemDefs.filter(pDef => pDef && !inlineProbSet.has(pDef.name) && String(pDef.name).toLowerCase() !== 'other_problem');
        if (flagsCard) {
          flagsCard.classList.toggle('hidden', nonFieldDefs.length === 0);
        }
        flagsGrid.innerHTML = nonFieldDefs.map(pDef => {
          const probName = pDef.name;
          const isAct = isProblemActiveOnRecord(probName, rec);
          const formatProblemLabel = (raw) => {
            const clean = String(raw || '').replace(/[_ ]?problem$/i, '').replace(/_/g, ' ').replace(/([a-z])([A-Z])/g, '$1 $2').trim();
            return (!clean || clean.toLowerCase() === 'other') ? 'Needs Specialist' : clean;
          };
          const label = pDef.label ? formatProblemLabel(pDef.label) : formatProblemLabel(probName);
          const activeTileClass = 'border-brick bg-brick-light text-brick font-semibold';
          const activeCheckStyle = 'background:#c93a40;color:#ffffff;';
          return `
            <button type="button" data-no-swipe="true" data-flagged-row="${isAct ? 'true' : 'false'}" onclick="toggleProblemFlag('${probName}')" class="p-2.5 rounded border text-left flex items-start justify-between transition-all tap-highlight-transparent min-h-[44px] ${isAct ? activeTileClass : 'border-stone-200 bg-white text-muted hover:border-stone-300'}">
              <div class="min-w-0 pr-1">
                <span class="text-xs font-sans font-medium block truncate ${isAct ? 'text-brick font-semibold' : 'text-ink'}">${escapeHtml(label)}</span>
              </div>
              <span class="w-4 h-4 rounded flex-none mt-0.5 flex items-center justify-center text-[10px] font-bold ${isAct ? 'text-white' : 'border border-stone-300'}" style="${isAct ? activeCheckStyle : ''}">
                ${isAct ? '✓' : ''}
              </span>
            </button>
          `;
        }).join('');
      }
    }

    function applyManualProblemResolution(targetField, inputKey, probName) {
      const inp = document.getElementById(`manualInput_${inputKey}`);
      if (!inp) return;
      const val = inp.value.trim();
      if (!val) {
        showToast('Please enter a value before applying');
        return;
      }
      resolveFieldDiscrepancy(targetField, probName !== undefined ? probName : inputKey, val, true);
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
      renderDynamicForm(state.activeSchema, state.currentRecord);
      renderProblemsAndDiscrepancies(state.currentRecord);
      renderDetailView(false);
      showToast(newVal !== undefined ? `✓ Applied ${targetField}` : `✓ Cleared ${humanizeProblemName(probName)}`);
    }

    function humanizeProblemName(probName) {
      if (!probName) return 'Issue';
      const raw = String(probName).trim();
      const lower = raw.toLowerCase();
      if (lower === 'other_problem') return 'Needs Specialist';
      if (state.activeSchema && state.activeSchema.ui_sections && Array.isArray(state.activeSchema.ui_sections.problems)) {
        const found = state.activeSchema.ui_sections.problems.find(p => p && p.name === raw);
        if (found && (found.label || found.maps_to)) {
          return String(found.label || found.maps_to).replace(/_/g, ' ').trim();
        }
      }
      return raw.replace(/_?[Pp]roblem$/g, '').replace(/_/g, ' ').replace(/([a-z])([A-Z])/g, '$1 $2').trim() || raw;
    }

    function handleBottomNeedsSpecialistClick() {
      if (!state.currentRecord) return;
      toggleProblemFlag('Other_problem');
      const isNowOn = isProblemActiveOnRecord('Other_problem', state.currentRecord);
      if (isNowOn) {
        switchDetailTab('details');
        setTimeout(() => {
          const sec = document.getElementById('commentSection');
          if (sec && typeof sec.scrollIntoView === 'function') {
            sec.scrollIntoView({ behavior: 'smooth', block: 'center' });
          }
          const tagsRow = document.getElementById('specialistQuickTagsRow');
          if (tagsRow) {
            tagsRow.classList.add('ring-2', 'ring-teal-400', 'bg-teal-50/50', 'p-1');
            setTimeout(() => {
              tagsRow.classList.remove('ring-2', 'ring-teal-400', 'bg-teal-50/50', 'p-1');
            }, 1400);
          }
        }, 120);
      }
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
      renderDynamicForm(state.activeSchema, state.currentRecord);
      renderProblemsAndDiscrepancies(state.currentRecord);
      renderDetailView(false);
      const label = humanizeProblemName(probName);
      showToast(nextVal ? `⚠ Flagged ${label}` : `✓ Cleared ${label}`);
      if (nextVal && String(probName).toLowerCase() === 'other_problem' && typeof maybeShowTip === 'function') {
        maybeShowTip('tip_specialist');
      }
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
              <button type="button" onclick="removeBatchItem(${idx})" class="min-w-[38px] min-h-[38px] flex items-center justify-center rounded hover:bg-stone-100 text-stone-400 hover:text-brick text-sm font-bold tap-active">✕</button>
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
          invalidatePrefetchCache(payload.id);
          dirtyFields.clear();
          triggerHaptic('save_success');
          showToast('✓ Saved & synchronized', { passive: true });
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
      if (typeof renderSettingsTutorialPanel === 'function') renderSettingsTutorialPanel();
      openModal('settingsModal');
    }

    function openSettingsTutorialSection() {
      openSettingsModal();
      setTimeout(() => {
        const sec = document.getElementById('settingsPhoneTutorialSection');
        if (sec && typeof sec.scrollIntoView === 'function') {
          sec.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      }, 80);
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

    function updateFilterActiveDot() {
      const badge = document.getElementById('filterActiveBadge');
      if (!badge) return;
      const hasStatus = Boolean(state.activeStatusFilter && state.activeStatusFilter !== 'all');
      const hasLoc = Boolean(
        state.selectedCabinet ||
        state.selectedShelf ||
        (state.activeAdvancedFilters && state.activeAdvancedFilters.locations && Object.values(state.activeAdvancedFilters.locations).some(v => String(v || '').trim()))
      );
      const hasProb = Boolean(
        state.activeAdvancedFilters && state.activeAdvancedFilters.problems && Object.values(state.activeAdvancedFilters.problems).some(Boolean)
      );
      if (hasStatus || hasLoc || hasProb) badge.classList.remove('hidden');
      else badge.classList.add('hidden');
    }

    function openFilterModal() {
      const locContainer = document.getElementById('filterModalLocations');
      const locFields = (state.activeSchema && state.activeSchema.ui_sections && state.activeSchema.ui_sections.location) || [
        { name: 'Building' }, { name: 'Floor' }, { name: 'Cabinet' }, { name: 'Shelf' }
      ];
      const savedLocs = (state.activeAdvancedFilters && state.activeAdvancedFilters.locations) || {};
      if (locContainer) {
        locContainer.innerHTML = locFields.map(f => {
          const fname = f.name;
          let curVal = savedLocs[fname] || '';
          if (!curVal && fname.toLowerCase() === 'cabinet') curVal = state.selectedCabinet || '';
          if (!curVal && fname.toLowerCase() === 'shelf') curVal = state.selectedShelf || '';
          const safeId = `filterModal_loc_${fname.replace(/[^a-zA-Z0-9_-]/g, '_')}`;
          return `
            <div class="flex items-center justify-between gap-2 text-xs">
              <label for="${safeId}" class="font-mono text-muted text-[11px] w-24 shrink-0 truncate">${fname}:</label>
              <input type="text" id="${safeId}" data-loc-field="${fname.replace(/"/g, '&quot;')}" value="${String(curVal).replace(/"/g, '&quot;')}" placeholder="Any ${fname}..." class="flex-1 min-h-[40px] bg-stone-50 border border-bordercol rounded px-2.5 py-1.5 text-xs font-mono text-ink outline-none focus:border-fern" />
            </div>
          `;
        }).join('');
      }

      const probContainer = document.getElementById('filterModalProblems');
      if (probContainer) {
        const curStatus = state.activeStatusFilter || 'all';
        const statusOpts = [
          { val: 'all', label: 'All Objects' },
          { val: 'pending', label: 'Unreviewed' },
          { val: 'reviewed', label: 'Reviewed' },
          { val: 'flagged', label: 'Flagged' },
          { val: 'conflict', label: 'Conflicts' }
        ];
        const savedProbs = (state.activeAdvancedFilters && state.activeAdvancedFilters.problems) || {};
        const schemaProbs = (state.activeSchema && state.activeSchema.ui_sections && Array.isArray(state.activeSchema.ui_sections.problems))
          ? state.activeSchema.ui_sections.problems
          : [{ name: 'Other_problem', label: 'Needs Specialist' }];

        let html = `
          <div class="mb-2.5">
            <div class="text-[11px] font-mono text-muted mb-1.5">Review Status:</div>
            <div class="flex flex-wrap gap-1.5">
              ${statusOpts.map(opt => `
                <label class="inline-flex items-center gap-1.5 min-h-[36px] px-2.5 py-1 rounded-full border ${curStatus === opt.val ? 'border-fern bg-emerald-50 text-fern-dark font-bold' : 'border-bordercol bg-white text-ink-muted'} text-[11px] font-mono cursor-pointer">
                  <input type="radio" name="filterModalStatus" value="${opt.val}" ${curStatus === opt.val ? 'checked' : ''} class="sr-only" onchange="this.closest('div').querySelectorAll('label').forEach(l => l.className='inline-flex items-center gap-1.5 min-h-[36px] px-2.5 py-1 rounded-full border border-bordercol bg-white text-ink-muted text-[11px] font-mono cursor-pointer'); this.parentElement.className='inline-flex items-center gap-1.5 min-h-[36px] px-2.5 py-1 rounded-full border border-fern bg-emerald-50 text-fern-dark font-bold text-[11px] font-mono cursor-pointer';" />
                  <span>${opt.label}</span>
                </label>
              `).join('')}
            </div>
          </div>
          <div class="text-[11px] font-mono text-muted mb-1.5">Specific Problem Flags:</div>
          <div class="grid grid-cols-2 gap-1.5">
            ${schemaProbs.filter(p => p && p.name).map(p => {
              const checked = Boolean(savedProbs[p.name]);
              const lbl = humanizeProblemName(p.name);
              return `
                <label class="flex items-center gap-2 min-h-[40px] px-2.5 py-1.5 rounded border border-bordercol bg-stone-50 text-xs text-ink cursor-pointer">
                  <input type="checkbox" class="filter-modal-prob-cb rounded border-stone-400 text-fern focus:ring-fern" data-prob-name="${p.name.replace(/"/g, '&quot;')}" ${checked ? 'checked' : ''} />
                  <span class="truncate">${lbl}</span>
                </label>
              `;
            }).join('')}
          </div>
        `;
        probContainer.innerHTML = html;
      }

      openModal('filterModal');
    }

    function closeFilterModal() {
      closeModal('filterModal');
    }

    function clearAdvancedFilters() {
      state.activeAdvancedFilters = { locations: {}, problems: {} };
      state.activeStatusFilter = 'all';
      state.selectedCabinet = '';
      state.selectedShelf = '';
      const cabSelect = document.getElementById('quickFilterCabinet');
      const shelfSelect = document.getElementById('quickFilterShelf');
      if (cabSelect) cabSelect.value = '';
      if (shelfSelect) shelfSelect.value = '';
      updateFilterActiveDot();
      closeFilterModal();
      fetchObjects();
    }

    function applyAdvancedFilters() {
      const nextLocs = {};
      state.selectedCabinet = '';
      state.selectedShelf = '';

      document.querySelectorAll('#filterModalLocations input[data-loc-field]').forEach(inp => {
        const fname = inp.getAttribute('data-loc-field');
        const val = inp.value.trim();
        if (fname && val) {
          nextLocs[fname] = val;
          if (fname.toLowerCase() === 'cabinet') state.selectedCabinet = val;
          if (fname.toLowerCase() === 'shelf') state.selectedShelf = val;
        }
      });

      const selectedStatusEl = document.querySelector('input[name="filterModalStatus"]:checked');
      state.activeStatusFilter = selectedStatusEl ? selectedStatusEl.value : 'all';

      const nextProbs = {};
      document.querySelectorAll('#filterModalProblems .filter-modal-prob-cb').forEach(cb => {
        const pname = cb.getAttribute('data-prob-name');
        if (pname && cb.checked) nextProbs[pname] = true;
      });

      state.activeAdvancedFilters = { locations: nextLocs, problems: nextProbs };
      updateFilterActiveDot();
      closeFilterModal();
      fetchObjects();
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

    // Plain-English Field Guide (mirrors the exact Mobile V2 specimen page layout)
    const FIELD_GUIDE_EXPLANATIONS = {
      'Genus': {
        example: 'e.g. Betula',
        desc: 'The first word of the plant’s scientific name. If the physical box has an older name or synonym, tap 📜 Old names to check it — or tap the checkbox next to Genus on Data to flag it for Arbor Desktop.'
      },
      'Species': {
        example: 'e.g. pendula',
        desc: 'The second word of the scientific name. Compare with the physical box label; if they disagree, check 📜 Old names or tap the checkbox next to Species on Data.'
      },
      'Author': {
        example: 'e.g. L. or Roth',
        desc: 'The scientist who originally named the plant — NOT the person who collected it! (The person who found it goes in Collector.)'
      },
      'Family': {
        example: 'e.g. Betulaceae',
        desc: 'The broader plant family name, usually ending in "-aceae" (older labels may use a classical name like Compositae — check 📜 Old names).'
      },
      'Collector': {
        example: 'e.g. N. Moe',
        desc: 'The person who physically collected the specimen in the field. If the label disagrees or is unreadable, tap the checkbox next to Collector on Data.'
      },
      'Collection Date': {
        example: 'e.g. 1954 or 15.07.1965',
        desc: 'When the specimen was collected (DAY.MONTH.YEAR using 00 for unknown parts, e.g. 00.06.1912, or just the year) as written on the label.'
      },
      'Collection place': {
        example: 'e.g. Oslo, Tøyen',
        desc: 'Where the specimen was collected (city, region, country, or botanical garden).'
      },
      'Box label': {
        example: 'Text on outside of box',
        desc: 'Exact wording or short note printed on the physical storage box label.'
      },
      'Comment': {
        example: 'Curatorial notes',
        desc: 'General notes or messages for the next curator reviewing this object. Tap Write / Edit Comment on Data to add one.'
      }
    };

    function openFieldGuideModal() {
      const body = document.getElementById('fieldGuideBody');
      if (!body) return;

      const sectionsHtml = [];

      // 1. Status Badges (aligned 1:1 with Arbor Desktop)
      sectionsHtml.push(`
        <section class="bg-surface border border-bordercol rounded-lg p-3 space-y-2">
          <div class="font-mono text-[10px] font-bold uppercase text-fern-dark">1. Status Badges (Phone &amp; Desktop)</div>
          <div class="space-y-1.5 text-[11px]">
            <div><span class="font-mono font-bold px-1.5 py-0.5 rounded bg-stone-100 text-stone-700 border border-stone-300">[UNREV]</span> — Nobody has checked this physical object yet.</div>
            <div><span class="font-mono font-bold px-1.5 py-0.5 rounded bg-emerald-50 text-fern-dark border border-fern/30">[REV]</span> — Checked physically and everything matches what is on file.</div>
            <div><span class="font-mono font-bold px-1.5 py-0.5 rounded bg-amber-50 text-amber-900 border border-amber-300">[REV+ERR]</span> — Checked physically, with an actionable data/label mismatch flagged. <strong>You don’t have to solve every problem today</strong> — leaving it flagged queues it safely for the desk computer.</div>
            <div><span class="font-mono font-bold px-1.5 py-0.5 rounded bg-teal-50 text-teal-900 border border-teal-300">[REV+NOTE]</span> / <span class="font-mono font-bold px-1.5 py-0.5 rounded bg-indigo-50 text-indigo-900 border border-indigo-200">[NOTE]</span> — <strong>Needs Specialist</strong> only (broken objects or storage, mixed specimens, or expert question). Kept out of the everyday trainee Problem Queue.</div>
            <div><span class="font-mono font-bold px-1.5 py-0.5 rounded bg-slate-100 text-slate-700 border border-slate-300">[CFCT]</span> — Older catalog books disagree with the current record. Swipe to the <strong>Problems</strong> tab to compare them.</div>
            <div><span class="font-mono font-bold px-1.5 py-0.5 rounded bg-amber-50 text-amber-900 border border-amber-300">↗ Loaned</span> — Currently loaned out (toggle on the <strong>Location</strong> tab; shown as <code>LOAN</code> on Desktop).</div>
          </div>
          <p class="text-[10px] text-ink-muted pt-1 border-t border-bordercol/60"><strong>Desktop-only unreviewed badges:</strong> On the desk computer, unreviewed flagged cards also show category badges: <code>[TAX]</code> (plant name), <code>[PROV]</code> (collector/date/place), <code>[BOX]</code> (box label), <code>[IMG]</code> (photo), <code>[ERR+HIS]</code> (error + older books), <code>[ERR]</code> (other error), plus small chips <code>UKN</code> (ICEDIG code) and <code>UNVAL</code> (draft note).</p>
        </section>
      `);

      // 2. The 3-Way Problem Rule & ICEDIG Codes
      sectionsHtml.push(`
        <section class="bg-surface border border-bordercol rounded-lg p-3 space-y-1.5">
          <div class="font-mono text-[10px] font-bold uppercase text-fern-dark">2. The 3-Way Problem Rule &amp; ICEDIG Codes</div>
          <p class="text-[11px] text-ink-muted"><strong>1. Confirmed blank or unreadable?</strong> Tap the field value on <strong>Data</strong> (or <strong>ICEDIG ▾</strong> on <strong>Problems</strong>) to pick <code>unknown:missing</code> (absent on label — never use if older books have a value!), <code>unknown:indecipherable</code> (illegible), <code>unknown:undigitized</code> (skipped), or <code>withheld</code> (protected).</p>
          <p class="text-[11px] text-ink-muted"><strong>2. Data or label mismatch?</strong> Tick the checkbox next to the field on <strong>Data</strong> (e.g. box says Africa, file says China) → <code>[REV+ERR]</code>. If older books disagree (e.g. England vs. Finland), swipe to <strong>Problems</strong> to compare and tap <strong>Apply</strong> or <strong>✓ Value is Correct</strong>.</p>
          <p class="text-[11px] text-ink-muted"><strong>3. Physical damage or specialist question?</strong> Tap <strong>⚑ Needs Specialist</strong> in the bottom bar and add a short <strong>Comment</strong> → calm <code>[REV+NOTE]</code>.</p>
        </section>
      `);

      // 3. Storage Location (matches Set Shelf & Location Tab)
      sectionsHtml.push(`
        <section class="bg-surface border border-bordercol rounded-lg p-3 space-y-1.5">
          <div class="font-mono text-[10px] font-bold uppercase text-fern-dark">3. Storage Location (Where the Box Lives)</div>
          <p class="text-[11px] text-ink-muted"><strong>Building, Floor, Cabinet, Shelf</strong> record where this object lives so we can find it again. Tap <strong>Set Shelf</strong> once at the top of the list, then tap <strong>📍 Save to Shelf</strong> on each box you pull (with a 5-second <strong>↩ Undo</strong>).</p>
          <p class="text-[11px] text-ink-muted"><strong>Stored as:</strong> What kind of container holds it (paper box, plastic box, petridish, etc.).</p>
        </section>
      `);

      // 4. Mirrored Specimen Form Fields (grouped just like the Mobile V2 Data tab)
      const groups = [
        { title: '4. Plant Name (Taxonomy)', fields: ['Genus', 'Species', 'Author', 'Family'] },
        { title: '5. Collection Details', fields: ['Collector', 'Collection Date', 'Collection place'] },
        { title: '6. Box Label & Notes', fields: ['Box label', 'Comment'] },
      ];

      groups.forEach(g => {
        const rows = g.fields.map(fname => {
          const info = FIELD_GUIDE_EXPLANATIONS[fname] || { example: '', desc: 'Metadata field stored in the Excel workbook.' };
          const highlight = (fname === 'Genus' || fname === 'Species' || fname === 'Author')
            ? 'border-fern/40 bg-emerald-50/40'
            : 'border-bordercol bg-stone-50/70';
          return `
            <div class="p-2 rounded border ${highlight} space-y-0.5">
              <div class="flex items-center justify-between gap-2">
                <span class="font-mono font-bold text-[11px] text-ink">${fname}</span>
                <span class="font-mono text-[10px] text-muted">${info.example}</span>
              </div>
              <p class="text-[11px] text-ink-muted leading-snug">${info.desc}</p>
            </div>
          `;
        }).join('');
        sectionsHtml.push(`
          <section class="bg-surface border border-bordercol rounded-lg p-3 space-y-2">
            <div class="font-mono text-[10px] font-bold uppercase text-fern-dark">${g.title}</div>
            <div class="space-y-1.5">${rows}</div>
          </section>
        `);
      });

      // 7. Tabs & Everyday Rules
      sectionsHtml.push(`
        <section class="bg-surface border border-bordercol rounded-lg p-3 space-y-1.5">
          <div class="font-mono text-[10px] font-bold uppercase text-fern-dark">7. The 3 Tabs &amp; Everyday Rules</div>
          <p class="text-[11px] text-ink-muted"><strong>Data:</strong> Glance at the registered info against the real object, tick any mismatched field, tap a value for ICEDIG codes, or flag <strong>Photo &amp; Media Issues</strong> at the bottom.</p>
          <p class="text-[11px] text-ink-muted"><strong>Location:</strong> Check or edit Building, Floor, Cabinet, Shelf, <strong>Stored as</strong>, and <strong>Loaned Out</strong>.</p>
          <p class="text-[11px] text-ink-muted"><strong>Problems:</strong> Works just like Desktop’s Problem Resolution — compare older books with the real label, tap <strong>Apply</strong>, type a value, pick <strong>ICEDIG ▾</strong>, or tap <strong>✓ Value is Correct</strong>.</p>
          <p class="text-[11px] text-ink-muted"><strong>Physical-Inspection Rule:</strong> Only tap <strong>✓ Mark Reviewed</strong> after checking the real box in front of you — and still tap it even if you flagged a problem so nobody has to check the same box twice.</p>
        </section>
      `);

      body.innerHTML = sectionsHtml.join('');
      const modal = document.getElementById('fieldGuideModal');
      if (modal) modal.classList.remove('hidden');
    }

    function closeFieldGuideModal() {
      const modal = document.getElementById('fieldGuideModal');
      if (modal) modal.classList.add('hidden');
    }

    // Compact tap popover for status badges on List cards & Loaned header pill
    const MOBILE_BADGE_TOOLTIPS = {
      'REV+ERR': { label: '[REV+ERR]', desc: 'Checked physically, with a data/label mismatch flagged for desk follow-up.' },
      'REV+NOTE': { label: '[REV+NOTE]', desc: 'Checked physically; only Needs Specialist is ticked (broken objects or storage, or expert question).' },
      'REV': { label: '[REV]', desc: 'Checked physically and matches what is on file, with no open flags.' },
      'FLAGGED': { label: 'Flagged ⚠', desc: 'Not reviewed yet, with an actionable field problem flagged. Open Problems tab to inspect.' },
      'NOTE': { label: '[NOTE]', desc: 'Not reviewed yet; only Needs Specialist is ticked.' },
      'UNREV': { label: '[UNREV]', desc: 'Nobody has checked this physical object yet.' },
      'CFCT': { label: '[CFCT]', desc: 'Older catalog books disagree with the current record. Swipe to Problems to compare.' },
      'LOAN': { label: '↗ Loaned', desc: 'Currently loaned out. Toggle Loaned Out on the Location tab.' }
    };
    let _badgeTipTimer = null;

    function hideBadgeTooltip() {
      const el = document.getElementById('arborBadgeTooltip');
      if (el) el.remove();
      if (_badgeTipTimer) {
        clearTimeout(_badgeTipTimer);
        _badgeTipTimer = null;
      }
    }

    function showBadgeTooltip(anchorEl, code) {
      hideBadgeTooltip();
      const info = MOBILE_BADGE_TOOLTIPS[code];
      if (!info || !anchorEl) return;

      const tip = document.createElement('div');
      tip.id = 'arborBadgeTooltip';
      tip.className = 'fixed z-[80] max-w-[260px] rounded-lg bg-ink text-white text-[11px] leading-snug px-3 py-2 shadow-lg border border-stone-700';
      tip.innerHTML = `
        <div class="flex items-center justify-between gap-2 mb-0.5">
          <span class="font-mono font-bold text-[10px] text-emerald-300">${info.label}</span>
          <button type="button" onclick="hideBadgeTooltip(); openFieldGuideModal();" class="font-mono text-[10px] text-amber-200 underline">Guide →</button>
        </div>
        <div class="text-stone-100">${info.desc}</div>
      `;
      tip.addEventListener('click', (e) => e.stopPropagation());
      document.body.appendChild(tip);

      const rect = anchorEl.getBoundingClientRect();
      const tipRect = tip.getBoundingClientRect();
      let left = rect.right - tipRect.width;
      if (left < 10) left = 10;
      if (left + tipRect.width > window.innerWidth - 10) left = window.innerWidth - tipRect.width - 10;
      let top = rect.bottom + 6;
      if (top + tipRect.height > window.innerHeight - 12) {
        top = Math.max(10, rect.top - tipRect.height - 6);
      }
      tip.style.left = `${Math.round(left)}px`;
      tip.style.top = `${Math.round(top)}px`;

      _badgeTipTimer = setTimeout(hideBadgeTooltip, 4500);
      setTimeout(() => {
        document.addEventListener('click', hideBadgeTooltip, { once: true });
      }, 0);
    }

    // -------------------------------------------------------------
    // PHONE COACH TUTORIAL ENGINE & ONE-TIME CONTEXTUAL TIPS
    // -------------------------------------------------------------
    const _ARBOR_TUT_MODE_RAW = '{{ phone_tutorial_mode }}';
    const ARBOR_PHONE_TUTORIAL_MODE = ['ask', 'trainee', 'helper', 'off'].includes(_ARBOR_TUT_MODE_RAW) ? _ARBOR_TUT_MODE_RAW : 'ask';
    const ARBOR_SHOW_WALKTHROUGH = (ARBOR_PHONE_TUTORIAL_MODE !== 'off');
    const COACH_STORAGE_KEY = 'arbor_phone_tutorial';

    function _normCoachCoord(v) {
      const s = String(v ?? '').trim();
      if (!s || s === '—') return '';
      if (/^\\d+$/.test(s)) return s.replace(/^0+/, '') || '0';
      return s.toLowerCase();
    }

    function _isCoachLocationSaved() {
      if (!state.currentRecord) return false;
      const obs = state.currentRecord.observation || {};
      const curCab = _normCoachCoord(obs.Cabinet);
      const curShelf = _normCoachCoord(obs.Shelf);
      if (!curCab && !curShelf) return false;
      const armed = state.armedLocation;
      if (armed && (armed.cabinet || armed.shelf)) {
        const cabOk = !armed.cabinet || curCab === _normCoachCoord(armed.cabinet);
        const shelfOk = !armed.shelf || curShelf === _normCoachCoord(armed.shelf);
        return cabOk && shelfOk;
      }
      return true;
    }

    function _twoStageSaveReviewTarget() {
      if (!_isCoachLocationSaved()) {
        const stampBtn = document.getElementById('btnStampArmedLocation');
        if (stampBtn && !stampBtn.classList.contains('hidden')) return stampBtn;
      }
      return document.getElementById('btnDetailMarkReviewed');
    }

    let _coachTourCycleIdx = 0;
    const _COACH_TOUR_TABS = ['#tabBtnDetails', '#tabBtnLocation', '#tabBtnHistory'];

    const PHONE_TUTORIALS = {
      trainee: [
        {
          id: 't_shelf',
          badge: 'TRAINEE · STEP 1 OF 5',
          title: 'Set your shelf',
          body: "In Part 1 you practiced checking specimen data at your desk — in the collection, you also record each object's physical storage location (Building, Floor, Cabinet, and Shelf). Registering where every specimen lives is essential so curators and researchers can find it again later without searching through dozens of cabinets. Tap Set Shelf for the cabinet and shelf you're standing at so Arbor can save that location for every object here in one tap.",
          waitingText: 'Waiting for you to set a shelf…',
          target: '#btnStationSheetTrigger',
          check: () => Boolean(state.armedLocation && (state.armedLocation.cabinet || state.armedLocation.shelf))
        },
        {
          id: 't_search',
          badge: 'TRAINEE · STEP 2 OF 5',
          title: 'Find the object in your hand',
          body: "Pick up an object from the shelf, type its number into the search box, and tap it to open its record.",
          waitingText: 'Waiting for you to open an object…',
          target: '#searchBox',
          check: () => Boolean(state.currentRecord)
        },
        {
          id: 't_tour',
          badge: 'TRAINEE · STEP 3 OF 5',
          title: 'How the 3 tabs fit your check',
          body: 'Glance at Data against the real object in your hand: if something is wildly off (e.g. the label says Africa but Data says China), tick that field\\'s box to flag it. If Problems shows a number (e.g. one source says England and another says Finland), open Problems — it works just like Problem Resolution on Desktop — check the object and tap Apply to fix it on the spot. Location holds the shelf coordinates.',
          target: () => document.querySelector(_COACH_TOUR_TABS[_coachTourCycleIdx % _COACH_TOUR_TABS.length]),
          check: null
        },
        {
          id: 't_save_review',
          badge: 'TRAINEE · STEP 4 OF 5',
          title: 'Save the location, then Mark Reviewed',
          body: 'Tap 📍 Save to Shelf to record where this object lives, then tap ✓ Mark Reviewed to confirm you physically checked it. Do both for every object you inspect.',
          waitingText: 'Waiting for Save to Shelf & ✓ Mark Reviewed…',
          target: _twoStageSaveReviewTarget,
          check: () => Boolean(_isCoachLocationSaved() && state.isReviewed)
        },
        {
          id: 't_ready',
          badge: 'TRAINEE · STEP 5 OF 5',
          title: "You're ready!",
          body: 'Your hallway routine: Set Shelf → search → glance at Data (fix or flag mismatches in Problems) → Save to Shelf → Mark Reviewed. Pick up the next object! The first time you open Problems, ICEDIG, or Needs Specialist, a short one-time tip will guide you — then stay out of your way.',
          target: null,
          check: null,
          isFinal: true
        }
      ],
      helper: [
        {
          id: 'h_shelf',
          badge: 'HELPER · STEP 1 OF 4',
          title: 'Set your shelf',
          body: "A key part of working in the collection is recording each object's physical storage location (Building, Floor, Cabinet, and Shelf) so staff and researchers can find it again later without searching through dozens of cabinets. Tap Set Shelf for the cabinet and shelf you're standing at so you can save each object's location in one tap — and update it whenever you move to a new shelf.",
          waitingText: 'Waiting for you to set a shelf…',
          target: '#btnStationSheetTrigger',
          check: () => Boolean(state.armedLocation && (state.armedLocation.cabinet || state.armedLocation.shelf))
        },
        {
          id: 'h_search',
          badge: 'HELPER · STEP 2 OF 4',
          title: 'Find the object in your hand',
          body: "Pick up an object from the shelf, type its number in the search box, and tap it to open its card.",
          waitingText: 'Waiting for you to open an object…',
          target: '#searchBox',
          check: () => Boolean(state.currentRecord)
        },
        {
          id: 'h_check_save_review',
          badge: 'HELPER · STEP 3 OF 4',
          title: 'Quick check, save, mark reviewed',
          body: 'Glance at Data against the object in your hand. Spot a clear mismatch (e.g. label says Africa, file says China)? Tick that field\\'s box, or tap ⚑ Needs Specialist for physical damage. If Problems shows a number (conflicting sources like England vs. Finland), check the object and tap Apply on the right one — not sure? Leave it. Then tap 📍 Save to Shelf and ✓ Mark Reviewed.',
          waitingText: 'Waiting for Save to Shelf & ✓ Mark Reviewed…',
          target: _twoStageSaveReviewTarget,
          check: () => Boolean(_isCoachLocationSaved() && state.isReviewed)
        },
        {
          id: 'h_ready',
          badge: 'HELPER · STEP 4 OF 4',
          title: "You're ready!",
          body: 'Your routine: Set Shelf → search → quick check on Data & Problems → Save to Shelf → Mark Reviewed. If you are ever unsure about a label, just leave it flagged — the curator will review it at the desk later.',
          target: null,
          check: null,
          isFinal: true
        }
      ]
    };

    const COACH_TIPS = {
      tip_flagged: {
        label: 'Flagged objects on Data',
        title: 'This object has a flagged problem',
        versions: ['trainee', 'helper'],
        bodyTrainee: "Red-highlighted fields on Data mean something is missing or uncertain. Compare them with the real object in your hand — you can open the Problems tab to compare older books and tap Apply if the object makes the answer clear. Can't solve it in the hallway? Leave it checked and still tap ✓ Mark Reviewed so it's saved for your desk ([REV+ERR]).",
        bodyHelper: 'Red-highlighted fields on Data mean something needs checking. Open the Problems tab to compare older records against the object in your hand — tap Apply if it is clearly right, or leave it checked for the main worker.'
      },
      tip_history: {
        label: 'Problems tab (Problem Resolution)',
        title: 'This is the Problems tab',
        versions: ['trainee', 'helper'],
        explicitTool: true,
        bodyTrainee: "Problems works just like Problem Resolution on Desktop. If older books disagree (e.g. England vs. Finland), check the real object in your hand and tap Apply on the matching value — or tap ✓ Value is Correct if it was a false alarm, or ICEDIG ▾ if confirmed blank or unreadable.",
        bodyHelper: 'Problems lets you compare the current record with older books. Check the real label in your hand: if one clearly matches, tap Apply to fix it right here. Not sure? Leave it as is for the desk.'
      },
      tip_icedig: {
        label: 'ICEDIG codes (blank/unreadable)',
        title: 'Using ICEDIG codes',
        versions: ['trainee'],
        explicitTool: true,
        bodyTrainee: "ICEDIG codes mark a field as confirmed blank or unreadable — just like #198's Collector in Part 1. Pick unknown:missing if nothing is written on the label, or unknown:indecipherable if the ink can't be read. If older books still disagree, leave the field flagged for the desk instead."
      },
      tip_specialist: {
        label: 'Needs Specialist ([REV+NOTE])',
        title: 'Flagged as Needs Specialist',
        versions: ['trainee', 'helper'],
        explicitTool: true,
        bodyTrainee: 'Needs Specialist is for broken objects or storage, mixed specimens, or mysteries desk tools cannot fix. Add a short Comment (or tap a quick tag like + Broken Object / Storage) so a specialist knows what to check — it marks the object [REV+NOTE] and keeps it out of your regular desk queue.',
        bodyHelper: 'Needs Specialist is for broken objects or storage, or mixed specimens. Add a short Comment (or tap a quick tag like + Broken Object / Storage) so a specialist knows what to check.'
      },
      tip_rev_err: {
        label: 'Saved for desk follow-up ([REV+ERR])',
        title: 'Saved for your desk ([REV+ERR])',
        versions: ['trainee', 'helper'],
        bodyTrainee: "Nice work — marking this Reviewed confirms you physically checked the object and saved its shelf, while keeping the open flag safe. When your shift is over, press Stop on the computer — all your phone edits will be in Arbor ready to save, and you can filter for these anytime with Ctrl+G.",
        bodyHelper: 'Nice work — marking this Reviewed confirms you checked the object and saved its shelf, while leaving the open flag for the main worker at the desk.'
      }
    };

    const coachState = {
      phase: 'off', // 'off' | 'chooser' | 'active' | 'tip' | 'finished'
      tipId: null,
      pendingTip: null,
      lastTipDismissedAt: 0,
      highlightedEl: null,
      scrolledKey: null,
      timers: { poll: null, tour: null, advance: null }
    };

    function setCoachPhase(nextPhase, tipId = null) {
      if (nextPhase !== 'active') {
        _stopCoachTimers();
        _clearCoachHighlight();
      }
      coachState.phase = nextPhase;
      coachState.tipId = (nextPhase === 'tip') ? tipId : null;
    }

    function _loadCoachState() {
      const def = { mode: null, stepIdx: 0, finished: false, dismissed: false, tipsSeen: {}, tipsDisabled: false };
      try {
        const raw = localStorage.getItem(COACH_STORAGE_KEY);
        if (!raw) return def;
        const parsed = JSON.parse(raw);
        if (parsed && typeof parsed === 'object') {
          return {
            mode: parsed.mode || null,
            stepIdx: Number.isInteger(parsed.stepIdx) ? parsed.stepIdx : 0,
            finished: Boolean(parsed.finished),
            dismissed: Boolean(parsed.dismissed),
            tipsSeen: (parsed.tipsSeen && typeof parsed.tipsSeen === 'object') ? parsed.tipsSeen : {},
            tipsDisabled: Boolean(parsed.tipsDisabled)
          };
        }
      } catch (e) {}
      return def;
    }

    function _saveCoachState(st) {
      try {
        localStorage.setItem(COACH_STORAGE_KEY, JSON.stringify(st));
      } catch (e) {}
    }

    function _clearCoachHighlight() {
      if (coachState.highlightedEl) {
        try { coachState.highlightedEl.classList.remove('coach-target'); } catch (e) {}
        coachState.highlightedEl = null;
      }
    }

    function _stopCoachTimers() {
      if (coachState.timers.poll) { clearInterval(coachState.timers.poll); coachState.timers.poll = null; }
      if (coachState.timers.tour) { clearInterval(coachState.timers.tour); coachState.timers.tour = null; }
      if (coachState.timers.advance) { clearTimeout(coachState.timers.advance); coachState.timers.advance = null; }
    }

    function _positionCoachCard() {
      const card = document.getElementById('coachCard');
      if (!card) return;
      const detailView = document.getElementById('detailView');
      const onDetail = Boolean(detailView && !detailView.classList.contains('hidden'));
      card.classList.toggle('coach-on-list', !onDetail);
      if (onDetail) {
        card.classList.remove('bottom-4');
        card.classList.add('bottom-[92px]');
      } else {
        card.classList.remove('bottom-[92px]');
        card.classList.add('bottom-4');
      }
    }

    function _isAnyBlockingModalOpen() {
      const modals = document.querySelectorAll('.fixed.inset-0.z-50:not(.hidden)');
      return modals.length > 0;
    }

    function _renderCoachCard() {
      const card = document.getElementById('coachCard');
      if (!card) return;
      const st = _loadCoachState();
      const steps = PHONE_TUTORIALS[st.mode];
      if (coachState.phase !== 'active' || !steps || st.stepIdx < 0 || st.stepIdx >= steps.length) {
        card.classList.add('hidden');
        setCoachPhase('off');
        return;
      }

      const step = steps[st.stepIdx];
      coachState.tipId = null;
      card.classList.remove('z-[60]');
      card.classList.add('z-40');
      _positionCoachCard();

      const badgeEl = document.getElementById('coachBadge');
      const titleEl = document.getElementById('coachTitle');
      const bodyEl = document.getElementById('coachBody');
      const statusEl = document.getElementById('coachStatus');
      const chooserRow = document.getElementById('coachChooserActions');
      const stepRow = document.getElementById('coachStepActions');
      const tipRow = document.getElementById('coachTipActions');
      const backBtn = document.getElementById('coachBackBtn');
      const skipBtn = document.getElementById('coachSkipBtn');
      const nextBtn = document.getElementById('coachNextBtn');

      if (badgeEl) badgeEl.textContent = step.badge;
      if (titleEl) titleEl.textContent = step.title;
      if (bodyEl) bodyEl.textContent = step.body;
      if (chooserRow) chooserRow.classList.add('hidden');
      if (tipRow) tipRow.classList.add('hidden');
      if (stepRow) stepRow.classList.remove('hidden');

      if (backBtn) backBtn.classList.toggle('hidden', st.stepIdx === 0);
      if (skipBtn) skipBtn.classList.toggle('hidden', Boolean(step.isFinal));

      const hasCheck = (typeof step.check === 'function');
      if (statusEl) {
        if (hasCheck && step.waitingText) {
          statusEl.textContent = step.waitingText;
          statusEl.classList.remove('hidden');
        } else {
          statusEl.classList.add('hidden');
        }
      }
      if (nextBtn) {
        if (step.isFinal) {
          nextBtn.textContent = 'Finish ✓';
          nextBtn.classList.remove('hidden');
        } else if (!hasCheck) {
          nextBtn.textContent = 'Next →';
          nextBtn.classList.remove('hidden');
        } else {
          nextBtn.classList.add('hidden');
        }
      }

      card.classList.remove('hidden');

      if (coachState.timers.tour) { clearInterval(coachState.timers.tour); coachState.timers.tour = null; }
      if (step.id === 't_tour') {
        _coachTourCycleIdx = 0;
        coachState.timers.tour = setInterval(() => {
          _coachTourCycleIdx = (_coachTourCycleIdx + 1) % _COACH_TOUR_TABS.length;
          coachTick();
        }, 1500);
      }

      if (typeof step.onEnter === 'function') {
        try { step.onEnter(); } catch (e) {}
      }

      coachTick();
    }

    function coachTick() {
      if (coachState.phase !== 'active') return;
      _positionCoachCard();
      const st = _loadCoachState();
      const steps = PHONE_TUTORIALS[st.mode];
      if (!steps || st.stepIdx < 0 || st.stepIdx >= steps.length) return;
      const step = steps[st.stepIdx];

      // Resolve target fresh every tick (elements re-render dynamically)
      let targetEl = null;
      try {
        if (typeof step.target === 'function') {
          targetEl = step.target();
        } else if (typeof step.target === 'string') {
          targetEl = document.querySelector(step.target);
        }
      } catch (e) {}

      if (targetEl !== coachState.highlightedEl) {
        _clearCoachHighlight();
        if (targetEl) {
          coachState.highlightedEl = targetEl;
          targetEl.classList.add('coach-target');
          const scrollKey = `${step.id}:${targetEl.id || ''}`;
          if (coachState.scrolledKey !== scrollKey && step.id !== 't_tour') {
            coachState.scrolledKey = scrollKey;
            try { targetEl.scrollIntoView({ behavior: 'smooth', block: 'center' }); } catch (e) {}
          }
        }
      }

      if (typeof step.check === 'function' && !coachState.timers.advance) {
        let passed = false;
        try { passed = Boolean(step.check()); } catch (e) {}
        if (passed) {
          const statusEl = document.getElementById('coachStatus');
          const nextBtn = document.getElementById('coachNextBtn');
          if (statusEl) {
            statusEl.textContent = '✓ Done';
            statusEl.classList.remove('hidden');
          }
          if (nextBtn) {
            nextBtn.textContent = 'Next →';
            nextBtn.classList.remove('hidden');
          }
          coachState.timers.advance = setTimeout(() => {
            coachState.timers.advance = null;
            coachNextStep();
          }, 600);
        }
      }
    }

    function startPhoneTutorial(mode) {
      if (!PHONE_TUTORIALS[mode]) return;
      _stopCoachTimers();
      _clearCoachHighlight();
      coachState.scrolledKey = null;
      const st = _loadCoachState();
      st.mode = mode;
      st.stepIdx = 0;
      st.finished = false;
      st.dismissed = false;
      _saveCoachState(st);
      setCoachPhase('active');
      _renderCoachCard();
      coachState.timers.poll = setInterval(coachTick, 500);
    }

    function coachNextStep() {
      if (coachState.timers.advance) { clearTimeout(coachState.timers.advance); coachState.timers.advance = null; }
      const st = _loadCoachState();
      const steps = PHONE_TUTORIALS[st.mode];
      if (!steps) return;
      if (st.stepIdx < steps.length - 1) {
        st.stepIdx += 1;
        _saveCoachState(st);
        coachState.scrolledKey = null;
        _renderCoachCard();
      } else {
        st.finished = true;
        _saveCoachState(st);
        setCoachPhase('finished');
        const card = document.getElementById('coachCard');
        if (card) card.classList.add('hidden');
      }
    }

    function coachPrevStep() {
      if (coachState.timers.advance) { clearTimeout(coachState.timers.advance); coachState.timers.advance = null; }
      const st = _loadCoachState();
      if (st.stepIdx > 0) {
        st.stepIdx -= 1;
        _saveCoachState(st);
        coachState.scrolledKey = null;
        _renderCoachCard();
      }
    }

    function exitPhoneTutorial() {
      const st = _loadCoachState();
      if (coachState.phase === 'active' || coachState.phase === 'chooser') {
        st.dismissed = true;
        _saveCoachState(st);
      }
      setCoachPhase('off');
      const card = document.getElementById('coachCard');
      if (card) {
        card.classList.add('hidden');
        card.classList.remove('z-[60]');
        card.classList.add('z-40');
      }
    }

    function dismissPhoneTutorialChooser() {
      const st = _loadCoachState();
      st.dismissed = true;
      _saveCoachState(st);
      exitPhoneTutorial();
    }

    function showPhoneTutorialChooser() {
      const card = document.getElementById('coachCard');
      if (!card) return;
      setCoachPhase('chooser');
      _positionCoachCard();
      const badgeEl = document.getElementById('coachBadge');
      const titleEl = document.getElementById('coachTitle');
      const bodyEl = document.getElementById('coachBody');
      const statusEl = document.getElementById('coachStatus');
      const chooserRow = document.getElementById('coachChooserActions');
      const stepRow = document.getElementById('coachStepActions');
      const tipRow = document.getElementById('coachTipActions');
      if (badgeEl) badgeEl.textContent = 'PHONE TUTORIAL';
      if (titleEl) titleEl.textContent = 'Welcome to Arbor on your phone';
      if (bodyEl) bodyEl.textContent = 'Pick the quick hands-on guide that fits you best — you can exit anytime.';
      if (statusEl) statusEl.classList.add('hidden');
      if (stepRow) stepRow.classList.add('hidden');
      if (tipRow) tipRow.classList.add('hidden');
      if (chooserRow) chooserRow.classList.remove('hidden');
      card.classList.remove('hidden');
    }

    function _flushPendingCoachTip() {
      if (!coachState.pendingTip) return;
      const detailView = document.getElementById('detailView');
      const onDetail = Boolean(detailView && !detailView.classList.contains('hidden'));
      const pending = coachState.pendingTip;
      coachState.pendingTip = null;
      if (onDetail) {
        maybeShowTip(pending.tipId, pending.options);
      }
    }

    function maybeShowTip(tipId, options = null) {
      const tip = COACH_TIPS[tipId];
      if (!tip) return;
      if (coachState.phase === 'active' || coachState.phase === 'chooser') return;
      // Anti-overwhelm: never stack a new tip on top of one the user is already reading
      if (coachState.phase === 'tip' && !tip.explicitTool) return;
      const allowOverModal = Boolean(options && options.allowOverModal);
      if (!allowOverModal && _isAnyBlockingModalOpen()) return;

      const st = _loadCoachState();
      if (st.tipsDisabled) return;
      if (st.tipsSeen && st.tipsSeen[tipId]) return;

      // Anti-overwhelm: pace passive tips so they don't fire back-to-back within 10s
      if (!tip.explicitTool && coachState.lastTipDismissedAt && (Date.now() - coachState.lastTipDismissedAt) < 10000) {
        return;
      }

      if (_toastHasActiveAction) {
        coachState.pendingTip = { tipId, options };
        return;
      }

      const version = (st.mode === 'helper' || ARBOR_PHONE_TUTORIAL_MODE === 'helper') ? 'helper' : 'trainee';
      if (!tip.versions.includes(version)) return;

      const bodyText = (version === 'helper' && tip.bodyHelper) ? tip.bodyHelper : tip.bodyTrainee;
      if (!bodyText) return;

      st.tipsSeen = st.tipsSeen || {};
      st.tipsSeen[tipId] = true;
      _saveCoachState(st);

      const card = document.getElementById('coachCard');
      if (!card) return;
      setCoachPhase('tip', tipId);
      _positionCoachCard();
      if (allowOverModal) {
        card.classList.remove('z-40');
        card.classList.add('z-[60]');
      } else {
        card.classList.remove('z-[60]');
        card.classList.add('z-40');
      }

      const badgeEl = document.getElementById('coachBadge');
      const titleEl = document.getElementById('coachTitle');
      const bodyEl = document.getElementById('coachBody');
      const statusEl = document.getElementById('coachStatus');
      const chooserRow = document.getElementById('coachChooserActions');
      const stepRow = document.getElementById('coachStepActions');
      const tipRow = document.getElementById('coachTipActions');
      if (badgeEl) badgeEl.textContent = 'QUICK TIP · SHOWN ONCE';
      if (titleEl) titleEl.textContent = tip.title;
      if (bodyEl) bodyEl.textContent = bodyText;
      if (statusEl) statusEl.classList.add('hidden');
      if (chooserRow) chooserRow.classList.add('hidden');
      if (stepRow) stepRow.classList.add('hidden');
      if (tipRow) tipRow.classList.remove('hidden');
      card.classList.remove('hidden');
    }

    function dismissCoachTip() {
      if (coachState.phase === 'tip') {
        coachState.lastTipDismissedAt = Date.now();
      }
      setCoachPhase('off');
      const card = document.getElementById('coachCard');
      if (card) {
        card.classList.add('hidden');
        card.classList.remove('z-[60]');
        card.classList.add('z-40');
      }
    }

    function disableCoachTipsFromCard() {
      const st = _loadCoachState();
      st.tipsDisabled = true;
      _saveCoachState(st);
      dismissCoachTip();
      showToast('One-time tips turned off (re-enable in Settings)');
    }

    function toggleCoachTipsEnabled(enabled) {
      const st = _loadCoachState();
      st.tipsDisabled = !Boolean(enabled);
      _saveCoachState(st);
      renderSettingsTutorialPanel();
    }

    function resetCoachTips() {
      const st = _loadCoachState();
      st.tipsSeen = {};
      st.tipsDisabled = false;
      _saveCoachState(st);
      renderSettingsTutorialPanel();
      showToast('✓ One-time tips reset');
    }

    function renderSettingsTutorialPanel() {
      const st = _loadCoachState();
      const cb = document.getElementById('settingEnableCoachTips');
      if (cb) cb.checked = !st.tipsDisabled;
      const listEl = document.getElementById('settingsTipsList');
      if (!listEl) return;
      const seen = st.tipsSeen || {};
      listEl.innerHTML = Object.entries(COACH_TIPS).map(([id, t]) => {
        const isSeen = Boolean(seen[id]);
        return `<div class="flex items-center justify-between py-0.5"><span class="text-ink">${escapeHtml(t.label)}</span><span class="font-mono text-xs font-bold ${isSeen ? 'text-fern' : 'text-muted'}">${isSeen ? '✓' : '○'}</span></div>`;
      }).join('');
    }

    function initPhoneTutorialOnLoad() {
      const st = _loadCoachState();
      const forceParam = (typeof window !== 'undefined' && window.location && new URLSearchParams(window.location.search).get('tutorial') === '1');
      if (forceParam) {
        showPhoneTutorialChooser();
        return;
      }
      // Resume an in-progress tutorial across phone sleep / page reload
      if (st.mode && PHONE_TUTORIALS[st.mode] && !st.finished && !st.dismissed) {
        _coachActive = true;
        _renderCoachCard();
        _coachInterval = setInterval(coachTick, 500);
        return;
      }
      if (st.finished || st.dismissed) return;
      if (ARBOR_PHONE_TUTORIAL_MODE === 'off') return;
      if (ARBOR_PHONE_TUTORIAL_MODE === 'trainee' || ARBOR_PHONE_TUTORIAL_MODE === 'helper') {
        startPhoneTutorial(ARBOR_PHONE_TUTORIAL_MODE);
      } else {
        showPhoneTutorialChooser();
      }
    }

    // Register Service Worker for offline vault resilience
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('/service-worker.js').catch(err => console.warn('ServiceWorker registration error:', err));
    }

    // Start App
    if (document.readyState === 'loading') {
      window.addEventListener('DOMContentLoaded', () => { init(); initPhoneTutorialOnLoad(); });
    } else {
      init();
      initPhoneTutorialOnLoad();
    }
  </script>
</body>
</html>

"""

"""
backend/mobile_archived_flag_issue.py

Archived legacy "⚑ Flag Issue" modal and JS handlers removed from
`backend/mobile_template_v2.py` (`INDEX_TEMPLATE_V2`) per MOBILE_COMPANION_GUIDE §4.

Why removed:
- `submitDiscrepancy()` wrote hard-coded `Physical_Damage_Problem`, `Location_Problem`,
  `Taxon_Problem`, and `General_Problem` flags that do not exist in `config.py`
  (causing `/api/update` to append unexpected columns to the Excel workbook).
- It overwrote `Notes` instead of using `Comment` and never set `Other_problem`,
  so damaged specimens ended up as `[REV+ERR]` in the desk queue instead of `[REV+NOTE]`.

Replaced by:
- Bottom-bar `⚑ Needs Specialist` (`#btnDetailNeedsSpecialist`), synced to `Other_problem`
  and the Comment + quick-tag pills section on the Details tab.
"""

ARCHIVED_FLAG_ISSUE_BUTTON_HTML = r"""
          <button
            type="button"
            onclick="openAddDiscrepancyModal()"
            class="min-h-[42px] px-3.5 py-2.5 bg-amber-50 hover:bg-amber-100 text-amber-900 border border-amber-300 rounded font-sans font-semibold text-xs flex items-center justify-center gap-1.5 tap-active"
            title="Flag Physical Issue"
          >
            <span>⚑</span>
            <span>Flag Issue</span>
          </button>
"""

ARCHIVED_FLAG_ISSUE_MODAL_HTML = r"""
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
"""

ARCHIVED_FLAG_ISSUE_JS = r"""
    function openAddDiscrepancyModal(defaultField = '') {
      const select = document.getElementById('discrepancyFieldSelect');
      if (select) {
        const options = [
          { val: 'Physical_Damage_Problem', label: 'Physical Specimen Damaged' },
          { val: 'Location_Problem', label: 'Physical Specimen Misplaced' },
          { val: 'Taxon_Problem', label: 'Taxon / Identification Issue' },
          { val: 'General_Problem', label: 'General Specimen Issue' }
        ];
        if (state.activeSchema && state.activeSchema.ui_sections && state.activeSchema.ui_sections.problems) {
          state.activeSchema.ui_sections.problems.forEach(p => {
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
"""

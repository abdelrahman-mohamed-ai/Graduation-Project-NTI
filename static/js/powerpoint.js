'use strict';
(() => {
  const root = document.querySelector('#powerpoint-app');
  const dataEl = document.querySelector('#presentation-data');
  if (!root || !dataEl) return;

  const payload = JSON.parse(dataEl.textContent);
  const slidesEl = document.querySelector('#pp-slides');
  const stage = document.querySelector('#pp-stage');
  const frame = document.querySelector('#pp-slide-frame');
  const charts = [];
  const state = { index: 0, language: document.documentElement.lang === 'ar' ? 'ar' : 'en', pointerX: null };
  const metrics = payload.metrics || {};
  const dataset = payload.dataset || {};
  const esc = value => window.EG?.esc ? EG.esc(value) : String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const ui = () => payload.ui[state.language];
  const slides = () => payload.slides[state.language];
  const pct = value => `${(Number(value) * 100).toFixed(2)}%`;
  const num = (value, digits = 3) => Number(value).toFixed(digits);
  const count = value => Number(value || 0).toLocaleString(state.language === 'ar' ? 'ar-EG' : 'en-US');
  const metricCard = (label, value, note = '', cls = '') => `<article class="pp-metric ${cls}"><span>${esc(label)}</span><strong>${esc(value)}</strong>${note ? `<small>${esc(note)}</small>` : ''}</article>`;
  const bullets = values => `<ul class="pp-bullets">${(values || []).map(value => `<li>${esc(value)}</li>`).join('')}</ul>`;
  const why = slide => slide.why ? `<aside class="pp-why"><b>${esc(ui().why)}</b><span>${esc(slide.why)}</span></aside>` : '';
  const flow = (values, cls = '') => `<div class="pp-academic-flow ${cls}">${(values || []).map((value, i) => `<div class="pp-flow-node"><small>${String(i + 1).padStart(2, '0')}</small><b>${esc(value)}</b></div>`).join('')}</div>`;
  const bars = (items, max) => `<div class="pp-bars">${items.map(item => `<div class="pp-bar-row"><span>${esc(item.label)}</span><div class="pp-bar-track"><i style="width:${max ? Math.max(2, Number(item.value) / max * 100) : 2}%"></i></div><b>${esc(item.display ?? count(item.value))}</b></div>`).join('')}</div>`;
  const common = (slide, index) => `<div class="pp-slide-head"><span class="pp-slide-number">${String(index + 1).padStart(2, '0')} / ${slides().length}</span><span class="pp-section-label">${esc(slide.eyebrow || (state.language === 'ar' ? 'عرض أكاديمي' : 'Academic presentation'))}</span></div><h2>${esc(slide.title)}</h2>${slide.lead ? `<p class="pp-lead">${esc(slide.lead)}</p>` : ''}`;

  function slideMarkup(slide, index) {
    const m = metrics;
    const t = ui();
    const wrap = content => `<article class="pp-slide ${slide.type === 'cover' ? 'pp-cover' : ''}" data-index="${index}">${common(slide, index)}${content}</article>`;
    if (slide.type === 'cover') return `<article class="pp-slide pp-cover" data-index="${index}"><div class="pp-cover-rule">${esc(slide.eyebrow)}</div><h2>${esc(slide.title)}</h2><p class="pp-cover-subtitle">${esc(slide.subtitle)}</p><div class="pp-cover-meta">${slide.meta.map(item => `<span>${esc(item)}</span>`).join('')}</div><p class="pp-cover-body">${esc(slide.body)}</p><div class="pp-cover-footer"><span>EduGuard AI</span><span>${String(index + 1).padStart(2, '0')} / ${slides().length}</span></div></article>`;
    if (slide.type === 'idea') return wrap(`<div class="pp-two-column"><div>${bullets(slide.points)}</div><div>${flow(slide.diagram, 'pp-flow-three')}</div></div>`);
    if (slide.type === 'problem') return wrap(`${bullets(slide.points)}<div class="pp-question"><span>Research / project question</span><strong>${esc(slide.question)}</strong></div>`);
    if (slide.type === 'objectives') return wrap(`<div class="pp-objectives">${slide.objectives.map((item, i) => `<div><b>${i + 1}</b><span>${esc(item)}</span></div>`).join('')}</div>`);
    if (slide.type === 'scope') return wrap(`<div class="pp-two-column pp-scope"><section class="pp-panel positive"><h3>${state.language === 'ar' ? 'ما يفعله النظام' : 'What the system does'}</h3>${bullets(slide.does)}</section><section class="pp-panel negative"><h3>${state.language === 'ar' ? 'ما لا يفعله النظام' : 'What the system does not do'}</h3>${bullets(slide.does_not)}</section></div><div class="pp-scope-callout">${esc(slide.callout)}</div>`);
    if (slide.type === 'dataset') { const outcomes = Object.entries(dataset.outcomes || {}); return wrap(`<div class="pp-metrics pp-metrics-four">${metricCard(t.dataset_students, count(dataset.total_students))}${metricCard(t.input_features, count(dataset.input_features))}${metricCard(t.outcomes, count(outcomes.length))}${metricCard(state.language === 'ar' ? 'مراحل الإنذار المبكر' : 'Early-warning stages', '2')}</div><div class="pp-outcomes">${outcomes.map(([label, value]) => `<div><b>${esc(label)}</b><strong>${count(value)}</strong><span>${esc(t.students)}</span></div>`).join('')}</div><div class="pp-source"><span>${esc(state.language === 'ar' ? 'المصدر' : 'Source')}</span><b>${esc(slide.source)}</b></div><p class="pp-note">${esc(slide.why)}</p>`); }
    if (slide.type === 'target') return wrap(`<div class="pp-target-grid"><div class="pp-target-card"><span>${esc(slide.resolved[0])}</span><strong>${esc(slide.resolved[1])}</strong></div><div class="pp-target-card"><span>${esc(slide.resolved[2])}</span><strong>${esc(slide.resolved[3])}</strong></div><div class="pp-target-card unresolved"><span>${state.language === 'ar' ? 'لا يدخل التدريب' : 'Not used for training'}</span><strong>${esc(slide.unresolved)}</strong></div></div><p class="pp-note">${esc(slide.note)}</p>${why(slide)}`);
    if (slide.type === 'leakage') return wrap(`<div class="pp-two-column"><section class="pp-panel positive"><h3>${state.language === 'ar' ? 'مسموح عند نقطة القرار' : 'Available at the decision point'}</h3>${bullets(slide.allowed)}</section><section class="pp-panel negative"><h3>${state.language === 'ar' ? 'مستبعد لتجنب التسرب' : 'Excluded to prevent leakage'}</h3>${bullets(slide.excluded)}</section></div><p class="pp-note">${esc(slide.note)}</p>${why(slide)}`);
    if (slide.type === 'preprocessing') return wrap(`${flow(slide.pipeline, 'pp-flow-pipeline')}${bullets(slide.points)}${why(slide)}`);
    if (slide.type === 'outliers') return wrap(`<div class="pp-two-column"><div>${bullets(slide.points)}</div><section class="pp-panel"><h3>${state.language === 'ar' ? 'اختيارات النمذجة' : 'Modeling choices'}</h3>${bullets(slide.methods)}</section></div>${why(slide)}`);
    if (slide.type === 'imbalance') { const graduate = m.target_counts?.Graduate || 0; const dropout = m.target_counts?.Dropout || 0; return wrap(`<div class="pp-metrics pp-metrics-two">${metricCard(t.graduate, count(graduate))}${metricCard(t.dropout, count(dropout), '', 'accent')}</div>${bars([{label:t.graduate, value:graduate}, {label:t.dropout, value:dropout}], Math.max(graduate, dropout))}<div class="pp-method-row"><span>${esc(slide.handling[0])}</span><span>${esc(slide.handling[1])}</span></div><p class="pp-note">${esc(slide.smote)}</p>${why(slide)}`); }
    if (slide.type === 'models') return wrap(`<div class="pp-chart-card pp-model-chart"><canvas id="pp-model-chart" aria-label="Cross-validation PR-AUC by model"></canvas></div><div class="pp-model-notes">${slide.model_notes.map(item => `<div><b>${esc(item[0])}</b><span>${esc(item[1])}</span></div>`).join('')}</div>${why(slide)}`);
    if (slide.type === 'selection') return wrap(`<div class="pp-selection-summary"><div class="pp-selection-metric"><span>${esc(state.language === 'ar' ? 'مقياس الاختيار الأساسي' : 'Primary selection metric')}</span><strong>${esc(slide.selection_metric)}</strong></div><div class="pp-selection-metric"><span>${esc(t.status)}</span><strong>${esc(m.selected_model || '—')}</strong></div></div><div class="pp-chart-card pp-selection-chart"><canvas id="pp-selection-chart" aria-label="Train and cross-validation PR-AUC"></canvas></div>${bullets(slide.points)}${why(slide)}`);
    if (slide.type === 'calibration') { const high = Number(m.thresholds?.high_risk || 0); const medium = Number(m.thresholds?.medium_risk || 0); const margin = Number(m.thresholds?.review_margin || 0); return wrap(`<div class="pp-calibration-summary"><div class="pp-calibrator"><span>${state.language === 'ar' ? 'أداة المعايرة' : 'Calibration method'}</span><strong>${esc(slide.calibrator)}</strong></div><div class="pp-threshold-scale"><i style="left:${medium * 100}%"><b>${esc(t.medium)} ${pct(medium)}</b></i><i style="left:${high * 100}%"><b>${esc(t.high)} ${pct(high)}</b></i></div><div class="pp-metrics pp-metrics-three">${metricCard(t.threshold, pct(high))}${metricCard(t.medium, pct(medium))}${metricCard(t.review_margin, `±${pct(margin)}`)}</div></div>${bullets(slide.points)}${why(slide)}`); }
    if (slide.type === 'performance') { const x = m.test_metrics || {}; return wrap(`<div class="pp-metrics pp-metrics-four">${metricCard(t.accuracy, pct(x.Accuracy))}${metricCard(t.precision, pct(x.Precision))}${metricCard(t.recall, pct(x.Recall), '', 'emphasis')}${metricCard(t.f1, pct(x.F1))}${metricCard(t.pr_auc, pct(x['PR-AUC']))}${metricCard(t.roc_auc, pct(x['ROC-AUC']))}${metricCard(t.brier, num(x['Brier Score'], 4))}</div><div class="pp-academic-callout"><b>${esc(t.recall)}</b><span>${esc(slide.why)}</span></div>`); }
    if (slide.type === 'evaluation') { const cm = m.confusion_matrix || [[0, 0], [0, 0]]; const intervals = m.confidence_intervals || []; return wrap(`<div class="pp-evaluation-top"><div><h3>${esc(state.language === 'ar' ? 'الفعلي × المتوقع' : 'Actual × predicted')}</h3><div class="pp-matrix"><div><b>${cm[0][0]}</b><span>${esc(t.true_graduate)}</span></div><div><b>${cm[0][1]}</b><span>${esc(t.false_alert)}</span></div><div><b>${cm[1][0]}</b><span>${esc(t.missed_dropout)}</span></div><div><b>${cm[1][1]}</b><span>${esc(t.true_dropout)}</span></div></div></div><div class="pp-ci"><h3>${esc(state.language === 'ar' ? 'فواصل الثقة 95٪' : '95% confidence intervals')}</h3>${intervals.slice(0, 3).map(row => `<div><span>${esc(row.Metric)}</span><b>${num(row['95% CI Low'], 3)}–${num(row['95% CI High'], 3)}</b></div>`).join('')}</div></div><div class="pp-chart-row"><div class="pp-chart-card"><h4>ROC-AUC ${num(m.test_metrics?.['ROC-AUC'], 3)}</h4><canvas id="pp-roc-chart"></canvas></div><div class="pp-chart-card"><h4>PR-AUC ${num(m.test_metrics?.['PR-AUC'], 3)}</h4><canvas id="pp-pr-chart"></canvas></div><div class="pp-chart-card"><h4>${esc(state.language === 'ar' ? 'المعايرة' : 'Calibration')}</h4><canvas id="pp-cal-chart"></canvas></div></div><p class="pp-note">${esc(slide.interpretation)}</p>`); }
    if (slide.type === 'explainability') { const global = (m.shap_global || []).slice(0, 5); const max = global[0]?.['Mean |SHAP|'] || 1; return wrap(`<div class="pp-definition-grid">${slide.definitions.map(item => `<div><b>${esc(item[0])}</b><span>${esc(item[1])}</span></div>`).join('')}</div><div class="pp-explain-grid"><section><h3>${esc(t.permutation)}</h3>${(m.permutation_importance || []).slice(0, 5).map(row => `<div class="pp-feature-row"><span>${esc(row.Feature)}</span><i style="width:${Math.max(3, row.Importance / Math.max((m.permutation_importance || [])[0]?.Importance || 1, 1e-9) * 100)}%"></i><b>${num(row.Importance, 3)}</b></div>`).join('')}</section><section><h3>${esc(t.shap)}</h3>${global.map(row => `<div class="pp-feature-row"><span>${esc(row.Feature)}</span><i style="width:${Math.max(3, row['Mean |SHAP|'] / max * 100)}%"></i><b>${num(row['Mean |SHAP|'], 3)}</b></div>`).join('')}</section></div><p class="pp-feature-note"><b>${state.language === 'ar' ? 'أمثلة على الخصائص المهمة:' : 'Examples of important features:'}</b> ${slide.features.map(feature => esc(feature)).join(' · ')}</p>${why(slide)}`); }
    if (slide.type === 'enrolled') { const risk = m.risk_counts || {}; return wrap(`<div class="pp-metrics pp-metrics-four">${metricCard(t.enrolled, count(m.enrolled_total))}${metricCard(t.low, count(risk.Low))}${metricCard(t.medium, count(risk.Medium))}${metricCard(t.high, count(risk.High), '', 'accent')}</div>${bars([{label:t.low, value:risk.Low || 0}, {label:t.medium, value:risk.Medium || 0}, {label:t.high, value:risk.High || 0}], Math.max(risk.Low || 0, risk.Medium || 0, risk.High || 0))}<div class="pp-review-count"><span>${esc(t.human_review)}</span><strong>${count(m.human_review_count)}</strong></div><p class="pp-note">${esc(slide.note)}</p>`); }
    if (slide.type === 'recommendations') return wrap(`${flow(slide.steps, 'pp-flow-recommendations')}<div class="pp-action-list">${slide.actions.map(action => `<span>${esc(action)}</span>`).join('')}</div><p class="pp-note">${esc(slide.note)}</p>`);
    return wrap(`${flow(slide.system, 'pp-flow-system')}<div class="pp-conclusion"><p>${esc(slide.conclusion)}</p><strong>${esc(slide.closing)}</strong></div>`);
  }

  function destroyCharts() { charts.splice(0).forEach(chart => chart.destroy?.()); }
  function fitFrame() {
    if (!frame || !stage) return;
    const bounds = stage.getBoundingClientRect();
    const width = Math.max(0, Math.min(bounds.width, bounds.height * 16 / 9));
    frame.style.width = `${Math.floor(width)}px`;
    frame.style.height = `${Math.floor(width * 9 / 16)}px`;
  }
  function chartOptions() { return { responsive: true, maintainAspectRatio: false, animation: { duration: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 0 : 650 }, plugins: { legend: { display: false }, tooltip: { backgroundColor: '#142441', titleColor: '#fff', bodyColor: '#d9e4f5', padding: 9 } }, scales: { x: { grid: { color: 'rgba(145,164,209,.12)' }, ticks: { color: '#a7b3ce', font: { size: 9 }, maxTicksLimit: 6 } }, y: { beginAtZero: true, grid: { color: 'rgba(145,164,209,.12)' }, ticks: { color: '#a7b3ce', font: { size: 9 }, maxTicksLimit: 5 } } } }; }
  function initCharts() {
    if (!window.Chart || !slides()[state.index]) return;
    const type = slides()[state.index].type;
    if (type === 'models' && document.querySelector('#pp-model-chart')) {
      const rows = metrics.cv_results || [];
      charts.push(new Chart(document.querySelector('#pp-model-chart'), { type: 'bar', data: { labels: rows.map(row => row.Model), datasets: [{ data: rows.map(row => row['CV PR-AUC']), backgroundColor: rows.map(row => row.Model === metrics.selected_model ? '#65e0b2' : '#747bf0'), borderRadius: 5 }] }, options: { ...chartOptions(), indexAxis: 'y', scales: { x: { min: .85, max: 1, grid: { color: 'rgba(145,164,209,.12)' }, ticks: { color: '#a7b3ce', font: { size: 9 } } }, y: { grid: { display: false }, ticks: { color: '#e9effb', font: { size: 10 } } } } } }));
    }
    if (type === 'selection' && document.querySelector('#pp-selection-chart')) {
      const rows = metrics.cv_results || [];
      charts.push(new Chart(document.querySelector('#pp-selection-chart'), { type: 'bar', data: { labels: rows.map(row => row.Model), datasets: [{ label: 'Train PR-AUC', data: rows.map(row => row['Train PR-AUC']), backgroundColor: '#747bf0', borderRadius: 4 }, { label: 'CV PR-AUC', data: rows.map(row => row['CV PR-AUC']), backgroundColor: '#65e0b2', borderRadius: 4 }] }, options: { ...chartOptions(), scales: { x: { grid: { display: false }, ticks: { color: '#a7b3ce', font: { size: 9 } } }, y: { min: .8, max: 1, grid: { color: 'rgba(145,164,209,.12)' }, ticks: { color: '#a7b3ce', font: { size: 9 } } } } } }));
    }
    if (type === 'evaluation') {
      const curve = metrics.curves || {};
      const line = (id, labels, values, color, xTitle) => { const canvas = document.querySelector(`#${id}`); if (!canvas) return; charts.push(new Chart(canvas, { type: 'line', data: { labels: labels || [], datasets: [{ data: values || [], borderColor: color, backgroundColor: `${color}22`, pointRadius: 0, borderWidth: 2, tension: .18, fill: true }] }, options: { ...chartOptions(), scales: { x: { grid: { color: 'rgba(145,164,209,.12)' }, ticks: { display: false }, title: { display: true, text: xTitle, color: '#8999bc', font: { size: 9 } } }, y: { min: 0, max: 1, grid: { color: 'rgba(145,164,209,.12)' }, ticks: { color: '#a7b3ce', font: { size: 9 }, maxTicksLimit: 4 } } } } })); };
      line('pp-roc-chart', curve.roc?.x, curve.roc?.y, '#6fe1ba', 'FPR');
      line('pp-pr-chart', curve.precision_recall?.x, curve.precision_recall?.y, '#7e85ff', 'Recall');
      line('pp-cal-chart', curve.calibration?.mean_predicted, curve.calibration?.fraction_positive, '#efbd69', 'Mean predicted');
    }
  }
  function renderSelectionEvidence() {
    if (slides()[state.index]?.type !== 'selection') return;
    const summary = document.querySelector('.pp-selection-summary');
    if (!summary) return;
    summary.classList.add('pp-selection-evidence');
    summary.insertAdjacentHTML('beforeend', metricCard(ui().train_pr, pct(metrics.train_pr_auc), '', 'accent') + metricCard(ui().cv_pr, pct(metrics.cv_pr_auc), '', 'emphasis') + metricCard(ui().gap, `${(Number(metrics.train_cv_gap) * 100).toFixed(2)} pp`));
  }
  function render() {
    state.language = document.documentElement.lang === 'ar' ? 'ar' : 'en';
    root.dir = state.language === 'ar' ? 'rtl' : 'ltr';
    const active = state.index;
    destroyCharts();
    slidesEl.innerHTML = slides().map(slideMarkup).join('');
    slidesEl.querySelectorAll('.pp-slide').forEach((slide, index) => slide.classList.toggle('active', index === active));
    renderSelectionEvidence();
    fitFrame();
    document.querySelector('#powerpoint-app').setAttribute('aria-label', state.language === 'ar' ? 'العرض التقديمي' : 'PowerPoint presentation');
    document.querySelector('#pp-kicker').textContent = state.language === 'ar' ? 'EduGuard AI · عرض أكاديمي' : 'EduGuard AI · academic presentation';
    document.querySelector('#pp-title').textContent = state.language === 'ar' ? 'العرض التقديمي' : 'PowerPoint';
    document.querySelector('#pp-fullscreen').setAttribute('aria-label', document.fullscreenElement ? ui().exit_fullscreen : ui().fullscreen);
    document.querySelector('.pp-exit').setAttribute('aria-label', ui().back);
    document.querySelector('.pp-controls').setAttribute('aria-label', ui().controls);
    document.querySelector('#pp-prev span').textContent = ui().previous;
    document.querySelector('#pp-next span').textContent = ui().next;
    document.querySelector('#pp-fullscreen span').textContent = document.fullscreenElement ? ui().exit_fullscreen : ui().fullscreen;
    document.querySelector('#pp-slide-label').textContent = ui().slide;
    document.querySelector('#pp-count').textContent = `${active + 1} / ${slides().length}`;
    document.querySelector('#pp-hint').textContent = ui().keyboard;
    document.querySelector('#pp-progress').style.width = `${((active + 1) / slides().length) * 100}%`;
    document.querySelector('#pp-prev').disabled = active === 0;
    document.querySelector('#pp-next').disabled = active === slides().length - 1;
    EG?.icons?.();
    requestAnimationFrame(initCharts);
  }
  function go(delta) { const next = Math.max(0, Math.min(slides().length - 1, state.index + delta)); if (next !== state.index) { state.index = next; render(); } }

  document.querySelector('#pp-prev').addEventListener('click', () => go(-1));
  document.querySelector('#pp-next').addEventListener('click', () => go(1));
  document.querySelector('#pp-fullscreen').addEventListener('click', () => { if (!document.fullscreenElement) root.requestFullscreen?.(); else document.exitFullscreen?.(); });
  document.addEventListener('fullscreenchange', render);
  document.addEventListener('keydown', event => { if (event.target instanceof Element && event.target.matches('input,textarea,select,button,a')) return; if (event.key === 'ArrowRight') { event.preventDefault(); go(state.language === 'ar' ? -1 : 1); } if (event.key === 'ArrowLeft') { event.preventDefault(); go(state.language === 'ar' ? 1 : -1); } if (event.key === ' ') { event.preventDefault(); go(1); } });
  stage.addEventListener('pointerdown', event => { state.pointerX = event.clientX; });
  stage.addEventListener('pointerup', event => { if (state.pointerX === null) return; const distance = event.clientX - state.pointerX; state.pointerX = null; if (Math.abs(distance) > 45) go(distance < 0 ? 1 : -1); });
  document.addEventListener('languagechange', render);
  window.addEventListener('resize', fitFrame, { passive: true });
  window.presentationViewer = { go, render, state, payload };
  render();
})();

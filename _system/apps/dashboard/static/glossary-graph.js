/* Shared glossary term-network rendering (ADR-0023).
 *
 * Single source of the cytoscape STYLE, the layout-engine registration and the
 * layout options, used by BOTH the full view (`/graph/glossary`, graph.html) and
 * the per-term ego snippet on a glossary detail page (mountEgo, detail.html).
 * Keeping styling/layout here means a colour or layout tweak lands in one place.
 */
window.AQ_GLOSSARY_GRAPH = (function () {
  // Colours/encoding per ADR-0023 (dark-theme amendment): GLO = blue hero, size =
  // degree; neighbour types carry their own colour; state = border colour.
  var STYLE = [
    { selector: 'node', style: {
        'label': 'data(label)', 'font-size': 11,
        'text-valign': 'center', 'text-halign': 'center',
        'text-wrap': 'wrap', 'text-max-width': 112,
        'width': 'label', 'height': 'label', 'padding': '8px',
        'color': '#e8eef9', 'text-outline-color': '#0e1726', 'text-outline-width': 2.5,
        'border-width': 1.5
    }},
    { selector: 'node[type="GLO"]', style: {
        'shape': 'round-rectangle',
        'padding': 'mapData(degree, 0, 8, 9, 26)',
        'background-color': '#2f6fb3', 'color': '#ffffff',
        'text-outline-color': '#13243f', 'border-color': '#9fb0cc', 'border-width': 2.5
    }},
    { selector: 'node[type="GLO"][state="agreed"]', style: { 'border-color': '#46d3b0', 'border-width': 3.5 }},
    { selector: 'node[type="GLO"][state="draft"]',  style: { 'border-color': '#ffb454', 'border-width': 2.5 }},
    { selector: 'node[type="GLO"][state="deprecated"]', style: {
        'background-color': '#3a4a63', 'border-color': '#6f81a3',
        'border-style': 'dashed', 'color': '#cdd6e6', 'opacity': 0.6
    }},
    { selector: 'node[type="GLO"][?assumption]', style: { 'border-style': 'dashed' }},
    { selector: 'node[type="DM"]',   style: { 'shape':'round-rectangle','background-color':'#3a8f7d','border-color':'#6fc2ad','color':'#ffffff','text-outline-color':'#10342b' }},
    { selector: 'node[type="STK"]',  style: { 'shape':'ellipse','background-color':'#c98a2b','border-color':'#e6b667','color':'#ffffff','text-outline-color':'#3d2908' }},
    { selector: 'node[type="EIF"]',  style: { 'shape':'hexagon','background-color':'#7a5ea8','border-color':'#b39ad6','color':'#ffffff','text-outline-color':'#271a3a' }},
    { selector: 'node[type="GOAL"]', style: { 'shape':'diamond','background-color':'#b8932f','border-color':'#e0c068','color':'#ffffff','text-outline-color':'#3a2d08' }},
    { selector: 'node[rest]',
      style: { 'shape':'diamond','background-color':'#7e8aa3','border-color':'#aab4c9','color':'#ffffff','text-outline-color':'#1d2436' }},
    { selector: 'edge', style: { 'width':1.2, 'line-color':'#3a4a72', 'curve-style':'bezier' }},
    { selector: 'edge[?cross]', style: { 'line-color':'#2f3d61', 'line-style':'dashed' }},
    { selector: '.hidden', style: { 'display':'none' }},
    { selector: '.faded', style: { 'opacity':0.12, 'text-opacity':0.12 }},
    { selector: 'edge.high', style: { 'line-color':'#3ea6ff', 'width':2.4, 'opacity':1 }},
    // ego snippet: ring the focal term so it reads as the centre of its network
    { selector: 'node[?focus]', style: { 'border-color': '#3ea6ff', 'border-width': 4 }}
  ];

  // Register fcose (needs cytoscape.use) and detect cola (auto-registers on load).
  // Returns the available engines and the default (cola → fcose → builtin cose).
  function register(cytoscape) {
    var avail = { cose: true, fcose: false, cola: false };
    try { if (window.cytoscapeFcose) { cytoscape.use(window.cytoscapeFcose); avail.fcose = true; } } catch (e) {}
    if (window.cytoscapeCola && window.cola) { avail.cola = true; }
    return { avail: avail, layout: avail.cola ? 'cola' : (avail.fcose ? 'fcose' : 'cose') };
  }

  // Layout options for the chosen engine. `compact:true` tightens spacing for the
  // small ego snippet; the full view passes no extra and gets the original params.
  function layoutOpts(name, randomize, extra) {
    extra = extra || {};
    var c = !!extra.compact;
    var base = { name: name, animate: true, animationDuration: 450, fit: !c,
                 padding: c ? 24 : 45, nodeDimensionsIncludeLabels: true };
    if (name === 'cola') {
      // Finite + avoidOverlap (label-sized boxes): settles and STOPS, so afterwards a
      // drag moves only the grabbed node; fit:false → caller frames once on layoutstop.
      return Object.assign(base, {
        randomize: !!randomize, fit: false,
        avoidOverlap: true, handleDisconnected: true,
        nodeSpacing: function () { return c ? 12 : 16; },
        edgeLength: c ? 110 : 150, maxSimulationTime: c ? 2500 : 4000,
        convergenceThreshold: 0.005, unconstrIter: 15, userConstIter: 20, allConstIter: 40
      });
    }
    if (name === 'fcose') {
      return Object.assign(base, {
        quality: 'proof', randomize: !!randomize, nodeSeparation: c ? 90 : 150,
        idealEdgeLength: c ? 95 : 130, nodeRepulsion: c ? 8000 : 12000,
        gravity: 0.15, gravityRange: 3.8, packComponents: true
      });
    }
    return Object.assign(base, {   // built-in cose fallback
      randomize: !!randomize, nodeOverlap: 30, componentSpacing: c ? 90 : 140,
      idealEdgeLength: c ? 95 : 130, gravity: 0.2
    });
  }

  // Compact, mostly-read-only ego snippet for a glossary detail page. Shows the focal
  // term + its direct GLO neighbours by default; the DM/STK/GOAL buttons reveal the
  // term's neighbours of that type (1-hop). A node tap opens that page.
  function mountEgo(opts) {
    var cytoscape = window.cytoscape;
    if (!cytoscape || !opts || !opts.container) return null;
    var reg = register(cytoscape);
    var LAYOUT = reg.layout;
    var data = opts.data;
    var layersEl = opts.layersSelector ? document.querySelector(opts.layersSelector) : null;

    var cy = cytoscape({
      container: opts.container,
      elements: { nodes: data.nodes, edges: data.edges },
      wheelSensitivity: 0.2,
      style: STYLE,
      layout: { name: 'preset' }
    });

    function relayout(randomize) {
      cy.nodes().off('grab free position lock unlock');
      var l = cy.elements(':visible').layout(layoutOpts(LAYOUT, randomize, { compact: true }));
      if (LAYOUT === 'cola') {
        l.one('layoutstop', function () {
          cy.nodes().off('grab free position lock unlock');
          cy.animate({ fit: { eles: cy.elements(':visible'), padding: 24 } }, { duration: 300 });
        });
      }
      l.run();
    }

    // default: focal term + direct GLO neighbours; cross-type neighbours hidden
    cy.batch(function () {
      cy.nodes().filter(function (n) { return n.data('type') !== 'GLO'; }).addClass('hidden');
      cy.edges().filter(function (e) { return !!e.data('cross'); }).addClass('hidden');
    });

    if (layersEl) {
      layersEl.querySelectorAll('.layer-btn[data-layer]').forEach(function (btn) {
        btn.addEventListener('click', function () {
          var on = btn.getAttribute('aria-pressed') !== 'true';
          btn.setAttribute('aria-pressed', on ? 'true' : 'false');
          btn.classList.toggle('on', on);
          var t = btn.dataset.layer;
          cy.batch(function () {
            var act = on ? 'removeClass' : 'addClass';
            cy.nodes('[type="' + t + '"]')[act]('hidden');
            cy.edges('[ntype="' + t + '"]')[act]('hidden');
          });
          relayout(false);
        });
      });
    }

    // the snippet doubles as navigation: tap a node → open its page
    cy.on('tap', 'node', function (e) { var u = e.target.data('url'); if (u) window.location = u; });

    relayout(true);
    return cy;
  }

  return { STYLE: STYLE, register: register, layoutOpts: layoutOpts, mountEgo: mountEgo };
})();

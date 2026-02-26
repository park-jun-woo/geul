(function () {
  'use strict';

  var canvas = document.getElementById('bg-canvas');
  if (!canvas) return;
  var ctx = canvas.getContext('2d');

  var W = 0;
  var H = 0;
  var dpr = window.devicePixelRatio || 1;
  var stars = [];
  var COUNT = 90;
  var time = 0;

  function resize() {
    W = window.innerWidth;
    H = window.innerHeight;
    canvas.width = W * dpr;
    canvas.height = H * dpr;
    canvas.style.width = W + 'px';
    canvas.style.height = H + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  function rand(lo, hi) {
    return Math.random() * (hi - lo) + lo;
  }

  function makeStar(offscreen) {
    var r = rand(0.4, 2.2);
    var x = offscreen ? -r - rand(0, W * 0.4) : rand(0, W);
    var cy = H * 0.88;
    var spread = H * 0.12;
    var y = cy + rand(-spread, spread);
    var baseAlpha = rand(0.15, 0.7);
    var warm = Math.random();

    return {
      x: x,
      y: y,
      baseY: y,
      r: r,
      alpha: baseAlpha,
      baseAlpha: baseAlpha,
      vx: rand(0.15, 0.6),
      amp: rand(10, 60),
      freq: rand(0.001, 0.004),
      twinkleSpeed: rand(0.01, 0.04),
      twinklePhase: rand(0, Math.PI * 2),
      warm: warm,
      hasRays: r > 1.6 && Math.random() > 0.5
    };
  }

  function init() {
    resize();
    stars = [];
    for (var i = 0; i < COUNT; i++) {
      stars.push(makeStar(false));
    }
  }

  function drawStar(s) {
    var twinkle = 0.5 + 0.5 * Math.sin(time * s.twinkleSpeed + s.twinklePhase);
    var alpha = s.baseAlpha * (0.4 + 0.6 * twinkle);

    var r, g, b;
    if (s.warm > 0.7) {
      r = 245; g = 166 + Math.round(s.warm * 30); b = 35 + Math.round(s.warm * 40);
    } else if (s.warm > 0.4) {
      r = 220 + Math.round(s.warm * 35); g = 220 + Math.round(s.warm * 30); b = 210 + Math.round(s.warm * 40);
    } else {
      r = 180 + Math.round(s.warm * 60); g = 200 + Math.round(s.warm * 40); b = 235 + Math.round(s.warm * 20);
    }

    var color = 'rgba(' + r + ',' + g + ',' + b + ',';

    if (s.hasRays) {
      var rayLen = s.r * (2.5 + 1.5 * twinkle);
      var rayAlpha = alpha * 0.3;
      ctx.strokeStyle = color + rayAlpha + ')';
      ctx.lineWidth = 0.5;
      ctx.beginPath();
      ctx.moveTo(s.x - rayLen, s.y);
      ctx.lineTo(s.x + rayLen, s.y);
      ctx.moveTo(s.x, s.y - rayLen);
      ctx.lineTo(s.x, s.y + rayLen);
      ctx.stroke();
    }

    if (s.r > 1.0) {
      var grad = ctx.createRadialGradient(s.x, s.y, 0, s.x, s.y, s.r * 3);
      grad.addColorStop(0, color + (alpha * 0.25) + ')');
      grad.addColorStop(1, color + '0)');
      ctx.beginPath();
      ctx.arc(s.x, s.y, s.r * 3, 0, Math.PI * 2);
      ctx.fillStyle = grad;
      ctx.fill();
    }

    ctx.beginPath();
    ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
    ctx.fillStyle = color + alpha + ')';
    ctx.fill();
  }

  function draw() {
    ctx.clearRect(0, 0, W, H);
    time++;

    for (var i = 0; i < stars.length; i++) {
      var s = stars[i];
      s.x += s.vx;
      s.y = s.baseY + s.amp * Math.sin(s.x * s.freq);

      if (s.x - s.r * 3 > W) {
        stars[i] = makeStar(true);
        continue;
      }

      drawStar(s);
    }

    requestAnimationFrame(draw);
  }

  window.addEventListener('resize', resize);
  init();
  draw();
})();

---
title: Autocorrelation names the accompaniment's low notes, so it cannot check a melody played over chords
tags: [audio, testing, signal-processing]
added: 2026-11-04
---

## Fact

An autocorrelation pitch detector finds the strongest repeating period in the
whole signal. Over chords that is the bass, a chord's common period or an
earlier note still ringing, not the tune on top. Rendered with a quiet
accompaniment, one 25-note melody read correctly on only a handful of its notes;
the rest came back an octave or more low.

Measuring the energy at each candidate note's frequency over a short window from
the note's start, and taking the loudest in the melody's own range, read all 25.

## Why it matters

The wrong readings look like a bug in the synthesis or the note table, and a
balance fix made to satisfy the detector changes what is heard for no reason.

## How to apply

Render offline (`OfflineAudioContext` on the web) so timing is exact, then for
each note the score says starts at time `t`:

```js
const w = (2 * Math.PI * freq) / sampleRate;
let re = 0, im = 0;
for (let i = 0; i < n; i++) { re += d[a + i] * Math.cos(w * i); im += d[a + i] * Math.sin(w * i); }
const energy = re * re + im * im;
```

- Start just after the note's attack, and keep the window short enough to end
  before the next note: the tail of the last note is otherwise what you measure.
- Compare semitones from the melody's lowest note up, so the bass cannot win.
- A note that loses here is a real balance problem: the tune is not on top.

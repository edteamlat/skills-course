# Themes

Override the `:root` CSS variables to apply a different theme.
All other CSS remains identical — only the variable values change.

---

## dark-gold (default)

The EDteam default. Dark background, warm gold accent.

```css
:root {
  --bg:       #0a0a0a;
  --surface:  #111111;
  --surface2: #1a1a1a;
  --border:   rgba(255,255,255,0.08);
  --border2:  rgba(255,255,255,0.14);
  --text:     #f0ede8;
  --muted:    #6b6b6b;
  --accent:   #e8d5a3;
  --accent2:  #c8b98a;
  --green:    #7dba8a;
  --red:      #d97070;
  --blue:     #7aafcf;
}
```

---

## dark-blue

Cool, technical. Good for infrastructure, DevOps, systems topics.

```css
:root {
  --bg:       #080c12;
  --surface:  #0e1520;
  --surface2: #162030;
  --border:   rgba(100,160,255,0.1);
  --border2:  rgba(100,160,255,0.18);
  --text:     #e8edf5;
  --muted:    #5a6a82;
  --accent:   #7aafcf;
  --accent2:  #5a9abf;
  --green:    #6dbf8a;
  --red:      #d97070;
  --blue:     #9ac5e8;
}
```

---

## dark-green

Earthy, open source feel. Good for CLI tools, backend, Go, Rust topics.

```css
:root {
  --bg:       #080d09;
  --surface:  #0e1510;
  --surface2: #152018;
  --border:   rgba(80,200,100,0.1);
  --border2:  rgba(80,200,100,0.18);
  --text:     #e5f0e8;
  --muted:    #52705a;
  --accent:   #7dba8a;
  --accent2:  #5da06a;
  --green:    #9dd4a8;
  --red:      #d97070;
  --blue:     #7aafcf;
}
```

---

## light-minimal

Clean white. Good for design, UX, product, and business topics.

```css
:root {
  --bg:       #fafaf8;
  --surface:  #ffffff;
  --surface2: #f0ede8;
  --border:   rgba(0,0,0,0.07);
  --border2:  rgba(0,0,0,0.12);
  --text:     #1a1a18;
  --muted:    #999990;
  --accent:   #8b6914;
  --accent2:  #a07820;
  --green:    #2d7a40;
  --red:      #b03030;
  --blue:     #2060a0;
}
```

For light themes, also update the `.key-hint` and nav:
```css
.nav { background: #ffffff; }
.key { background: #f0ede8; }
```

---

## How to apply

Replace the entire `:root { … }` block in the HTML scaffold with the chosen theme's block.
Everything else stays the same.

If the user specifies a color (e.g. "purple accent", "blue theme") but doesn't name a
preset, derive the variables from that color:
- `--accent` = the named color at 70% lightness
- `--accent2` = the named color at 55% lightness
- Keep `--bg` as `#080808` to `#0e0e0e` range for dark themes
- Keep `--green` / `--red` / `--blue` as semantic colors (don't tint them)

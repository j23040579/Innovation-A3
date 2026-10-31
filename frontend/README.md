# Kikan React — exact-layout migration

This first React migration intentionally preserves the original Kikan HTML/CSS/JavaScript UI and interactions. It is a compatibility step before refactoring individual areas into native React components.

## Run locally (Windows)

1. Extract the ZIP completely.
2. Open the extracted `kikan-react-exact` folder — the folder that contains `package.json`. Do not run npm from the parent folder.
3. Install the dependencies and start Vite in PowerShell or Command Prompt:

```powershell
npm install
npm run dev
```

4. Open the local URL printed by Vite (usually `http://localhost:5173`). Keep that terminal window open while using the site.
5. To check a production build, stop the dev server and run `npm run build`. To preview the build, run `npm run preview`.

You need a supported Node.js/npm installation and an internet connection for the first dependency install unless the npm packages are already cached.

Next: connect the real project datasets to the existing SVG map to make it a data-driven choropleth without changing the visual design.

## Accessibility and visualization updates

- The top-right Menu holds navigation, accessibility controls (larger text, high contrast, reduced motion), and light/dark theme toggle. The menu closes after navigation, on outside click, or with Escape.
- Prediction's weather-monitoring card expands across the available row; the separate safety and emergency cards have been removed. A compact risk badge and prototype disclaimer are integrated into the monitoring card.
- Selecting a prefecture highlights it, dims other prefectures, and zooms the map to that prefecture. The existing zoom, pan, and reset controls remain available.
- The map disaster selector recolors the prefectures for typhoon, heavy rain, flood, landslide, or thunderstorm scores; the legend title follows the selected hazard. Heavy-snow map shading and the heavy-snow chart are available only when Niigata or Yamagata is selected. Changing away from those prefectures automatically switches the map back to typhoon mode.
- Data Visualization charts are rendered with D3.js. Zoom buttons adjust the visible months on the X-axis while keeping the Y-axis fixed at 0–100; Reset returns to the full year.
- D3.js is included as an npm dependency so charts do not rely on a separate CDN script.
- The shelter panel can render every shelter entry provided for a prefecture, but the currently bundled shelter names and generated route details are illustrative placeholders. They are not a verified official shelter directory and should not be used for real-world emergency decisions. Add verified municipal/open-data shelter records before presenting the directory as factual.



## Kikan UI design system

- Visual direction: Japanese-inspired, modern and restrained, with navy/blue/teal interface accents.
- Hazard levels are exactly **Low**, **Medium**, and **High** (green, amber, and red). These labels are UI categories; the underlying score thresholds remain those defined in the existing prototype logic.
- Light and dark themes use CSS variables for surfaces, text, axes, gridlines, and D3 series. Switching themes rerenders the D3 charts.
- Cards use subtle shadows and a restrained hover lift; reduced-motion preferences disable those transitions.
- The current project renders a legacy markup template inside a React wrapper. To avoid a risky full rewrite, this update styles the existing UI rather than introducing Material UI components into the legacy DOM. Material UI can be integrated safely as the app is refactored into regular React components.
- Prototype scores and example shelter information remain illustrative and are not for real-world safety decisions.


## Japanese-inspired theme update

The app uses a light background in Light mode and a deep navy background in Dark mode. Risk categories are limited to Low, Medium, and High. Run npm commands from this folder (the folder containing package.json).

## Trained-model integration (not connected yet)

The current UI still uses illustrative values embedded in the prototype code. The new map hazard selector changes which embedded hazard score is visualized; it does not connect or run trained models. To connect Assignment 2 models, provide the trained model artifacts (for example `.joblib`, `.pkl`, `.onnx`, or the format you used), the exact feature order, preprocessing/encoding and scaling code, target-label mapping, and a small example of model input/output. Raw training CSVs alone usually are not enough to reproduce predictions unless the training and inference pipeline is also supplied.

The intended integration is React UI → FastAPI endpoint → saved model plus its preprocessing pipeline → JSON prediction response → update the selected prefecture cards/map/charts. Never treat the existing illustrative values as live safety advice. Model files have not been connected in this ZIP.

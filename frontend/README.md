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
- Map selections request backend data using the last date interval applied with **Check risk**; before any interval has been applied, they use tomorrow in Japan time. Single-day predictions and the date-specific map overview use the interval's end date, while weather charts use the full interval because the prediction API does not provide interval-level hazard predictions. Heavy-rain and snow shading use their respective prediction results; other map hazards use the map overview's date-specific primary risk where available.
- The map disaster selector recolors prefectures for typhoon, heavy rain, flood, or heavy snow. Heavy-snow map shading uses the model's predicted risk level; prefectures without an inference prediction show white, and the option is hidden when the selected prefecture has no prediction. Changing to an unsupported prefecture automatically switches the map back to typhoon mode. The separate heavy-snow chart remains limited to Niigata and Yamagata.
- All chart rendering lives in `src/charts/d3Charts.js` and uses D3.js for both illustrative monthly analytics and live backend time series. Charts resize to their available container width for phone and desktop layouts; the zoom buttons and D3 wheel, drag, and touch gestures zoom the visible X-axis data, while Reset returns to the full range.
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

Most map hazards and seasonal summaries still use illustrative values embedded in the prototype code. Heavy-snow map shading is the exception: it loads the backend snow model's prediction for prefectures with forecast coverage and leaves other prefectures unshaded. To connect additional Assignment 2 models, provide the trained model artifacts (for example `.joblib`, `.pkl`, `.onnx`, or the format you used), the exact feature order, preprocessing/encoding and scaling code, target-label mapping, and a small example of model input/output. Raw training CSVs alone usually are not enough to reproduce predictions unless the training and inference pipeline is also supplied.

The intended integration is React UI → FastAPI endpoint → saved model plus its preprocessing pipeline → JSON prediction response → update the selected prefecture cards/map/charts. Never treat the existing illustrative values as live safety advice. Model files have not been connected in this ZIP.

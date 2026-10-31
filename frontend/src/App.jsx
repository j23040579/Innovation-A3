import { useEffect, useRef } from "react";
import * as d3 from "d3";
import { kikanMarkup } from "./legacy/kikanMarkup";
import { kikanLegacy } from "./legacy/kikanLegacy";
import "./legacy/kikan.css";

export default function App() {
  const rootRef = useRef(null);

  useEffect(() => {
    if (!rootRef.current) return;
    rootRef.current.innerHTML = kikanMarkup;
    window.d3 = d3;
    new Function(kikanLegacy)();
  }, []);

  return <div ref={rootRef} />;
}

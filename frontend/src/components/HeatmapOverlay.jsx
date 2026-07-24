import React, { useState } from 'react';
import { Eye, Layers, Download } from 'lucide-react';

export const HeatmapOverlay = ({ originalUrl, heatmapUrl, imageName = "radiograph.jpg" }) => {
  const [opacity, setOpacity] = useState(0.65);
  const [mode, setMode] = useState('blend'); // blend, split, sideBySide

  const downloadHeatmap = () => {
    const link = document.createElement('a');
    link.href = heatmapUrl || originalUrl;
    link.download = `gradcam_heatmap_${imageName}`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="glass-panel p-5 rounded-2xl space-y-4">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 border-b border-slate-200 pb-3">
        <div>
          <h3 className="text-base font-bold text-slate-900 flex items-center space-x-2">
            <Layers className="w-5 h-5 text-sky-600" />
            <span>Grad-CAM Explainable AI Heatmap</span>
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">Visual activation highlighting neural network decision regions</p>
        </div>
        <div className="flex items-center space-x-2">
          <button
            onClick={() => setMode('blend')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition ${
              mode === 'blend' ? 'bg-sky-600 text-white shadow-sm' : 'bg-slate-100 text-slate-600 hover:text-slate-900 hover:bg-slate-200'
            }`}
          >
            Overlay
          </button>
          <button
            onClick={() => setMode('sideBySide')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition ${
              mode === 'sideBySide' ? 'bg-sky-600 text-white shadow-sm' : 'bg-slate-100 text-slate-600 hover:text-slate-900 hover:bg-slate-200'
            }`}
          >
            Side-by-Side
          </button>
          <button
            onClick={downloadHeatmap}
            className="flex items-center space-x-1 px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-100 border border-slate-200 text-sky-700 hover:bg-slate-200 transition"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Save</span>
          </button>
        </div>
      </div>

      {mode === 'blend' ? (
        <div className="space-y-4">
          <div className="relative w-full aspect-square max-w-md mx-auto rounded-xl overflow-hidden border border-slate-200 bg-slate-900 flex items-center justify-center shadow-md">
            {/* Base original image */}
            <img
              src={originalUrl}
              alt="Original scan"
              className="absolute inset-0 w-full h-full object-contain"
            />
            {/* Heatmap overlay with opacity */}
            {heatmapUrl && (
              <img
                src={heatmapUrl}
                alt="Grad-CAM Overlay"
                className="absolute inset-0 w-full h-full object-contain transition-opacity duration-150"
                style={{ opacity: opacity }}
              />
            )}
          </div>

          <div className="max-w-md mx-auto space-y-1">
            <div className="flex justify-between text-xs font-medium text-slate-500">
              <span>Original Radiograph</span>
              <span className="text-sky-600 font-bold">{Math.round(opacity * 100)}% Heatmap Intensity</span>
              <span>Grad-CAM Color Map</span>
            </div>
            <input
              type="range"
              min="0"
              max="1"
              step="0.01"
              value={opacity}
              onChange={(e) => setOpacity(parseFloat(e.target.value))}
              className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-sky-600"
            />
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 max-w-2xl mx-auto">
          <div className="space-y-2">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Original Scan</span>
            <div className="aspect-square rounded-xl overflow-hidden border border-slate-200 bg-slate-900 shadow-sm">
              <img src={originalUrl} alt="Original" className="w-full h-full object-contain" />
            </div>
          </div>
          <div className="space-y-2">
            <span className="text-xs font-semibold text-sky-600 uppercase tracking-wider">Grad-CAM Jet Heatmap</span>
            <div className="aspect-square rounded-xl overflow-hidden border border-slate-200 bg-slate-900 shadow-sm">
              <img src={heatmapUrl || originalUrl} alt="Grad-CAM" className="w-full h-full object-contain" />
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

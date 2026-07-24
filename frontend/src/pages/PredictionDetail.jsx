import React, { useState, useEffect } from 'react';
import { useLocation, useParams, Link } from 'react-router-dom';
import api from '../services/api';
import { HeatmapOverlay } from '../components/HeatmapOverlay';
import { ReportModal } from '../components/ReportModal';
import { Activity, ShieldCheck, FileText, ArrowLeft, AlertCircle, Sparkles, CheckCircle2, RefreshCw } from 'lucide-react';

export const PredictionDetail = () => {
  const { id } = useParams();
  const location = useLocation();
  const [prediction, setPrediction] = useState(location.state?.prediction || null);
  const [report, setReport] = useState(null);
  const [loadingReport, setLoadingReport] = useState(false);
  const [showReportModal, setShowReportModal] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!prediction && id) {
      fetchPrediction();
    }
  }, [id]);

  const fetchPrediction = async () => {
    try {
      const res = await api.get('/history');
      if (res.data.success) {
        const found = res.data.data.find(p => p.id === id || p._id === id);
        if (found) setPrediction(found);
      }
    } catch (err) {
      setError('Unable to load scan prediction details.');
    }
  };

  const handleGenerateReport = async () => {
    if (!prediction) return;
    setLoadingReport(true);
    setError('');
    try {
      const res = await api.post('/generate-report', {
        prediction_id: prediction.id || prediction._id,
        patient_id: "P-100234",
        clinical_context: "Chest radiograph evaluation for acute respiratory distress"
      });
      if (res.data.success) {
        setReport(res.data.data);
        setShowReportModal(true);
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Report generation failed.');
    } finally {
      setLoadingReport(false);
    }
  };

  if (!prediction) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-4">
        <Activity className="w-10 h-10 text-sky-400 animate-spin" />
        <p className="text-slate-600 font-semibold">Loading Diagnostic Results...</p>
      </div>
    );
  }

  const isNormal = prediction.predicted_class?.toLowerCase() === 'normal';

  return (
    <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8 space-y-8">
      
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-slate-200 pb-6">
        <div className="flex items-center space-x-3">
          <Link
            to="/history"
            className="p-2 rounded-xl bg-slate-100 text-slate-500 hover:text-slate-900 transition"
          >
            <ArrowLeft className="w-5 h-5" />
          </Link>
          <div>
            <h1 className="text-2xl font-extrabold text-slate-900 flex items-center space-x-2">
              <span>Diagnostic Result</span>
              <span className="text-xs px-2.5 py-0.5 rounded-full bg-sky-50 text-sky-700 border border-sky-200">
                {prediction.organ_system || 'Chest Radiograph'}
              </span>
            </h1>
            <p className="text-xs text-slate-500 mt-0.5">Scan ID: {prediction.id || prediction._id}</p>
          </div>
        </div>

        <button
          onClick={handleGenerateReport}
          disabled={loadingReport}
          className="flex items-center space-x-2 px-5 py-3 rounded-xl bg-gradient-to-r from-teal-500 via-sky-500 to-indigo-600 hover:from-teal-400 hover:to-indigo-500 text-white font-bold text-sm shadow-lg shadow-sky-500/20 transition disabled:opacity-50"
        >
          {loadingReport ? (
            <>
              <RefreshCw className="w-4 h-4 animate-spin" />
              <span>Generating Gemini Report...</span>
            </>
          ) : (
            <>
              <Sparkles className="w-4 h-4" />
              <span>Generate AI Clinical Report</span>
            </>
          )}
        </button>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-sm flex items-center space-x-2">
          <AlertCircle className="w-5 h-5 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Main Grid: Prediction Results + Grad-CAM Heatmap */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Left Column: Classification Outcome & Probabilities (5 cols) */}
        <div className="lg:col-span-5 space-y-6">
          
          {/* Top Prediction Badge */}
          <div className="glass-panel p-6 rounded-3xl space-y-4 border border-slate-200">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider block">Top Pathological Finding</span>
            <div className="flex items-center justify-between">
              <span className={`text-3xl font-extrabold ${isNormal ? 'text-emerald-400' : 'text-rose-400'}`}>
                {prediction.predicted_class}
              </span>
              <div className={`p-3 rounded-2xl ${isNormal ? 'bg-emerald-100 text-emerald-600' : 'bg-rose-100 text-rose-600'}`}>
                {isNormal ? <CheckCircle2 className="w-8 h-8" /> : <AlertCircle className="w-8 h-8" />}
              </div>
            </div>

            <div className="space-y-1.5 pt-2">
              <div className="flex justify-between text-xs font-semibold">
                <span className="text-slate-700">Diagnostic Confidence</span>
                <span className="text-sky-600 font-extrabold">{prediction.confidence}%</span>
              </div>
              <div className="w-full h-3 bg-slate-200 rounded-full overflow-hidden">
                <div
                  className={`h-full rounded-full ${isNormal ? 'bg-emerald-500' : 'bg-gradient-to-r from-amber-500 to-rose-500'}`}
                  style={{ width: `${prediction.confidence}%` }}
                ></div>
              </div>
            </div>
          </div>

          {/* Probability Distribution */}
          <div className="glass-panel p-6 rounded-3xl space-y-4">
            <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider">Multi-Class Probability Distribution</h3>
            <div className="space-y-3">
              {prediction.all_probabilities?.map((prob, idx) => (
                <div key={idx} className="space-y-1">
                  <div className="flex justify-between text-xs font-semibold">
                    <span className="text-slate-700">{prob.class_name}</span>
                    <span className="text-slate-500">{prob.confidence}%</span>
                  </div>
                  <div className="w-full h-2 bg-slate-200 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-sky-500 rounded-full"
                      style={{ width: `${prob.confidence}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </div>

        </div>

        {/* Right Column: Grad-CAM Explainable AI Heatmap (7 cols) */}
        <div className="lg:col-span-7">
          <HeatmapOverlay
            originalUrl={prediction.image_url}
            heatmapUrl={prediction.gradcam_heatmap_url}
            imageName={prediction.image_name}
          />
        </div>

      </div>

      {/* Render AI Report Modal */}
      {showReportModal && (
        <ReportModal report={report} onClose={() => setShowReportModal(false)} />
      )}

    </div>
  );
};

import React from 'react';
import { FileText, X, Printer, AlertTriangle, CheckCircle2, ShieldAlert, User, Calendar, Stethoscope } from 'lucide-react';

export const ReportModal = ({ report, onClose }) => {
  if (!report) return null;

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm overflow-y-auto">
      <div className="relative w-full max-w-4xl glass-panel bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl overflow-hidden my-8">
        
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-slate-800 bg-slate-950/80">
          <div className="flex items-center space-x-3">
            <div className="p-2.5 rounded-xl bg-sky-500/20 border border-sky-500/30 text-sky-400">
              <FileText className="w-6 h-6" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-white">AI Clinical Diagnostic Report</h2>
              <p className="text-xs text-slate-400">Automated LLM Synthesis • Patient ID: {report.patient_id || 'P-100234'}</p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <button
              onClick={handlePrint}
              className="flex items-center space-x-1.5 px-3.5 py-2 rounded-lg bg-sky-500 text-white font-semibold text-xs hover:bg-sky-400 transition"
            >
              <Printer className="w-4 h-4" />
              <span>Print Report</span>
            </button>
            <button
              onClick={onClose}
              className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Content Body */}
        <div className="p-6 space-y-6 max-h-[75vh] overflow-y-auto print:max-h-none print:overflow-visible">
          
          {/* Executive Summary */}
          <div className="p-4 rounded-xl bg-sky-500/10 border border-sky-500/20 space-y-2">
            <h3 className="text-xs font-bold uppercase tracking-wider text-sky-400 flex items-center space-x-1.5">
              <Stethoscope className="w-4 h-4" />
              <span>Clinical Summary</span>
            </h3>
            <p className="text-sm text-slate-200 leading-relaxed">{report.summary}</p>
          </div>

          {/* Key Diagnostic Findings & Confidence */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-4 rounded-xl bg-slate-800/60 border border-slate-700/80 space-y-2">
              <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">AI Findings</h4>
              <p className="text-sm text-slate-100 font-medium">{report.prediction_findings}</p>
            </div>
            <div className="p-4 rounded-xl bg-slate-800/60 border border-slate-700/80 space-y-2">
              <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Confidence Assessment</h4>
              <p className="text-sm text-slate-100 font-medium">{report.confidence_assessment}</p>
            </div>
          </div>

          {/* Differential Causes & Risk Factors */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-4 rounded-xl bg-slate-800/40 border border-slate-800 space-y-2">
              <h4 className="text-xs font-bold text-amber-400 uppercase tracking-wider flex items-center space-x-1.5">
                <AlertTriangle className="w-4 h-4" />
                <span>Possible Causes</span>
              </h4>
              <ul className="space-y-1 text-xs text-slate-300 list-disc list-inside">
                {report.possible_causes?.map((item, idx) => (
                  <li key={idx}>{item}</li>
                ))}
              </ul>
            </div>

            <div className="p-4 rounded-xl bg-slate-800/40 border border-slate-800 space-y-2">
              <h4 className="text-xs font-bold text-rose-400 uppercase tracking-wider flex items-center space-x-1.5">
                <ShieldAlert className="w-4 h-4" />
                <span>Risk Factors</span>
              </h4>
              <ul className="space-y-1 text-xs text-slate-300 list-disc list-inside">
                {report.risk_factors?.map((item, idx) => (
                  <li key={idx}>{item}</li>
                ))}
              </ul>
            </div>
          </div>

          {/* Clinical Precautions & Lifestyle Advice */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-4 rounded-xl bg-slate-800/40 border border-slate-800 space-y-2">
              <h4 className="text-xs font-bold text-emerald-400 uppercase tracking-wider flex items-center space-x-1.5">
                <CheckCircle2 className="w-4 h-4" />
                <span>Clinical Precautions</span>
              </h4>
              <ul className="space-y-1 text-xs text-slate-300 list-disc list-inside">
                {report.precautions?.map((item, idx) => (
                  <li key={idx}>{item}</li>
                ))}
              </ul>
            </div>

            <div className="p-4 rounded-xl bg-slate-800/40 border border-slate-800 space-y-2">
              <h4 className="text-xs font-bold text-sky-400 uppercase tracking-wider">Lifestyle Recommendations</h4>
              <ul className="space-y-1 text-xs text-slate-300 list-disc list-inside">
                {report.lifestyle_advice?.map((item, idx) => (
                  <li key={idx}>{item}</li>
                ))}
              </ul>
            </div>
          </div>

          {/* Recommended Consultation */}
          <div className="p-4 rounded-xl bg-indigo-500/10 border border-indigo-500/30">
            <h4 className="text-xs font-bold text-indigo-400 uppercase tracking-wider mb-1">Recommended Consultation</h4>
            <p className="text-sm font-semibold text-indigo-200">{report.recommended_consultation}</p>
          </div>

          {/* Medical Disclaimer */}
          <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-300 text-xs leading-relaxed space-y-1">
            <span className="font-bold block">Medical Disclaimer</span>
            <p>{report.disclaimer}</p>
          </div>

        </div>

      </div>
    </div>
  );
};

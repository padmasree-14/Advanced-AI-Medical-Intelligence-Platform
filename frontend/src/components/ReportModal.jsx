import React from 'react';
import { FileText, X, Printer, AlertTriangle, CheckCircle2, ShieldAlert, User, Calendar, Stethoscope } from 'lucide-react';

export const ReportModal = ({ report, onClose }) => {
  if (!report) return null;

  const handlePrint = () => {
    window.print();
  };

  const renderSafeList = (items) => {
    if (!items) return <li>None specified</li>;
    if (Array.isArray(items)) {
      return items.map((item, idx) => <li key={idx}>{item}</li>);
    }
    // If LLM returned a string instead of an array, safely render it
    return <li>{String(items)}</li>;
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm overflow-y-auto">
      <div className="relative w-full max-w-4xl glass-panel bg-white border border-slate-200 rounded-2xl shadow-2xl overflow-hidden my-8">
        
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-slate-200 bg-slate-50">
          <div className="flex items-center space-x-3">
            <div className="p-2.5 rounded-xl bg-sky-50 border border-sky-200 text-sky-600">
              <FileText className="w-6 h-6" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-slate-900">AI Clinical Diagnostic Report</h2>
              <p className="text-xs text-slate-500">Automated LLM Synthesis • Patient ID: {report.patient_id || 'P-100234'}</p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <button
              onClick={handlePrint}
              className="flex items-center space-x-1.5 px-3.5 py-2 rounded-lg bg-sky-600 text-white font-semibold text-xs hover:bg-sky-500 transition shadow-sm"
            >
              <Printer className="w-4 h-4" />
              <span>Print Report</span>
            </button>
            <button
              onClick={onClose}
              className="p-2 rounded-lg text-slate-500 hover:text-slate-800 hover:bg-slate-100 transition"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Content Body */}
        <div className="p-6 space-y-6 max-h-[75vh] overflow-y-auto print:max-h-none print:overflow-visible">
          
          {/* Executive Summary */}
          <div className="p-4 rounded-xl bg-sky-50/80 border border-sky-200 space-y-2">
            <h3 className="text-xs font-bold uppercase tracking-wider text-sky-700 flex items-center space-x-1.5">
              <Stethoscope className="w-4 h-4" />
              <span>Clinical Summary</span>
            </h3>
            <p className="text-sm text-slate-800 leading-relaxed font-medium">{report.summary}</p>
          </div>

          {/* Key Diagnostic Findings & Confidence */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-2">
              <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-wider">AI Findings</h4>
              <p className="text-sm text-slate-900 font-semibold">{report.prediction_findings}</p>
            </div>
            <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-2">
              <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Confidence Assessment</h4>
              <p className="text-sm text-slate-900 font-semibold">{report.confidence_assessment}</p>
            </div>
          </div>

          {/* Differential Causes & Risk Factors */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-4 rounded-xl bg-amber-50/60 border border-amber-200 space-y-2">
              <h4 className="text-xs font-bold text-amber-700 uppercase tracking-wider flex items-center space-x-1.5">
                <AlertTriangle className="w-4 h-4" />
                <span>Possible Causes</span>
              </h4>
              <ul className="space-y-1 text-xs text-slate-700 list-disc list-inside">
                {renderSafeList(report.possible_causes)}
              </ul>
            </div>

            <div className="p-4 rounded-xl bg-rose-50/60 border border-rose-200 space-y-2">
              <h4 className="text-xs font-bold text-rose-700 uppercase tracking-wider flex items-center space-x-1.5">
                <ShieldAlert className="w-4 h-4" />
                <span>Risk Factors</span>
              </h4>
              <ul className="space-y-1 text-xs text-slate-700 list-disc list-inside">
                {renderSafeList(report.risk_factors)}
              </ul>
            </div>
          </div>

          {/* Clinical Precautions & Lifestyle Advice */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-4 rounded-xl bg-emerald-50/60 border border-emerald-200 space-y-2">
              <h4 className="text-xs font-bold text-emerald-700 uppercase tracking-wider flex items-center space-x-1.5">
                <CheckCircle2 className="w-4 h-4" />
                <span>Clinical Precautions</span>
              </h4>
              <ul className="space-y-1 text-xs text-slate-700 list-disc list-inside">
                {renderSafeList(report.precautions)}
              </ul>
            </div>

            <div className="p-4 rounded-xl bg-sky-50/60 border border-sky-200 space-y-2">
              <h4 className="text-xs font-bold text-sky-700 uppercase tracking-wider">Lifestyle Recommendations</h4>
              <ul className="space-y-1 text-xs text-slate-700 list-disc list-inside">
                {renderSafeList(report.lifestyle_advice)}
              </ul>
            </div>
          </div>

          {/* Recommended Consultation */}
          <div className="p-4 rounded-xl bg-indigo-50 border border-indigo-200">
            <h4 className="text-xs font-bold text-indigo-700 uppercase tracking-wider mb-1">Recommended Consultation</h4>
            <p className="text-sm font-semibold text-indigo-950">{report.recommended_consultation}</p>
          </div>

          {/* Medical Disclaimer */}
          <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-xs leading-relaxed space-y-1">
            <span className="font-bold block">Medical Disclaimer</span>
            <p>{report.disclaimer}</p>
          </div>

        </div>

      </div>
    </div>
  );
};

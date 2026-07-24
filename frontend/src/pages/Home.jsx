import React from 'react';
import { Link } from 'react-router-dom';
import { Activity, ShieldCheck, Cpu, Eye, FileText, ArrowRight, Zap, Database, Lock } from 'lucide-react';

export const Home = () => {
  return (
    <div className="space-y-24 py-10">
      
      {/* Hero Section */}
      <section className="relative text-center space-y-8 max-w-4xl mx-auto px-4">
        <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-sky-50 border border-sky-200 text-sky-700 text-xs font-semibold uppercase tracking-wider shadow-sm">
          <Zap className="w-3.5 h-3.5" />
          <span>Next-Generation AI Medical Diagnostics</span>
        </div>

        <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight text-slate-900 leading-tight">
          Advanced AI Diagnostic Intelligence for <span className="bg-gradient-to-r from-sky-600 via-indigo-600 to-teal-600 bg-clip-text text-transparent">Radiology & Clinical Care</span>
        </h1>

        <p className="text-slate-600 text-lg sm:text-xl max-w-2xl mx-auto leading-relaxed font-normal">
          Classify chest radiographs with EfficientNet-B0 transfer learning, inspect neural decision regions using Grad-CAM heatmaps, and generate complete LLM clinical reports in seconds.
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
          <Link
            to="/register"
            className="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white font-bold shadow-lg shadow-sky-500/20 flex items-center justify-center space-x-2 transition-all transform hover:-translate-y-0.5"
          >
            <span>Launch Clinical Workspace</span>
            <ArrowRight className="w-5 h-5" />
          </Link>
          <Link
            to="/login"
            className="w-full sm:w-auto px-8 py-3.5 rounded-xl glass-panel hover:bg-slate-100 text-slate-700 font-semibold border border-slate-200 shadow-sm flex items-center justify-center transition"
          >
            Log In to Account
          </Link>
        </div>
      </section>

      {/* Feature Grid */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-2xl sm:text-3xl font-bold text-slate-900">Enterprise Diagnostic Capabilities</h2>
          <p className="text-slate-500 text-sm mt-2">Engineered for precision, explainability, and seamless workflow integration</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="glass-panel glass-panel-hover p-8 rounded-2xl space-y-4">
            <div className="w-12 h-12 rounded-xl bg-sky-50 border border-sky-200 flex items-center justify-center text-sky-600">
              <Cpu className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold text-slate-900">EfficientNet-B0 DL Model</h3>
            <p className="text-slate-600 text-sm leading-relaxed">
              Fine-tuned deep convolutional network delivering high-accuracy multi-class predictions across Normal, Pneumonia, Tuberculosis, and COVID-19.
            </p>
          </div>

          <div className="glass-panel glass-panel-hover p-8 rounded-2xl space-y-4">
            <div className="w-12 h-12 rounded-xl bg-indigo-50 border border-indigo-200 flex items-center justify-center text-indigo-600">
              <Eye className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold text-slate-900">Grad-CAM Visual Heatmaps</h3>
            <p className="text-slate-600 text-sm leading-relaxed">
              Gradient-weighted class activation mapping highlighting specific anatomical regions driving model predictions with interactive intensity sliders.
            </p>
          </div>

          <div className="glass-panel glass-panel-hover p-8 rounded-2xl space-y-4">
            <div className="w-12 h-12 rounded-xl bg-teal-50 border border-teal-200 flex items-center justify-center text-teal-600">
              <FileText className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold text-slate-900">LLM Medical Reports</h3>
            <p className="text-slate-600 text-sm leading-relaxed">
              Automated synthesis using Gemini API generating structured reports with differential causes, precautions, risk factors, and disclaimers.
            </p>
          </div>
        </div>
      </section>

      {/* Tech Stack Banner */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="glass-panel p-8 sm:p-12 rounded-3xl border border-slate-200 bg-white/90 shadow-sm space-y-8">
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
            <div className="space-y-2 max-w-xl">
              <h3 className="text-2xl font-bold text-slate-900">Full-Stack Enterprise Architecture</h3>
              <p className="text-slate-500 text-sm">FastAPI REST Services • Async PyMongo MongoDB Repository • PyTorch Deep Learning • React 18 & Tailwind CSS</p>
            </div>
            <div className="flex items-center space-x-4">
              <div className="px-4 py-2 rounded-xl bg-slate-100 border border-slate-200 text-xs font-mono text-sky-700 font-semibold">
                FastAPI v0.104
              </div>
              <div className="px-4 py-2 rounded-xl bg-slate-100 border border-slate-200 text-xs font-mono text-indigo-700 font-semibold">
                PyTorch v2.1
              </div>
              <div className="px-4 py-2 rounded-xl bg-slate-100 border border-slate-200 text-xs font-mono text-teal-700 font-semibold">
                MongoDB Atlas
              </div>
            </div>
          </div>
        </div>
      </section>

    </div>
  );
};

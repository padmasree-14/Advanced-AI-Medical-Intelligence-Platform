import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import { Upload as UploadIcon, Image as ImageIcon, FileCheck, Activity, AlertCircle, Sparkles } from 'lucide-react';

export const Upload = () => {
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [organSystem, setOrganSystem] = useState("Chest Radiograph");
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleFileChange = (selectedFile) => {
    if (!selectedFile) return;
    if (!selectedFile.type.startsWith('image/')) {
      setError('Please select a valid image file (JPEG, PNG, DICOM-export).');
      return;
    }
    setError('');
    setFile(selectedFile);
    const reader = new FileReader();
    reader.onload = () => setPreviewUrl(reader.result);
    reader.readAsDataURL(selectedFile);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileChange(e.dataTransfer.files[0]);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please upload a medical radiograph scan image.');
      return;
    }

    setUploading(true);
    setError('');

    const formData = new FormData();
    formData.append('file', file);
    formData.append('organ_system', organSystem);

    try {
      const res = await api.post('/predict', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      if (res.data.success) {
        navigate(`/prediction/${res.data.data.id}`, { state: { prediction: res.data.data } });
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Image processing failed. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto py-10 px-4 space-y-8">
      
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-extrabold text-white">Upload Medical Radiograph</h1>
        <p className="text-sm text-slate-400 max-w-xl mx-auto">
          Upload chest radiograph or scan for immediate EfficientNet-B0 classification & Grad-CAM visual heatmap explainability.
        </p>
      </div>

      {error && (
        <div className="p-4 rounded-2xl bg-rose-500/10 border border-rose-500/30 text-rose-400 text-sm flex items-center space-x-2">
          <AlertCircle className="w-5 h-5 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        
        {/* Organ System Selection */}
        <div className="glass-panel p-5 rounded-2xl space-y-2">
          <label className="text-xs font-bold text-slate-300 uppercase tracking-wider">Target Examination Anatomy</label>
          <select
            value={organSystem}
            onChange={(e) => setOrganSystem(e.target.value)}
            className="w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white font-medium text-sm focus:outline-none focus:border-sky-500 transition"
          >
            <option value="Chest Radiograph">Chest Radiograph (PA/AP View)</option>
            <option value="Pulmonary CT Scan">Pulmonary CT Axial Slice</option>
            <option value="Dermatological Lesion">Dermatological Dermoscopy</option>
          </select>
        </div>

        {/* Drag & Drop Upload Zone */}
        <div
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          className={`glass-panel p-10 rounded-3xl border-2 border-dashed transition-all text-center cursor-pointer ${
            file ? 'border-sky-500/80 bg-sky-500/5' : 'border-slate-700 hover:border-sky-500/50'
          }`}
          onClick={() => document.getElementById('file-upload-input').click()}
        >
          <input
            id="file-upload-input"
            type="file"
            accept="image/*"
            className="hidden"
            onChange={(e) => e.target.files && handleFileChange(e.target.files[0])}
          />

          {previewUrl ? (
            <div className="space-y-4">
              <div className="relative w-48 h-48 mx-auto rounded-2xl overflow-hidden border-2 border-sky-500 bg-black shadow-xl">
                <img src={previewUrl} alt="Scan Preview" className="w-full h-full object-contain" />
              </div>
              <div>
                <span className="text-sm font-bold text-sky-400 flex items-center justify-center space-x-1">
                  <FileCheck className="w-4 h-4" />
                  <span>{file.name}</span>
                </span>
                <span className="text-xs text-slate-400 block mt-1">{(file.size / 1024 / 1024).toFixed(2)} MB • Click or drag to replace</span>
              </div>
            </div>
          ) : (
            <div className="space-y-4 py-6">
              <div className="w-16 h-16 rounded-2xl bg-sky-500/20 border border-sky-500/30 flex items-center justify-center mx-auto text-sky-400 shadow-lg shadow-sky-500/20">
                <UploadIcon className="w-8 h-8" />
              </div>
              <div>
                <p className="text-base font-bold text-white">Drag & drop medical image here</p>
                <p className="text-xs text-slate-400 mt-1">Supports PNG, JPEG, DICOM exported files up to 10MB</p>
              </div>
            </div>
          )}
        </div>

        {/* Execute Button */}
        <button
          type="submit"
          disabled={!file || uploading}
          className="w-full py-4 rounded-2xl bg-gradient-to-r from-sky-500 via-indigo-600 to-teal-500 hover:from-sky-400 hover:to-teal-400 text-white font-extrabold text-base shadow-xl shadow-sky-500/25 flex items-center justify-center space-x-2 transition disabled:opacity-50"
        >
          {uploading ? (
            <div className="flex items-center space-x-2">
              <Activity className="w-5 h-5 animate-spin" />
              <span>Analyzing Radiograph with EfficientNet-B0...</span>
            </div>
          ) : (
            <div className="flex items-center space-x-2">
              <Sparkles className="w-5 h-5" />
              <span>Execute AI Diagnostic Analysis</span>
            </div>
          )}
        </button>

      </form>
    </div>
  );
};

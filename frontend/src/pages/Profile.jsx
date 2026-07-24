import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import { User, Shield, Key, Activity, CheckCircle, Mail, Clock } from 'lucide-react';

export const Profile = () => {
  const { user } = useAuth();
  const [profile, setProfile] = useState(user);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const res = await api.get('/profile');
      if (res.data.success) {
        setProfile(res.data.data);
      }
    } catch (err) {
      console.error("Failed to refresh profile", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto py-10 px-4 sm:px-6 lg:px-8 space-y-8">
      
      {/* User Header */}
      <div className="glass-panel p-8 rounded-3xl flex flex-col sm:flex-row items-center space-y-4 sm:space-y-0 sm:space-x-6 border border-slate-200">
        <div className="w-20 h-20 rounded-2xl bg-gradient-to-tr from-sky-500 to-indigo-600 flex items-center justify-center text-white font-bold text-3xl shadow-xl shadow-sky-500/20">
          {profile?.full_name ? profile.full_name.charAt(0) : 'D'}
        </div>
        <div className="text-center sm:text-left space-y-1">
          <h1 className="text-2xl font-extrabold text-slate-900">{profile?.full_name || profile?.username}</h1>
          <p className="text-xs font-semibold text-sky-600 uppercase tracking-wider">{profile?.role || 'Radiologist'}</p>
          <p className="text-xs text-slate-500 flex items-center justify-center sm:justify-start space-x-1 pt-1">
            <Mail className="w-3.5 h-3.5" />
            <span>{profile?.email}</span>
          </p>
        </div>
      </div>

      {/* Profile Details Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        {/* Account Metadata */}
        <div className="glass-panel p-6 rounded-3xl space-y-4">
          <h3 className="text-base font-bold text-white flex items-center space-x-2">
            <User className="w-5 h-5 text-sky-600" />
            <span>Practitioner Identity</span>
          </h3>

          <div className="space-y-3 text-xs">
            <div className="flex justify-between border-b border-slate-200 pb-2">
              <span className="text-slate-500">Username</span>
              <span className="font-mono text-slate-800">{profile?.username}</span>
            </div>
            <div className="flex justify-between border-b border-slate-800 pb-2">
              <span className="text-slate-500">Role Specialty</span>
              <span className="font-semibold text-slate-800 capitalize">{profile?.role}</span>
            </div>
            <div className="flex justify-between border-b border-slate-800 pb-2">
              <span className="text-slate-500">Total Scans Analyzed</span>
              <span className="font-bold text-sky-600">{profile?.total_predictions || 0}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">Account Status</span>
              <span className="font-semibold text-emerald-400 flex items-center space-x-1">
                <CheckCircle className="w-3.5 h-3.5" />
                <span>Active & Verified</span>
              </span>
            </div>
          </div>
        </div>

        {/* System & LLM Status */}
        <div className="glass-panel p-6 rounded-3xl space-y-4">
          <h3 className="text-base font-bold text-white flex items-center space-x-2">
            <Shield className="w-5 h-5 text-indigo-600" />
            <span>AI Platform Configuration</span>
          </h3>

          <div className="space-y-3 text-xs">
            <div className="flex justify-between border-b border-slate-800 pb-2">
              <span className="text-slate-500">Vision Network</span>
              <span className="font-mono text-slate-800">EfficientNet-B0 (PyTorch)</span>
            </div>
            <div className="flex justify-between border-b border-slate-800 pb-2">
              <span className="text-slate-500">Explainable AI</span>
              <span className="font-mono text-slate-800">Grad-CAM (PyTorch Hooks)</span>
            </div>
            <div className="flex justify-between border-b border-slate-800 pb-2">
              <span className="text-slate-500">Report Generator</span>
              <span className="font-mono text-sky-600">Gemini LLM / Mock Provider</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">Database Engine</span>
              <span className="font-mono text-teal-600">Async PyMongo MongoDB</span>
            </div>
          </div>
        </div>

      </div>

    </div>
  );
};

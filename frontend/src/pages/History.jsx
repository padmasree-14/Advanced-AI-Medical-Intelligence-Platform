import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../services/api';
import { History as HistoryIcon, Search, Trash2, Eye, FileText, Activity, AlertCircle } from 'lucide-react';

export const History = () => {
  const [history, setHistory] = useState([]);
  const [filteredHistory, setFilteredHistory] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedClass, setSelectedClass] = useState('ALL');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const res = await api.get('/history');
      if (res.data.success) {
        setHistory(res.data.data);
        setFilteredHistory(res.data.data);
      }
    } catch (err) {
      setError('Failed to fetch prediction history records.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    let result = history;
    if (selectedClass !== 'ALL') {
      result = result.filter(item => item.predicted_class?.toUpperCase() === selectedClass.toUpperCase());
    }
    if (searchQuery.trim() !== '') {
      const q = searchQuery.toLowerCase();
      result = result.filter(item =>
        item.image_name?.toLowerCase().includes(q) ||
        item.predicted_class?.toLowerCase().includes(q) ||
        (item.id || item._id)?.toLowerCase().includes(q)
      );
    }
    setFilteredHistory(result);
  }, [searchQuery, selectedClass, history]);

  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this scan record?")) return;
    try {
      await api.delete(`/history/${id}`);
      setHistory(prev => prev.filter(item => (item.id || item._id) !== id));
    } catch (err) {
      alert("Failed to delete record.");
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="flex items-center space-x-3 text-sky-400">
          <Activity className="w-8 h-8 animate-spin" />
          <span className="font-semibold text-lg">Loading Prediction Vault...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8 space-y-6">
      
      {/* Header & Controls */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 glass-panel p-6 rounded-3xl">
        <div>
          <h1 className="text-2xl font-extrabold text-white flex items-center space-x-2">
            <HistoryIcon className="w-6 h-6 text-sky-400" />
            <span>Diagnostic History Vault</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">Archived medical image classification records & Grad-CAM visual maps</p>
        </div>

        {/* Search & Filter Inputs */}
        <div className="flex flex-col sm:flex-row items-center gap-3">
          <div className="relative w-full sm:w-64">
            <Search className="w-4 h-4 absolute left-3.5 top-3 text-slate-500" />
            <input
              type="text"
              placeholder="Search scans..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 rounded-xl bg-slate-900 border border-slate-700 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-sky-500 transition"
            />
          </div>

          <select
            value={selectedClass}
            onChange={(e) => setSelectedClass(e.target.value)}
            className="w-full sm:w-auto px-4 py-2 rounded-xl bg-slate-900 border border-slate-700 text-xs font-medium text-white focus:outline-none focus:border-sky-500 transition"
          >
            <option value="ALL">All Finding Classes</option>
            <option value="NORMAL">Normal</option>
            <option value="PNEUMONIA">Pneumonia</option>
            <option value="TUBERCULOSIS">Tuberculosis</option>
            <option value="COVID-19">COVID-19</option>
          </select>
        </div>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-400 text-sm flex items-center space-x-2">
          <AlertCircle className="w-5 h-5 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* History Table */}
      <div className="glass-panel p-6 rounded-3xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="text-slate-400 border-b border-slate-800 uppercase font-semibold">
              <tr>
                <th className="pb-3 px-3">Scan Image</th>
                <th className="pb-3 px-3">Scan ID</th>
                <th className="pb-3 px-3">File Name</th>
                <th className="pb-3 px-3">Predicted Class</th>
                <th className="pb-3 px-3">Confidence</th>
                <th className="pb-3 px-3">Timestamp</th>
                <th className="pb-3 px-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-slate-200">
              {filteredHistory.length > 0 ? (
                filteredHistory.map((item) => {
                  const itemId = item.id || item._id;
                  const isNorm = item.predicted_class?.toLowerCase() === 'normal';
                  return (
                    <tr key={itemId} className="hover:bg-slate-800/40 transition">
                      <td className="py-3 px-3">
                        <img src={item.image_url} alt="Thumbnail" className="w-10 h-10 object-cover rounded-lg border border-slate-700 bg-black" />
                      </td>
                      <td className="py-3 px-3 font-mono text-slate-400">{itemId.substring(0, 8)}...</td>
                      <td className="py-3 px-3 font-mono text-slate-200">{item.image_name}</td>
                      <td className="py-3 px-3">
                        <span className={`px-2.5 py-1 rounded-full font-bold ${
                          isNorm ? 'bg-emerald-500/20 text-emerald-400' : 'bg-rose-500/20 text-rose-400'
                        }`}>
                          {item.predicted_class}
                        </span>
                      </td>
                      <td className="py-3 px-3 font-semibold">{item.confidence}%</td>
                      <td className="py-3 px-3 text-slate-400">{new Date(item.created_at).toLocaleString()}</td>
                      <td className="py-3 px-3 text-right space-x-2">
                        <button
                          onClick={() => navigate(`/prediction/${itemId}`, { state: { prediction: item } })}
                          className="px-3 py-1.5 rounded-lg bg-sky-500/10 text-sky-400 border border-sky-500/20 hover:bg-sky-500/20 font-semibold"
                        >
                          View Heatmap
                        </button>
                        <button
                          onClick={() => handleDelete(itemId)}
                          className="p-1.5 rounded-lg text-slate-500 hover:text-rose-400 hover:bg-rose-500/10 transition"
                          title="Delete scan"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </td>
                    </tr>
                  );
                })
              ) : (
                <tr>
                  <td colSpan={7} className="text-center py-10 text-slate-500">
                    No matching scan records found in history.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
};

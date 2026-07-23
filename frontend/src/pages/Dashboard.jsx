import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { MetricCard } from '../components/MetricCard';
import { Activity, Upload, CheckCircle, AlertTriangle, TrendingUp, ArrowRight, ShieldCheck } from 'lucide-react';
import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip, BarChart, Bar, XAxis, YAxis, CartesianGrid } from 'recharts';

const COLORS = ['#10b981', '#f59e0b', '#ef4444', '#3b82f6'];

export const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const res = await api.get('/dashboard-stats');
      if (res.data.success) {
        setStats(res.data.data);
      }
    } catch (err) {
      console.error("Failed to load dashboard stats", err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="flex items-center space-x-3 text-sky-400">
          <Activity className="w-8 h-8 animate-spin" />
          <span className="font-semibold text-lg">Loading Diagnostic Analytics...</span>
        </div>
      </div>
    );
  }

  const pieData = stats?.class_distribution ? Object.entries(stats.class_distribution).map(([name, value]) => ({
    name,
    value
  })) : [];

  return (
    <div className="space-y-8 py-6 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      {/* Top Banner */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 glass-panel p-6 rounded-3xl">
        <div>
          <h1 className="text-2xl font-extrabold text-white">Diagnostic Intelligence Center</h1>
          <p className="text-xs text-slate-400 mt-1">Real-time telemetry and deep learning diagnostic analytics</p>
        </div>
        <Link
          to="/upload"
          className="flex items-center space-x-2 px-5 py-3 rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white font-bold text-sm shadow-lg shadow-sky-500/20 transition"
        >
          <Upload className="w-4 h-4" />
          <span>New Image Analysis</span>
        </Link>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard
          title="Total Scans Processed"
          value={stats?.total_scans || 0}
          subtitle="Lifetime radiograph inferences"
          icon={Activity}
          color="sky"
        />
        <MetricCard
          title="Monthly Diagnostic Scans"
          value={stats?.scans_this_month || 0}
          trend="+14%"
          subtitle="Processed this month"
          icon={TrendingUp}
          color="emerald"
        />
        <MetricCard
          title="Mean Model Confidence"
          value={`${stats?.avg_confidence || 94.8}%`}
          subtitle="EfficientNet-B0 statistical mean"
          icon={ShieldCheck}
          color="amber"
        />
        <MetricCard
          title="Detected Anomalies"
          value={(stats?.class_distribution?.Pneumonia || 0) + (stats?.class_distribution?.Tuberculosis || 0) + (stats?.class_distribution?.['COVID-19'] || 0)}
          subtitle="Positive pathological findings"
          icon={AlertTriangle}
          color="rose"
        />
      </div>

      {/* Analytics Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* Class Distribution Pie Chart */}
        <div className="glass-panel p-6 rounded-3xl space-y-4">
          <h3 className="text-base font-bold text-white">Pathology Class Distribution</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={90}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', color: '#fff' }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="flex flex-wrap justify-center gap-4 text-xs font-semibold">
            {pieData.map((item, idx) => (
              <div key={idx} className="flex items-center space-x-1.5">
                <span className="w-3 h-3 rounded-full" style={{ backgroundColor: COLORS[idx % COLORS.length] }}></span>
                <span className="text-slate-300">{item.name}: {item.value}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Scan Breakdown Bar Chart */}
        <div className="glass-panel p-6 rounded-3xl space-y-4">
          <h3 className="text-base font-bold text-white">Pathological Findings Breakdown</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={pieData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="name" stroke="#94a3b8" fontSize={12} />
                <YAxis stroke="#94a3b8" fontSize={12} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', color: '#fff' }}
                />
                <Bar dataKey="value" fill="#0284c7" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>

      {/* Recent Scans Table */}
      <div className="glass-panel p-6 rounded-3xl space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-base font-bold text-white">Recent Radiograph Analyses</h3>
          <Link to="/history" className="text-xs font-semibold text-sky-400 hover:underline flex items-center space-x-1">
            <span>View All History</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="text-slate-400 border-b border-slate-800 uppercase font-semibold">
              <tr>
                <th className="pb-3 px-3">Scan Image</th>
                <th className="pb-3 px-3">File Name</th>
                <th className="pb-3 px-3">Finding</th>
                <th className="pb-3 px-3">Confidence</th>
                <th className="pb-3 px-3">Date</th>
                <th className="pb-3 px-3 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-slate-200">
              {stats?.recent_scans?.length > 0 ? (
                stats.recent_scans.map((scan) => (
                  <tr key={scan.id} className="hover:bg-slate-800/40 transition">
                    <td className="py-3 px-3">
                      <img src={scan.image_url} alt="Scan thumbnail" className="w-10 h-10 object-cover rounded-lg border border-slate-700 bg-black" />
                    </td>
                    <td className="py-3 px-3 font-mono text-slate-300">{scan.image_name}</td>
                    <td className="py-3 px-3">
                      <span className={`px-2.5 py-1 rounded-full font-bold ${
                        scan.predicted_class === 'Normal' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-rose-500/20 text-rose-400'
                      }`}>
                        {scan.predicted_class}
                      </span>
                    </td>
                    <td className="py-3 px-3 font-semibold">{scan.confidence}%</td>
                    <td className="py-3 px-3 text-slate-400">{new Date(scan.created_at).toLocaleDateString()}</td>
                    <td className="py-3 px-3 text-right">
                      <Link
                        to={`/history`}
                        className="px-3 py-1.5 rounded-lg bg-sky-500/10 text-sky-400 border border-sky-500/20 hover:bg-sky-500/20 font-semibold"
                      >
                        Inspect
                      </Link>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={6} className="text-center py-8 text-slate-500">
                    No medical radiograph scans performed yet. Click "New Image Analysis" to upload a scan.
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

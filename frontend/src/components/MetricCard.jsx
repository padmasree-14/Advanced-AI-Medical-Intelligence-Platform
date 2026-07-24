import React from 'react';

export const MetricCard = ({ title, value, subtitle, icon: Icon, trend, color = 'sky' }) => {
  const colorMap = {
    sky: 'from-sky-50 to-indigo-50/50 border-sky-200 text-sky-600',
    emerald: 'from-emerald-50 to-teal-50/50 border-emerald-200 text-emerald-600',
    amber: 'from-amber-50 to-orange-50/50 border-amber-200 text-amber-600',
    rose: 'from-rose-50 to-red-50/50 border-rose-200 text-rose-600',
  };

  return (
    <div className={`glass-panel p-5 rounded-2xl border bg-gradient-to-br ${colorMap[color] || colorMap.sky} transition-all`}>
      <div className="flex items-center justify-between">
        <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">{title}</span>
        {Icon && <Icon className="w-5 h-5 opacity-90" />}
      </div>
      <div className="mt-3 flex items-baseline justify-between">
        <span className="text-3xl font-extrabold text-slate-900">{value}</span>
        {trend && (
          <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-700">
            {trend}
          </span>
        )}
      </div>
      {subtitle && <p className="text-xs text-slate-500 mt-1">{subtitle}</p>}
    </div>
  );
};

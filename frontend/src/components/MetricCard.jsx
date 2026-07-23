import React from 'react';

export const MetricCard = ({ title, value, subtitle, icon: Icon, trend, color = 'sky' }) => {
  const colorMap = {
    sky: 'from-sky-500/20 to-indigo-500/10 border-sky-500/30 text-sky-400',
    emerald: 'from-emerald-500/20 to-teal-500/10 border-emerald-500/30 text-emerald-400',
    amber: 'from-amber-500/20 to-orange-500/10 border-amber-500/30 text-amber-400',
    rose: 'from-rose-500/20 to-red-500/10 border-rose-500/30 text-rose-400',
  };

  return (
    <div className={`glass-panel p-5 rounded-2xl border bg-gradient-to-br ${colorMap[color] || colorMap.sky} transition-all`}>
      <div className="flex items-center justify-between">
        <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">{title}</span>
        {Icon && <Icon className="w-5 h-5 opacity-90" />}
      </div>
      <div className="mt-3 flex items-baseline justify-between">
        <span className="text-3xl font-extrabold text-white">{value}</span>
        {trend && (
          <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-slate-800/80 text-emerald-400">
            {trend}
          </span>
        )}
      </div>
      {subtitle && <p className="text-xs text-slate-400 mt-1">{subtitle}</p>}
    </div>
  );
};

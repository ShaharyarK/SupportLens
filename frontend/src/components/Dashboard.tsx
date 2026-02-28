import React, { useState, useEffect } from 'react';
import { format } from 'date-fns';
import {
    BarChart3, Clock, MessageSquare, Filter, ChevronDown, ChevronRight, Activity
} from 'lucide-react';
import { api } from '../api';
import type { Trace, Analytics } from '../types';

const categoryColors: Record<string, string> = {
    'Billing': 'bg-blue-100 text-blue-700 border-blue-200',
    'Refund': 'bg-red-100 text-red-700 border-red-200',
    'Account Access': 'bg-amber-100 text-amber-700 border-amber-200',
    'Cancellation': 'bg-orange-100 text-orange-700 border-orange-200',
    'General Inquiry': 'bg-emerald-100 text-emerald-700 border-emerald-200'
};

const defaultColor = 'bg-slate-100 text-slate-700 border-slate-200';

export const Dashboard: React.FC<{ refreshKey: number }> = ({ refreshKey }) => {
    const [traces, setTraces] = useState<Trace[]>([]);
    const [analytics, setAnalytics] = useState<Analytics | null>(null);
    const [filter, setFilter] = useState('');
    const [expandedId, setExpandedId] = useState<string | null>(null);

    const loadData = async () => {
        try {
            const [t, a] = await Promise.all([
                api.getTraces(filter || undefined),
                api.getAnalytics()
            ]);
            setTraces(t);
            setAnalytics(a);
        } catch (e) {
            console.error(e);
        }
    };

    useEffect(() => {
        loadData();
    }, [filter, refreshKey]);

    return (
        <div className="flex flex-col h-full bg-slate-50/50 rounded-2xl overflow-hidden shadow-[inset_0_2px_10px_rgba(0,0,0,0.02)]">
            {/* Analytics Header */}
            <div className="p-6 border-b border-slate-200 bg-white shadow-sm z-10">
                <h1 className="text-2xl font-bold text-slate-800 mb-6 flex items-center">
                    <Activity className="mr-3 text-indigo-600" /> Observability Dashboard
                </h1>

                {analytics && (
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div className="bg-gradient-to-br from-indigo-50 to-white p-5 rounded-xl border border-indigo-100 shadow-sm flex items-center justify-between transition-transform hover:-translate-y-1 duration-200">
                            <div>
                                <p className="text-indigo-600 font-medium text-sm mb-1 uppercase tracking-wider">Total Traces</p>
                                <p className="text-3xl font-bold text-slate-800">{analytics.total_traces}</p>
                            </div>
                            <div className="bg-indigo-100 p-3 rounded-full text-indigo-600">
                                <MessageSquare size={24} />
                            </div>
                        </div>

                        <div className="bg-gradient-to-br from-emerald-50 to-white p-5 rounded-xl border border-emerald-100 shadow-sm flex items-center justify-between transition-transform hover:-translate-y-1 duration-200">
                            <div>
                                <p className="text-emerald-600 font-medium text-sm mb-1 uppercase tracking-wider">Avg Response</p>
                                <p className="text-3xl font-bold text-slate-800">{analytics.average_response_time_ms}<span className="text-lg text-slate-500 font-medium ml-1">ms</span></p>
                            </div>
                            <div className="bg-emerald-100 p-3 rounded-full text-emerald-600">
                                <Clock size={24} />
                            </div>
                        </div>

                        <div className="bg-gradient-to-br from-violet-50 to-white p-5 rounded-xl border border-violet-100 shadow-sm flex flex-col justify-center transition-transform hover:-translate-y-1 duration-200">
                            <div className="flex items-center justify-between mb-2 pb-2 border-b border-violet-100">
                                <p className="text-violet-600 font-medium text-sm uppercase tracking-wider flex items-center"><BarChart3 size={16} className="mr-2" /> Categories</p>
                            </div>
                            <div className="space-y-1.5 h-[60px] overflow-y-auto pr-1 custom-scrollbar">
                                {analytics.category_breakdown.map(c => (
                                    <div key={c.category} className="flex justify-between items-center text-sm">
                                        <span className="text-slate-600 truncate mr-2" title={c.category}>{c.category}</span>
                                        <div className="flex items-center">
                                            <span className="font-semibold text-slate-800 w-6 text-right">{c.count}</span>
                                            <span className="text-slate-400 text-xs w-10 text-right ml-1">({c.percentage}%)</span>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                )}
            </div>

            {/* Trace List */}
            <div className="flex-1 overflow-hidden flex flex-col">
                <div className="px-6 py-4 flex justify-between items-center bg-white border-b border-slate-100">
                    <h2 className="text-lg font-semibold text-slate-800">Recent Traces</h2>
                    <div className="flex items-center space-x-2 bg-slate-50 border border-slate-200 rounded-lg p-1">
                        <Filter size={16} className="text-slate-400 ml-2" />
                        <select
                            value={filter}
                            onChange={(e) => setFilter(e.target.value)}
                            className="bg-transparent border-none text-sm text-slate-700 outline-none pr-3 py-1.5 cursor-pointer appearance-none hover:text-slate-900 focus:ring-0"
                            style={{ paddingRight: '10px' }}
                        >
                            <option value="">All Categories</option>
                            {Object.keys(categoryColors).map(cat => (
                                <option key={cat} value={cat}>{cat}</option>
                            ))}
                        </select>
                    </div>
                </div>

                <div className="flex-1 overflow-y-auto bg-slate-50 p-6 custom-scrollbar">
                    <div className="space-y-3">
                        {traces.map((trace) => {
                            const isExpanded = expandedId === trace.id;
                            const badgeColor = categoryColors[trace.category] || defaultColor;

                            return (
                                <div
                                    key={trace.id}
                                    className={`bg-white rounded-xl border transition-all duration-200 shadow-sm overflow-hidden ${isExpanded ? 'border-indigo-300 ring-1 ring-indigo-100 shadow-md' : 'border-slate-200 hover:border-indigo-200 hover:shadow-md'}`}
                                >
                                    <div
                                        className="p-4 cursor-pointer flex items-center justify-between gap-4"
                                        onClick={() => setExpandedId(isExpanded ? null : trace.id)}
                                    >
                                        <div className="flex-shrink-0 text-slate-400">
                                            {isExpanded ? <ChevronDown size={20} /> : <ChevronRight size={20} />}
                                        </div>

                                        <div className="flex-1 min-w-0 flex flex-col sm:flex-row gap-2 sm:gap-6 sm:items-center">
                                            <div className="w-full sm:w-1/3 text-sm truncate font-medium text-slate-800">
                                                {trace.user_message}
                                            </div>
                                            <div className="w-full sm:w-1/2 text-sm truncate text-slate-500">
                                                {trace.bot_response}
                                            </div>
                                        </div>

                                        <div className="flex-shrink-0 flex items-center space-x-4">
                                            <span className={`px-2.5 py-1 text-xs font-semibold rounded-full border whitespace-nowrap ${badgeColor}`}>
                                                {trace.category}
                                            </span>
                                            <div className="hidden md:flex flex-col text-right">
                                                <span className="text-xs text-slate-400 font-medium">
                                                    {format(new Date(trace.timestamp), 'MMM d, HH:mm')}
                                                </span>
                                                <span className="text-xs text-slate-400">
                                                    {trace.response_time_ms} ms
                                                </span>
                                            </div>
                                        </div>
                                    </div>

                                    {isExpanded && (
                                        <div className="px-5 py-4 bg-slate-50/80 border-t border-slate-100 space-y-4">
                                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                                <div className="bg-white p-4 rounded-lg border border-slate-200 shadow-sm relative">
                                                    <span className="absolute -top-2.5 left-3 bg-white px-2 text-[10px] font-bold tracking-wider text-indigo-500 uppercase rounded">User</span>
                                                    <p className="text-sm text-slate-700 whitespace-pre-wrap leading-relaxed mt-1">{trace.user_message}</p>
                                                </div>
                                                <div className="bg-white p-4 rounded-lg border border-slate-200 shadow-sm relative">
                                                    <span className="absolute -top-2.5 left-3 bg-white px-2 text-[10px] font-bold tracking-wider text-emerald-500 uppercase rounded">Bot Response</span>
                                                    <p className="text-sm text-slate-700 whitespace-pre-wrap leading-relaxed mt-1">{trace.bot_response}</p>
                                                </div>
                                            </div>
                                            <div className="flex text-xs text-slate-500 space-x-6 justify-end bg-slate-100/50 p-2 rounded border border-slate-200">
                                                <span><span className="font-semibold text-slate-600">ID:</span> {trace.id}</span>
                                                <span><span className="font-semibold text-slate-600">Time:</span> {format(new Date(trace.timestamp), 'MMM d, yyyy HH:mm:ss')}</span>
                                                <span><span className="font-semibold text-slate-600">Latency:</span> {trace.response_time_ms}ms</span>
                                            </div>
                                        </div>
                                    )}
                                </div>
                            );
                        })}

                        {traces.length === 0 && (
                            <div className="text-center py-16 bg-white rounded-xl border border-slate-200 border-dashed">
                                <MessageSquare className="mx-auto h-12 w-12 text-slate-300 mb-3" />
                                <h3 className="text-lg font-medium text-slate-900">No traces found</h3>
                                <p className="text-slate-500 text-sm mt-1">Start chatting to see results here.</p>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Loader2 } from 'lucide-react';
import { api } from '../api';

interface Message {
    id: string;
    role: 'user' | 'bot';
    content: string;
}

export const Chat: React.FC<{ onTraceAdded: () => void }> = ({ onTraceAdded }) => {
    const [messages, setMessages] = useState<Message[]>([
        { id: '1', role: 'bot', content: 'Hi there! I am the SupportLens assistant. How can I help you today?' }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const scrollRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [messages]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim() || isLoading) return;

        const userMsg = input.trim();
        setInput('');
        setMessages(prev => [...prev, { id: Date.now().toString(), role: 'user', content: userMsg }]);
        setIsLoading(true);

        try {
            const { response } = await api.chat(userMsg);
            setMessages(prev => [...prev, { id: Date.now().toString() + 'bot', role: 'bot', content: response }]);
            onTraceAdded();
        } catch (error) {
            console.error(error);
            setMessages(prev => [...prev, { id: Date.now().toString() + 'err', role: 'bot', content: 'Sorry, I encountered an error. Please try again later.' }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-full bg-white rounded-2xl shadow-xl border border-slate-100 overflow-hidden">
            <div className="bg-gradient-to-r from-blue-600 to-indigo-700 p-5 text-white flex items-center space-x-3 shadow-sm z-10">
                <div className="bg-white/20 p-2 rounded-lg backdrop-blur-sm">
                    <Bot size={24} className="text-white" />
                </div>
                <div>
                    <h2 className="font-semibold text-lg leading-tight">SupportLens AI</h2>
                    <p className="text-blue-100 text-xs">Customer Service</p>
                </div>
            </div>

            <div className="flex-1 overflow-y-auto p-5 space-y-4 bg-slate-50 relative" ref={scrollRef}>
                {messages.map(msg => (
                    <div key={msg.id} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`flex max-w-[85%] ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'} items-end gap-2`}>
                            <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 shadow-sm ${msg.role === 'user' ? 'bg-indigo-100 text-indigo-700' : 'bg-white border border-slate-200 text-slate-700'}`}>
                                {msg.role === 'user' ? <User size={16} /> : <Bot size={16} />}
                            </div>
                            <div className={`p-3.5 rounded-2xl text-[15px] leading-relaxed shadow-sm ${msg.role === 'user'
                                    ? 'bg-indigo-600 text-white rounded-br-sm'
                                    : 'bg-white border border-slate-100 text-slate-800 rounded-bl-sm'
                                }`}>
                                {msg.content}
                            </div>
                        </div>
                    </div>
                ))}
                {isLoading && (
                    <div className="flex justify-start">
                        <div className="flex max-w-[85%] flex-row items-end gap-2">
                            <div className="w-8 h-8 rounded-full flex items-center justify-center shrink-0 shadow-sm bg-white border border-slate-200 text-slate-700">
                                <Bot size={16} />
                            </div>
                            <div className="p-4 rounded-2xl bg-white border border-slate-100 shadow-sm rounded-bl-sm flex space-x-2">
                                <div className="w-2 h-2 bg-slate-300 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
                                <div className="w-2 h-2 bg-slate-300 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
                                <div className="w-2 h-2 bg-slate-300 rounded-full animate-bounce"></div>
                            </div>
                        </div>
                    </div>
                )}
            </div>

            <div className="p-4 bg-white border-t border-slate-100">
                <form onSubmit={handleSubmit} className="flex relative items-center">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Type your message..."
                        className="flex-1 bg-slate-100 border-transparent focus:bg-white focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 rounded-full py-3.5 pl-5 pr-14 outline-none transition-all duration-200 text-slate-800 placeholder-slate-400"
                    />
                    <button
                        type="submit"
                        disabled={!input.trim() || isLoading}
                        className="absolute right-2 p-2 bg-indigo-600 text-white rounded-full hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-md"
                    >
                        {isLoading ? <Loader2 size={18} className="animate-spin" /> : <Send size={18} className="ml-0.5" />}
                    </button>
                </form>
            </div>
        </div>
    );
};

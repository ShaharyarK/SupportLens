import type { Trace, Analytics } from './types'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const api = {
    chat: async (message: string): Promise<{ response: string }> => {
        const res = await fetch(`${API_URL}/api/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message }),
        })
        if (!res.ok) throw new Error('API Error')
        return res.json()
    },
    getTraces: async (category?: string): Promise<Trace[]> => {
        const url = category ? `${API_URL}/api/traces?category=${encodeURIComponent(category)}` : `${API_URL}/api/traces`
        const res = await fetch(url)
        if (!res.ok) throw new Error('API Error')
        return res.json()
    },
    getAnalytics: async (): Promise<Analytics> => {
        const res = await fetch(`${API_URL}/api/analytics`)
        if (!res.ok) throw new Error('API Error')
        return res.json()
    }
}

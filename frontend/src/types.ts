export interface Trace {
    id: string;
    user_message: string;
    bot_response: string;
    category: string;
    timestamp: string;
    response_time_ms: number;
}

export interface CategoryStat {
    category: string;
    count: number;
    percentage: number;
}

export interface Analytics {
    total_traces: number;
    category_breakdown: CategoryStat[];
    average_response_time_ms: number;
}

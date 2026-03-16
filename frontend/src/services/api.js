/**
 * API Service Layer
 * Handles all backend communication
 */

const API_URL = import.meta.env.VITE_API_URL || 'https://tibby-backend.onrender.com';

/**
 * Send a chat message to the backend
 * @param {string} message - The user's message
 * @returns {Promise<{reply: string, confidence: number, cached: boolean}>}
 */
export async function sendChatMessage(message) {
    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message }),
        });

        if (!response.ok) {
            // Try to get the friendly message the backend sends in 'reply'
            let friendlyMsg = 'Something went wrong. Please try again.';
            try {
                const data = await response.json();
                if (data.reply) friendlyMsg = data.reply;
            } catch (_) { /* ignore parse errors */ }

            if (response.status === 429) {
                throw new Error('⏳ Too many requests. Please wait a moment before trying again.');
            }
            throw new Error(friendlyMsg);
        }

        const data = await response.json();
        // Guard: ensure reply is always a string
        if (!data.reply) data.reply = '🐾 I received your message but had trouble forming a response. Please try again!';
        return data;
    } catch (error) {
        if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
            throw new Error('📶 Unable to connect to the server. Please check your internet connection.');
        }
        throw error;
    }
}

/**
 * Get health status from backend
 * @returns {Promise<{status: string, intents_loaded: number}>}
 */
export async function getHealth() {
    try {
        const response = await fetch(`${API_URL}/health`);
        if (!response.ok) throw new Error('Health check failed');
        return await response.json();
    } catch (error) {
        console.error('Health check error:', error);
        return { status: 'error', intents_loaded: 0 };
    }
}

/**
 * Get chatbot statistics
 * @returns {Promise<Object>}
 */
export async function getStats() {
    try {
        const response = await fetch(`${API_URL}/stats`);
        if (!response.ok) throw new Error('Stats fetch failed');
        return await response.json();
    } catch (error) {
        console.error('Stats fetch error:', error);
        return null;
    }
}

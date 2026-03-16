/**
 * API Service Layer
 * Handles all backend communication
 */

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

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
            if (response.status === 429) {
                throw new Error('Too many requests. Please wait a moment.');
            }
            if (response.status === 400) {
                const data = await response.json();
                throw new Error(data.error || 'Invalid request');
            }
            throw new Error('Failed to send message');
        }

        return await response.json();
    } catch (error) {
        if (error.message.includes('Failed to fetch')) {
            throw new Error('Unable to connect to server. Please check your connection.');
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

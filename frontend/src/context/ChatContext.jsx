import React, { createContext, useContext, useReducer, useCallback } from 'react';
import { sendChatMessage } from '../services/api';
import { useLocalStorage } from '../hooks/useLocalStorage';

const ChatContext = createContext();

// Action types
const ACTIONS = {
    ADD_MESSAGE: 'ADD_MESSAGE',
    SET_LOADING: 'SET_LOADING',
    SET_ERROR: 'SET_ERROR',
    SET_INPUT: 'SET_INPUT',
    CLEAR_CHAT: 'CLEAR_CHAT',
    LOAD_HISTORY: 'LOAD_HISTORY',
};

// Reducer
function chatReducer(state, action) {
    switch (action.type) {
        case ACTIONS.ADD_MESSAGE:
            return {
                ...state,
                messages: [...state.messages, action.payload],
                error: null,
            };
        case ACTIONS.SET_LOADING:
            return {
                ...state,
                isLoading: action.payload,
            };
        case ACTIONS.SET_ERROR:
            return {
                ...state,
                error: action.payload,
                isLoading: false,
            };
        case ACTIONS.SET_INPUT:
            return {
                ...state,
                inputValue: action.payload,
            };
        case ACTIONS.CLEAR_CHAT:
            return {
                ...state,
                messages: [],
                error: null,
            };
        case ACTIONS.LOAD_HISTORY:
            return {
                ...state,
                messages: action.payload,
            };
        default:
            return state;
    }
}

// Initial state
const initialState = {
    messages: [],
    isLoading: false,
    error: null,
    inputValue: '',
};

export function ChatProvider({ children }) {
    const [state, dispatch] = useReducer(chatReducer, initialState);
    const [, setStoredMessages] = useLocalStorage('chat-history', []);

    // Load history on mount
    React.useEffect(() => {
        const stored = localStorage.getItem('chat-history');
        if (stored) {
            try {
                const messages = JSON.parse(stored);
                dispatch({ type: ACTIONS.LOAD_HISTORY, payload: messages });
            } catch (error) {
                console.error('Error loading chat history:', error);
            }
        }
    }, []);

    // Save messages to localStorage whenever they change
    React.useEffect(() => {
        if (state.messages.length > 0) {
            setStoredMessages(state.messages);
        }
    }, [state.messages, setStoredMessages]);

    const sendMessage = useCallback(async (text) => {
        if (!text.trim()) return;

        const userMessage = {
            id: Date.now().toString(),
            text: text.trim(),
            sender: 'user',
            timestamp: new Date(),
        };

        dispatch({ type: ACTIONS.ADD_MESSAGE, payload: userMessage });
        dispatch({ type: ACTIONS.SET_LOADING, payload: true });
        dispatch({ type: ACTIONS.SET_INPUT, payload: '' });

        try {
            const response = await sendChatMessage(text.trim());

            const botMessage = {
                id: (Date.now() + 1).toString(),
                text: response.reply,
                sender: 'bot',
                timestamp: new Date(),
                confidence: response.confidence,
                cached: response.cached,
            };

            dispatch({ type: ACTIONS.ADD_MESSAGE, payload: botMessage });
        } catch (error) {
            dispatch({ type: ACTIONS.SET_ERROR, payload: error.message });

            const errorMessage = {
                id: (Date.now() + 1).toString(),
                text: error.message && !error.message.includes('undefined')
                    ? error.message
                    : '🐾 Oops! Something went wrong. Please try again in a moment.',
                sender: 'bot',
                timestamp: new Date(),
                isError: true,
            };

            dispatch({ type: ACTIONS.ADD_MESSAGE, payload: errorMessage });
        } finally {
            dispatch({ type: ACTIONS.SET_LOADING, payload: false });
        }
    }, []);

    const clearChat = useCallback(() => {
        dispatch({ type: ACTIONS.CLEAR_CHAT });
        localStorage.removeItem('chat-history');
    }, []);

    const setInputValue = useCallback((value) => {
        dispatch({ type: ACTIONS.SET_INPUT, payload: value });
    }, []);

    const value = {
        messages: state.messages,
        isLoading: state.isLoading,
        error: state.error,
        inputValue: state.inputValue,
        sendMessage,
        clearChat,
        setInputValue,
    };

    return <ChatContext.Provider value={value}>{children}</ChatContext.Provider>;
}

export function useChat() {
    const context = useContext(ChatContext);
    if (!context) {
        throw new Error('useChat must be used within a ChatProvider');
    }
    return context;
}

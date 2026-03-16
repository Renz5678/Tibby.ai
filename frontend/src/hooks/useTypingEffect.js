import { useState, useEffect } from 'react';

/**
 * Custom hook for typing effect animation
 * @param {string} text - Full text to display
 * @param {number} speed - Typing speed in milliseconds
 * @returns {string} - Currently displayed text
 */
export function useTypingEffect(text, speed = 30) {
    const [displayedText, setDisplayedText] = useState('');

    useEffect(() => {
        if (!text) {
            setDisplayedText('');
            return;
        }

        let index = 0;
        setDisplayedText('');

        const interval = setInterval(() => {
            if (index < text.length) {
                setDisplayedText((prev) => prev + text.charAt(index));
                index++;
            } else {
                clearInterval(interval);
            }
        }, speed);

        return () => clearInterval(interval);
    }, [text, speed]);

    return displayedText;
}

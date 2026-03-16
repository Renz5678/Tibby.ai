import { useState, useEffect } from 'react';

/**
 * Custom hook for typing effect animation.
 * Uses Array.from() to correctly iterate Unicode code points,
 * preventing emoji/multi-byte characters from being split mid-animation.
 *
 * @param {string} text  - Full text to display
 * @param {number} speed - Typing speed in milliseconds per character
 * @returns {string}     - Currently displayed text
 */
export function useTypingEffect(text, speed = 30) {
    const [displayedText, setDisplayedText] = useState('');

    useEffect(() => {
        if (!text) {
            setDisplayedText('');
            return;
        }

        // Array.from splits by Unicode code points (not UTF-16 code units),
        // so emojis and other multi-byte chars are treated as single units.
        const chars = Array.from(text);
        let index = 0;
        setDisplayedText('');

        const interval = setInterval(() => {
            if (index < chars.length) {
                setDisplayedText((prev) => prev + chars[index]);
                index++;
            } else {
                clearInterval(interval);
            }
        }, speed);

        return () => clearInterval(interval);
    }, [text, speed]);

    return displayedText;
}

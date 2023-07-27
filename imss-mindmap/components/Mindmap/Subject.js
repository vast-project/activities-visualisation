/**
 * Get the center subject of the mindmap
 * @param isItalian Whether the mindmap is in Italian or English
 * @returns {string} The center subject
 */
export const getCenterSubject = function (isItalian) {
    return isItalian ? "Uguaglianza tra i popoli" : "Equality among people";
}

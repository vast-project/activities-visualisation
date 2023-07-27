const backendUrl = "https://activities-backend.vast-project.eu";
// const backendUrl = "http://localhost:8000";

/**
 * Save visitor data to the backend
 * @param visitorData - the data to be saved
 * @returns {Promise<Response>}
 */
export const saveVisitor = async function (visitorData) {
    // Send the POST request
    return fetch(backendUrl + '/rest/visitors/', {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(visitorData),
    }).then(response => {
        if (!response.ok) {
            throw new Error(`Error! Status: ${response.status}`);
        }
        console.log("Visitor created successfully");
    }).catch(error => {
        console.error("Error:", error);
    });
}

/**
 * Save mindmap data to the backend
 * @param data - the data to be saved
 * @returns {Promise<Response>}
 */
export const saveMindmap = async function (data) {
    const url = backendUrl + "/api/save-statements";

    console.log("Saving mindmap", JSON.stringify(data));
    return fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    }).then(response => {
        if (!response.ok) {
            throw new Error(`Error! Status: ${response.status}`);
        }
        console.log("Form data submitted successfully");
    }).catch(error => {
        console.error("Form data submission failed:", error);
    });
}

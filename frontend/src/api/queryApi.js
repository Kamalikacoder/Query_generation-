const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || "").trim().replace(/\/$/, "");

function buildUrl(path) {
  return API_BASE_URL ? `${API_BASE_URL}${path}` : path;
}

export async function generateQuery(claim) {
  try {
    const response = await fetch(buildUrl("/generate-query"), {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ claim }),
    });

    const rawText = await response.text();
    let payload = {};

    try {
      payload = rawText ? JSON.parse(rawText) : {};
    } catch {
      payload = {};
    }

    if (!response.ok) {
      const detail = Array.isArray(payload.detail) ? payload.detail[0]?.msg : payload.message;
      throw new Error(
        detail ||
          `Backend request failed with status ${response.status}. Make sure backend is running and /generate-query is available.`,
      );
    }

    return payload;
  } catch (error) {
    if (error instanceof TypeError) {
      throw new Error(
        "Backend connection failed. Make sure the FastAPI server is running on http://127.0.0.1:8000.",
      );
    }

    throw error;
  }
}

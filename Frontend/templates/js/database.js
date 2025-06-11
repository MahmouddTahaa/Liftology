const API_BASE_URL = "https://liftologybackend-production.up.railway.app";

// User functions
async function createUser({ email, password }) {
  try {
    const response = await fetch(`${API_BASE_URL}/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Failed to register user");
    }

    return await response.json();
  } catch (error) {
    console.error("Error creating user:", error);
    return null;
  }
}

async function loginUser({ email, password }) {
  try {
    const response = await fetch(`${API_BASE_URL}/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Failed to login");
    }

    return await response.json();
  } catch (error) {
    console.error("Error logging in:", error);
    return null;
  }
}

async function updateUserPlan(token, planData) {
  try {
    const response = await fetch(`${API_BASE_URL}/user/plan`, {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(planData),
    });

    return response.ok;
  } catch (error) {
    console.error("Error updating user plan:", error);
    return false;
  }
}

export { createUser, loginUser, updateUserPlan };

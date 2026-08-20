import React, { useState } from "react";

function App() {
  const [prompt, setPrompt] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  async function runAgent() {
    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/api/agents/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt, agent_name: "support_agent" }),
      });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  }

  return (
    <div style={{ padding: "20px", maxWidth: "900px", margin: "0 auto" }}>
      <h1>🛡️ AI Agent Governance Dashboard</h1>

      <textarea
        rows="6"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Try: What is your return policy?"
        style={{ width: "100%", padding: "10px" }}
      />

      <button onClick={runAgent} disabled={loading} style={{ marginTop: "10px", padding: "10px 20px" }}>
        {loading ? "Running..." : "Run Agent"}
      </button>

      {result && (
        <div style={{ marginTop: "20px" }}>
          <h3>Response</h3>
          <p>{result.response}</p>
          <p>Status: {result.blocked ? "BLOCKED" : "COMPLETED"}</p>

          <h3>Violations</h3>
          <pre>{JSON.stringify(result.violations, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;

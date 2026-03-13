import React from "react";
export default function JLLOnboardingPortal() {
  const [formData, setFormData] = React.useState({
    role_title: "Facilities Manager",
    is_manager: "Yes",
    function: "Facilities",
    region: "EMEA",
    country: "UK",
    device_platform: "Windows",
    ram: 16,
    installed_app_count: 25,
  });

  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState("");
  const [result, setResult] = React.useState(null);

  const backendUrl = "http://127.0.0.1:8000/onboard_employee";

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === "ram" || name === "installed_app_count" ? Number(value) : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(backendUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const text = await response.text();
        throw new Error(text || "Failed to generate onboarding plan.");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  const fieldClass =
    "mt-2 w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm shadow-sm outline-none transition focus:border-slate-400";

  return (
    <div className="min-h-screen bg-slate-50 p-6 md:p-10">
      <div className="mx-auto max-w-7xl">
        <div className="mb-8 flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
          <div>
            <p className="text-sm font-medium uppercase tracking-[0.2em] text-slate-500">
              JLL MVP
            </p>
            <h1 className="mt-2 text-3xl font-semibold tracking-tight text-slate-900 md:text-4xl">
              AI Onboarding Portal
            </h1>
            <p className="mt-3 max-w-2xl text-sm text-slate-600 md:text-base">
              Predict application bundles, generate provisioning recommendations, and explain the onboarding plan using your multi-agent backend.
            </p>
          </div>
          <div className="rounded-2xl bg-white px-4 py-3 shadow-sm ring-1 ring-slate-200">
            <div className="text-xs uppercase tracking-wide text-slate-500">Backend Endpoint</div>
            <div className="mt-1 text-sm font-medium text-slate-800">{backendUrl}</div>
          </div>
        </div>

        <div className="grid grid-cols-1 gap-6 lg:grid-cols-5">
          <div className="lg:col-span-2">
            <div className="rounded-3xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
              <h2 className="text-xl font-semibold text-slate-900">Employee Intake</h2>
              <p className="mt-2 text-sm text-slate-600">
                Enter the employee profile to generate a persona, bundle recommendation, application list, and onboarding explanation.
              </p>

              <form className="mt-6 space-y-5" onSubmit={handleSubmit}>
                <div>
                  <label className="text-sm font-medium text-slate-700">Job Title</label>
                  <input
                    className={fieldClass}
                    name="role_title"
                    value={formData.role_title}
                    onChange={handleChange}
                    placeholder="e.g. Building Operations Manager"
                  />
                </div>

                <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
                  <div>
                    <label className="text-sm font-medium text-slate-700">Is Manager</label>
                    <select className={fieldClass} name="is_manager" value={formData.is_manager} onChange={handleChange}>
                      <option>Yes</option>
                      <option>No</option>
                    </select>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-slate-700">Function</label>
                    <input className={fieldClass} name="function" value={formData.function} onChange={handleChange} />
                  </div>
                </div>

                <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
                  <div>
                    <label className="text-sm font-medium text-slate-700">Region</label>
                    <input className={fieldClass} name="region" value={formData.region} onChange={handleChange} />
                  </div>
                  <div>
                    <label className="text-sm font-medium text-slate-700">Country</label>
                    <input className={fieldClass} name="country" value={formData.country} onChange={handleChange} />
                  </div>
                </div>

                <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
                  <div>
                    <label className="text-sm font-medium text-slate-700">Platform</label>
                    <select className={fieldClass} name="device_platform" value={formData.device_platform} onChange={handleChange}>
                      <option>Windows</option>
                      <option>Mac</option>
                      <option>Linux</option>
                    </select>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-slate-700">RAM (GB)</label>
                    <input className={fieldClass} type="number" name="ram" value={formData.ram} onChange={handleChange} />
                  </div>
                  <div>
                    <label className="text-sm font-medium text-slate-700">Installed App Count</label>
                    <input
                      className={fieldClass}
                      type="number"
                      name="installed_app_count"
                      value={formData.installed_app_count}
                      onChange={handleChange}
                    />
                  </div>
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full rounded-2xl bg-slate-900 px-5 py-3 text-sm font-medium text-white shadow-sm transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  {loading ? "Generating onboarding plan..." : "Generate Onboarding Plan"}
                </button>
              </form>
            </div>
          </div>

          <div className="lg:col-span-3">
            <div className="rounded-3xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
              <div className="flex items-center justify-between gap-4">
                <div>
                  <h2 className="text-xl font-semibold text-slate-900">AI Onboarding Output</h2>
                  <p className="mt-2 text-sm text-slate-600">
                    Results from persona normalization, bundle prediction, provisioning logic, and reasoning.
                  </p>
                </div>
                {result && (
                  <div className="rounded-2xl bg-emerald-50 px-4 py-2 text-sm font-medium text-emerald-700 ring-1 ring-emerald-200">
                    Plan generated
                  </div>
                )}
              </div>

              {error && (
                <div className="mt-6 rounded-2xl bg-rose-50 p-4 text-sm text-rose-700 ring-1 ring-rose-200">
                  {error}
                </div>
              )}

              {!result && !error && (
                <div className="mt-8 rounded-3xl border border-dashed border-slate-300 bg-slate-50 p-10 text-center text-sm text-slate-500">
                  Submit an employee profile to view the generated onboarding plan.
                </div>
              )}

              {result && (
                <div className="mt-8 space-y-6">
                  <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
                    <div className="rounded-2xl bg-slate-50 p-4 ring-1 ring-slate-200">
                      <div className="text-xs uppercase tracking-wide text-slate-500">Persona</div>
                      <div className="mt-2 text-lg font-semibold text-slate-900">{result.persona || "N/A"}</div>
                    </div>
                    <div className="rounded-2xl bg-slate-50 p-4 ring-1 ring-slate-200">
                      <div className="text-xs uppercase tracking-wide text-slate-500">Bundle</div>
                      <div className="mt-2 text-lg font-semibold text-slate-900">{result.bundle || "N/A"}</div>
                    </div>
                    <div className="rounded-2xl bg-slate-50 p-4 ring-1 ring-slate-200">
                      <div className="text-xs uppercase tracking-wide text-slate-500">Applications</div>
                      <div className="mt-2 text-lg font-semibold text-slate-900">
                        {Array.isArray(result.applications) ? result.applications.length : 0}
                      </div>
                    </div>
                  </div>

                  <div className="rounded-3xl bg-slate-50 p-5 ring-1 ring-slate-200">
                    <h3 className="text-base font-semibold text-slate-900">Provisioning Plan</h3>
                    <div className="mt-4 grid grid-cols-1 gap-3 md:grid-cols-2 xl:grid-cols-3">
                      {(result.applications || []).map((app, idx) => (
                        <div
                          key={`${app}-${idx}`}
                          className="rounded-2xl bg-white px-4 py-3 text-sm text-slate-700 shadow-sm ring-1 ring-slate-200"
                        >
                          {app}
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="rounded-3xl bg-slate-50 p-5 ring-1 ring-slate-200">
                    <h3 className="text-base font-semibold text-slate-900">AI Explanation</h3>
                    <p className="mt-4 whitespace-pre-wrap text-sm leading-7 text-slate-700">
                      {result.explanation || "No explanation returned."}
                    </p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}


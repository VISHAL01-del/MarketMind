
import { useState } from "react";

interface AnomalyResponse {
  is_anomaly: boolean;
  anomaly_prediction: number;
  message: string;
}

export default function AnomalyDetectionForm() {
  const [formData, setFormData] = useState({
    age: "30",
    membership_years: "2",
    total_orders: "10",
    average_order_value: "500",
    days_since_last_purchase: "45",
    total_spending: "5000",
  });

  const [result, setResult] =
    useState<AnomalyResponse | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function handleChange(
    event: React.ChangeEvent<HTMLInputElement>
  ) {
    setFormData({
      ...formData,
      [event.target.name]: event.target.value,
    });
  }

  async function handleSubmit(
    event: React.FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();
    setResult(null);
    setError("");
    setLoading(true);

    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_BASE_URL}/customers/anomalies`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            age: Number(formData.age),
            membership_years: Number(
              formData.membership_years
            ),
            total_orders: Number(formData.total_orders),
            average_order_value: Number(
              formData.average_order_value
            ),
            days_since_last_purchase: Number(
              formData.days_since_last_purchase
            ),
            total_spending: Number(formData.total_spending),
          }),
        }
      );

      if (!response.ok) {
        throw new Error(`Request failed: HTTP ${response.status}`);
      }

      const data: AnomalyResponse = await response.json();
      setResult(data);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Could not analyze this customer."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <section>
      <h2>Customer anomaly detection</h2>
      <p>
        Use the trained Isolation Forest model to flag unusual
        customer profiles for review.
      </p>

      <form onSubmit={handleSubmit}>
        <label>
          Age
          <input
            name="age"
            type="number"
            min="18"
            max="100"
            value={formData.age}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Membership years
          <input
            name="membership_years"
            type="number"
            min="0"
            max="100"
            value={formData.membership_years}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Total orders
          <input
            name="total_orders"
            type="number"
            min="0"
            value={formData.total_orders}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Average order value
          <input
            name="average_order_value"
            type="number"
            min="0.01"
            step="0.01"
            value={formData.average_order_value}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Days since last purchase
          <input
            name="days_since_last_purchase"
            type="number"
            min="0"
            value={formData.days_since_last_purchase}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Total spending
          <input
            name="total_spending"
            type="number"
            min="0"
            step="0.01"
            value={formData.total_spending}
            onChange={handleChange}
            required
          />
        </label>

        <button type="submit" disabled={loading}>
          {loading ? "Analyzing..." : "Detect anomalies"}
        </button>
      </form>

      {error && <p role="alert">Error: {error}</p>}

      {result && (
        <div aria-live="polite">
          <h3>Analysis result</h3>
          <p>
            <strong>Status:</strong>{" "}
            {result.is_anomaly
              ? "Unusual customer pattern detected"
              : "No unusual pattern detected"}
          </p>
          <p>{result.message}</p>
          <p>
            <strong>Model output:</strong>{" "}
            {result.anomaly_prediction}
          </p>
        </div>
      )}
    </section>
  );
}

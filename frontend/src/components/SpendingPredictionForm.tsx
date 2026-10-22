
import { useState } from "react";

interface SpendingPredictionResponse {
  predicted_total_spending: number;
  message: string;
}

export default function SpendingPredictionForm() {
  const [formData, setFormData] = useState({
    age: "30",
    membership_years: "2",
    total_orders: "10",
    average_order_value: "500",
    days_since_last_purchase: "45",
  });

  const [result, setResult] =
    useState<SpendingPredictionResponse | null>(null);
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
        `${import.meta.env.VITE_API_BASE_URL}/predict/spending`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            age: Number(formData.age),
            membership_years: Number(formData.membership_years),
            total_orders: Number(formData.total_orders),
            average_order_value: Number(
              formData.average_order_value
            ),
            days_since_last_purchase: Number(
              formData.days_since_last_purchase
            ),
          }),
        }
      );

      if (!response.ok) {
        throw new Error(
          `Request failed: HTTP ${response.status}`
        );
      }

      const data: SpendingPredictionResponse =
        await response.json();

      setResult(data);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Could not predict spending."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <section>
      <h2>Spending prediction</h2>
      <p>
        Enter customer details to estimate total spending.
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

        <button type="submit" disabled={loading}>
          {loading
            ? "Predicting..."
            : "Predict spending"}
        </button>
      </form>

      {error && <p role="alert">Error: {error}</p>}

      {result && (
        <div aria-live="polite">
          <h3>Prediction result</h3>
          <p>
            <strong>Estimated total spending:</strong>{" "}
            {result.predicted_total_spending.toLocaleString(
              "en-IN",
              {
                maximumFractionDigits: 2,
              }
            )}
          </p>
          <p>{result.message}</p>
        </div>
      )}
    </section>
  );
}

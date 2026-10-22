
import { useState } from "react";

interface SegmentationResponse {
  customer_segment: number;
  message: string;
}

export default function CustomerSegmentationForm() {
  const [formData, setFormData] = useState({
    total_orders: "10",
    average_order_value: "500",
    days_since_last_purchase: "45",
    total_spending: "5000",
  });

  const [result, setResult] =
    useState<SegmentationResponse | null>(null);
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
        `${import.meta.env.VITE_API_BASE_URL}/customers/segment`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
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

      const data: SegmentationResponse =
        await response.json();

      setResult(data);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Could not assign customer segment."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <section>
      <h2>Customer segmentation</h2>
      <p>
        Group customer profiles using your trained K-Means model.
      </p>

      <form onSubmit={handleSubmit}>
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
          {loading ? "Analyzing..." : "Find customer segment"}
        </button>
      </form>

      {error && <p role="alert">Error: {error}</p>}

      {result && (
        <div aria-live="polite">
          <h3>Segmentation result</h3>
          <p>
            <strong>Customer segment:</strong>{" "}
            {result.customer_segment}
          </p>
          <p>{result.message}</p>
        </div>
      )}
    </section>
  );
}

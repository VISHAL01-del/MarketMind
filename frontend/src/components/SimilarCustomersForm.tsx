
import { useState } from "react";

interface SimilarCustomer {
  customer_id: number;
  age: number;
  total_orders: number;
  average_order_value: number;
  days_since_last_purchase: number;
  total_spending: number;
  similarity_distance: number;
}

interface SimilarCustomersResponse {
  similar_customers: SimilarCustomer[];
}

export default function SimilarCustomersForm() {
  const [formData, setFormData] = useState({
    age: "30",
    membership_years: "2",
    total_orders: "10",
    average_order_value: "500",
    days_since_last_purchase: "45",
    total_spending: "5000",
  });

  const [result, setResult] =
    useState<SimilarCustomersResponse | null>(null);
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
        `${import.meta.env.VITE_API_BASE_URL}/customers/similar`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            age: Number(formData.age),
            membership_years: Number(formData.membership_years),
            total_orders: Number(formData.total_orders),
            average_order_value: Number(formData.average_order_value),
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

      const data: SimilarCustomersResponse = await response.json();
      setResult(data);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Could not find similar customers."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="ml-form-card">
      <h2>Similar customers</h2>
      <p>
        Find five customer profiles with similar characteristics
        using your trained KNN model.
      </p>

      <form onSubmit={handleSubmit} className="ml-form-grid">
        <label>
          Age
          <input name="age" type="number" min="18" max="100"
            value={formData.age} onChange={handleChange} required />
        </label>

        <label>
          Membership years
          <input name="membership_years" type="number" min="0" max="100"
            value={formData.membership_years} onChange={handleChange} required />
        </label>

        <label>
          Total orders
          <input name="total_orders" type="number" min="0"
            value={formData.total_orders} onChange={handleChange} required />
        </label>

        <label>
          Average order value
          <input name="average_order_value" type="number" min="0.01" step="0.01"
            value={formData.average_order_value} onChange={handleChange} required />
        </label>

        <label>
          Days since last purchase
          <input name="days_since_last_purchase" type="number" min="0"
            value={formData.days_since_last_purchase} onChange={handleChange} required />
        </label>

        <label>
          Total spending
          <input name="total_spending" type="number" min="0" step="0.01"
            value={formData.total_spending} onChange={handleChange} required />
        </label>

        <button type="submit" disabled={loading}>
          {loading ? "Finding customers..." : "Find similar customers"}
        </button>
      </form>

      {error && <p role="alert">Error: {error}</p>}

      {result && (
        <div aria-live="polite">
          <h3>Similar customer profiles</h3>
          {result.similar_customers?.length ? (
            result.similar_customers.map((customer) => (
              <article key={customer.customer_id}>
                <h4>Customer #{customer.customer_id}</h4>
                <p>Age: {customer.age}</p>
                <p>Total orders: {customer.total_orders}</p>
                <p>
                  Average order value: ₹
                  {customer.average_order_value.toFixed(2)}
                </p>
                <p>
                  Days since last purchase:{" "}
                  {customer.days_since_last_purchase}
                </p>
                <p>
                  Total spending: ₹
                  {customer.total_spending.toFixed(2)}
                </p>
                <p>
                  Similarity distance: {customer.similarity_distance}
                </p>
              </article>
            ))
          ) : (
            <p>No similar customers were returned.</p>
          )}
        </div>
      )}
    </section>
  );
}

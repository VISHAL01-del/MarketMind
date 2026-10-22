import { useState } from 'react'

interface ChurnPredictionResponse {
  churn_prediction: number
  churn_probability: number
  message: string
}

function ChurnPredictionForm() {
  const [formData, setFormData] = useState({
    age: '30',
    membership_years: '2',
    total_orders: '10',
    average_order_value: '500',
    days_since_last_purchase: '30',
    total_spending: '5000',
  })

  const [message, setMessage] = useState('')
  const [result, setResult] =
    useState<ChurnPredictionResponse | null>(null)
  const [loading, setLoading] = useState(false)

  function handleChange(
    event: React.ChangeEvent<HTMLInputElement>
  ) {
    const { name, value } = event.target

    setFormData((previousData) => ({
      ...previousData,
      [name]: value,
    }))

    setMessage('')
    setResult(null)
  }

  async function handleSubmit(
    event: React.FormEvent<HTMLFormElement>
  ) {
    event.preventDefault()

    setLoading(true)
    setMessage('')
    setResult(null)

    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_BASE_URL}/predict/churn`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
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
            total_spending: Number(formData.total_spending),
          }),
        }
      )

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status}`)
      }

      const prediction: ChurnPredictionResponse =
        await response.json()

      setResult(prediction)
    } catch (error) {
      console.error('Churn prediction failed:', error)
      setMessage(
        'Unable to get prediction. Check that the backend is running and the API URL is correct.'
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="panel churn-form-panel ml-form-card" id="churn-form">
      <div className="panel-heading">
        <div>
          <h3>Churn prediction</h3>
          <p>Enter a customer's details to assess churn risk.</p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="churn-form ml-form-grid">
        <label>
          Age
          <input
            type="number"
            name="age"
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
            type="number"
            name="membership_years"
            min="0"
            value={formData.membership_years}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Total orders
          <input
            type="number"
            name="total_orders"
            min="0"
            value={formData.total_orders}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Average order value
          <input
            type="number"
            name="average_order_value"
            min="0"
            step="0.01"
            value={formData.average_order_value}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Days since last purchase
          <input
            type="number"
            name="days_since_last_purchase"
            min="0"
            value={formData.days_since_last_purchase}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Total spending
          <input
            type="number"
            name="total_spending"
            min="0"
            step="0.01"
            value={formData.total_spending}
            onChange={handleChange}
            required
          />
        </label>

        <button
          type="submit"
          className="hero-button"
          disabled={loading}
        >
          {loading ? 'Analyzing customer...' : 'Check churn risk →'}
        </button>

        {message && <p role="alert">{message}</p>}

        {result && (
          <div className="prediction-result" role="status">
            <h4>Prediction result</h4>

            <p>
              <strong>Status:</strong> {result.message}
            </p>

            <p>
              <strong>Churn probability:</strong>{' '}
              {(result.churn_probability * 100).toFixed(2)}%
            </p>

            <p>
              <strong>Prediction class:</strong>{' '}
              {result.churn_prediction}
            </p>
          </div>
        )}
      </form>
    </section>
  )
}

export default ChurnPredictionForm

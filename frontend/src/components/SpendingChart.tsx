
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
} from 'recharts'
const spendingData = [
  { segment: 'Segment 0', spending: 12000 },
  { segment: 'Segment 1', spending: 16500 },
  { segment: 'Segment 2', spending: 19000 },
  { segment: 'Segment 3', spending: 22500 },
  { segment: 'Segment 4', spending: 17500 },
]

function SpendingChart() {
  return (
    <div className="spending-chart">
      <div className="chart-title">
        <div>
          <h3>Average spending by segment</h3>
          <p>Illustrative values · ₹ per customer</p>
        </div>
        <span className="chart-badge">Preview</span>
      </div>
<div className="chart-container">
  <ResponsiveContainer width="100%" height={260}>
    <BarChart
      data={spendingData}
      margin={{ top: 12, right: 10, left: 0, bottom: 10 }}
    >
      <CartesianGrid
        stroke="#ececf4"
        strokeDasharray="4 4"
        vertical={false}
      />

      <XAxis
        dataKey="segment"
        tick={{ fill: '#858ba0', fontSize: 10 }}
        axisLine={false}
        tickLine={false}
      />

      <YAxis
        tick={{ fill: '#858ba0', fontSize: 10 }}
        axisLine={false}
        tickLine={false}
        tickFormatter={(value: number) => `₹${value / 1000}k`}
        width={48}
      />

      <Tooltip
        formatter={(value) => [
          `₹${Number(value).toLocaleString('en-IN')}`,
          'Average spending',
        ]}
      />

      <Bar
        dataKey="spending"
        fill="#7965e8"
        radius={[6, 6, 0, 0]}
        maxBarSize={42}
      />
    </BarChart>
  </ResponsiveContainer>
</div>
    </div>
  )
}

export default SpendingChart

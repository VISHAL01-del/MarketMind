
import { useEffect, useState } from 'react'
import './App.css'
import SpendingChart from './components/SpendingChart'
import ChurnPredictionForm from './components/ChurnPredictionForm'
import SpendingPredictionForm from './components/SpendingPredictionForm'
import CustomerInsightsForm from './components/CustomerInsightsForm'
import CustomerSegmentationForm from './components/CustomerSegmentationForm'
import AnomalyDetectionForm from './components/AnomalyDetectionForm'
import SimilarCustomersForm from './components/SimilarCustomersForm'
const features = [
  {
    id: 'churn',
    target: 'churn-tool',
    number: '01',
    icon: '◉',
    title: 'Churn prediction',
    description: 'Identify customers who may stop purchasing.',
    color: 'violet',
  },
  {
    id: 'spending',
    target: 'spending-tool',
    number: '02',
    icon: '↗',
    title: 'Spending prediction',
    description: 'Estimate customer spending from their profile.',
    color: 'blue',
  },
  {
    id: 'insights',
    target: 'insights-tool',
    number: '03',
    icon: '✧',
    title: 'Customer insights',
    description: 'Explore engagement risks and retention actions.',
    color: 'green',
  },
  {
    id: 'segments',
    target: 'segments-tool',
    number: '04',
    icon: '◷',
    title: 'Customer segmentation',
    description: 'Discover groups with similar buying behavior.',
    color: 'orange',
  },
  {
    id: 'anomalies',
    target: 'anomalies-tool',
    number: '05',
    icon: '⌁',
    title: 'Anomaly detection',
    description: 'Flag unusual customer patterns for review.',
    color: 'pink',
  },
  {
    id: 'similar',
    target: 'similar-tool',
    number: '06',
    icon: '⇄',
    title: 'Similar customers',
    description: 'Find profiles with similar characteristics.',
    color: 'cyan',
  },
]

const navItems = [
  { target: 'dashboard', icon: '▦', label: 'Overview' },
  { target: 'churn-tool', icon: '◉', label: 'Churn prediction' },
  { target: 'spending-tool', icon: '↗', label: 'Spending prediction' },
  { target: 'insights-tool', icon: '✧', label: 'Customer insights' },
  { target: 'segments-tool', icon: '◷', label: 'Segmentation' },
  { target: 'anomalies-tool', icon: '⌁', label: 'Anomaly detection' },
  { target: 'similar-tool', icon: '⇄', label: 'Similar customers' },
]

function App() {
  const [activeSection, setActiveSection] = useState('dashboard')

  useEffect(() => {
    const sections = navItems
      .map(({ target }) => document.getElementById(target))
      .filter((section): section is HTMLElement => section !== null)
    const observer = new IntersectionObserver(
      (entries) => {
        const visibleSection = entries.find((entry) => entry.isIntersecting)
        if (visibleSection) setActiveSection(visibleSection.target.id)
      },
      { rootMargin: '-18% 0px -70% 0px' },
    )
    sections.forEach((section) => observer.observe(section))
    return () => observer.disconnect()
  }, [])

  return (
    <div className="app-layout">
      <aside className="sidebar">
        <a href="#dashboard" className="brand">
          <div className="brand-icon">M</div>
          <div>
            <h2>
              MarketMind<span>.</span>
            </h2>
            <p>INTELLIGENCE PLATFORM</p>
          </div>
        </a>

        <p className="nav-label">WORKSPACE</p>

        <nav className="navigation">
          {navItems.map((item) => (
            <a
              href={`#${item.target}`}
              className={`nav-item ${activeSection === item.target ? 'active' : ''}`}
              onClick={() => setActiveSection(item.target)}
              key={item.target}
            >
              <span>{item.icon}</span> {item.label}
            </a>
          ))}
        </nav>

        <div className="sidebar-note">
          <div className="note-icon">✳</div>
          <strong>Built with machine learning</strong>
          <p>Explore customer behavior with your ML toolkit.</p>
        </div>

        <div className="sidebar-footer">
          <div className="avatar">ML</div>
          <div>
            <strong>ML Workspace</strong>
            <p>Local environment</p>
          </div>
          <span className="footer-dots">···</span>
        </div>
      </aside>

      <main className="main-content" id="dashboard">
        <header className="topbar">
          <div>
            <p className="breadcrumb">
              Workspace <span>/</span> Overview
            </p>
            <h1>Customer intelligence</h1>
            <p className="page-subtitle">
              Understand your customers. Make smarter decisions.
            </p>
          </div>

          <div className="topbar-actions">
            <span className="environment-pill">
              <span className="environment-dot" />
              DEVELOPMENT
            </span>
            <div className="topbar-avatar">V</div>
          </div>
        </header>

        <section className="welcome-banner">
          <div className="hero-copy">
            <span className="hero-tag">✦ YOUR ML WORKSPACE</span>
            <h2>
              Every customer
              <br />
              has a <span>story.</span>
            </h2>
            <p>
              Turn customer data into actionable insights with your
              machine learning models.
            </p>
            <a href="#tools" className="hero-button">
              Explore ML tools <span>↗</span>
            </a>
          </div>

          <div className="hero-art" aria-hidden="true">
            <div className="hero-ring ring-one" />
            <div className="hero-ring ring-two" />
            <div className="hero-orb">AI</div>
            <div className="floating-chip chip-top">✦ Predict</div>
            <div className="floating-chip chip-bottom">↗ Analyze</div>
            <div className="hero-spark spark-one">✳</div>
            <div className="hero-spark spark-two">✧</div>
          </div>
        </section>

        <section className="section-heading">
          <div>
            <h2>Your workspace at a glance</h2>
            <p>Project overview and available capabilities</p>
          </div>
          <span className="sample-label">PROJECT OVERVIEW</span>
        </section>

        <section className="stats-grid">
          <article className="stat-card">
            <div className="stat-top">
              <span>Customer records</span>
              <span className="stat-icon violet">♙</span>
            </div>
            <strong>1,000</strong>
            <p>
              <span className="stat-neutral">Synthetic dataset</span>
            </p>
            <div className="stat-track">
              <div className="stat-fill violet-fill" />
            </div>
          </article>

          <article className="stat-card">
            <div className="stat-top">
              <span>ML API features</span>
              <span className="stat-icon green">✳</span>
            </div>
            <strong>6</strong>
            <p>
              <span className="stat-neutral">Core capabilities</span>
            </p>
            <div className="stat-track">
              <div className="stat-fill green-fill" />
            </div>
          </article>

          <article className="stat-card">
            <div className="stat-top">
              <span>Saved ML models</span>
              <span className="stat-icon blue">⌘</span>
            </div>
            <strong>10</strong>
            <p>
              <span className="stat-neutral">Classical ML techniques</span>
            </p>
            <div className="stat-track">
              <div className="stat-fill blue-fill" />
            </div>
          </article>

          <article className="stat-card">
            <div className="stat-top">
              <span>Backend health</span>
              <span className="stat-icon orange">⌁</span>
            </div>
            <strong className="health-value">Configured</strong>
            <p>
              <span className="stat-neutral">
                Live status check coming later
              </span>
            </p>
            <div className="stat-track">
              <div className="stat-fill orange-fill" />
            </div>
          </article>
        </section>

        <section className="analytics-grid">
          <article className="panel chart-panel">
            <SpendingChart />
          </article>

          <article className="panel insights-panel">
            <div className="panel-heading">
              <div>
                <h3>Project highlights</h3>
                <p>What you can explore</p>
              </div>
              <span className="highlight-spark">✦</span>
            </div>

            <a className="highlight-item" href="#churn-tool">
              <span className="highlight-icon violet">◉</span>
              <div>
                <strong>Understand churn</strong>
                <p>Estimate customer churn risk.</p>
              </div>
              <span className="highlight-arrow">↗</span>
            </a>

            <a className="highlight-item" href="#segments-tool">
              <span className="highlight-icon green">◷</span>
              <div>
                <strong>Discover segments</strong>
                <p>Explore customer group assignments.</p>
              </div>
              <span className="highlight-arrow">↗</span>
            </a>

            <a className="highlight-item" href="#anomalies-tool">
              <span className="highlight-icon orange">⌁</span>
              <div>
                <strong>Review anomalies</strong>
                <p>Flag unusual profiles for investigation.</p>
              </div>
              <span className="highlight-arrow">↗</span>
            </a>
          </article>
        </section>

        <section className="section-heading tools-heading" id="tools">
          <div>
            <h2>
              Explore your ML toolkit <span>✦</span>
            </h2>
            <p>Six capabilities, one customer intelligence workspace.</p>
          </div>
          <span className="sample-label">6 FEATURES</span>
        </section>

        <section className="feature-grid">
          {features.map((feature) => (
            <article
              className="feature-card"
              id={`feature-${feature.id}`}
              key={feature.id}
            >
              <div className="feature-card-top">
                <div className={`feature-icon ${feature.color}`}>
                  {feature.icon}
                </div>
                <span className="feature-number">{feature.number}</span>
              </div>
              <h3>{feature.title}</h3>
              <p>{feature.description}</p>
              <a
                href={`#${feature.target}`}
              >
                Open tool <span>↗</span>
              </a>
            </article>
          ))}
        </section>
        <section className="section-heading" id="churn-tool">
          <div>
           <h2>Customer risk analysis</h2>
           <p>Enter customer details to explore churn prediction.</p>
          </div>
          <span className="sample-label">CHURN MODEL</span>
        </section>

<ChurnPredictionForm />

<section className="section-heading" id="spending-tool">
  <div>
    <h2>Customer spending analysis</h2>
    <p>
      Estimate total customer spending using your trained ML model.
    </p>
  </div>
  <span className="sample-label">SPENDING MODEL</span>
</section>

<SpendingPredictionForm />
<section className="section-heading" id="insights-tool">
  <div>
    <h2>Customer insights</h2>
    <p>
      Explore engagement risk, churn probability, and retention recommendations.
    </p>
  </div>
  <span className="sample-label">INSIGHTS MODEL</span>
</section>

<CustomerInsightsForm />
<section className="section-heading" id="segments-tool">
  <div>
    <h2>Customer segmentation</h2>
    <p>
      Discover customer groups using your trained K-Means model.
    </p>
  </div>
  <span className="sample-label">SEGMENTATION MODEL</span>
</section>

<CustomerSegmentationForm />

<section className="section-heading" id="anomalies-tool">
  <div>
    <h2>Anomaly detection</h2>
    <p>
      Identify unusual customer profiles using your
      trained Isolation Forest model.
    </p>
  </div>
  <span className="sample-label">ANOMALY MODEL</span>
</section>

<AnomalyDetectionForm />
<section className="section-heading" id="similar-tool">
  <div>
    <h2>Similar customers</h2>
    <p>
      Find five customer profiles with similar buying
      characteristics using your trained KNN model.
    </p>
  </div>
  <span className="sample-label">KNN MODEL</span>
</section>

<SimilarCustomersForm />
        <footer className="dashboard-footer">
          <span>
            MarketMind <span className="footer-dot">·</span> E-commerce ML
            Project
          </span>
          <span>Built with React, TypeScript &amp; FastAPI</span>
        </footer>
      </main>
    </div>
  )
}

export default App

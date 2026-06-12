import { useState, useEffect } from 'react'
import { getOverview, getHeatmap, getCohorts } from '../utils/api'
import RiskHeatmap from '../components/RiskHeatmap'

function StatCard({ label, value, color }) {
  return (
    <div className="bg-dark-card border border-dark-border rounded-lg p-6">
      <div className="text-sm text-gray-400 mb-2">{label}</div>
      <div className={`text-3xl font-bold ${color}`}>{value}</div>
    </div>
  )
}

function CohortAlertBanner({ alerts }) {
  if (!alerts || alerts.length === 0) return null
  
  return (
    <div className="bg-accent-warning/10 border border-accent-warning/30 rounded-lg p-4 mb-6">
      <div className="flex items-start">
        <div className="flex-shrink-0">
          <svg className="h-6 w-6 text-accent-warning" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
        <div className="ml-3 flex-1">
          <h3 className="text-sm font-medium text-accent-warning">
            {alerts.length} Active Cohort Alert{alerts.length > 1 ? 's' : ''}
          </h3>
          {alerts.map((alert, i) => (
            <div key={i} className="mt-2 text-sm text-gray-300">
              <span className="font-semibold">{alert.batch}</span> - {alert.affected_students} students affected ({alert.affected_percentage}%)
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

function Home() {
  const [overview, setOverview] = useState(null)
  const [heatmap, setHeatmap] = useState([])
  const [cohorts, setCohorts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [lastUpdate, setLastUpdate] = useState(new Date())

  const fetchData = async () => {
    try {
      const [overviewData, heatmapData, cohortsData] = await Promise.all([
        getOverview(),
        getHeatmap(),
        getCohorts()
      ])
      
      setOverview(overviewData)
      setHeatmap(heatmapData)
      setCohorts(cohortsData)
      setLastUpdate(new Date())
      setError(null)
    } catch (err) {
      setError(err.message)
      console.error('Failed to fetch data:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
    
    // Poll every 30 seconds
    const interval = setInterval(fetchData, 30000)
    return () => clearInterval(interval)
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-400">Loading dashboard...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-accent-danger/10 border border-accent-danger/30 rounded-lg p-4">
        <div className="text-accent-danger">Error: {error}</div>
        <button 
          onClick={fetchData}
          className="mt-2 px-4 py-2 bg-accent-primary text-dark-bg rounded hover:bg-accent-primary/90"
        >
          Retry
        </button>
      </div>
    )
  }

  // Find active cohort alerts
  const activeAlerts = cohorts.filter(c => c.active_alerts > 0)

  return (
    <div className="space-y-6">
      {/* Cohort Alerts Banner */}
      {activeAlerts.length > 0 && (
        <CohortAlertBanner alerts={activeAlerts} />
      )}

      {/* Overview Stats */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-bold text-white">Overview</h2>
          <div className="text-xs text-gray-500">
            Last updated: {lastUpdate.toLocaleTimeString()}
          </div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <StatCard 
            label="Total Students" 
            value={overview?.total_students || 0}
            color="text-gray-200"
          />
          <StatCard 
            label="Stable" 
            value={overview?.stable_count || 0}
            color="text-accent-success"
          />
          <StatCard 
            label="At Risk" 
            value={overview?.at_risk_count || 0}
            color="text-accent-warning"
          />
          <StatCard 
            label="Crisis" 
            value={overview?.crisis_count || 0}
            color="text-accent-danger"
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
          <StatCard 
            label="Check-in Rate (7d)" 
            value={`${overview?.check_in_rate_7d?.toFixed(1) || 0}%`}
            color="text-accent-primary"
          />
          <StatCard 
            label="Interventions Today" 
            value={overview?.interventions_today || 0}
            color="text-accent-primary"
          />
          <StatCard 
            label="Active Cohort Alerts" 
            value={overview?.cohort_alerts_active || 0}
            color="text-accent-warning"
          />
        </div>
      </div>

      {/* Risk Heatmap */}
      <div>
        <h2 className="text-2xl font-bold text-white mb-4">Risk Heatmap</h2>
        <RiskHeatmap students={heatmap} />
      </div>
    </div>
  )
}

export default Home

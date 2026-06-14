import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts'
import { getStudentProfile } from '../utils/api'

const stateColors = {
  stable: '#26de81',
  at_risk: '#ffa502',
  crisis: '#ff4757'
}

function StudentProfile() {
  const { studentId } = useParams()
  const navigate = useNavigate()
  const [profile, setProfile] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [expandedReasoning, setExpandedReasoning] = useState({})

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const data = await getStudentProfile(studentId)
        setProfile(data)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchProfile()
  }, [studentId])

  if (loading) {
    return <div className="text-center py-12 text-gray-400">Loading profile...</div>
  }

  if (error) {
    return (
      <div className="bg-accent-danger/10 border border-accent-danger/30 rounded-lg p-4">
        <div className="text-accent-danger">Error: {error}</div>
        <button 
          onClick={() => navigate('/')}
          className="mt-2 px-4 py-2 bg-accent-primary text-dark-bg rounded hover:bg-accent-primary/90"
        >
          Back to Dashboard
        </button>
      </div>
    )
  }

  const { basic_info, checkins_14d, state_history, interventions, adversarial_summary } = profile

  // Prepare chart data
  const chartData = checkins_14d.map((c) => ({
    date: new Date(c.checked_in_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
    score: c.mood_score,
    sentiment: c.sentiment_score
  }))

  // Word cloud data from one_words
  const words = checkins_14d.map(c => c.one_word).filter(Boolean)
  const wordFreq = words.reduce((acc, word) => {
    acc[word] = (acc[word] || 0) + 1
    return acc
  }, {})
  const wordCloud = Object.entries(wordFreq)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)

  return (
    <div className="space-y-6 page-enter">
      {/* Back Button */}
      <button
        onClick={() => navigate('/dashboard')}
        className="flex items-center text-accent-primary hover:text-accent-primary/80 transition"
      >
        <svg className="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
        </svg>
        Back to Dashboard
      </button>

      {/* Header */}
      <div className="bg-dark-card border border-dark-border rounded-lg p-6">
        <div className="flex items-start justify-between gap-6">
          <div className="flex-1">
            <h1 className="text-3xl font-bold text-white mb-2">{basic_info.name}</h1>
            <div className="flex items-center space-x-4 text-sm text-gray-400">
              <span>{basic_info.batch}</span>
              <span>•</span>
              <span>Year {basic_info.year_of_study}</span>
              <span>•</span>
              <span>Baseline: {basic_info.baseline_score != null ? basic_info.baseline_score.toFixed(1) : 'N/A'}</span>
            </div>
          </div>

          {/* Hero Risk Score Gauge */}
          <div className="flex items-center gap-6">
            <div className="relative flex items-center justify-center">
              {/* Circular gauge */}
              <svg className="transform -rotate-90" width="120" height="120">
                {/* Background circle */}
                <circle
                  cx="60"
                  cy="60"
                  r="50"
                  fill="none"
                  stroke="#2a2a3e"
                  strokeWidth="10"
                />
                {/* Progress circle */}
                <circle
                  cx="60"
                  cy="60"
                  r="50"
                  fill="none"
                  stroke={
                    basic_info.current_state === 'crisis' ? '#ff4757' :
                    basic_info.current_state === 'at_risk' ? '#E67E22' :
                    '#26de81'
                  }
                  strokeWidth="10"
                  strokeDasharray={`${(basic_info.risk_score || 0) * 3.14} 314`}
                  strokeLinecap="round"
                  className={basic_info.current_state === 'crisis' ? 'crisis-pulse' : ''}
                />
              </svg>
              {/* Center content */}
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <div className="text-4xl font-bold text-white">{basic_info.risk_score || 0}</div>
                <div className={`text-xs font-bold uppercase mt-1 ${
                  basic_info.current_state === 'crisis' ? 'text-accent-danger' :
                  basic_info.current_state === 'at_risk' ? 'text-[#E67E22]' :
                  'text-accent-success'
                }`}>
                  {basic_info.current_state?.replace('_', '-') || 'stable'}
                </div>
              </div>
            </div>
            
            {/* Adversarial Badge */}
            {adversarial_summary.gaming_detected_count > 0 && (
              <div className="bg-accent-warning/20 border border-accent-warning/50 rounded-lg px-4 py-2">
                <div className="text-accent-warning text-sm font-semibold">⚠️ Gaming Detected</div>
                <div className="text-xs text-gray-400 mt-1">
                  {adversarial_summary.gaming_detected_count} / {adversarial_summary.total_assessments} assessments
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* 14-Day Score Trend */}
      <div className="bg-dark-card border border-dark-border rounded-lg p-6">
        <h2 className="text-xl font-bold text-white mb-4">14-Day Mood Trend</h2>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#2a2a3e" />
            <XAxis dataKey="date" stroke="#666" />
            <YAxis domain={[0, 5]} stroke="#666" />
            <Tooltip
              contentStyle={{ backgroundColor: '#1a1a2e', border: '1px solid #2a2a3e' }}
              labelStyle={{ color: '#fff' }}
            />
            {/* Baseline Reference Line */}
            <ReferenceLine 
              y={basic_info.baseline_score || 3.8} 
              stroke="#00D4AA" 
              strokeDasharray="4 4"
              label={{ 
                value: 'Personal Baseline', 
                fill: '#00D4AA', 
                fontSize: 10,
                position: 'right'
              }} 
            />
            <Line type="monotone" dataKey="score" stroke="#00d4aa" strokeWidth={2} dot={{ fill: '#00d4aa' }} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* HMM State Timeline */}
      <div className="bg-dark-card border border-dark-border rounded-lg p-6">
        <h2 className="text-xl font-bold text-white mb-4">Mental Health State Timeline</h2>
        <div className="space-y-2">
          {/* Show only the most recent assessment per day for cleaner timeline */}
          {state_history.reduce((acc, state) => {
            const date = new Date(state.assessed_at).toLocaleDateString()
            // Keep only the last assessment for each date
            const existingIndex = acc.findIndex(s => new Date(s.assessed_at).toLocaleDateString() === date)
            if (existingIndex >= 0) {
              // Replace with later assessment
              if (new Date(state.assessed_at) > new Date(acc[existingIndex].assessed_at)) {
                acc[existingIndex] = state
              }
            } else {
              acc.push(state)
            }
            return acc
          }, []).map((state, i) => {
            // Calculate display percentage based on state + trend
            let displayPercentage
            if (state.state === 'crisis') {
              displayPercentage = 85 + Math.min(state.consecutive_low_days * 2, 10)
            } else if (state.state === 'at_risk') {
              displayPercentage = 50 + Math.max(Math.abs(state.trend_score) * 10, 0)
            } else {
              displayPercentage = Math.max(15 - (state.trend_score > 0 ? state.trend_score * 5 : 0), 5)
            }
            displayPercentage = Math.round(Math.min(displayPercentage, 95))

            const stateDate = new Date(state.assessed_at)
            const formattedDate = stateDate.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
            
            return (
              <div key={i} className="flex items-center space-x-4">
                <div className="text-xs text-gray-500 w-24">
                  {formattedDate}
                </div>
                <div
                  className="flex-1 h-12 rounded flex items-center justify-between px-4 text-sm font-semibold text-white"
                  style={{ backgroundColor: stateColors[state.state] }}
                >
                  <span>
                    {state.state.toUpperCase()} since {formattedDate}
                    {state.variance_flag && <span className="ml-2">⚠️</span>}
                    {state.cohort_flag && <span className="ml-2">👥</span>}
                  </span>
                  <span className="text-xs opacity-90">
                    {displayPercentage}% risk
                  </span>
                </div>
                <div className="text-xs text-gray-500 w-20 text-right">
                  {state.trend_score != null ? (state.trend_score > 0 ? '+' : '') + state.trend_score.toFixed(1) : '0.0'}
                </div>
              </div>
            )
          })}
        </div>
        <div className="mt-4 text-xs text-gray-500">
          Showing most recent assessment per day. Total assessments: {state_history.length}
        </div>
      </div>

      {/* One-Word Cloud */}
      <div className="bg-dark-card border border-dark-border rounded-lg p-6">
        <h2 className="text-xl font-bold text-white mb-4">Emotional Keywords</h2>
        <div className="flex flex-wrap gap-3">
          {wordCloud.map(([word, count]) => {
            const sentinelWords = ["hopeless", "empty", "lost", "worthless", "tired", "exhausted", "overwhelmed", "scared", "alone", "trapped"]
            const isSentinel = sentinelWords.some(sw => word.toLowerCase().includes(sw))
            const baseSize = 12
            const sizeMultiplier = Math.min(count * 3, 16)
            const opacity = Math.min(0.5 + (count * 0.15), 1)
            
            return (
              <span
                key={word}
                className={`px-4 py-2 rounded-full font-medium ${
                  isSentinel 
                    ? 'bg-accent-danger/20 text-accent-danger border border-accent-danger/40' 
                    : 'bg-accent-primary/10 text-accent-primary'
                }`}
                style={{ 
                  fontSize: `${baseSize + sizeMultiplier}px`,
                  opacity: isSentinel ? 1 : opacity
                }}
              >
                {word} {!isSentinel && `(${count})`}
              </span>
            )
          })}
        </div>
      </div>

      {/* Interventions */}
      <div className="bg-dark-card border border-dark-border rounded-lg p-6">
        <h2 className="text-xl font-bold text-white mb-4">Intervention History</h2>
        {interventions.length === 0 ? (
          <div className="text-gray-500 text-center py-8">No interventions yet</div>
        ) : (
          <div className="space-y-6 relative">
            {/* Vertical timeline line */}
            <div className="absolute left-[15px] top-0 bottom-0 w-0.5 bg-dark-border"></div>
            
            {interventions.map((intervention) => {
              const levelColor = 
                intervention.level === 3 ? '#ff4757' :
                intervention.level === 2 ? '#E67E22' :
                '#26de81'
              
              return (
                <div key={intervention.id} className="relative pl-10">
                  {/* Timeline dot */}
                  <div 
                    className="absolute left-0 top-1 w-8 h-8 rounded-full flex items-center justify-center font-bold text-white text-xs"
                    style={{ backgroundColor: levelColor }}
                  >
                    L{intervention.level}
                  </div>
                  
                  {/* Content */}
                  <div className="border border-dark-border rounded-lg p-4">
                    <div className="flex items-start justify-between mb-2">
                      <div>
                        <span className={`
                          inline-block px-3 py-1 rounded-full text-xs font-semibold uppercase
                          ${intervention.level === 3 ? 'bg-accent-danger/20 text-accent-danger' :
                            intervention.level === 2 ? 'bg-[#E67E22]/20 text-[#E67E22]' :
                            'bg-accent-success/20 text-accent-success'}
                        `}>
                          {intervention.recipient}
                        </span>
                      </div>
                      <div className="text-xs text-gray-500">
                        {new Date(intervention.triggered_at).toLocaleString('en-US', {
                          month: 'short',
                          day: 'numeric',
                          hour: 'numeric',
                          minute: '2-digit'
                        })}
                      </div>
                    </div>
                    
                    {/* Message content - visible by default */}
                    <div className="mt-3 p-3 bg-dark-bg rounded text-sm text-gray-300 border-l-2" style={{ borderLeftColor: levelColor }}>
                      <div className="flex items-start">
                        <span className="text-gray-500 mr-2">"</span>
                        <div className="flex-1 italic">{intervention.message_sent}</div>
                        <span className="text-gray-500 ml-2">"</span>
                      </div>
                    </div>
                    
                    {/* Expandable reasoning */}
                    <div className="mt-3">
                      <button
                        onClick={() => setExpandedReasoning(prev => ({
                          ...prev,
                          [intervention.id]: !prev[intervention.id]
                        }))}
                        className="text-accent-primary hover:underline text-xs"
                      >
                        {expandedReasoning[intervention.id] ? '▼' : '▶'} Agent Reasoning
                      </button>
                      
                      {expandedReasoning[intervention.id] && (
                        <div className="mt-2 p-3 bg-dark-bg rounded text-xs text-gray-400">
                          {intervention.trigger_reason}
                        </div>
                      )}
                    </div>
                    
                    <div className="mt-3 flex items-center space-x-4 text-xs">
                      <span className={`
                        font-medium
                        ${intervention.was_acknowledged ? 'text-accent-success' : 'text-gray-500'}
                      `}>
                        {intervention.was_acknowledged ? '✓ Acknowledged' : '○ Pending'}
                      </span>
                      <span className="text-gray-500">•</span>
                      <span className={`
                        ${intervention.outcome === 'recovered' ? 'text-accent-success' :
                          intervention.outcome === 'escalated' ? 'text-accent-danger' :
                          'text-gray-400'}
                      `}>
                        {intervention.outcome}
                      </span>
                    </div>
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}

export default StudentProfile

import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { getRecentInterventions } from '../utils/api'

const levelColors = {
  1: { bg: 'bg-accent-primary/20', text: 'text-accent-primary', label: 'Peer Nudge' },
  2: { bg: 'bg-accent-warning/20', text: 'text-accent-warning', label: 'Counsellor Alert' },
  3: { bg: 'bg-accent-danger/20', text: 'text-accent-danger', label: 'Emergency' },
  4: { bg: 'bg-purple-500/20', text: 'text-purple-400', label: 'Institutional' }
}

function ActionLog() {
  const navigate = useNavigate()
  const [interventions, setInterventions] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [filterLevel, setFilterLevel] = useState('all')
  const [expandedIds, setExpandedIds] = useState(new Set())

  useEffect(() => {
    const fetchInterventions = async () => {
      try {
        const data = await getRecentInterventions(50)
        setInterventions(data)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchInterventions()
  }, [])

  if (loading) {
    return <div className="text-center py-12 text-gray-400">Loading action log...</div>
  }

  if (error) {
    return (
      <div className="bg-accent-danger/10 border border-accent-danger/30 rounded-lg p-4">
        <div className="text-accent-danger">Error: {error}</div>
      </div>
    )
  }

  // Filter interventions
  const filteredInterventions = filterLevel === 'all'
    ? interventions
    : interventions.filter(i => i.level === parseInt(filterLevel))

  const toggleExpanded = (id) => {
    setExpandedIds(prev => {
      const newSet = new Set(prev)
      if (newSet.has(id)) {
        newSet.delete(id)
      } else {
        newSet.add(id)
      }
      return newSet
    })
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white mb-2">Autonomous Action Log</h1>
          <p className="text-gray-400">
            Complete audit trail of all autonomous interventions taken by SaviorAI
          </p>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-dark-card border border-dark-border rounded-lg p-4">
        <div className="flex flex-wrap items-center gap-4">
          <div className="flex items-center space-x-2">
            <label className="text-sm text-gray-400">Filter by level:</label>
            <select
              value={filterLevel}
              onChange={(e) => setFilterLevel(e.target.value)}
              className="bg-dark-bg border border-dark-border rounded px-3 py-1 text-sm text-white"
            >
              <option value="all">All Levels</option>
              <option value="1">Level 1 - Peer Nudge</option>
              <option value="2">Level 2 - Counsellor Alert</option>
              <option value="3">Level 3 - Emergency</option>
              <option value="4">Level 4 - Institutional</option>
            </select>
          </div>

          <div className="ml-auto text-sm text-gray-400">
            Showing {filteredInterventions.length} interventions
          </div>
        </div>
      </div>

      {/* Stats Bar */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[1, 2, 3, 4].map(level => {
          const count = interventions.filter(i => i.level === level).length
          const colors = levelColors[level]
          return (
            <div key={level} className="bg-dark-card border border-dark-border rounded-lg p-4">
              <div className="text-sm text-gray-400 mb-1">{colors.label}</div>
              <div className={`text-2xl font-bold ${colors.text}`}>{count}</div>
            </div>
          )
        })}
      </div>

      {/* Intervention Feed */}
      <div className="space-y-4">
        {filteredInterventions.length === 0 ? (
          <div className="text-center py-12 text-gray-500">No interventions found</div>
        ) : (
          filteredInterventions.map((intervention) => {
            const colors = levelColors[intervention.level] || levelColors[1]
            const isExpanded = expandedIds.has(intervention.id)

            return (
              <div key={intervention.id} className={`
                bg-dark-card border ${colors.bg} border-opacity-30 rounded-lg p-6 transition
              `}>
                {/* Header */}
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-start space-x-4">
                    {/* Level Badge */}
                    <div className={`${colors.bg} ${colors.text} px-4 py-2 rounded-lg text-sm font-bold`}>
                      L{intervention.level}
                    </div>
                    
                    {/* Student Info */}
                    <div>
                      <button
                        onClick={() => navigate(`/student/${intervention.student.id}`)}
                        className="text-white font-semibold hover:text-accent-primary transition"
                      >
                        {intervention.student.name}
                      </button>
                      <div className="text-sm text-gray-400">
                        {intervention.student.batch} • {intervention.student.institution}
                      </div>
                    </div>
                  </div>

                  {/* Timestamp */}
                  <div className="text-xs text-gray-500 text-right">
                    {new Date(intervention.triggered_at).toLocaleString()}
                  </div>
                </div>

                {/* Level Name & Recipient */}
                <div className="flex items-center space-x-4 mb-4 text-sm">
                  <span className={`${colors.text} font-semibold`}>
                    {intervention.level_name}
                  </span>
                  <span className="text-gray-400">→</span>
                  <span className="text-gray-300">
                    Recipient: {intervention.recipient}
                  </span>
                  <span className="text-gray-400">•</span>
                  <span className={`
                    ${intervention.was_acknowledged ? 'text-accent-success' : 'text-gray-500'}
                  `}>
                    {intervention.was_acknowledged ? '✓ Acknowledged' : 'Pending'}
                  </span>
                </div>

                {/* Agent Reasoning (Expandable) */}
                <div className="border-t border-dark-border pt-4 mt-4">
                  <button
                    onClick={() => toggleExpanded(intervention.id)}
                    className="flex items-center text-accent-primary hover:text-accent-primary/80 transition text-sm font-medium"
                  >
                    <svg
                      className={`w-4 h-4 mr-2 transition-transform ${isExpanded ? 'rotate-90' : ''}`}
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                    Agent Reasoning & Message
                  </button>

                  {isExpanded && (
                    <div className="mt-4 space-y-4">
                      {/* Trigger Reason */}
                      <div>
                        <div className="text-xs font-semibold text-gray-400 uppercase mb-2">
                          Trigger Reasoning:
                        </div>
                        <div className="bg-dark-bg rounded p-4 text-sm text-gray-300 leading-relaxed">
                          {intervention.trigger_reason}
                        </div>
                      </div>

                      {/* Action Taken */}
                      <div>
                        <div className="text-xs font-semibold text-gray-400 uppercase mb-2">
                          Action Taken:
                        </div>
                        <div className="text-sm text-gray-300">
                          {intervention.action_taken}
                        </div>
                      </div>

                      {/* Message Sent */}
                      <div>
                        <div className="text-xs font-semibold text-gray-400 uppercase mb-2">
                          Message Sent to {intervention.recipient}:
                        </div>
                        <div className="bg-dark-bg rounded p-4 text-sm text-gray-300 whitespace-pre-line">
                          {intervention.message_sent}
                        </div>
                      </div>

                      {/* Outcome */}
                      <div className="flex items-center space-x-4 text-sm">
                        <span className="text-gray-400">Current Outcome:</span>
                        <span className={`
                          font-semibold
                          ${intervention.outcome === 'recovered' ? 'text-accent-success' :
                            intervention.outcome === 'escalated' ? 'text-accent-danger' :
                            'text-gray-400'}
                        `}>
                          {intervention.outcome.toUpperCase()}
                        </span>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )
          })
        )}
      </div>

      {/* Info Box for Judges */}
      <div className="bg-accent-primary/10 border border-accent-primary/30 rounded-lg p-6">
        <h3 className="text-accent-primary font-semibold mb-2">
          📋 Note
        </h3>
        <p className="text-sm text-gray-300 leading-relaxed">
          This Action Log demonstrates <strong>full autonomous behavior</strong>. Each entry shows:
          <br />• The exact reasoning the AI agent used to decide intervention was needed
          <br />• The specific action taken (peer nudge, counsellor alert, emergency escalation)
          <br />• The actual message content sent to students/counsellors
          <br />• Complete audit trail with timestamps and outcomes
          <br /><br />
          <strong>Expand any entry</strong> to see the full AI reasoning chain. This proves SaviorAI 
          operates autonomously while maintaining complete transparency and human oversight capability.
        </p>
      </div>
    </div>
  )
}

export default ActionLog


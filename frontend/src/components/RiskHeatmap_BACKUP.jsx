// BACKUP - Original RiskHeatmap.jsx
// Saved on 2026-06-14
// Use this to restore if needed

import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

const stateColors = {
  stable: 'bg-accent-success/20 border-accent-success/50 text-accent-success',
  at_risk: 'bg-accent-warning/20 border-accent-warning/50 text-accent-warning',
  crisis: 'bg-accent-danger/20 border-accent-danger/50 text-accent-danger'
}

const stateLabels = {
  stable: 'Stable',
  at_risk: 'At Risk',
  crisis: 'Crisis'
}

const trendIcons = {
  improving: '↗',
  stable: '→',
  declining: '↘'
}

function StudentCard({ student }) {
  const navigate = useNavigate()
  const [isHovered, setIsHovered] = useState(false)
  
  const colorClass = stateColors[student.state] || stateColors.stable
  
  const handleClick = () => {
    navigate(`/student/${student.student_id}`)
  }
  
  const formatDate = (dateStr) => {
    if (!dateStr) return 'Never'
    const date = new Date(dateStr)
    const now = new Date()
    const diffMs = now - date
    const diffMins = Math.floor(diffMs / 60000)
    const diffHours = Math.floor(diffMs / 3600000)
    const diffDays = Math.floor(diffMs / 86400000)
    
    if (diffMins < 60) return `${diffMins}m ago`
    if (diffHours < 24) return `${diffHours}h ago`
    if (diffDays === 1) return 'Yesterday'
    if (diffDays < 7) return `${diffDays}d ago`
    return date.toLocaleDateString()
  }
  
  return (
    <div
      className={`
        ${colorClass} border rounded-lg p-4 cursor-pointer transition-all
        hover:scale-105 hover:shadow-lg relative
      `}
      onClick={handleClick}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {/* Risk Score Badge */}
      <div className="absolute top-2 right-2 text-xs font-bold opacity-50">
        {student.risk_score}
      </div>
      
      {/* Student Info */}
      <div className="mb-2">
        <div className="font-semibold text-white truncate">{student.name}</div>
        <div className="text-xs opacity-70">{student.batch}</div>
      </div>
      
      {/* Status */}
      <div className="flex items-center justify-between text-xs">
        <span className="font-medium">{stateLabels[student.state]}</span>
        <span className="opacity-70">
          {trendIcons[student.trend]} {student.trend}
        </span>
      </div>
      
      {/* Last Check-in */}
      <div className="mt-2 text-xs opacity-60">
        {formatDate(student.last_checkin)}
      </div>
      
      {/* Hover Mini Sparkline (Simplified) */}
      {isHovered && (
        <div className="absolute inset-0 bg-dark-card/95 rounded-lg flex items-center justify-center">
          <div className="text-center p-4">
            <div className="text-sm font-semibold text-white mb-1">
              Risk Score: {student.risk_score}%
            </div>
            <div className="text-xs text-gray-400">
              Click to view full profile
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

function RiskHeatmap({ students }) {
  const [sortBy, setSortBy] = useState('risk')
  const [filterBatch, setFilterBatch] = useState('all')
  
  // Get unique batches
  const batches = ['all', ...new Set(students.map(s => s.batch))].filter(Boolean)
  
  // Sort and filter students
  let filteredStudents = [...students]
  
  // Filter by batch
  if (filterBatch !== 'all') {
    filteredStudents = filteredStudents.filter(s => s.batch === filterBatch)
  }
  
  // Sort
  filteredStudents.sort((a, b) => {
    if (sortBy === 'risk') {
      return b.risk_score - a.risk_score
    } else if (sortBy === 'batch') {
      return a.batch.localeCompare(b.batch)
    } else if (sortBy === 'checkin') {
      if (!a.last_checkin) return 1
      if (!b.last_checkin) return -1
      return new Date(b.last_checkin) - new Date(a.last_checkin)
    }
    return 0
  })
  
  return (
    <div className="space-y-4">
      {/* Controls */}
      <div className="flex flex-wrap gap-4 items-center bg-dark-card border border-dark-border rounded-lg p-4">
        <div className="flex items-center space-x-2">
          <label className="text-sm text-gray-400">Sort by:</label>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="bg-dark-bg border border-dark-border rounded px-3 py-1 text-sm text-white"
          >
            <option value="risk">Risk Level</option>
            <option value="batch">Batch</option>
            <option value="checkin">Last Check-in</option>
          </select>
        </div>
        
        <div className="flex items-center space-x-2">
          <label className="text-sm text-gray-400">Batch:</label>
          <select
            value={filterBatch}
            onChange={(e) => setFilterBatch(e.target.value)}
            className="bg-dark-bg border border-dark-border rounded px-3 py-1 text-sm text-white"
          >
            {batches.map(batch => (
              <option key={batch} value={batch}>
                {batch === 'all' ? 'All Batches' : batch}
              </option>
            ))}
          </select>
        </div>
        
        <div className="ml-auto text-sm text-gray-400">
          Showing {filteredStudents.length} students
        </div>
      </div>
      
      {/* Student Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filteredStudents.map((student) => (
          <StudentCard key={student.student_id} student={student} />
        ))}
      </div>
      
      {filteredStudents.length === 0 && (
        <div className="text-center py-12 text-gray-500">
          No students found
        </div>
      )}
    </div>
  )
}

export default RiskHeatmap

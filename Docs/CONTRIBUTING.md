# Contributing to SaviorAI

Thank you for your interest in contributing to SaviorAI! Every contribution helps us get closer to preventing student suicides.

## 🎯 Mission-Aligned Contributions

SaviorAI exists to **save lives**, not optimize engagement metrics. All contributions should align with this mission:

✅ **Good:** Better burnout detection, cultural adaptation, privacy improvements  
❌ **Not aligned:** Monetization features, data selling, surveillance expansion

---

## 🛠️ Areas for Contribution

### 1. **Agent Intelligence Improvements**
- **HMM refinement:** Better transition probabilities from real student data
- **Adversarial detection:** Additional gaming patterns (e.g., AI-generated responses)
- **Cohort patterns:** Semester-specific, exam-season specific triggers
- **Feedback loops:** How to learn from intervention outcomes

### 2. **Cultural Adaptation**
- **Japan-specific features:** LINE integration, exam season patterns, parent portals
- **Language support:** Hindi, Tamil, Telugu, Bengali, Japanese
- **Cultural sensitivity:** Region-specific stigma handling, collectivist vs individualist messaging

### 3. **Technical Infrastructure**
- **Performance:** Query optimization, caching strategies
- **Security:** GDPR/DPDPA compliance, encryption at rest, audit logs
- **Testing:** Unit tests, integration tests, E2E demo scenarios
- **Documentation:** API docs, deployment guides, troubleshooting

### 4. **Research Validation**
- **Outcome studies:** Does early detection actually prevent crises?
- **False positive rates:** How often does the agent cry wolf?
- **Counsellor feedback:** What do real mental health professionals need?

---

## 🔄 Development Workflow

### Setup Development Environment

```bash
# Fork the repo on GitHub, then clone your fork
git clone https://github.com/YOUR-USERNAME/SaviorAI.git
cd SaviorAI

# Create a feature branch
git checkout -b feature/your-feature-name

# Backend setup
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r backend/requirements.txt

# Frontend setup
cd frontend
npm install
cd ..

# Copy environment template
cp .env.example .env
# Fill in your API keys
```

### Making Changes

1. **Write code** following existing patterns
2. **Test locally** with demo scenarios
3. **Update documentation** if APIs change
4. **Commit with clear messages:**
   ```bash
   git commit -m "feat: Add LINE messenger integration for Japan deployment"
   ```

### Commit Message Convention

Use semantic commit messages:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation only
- `refactor:` Code restructuring without behavior change
- `test:` Adding or updating tests
- `perf:` Performance improvement
- `chore:` Maintenance tasks

### Pull Request Process

1. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request** on GitHub
   - Title: Clear, specific description
   - Description: What changed, why, how to test
   - Link to any related issues

3. **Code Review:**
   - Maintainer will review within 48 hours
   - Address feedback promptly
   - Keep discussion respectful

4. **Merge:**
   - After approval, maintainer will merge
   - Your contribution is now part of SaviorAI!

---

## 🧪 Testing Your Changes

### Run Demo Scenarios

```bash
# Reset database
python backend/utils/demo_runner.py --scenario reset

# Setup test data
python backend/utils/demo_runner.py --scenario setup

# Run live simulation
python backend/utils/demo_runner.py --scenario live

# Verify dashboard loads
# Open http://localhost:3000
# Set localStorage institutionId (printed in setup)
# Check that your changes work correctly
```

### Manual Testing Checklist

- [ ] Backend starts without errors
- [ ] Frontend compiles and loads
- [ ] Demo setup creates 50 students
- [ ] Risk scores display correctly (crisis = 85-95%)
- [ ] Student profile timeline renders
- [ ] Interventions show agent reasoning
- [ ] No console errors in browser

### Unit Tests (TODO)

```bash
# Backend tests (once implemented)
pytest backend/tests/

# Frontend tests (once implemented)
cd frontend
npm test
```

---

## 📋 Code Style

### Python (Backend)

- **PEP 8** formatting
- **Type hints** on all function signatures
- **Async/await** for database operations
- **Docstrings** for classes and complex functions

Example:
```python
async def assess_burnout(
    student_id: UUID,
    recent_scores: List[int],
    db: AsyncSession
) -> BurnoutAssessment:
    """
    Run full HMM burnout assessment for a student.
    
    Args:
        student_id: UUID of student to assess
        recent_scores: List of mood scores (1-5)
        db: Database session
    
    Returns:
        BurnoutAssessment with state, probability, reasoning
    """
    hmm = BurnoutHMM()
    return hmm.assess(recent_scores)
```

### JavaScript (Frontend)

- **ESLint** rules (defined in `.eslintrc`)
- **Functional components** with hooks
- **Tailwind CSS** for styling (avoid custom CSS)
- **Clear prop types**

Example:
```javascript
function StudentCard({ student, onClick }) {
  const riskColor = {
    stable: 'bg-green-500',
    at_risk: 'bg-yellow-500',
    crisis: 'bg-red-500'
  }[student.state]
  
  return (
    <div 
      className={`${riskColor} rounded-lg p-4 cursor-pointer`}
      onClick={() => onClick(student.id)}
    >
      <h3 className="font-bold">{student.name}</h3>
      <p className="text-sm">Risk: {student.risk_score}%</p>
    </div>
  )
}
```

---

## 🔐 Security Guidelines

### Sensitive Data
- **Never commit API keys** (use `.env`, add to `.gitignore`)
- **Never log passwords** or tokens
- **Never expose student PII** in error messages

### Database Queries
- **Always use parameterized queries** (SQLAlchemy ORM handles this)
- **Never concatenate user input** into SQL strings
- **Sanitize phone numbers** before database lookups

### API Endpoints
- **Validate all inputs** (FastAPI Pydantic models)
- **Rate limit webhooks** (prevent DDoS)
- **Authenticate dashboard** (API key required)

---

## 🌍 Cultural Sensitivity

SaviorAI operates in sensitive contexts. When contributing:

### Language & Tone
- **Never use clinical labels** ("depression", "mental illness") in student-facing messages
- **Avoid surveillance language** ("monitoring", "tracking", "watching")
- **Keep peer nudges warm and casual**, like a caring friend checking in
- **Counsellor alerts professional but empathetic**

### Privacy
- **Minimize data collection:** Only essential check-in data
- **Aggregate for cohort alerts:** No individual names in institutional reports
- **Consent-first:** Students must opt in explicitly

### Regional Adaptation
- **India:** WhatsApp-first, English + regional languages, exam season awareness
- **Japan:** LINE integration, examination hell patterns, parent-teacher portals
- **US/Europe:** SMS fallback, FERPA/GDPR compliance, campus-specific triggers

---

## 📚 Helpful Resources

### Research Papers
- [Maslach Burnout Inventory](https://www.mindgarden.com/117-maslach-burnout-inventory)
- [Schaufeli & Leiter (2000) Burnout Progression](https://doi.org/10.1080/135943200750035358)
- [NIMHANS Student Wellness Study](https://nimhans.ac.in/)

### Technical Documentation
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Twilio WhatsApp API](https://www.twilio.com/docs/whatsapp)
- [OpenAI GPT-4 API](https://platform.openai.com/docs/)
- [React Hooks Guide](https://react.dev/reference/react)

### Related Projects
- [Crisis Text Line](https://www.crisistextline.org/) — Human-powered crisis intervention
- [Wysa](https://www.wysa.io/) — AI mental health chatbot (not autonomous)
- [Talkspace](https://www.talkspace.com/) — Teletherapy platform

---

## ❓ Questions?

- **Technical issues:** [Open an issue](https://github.com/yourusername/SaviorAI/issues)
- **Feature ideas:** [Start a discussion](https://github.com/yourusername/SaviorAI/discussions)
- **Security concerns:** Email security@SaviorAI.dev (do not open public issue)

---

## 🙏 Thank You

Every commit, every bug fix, every feature brings us closer to zero student suicides.

**You're not just writing code. You're saving lives.**


# Gravitas Vault: Scaling Strategy & Migration Path

**Date:** 2026-01-08  
**Author:** Dan Flory + Antigravity  
**Purpose:** Long-term scaling plan for code-server vault from 50 → 10,000+ users  
**Related:** [Feasibility Study](../feasibility/code-oss-browser-vault.md)

---

## Executive Summary

The Gravitas Vault architecture (code-server in browser) scales from **50 to 10,000+ users** with **gradual infrastructure upgrades**, not major rewrites. Each scaling tier adds capability without breaking existing functionality.

**Key Insight:** Start simple, scale incrementally as revenue grows.

---

## Scaling Tiers Overview

| Tier | User Count | Infrastructure | Monthly Cost | Engineering Effort |
|------|------------|----------------|--------------|-------------------|
| **Bootstrap** | 1-50 | Your workstation + AWS spot | $10-20 | 5 weeks (initial build) |
| **Startup** | 50-500 | + Redis, Load Balancer | $100-200 | +1-2 weeks |
| **Growth** | 500-2,000 | + Kubernetes, S3 storage | $500-2,000 | +4-6 weeks |
| **Scale** | 2,000-10,000 | + Multi-region, CDN | $2,000-10,000 | +8-12 weeks |
| **Enterprise** | 10,000+ | + Full SRE team | $10,000+ | Ongoing team |

---

## Tier 1: Bootstrap (1-50 Users)

### Target Timeline
**Months 1-3:** MVP launch with first cohort

### Architecture
```
┌──────────────────────────────────────┐
│  Your Workstation (Dan's PC)         │
│  - Nginx router                      │
│  - 10 local code-server instances   │
│  - User vault storage (local SSD)   │
└──────────────┬───────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│  AWS Spot Instances (overflow)       │
│  - Auto-spawn when >10 users         │
│  - $0.015/hour per instance          │
│  - NFS mount to your workstation     │
└──────────────────────────────────────┘
```

### Components
- **Router:** Single nginx on your PC
- **Sessions:** In-memory tracking
- **Storage:** Local filesystem (`/gravitas/vaults/`)
- **Overflow:** AWS EC2 spot instances
- **Monitoring:** Basic logs + htop

### Capacity
- **Local:** 10 concurrent users
- **Cloud burst:** Unlimited (cost-limited)
- **Peak handling:** 50 users at 20% concurrency

### Monthly Cost
- **Infrastructure:** $0 (your hardware)
- **Cloud overflow:** $10-20 (occasional spikes)
- **Total:** **~$20/month**

### What Works
✅ Perfect for beta testing  
✅ Proves the concept  
✅ Minimal operating costs  
✅ Fast iteration

### What Breaks
❌ Your workstation goes down = everyone down  
❌ Your internet is the bottleneck  
❌ No redundancy/backup

### Success Metrics
- 50 active users
- <5 second vault load time
- 99% uptime (manual monitoring)

---

## Tier 2: Startup (50-500 Users)

### Target Timeline
**Months 4-9:** Product-market fit validated

### Architecture Changes
```diff
+ AWS Application Load Balancer (ALB)
+ Redis (session management)
+ Daily automated backups
+ CloudWatch monitoring
- In-memory session tracking
```

### New Components
1. **Redis Cluster**
   - Tracks which user is on which instance
   - Shared session state
   - Auto-failover support

2. **AWS ALB**
   - Replaces nginx for routing
   - SSL termination
   - Health checks on instances

3. **Automated Backups**
   - Daily snapshot of `/gravitas/vaults/`
   - S3 storage for 30-day retention

4. **Monitoring**
   - CloudWatch dashboards
   - Alerts on >80% capacity
   - Usage analytics

### Migration Steps
1. **Week 1:** Set up Redis (ElastiCache)
2. **Week 2:** Configure ALB, migrate routing
3. **Week 3:** Implement backup automation
4. **Week 4:** Test failover scenarios

### Capacity
- **Local:** Still 10 concurrent
- **Cloud burst:** 50-100 concurrent
- **Peak handling:** 500 users at 20% concurrency

### Monthly Cost
- **Redis:** $30-50
- **ALB:** $20-30
- **S3 backups:** $10-20
- **Cloud instances:** $50-100
- **Total:** **~$150/month**

### Engineering Effort
- **Time:** 1-2 weeks
- **Difficulty:** Low-Medium
- **Team size:** 1 developer (you)

### Success Metrics
- 500 active users
- <3 second vault load time
- 99.5% uptime
- Automated alerting working

---

## Tier 3: Growth (500-2,000 Users)

### Target Timeline
**Months 10-18:** Revenue justifies infrastructure investment

### Architecture Changes
```diff
+ Kubernetes cluster (EKS/GKE)
+ S3 as primary vault storage
+ Multiple router instances
+ Auto-scaling code-server pools
- Your workstation as primary
- NFS mounts from cloud to local
```

### New Components

1. **Kubernetes (Managed - EKS/GKE)**
   - Auto-scales code-server pods
   - Rolling updates, zero downtime
   - Container-based isolation

2. **S3 + CloudFront**
   - Vaults stored in S3
   - S3FS mounts in code-server
   - CloudFront CDN for static assets

3. **Pre-warmed Pool**
   - Keep 10-20 idle code-server pods ready
   - <2 second user connection time
   - Scales 0→100 in 1 minute

4. **Database (RDS PostgreSQL)**
   - User metadata
   - Session tracking (replace Redis)
   - Vault permissions/sharing

### Migration Steps
1. **Phase 1 (2 weeks):** Set up Kubernetes cluster
2. **Phase 2 (2 weeks):** Migrate vaults to S3
3. **Phase 3 (1 week):** Deploy code-server to K8s
4. **Phase 4 (1 week):** Cutover traffic, parallel run
5. **Phase 5 (1 week):** Retire workstation as primary

### Capacity
- **Kubernetes:** 100+ concurrent pods
- **No local dependency**
- **Peak handling:** 2,000 users at 30% concurrency

### Monthly Cost
- **EKS cluster:** $73 (control plane)
- **EC2 nodes (5x m5.xlarge):** $500-800
- **S3 storage (10TB):** $230
- **RDS PostgreSQL:** $100-200
- **CloudFront:** $50-100
- **Total:** **~$1,200/month**

### Engineering Effort
- **Time:** 4-6 weeks
- **Difficulty:** Medium-High
- **Team size:** 1-2 developers

### Success Metrics
- 2,000 active users
- <2 second vault load time
- 99.9% uptime
- Automated scaling working
- Cost per user <$1/month

---

## Tier 4: Scale (2,000-10,000 Users)

### Target Timeline
**Months 19-36:** Established product, growing user base

### Architecture Changes
```diff
+ Multi-region deployment
+ Global load balancing
+ Distributed tracing
+ Dedicated SRE engineer
+ Premium tier (dedicated resources)
```

### New Components

1. **Multi-Region**
   - US-East, US-West, EU-Central
   - Route users to nearest region
   - <100ms latency worldwide

2. **Observability Stack**
   - Prometheus + Grafana
   - Distributed tracing (Jaeger)
   - Log aggregation (ELK stack)
   - On-call rotation

3. **Premium Tier**
   - Dedicated m5.2xlarge instances
   - Guaranteed availability
   - Higher resource limits
   - $20-50/month per user

4. **Security Hardening**
   - WAF (Web Application Firewall)
   - DDoS protection
   - Security audits
   - Compliance (SOC2, GDPR)

### Capacity
- **Global:** 500+ concurrent per region
- **Peak handling:** 10,000 users at 40% concurrency
- **Premium users:** Isolated, no resource contention

### Monthly Cost
- **Infrastructure (3 regions):** $3,000-5,000
- **Monitoring/logging:** $500-1,000
- **Security/compliance:** $1,000-2,000
- **Total:** **~$6,000/month**
- **Revenue:** ~$50,000/month (assuming $5/user avg)

### Engineering Effort
- **Time:** 8-12 weeks
- **Difficulty:** High
- **Team size:** 2-3 developers + 1 SRE

### Success Metrics
- 10,000 active users
- <1 second vault load time (globally)
- 99.95% uptime
- <0.1% error rate
- Profit margin >80%

---

## Tier 5: Enterprise (10,000+ Users)

### Target Timeline
**Year 3+:** Market leader

### Architecture Changes
```diff
+ Dedicated infrastructure team
+ Custom K8s operators
+ Advanced caching strategies
+ Enterprise support contracts
+ White-label partnerships
```

### Organizational Changes
- **Team:** 5-10 engineers (backend, frontend, SRE, security)
- **On-call:** 24/7 rotation
- **Process:** Formal change management, incident response
- **Budget:** Engineering + infrastructure controlled separately

### Advanced Features
1. **Custom Workspace Images**
   - Pre-configured environments per team
   - Language/framework templates
   - Customer-branded vaults

2. **Advanced Collaboration**
   - Live sharing (VS Code Live Share integration)
   - Team workspaces
   - Admin dashboards

3. **Enterprise Integrations**
   - SSO (SAML, OIDC)
   - LDAP/Active Directory
   - Slack/Teams notifications
   - Jira/GitHub integrations

### Capacity
- **Unlimited** (auto-scaling infrastructure)
- **Multi-cloud** (AWS + GCP + Azure backups)

### Monthly Cost
- **Variable:** $10,000-100,000+ (scales with users)
- **Per-user cost drops:** $0.50-$1.00/user at scale

---

## Cost Per User Analysis

| Tier | Users | Monthly Cost | Cost/User |
|------|-------|--------------|-----------|
| Bootstrap | 50 | $20 | $0.40 |
| Startup | 500 | $150 | $0.30 |
| Growth | 2,000 | $1,200 | $0.60 |
| Scale | 10,000 | $6,000 | $0.60 |
| Enterprise | 50,000 | $30,000 | $0.60 |

**Insight:** Cost per user stabilizes at **$0.50-$0.60** after Growth tier.

---

## What Stays Constant (Never Re-Engineer)

Throughout all tiers, these **core components remain unchanged**:

✅ **User vault structure** (Public/SharedBy/Groups/User folders)  
✅ **code-server as editor** (just deploy differently)  
✅ **Chat integration architecture** (WebSocket to backend)  
✅ **Authentication flow** (Lobby → Hallway → Vault)  
✅ **Agent system** (chatTwins, routing logic)  

**You're building the RIGHT foundation from day one.**

---

## Migration Risk Assessment

| Transition | Risk Level | Why | Mitigation |
|------------|------------|-----|------------|
| Tier 1→2 | 🟢 Low | Additive only | Parallel run both systems |
| Tier 2→3 | 🟡 Medium | Storage migration | Gradual vault-by-vault move |
| Tier 3→4 | 🟢 Low | Replication | Multi-region staged rollout |
| Tier 4→5 | 🟢 Low | Organizational | Hire before you need |

**Key:** No "big bang" rewrites required.

---

## Decision Points (When to Upgrade)

### Tier 1 → Tier 2
**Triggers:**
- Your workstation downtime affects users
- Support requests about "slow vault access"
- >30 daily active users consistently

**Time to decide:** Month 3-4

### Tier 2 → Tier 3
**Triggers:**
- Redis hits memory limits (>300 sessions)
- AWS costs >$500/month (spot instance overflow)
- Customer requests enterprise features

**Time to decide:** Month 8-12

### Tier 3 → Tier 4
**Triggers:**
- Users complain about latency (EU/Asia)
- Revenue >$20k/month (justifies multi-region)
- Compliance requirements (data sovereignty)

**Time to decide:** Month 18-24

### Tier 4 → Tier 5
**Triggers:**
- Enterprise sales pipeline (>$100k contracts)
- Need 99.99% SLA guarantees
- White-label partnership opportunities

**Time to decide:** Year 2-3

---

## Financial Model

### Revenue Assumptions

| Tier | Users | Avg $/User/Mo | Monthly Revenue | Profit Margin |
|------|-------|---------------|----------------|---------------|
| Bootstrap | 50 | $0 (beta) | $0 | N/A |
| Startup | 500 | $2 | $1,000 | 85% ($850) |
| Growth | 2,000 | $5 | $10,000 | 88% ($8,800) |
| Scale | 10,000 | $7 | $70,000 | 91% ($64,000) |
| Enterprise | 50,000 | $10 | $500,000 | 94% ($470,000) |

**Key Insight:** Infrastructure scales linearly, revenue scales superlinearly.

---

## Technology Choices (Future-Proof)

### What We're Using
- **Container:** Docker (✅ industry standard)
- **Orchestration:** Kubernetes (✅ cloud-agnostic)
- **Storage:** S3-compatible (✅ portable to MinIO/Ceph)
- **Database:** PostgreSQL (✅ scales to billions of rows)
- **Cache:** Redis (✅ standard for sessions)

### Why This Stack Scales
- ✅ No vendor lock-in (can move AWS→GCP→Azure)
- ✅ Open-source foundation (no licensing surprises)
- ✅ Massive community (hire talent easily)
- ✅ Battle-tested (used by companies 100x your scale)

---

## Key Takeaways

1. **Start Simple:** Your workstation + AWS spot = perfect for 50 users
2. **Scale Gradually:** Each tier is 4-12 weeks of work, not months
3. **No Rewrites:** Core architecture stays constant
4. **Revenue First:** Upgrade when revenue justifies cost
5. **Profit Margins:** 85-95% throughout (infrastructure is cheap!)

---

## Next Steps

### Immediate (Now)
- ✅ Build Tier 1 architecture (5 weeks)
- ✅ Launch with 10-50 beta users
- ✅ Validate product-market fit

### Short-term (Months 3-6)
- Monitor usage patterns
- Identify bottlenecks
- Plan Tier 2 migration if needed

### Long-term (Year 1+)
- Revisit this plan quarterly
- Adjust based on actual growth
- Hire when revenue supports it

---

## Conclusion

The Gravitas Vault architecture scales from **50 to 10,000+ users** without fundamental redesign. Each tier builds on the previous one, maintaining the core user experience while adding infrastructure as needed.

**You're building for scalability from day one, but paying only for what you need today.**

---

## Appendix: Quick Reference

### When to Upgrade Checklist

- [ ] Current tier hitting 80% capacity consistently
- [ ] User complaints about performance
- [ ] Revenue supports next tier costs
- [ ] Team bandwidth available for migration

### Red Flags (Don't Upgrade Yet)

- ⚠️ <50% capacity utilization
- ⚠️ Churn rate >10% (fix product first)
- ⚠️ Revenue doesn't cover 3x next tier costs
- ⚠️ No engineering bandwidth for 4+ week project

---

**Document Version:** 1.0  
**Last Updated:** 2026-01-08  
**Next Review:** 2026-04-08 (after 3 months operation)

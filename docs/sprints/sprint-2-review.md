# Sprint 2 – Review  
**Date:** November 13 , 2025  

## Sprint Goal  
Deploy working web app connected to Yale and New Haven event feeds.  

✅ Goal partially achieved: deployment successful with live feed integration, but search and calendar features not yet functional.  

**Deployed URL:** https://yale-events-aggregator.onrender.com  

## Completed User Stories  
| ID | Title | Story Points | Notes |
|:--:|:--|:--:|:--|
| #7 | Event Source API Integration | 8 | Successfully connected Yale + NHV feeds. Verified JSON output and database updates. |
| #1 | Unified Event Feed Display | 5 | Frontend renders real-time data with basic pagination. |
| #8 | Responsive Web UI | 3 | Mobile and desktop layouts validated through browser testing. |

**Screenshots:** see README or staging demo.  

## Incomplete Stories  
| ID | Title | Reason | Disposition |
|:--:|:--|:--|:--|
| #3 | Keyword Search | API query parameter parsing not implemented | Carry over to Sprint 3 |
| #4 | Date Filter | Frontend logic requires moment.js or custom parser | Carry over |
| #5 | Add to Calendar (.ics) | Calendar export library not integrated | Carry over |
| #6 | More Info Link | Some events lack URL fields | Fix in Sprint 3 |
| #14 | Personalized Recommendation Prototype | Out of scope for Sprint 2 | Drop until MVP complete |

## Metrics  
- **Planned Story Points:** 32  
- **Completed Story Points:** 16  
- **Velocity:** 16 points / sprint  
- **Completion Rate:** 50 %  

## Lessons Learned  
- Yale and NHV feeds have inconsistent HTML structure → need more robust parser.  
- Deployment to Render was smooth and stable.  
- One-week iteration felt tight; backend stabilization should precede UI expansion.  

## Product Backlog Updates  
- Carry over #3, #4, #5, #6 to Sprint 3.  
- Add new task: implement feed deduplication logic (#19).  
- Plan for search and calendar integration testing in next sprint. 
